import os
import streamlit as st
import datetime
import plotly.express as px
import pandas as pd
from pyowm import OWM

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Prévision Production Solaire",
    page_icon="☀️",
    layout="wide",
)

# Récupération des variables d'environnement (configurations de l'addon)
latitude = 48.831923130095056
longitude = 2.5716759068377257
api_key = "ec6051d6d6c6360fbb75fb737bcef45f"

# Input pour la puissance des panneaux
panel_power = st.number_input('Puissance des panneaux solaires (W)', min_value=1, value=1000)
efficiency = 0.2  # Efficacité des panneaux (20%)
    
def main():
    st.title("☀️ Prévision de Production Solaire")
    
    # Affichage des informations de configuration
    with st.expander("Configuration"):
        st.write(f"Latitude: {latitude}")
        st.write(f"Longitude: {longitude}")
        st.write(f"Puissance des panneaux: {panel_power} W")
        st.write(f"Efficacité: {efficiency * 100}%")
    
    # Puissance effective des panneaux
    power_effective = panel_power * efficiency
    
    # Inputs pour les heures (remplacer par une sélection plus simple)
    col1, col2 = st.columns(2)
    with col1:
        start_time = st.time_input('Heure de début', datetime.time(8, 0), key="start_time")
    with col2:
        end_time = st.time_input('Heure de fin', datetime.time(18, 0), key="end_time")
    
    # Option pour afficher les données automatiquement au chargement
    auto_fetch = st.checkbox("Mettre à jour automatiquement", value=True)
    
    # Bouton pour rafraîchir les données
    fetch_data = st.button("Rafraîchir les données") or auto_fetch
    
    if fetch_data:
        if not api_key:
            st.error("Clé API OpenWeatherMap non configurée dans les options de l'addon.")
            st.info("Veuillez configurer l'addon dans les paramètres de Home Assistant.")
        else:
            try:
                owm = OWM(api_key)
                mgr = owm.weather_manager()
                
                # Créer un conteneur pour afficher la progression
                status_container = st.empty()
                status_container.info("Récupération des données météorologiques...")
                
                # Obtenir les données météo actuelles
                observation = mgr.weather_at_coords(latitude, longitude)
                w = observation.weather
                
                # Mise à jour du statut
                status_container.info("Récupération des prévisions...")
                
                # Calculer les heures de lever et coucher du soleil
                sunrise_unix = w.sunrise_time()
                sunset_unix = w.sunset_time()
                
                # Convertir en datetime
                sunrise_datetime = datetime.datetime.fromtimestamp(sunrise_unix)
                sunset_datetime = datetime.datetime.fromtimestamp(sunset_unix)
                
                # Créer un tableau pour les informations actuelles
                current_info = {
                    "Température": f"{w.temperature('celsius')['temp']}°C",
                    "Conditions": w.detailed_status.capitalize(),
                    "Humidité": f"{w.humidity}%",
                    "Vitesse du vent": f"{w.wind()['speed']} m/s",
                    "Lever du soleil": sunrise_datetime.strftime('%H:%M'),
                    "Coucher du soleil": sunset_datetime.strftime('%H:%M'),
                    "Taux d'ensoleillement": f"{100 - w.clouds}%",
                    "Puissance instantanée": f"{power_effective * (100 - w.clouds) / 100:.2f} W"
                }
                
                # Afficher les informations en colonnes
                st.subheader("Conditions météorologiques actuelles")
                cols = st.columns(4)
                for i, (key, value) in enumerate(current_info.items()):
                    cols[i % 4].metric(key, value)
                
                # Obtenir les prévisions
                forecast = mgr.forecast_at_coords(latitude, longitude, '3h', limit=8)
                
                # Utiliser la date actuelle
                current_date = datetime.datetime.now().date()
                
                # Créer les objets datetime pour start et end time
                start_datetime = datetime.datetime.combine(current_date, start_time)
                end_datetime = datetime.datetime.combine(current_date, end_time)
                
                # Vérifier si la plage s'étend sur deux jours
                if end_time < start_time:
                    next_day = current_date + datetime.timedelta(days=1)
                    end_datetime = datetime.datetime.combine(next_day, end_time)
                
                # Créer un DataFrame pour les données de prévision
                data = []
                
                # Mise à jour du statut
                status_container.info("Traitement des données...")
                
                # Traiter les prévisions
                for weather in forecast.forecast:
                    # Obtenir le timestamp Unix et convertir en datetime
                    timestamp_unix = weather.reference_time()
                    timestamp_datetime = datetime.datetime.fromtimestamp(timestamp_unix)
                    
                    # Obtenir le taux de nuages et calculer la production
                    clouds_percent = weather.clouds
                    sunshine_factor = (100 - clouds_percent) / 100
                    production = power_effective * sunshine_factor
                    
                    # Vérifier si c'est pendant la journée (entre lever et coucher du soleil)
                    time_only = timestamp_datetime.time()
                    is_daytime = sunrise_datetime.time() <= time_only <= sunset_datetime.time()
                    
                    # Vérifier si dans la plage horaire spécifiée
                    in_time_range = False
                    
                    # Si c'est le même jour
                    if start_time <= end_time:
                        in_time_range = start_time <= time_only <= end_time
                    # Si la plage s'étend sur deux jours
                    else:
                        in_time_range = time_only >= start_time or time_only <= end_time
                    
                    # Déterminer si ce point est dans la plage sélectionnée
                    selected = in_time_range and is_daytime
                    
                    # Ajouter au DataFrame
                    data.append({
                        'timestamp': timestamp_datetime,
                        'production': production,
                        'selected': selected,
                        'clouds': clouds_percent,
                        'température': weather.temperature('celsius')['temp']
                    })
                
                # Effacer le message de statut
                status_container.empty()
                
                # Créer le DataFrame
                df = pd.DataFrame(data)
                
                # Vérifier si nous avons des données
                if df.empty:
                    st.warning("Aucune donnée de prévision disponible.")
                else:
                    # Calculer la production totale (en kWh)
                    selected_data = df[df['selected']]
                    total_production = selected_data['production'].sum() * 3 / 1000  # Convertir en kWh (prévisions sur 3h)
                    
                    # Afficher la production totale estimée
                    st.subheader("Production solaire estimée")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Production totale estimée", 
                            f"{total_production:.2f} kWh",
                            f"Sur {len(selected_data) * 3} heures"
                        )
                    with col2:
                        st.metric(
                            "Puissance moyenne", 
                            f"{selected_data['production'].mean():.2f} W" if not selected_data.empty else "0 W",
                            f"{selected_data['production'].max() - selected_data['production'].mean():.2f} W (max)"
                        )
                    
                    # Créer le graphique avec pandas et plotly
                    st.subheader("Graphique de production")
                    
                    # Personnaliser l'apparence du graphique
                    fig = px.line(
                        df, 
                        x='timestamp', 
                        y='production', 
                        labels={'timestamp': 'Heure', 'production': 'Production (W)'},
                        title="Prévision de production solaire",
                        color_discrete_sequence=['#0078D7']
                    )
                    
                    fig.update_layout(
                        xaxis_title="Heure",
                        yaxis_title="Production (W)",
                        plot_bgcolor='rgba(240,240,240,0.8)',
                        hovermode='x unified'
                    )
                    
                    # Ajouter les points sélectionnés en évidence
                    if not selected_data.empty:
                        fig.add_scatter(
                            x=selected_data['timestamp'], 
                            y=selected_data['production'], 
                            mode='markers', 
                            name='Période sélectionnée', 
                            marker=dict(size=10, color='#E74C3C')
                        )
                    
                    # Zones pour le début et la fin
                    fig.add_vrect(
                        x0=start_datetime,
                        x1=start_datetime + datetime.timedelta(minutes=30),
                        fillcolor="green",
                        opacity=0.3,
                        layer="below",
                        line_width=0,
                        annotation_text="Début",
                        annotation_position="top left"
                    )
                    
                    fig.add_vrect(
                        x0=end_datetime - datetime.timedelta(minutes=30),
                        x1=end_datetime,
                        fillcolor="red",
                        opacity=0.3,
                        layer="below",
                        line_width=0,
                        annotation_text="Fin",
                        annotation_position="top left"
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tableau des données détaillées
                    st.subheader("Détails des prévisions")
                    df_display = df.copy()
                    df_display['timestamp'] = df_display['timestamp'].dt.strftime('%d/%m %H:%M')
                    df_display['production'] = df_display['production'].round(2).astype(str) + ' W'
                    df_display['clouds'] = df_display['clouds'].astype(str) + '%'
                    df_display['température'] = df_display['température'].round(1).astype(str) + '°C'
                    df_display.rename(columns={
                        'timestamp': 'Heure',
                        'production': 'Production',
                        'clouds': 'Couverture nuageuse',
                        'température': 'Température'
                    }, inplace=True)
                    df_display.drop(columns=['selected'], inplace=True)
                    st.dataframe(df_display, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Erreur lors de la récupération des données: {str(e)}")
                st.exception(e)
    
    # Pied de page
    st.markdown("---")
    st.markdown(
        "**Solar Forecast Addon** | "
        "Données fournies par [OpenWeatherMap](https://openweathermap.org/) | "
        "Intégré avec [Home Assistant](https://www.home-assistant.io/)"
    )

if __name__ == "__main__":
    main()

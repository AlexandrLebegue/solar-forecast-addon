#!/usr/bin/with-contenv bashio

# Récupération des configurations
LATITUDE=$(bashio::config 'latitude')
LONGITUDE=$(bashio::config 'longitude')
API_KEY=$(bashio::config 'api_key')
PANEL_POWER=$(bashio::config 'panel_power')
EFFICIENCY=$(bashio::config 'efficiency')

# Exportation des variables d'environnement pour l'application
export LATITUDE=${LATITUDE}
export LONGITUDE=${LONGITUDE}
export API_KEY=${API_KEY}
export PANEL_POWER=${PANEL_POWER}
export EFFICIENCY=${EFFICIENCY}

# Lancement de Streamlit
exec streamlit run /app/app.py 
    # --server.address 0.0.0.0 \
    # --server.port 8501 \
    # --server.baseUrlPath="{{ingress_entry}}" \
    # --server.enableCORS=false \
    # --server.enableWebsocketCompression=false

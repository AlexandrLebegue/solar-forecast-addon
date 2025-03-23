# Home Assistant Add-on: Example add-on

## How to use

This add-on really does nothing. It is just an example.

When started it will print the configured message or "Hello world" in the log.

It will also print "All done!" in `/share/example_addon_output.txt` to show
simple example of the usage of `map` in addon config.
# Addon Home Assistant : Prévision de Production Solaire

Cet addon permet de prévoir la production d'énergie de vos panneaux solaires en fonction des données météorologiques d'OpenWeatherMap. Il affiche des graphiques et des statistiques pour vous aider à optimiser votre consommation énergétique.

## Fonctionnalités

- Affichage des conditions météorologiques actuelles
- Prévision de production solaire sur les prochaines 24 heures
- Estimation de la production totale d'énergie pour une période spécifique
- Graphique interactif de la production prévue
- Tableau détaillé des prévisions

## Installation

1. Dans Home Assistant, naviguez vers **Paramètres** → **Addons** → **Boutique d'add-ons**
2. Cliquez sur les trois points en haut à droite et sélectionnez **Dépôts**
3. Ajoutez l'URL de ce dépôt et cliquez sur **Ajouter**
4. Cherchez "Solar Production Forecast" dans la liste des addons disponibles
5. Cliquez sur l'addon et sur **Installer**

## Configuration

Après l'installation, vous devrez configurer l'addon avec les paramètres suivants :

| Paramètre | Description |
|-----------|-------------|
| `latitude` | Latitude de l'emplacement de vos panneaux solaires |
| `longitude` | Longitude de l'emplacement de vos panneaux solaires |
| `api_key` | Clé API OpenWeatherMap (gratuite) |
| `panel_power` | Puissance totale de vos panneaux solaires en Watts |
| `efficiency` | Efficacité de vos panneaux (entre 0.01 et 1) |

### Obtenir une clé API OpenWeatherMap

1. Créez un compte sur [OpenWeatherMap](https://openweathermap.org/)
2. Naviguez vers votre profil → API Keys
3. Copiez votre clé API et collez-la dans la configuration de l'addon

## Utilisation

Une fois configuré, l'addon sera accessible depuis le tableau de bord de Home Assistant. Vous pouvez :

- Sélectionner l'heure de début et de fin pour calculer la production estimée
- Activer/désactiver les mises à jour automatiques
- Consulter les détails des prévisions dans le tableau

## Intégration avec Home Assistant

Vous pouvez intégrer les données de cet addon dans votre tableau de bord Home Assistant en utilisant des capteurs personnalisés. Consultez la documentation Home Assistant pour plus d'informations sur la façon de créer des capteurs personnalisés basés sur les données de l'addon.

## Support

Si vous rencontrez des problèmes ou avez des suggestions, n'hésitez pas à ouvrir un ticket sur le dépôt GitHub de ce projet.

## Licence

Ce projet est sous licence MIT.

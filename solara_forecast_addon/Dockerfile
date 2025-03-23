ARG BUILD_FROM=ghcr.io/home-assistant/amd64-base-python:3.11

FROM ${BUILD_FROM}

# Installation des dépendances
RUN pip install --no-cache-dir \
    streamlit==1.37.0 \
    plotly==5.21.0 \
    pandas==2.2.1 \
    pyowm==3.3.0

# Copie des fichiers de l'application
WORKDIR /app
COPY run.sh /
COPY app.py /app/

# Autoriser l'exécution du script
RUN chmod a+x /run.sh

# Configuration de Streamlit pour fonctionner avec ingress
RUN mkdir -p /root/.streamlit
RUN echo "\
[server]\n\
headless = true\n\
enableCORS = false\n\
enableXsrfProtection = false\n\
" > /root/.streamlit/config.toml

# Port pour Streamlit
EXPOSE 8501

# Démarrage de l'application
CMD [ "/run.sh" ]

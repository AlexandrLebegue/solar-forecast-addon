ARG BUILD_FROM
FROM $BUILD_FROM

# Install requirements for add-on
RUN \
    apk add --no-cache \
    python3

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

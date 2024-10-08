# Utiliser une image de base Python officielle basée sur Alpine
FROM python:3.8-alpine

# Installer git
RUN apk update && \
    apk add --no-cache git && \
    rm -rf /var/cache/apk/*

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Cloner le dépôt GitHub spécifique
RUN git clone https://github.com/marccuculiere/librasky.git .

# Installer les dépendances  
COPY requirements.txt .  

RUN apk add -u libffi-dev g++ unixodbc-dev

RUN apk add --no-cache build-base && \  
    pip install --no-cache-dir -r requirements.txt  

# Exposer le port sur lequel l'application va tourner
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["python", "main.py"]

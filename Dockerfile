# Utiliser une image de base Ubuntu officielle (version légère)  
FROM ubuntu:20.04  
  
# Éviter les prompts de l'interface utilisateur de la part des paquets tzdata et autres  
ENV DEBIAN_FRONTEND=noninteractive  
  
# Mettre à jour les paquets et installer Python et pip  
RUN apt-get update && apt-get install -y --no-install-recommends \  
    python3.8 \  
    python3-pip \  
    python3.8-dev \  
    git \  
    build-essential \  
 && rm -rf /var/lib/apt/lists/*  
  
# Définir le répertoire de travail dans le conteneur  
WORKDIR /app  
  
# Cloner le dépôt GitHub spécifique  
RUN git clone https://github.com/marccuculiere/librasky.git .  
  
# Copier le fichier de dépendances Python et installer les dépendances  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
  
# Exposer le port sur lequel l'application va tourner  
EXPOSE 5000  
  
# Commande pour démarrer l'application  
CMD ["python3.8", "main.py"]  
  
# Réinitialiser l'argument pour les couches suivantes  
ARG DEBIAN_FRONTEND=dialog  

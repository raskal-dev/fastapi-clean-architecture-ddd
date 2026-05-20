# Utilisation d'une image Python officielle allégée (slim)
FROM python:3.12-slim

# Empêche Python de créer des fichiers .pyc
ENV PYTHONDONTWRITEBYTECODE=1
# Empêche Python de bufferiser stdout/stderr (les logs s'afficheront en temps réel)
ENV PYTHONUNBUFFERED=1

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Installation des dépendances système de base
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc python3-dev \
    && rm -rf /var/lib/apt/lists/*

# On copie le fichier pyproject.toml pour installer les dépendances en premier.
# Cela permet d'utiliser le cache Docker : si le code source change mais pas les dépendances,
# Docker ne relancera pas l'installation longue des packages.
COPY pyproject.toml .

# Installation de notre application (qui installera toutes nos dépendances)
RUN pip install --no-cache-dir .

# Copie de tout le code source dans le conteneur (les dossiers ignorés sont dans .dockerignore)
COPY . .

# Copie du script de démarrage et attribution des droits d'exécution
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Indique le port sur lequel l'application écoute
EXPOSE 8000

# Le script qui sera lancé au démarrage du conteneur
ENTRYPOINT ["/app/entrypoint.sh"]

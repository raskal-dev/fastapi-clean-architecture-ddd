#!/bin/bash

# Le script s'arrêtera si n'importe quelle commande échoue
set -e

echo "==========================================="
echo "Application des migrations de base de données"
echo "==========================================="
# Cette commande s'assure que la table users existe avant de lancer l'API
alembic upgrade head

echo "==========================================="
echo "Démarrage de l'API FastAPI"
echo "==========================================="
# On utilise `fastapi run` au lieu de `fastapi dev` pour un mode optimisé production
fastapi run app/main.py --host 0.0.0.0 --port 8000

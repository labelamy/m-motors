#!/bin/bash
# start.sh - script de démarrage pour le backend FastAPI

# Active l'environnement virtuel (modifie le chemin si nécessaire)
source ./venv/bin/activate

# Installe les dépendances (optionnel, utile si tu veux que ça s'assure à chaque démarrage)
pip install -r requirements.txt

# Lancer l'application avec uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000
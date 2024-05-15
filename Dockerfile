# Utiliser une image de base Python
FROM python:3.9-slim-buster

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers du projet dans le répertoire de travail
COPY . /app

# Installer les dépendances du projet
RUN pip install -r dep.txt

# Exposer le port 80
EXPOSE 8000

# Démarrer le serveur FastAPI
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
# Utilisation de l'image officielle Python
FROM python:3.12

# Définition du répertoire de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8000
EXPOSE 8000

# Commande pour démarrer le serveur Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "hassaniya.wsgi:application"]

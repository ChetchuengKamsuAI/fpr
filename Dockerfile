# Utiliser l'image officielle Python 3.9 comme base
FROM python:3.9.13

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tous les fichiers du projet dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install -r requirements.txt

# Commande pour exécuter votre application
CMD ["python", "login.py"]

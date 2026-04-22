# 1. Image Python officielle
FROM python:3.12-slim

# 2. Répertoire de travail
WORKDIR /app

# 3. Copier le fichier des dépendances
COPY requirements.txt .

# 4. Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier tout le code de l'application
COPY ./app /app

# 6. Exposer le port
EXPOSE 5000

# 7. Lancer l'application
CMD ["python", "app.py"]
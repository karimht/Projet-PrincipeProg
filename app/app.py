from flask import Flask, jsonify
from database import db
from models import User, Profile, Game, Tag
import os

app = Flask(__name__)

# Configuration de la base de données
# La variable DATABASE_URL est définie dans docker-compose.yml
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user_backlog:motdepasse@db:5432/backlog_jeux'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# On initialise l'ORM avec l'app Flask
db.init_app(app)


@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue dans l'API Backlog de jeux vidéo !"
    })


# Créer les tables au démarrage si elles n'existent pas
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    # host=0.0.0.0 pour que l'API soit accessible depuis l'extérieur du conteneur
    app.run(host='0.0.0.0', port=5000, debug=True)
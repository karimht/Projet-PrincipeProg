from flask import Flask, jsonify
from database import db
from models import User, Profile, Game, Tag, BacklogEntry
from routes.users import users_bp   # ← nouvel import
from routes.users import users_bp
from routes.games import games_bp   # ← nouvelle ligne
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user_backlog:motdepasse@db:5432/backlog_jeux'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Enregistrement du blueprint des utilisateurs
app.register_blueprint(users_bp)   # ← nouvelle ligne
app.register_blueprint(users_bp)
app.register_blueprint(games_bp)   # ← nouvelle ligne

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue dans l'API Backlog de jeux vidéo !"
    })


with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
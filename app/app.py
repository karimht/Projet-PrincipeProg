from flask import Flask, jsonify
from database import db
from models import User, Profile, Game, Tag, BacklogEntry
from routes.users import users_bp
from routes.users import users_bp
from routes.games import games_bp
from routes.tags import tags_bp
from routes.backlog import backlog_bp
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://user_backlog:motdepasse@db:5432/backlog_jeux'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Enregistrement du blueprint des utilisateurs
app.register_blueprint(users_bp)
app.register_blueprint(users_bp)
app.register_blueprint(games_bp)
app.register_blueprint(tags_bp)
app.register_blueprint(backlog_bp)

@app.route('/')
def home():
    return jsonify({
        "message": "Bienvenue dans l'API Backlog de jeux vidéo !",
        "routes": ["/users", "/games", "/tags", "/backlog"]
    })

# Gestion globale des erreurs
# Si une route n'existe pas (URL inconnue) → renvoie un JSON propre au lieu du HTML par défaut
@app.errorhandler(404)
def not_found(error):
    return jsonify({"erreur": "Route introuvable"}), 404


# Si une erreur serveur inattendue se produit → renvoie un JSON propre
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"erreur": "Erreur interne du serveur"}), 500


# Si le JSON envoyé est mal formé
@app.errorhandler(400)
def bad_request(error):
    return jsonify({"erreur": "Requête invalide"}), 400

with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
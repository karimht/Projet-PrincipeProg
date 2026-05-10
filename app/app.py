from flask import Flask, jsonify, CORS
from flasgger import Swagger
from database import db
from models import User, Profile, Game, Tag, BacklogEntry
from routes.users import users_bp
from routes.games import games_bp
from routes.tags import tags_bp
from routes.backlog import backlog_bp
import os


def create_app():
    """Factory pour créer l'application Flask."""
    app = Flask(__name__)

    CORS(app)   # active CORS pour toutes les routes

    # Configuration de la base de données
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'postgresql://user_backlog:motdepasse@db:5432/backlog_jeux'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configuration de Swagger
    app.config['SWAGGER'] = {
        'title': 'API Backlog de Jeux Vidéo',
        'description': 'API REST pour gérer un backlog personnel de jeux vidéo',
        'version': '1.0.0',
        'uiversion': 3
    }

    # Initialisation de l'ORM avec l'app Flask
    db.init_app(app)

    # Initialisation de Swagger
    Swagger(app)

    # Enregistrement des blueprints
    app.register_blueprint(users_bp)
    app.register_blueprint(games_bp)
    app.register_blueprint(tags_bp)
    app.register_blueprint(backlog_bp)

    # ============================================================
    # Route d'accueil
    # ============================================================
    @app.route('/')
    def home():
        return jsonify({
            "message": "Bienvenue dans l'API Backlog de jeux vidéo !",
            "routes": ["/users", "/games", "/tags", "/backlog"]
        })

    # ============================================================
    # Gestion globale des erreurs
    # ============================================================
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"erreur": "Route introuvable"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"erreur": "Erreur interne du serveur"}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"erreur": "Requête invalide"}), 400

    # Création des tables au démarrage
    with app.app_context():
        db.create_all()

    return app


# Création de l'app pour le démarrage normal
app = create_app()


if __name__ == '__main__':
    # host=0.0.0.0 pour que l'API soit accessible depuis l'extérieur du conteneur
    app.run(host='0.0.0.0', port=5000, debug=True)
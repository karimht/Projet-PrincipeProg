from flask import Blueprint, request, jsonify
from database import db
from models import Game

# Création du Blueprint pour les routes des jeux
games_bp = Blueprint('games', __name__)


# Afficher tous les jeux
@games_bp.route('/games', methods=['GET'])
def get_games():
    games = Game.query.all()
    return jsonify([g.to_dict() for g in games])


# Afficher un jeu par son id
@games_bp.route('/games/<int:id>', methods=['GET'])
def get_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"erreur": "Le jeu n'existe pas !"}), 404
    return jsonify(game.to_dict())


# Ajouter un jeu
@games_bp.route('/games', methods=['POST'])
def add_game():
    data = request.get_json()
    if not data.get('title'):
        return jsonify({"erreur": "Le titre est obligatoire"}), 400

    new_game = Game(
        title=data['title'],
        developer=data.get('developer'),
        release_year=data.get('release_year')
    )
    db.session.add(new_game)
    db.session.commit()
    return jsonify(new_game.to_dict()), 201  # 201 = création réussie


# Mettre à jour un jeu
@games_bp.route('/games/<int:id>', methods=['PUT'])
def update_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"erreur": "Le jeu n'existe pas !"}), 404

    data = request.get_json()
    if 'title' in data:
        game.title = data['title']
    if 'developer' in data:
        game.developer = data['developer']
    if 'release_year' in data:
        game.release_year = data['release_year']

    db.session.commit()
    return jsonify(game.to_dict())


# Supprimer un jeu
@games_bp.route('/games/<int:id>', methods=['DELETE'])
def delete_game(id):
    game = Game.query.get(id)
    if not game:
        return jsonify({"erreur": "Le jeu n'existe pas !"}), 404

    db.session.delete(game)
    db.session.commit()
    return jsonify({"message": "Jeu supprimé"}), 200
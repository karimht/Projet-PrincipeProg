from flask import Blueprint, request, jsonify
from database import db
from models import BacklogEntry, User, Game

# Création du Blueprint pour le backlog
backlog_bp = Blueprint('backlog', __name__)


# Afficher le backlog d'un utilisateur
# Filtre optionnel par statut : /users/1/backlog?status=playing
@backlog_bp.route('/users/<int:user_id>/backlog', methods=['GET'])
def get_user_backlog(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404

    # Récupération du paramètre de filtre dans l'URL (?status=...)
    status_filter = request.args.get('status')

    query = BacklogEntry.query.filter_by(user_id=user_id)
    if status_filter:
        query = query.filter_by(status=status_filter)

    entries = query.all()
    return jsonify([e.to_dict() for e in entries])


# Ajouter un jeu au backlog d'un utilisateur
@backlog_bp.route('/users/<int:user_id>/backlog', methods=['POST'])
def add_to_backlog(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404

    data = request.get_json()
    game_id = data.get('game_id')
    if not game_id:
        return jsonify({"erreur": "game_id obligatoire"}), 400

    game = Game.query.get(game_id)
    if not game:
        return jsonify({"erreur": "Le jeu n'existe pas !"}), 404

    # Vérifier que le jeu n'est pas déjà dans le backlog de cet utilisateur
    existing = BacklogEntry.query.filter_by(user_id=user_id, game_id=game_id).first()
    if existing:
        return jsonify({"erreur": "Ce jeu est déjà dans le backlog"}), 400

    new_entry = BacklogEntry(
        user_id=user_id,
        game_id=game_id,
        status=data.get('status', 'to_play'),
        rating=data.get('rating'),
        review=data.get('review')
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify(new_entry.to_dict()), 201


# Modifier une entrée du backlog (changer le statut, la note, l'avis...)
@backlog_bp.route('/backlog/<int:id>', methods=['PATCH'])
def update_backlog_entry(id):
    entry = BacklogEntry.query.get(id)
    if not entry:
        return jsonify({"erreur": "L'entrée n'existe pas !"}), 404

    data = request.get_json()
    if 'status' in data:
        entry.status = data['status']
    if 'rating' in data:
        entry.rating = data['rating']
    if 'review' in data:
        entry.review = data['review']

    db.session.commit()
    return jsonify(entry.to_dict())


# Retirer un jeu du backlog
@backlog_bp.route('/backlog/<int:id>', methods=['DELETE'])
def delete_backlog_entry(id):
    entry = BacklogEntry.query.get(id)
    if not entry:
        return jsonify({"erreur": "L'entrée n'existe pas !"}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Jeu retiré du backlog"}), 200


# Statistiques d'un utilisateur : nombre de jeux par statut
@backlog_bp.route('/users/<int:user_id>/stats', methods=['GET'])
def get_user_stats(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404

    stats = {
        "to_play": BacklogEntry.query.filter_by(user_id=user_id, status='to_play').count(),
        "playing": BacklogEntry.query.filter_by(user_id=user_id, status='playing').count(),
        "finished": BacklogEntry.query.filter_by(user_id=user_id, status='finished').count(),
        "dropped": BacklogEntry.query.filter_by(user_id=user_id, status='dropped').count(),
        "total": BacklogEntry.query.filter_by(user_id=user_id).count()
    }
    return jsonify(stats)
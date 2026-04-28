from flask import Blueprint, request, jsonify
from database import db
from models import User

# Création du Blueprint pour les routes utilisateurs
users_bp = Blueprint('users', __name__)


# Afficher tous les utilisateurs
@users_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])


# Afficher un utilisateur par son id
@users_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404
    return jsonify(user.to_dict())


# Ajouter un utilisateur
@users_bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    # Vérification des champs obligatoires
    if not data.get('email') or not data.get('username'):
        return jsonify({"erreur": "email et username obligatoires"}), 400

    new_user = User(
        email=data['email'],
        username=data['username']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201  # 201 = création réussie


# Mettre à jour un utilisateur
@users_bp.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404

    data = request.get_json()
    if 'email' in data:
        user.email = data['email']
    if 'username' in data:
        user.username = data['username']

    db.session.commit()
    return jsonify(user.to_dict())


# Supprimer un utilisateur
# (supprime aussi son profil et son backlog en cascade)
@users_bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Utilisateur supprimé"}), 200
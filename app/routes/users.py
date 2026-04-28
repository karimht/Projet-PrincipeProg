from flask import Blueprint, request, jsonify
from database import db
from models import User, Profile

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

# ============================================================
# Routes pour le profil (relation ONE-TO-ONE avec User)
# ============================================================

# Créer ou mettre à jour le profil d'un utilisateur
@users_bp.route('/users/<int:id>/profile', methods=['PUT'])
def update_profile(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"erreur": "L'utilisateur n'existe pas !"}), 404

    data = request.get_json()

    # Si l'utilisateur n'a pas encore de profil, on en crée un
    if not user.profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        user.profile = profile

    # Mise à jour des champs (seulement ceux présents dans la requête)
    if 'avatar_url' in data:
        user.profile.avatar_url = data['avatar_url']
    if 'favorite_platform' in data:
        user.profile.favorite_platform = data['favorite_platform']
    if 'bio' in data:
        user.profile.bio = data['bio']

    db.session.commit()
    return jsonify(user.profile.to_dict())
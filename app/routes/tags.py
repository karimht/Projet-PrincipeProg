from flask import Blueprint, request, jsonify
from database import db
from models import Tag

# Création du Blueprint pour les routes des tags
tags_bp = Blueprint('tags', __name__)


# Afficher tous les tags
@tags_bp.route('/tags', methods=['GET'])
def get_tags():
    tags = Tag.query.all()
    return jsonify([t.to_dict() for t in tags])


# Afficher un tag par son id
@tags_bp.route('/tags/<int:id>', methods=['GET'])
def get_tag(id):
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({"erreur": "Le tag n'existe pas !"}), 404
    return jsonify(tag.to_dict())


# Ajouter un tag
@tags_bp.route('/tags', methods=['POST'])
def add_tag():
    data = request.get_json()
    if not data.get('name'):
        return jsonify({"erreur": "Le nom du tag est obligatoire"}), 400

    # Vérifier qu'un tag avec ce nom n'existe pas déjà
    existing = Tag.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({"erreur": "Ce tag existe déjà"}), 400

    new_tag = Tag(name=data['name'])
    try:
        db.session.add(new_tag)
        db.session.commit()
        return jsonify(new_tag.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erreur": "Erreur lors de la création du tag"}), 400


# Supprimer un tag
@tags_bp.route('/tags/<int:id>', methods=['DELETE'])
def delete_tag(id):
    tag = Tag.query.get(id)
    if not tag:
        return jsonify({"erreur": "Le tag n'existe pas !"}), 404

    db.session.delete(tag)
    db.session.commit()
    return jsonify({"message": "Tag supprimé"}), 200
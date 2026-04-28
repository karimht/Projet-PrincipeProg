from database import db
from datetime import datetime


# ============================================================
# Modèle User
# ============================================================
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relation ONE-TO-ONE avec Profile
    # uselist=False => un user a UN seul profil (pas une liste)
    # cascade='all, delete-orphan' => si on supprime le user, son profil est aussi supprimé
    profile = db.relationship(
        'Profile',
        backref='user',
        uselist=False,
        cascade='all, delete-orphan'
    )

    # Méthode pour convertir l'objet en dictionnaire (pour jsonify)
    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'profile': self.profile.to_dict() if self.profile else None
        }


# ============================================================
# Modèle Profile (relation ONE-TO-ONE avec User)
# ============================================================
class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    # unique=True sur la clé étrangère => garantit la relation ONE-TO-ONE
    # (un user ne peut avoir qu'un seul profil)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    avatar_url = db.Column(db.String(255))
    favorite_platform = db.Column(db.String(50))  # ex: "PC", "PS5", "Switch"
    bio = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'avatar_url': self.avatar_url,
            'favorite_platform': self.favorite_platform,
            'bio': self.bio
        }
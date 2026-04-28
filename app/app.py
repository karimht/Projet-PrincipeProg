from flask import Flask, jsonify
from database import db
from models import User, Profile, Game, Tag, BacklogEntryimport os

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

    # ============================================================
# Modèle BacklogEntry
# Chaque entrée = un jeu dans le backlog d'un user
# avec son statut, sa note personnelle et son avis
# ============================================================
class BacklogEntry(db.Model):
    __tablename__ = 'backlog_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='to_play')
    # Statuts possibles : "to_play", "playing", "finished", "dropped"
    rating = db.Column(db.Integer)  # note de 0 à 10
    review = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'game_id': self.game_id,
            'game_title': self.game.title if self.game else None,
            'status': self.status,
            'rating': self.rating,
            'review': self.review,
            'added_at': self.added_at.isoformat() if self.added_at else None
        }
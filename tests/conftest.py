"""
Configuration partagée pour tous les tests.
Le 'fixture' client est utilisée par tous les tests pour faire des requêtes à l'API.
"""
import sys
import os
import pytest

# Ajouter le dossier 'app' au path pour pouvoir importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# IMPORTANT : on définit la variable d'environnement AVANT d'importer create_app
# pour que SQLAlchemy utilise SQLite en mémoire (pas PostgreSQL)
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

from app import create_app
from database import db


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.drop_all()
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()
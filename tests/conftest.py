"""
Configuration partagée pour tous les tests.
Le 'fixture' client est utilisée par tous les tests pour faire des requêtes à l'API.
"""
import sys
import os
import pytest

# Ajouter le dossier 'app' au path pour pouvoir importer les modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

from app import app
from database import db


@pytest.fixture
def client():
    # On utilise une base SQLite en mémoire pour les tests
    # (pas besoin de PostgreSQL pour tester)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Crée les tables
            yield client     # Donne le client de test au test
            db.session.remove()
            db.drop_all()    # Nettoie après le test
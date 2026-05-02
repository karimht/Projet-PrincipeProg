
"""
Tests pour les routes des jeux + la relation many-to-many avec les tags.
"""


def test_create_game(client):
    """POST /games crée un nouveau jeu."""
    response = client.post('/games', json={
        'title': 'Hollow Knight',
        'developer': 'Team Cherry',
        'release_year': 2017
    })
    assert response.status_code == 201
    assert response.get_json()['title'] == 'Hollow Knight'


def test_get_games(client):
    """GET /games renvoie la liste des jeux."""
    client.post('/games', json={'title': 'Celeste'})
    client.post('/games', json={'title': 'Hades'})

    response = client.get('/games')
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_create_game_without_title(client):
    """POST /games sans titre renvoie 400."""
    response = client.post('/games', json={'developer': 'Anonymous'})
    assert response.status_code == 400


def test_many_to_many_game_tag(client):
    """Test de la relation Many-to-Many entre Game et Tag."""
    # Créer un jeu et un tag
    client.post('/games', json={'title': 'Hollow Knight'})
    client.post('/tags', json={'name': 'Indie'})

    # Associer le tag au jeu
    response = client.post('/games/1/tags/1')
    assert response.status_code == 201

    # Vérifier que le tag est bien associé
    response = client.get('/games/1')
    assert 'Indie' in response.get_json()['tags']

    # Retirer le tag
    response = client.delete('/games/1/tags/1')
    assert response.status_code == 200

    # Vérifier que le tag n'est plus associé
    response = client.get('/games/1')
    assert response.get_json()['tags'] == []
"""
Tests pour les routes du backlog (relation one-to-many).
"""


def setup_user_and_game(client):
    """Helper : crée un user et un jeu pour les tests."""
    client.post('/users', json={'email': 'a@b.c', 'username': 'alice'})
    client.post('/games', json={'title': 'Hollow Knight'})


def test_add_to_backlog(client):
    """POST /users/<id>/backlog ajoute un jeu au backlog."""
    setup_user_and_game(client)

    response = client.post('/users/1/backlog', json={
        'game_id': 1,
        'status': 'playing',
        'rating': 9
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == 'playing'
    assert data['rating'] == 9


def test_get_user_backlog(client):
    """GET /users/<id>/backlog renvoie le backlog du user."""
    setup_user_and_game(client)
    client.post('/users/1/backlog', json={'game_id': 1, 'status': 'playing'})

    response = client.get('/users/1/backlog')
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_filter_backlog_by_status(client):
    """GET /users/<id>/backlog?status=... filtre par statut."""
    setup_user_and_game(client)
    client.post('/games', json={'title': 'Celeste'})
    client.post('/users/1/backlog', json={'game_id': 1, 'status': 'playing'})
    client.post('/users/1/backlog', json={'game_id': 2, 'status': 'to_play'})

    response = client.get('/users/1/backlog?status=playing')
    assert response.status_code == 200
    entries = response.get_json()
    assert len(entries) == 1
    assert entries[0]['status'] == 'playing'


def test_update_backlog_entry(client):
    """PATCH /backlog/<id> met à jour une entrée."""
    setup_user_and_game(client)
    client.post('/users/1/backlog', json={'game_id': 1, 'status': 'playing'})

    response = client.patch('/backlog/1', json={'status': 'finished', 'rating': 10})
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'finished'
    assert data['rating'] == 10


def test_user_stats(client):
    """GET /users/<id>/stats renvoie les stats du backlog."""
    setup_user_and_game(client)
    client.post('/games', json={'title': 'Celeste'})
    client.post('/users/1/backlog', json={'game_id': 1, 'status': 'finished'})
    client.post('/users/1/backlog', json={'game_id': 2, 'status': 'playing'})

    response = client.get('/users/1/stats')
    assert response.status_code == 200
    stats = response.get_json()
    assert stats['finished'] == 1
    assert stats['playing'] == 1
    assert stats['total'] == 2
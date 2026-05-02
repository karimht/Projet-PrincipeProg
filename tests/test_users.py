"""
Tests pour les routes des utilisateurs.
"""


def test_get_users_empty(client):
    """GET /users renvoie une liste vide quand aucun user n'existe."""
    response = client.get('/users')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_user(client):
    """POST /users crée un nouvel utilisateur."""
    response = client.post('/users', json={
        'email': 'alice@test.com',
        'username': 'alice'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == 'alice@test.com'
    assert data['username'] == 'alice'
    assert 'id' in data


def test_create_user_missing_fields(client):
    """POST /users sans champs obligatoires renvoie 400."""
    response = client.post('/users', json={'email': 'a@b.c'})  # username manquant
    assert response.status_code == 400


def test_get_user_by_id(client):
    """GET /users/<id> renvoie le bon user."""
    # On crée d'abord un user
    client.post('/users', json={'email': 'bob@test.com', 'username': 'bob'})

    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.get_json()['username'] == 'bob'


def test_get_user_not_found(client):
    """GET /users/<id> renvoie 404 si le user n'existe pas."""
    response = client.get('/users/999')
    assert response.status_code == 404


def test_update_user(client):
    """PUT /users/<id> met à jour un user."""
    client.post('/users', json={'email': 'old@test.com', 'username': 'old'})

    response = client.put('/users/1', json={'username': 'new'})
    assert response.status_code == 200
    assert response.get_json()['username'] == 'new'


def test_delete_user(client):
    """DELETE /users/<id> supprime un user."""
    client.post('/users', json={'email': 'x@test.com', 'username': 'todelete'})

    response = client.delete('/users/1')
    assert response.status_code == 200

    # Vérifier que le user n'existe plus
    response = client.get('/users/1')
    assert response.status_code == 404


def test_update_profile(client):
    """PUT /users/<id>/profile crée le profil si inexistant (relation 1-1)."""
    client.post('/users', json={'email': 'a@b.c', 'username': 'alice'})

    response = client.put('/users/1/profile', json={
        'favorite_platform': 'PC',
        'bio': 'Joueuse passionnée'
    })
    assert response.status_code == 200
    assert response.get_json()['favorite_platform'] == 'PC'
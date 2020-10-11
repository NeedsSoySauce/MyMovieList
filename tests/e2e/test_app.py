import pytest
from flask.testing import FlaskClient


def test_get_home(client: FlaskClient):
    response = client.get('/')
    assert response.status_code == 200


def test_get_search(client: FlaskClient):
    response = client.get('/search')
    assert response.status_code == 200

    data = {
        'query': 'john wick',
        'genre': 'action',
        'director': 'Chad Stahelski',
        'actor': 'keanu reeves'
    }

    response = client.get('/search', data=data)
    assert response.status_code == 200


def test_get_movie(client: FlaskClient):
    response = client.get('/movie/7')
    assert response.status_code == 200

    response = client.get('/movie/1234')
    assert response.status_code == 404


def test_get_movie_reviews(client: FlaskClient):
    response = client.get('/movie/7/reviews')
    assert response.status_code == 200

    response = client.get('/movie/1234/reviews')
    assert response.status_code == 404


def test_register(client: FlaskClient):
    response = client.get('/register')
    assert response.status_code == 200

    data = {
        'username': 'thorke',
        'password': 'cLQ^C#oFXloS'
    }

    response = client.post('/register', data=data)
    assert response.status_code == 200


def test_login(client: FlaskClient):
    response = client.get('/login')
    assert response.status_code == 200

    data = {
        'username': 'thorke',
        'password': 'cLQ^C#oFXloS'
    }

    client.post('/register', data=data)
    response = client.post('/login', data=data)
    assert response.status_code == 200

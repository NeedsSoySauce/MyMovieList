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
    response = client.get('/movie')
    assert response.status_code == 200

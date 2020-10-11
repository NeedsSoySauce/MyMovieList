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


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Username required'),
        ('cj', '', b'Usernames must be at least 3 characters'),
        ('test', '', b'Password required'),
        ('test', 'test', b'Your password must be at least 8 characters, contain an upper case letter, a lower case ' \
                         b'letter, and a digit'),
        ('test', 'test123A', b'Username unavailable'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


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


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('abcd', 'abcd', b'Unrecognized username - please check and try again.'),
        ('test', 'abcd', b'Incorrect password - please check and try again.')
))
def test_login_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/login',
        data={'username': username, 'password': password}
    )
    assert message in response.data

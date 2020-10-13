import pytest
from flask import session
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


def test_add_review_anonymous(client: FlaskClient):
    response = client.get('/movie/1/reviews')
    assert response.status_code == 200

    data = {
        'rating': 1,
        'review': 'abc 123'
    }

    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)

    assert b'Anonymous' in response.data
    assert b'1' in response.data
    assert b'abc 123' in response.data


def test_add_review_authenticated(client: FlaskClient, auth):
    data = {
        'rating': 1,
        'review': 'abc 123'
    }

    auth.login()
    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)

    assert b'test' in response.data
    assert b'1' in response.data
    assert b'abc 123' in response.data


@pytest.mark.parametrize(('rating', 'text', 'message'), (
        ('', 'abc', b'Invalid Choice: could not coerce'),
        (0, 'abc', b'Ratings must be an integer between 1 and 10.'),
        (11, 'abc', b'Ratings must be an integer between 1 and 10.'),
        (2.5, 'abc', b'Invalid Choice: could not coerce'),
        (1, '', b'Reviews must be at least one character long.'),
        (1, 'crap', b'Please keep it PG (no profanity!).')
))
def test_add_review_invalid_input(client, rating, text, message):
    data = {
        'rating': rating,
        'review': text
    }

    if rating is None:
        del data['rating']

    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)
    assert message in response.data


def test_watchlist(client: FlaskClient, auth):
    auth.login()

    # User should have no movies on their watchlist to start with
    response = client.get('/watchlist')
    assert b'Looks like your watchlist is empty.' in response.data

    # Add movie
    response = client.post('/watchlist/1')
    assert response.status_code == 201

    # Check movie has been added
    response = client.get('/watchlist')
    assert b'Looks like your watchlist is empty.' not in response.data

    # Remove movie
    response = client.delete('/watchlist/1')
    assert response.status_code == 200


def test_user(client: FlaskClient):
    response = client.get('/user/test')
    assert response.status_code == 200
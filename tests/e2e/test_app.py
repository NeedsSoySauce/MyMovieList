import pytest
from flask import session
from flask.testing import FlaskClient

from movie.auth import auth
from movie.auth.auth import UNKNOWN_USER_MESSAGE
from movie.movie import movie
from movie.user import user
from tests.conftest import AuthenticationManager


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
        'password': 'test123A'
    }

    response = client.post('/register', data=data, follow_redirects=False)

    # Check client is redirected to homepage after a successful signup
    assert response.status_code == 302
    assert response.headers['location'] == 'http://localhost/'

    # Check a session is created
    with client:
        client.get('/')
        assert session['username'] == 'thorke'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', auth.USERNAME_REQUIRED_MESSAGE),
        ('cj', '', auth.INVALID_USERNAME_LENGTH_MESSAGE),
        ('test', '', auth.PASSWORD_REQUIRED_MESSAGE),
        ('testuser', 'test', auth.INVALID_PASSWORD_MESSAGE),
        ('testuser', 'test123Ab', auth.USERNAME_UNAVAILABLE_MESSAGE)
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/register',
        data={'username': username, 'password': password}
    )
    assert message.encode() in response.data


def test_login(client: FlaskClient, auth):
    response = client.get('/login')
    assert response.status_code == 200

    response = auth.login()

    # Check client is redirected to homepage
    assert response.status_code == 302
    assert response.headers['location'] == 'http://localhost/'

    # Check a session is created
    with client:
        client.get('/')
        assert session['username'] == 'testuser'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('abcd', 'abcd', auth.UNKNOWN_USER_MESSAGE),
        ('testuser', 'abcd', auth.INCORRECT_PASSWORD_MESSAGE)
))
def test_login_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/login',
        data={'username': username, 'password': password}
    )
    assert message.encode() in response.data


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
        ('', 'abc', movie.INVALID_CHOICE_MESSAGE),
        (0, 'abc', movie.INVALID_RATING_RANGE_MESSAGE),
        (11, 'abc', movie.INVALID_RATING_RANGE_MESSAGE),
        (2.5, 'abc', movie.INVALID_CHOICE_MESSAGE),
        (1, '', movie.INVALID_REVIEW_TEXT_LENGTH_MESSAGE),
        (1, 'crap', movie.REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE)
))
def test_add_review_invalid_input(client, rating, text, message):
    data = {
        'rating': rating,
        'review': text
    }

    if rating is None:
        del data['rating']

    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)
    assert message.encode() in response.data


def test_user(client: FlaskClient):
    response = client.get('/user/testuser')
    assert response.status_code == 200


def test_change_username(client: FlaskClient, auth: AuthenticationManager):
    auth.login()

    data = {
        'new_username': 'abc123'
    }

    # Check user is redirected after a successful username change
    response = client.post('/user/testuser/username/change', data=data, follow_redirects=False)
    assert response.status_code == 302
    assert response.headers['location'] == 'http://localhost/user/abc123'

    # Check old user no longer exists
    response = client.get('/user/test')
    assert response.status_code == 404


@pytest.mark.parametrize(('new_username', 'message'), (
        ('', user.NEW_USERNAME_REQUIRED_MESSAGE),
        ('ab', auth.INVALID_USERNAME_LENGTH_MESSAGE),
        ('testuser2', auth.USERNAME_UNAVAILABLE_MESSAGE)
))
def test_change_username_invalid_input(client: FlaskClient, auth: AuthenticationManager, new_username, message):
    auth.login()

    data = {
        'new_username': new_username
    }

    response = client.post('/user/testuser/username/change', data=data, follow_redirects=True)
    assert message.encode() in response.data


def test_change_username_unauthorized(client: FlaskClient, auth: AuthenticationManager):
    auth.login()

    data = {
        'new_username': 'abc123'
    }

    response = client.post('/user/testuser2/username/change', data=data)
    assert response.status_code == 401

    # Check the other user's account is okay
    response = client.get('/user/testuser2')
    assert response.status_code == 200


def test_change_password(client: FlaskClient, auth: AuthenticationManager):
    auth.login()

    data = {
        'current_password': 'test123A',
        "new_password": "test123B"
    }

    # Check user is redirected after a successful password change
    response = client.post('/user/testuser/password/change', data=data)

    assert response.status_code == 302
    assert response.headers['location'] == 'http://localhost/user/testuser'

    # Check the new credentials work
    auth.logout()

    with client:
        response = auth.login(username='testuser', password='test123B', follow_redirects=True)
        assert response.status_code == 200
        assert session['username'] == 'testuser'


@pytest.mark.parametrize(('current_password', 'new_password', 'message'), (
        ('', '', user.CURRENT_PASSWORD_REQUIRED_MESSAGE),
        ('test123A', '', user.NEW_PASSWORD_REQUIRED_MESSAGE),
        ('abcd123A', 'abcd123A', user.PASSWORDS_EQUAL_MESSAGE),
        ('test123A', 'test123A', user.PASSWORDS_EQUAL_MESSAGE),
        ('incorrectpassword', 'test123A', auth.INCORRECT_PASSWORD_MESSAGE)
))
def test_change_password_invalid_input(client: FlaskClient,
                                       auth: AuthenticationManager,
                                       current_password,
                                       new_password,
                                       message):
    auth.login()

    data = {
        'current_password': current_password,
        "new_password": new_password
    }

    # Check user is redirected after a successful password change
    response = client.post('/user/testuser/password/change', data=data)

    assert message.encode() in response.data


def test_change_password_unauthorized(client: FlaskClient, auth: AuthenticationManager):
    auth.login()

    data = {
        'current_password': 'test123A',
        "new_password": "test123B"
    }

    response = client.post('/user/testuser2/password/change', data=data)
    assert response.status_code == 401

    # Check the other user's account is okay
    response = client.get('/user/testuser2')
    assert response.status_code == 200


def test_delete_account(client: FlaskClient, auth: AuthenticationManager):
    auth.login()

    data = {
        'confirmation': 'testuser'
    }

    # Check user is redirected after successful account deletion
    response = client.post('/user/testuser/delete', data=data)

    assert response.status_code == 302
    assert response.headers['location'] == 'http://localhost/'

    # Check user is signed out
    with client:
        response = client.get('/')
        assert response.status_code == 200
        assert 'username' not in session

    # Check user no longer exists
    response = client.get('/user/testuser')
    assert response.status_code == 404

    # Check user's old credentials no longer work
    response = auth.login()
    assert response.status_code == 200
    assert UNKNOWN_USER_MESSAGE.encode() in response.data


@pytest.mark.parametrize(('confirmation', 'message'), (
        ('', user.CONFIRMATION_REQUIRED_MESSAGE),
        ('abc123', user.CONFIRMATION_FAILED_MESSAGE)
))
def test_delete_account_invalid_input(client: FlaskClient,
                                      auth: AuthenticationManager,
                                      confirmation,
                                      message):
    auth.login()

    data = {
        'confirmation': confirmation
    }

    response = client.post('/user/testuser/delete', data=data)

    assert message.encode() in response.data


def test_delete_account_unauthorized(client: FlaskClient, auth: AuthenticationManager):
    auth.login()

    data = {
        'confirmation': 'testuser'
    }

    response = client.post('/user/testuser2/delete', data=data)
    assert response.status_code == 401

    # Check the other user's account is okay
    response = client.get('/user/testuser2')
    assert response.status_code == 200

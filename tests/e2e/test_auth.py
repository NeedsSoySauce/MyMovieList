import pytest
from flask import session
from flask.testing import FlaskClient

from movie.auth import auth


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

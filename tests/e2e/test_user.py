import pytest
from flask import session
from flask.testing import FlaskClient

import movie
import movie.auth.auth as auth
from movie.user import user
from tests.conftest import AuthenticationManager


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
    assert movie.auth.auth.UNKNOWN_USER_MESSAGE.encode() in response.data


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

import pytest

from movie.auth.services import *


def test_add_user(memory_repository):
    username = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, username, password)
    user = get_user(memory_repository, username)

    assert user.username == username


def test_add_user_existing(memory_repository):
    username = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, username, password)

    with pytest.raises(NameNotUniqueException):
        add_user(memory_repository, username, password)


def test_get_user_not_existing(memory_repository):
    with pytest.raises(UnknownUserException):
        get_user(memory_repository, 'test')


def test_authenticate_user(memory_repository):
    username = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, username, password)

    authenticate_user(memory_repository, username, password)


def test_authenticate_user_exception(memory_repository):
    username = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, username, password)

    with pytest.raises(AuthenticationException):
        authenticate_user(memory_repository, 'abc123', 'wrongpassword')

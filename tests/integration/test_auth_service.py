import pytest

from movie.auth.services import *


def test_add_user(memory_repository):
    user_name = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, user_name, password)
    user = get_user(memory_repository, user_name)

    assert user.user_name == user_name


def test_add_user_existing(memory_repository):
    user_name = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, user_name, password)

    with pytest.raises(NameNotUniqueException):
        add_user(memory_repository, user_name, password)


def test_get_user_not_existing(memory_repository):
    with pytest.raises(UnknownUserException):
        get_user(memory_repository, 'test')


def test_authenticate_user(memory_repository):
    user_name = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, user_name, password)

    authenticate_user(memory_repository, user_name, password)


def test_authenticate_user_exception(memory_repository):
    user_name = 'abc123'
    password = 'abcABC123'

    add_user(memory_repository, user_name, password)

    with pytest.raises(AuthenticationException):
        authenticate_user(memory_repository, 'abc123', 'wrongpassword')

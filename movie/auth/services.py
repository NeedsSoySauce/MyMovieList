from werkzeug.security import generate_password_hash, check_password_hash

from movie.adapters.repository import AbstractRepository
from movie.domain.user import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(repo: AbstractRepository, username: str, password: str) -> None:
    # Check that the given username is available.
    try:
        _ = repo.get_user(username)
        raise NameNotUniqueException
    except ValueError:
        # No user with that username could be found
        pass

    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)

    # Create and store the new User, with password encrypted.
    user = User(username, password_hash)
    repo.add_user(user)


def get_user(repo: AbstractRepository, user_name: str) -> User:
    try:
        return repo.get_user(user_name)
    except ValueError:
        raise UnknownUserException


def authenticate_user(repo: AbstractRepository, username: str, password: str) -> None:
    """ Raises an AuthenticationException if the given username and or password are not valid. """
    try:
        user = repo.get_user(username)
    except ValueError:
        raise UnknownUserException

    if not check_password_hash(user.password, password):
        raise AuthenticationException

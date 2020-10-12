from werkzeug.security import generate_password_hash, check_password_hash

from movie.adapters.repository import AbstractRepository
from movie.domain.user import User


class NameNotUniqueException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def check_if_user_exists(repo: AbstractRepository, username: str) -> bool:
    """ Returns True if a user with the given name exists in the given repository otherwise False. """
    try:
        _ = repo.get_user(username)
    except ValueError:
        return False
    return True


def add_user(repo: AbstractRepository, username: str, password: str) -> None:
    # Check that the given username is available.
    if check_if_user_exists(repo, username):
        raise NameNotUniqueException

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


def change_username(repo: AbstractRepository, user: User, username: str) -> None:
    """
    Sets the given user's username to the given username.

    Raises:
        NameNotUniqueException: if the given username is already taken.
    """
    # Check that the given username is available.
    if check_if_user_exists(repo, username):
        raise NameNotUniqueException

    repo.update_username(user, username)


def change_password(repo: AbstractRepository, user: User, password: str) -> None:
    """ Sets the given user's password to the given password. """
    user.password = generate_password_hash(password)


def delete_user(repo: AbstractRepository, user: User) -> None:
    """ Removes the given user from the given repository. """
    repo.delete_user(user)

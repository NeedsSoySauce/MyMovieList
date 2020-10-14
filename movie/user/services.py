from werkzeug.security import check_password_hash

from movie.adapters.repository import AbstractRepository
from movie.auth.services import AuthenticationException, UnknownUserException
from movie.domain.user import User


def get_user(repo: AbstractRepository, username: str) -> User:
    try:
        return repo.get_user(username)
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

from movie.adapters.repository import AbstractRepository
from movie.domain.user import User


def get_user(repo: AbstractRepository, user_name: str) -> User:
    return repo.get_user(user_name)

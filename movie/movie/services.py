from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie


def get_movie_by_id(repo: AbstractRepository, movie_id: int) -> Movie:
    return repo.get_movie_by_id(movie_id)

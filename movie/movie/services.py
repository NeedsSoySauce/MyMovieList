
from movie.adapters.repository import instance as repo
from movie.domain.movie import Movie


def get_movie_by_id(movie_id: int) -> Movie:
    return repo.get_movie_by_id(movie_id)

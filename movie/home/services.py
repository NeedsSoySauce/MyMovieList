from typing import List, Dict

from movie.adapters.repository import instance as repo
from movie.domain.genre import Genre


def get_number_of_movies():
    return repo.get_number_of_movies()


def get_genres():
    return repo.get_genres()


def get_movies_per_genre(genres: List[Genre]) -> Dict[Genre, int]:
    movies: Dict[Genre, int] = {}

    for genre in genres:
        movies[genre] = repo.get_number_of_movies(genres=[genre])

    return movies

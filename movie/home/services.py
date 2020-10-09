from typing import List, Dict

from movie.adapters.repository import instance as repo
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre


def get_number_of_movies() -> int:
    return repo.get_number_of_movies()


def get_genres() -> List[Genre]:
    return repo.get_genres()


def get_movies_per_genre(genres: List[Genre]) -> Dict[Genre, int]:
    movies: Dict[Genre, int] = {}

    for genre in genres:
        movies[genre] = repo.get_number_of_movies(genres=[genre])

    return movies


def get_directors() -> List[Director]:
    return repo.get_directors()


def get_movies_per_director(directors: List[Director]) -> Dict[Director, int]:
    movies: Dict[Director, int] = {}

    for director in directors:
        movies[director] = repo.get_number_of_movies(director=director)

    return movies


def get_actors() -> List[Actor]:
    return repo.get_actors()


def get_movies_per_actor(actors: List[Actor]) -> Dict[Actor, int]:
    movies: Dict[Actor, int] = {}

    for actor in actors:
        movies[actor] = repo.get_number_of_movies(actors=[actor])

    return movies

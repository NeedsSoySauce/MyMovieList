from typing import List, Dict

from movie.adapters.repository import AbstractRepository
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre


def get_number_of_movies(repo: AbstractRepository) -> int:
    return repo.get_number_of_movies()


def get_genres(repo: AbstractRepository) -> List[Genre]:
    return repo.get_genres()


def get_movies_per_genre(repo: AbstractRepository) -> Dict[Genre, int]:
    return repo.get_movies_per_genre()


def get_directors(repo: AbstractRepository) -> List[Director]:
    return repo.get_directors()


def get_movies_per_director(repo: AbstractRepository, directors: List[Director]) -> Dict[Director, int]:
    movies: Dict[Director, int] = {}

    for director in directors:
        movies[director] = repo.get_number_of_movies(director=director)

    return movies


def get_actors(repo: AbstractRepository) -> List[Actor]:
    return repo.get_actors()


def get_movies_per_actor(repo: AbstractRepository, actors: List[Actor]) -> Dict[Actor, int]:
    movies: Dict[Actor, int] = {}

    for actor in actors:
        movies[actor] = repo.get_number_of_movies(actors=[actor])

    return movies

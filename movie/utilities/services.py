from typing import List, Dict

from movie.adapters.repository import AbstractRepository
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre


def get_number_of_movies(repo: AbstractRepository) -> int:
    """ Returns the number of movies in the given repository. """
    return repo.get_number_of_movies()


def get_genres(repo: AbstractRepository) -> List[Genre]:
    """ Returns a list of all Genres in the given repository. """
    return repo.get_genres()


def get_movies_per_genre(repo: AbstractRepository) -> Dict[Genre, int]:
    """ Returns a dict mapping Genres to the number of movies in the given repository with that genre. """
    return repo.get_movies_per_genre()


def get_directors(repo: AbstractRepository) -> List[Director]:
    """ Returns a list of all Directors in the given repository. """
    return repo.get_directors()


def get_movies_per_director(repo: AbstractRepository, directors: List[Director]) -> Dict[Director, int]:
    """ Returns a dict mapping Directors to the number of movies in the given repository with that director. """
    movies: Dict[Director, int] = {}

    for director in directors:
        movies[director] = repo.get_number_of_movies(director=director)

    return movies


def get_actors(repo: AbstractRepository) -> List[Actor]:
    """ Returns a list of all Actors in the given repository. """
    return repo.get_actors()


def get_movies_per_actor(repo: AbstractRepository, actors: List[Actor]) -> Dict[Actor, int]:
    """ Returns a dict mapping Actors to the number of movies in the given repository with that actor. """
    movies: Dict[Actor, int] = {}

    for actor in actors:
        movies[actor] = repo.get_number_of_movies(actors=[actor])

    return movies

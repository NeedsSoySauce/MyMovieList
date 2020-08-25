from typing import List, NamedTuple
from abc import ABC, abstractmethod

from domainmodel.movie import Movie
from domainmodel.user import User
from domainmodel.review import Review


class AbstractMovingWatchingSimulation(ABC):
    class State(NamedTuple):
        users: List[User]
        reviews: List[Review]

    def __init__(self, movies: List[Movie]) -> None:
        self._movies = movies
        self._users: List[User] = []
        self._reviews: List[Review] = []

    @property
    def _movies(self):
        return self.__movies

    @_movies.setter
    def _movies(self, movies: List[Movie]):
        if not isinstance(movies, list) or any(not isinstance(movie, Movie) for movie in movies):
            raise TypeError(f"'movies' must be of type 'List[Movie]' but was '{type(movies).__name__}'")

        self.__movies = movies

    @property
    def movies(self):
        return self._movies

    @property
    def users(self):
        return self._users

    @property
    def reviews(self):
        return self._reviews

    @abstractmethod
    def simulate(self) -> State:
        """
        Simulates users watching movies and writing reviews.

        Returns:
            An AbstractMovieWatchingSimulation.State object containing a shallow copy of the simulation's state
        """
        raise NotImplemented

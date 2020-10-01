import abc
from typing import List
from datetime import date

from movie.domain.movie import Movie

repo = None

class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_movie(self, movie: Movie) -> None:
        """ Adds the given Movie to this repository. Does nothing if the given movie has already been added. """
        raise NotImplementedError

    def add_movies(self, movies: List[Movie]) -> None:
        """ Adds the given Movies to this repository. If a movie is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self) -> List[Movie]:
        """ Returns a list of all Movies in this repository ordered by title and then release date. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Returns the number of movies in this repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_page(self, page_number: int, page_size: int) -> List[Movie]:
        """ Returns a list containing the nth page of Movies in this repository ordered by title and then release date.

        Args:
            page_number (int): page number of the the page to return, starting from zero.
            page_size (int): number of results per page. The last page may have less results than this.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_page(self, page_number: int, page_size: int) -> List[Movie]:
        """ Returns a list containing the nth page of Movies in this repository ordered by title and then release date.

        Args:
            page_number (int): page number of the the page to return, starting from zero.
            page_size (int): number of results per page. The last page may have less results than this.
        """
        raise NotImplementedError

    def __repr__(self):
        return f'<{type(self).__name__}>'

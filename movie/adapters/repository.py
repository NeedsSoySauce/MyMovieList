import abc
from typing import List, Union

from movie.domain.movie import Movie
from movie.domain.genre import Genre
from movie.datafilereaders.movie_file_csv_reader import MovieFileCSVReader

instance: Union[None, 'AbstractRepository'] = None
""" Application wide repository instance. """


class AbstractRepository(abc.ABC):
    DEFAULT_PAGE_SIZE = 25

    @abc.abstractmethod
    def add_movie(self, movie: Movie) -> None:
        """ Adds the given Movie to this repository. Does nothing if the given movie has already been added. """
        raise NotImplementedError

    def add_movies(self, movies: List[Movie]) -> None:
        """ Adds the given Movies to this repository. If a movie is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre) -> None:
        """ Adds the given Genre to this repository. Does nothing if the given genre has already been added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genres(self, genre: List[Genre]) -> None:
        """ Adds the given Genres to this repository. If a genre is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self) -> int:
        """ Returns the number of movies in this repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self,
                   page_number: int,
                   page_size: int = DEFAULT_PAGE_SIZE,
                   query: str = "",
                   genres: List[Genre] = []) -> List[Movie]:
        """ Returns a list containing the nth page of Movies in this repository ordered by title and then release date.

        Args:
            page_number (int): page number of the the page to return, starting from zero.
            page_size (int, optional): number of results per page. The last page may have less results than this.
            query (str, optional): string to search for in a movie's title.
            genres (List[Genre], optional): genres to filter movies by. A movie must have all of the specified genres
                for it to be included in the results.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns a list containing all genres in this repository ordered by each genres name. """
        raise NotImplementedError

    def __repr__(self):
        return f'<{type(self).__name__}>'


def populate(repo: AbstractRepository, data_path: str):
    """ Populates the given repository with the data at the given path. """
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()
    repo.add_movies(reader.dataset_of_movies)
    repo.add_genres(reader.dataset_of_genres)

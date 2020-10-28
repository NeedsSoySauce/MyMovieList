from typing import Union, List, Iterator

from sqlalchemy.orm.collections import collection

from .movie import Movie


class WatchList:
    def __init__(self) -> None:
        self._movies: List[Movie] = []

    @collection.appender
    def add_movie(self, movie: Movie) -> None:
        """ Adds the given Movie to this WatchList. Does nothing if the given Movie is already in this Watchlist.  """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        if movie in self._movies:
            return

        self._movies.append(movie)

    @collection.remover
    def remove_movie(self, movie: Movie) -> None:
        """ Removes the given Movie from this WatchList. Does nothing if the given Movie isn't in this Watchlist.  """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")
        try:
            self._movies.remove(movie)
        except ValueError:
            return

    def select_movie_to_watch(self, index: int) -> Union[Movie, None]:
        """ Returns the Movie at the given index position of this WatchList or None if there is no Movie at that index.
        """
        try:
            return self._movies[index]
        except IndexError:
            return None

    def size(self) -> int:
        """ Returns the number of Movies int his WatchList. """
        return len(self._movies)

    def first_movie_in_watch_list(self) -> Union[Movie, None]:
        """ Returns the Movie at index position 0 of this WatchList or None if there are no Movies in this WatchList.
        """
        try:
            return self._movies[0]
        except IndexError:
            return None

    @collection.iterator
    def __iter__(self) -> Iterator[Movie]:
        return iter(self._movies)

    def __contains__(self, item):
        return item in self._movies

    def __repr__(self):
        return repr(self._movies)

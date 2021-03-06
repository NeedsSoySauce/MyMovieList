from datetime import datetime
from typing import List

from .movie import Movie
from .review import Review
from .watchlist import WatchList


class User:
    def __init__(self, username: str, password: str, id_: int = None) -> None:
        self._username = username
        self._password = password
        self._watched_movies: List[Movie] = []
        self._reviews: List[Review] = []
        self._time_spent_watching_movies_minutes: int = 0
        self._watchlist = WatchList()
        self._joined_on_utc = datetime.utcnow()
        self._id: int = id_ or hash(self)

    @property
    def _username(self):
        return self._mapped_username

    @_username.setter
    def _username(self, username):
        if username == "" or not isinstance(username, str):
            self._mapped_username = None
        else:
            self._mapped_username = username.strip()

    @property
    def _password(self):
        return self._mapped_password

    @_password.setter
    def _password(self, password):
        if not isinstance(password, str):
            raise TypeError(f"'password' must be of type 'str' but was '{type(password).__name__}'")
        self._mapped_password = password

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    @property
    def watchlist(self):
        return self._watchlist

    @property
    def id(self):
        return self._id

    @property
    def joined_on_utc(self):
        return self._joined_on_utc

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self._id}, {self._username}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self._username == other._username and self._password == other._password

    def __lt__(self, other) -> bool:
        if not isinstance(other, User):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self._username < other._username

    def __hash__(self) -> int:
        return hash(self._username)

    def watch_movie(self, movie: Movie) -> None:
        """
        Adds the given movie to this user's list of watched movies, updates time_spent_watching_movies_minutes, and
        removes the movie from this user's WatchList (if it's in their WatchList).
        """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        if movie in self._watched_movies:
            return

        self._watched_movies.append(movie)
        self._watchlist.remove_movie(movie)

        if isinstance(movie.runtime_minutes, int) and movie.runtime_minutes > 0:
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def remove_from_watched_movies(self, movie: Movie) -> None:
        """
        Removes the given movie to this user's list of watched movies and updates time_spent_watching_movies_minutes.
        Does nothing if this user hasn't watched the given movie.
        """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        try:
            self._watched_movies.remove(movie)
        except ValueError:
            # User hasn't watched this movie
            return

        if isinstance(movie.runtime_minutes, int) and movie.runtime_minutes > 0:
            self._time_spent_watching_movies_minutes -= movie.runtime_minutes

    def add_review(self, review: Review) -> None:
        """ Adds the given review to the list of reviews written by this user. """
        if not isinstance(review, Review):
            raise TypeError(f"'review' must be of type 'Review' but was '{type(review).__name__}'")

        if review in self._reviews:
            return

        self._reviews.append(review)

    def add_to_watchlist(self, movie: Movie) -> None:
        """ Adds the given movie to this user's WatchList. """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        self._watchlist.add_movie(movie)

    def remove_from_watchlist(self, movie: Movie) -> None:
        """ Removes the given movie from this user's WatchList. """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        self._watchlist.remove_movie(movie)

    def watchlist_size(self) -> int:
        """ Returns the number of movies in this user's WatchList. """
        return self._watchlist.size()

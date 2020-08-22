from typing import List

from domainmodel.movie import Movie
from domainmodel.review import Review


class User:
    def __init__(self, user_name: str, password: str) -> None:
        self._user_name = user_name
        self._password = password
        self._watched_movies: List[Movie] = []
        self._reviews: List[Review] = []
        self._time_spent_watching_movies_minutes: int = 0

    @property
    def _user_name(self):
        return self.__user_name

    @_user_name.setter
    def _user_name(self, user_name):
        if user_name == "" or not isinstance(user_name, str):
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()

    @property
    def _password(self):
        return self.__password

    @_password.setter
    def _password(self, password):
        if not isinstance(password, str):
            raise TypeError(f"'password' must be of type 'str' but was '{type(password).__name__}'")
        self.__password = password

    @property
    def user_name(self):
        return self._user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self._watched_movies

    @property
    def reviews(self):
        return self._reviews

    @property
    def time_spent_watching_movies_minutes(self):
        return self._time_spent_watching_movies_minutes

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self._user_name}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self._user_name == other._user_name and self._password == other._password

    def __lt__(self, other) -> bool:
        if not isinstance(other, User):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return self._user_name < other._user_name

    def __hash__(self) -> int:
        return hash(self._user_name)

    def watch_movie(self, movie: Movie) -> None:
        """ Adds the given movie to this user's list of watched movies and updates time_spent_watching_movies_minutes.
        """
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        if movie in self._watched_movies:
            return

        self._watched_movies.append(movie)

        if isinstance(movie.runtime_minutes, int) and movie.runtime_minutes > 0:
            self._time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review) -> None:
        """ Adds the given review to the list of reviews written by this user. """
        if not isinstance(review, Review):
            raise TypeError(f"'review' must be of type 'Review' but was '{type(review).__name__}'")

        if review in self._reviews:
            return

        self._reviews.append(review)

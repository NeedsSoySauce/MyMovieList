from datetime import datetime

from .movie import Movie

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User


class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int, timestamp: datetime = None,
                 user: 'User' = None, id_: int = None) -> None:
        self._user = user
        self._movie = movie
        self._review_text = review_text
        self._rating = rating
        self._timestamp = timestamp or datetime.utcnow()
        self._id = id_

    @property
    def _movie(self):
        return self._mapped_movie

    @_movie.setter
    def _movie(self, movie: Movie):
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")
        self._mapped_movie = movie

    @property
    def _review_text(self):
        return self._mapped_review_text

    @_review_text.setter
    def _review_text(self, review_text):
        if review_text == "" or not isinstance(review_text, str):
            self._mapped_review_text = None
        else:
            self._mapped_review_text = review_text.strip()

    @property
    def _rating(self):
        return self._mapped_rating

    @_rating.setter
    def _rating(self, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 10:
            self._mapped_rating = None
        else:
            self._mapped_rating = rating

    @property
    def _timestamp(self):
        return self._mapped_timestamp

    @_timestamp.setter
    def _timestamp(self, timestamp):
        if not isinstance(timestamp, datetime):
            raise TypeError(f"'timestamp' must be of type 'datetime' but was '{type(timestamp).__name__}'")
        else:
            self._mapped_timestamp = timestamp

    @property
    def movie(self):
        return self._movie

    @property
    def review_text(self):
        return self._review_text

    @property
    def rating(self):
        return self._rating

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def user(self):
        return self._user

    @property
    def id(self):
        return self._id

    def __hash__(self):
        return hash(f'{self._movie}{self._review_text}{self._rating}{self._timestamp}')

    def __lt__(self, other):
        if not isinstance(other, Review):
            raise TypeError(
                f"'<' not supported between instances of '{type(self).__name__}' and '{type(other).__name__}'")
        return other._timestamp < self._timestamp

    def __repr__(self) -> str:
        return (
            f'<{type(self).__name__} {self._movie}, {self._review_text}, {self._rating}, {self._timestamp.isoformat()},'
            f' {self._user}>'
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return (
                self._movie == other._movie and
                self._review_text == other._review_text and
                self._rating == other._rating and
                self._timestamp == other._timestamp
        )

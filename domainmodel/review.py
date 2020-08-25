from datetime import datetime

from domainmodel.movie import Movie


class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int, timestamp: datetime = None) -> None:
        self._movie = movie
        self._review_text = review_text
        self._rating = rating
        self._timestamp = timestamp or datetime.utcnow()

    @property
    def _movie(self):
        return self.__movie

    @_movie.setter
    def _movie(self, movie):
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")
        self.__movie = movie

    @property
    def _review_text(self):
        return self.__review_text

    @_review_text.setter
    def _review_text(self, review_text):
        if review_text == "" or not isinstance(review_text, str):
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()

    @property
    def _rating(self):
        return self.__rating

    @_rating.setter
    def _rating(self, rating):
        if not isinstance(rating, int) or rating < 1 or rating > 10:
            self.__rating = None
        else:
            self.__rating = rating

    @property
    def _timestamp(self):
        return self.__timestamp

    @_timestamp.setter
    def _timestamp(self, timestamp):
        if not isinstance(timestamp, datetime):
            raise TypeError(f"'timestamp' must be of type 'datetime' but was '{type(timestamp).__name__}'")
        else:
            self.__timestamp = timestamp

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

    def __repr__(self) -> str:
        return f'<{type(self).__name__} {self._movie}, {self._review_text}, {self._rating}, {self._timestamp.isoformat()}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, Review):
            return False
        return (
                self._movie == other._movie and
                self._review_text == other._review_text and
                self._rating == other._rating and
                self._timestamp == other._timestamp
        )

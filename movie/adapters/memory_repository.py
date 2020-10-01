from typing import List

from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie

from bisect import insort
from math import ceil


class MemoryRepository(AbstractRepository):
    DEFAULT_PAGE_SIZE = 25

    def __init__(self):
        self._movies: List[Movie] = []
        self._number_of_movies: int = 0

    def add_movie(self, movie: Movie) -> None:
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        if movie in self._movies:
            return

        insort(self._movies, movie)
        self._number_of_movies += 1

    def add_movies(self, movies: List[Movie]) -> None:
        if not isinstance(movies, list):
            raise TypeError(f"'movies' must be of type 'List[Movie]' but was '{type(movies).__name__}'")

        for movie in movies:
            self.add_movie(movie)

    def get_movies(self) -> List[Movie]:
        return self._movies

    def get_number_of_movies(self) -> int:
        return self._number_of_movies

    def get_movies_page(self, page_number: int, page_size: int = DEFAULT_PAGE_SIZE) -> List[Movie]:
        if not isinstance(page_number, int):
            raise TypeError(f"'page_number' must be of type 'int' but was '{type(page_number).__name__}'")

        if not isinstance(page_size, int):
            raise TypeError(f"'page_size' must be of type 'int' but was '{type(page_size).__name__}'")

        if page_number < 0:
            raise ValueError(f"'page_number' must be at least zero but was {page_number}")

        if page_size < 1:
            raise ValueError(f"'page_size' must be at least 1 but was {page_size}")

        # If there arent enough movies to create an nth page of the given size
        if ceil(self._number_of_movies / page_size) <= page_number:
            raise ValueError("insufficient data to create page")

        offset = page_number * page_size
        return self._movies[offset:min(offset + page_size, self._number_of_movies)]

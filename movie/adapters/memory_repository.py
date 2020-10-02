from typing import List

from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie
from movie.domain.movie import Genre

from bisect import insort
from math import ceil


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies: List[Movie] = []
        self._number_of_movies: int = 0
        self._genres: List[Genre] = []

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

    def add_genre(self, genre: Genre):
        if not isinstance(genre, Genre):
            raise TypeError(f"'genre' must be of type 'Genre' but was '{type(genre).__name__}'")

        if genre in self._genres:
            return

        insort(self._genres, genre)

    def add_genres(self, genres: List[Genre]) -> None:
        if not isinstance(genres, list):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        for genre in genres:
            self.add_genre(genre)

    def get_number_of_movies(self) -> int:
        return self._number_of_movies

    def get_movies(self,
                   page_number: int,
                   page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                   genres: List[Genre] = []) -> List[Movie]:
        if not isinstance(page_number, int):
            raise TypeError(f"'page_number' must be of type 'int' but was '{type(page_number).__name__}'")

        if not isinstance(page_size, int):
            raise TypeError(f"'page_size' must be of type 'int' but was '{type(page_size).__name__}'")

        if not isinstance(genres, list) or any(not isinstance(genre, Genre) for genre in genres):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        if page_number < 0:
            raise ValueError(f"'page_number' must be at least zero but was {page_number}")

        if page_size < 1:
            raise ValueError(f"'page_size' must be at least 1 but was {page_size}")

        filtered = self._movies

        if genres:
            filtered = list(filter(lambda x: all(genre in x.genres for genre in genres), filtered))

        # If there arent enough movies to create an nth page of the given size
        if ceil(len(filtered) / page_size) <= page_number:
            raise ValueError("insufficient data to create page")

        offset = page_number * page_size
        return filtered[offset:min(offset + page_size, self._number_of_movies)]

    def get_genres(self) -> List[Genre]:
        return self._genres

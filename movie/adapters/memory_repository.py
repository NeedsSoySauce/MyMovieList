from typing import List, Dict, Optional

from movie.adapters.repository import AbstractRepository
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.movie import Movie
from movie.domain.movie import Genre

from bisect import insort
from math import ceil
from fuzzywuzzy import fuzz


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies: List[Movie] = []
        self._genres: List[Genre] = []
        self._genre_map: Dict[str, Genre] = {}
        self._directors: List[Director] = []
        self._director_map: Dict[str, Director] = {}
        self._actors: List[Actor] = []
        self._actor_map: Dict[str, Actor] = {}

    def add_movie(self, movie: Movie) -> None:
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        if movie in self._movies:
            return

        insort(self._movies, movie)

        if movie.genres:
            self.add_genres(movie.genres)

        if movie.actors:
            self.add_actors(movie.actors)

        if movie.director:
            self.add_director(movie.director)

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
        self._genre_map[genre.genre_name.lower()] = genre

    def add_genres(self, genres: List[Genre]) -> None:
        if not isinstance(genres, list):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        for genre in genres:
            self.add_genre(genre)

    def get_genre(self, genre_name: str) -> Genre:
        try:
            return self._genre_map[genre_name.lower()]
        except KeyError:
            raise ValueError(f"No genre with the name '{genre_name}'")

    def add_director(self, director: Director) -> None:
        if not isinstance(director, Director):
            raise TypeError(f"'director' must be of type 'Director' but was '{type(director).__name__}'")

        if director in self._directors:
            return

        insort(self._directors, director)
        self._director_map[director.director_full_name.lower()] = director

    def add_directors(self, directors: List[Director]) -> None:
        if not isinstance(directors, list):
            raise TypeError(f"'directors' must be of type 'List[Director]' but was '{type(directors).__name__}'")

        for director in directors:
            self.add_director(director)

    def get_director(self, director_name: str) -> Director:
        try:
            return self._director_map[director_name.lower()]
        except KeyError:
            raise ValueError(f"No director with the name '{director_name}'")

    def add_actor(self, actor: Actor) -> None:
        if not isinstance(actor, Actor):
            raise TypeError(f"'actor' must be of type 'Actor' but was '{type(actor).__name__}'")

        if actor in self._actors:
            return

        insort(self._actors, actor)
        self._actor_map[actor.actor_full_name.lower()] = actor

    def add_actors(self, actors: List[Actor]) -> None:
        if not isinstance(actors, list):
            raise TypeError(f"'actors' must be of type 'List[Actor]' but was '{type(actors).__name__}'")

        for actor in actors:
            self.add_actor(actor)

    def get_actor(self, actor_name: str) -> Actor:
        try:
            return self._actor_map[actor_name.lower()]
        except KeyError:
            raise ValueError(f"No actor with the name '{actor_name}'")

    @staticmethod
    def _query_filter(movie: Movie, query: str = "", min_ratio: int = 80) -> bool:

        title = movie.title.lower()
        director = movie.director.director_full_name.lower()
        description = movie.description.lower()
        genres = [genre.genre_name.lower() for genre in movie.genres]
        actors = [actor.actor_full_name.lower() for actor in movie.actors]

        movie_str = " ".join([title, director, description] + genres + actors)

        return fuzz.token_set_ratio(query, movie_str) >= min_ratio

    def _get_filtered_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             director: Optional[Director] = None,
                             actors: List[Actor] = []) -> List[Movie]:

        filtered = self._movies

        _query = query.strip().lower()
        if _query:
            filtered = filter(lambda x: self._query_filter(x, _query), filtered)

        if genres:
            filtered = filter(lambda x: all(genre in x.genres for genre in genres), filtered)

        if director:
            filtered = filter(lambda x: director == x.director, filtered)

        if actors:
            filtered = filter(lambda x: all(actor in x.actors for actor in actors), filtered)

        return list(filtered)

    def get_number_of_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             director: Optional[Director] = None,
                             actors: List[Actor] = []) -> int:
        return len(self._get_filtered_movies(query, genres, director, actors))

    def get_number_of_pages(self,
                            page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                            query: str = "",
                            genres: List[Genre] = [],
                            director: Optional[Director] = None,
                            actors: List[Actor] = []) -> int:
        return ceil(self.get_number_of_movies(query, genres, director, actors) / page_size)

    def get_movies(self,
                   page_number: int,
                   page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                   query: str = "",
                   genres: List[Genre] = [],
                   director: Optional[Director] = None,
                   actors: List[Actor] = []) -> List[Movie]:

        if not isinstance(page_number, int):
            raise TypeError(f"'page_number' must be of type 'int' but was '{type(page_number).__name__}'")

        if not isinstance(page_size, int):
            raise TypeError(f"'page_size' must be of type 'int' but was '{type(page_size).__name__}'")

        if not isinstance(query, str):
            raise TypeError(f"'query' must be of type 'str' but was '{type(query).__name__}'")

        if not isinstance(genres, list) or any(not isinstance(genre, Genre) for genre in genres):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        if director is not None and not isinstance(director, Director):
            raise TypeError(f"'director' must be of type 'Director' or None but was '{type(director).__name__}'")

        if not isinstance(actors, list) or any(not isinstance(actors, Actor) for actors in actors):
            raise TypeError(f"'actors' must be of type 'List[Actor]' but was '{type(genres).__name__}'")

        if page_number < 0:
            raise ValueError(f"'page_number' must be at least zero but was {page_number}")

        if page_size < 1:
            raise ValueError(f"'page_size' must be at least 1 but was {page_size}")

        filtered = self._get_filtered_movies(query, genres, director, actors)

        offset = page_number * page_size
        return filtered[offset:min(offset + page_size, len(self._movies))]

    def get_genres(self) -> List[Genre]:
        return self._genres

    def get_directors(self) -> List[Director]:
        return self._directors

    def get_actors(self) -> List[Actor]:
        return self._actors

from typing import List, Dict, Optional, Union

from movie.adapters.repository import AbstractRepository
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.movie import Movie
from movie.domain.movie import Genre

from bisect import insort
from math import ceil
from fuzzywuzzy import fuzz

from movie.domain.review import Review
from movie.domain.user import User

from collections import defaultdict


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self._movies: List[Movie] = []
        self._movie_map: Dict[int, Movie] = {}
        self._genres: List[Genre] = []
        self._genre_map: Dict[str, Genre] = {}
        self._directors: List[Director] = []
        self._director_map: Dict[str, Director] = {}
        self._actors: List[Actor] = []
        self._actor_map: Dict[str, Actor] = {}
        self._users: List[User] = []
        self._user_id_map: Dict[str, int] = {}  # maps usernames to a user id
        self._user_map: Dict[int, User] = {}  # maps user ids to a User
        self._reviews: List[Review] = []
        self._reviews_movie_map: Dict[Movie, List[Review]] = defaultdict(list)
        self._reviews_user_map: Dict[Review, Union[User, None]] = {}

    def add_movie(self, movie: Movie) -> None:
        if not isinstance(movie, Movie):
            raise TypeError(f"'movie' must be of type 'Movie' but was '{type(movie).__name__}'")

        if movie in self._movies:
            return

        insort(self._movies, movie)
        self._movie_map[movie.id] = movie

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

    def add_user(self, user: User) -> None:
        if not isinstance(user, User):
            raise TypeError(f"'user' must be of type 'User' but was '{type(user).__name__}'")

        if user in self._users:
            return

        insort(self._users, user)
        self._user_id_map[user.user_name] = user.id
        self._user_map[user.id] = user

        if user.reviews:
            for review in user.reviews:
                self._reviews_user_map[review] = user

    def add_users(self, users: List[User]) -> None:
        if not isinstance(users, list):
            raise TypeError(f"'users' must be of type 'List[User]' but was '{type(users).__name__}'")

        for user in users:
            self.add_user(user)

    def get_user(self, user_name: str) -> User:
        try:
            return self._user_map[self._user_id_map[user_name]]
        except KeyError:
            raise ValueError(f"No user with the name '{user_name}'")

    def update_username(self, user: User, new_username: str) -> None:
        # Update the mapping from username to user id
        del self._user_id_map[user.user_name]
        self._user_id_map[new_username] = user.id
        user.user_name = new_username

    def add_review(self, review: Review, user: Union[User, None] = None) -> None:
        if review in self._reviews:
            return
        insort(self._reviews, review)
        insort(self._reviews_movie_map[review.movie], review)
        if user:
            self._reviews_user_map[review] = user

    def add_reviews(self, reviews: List[Review]) -> None:
        for review in reviews:
            self.add_review(review)

    def get_movie_reviews(self, movie: Movie) -> List[Review]:
        return self._reviews_movie_map[movie]

    def get_review_user(self, review: Review) -> Union[User, None]:
        try:
            return self._reviews_user_map[review]
        except KeyError:
            return None

    @staticmethod
    def _query_filter(movie: Movie, query: str = "", min_ratio: int = 80) -> bool:

        title = movie.title.lower()
        director = movie.director.director_full_name.lower() if movie.director else ''
        description = movie.description.lower() if movie.description else ''
        genres = [genre.genre_name.lower() for genre in movie.genres] if movie.genres else []
        actors = [actor.actor_full_name.lower() for actor in movie.actors] if movie.actors else []

        movie_str = " ".join([title, director, description] + genres + actors)

        return fuzz.token_set_ratio(query, movie_str) >= min_ratio

    def _get_filtered_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             directors: List[Director] = [],
                             actors: List[Actor] = []) -> List[Movie]:

        filtered = self._movies

        _query = query.strip().lower()
        if _query:
            filtered = filter(lambda x: self._query_filter(x, _query), filtered)

        if genres:
            filtered = filter(lambda x: all(genre in x.genres for genre in genres), filtered)

        if directors:
            filtered = filter(lambda x: any(director == x.director for director in directors), filtered)

        if actors:
            filtered = filter(lambda x: all(actor in x.actors for actor in actors), filtered)

        return list(filtered)

    def get_number_of_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             directors: List[Director] = [],
                             actors: List[Actor] = []) -> int:
        return len(self._get_filtered_movies(query, genres, directors, actors))

    def get_number_of_pages(self,
                            page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                            query: str = "",
                            genres: List[Genre] = [],
                            directors: List[Director] = [],
                            actors: List[Actor] = []) -> int:
        return ceil(self.get_number_of_movies(query, genres, directors, actors) / page_size)

    def get_movies(self,
                   page_number: int,
                   page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                   query: str = "",
                   genres: List[Genre] = [],
                   directors: List[Director] = [],
                   actors: List[Actor] = []) -> List[Movie]:

        if not isinstance(page_number, int):
            raise TypeError(f"'page_number' must be of type 'int' but was '{type(page_number).__name__}'")

        if not isinstance(page_size, int):
            raise TypeError(f"'page_size' must be of type 'int' but was '{type(page_size).__name__}'")

        if not isinstance(query, str):
            raise TypeError(f"'query' must be of type 'str' but was '{type(query).__name__}'")

        if not isinstance(genres, list) or any(not isinstance(genre, Genre) for genre in genres):
            raise TypeError(f"'genres' must be of type 'List[Genre]' but was '{type(genres).__name__}'")

        if not isinstance(directors, list) or any(not isinstance(director, Director) for director in directors):
            raise TypeError(f"'directors' must be of type 'List[Director]' but was '{type(directors).__name__}'")

        if not isinstance(actors, list) or any(not isinstance(actors, Actor) for actors in actors):
            raise TypeError(f"'actors' must be of type 'List[Actor]' but was '{type(genres).__name__}'")

        if page_number < 0:
            raise ValueError(f"'page_number' must be at least zero but was {page_number}")

        if page_size < 1:
            raise ValueError(f"'page_size' must be at least 1 but was {page_size}")

        filtered = self._get_filtered_movies(query, genres, directors, actors)

        offset = page_number * page_size
        return filtered[offset:min(offset + page_size, len(self._movies))]

    def get_movie_by_id(self, movie_id: int) -> Movie:
        try:
            return self._movie_map[movie_id]
        except KeyError:
            raise ValueError(f"no movie with the id '{movie_id}'")

    def get_genres(self) -> List[Genre]:
        return self._genres

    def get_directors(self) -> List[Director]:
        return self._directors

    def get_actors(self) -> List[Actor]:
        return self._actors

    def get_movies_per_genre(self) -> Dict[Genre, int]:
        movies_per_genre: Dict[Genre, int] = defaultdict(int)

        for movie in self._movies:
            if movie.genres:
                for genre in movie.genres:
                    movies_per_genre[genre] += 1

        return movies_per_genre

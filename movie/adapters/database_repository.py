from typing import List, Dict, Union, Optional

from flask import _app_ctx_stack
from sqlalchemy import any_, func, or_
from sqlalchemy.orm import scoped_session, Session, Query
from werkzeug.security import generate_password_hash

from movie.activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from movie.adapters.orm import movie_genres, movie_actors
from movie.adapters.repository import AbstractRepository
from movie.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    # Doesn't return a session, but typing this as returning a session provides better IDE suggestions
    @property
    def session(self) -> Session:
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if self.__session is not None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_movie(self, movie: Movie) -> None:
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def add_movies(self, movies: List[Movie]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(movies)
            scm.commit()

    def add_genre(self, genre: Genre) -> None:
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def add_genres(self, genres: List[Genre]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(genres)
            scm.commit()

    def get_genre(self, genre_name: str) -> Genre:
        raise NotImplementedError

    def add_director(self, director: Director) -> None:
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def add_directors(self, directors: List[Director]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(directors)
            scm.commit()

    def get_director(self, director_name: str) -> Director:
        raise NotImplementedError

    def add_actor(self, actor: Actor) -> None:
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def add_actors(self, actors: List[Actor]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(actors)
            scm.commit()

    def get_actor(self, actor_name: str) -> Actor:
        raise NotImplementedError

    def add_user(self, user: User) -> None:
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_users(self, users: List[User]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(users)
            scm.commit()

    def get_user(self, username: str) -> User:
        raise NotImplementedError

    def delete_user(self, user: User) -> None:
        raise NotImplementedError

    def update_username(self, user: User, new_username: str) -> None:
        raise NotImplementedError

    def add_review(self, review: Review, user: Union[User, None] = None) -> None:
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_reviews(self, reviews: List[Review]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(reviews)
            scm.commit()

    def get_review_user(self, review: Review) -> Union[User, None]:
        raise NotImplementedError

    def get_number_of_reviews_for_movie(self, movie: Movie) -> int:
        raise NotImplementedError

    def get_number_of_review_pages_for_movie(self,
                                             movie: Movie,
                                             page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> int:
        raise NotImplementedError

    def get_reviews_for_movie(self,
                              movie: Movie,
                              page_number: int,
                              page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> List[Review]:
        raise NotImplementedError

    def get_number_of_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             directors: List[Director] = [],
                             actors: List[Actor] = []) -> int:
        with self._session_cm as scm:
            return scm.session.query(Movie).count()

    def get_number_of_movie_pages(self,
                                  page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                                  query: str = "",
                                  genres: List[Genre] = [],
                                  directors: List[Director] = [],
                                  actors: List[Actor] = []) -> int:
        raise NotImplementedError

    @staticmethod
    def _get_filtered_movies(session: Session,
                             query: str = "",
                             genres: List[Genre] = [],
                             directors: List[Director] = [],
                             actors: List[Actor] = []) -> Query:
        filtered: Query = session.query(Movie). \
            outerjoin(Director). \
            outerjoin(movie_genres). \
            outerjoin(Genre). \
            outerjoin(movie_actors). \
            outerjoin(Actor). \
            group_by(Movie._id)

        # title = movie.title.lower()
        # director = movie.director.director_full_name.lower() if movie.director else ''
        # description = movie.description.lower() if movie.description else ''
        # genres = [genre.genre_name.lower() for genre in movie.genres] if movie.genres else []
        # actors = [actor.actor_full_name.lower() for actor in movie.actors] if movie.actors else []
        # movie_str = " ".join([title, director, description] + genres + actors)

        # TODO - setup query search
        # TODO - test if filtering with a query and genres, etc, works!

        _query = query.strip()
        if _query:
            _query = f'%{_query}%'
            filtered = filtered. \
                filter(or_(
                Movie._mapped_title.ilike(_query),
                Movie._description.ilike(_query),
                Director._person_full_name.ilike(_query),
                Genre._genre_name.ilike(_query),
                Actor._person_full_name.ilike(_query)
            ))

        if genres:
            genre_names = [genre.genre_name for genre in genres]
            filtered = filtered. \
                filter(Genre._genre_name.in_(genre_names)). \
                having(func.count(Genre._genre_name.distinct()) == len(genre_names))

        # if directors:
        #     filtered = filter(lambda x: any(director == x.director for director in directors), filtered)
        #
        # if actors:
        #     filtered = filter(lambda x: all(actor in x.actors for actor in actors), filtered)

        print(filtered.statement.compile())

        return filtered

    def get_movies(self,
                   page_number: int,
                   page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                   query: str = "",
                   genres: List[Genre] = [],
                   directors: List[Director] = [],
                   actors: List[Actor] = []) -> List[Movie]:
        self._check_get_movies_args(page_number, page_size, query, genres, directors, actors)

        offset = page_number * page_size

        with self._session_cm as scm:
            return self._get_filtered_movies(scm.session, query, genres, directors, actors). \
                limit(page_size). \
                offset(offset). \
                all()

    def _get_all_movies(self) -> List[Movie]:
        """ For testing and debugging. Returns all the movies in this repository. """

        with self._session_cm as scm:
            return scm.session.query(Movie).all()

    def get_number_of_movies_for_user(self, user: User) -> int:
        raise NotImplementedError

    def get_number_of_movie_pages_for_user(self,
                                           user: User,
                                           page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> int:
        raise NotImplementedError

    def get_movies_for_user(self,
                            user: User,
                            page_number: int,
                            page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> List[Movie]:
        raise NotImplementedError

    def get_movie_by_id(self, movie_id: int) -> Movie:
        raise NotImplementedError

    def get_genres(self) -> List[Genre]:
        with self._session_cm as scm:
            return scm.session.query(Genre).all()

    def get_directors(self) -> List[Director]:
        raise NotImplementedError

    def get_actors(self) -> List[Actor]:
        raise NotImplementedError

    def get_movies_per_genre(self) -> Dict[Genre, int]:
        raise NotImplementedError


def populate(repo: AbstractRepository, data_path: str, seed: Optional[int] = None):
    """ Populates the given repository using data at the given path. """
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()

    sim = MovieWatchingSimulation(reader.dataset_of_movies, seed)
    state = sim.simulate(num_users=50, min_num_movies=10, max_num_movies=20)

    repo.add_genres(reader.dataset_of_genres)
    repo.add_directors(reader.dataset_of_directors)
    repo.add_actors(reader.dataset_of_actors)
    repo.add_movies(reader.dataset_of_movies)
    repo.add_users(state.users)
    repo.add_reviews(state.reviews)

    test_user = User('testuser', generate_password_hash('test123A'))
    repo.add_user(test_user)

    test_user2 = User('testuser2', generate_password_hash('test123A'))
    repo.add_user(test_user2)

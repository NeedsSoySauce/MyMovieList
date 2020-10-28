from math import ceil
from typing import List, Dict, Union, Optional

from flask import _app_ctx_stack
from sqlalchemy import func, or_, case
from sqlalchemy.orm import scoped_session, Session, Query
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.security import generate_password_hash

from cache import cache
from movie.activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from movie.adapters.orm import movie_genres, movie_actors, user_watched_movies, user_watchlist_movies
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
        self.__session: Session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

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
        with self._session_cm as scm:
            try:
                return scm.session.query(Genre).filter(Genre._genre_name == genre_name).one()
            except NoResultFound:
                raise ValueError

    def add_director(self, director: Director) -> None:
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def add_directors(self, directors: List[Director]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(directors)
            scm.commit()

    def get_director(self, director_name: str) -> Director:
        with self._session_cm as scm:
            try:
                return scm.session.query(Director).filter(Director._person_full_name == director_name).one()
            except NoResultFound:
                raise ValueError

    def add_actor(self, actor: Actor) -> None:
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def add_actors(self, actors: List[Actor]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(actors)
            scm.commit()

    def get_actor(self, actor_name: str) -> Actor:
        with self._session_cm as scm:
            try:
                return scm.session.query(Actor).filter(Actor._person_full_name == actor_name).one()
            except NoResultFound:
                raise ValueError

    def add_user(self, user: User) -> None:
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def add_users(self, users: List[User]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(users)
            scm.commit()

    def get_user(self, username: str) -> User:
        with self._session_cm as scm:
            try:
                return scm.session.query(User).filter(User._mapped_username == username).one()
            except NoResultFound:
                raise ValueError

    def delete_user(self, user: User) -> None:
        with self._session_cm as scm:
            scm.session.delete(user)
            scm.session.commit()

    def change_username(self, user: User, new_username: str) -> None:
        with self._session_cm as scm:
            user.username = new_username
            scm.session.commit()

    def change_password(self, user: User, new_password: str) -> None:
        with self._session_cm as scm:
            user.password = new_password
            scm.session.commit()

    def add_movie_to_watched(self, user: User, movie: Movie) -> None:
        with self._session_cm as scm:
            user.add_to_watchlist(movie)
            user.watch_movie(movie)
            scm.session.commit()

    def remove_from_watched(self, user: User, movie: Movie) -> None:
        with self._session_cm as scm:
            user.remove_from_watched_movies(movie)
            scm.session.commit()

    def add_movie_to_watchlist(self, user: User, movie: Movie) -> None:
        with self._session_cm as scm:
            user.add_to_watchlist(movie)
            scm.session.commit()

    def remove_from_watchlist(self, user: User, movie: Movie) -> None:
        with self._session_cm as scm:
            user.remove_from_watchlist(movie)
            scm.session.commit()

    def add_review(self, review: Review, user: Union[User, None] = None) -> None:
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

    def add_reviews(self, reviews: List[Review]) -> None:
        with self._session_cm as scm:
            scm.session.add_all(reviews)
            scm.commit()

    def get_review_user(self, review: Review) -> Union[User, None]:
        return review.user

    @staticmethod
    def _get_page(query: Query, page_number: int, page_size: int) -> List:
        offset = page_number * page_size
        return query.limit(page_size).offset(offset).all()

    @staticmethod
    def _get_reviews_for_movie_query(session: Session, movie: Movie) -> Query:
        return session.query(Review).join(Movie).filter(Movie._id == movie.id).order_by(Review._mapped_timestamp.desc())

    def get_number_of_reviews_for_movie(self, movie: Movie) -> int:
        with self._session_cm as scm:
            return self._get_reviews_for_movie_query(scm.session, movie).count()

    def get_number_of_review_pages_for_movie(self,
                                             movie: Movie,
                                             page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> int:
        return self._get_number_of_pages(self.get_number_of_reviews_for_movie(movie), page_size)

    def get_reviews_for_movie(self,
                              movie: Movie,
                              page_number: int,
                              page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> List[Review]:
        with self._session_cm as scm:
            return self._get_page(self._get_reviews_for_movie_query(scm.session, movie), page_number, page_size)

    @staticmethod
    def _get_number_of_pages(number_of_elements: int, page_size: int) -> int:
        return ceil(number_of_elements / page_size)

    def get_number_of_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             directors: List[Director] = [],
                             actors: List[Actor] = []) -> int:
        with self._session_cm as scm:
            return self._get_filtered_movies_query(scm.session, query, genres, directors, actors).count()

    def get_number_of_movie_pages(self,
                                  page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                                  query: str = "",
                                  genres: List[Genre] = [],
                                  directors: List[Director] = [],
                                  actors: List[Actor] = []) -> int:
        return self._get_number_of_pages(self.get_number_of_movies(query, genres, directors, actors), page_size)

    @staticmethod
    def _get_filtered_movies_query(session: Session,
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
            group_by(Movie._id). \
            order_by(Movie._mapped_title, Movie._mapped_release_date)

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

        if directors:
            director_names = [director.director_full_name for director in directors]
            filtered = filtered.filter(Director._person_full_name.in_(director_names))

        if actors:
            actor_names = [actor.actor_full_name for actor in actors]
            filtered = filtered. \
                filter(Actor._person_full_name.in_(actor_names)). \
                having(func.count(Actor._person_full_name.distinct()) == len(actor_names))

        return filtered

    def get_movies(self,
                   page_number: int,
                   page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE,
                   query: str = "",
                   genres: List[Genre] = [],
                   directors: List[Director] = [],
                   actors: List[Actor] = []) -> List[Movie]:
        self._check_get_movies_args(page_number, page_size, query, genres, directors, actors)

        with self._session_cm as scm:
            return self._get_page(self._get_filtered_movies_query(scm.session, query, genres, directors, actors),
                                  page_number, page_size)

    def _get_all_movies(self) -> List[Movie]:
        """ For testing and debugging. Returns all the movies in this repository. """

        with self._session_cm as scm:
            return scm.session.query(Movie).all()

    def _get_all_reviews(self) -> List[Review]:
        """ For testing and debugging. Returns all the reviews in this repository. """

        with self._session_cm as scm:
            return scm.session.query(Review).all()

    def _get_movies_for_user_query(self, user: User) -> Query:
        with self._session_cm as scm:
            session = scm.session

            subquery = session.query(user_watched_movies).union(session.query(user_watchlist_movies)).subquery()

            query = session.query(Movie). \
                join(subquery). \
                join(User). \
                filter(User._id == user.id). \
                order_by(Movie._mapped_title, Movie._mapped_release_date)

            return query

    def get_number_of_movies_for_user(self, user: User) -> int:
        return self._get_movies_for_user_query(user).count()

    def get_number_of_movie_pages_for_user(self,
                                           user: User,
                                           page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> int:
        return self._get_number_of_pages(self.get_number_of_movies_for_user(user), page_size)

    def get_movies_for_user(self,
                            user: User,
                            page_number: int,
                            page_size: int = AbstractRepository.DEFAULT_PAGE_SIZE) -> List[Movie]:
        return self._get_page(self._get_movies_for_user_query(user), page_number, page_size)

    def get_movie_by_id(self, movie_id: int) -> Movie:
        with self._session_cm as scm:
            movie = scm.session.query(Movie).get(movie_id)

        if movie is None:
            raise ValueError

        return movie

    # These methods are cached as otherwise things can get quite slow as they're called to populate the search form

    @cache.memoize(timeout=30)
    def get_genres(self) -> List[Genre]:
        with self._session_cm as scm:
            genres = scm.session.query(Genre).order_by(Genre._genre_name).all()
            scm.session.expunge_all()
            return genres

    @cache.memoize(timeout=30)
    def get_directors(self) -> List[Director]:
        with self._session_cm as scm:
            directors = scm.session.query(Director).order_by(Director._person_full_name).all()
            scm.session.expunge_all()
            return directors

    @cache.memoize(timeout=30)
    def get_actors(self) -> List[Actor]:
        with self._session_cm as scm:
            actors = scm.session.query(Actor).order_by(Actor._person_full_name).all()
            scm.session.expunge_all()
            return actors

    def get_movies_per_genre(self) -> Dict[Genre, int]:
        with self._session_cm as scm:
            rows = scm.session.query(Genre, func.sum(
                case(
                    [
                        (movie_genres.c.movie_id == None, 0)
                    ],
                    else_=1
                )
            )). \
                outerjoin(movie_genres). \
                group_by(Genre._genre_name). \
                all()

        return {row[0]: row[1] for row in rows}


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

import abc
from typing import List, Union, Dict

from werkzeug.security import generate_password_hash

from movie.activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from movie.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User


class AbstractRepository(abc.ABC):
    DEFAULT_PAGE_SIZE = 25

    @abc.abstractmethod
    def add_movie(self, movie: Movie) -> None:
        """ Adds the given Movie to this repository. Does nothing if the given movie has already been added. """
        raise NotImplementedError

    def add_movies(self, movies: List[Movie]) -> None:
        """ Adds the given Movies to this repository. If a movie is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre) -> None:
        """ Adds the given Genre to this repository. Does nothing if the given genre has already been added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genres(self, genre: List[Genre]) -> None:
        """ Adds the given Genres to this repository. If a genre is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genre(self, genre_name: str) -> Genre:
        """
        Returns the Genre with the given name in this repository. Note: this is case insensitive.

        Raises:
            ValueError: if there is no Genre in this repository with the given name
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director) -> None:
        """ Adds the given Director to this repository. Does nothing if the given director has already been added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_directors(self, directors: List[Director]) -> None:
        """ Adds the given Directors to this repository. If a director is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_director(self, director_name: str) -> Director:
        """
        Returns the Director with the given name in this repository. Note: this is case insensitive.

        Raises:
            ValueError: if there is no Director in this repository with the given name
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor) -> None:
        """ Adds the given Actor to this repository. Does nothing if the given actor has already been added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actors(self, actors: List[Actor]) -> None:
        """ Adds the given Actors to this repository. If a actor is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actor(self, actor_name: str) -> Actor:
        """
        Returns the Actor with the given name in this repository. Note: this is case insensitive.

        Raises:
            ValueError: if there is no Actor in this repository with the given name
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_user(self, user: User) -> None:
        """ Adds the given user to this repository. If the user is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_users(self, user: List[User]) -> None:
        """ Adds the given users to this repository. If a user is already in this repository it won't be added. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username: str) -> User:
        """
        Returns the User with the given name in this repository.

        Raises:
            ValueError: if there is no User in this repository with the given name
        """
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, user: User) -> None:
        """
        Removes the given user from this repository.

        This has the effect of removing any reviews the user may be linked to as well as any other data associated with
        them.
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def update_username(self, user: User, new_username: str) -> None:
        """ Updates the given user's username in this repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review, user: Union[User, None] = None) -> None:
        """
        Adds a review to this repository. If a user is specified it is treated as being the review's creator, otherwise
        the review is considered to be posted anonymously.
        """
        raise NotImplementedError

    def add_reviews(self, reviews: List[Review]) -> None:
        """ Adds the given reviews to this repository. """
        raise NotImplementedError

    def get_review_user(self, review: Review) -> Union[User, None]:
        """ Returns the User who created the given Review or None if the review was anonymous. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_reviews_for_movie(self, movie: Movie) -> int:
        """ Returns the number of Reviews for the given Movie."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_review_pages_for_movie(self,
                                             movie: Movie,
                                             page_size: int = DEFAULT_PAGE_SIZE) -> int:
        """ Returns the number of pages of reviews that can be created from the given filtering options. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_reviews_for_movie(self,
                              movie: Movie,
                              page_number: int,
                              page_size: int = DEFAULT_PAGE_SIZE) -> List[Review]:
        """
        Returns a list containing the nth page of Reviews for the given Movie ordered by the review's timestamp.

        Args:
            movie (Movie): movie to return reviews for.
            page_number (int): page number of the the page to return, starting from zero.
            page_size (int, optional): number of results per page. The last page may have less results than this.

        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self,
                             query: str = "",
                             genres: List[Genre] = [],
                             directors: List[Director] = [],
                             actors: List[Actor] = []) -> int:
        """
        Returns the number of movies in this repository.

        If any filtering options are specified returns the number of movies that meet the specified filters. Check
        'get_movies' for documentation on filtering options.
        """
        raise NotImplementedError

    def get_number_of_movie_pages(self,
                                  page_size: int = DEFAULT_PAGE_SIZE,
                                  query: str = "",
                                  genres: List[Genre] = [],
                                  directors: List[Director] = [],
                                  actors: List[Actor] = []) -> int:
        """
        Returns the number of pages of movies that can be created from the given filtering options.

        Check 'get_movies' for documentation on filtering options.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies(self,
                   page_number: int,
                   page_size: int = DEFAULT_PAGE_SIZE,
                   query: str = "",
                   genres: List[Genre] = [],
                   directors: List[Director] = [],
                   actors: List[Actor] = []) -> List[Movie]:
        """
        Returns a list containing the nth page of Movies in this repository ordered by title and then release date.

        Args:
            page_number (int): page number of the the page to return, starting from zero.
            page_size (int, optional): number of results per page. The last page may have less results than this.
            query (str, optional): string to search for in a movie's fields.
            genres (List[Genre], optional): genres to filter movies by. A movie must have all of the specified genres
                for it to be included in the results.
            directors (List[Director], optional): directors to filter movies by. A movie must be directed by one of the
                specified directors for it to be included in the results.
            actors (List[Actor], optional): actors to filter movies by. A movie must have all of the specified actors
                for it to be included in the results.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies_for_user(self, user: User) -> int:
        """  Returns the number of  unique movies from the given user's watchlist and watched list. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movie_pages_for_user(self,
                                           user: User,
                                           page_size: int = DEFAULT_PAGE_SIZE) -> int:
        """ Returns the number of pages of movies that can be created from the given filtering options. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_for_user(self,
                            user: User,
                            page_number: int,
                            page_size: int = DEFAULT_PAGE_SIZE) -> List[Movie]:
        """
        Returns a list containing the nth page of Movies in this repository ordered by title and then release date.

        Args:
            user (User): user to return movies for.
            page_number (int): page number of the the page to return, starting from zero.
            page_size (int, optional): number of results per page. The last page may have less results than this.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_id(self, movie_id: int) -> Movie:
        """ Returns the movie with the given id in this repository.

         Raises:
             ValueError: if there is no movie with the given id
         """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns a list containing all genres in this repository ordered by each genres name. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self) -> List[Director]:
        """ Returns a list containing all directors in this repository ordered by each directors name. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self) -> List[Actor]:
        """ Returns a list containing all actors in this repository ordered by each actors name. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_per_genre(self) -> Dict[Genre, int]:
        """ Returns the number of movies tagged with each genre in this repository. """
        raise NotImplementedError

    def __repr__(self):
        return f'<{type(self).__name__}>'


def populate(repo: AbstractRepository, data_path: str):
    """ Populates the given repository using data at the given path. """
    reader = MovieFileCSVReader(data_path)
    reader.read_csv_file()

    sim = MovieWatchingSimulation(reader.dataset_of_movies)
    state = sim.simulate(num_users=50, min_num_movies=10, max_num_movies=20)

    repo.add_movies(reader.dataset_of_movies)
    repo.add_genres(reader.dataset_of_genres)
    repo.add_directors(reader.dataset_of_directors)
    repo.add_actors(reader.dataset_of_actors)
    repo.add_users(state.users)
    repo.add_reviews(state.reviews)

    test_user = User('testuser', generate_password_hash('test123A'))
    repo.add_user(test_user)

    test_user2 = User('testuser2', generate_password_hash('test123A'))
    repo.add_user(test_user2)

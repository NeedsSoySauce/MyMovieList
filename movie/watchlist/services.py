from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie
from movie.domain.user import User
from movie.search.services import SearchResults

DEFAULT_PAGE_SIZE = 25


def get_user_movies(repo: AbstractRepository,
                    user: User,
                    page_number: int,
                    page_size: int = DEFAULT_PAGE_SIZE) -> SearchResults:
    """ Returns a page of a user's watchlist and watched movies. Page numbers start from zero. """

    movies = repo.get_movies_for_user(user, page_number, page_size)
    hits = repo.get_number_of_movies_for_user(user)
    pages = repo.get_number_of_movie_pages_for_user(user, page_size)

    return SearchResults(movies, hits, page_number, pages)


def add_movie_to_watchlist(repo: AbstractRepository, user: User, movie: Movie) -> None:
    """ Adds the given movie to the given user's watchlist. """
    user.add_to_watchlist(movie)


def remove_movie_from_watchlist(repo: AbstractRepository, user: User, movie: Movie) -> None:
    """ Removes the given movie from the given user's watchlist. """
    user.remove_from_watchlist(movie)



def add_movie_to_watched(repo: AbstractRepository, user: User, movie: Movie) -> None:
    """ Adds the given movie to the given user's list of watched movies. """
    user.watch_movie(movie)


def remove_movie_from_watched(repo: AbstractRepository, user: User, movie: Movie) -> None:
    """ Removes the given movie from the given user's list of watched movies. """
    user.remove_from_watched_movies(movie)


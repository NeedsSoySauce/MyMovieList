from movie.adapters.repository import AbstractRepository
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

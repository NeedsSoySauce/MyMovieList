from itertools import islice
from math import ceil

from flask import current_app

from movie.adapters.repository import AbstractRepository
from movie.domain.user import User
from movie.search.services import SearchResults

_DEFAULT_PAGE_SIZE = 25


def get_user_movies(user: User,
                    page_number: int,
                    page_size: int = _DEFAULT_PAGE_SIZE) -> SearchResults:
    """ Returns a page of a user's watchlist and watched movies. Page numbers start from zero. """

    watched_movies = user.watched_movies
    hits = user.watchlist_size() + len(watched_movies)
    pages = ceil(hits / page_size)
    page_number = max(0, min(page_number, pages - 1))
    offset = page_number * page_size

    movies = list(set(list(user.watchlist) + watched_movies))[offset:min(offset + page_size, hits)]
    movies.sort()

    return SearchResults(movies, hits, page_number, pages)

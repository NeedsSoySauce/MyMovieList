from itertools import islice
from math import ceil

from flask import current_app

from movie.adapters.repository import AbstractRepository
from movie.domain.user import User
from movie.search.services import SearchResults

_DEFAULT_PAGE_SIZE = 25


def get_watchlist_movies(user: User,
                         page_number: int,
                         page_size: int = _DEFAULT_PAGE_SIZE) -> SearchResults:
    """ Returns a page of a user's watchlist. Page numbers start from zero. """

    hits = user.watchlist_size()
    pages = ceil(hits / page_size)
    page_number = max(0, min(page_number, pages - 1))
    offset = page_number * page_size
    current_app.logger.debug(f"min = {offset}, max={min(offset + page_size, hits)}")
    movies = list(islice(user.watchlist, offset, min(offset + page_size, hits)))

    return SearchResults(movies, hits, page_number, pages)

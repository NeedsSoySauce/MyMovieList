from typing import List, NamedTuple

from movie.adapters.repository import instance as repo
from movie.domain.movie import Movie

_DEFAULT_PAGE_SIZE = 25


# Note - page numbers starts from 0.
class SearchResults(NamedTuple):
    movies: List[Movie]
    hits: int
    page: int
    pages: int


def search_movies(page_number: int, page_size: int = _DEFAULT_PAGE_SIZE, query: str = '',
                  genres: List[str] = []) -> SearchResults:
    """
    Searches for movies using the given filtering options and returns a SearchResults NamedTuple.

    Check the get_movies method in AbstractRepository for info on filtering options.
    """
    try:
        genres = [repo.get_genre(name) for name in genres]
    except ValueError:
        return SearchResults([], 0, page_number, 0)

    movies = repo.get_movies(page_number, page_size, query, genres)
    hits = repo.get_number_of_movies(query, genres)
    pages = repo.get_number_of_pages(page_size, query, genres)

    return SearchResults(movies, hits, page_number, pages)

from math import ceil
from typing import List, Dict, Union, NamedTuple

from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User

_DEFAULT_PAGE_SIZE = 25


# Note - page numbers starts from 0.
class SearchResults(NamedTuple):
    reviews: List[Review]
    hits: int
    page: int
    pages: int


def get_movie_by_id(repo: AbstractRepository, movie_id: int) -> Movie:
    return repo.get_movie_by_id(movie_id)


def get_movie_reviews(repo: AbstractRepository,
                      movie: Movie,
                      page_number: int,
                      page_size: int = _DEFAULT_PAGE_SIZE) -> SearchResults:
    """ Returns a page of the reviews for the specified movie. Page numbers start from zero. """

    reviews = repo.get_movie_reviews(movie)
    hits = len(reviews)
    pages = ceil(hits / page_size)
    page_number = max(0, min(page_number, pages - 1))
    offset = page_number * page_size

    reviews = reviews[offset:min(offset + page_size, hits)]

    return SearchResults(reviews, hits, page_number, pages)


def get_reviews_user_map(repo: AbstractRepository, reviews: List[Review]) -> Dict[Review, User]:
    reviews_user_map: Dict[Review, Union[User, None]] = {}

    for review in reviews:
        reviews_user_map[review] = repo.get_review_user(review)

    return reviews_user_map


def add_review(repo: AbstractRepository, review: Review, user: Union[User, None]):
    repo.add_review(review, user)
    user.add_review(review)

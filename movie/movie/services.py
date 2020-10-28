from math import ceil
from typing import List, Dict, Union, NamedTuple

from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User

DEFAULT_PAGE_SIZE = 25


# Note - page numbers starts from 0.
class SearchResults(NamedTuple):
    reviews: List[Review]
    hits: int
    page: int
    pages: int


def get_movie_by_id(repo: AbstractRepository, movie_id: int) -> Movie:
    """ Returns the Movie with the given id in the given repository. """
    return repo.get_movie_by_id(movie_id)


def get_movie_reviews(repo: AbstractRepository,
                      movie: Movie,
                      page_number: int,
                      page_size: int = DEFAULT_PAGE_SIZE) -> SearchResults:
    """ Returns a page of the reviews for the specified movie. Page numbers start from zero. """

    reviews = repo.get_reviews_for_movie(movie, page_number, page_size)
    hits = repo.get_number_of_reviews_for_movie(movie)
    pages = repo.get_number_of_review_pages_for_movie(movie, page_size)

    return SearchResults(reviews, hits, page_number, pages)


def get_reviews_user_map(repo: AbstractRepository, reviews: List[Review]) -> Dict[Review, User]:
    """
    Returns a dict that maps a Review to the User who posted it or None if the review was posted anonymously.
    """
    reviews_user_map: Dict[Review, Union[User, None]] = {}

    for review in reviews:
        reviews_user_map[review] = repo.get_review_user(review)

    return reviews_user_map


def add_review(repo: AbstractRepository, movie: Movie, review_text: str, rating: int, user: Union[User, None] = None):
    """
    Adds a review to this repository. If a user is specified it is treated as being the review's creator, otherwise the
    review is considered to be posted anonymously.
    """
    review = Review(movie, review_text, rating, user=user)
    repo.add_review(review, user)

    if user:
        user.add_review(review)

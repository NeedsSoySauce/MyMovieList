from typing import List, Dict, Union

from movie.adapters.repository import AbstractRepository
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User


def get_movie_by_id(repo: AbstractRepository, movie_id: int) -> Movie:
    return repo.get_movie_by_id(movie_id)


def get_movie_reviews(repo: AbstractRepository, movie: Movie) -> List[Review]:
    return repo.get_movie_reviews(movie)


def get_reviews_user_map(repo: AbstractRepository, reviews: List[Review]) -> Dict[Review, User]:
    reviews_user_map: Dict[Review, Union[User, None]] = {}

    for review in reviews:
        reviews_user_map[review] = repo.get_review_user(review)

    return reviews_user_map


def add_review(repo: AbstractRepository, review: Review, user: Union[User, None]):
    repo.add_review(review, user)

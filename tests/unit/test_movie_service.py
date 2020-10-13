import pytest

from movie.movie.services import *


def test_get_movie_by_id(populated_memory_repository):
    movies = populated_memory_repository.get_movies(0)
    movie = get_movie_by_id(populated_memory_repository, movies[0].id)

    assert movie == movies[0]


def test_get_movie_reviews(movie, memory_repository):
    review = Review(movie, '', 1)
    memory_repository.add_movie(movie)
    memory_repository.add_review(review)

    result = get_movie_reviews(memory_repository, movie, 0).reviews

    assert result[0] == review


def test_get_reviews_user_map(user, review, memory_repository):
    user.add_review(review)
    memory_repository.add_user(user)

    result = get_reviews_user_map(memory_repository, [review])

    assert result[review] == user


def test_add_review_with_user(user, review, memory_repository):
    add_review(memory_repository, review.movie, review.review_text, review.rating, user)

    result = get_reviews_user_map(memory_repository, [review])

    assert result[review] == user

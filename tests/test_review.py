import pytest
from datetime import datetime

from domainmodel.movie import Movie
from domainmodel.review import Review

# How many seconds review.timestamp should be within of the current POSIX timestamp when it's created
_TIMESTAMP_TOLERANCE = 0.05


def test_constructor(movie):
    review_text = "   Text    with   spaces  \n"

    review_text_expected = "Text    with   spaces"
    rating = 1
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text == review_text_expected
    assert review.rating == rating
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)

    review_text = "   Text    with   spaces  \n"
    review_text_expected = "Text    with   spaces"
    rating = 10
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text == review_text_expected
    assert review.rating == rating
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)


def test_constructor_invalid_movie_type():
    movie = 42
    review_text = "   Text    with   spaces  \n"
    rating = 1

    with pytest.raises(TypeError):
        _ = Review(movie, review_text, rating)


def test_constructor_empty_string_review_text(movie):
    review_text = ""
    rating = 1
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text is None
    assert review.rating == rating
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)


def test_constructor_invalid_review_text_type(movie):
    review_text = 42
    rating = 1
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text is None
    assert review.rating == rating
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)


def test_constructor_invalid_rating_value(movie):
    review_text = "   Text    with   spaces  \n"
    review_text_expected = "Text    with   spaces"
    rating = 0
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text == review_text_expected
    assert review.rating is None
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)

    review_text = "   Text    with   spaces  \n"
    review_text_expected = "Text    with   spaces"
    rating = 11
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text == review_text_expected
    assert review.rating is None
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)


def test_constructor_invalid_rating_type(movie):
    review_text = "   Text    with   spaces  \n"
    review_text_expected = "Text    with   spaces"
    rating = 1.0
    review = Review(movie, review_text, rating)

    assert review.movie == movie
    assert review.review_text == review_text_expected
    assert review.rating is None
    assert review.timestamp.timestamp() == pytest.approx(datetime.utcnow().timestamp(), abs=_TIMESTAMP_TOLERANCE)


def test_repr(review):
    expected = f'<Review <Movie TestMovie, 2020>, Text  with  some  spaces, 1, {review.timestamp.isoformat()}>'
    assert repr(review) == expected


def test_repr_no_review_text(movie):
    review_text = ""
    rating = 1
    review = Review(movie, review_text, rating)

    expected = f'<Review <Movie TestMovie, 2020>, None, 1, {review.timestamp.isoformat()}>'
    assert repr(review) == expected


def test_repr_no_rating(movie):
    review_text = "Test"
    rating = 1.0
    review = Review(movie, review_text, rating)

    expected = f'<Review <Movie TestMovie, 2020>, Test, None, {review.timestamp.isoformat()}>'
    assert repr(review) == expected


def test_equality_when_equal(review, movie):
    assert review == review


def test_equality_when_not_equal(review):
    # Check not equal when reviews are partially equal
    movie = Movie("Test", 2000)
    review_text = review.review_text
    rating = review.rating
    other = Review(movie, review_text, rating)
    assert review != other

    movie = review.movie
    review_text = "Test"
    rating = review.rating
    other = Review(movie, review_text, rating)
    assert review != other

    movie = review.movie
    review_text = review.review_text
    rating = 5
    other = Review(movie, review_text, rating)
    assert review != other

    # Check not equal when reviews are completely different
    movie = Movie("Test", 2000)
    review_text = "Test"
    rating = 5
    other = Review(movie, review_text, rating)
    assert review != other


def test_equality_with_different_type(review):
    assert review != 123

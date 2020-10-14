import pytest
from flask.testing import FlaskClient

from movie.movie import movie


def test_get_movie(client: FlaskClient):
    response = client.get('/movie/7')
    assert response.status_code == 200

    response = client.get('/movie/1234')
    assert response.status_code == 404


def test_get_movie_reviews(client: FlaskClient):
    response = client.get('/movie/7/reviews')
    assert response.status_code == 200

    response = client.get('/movie/1234/reviews')
    assert response.status_code == 404


def test_add_review_anonymous(client: FlaskClient):
    response = client.get('/movie/1/reviews')
    assert response.status_code == 200

    data = {
        'rating': 1,
        'review': 'abc 123'
    }

    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)

    assert b'Anonymous' in response.data
    assert b'1' in response.data
    assert b'abc 123' in response.data


def test_add_review_authenticated(client: FlaskClient, auth):
    data = {
        'rating': 1,
        'review': 'abc 123'
    }

    auth.login()
    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)

    assert b'test' in response.data
    assert b'1' in response.data
    assert b'abc 123' in response.data


@pytest.mark.parametrize(('rating', 'text', 'message'), (
        ('', 'abc', movie.INVALID_CHOICE_MESSAGE),
        (0, 'abc', movie.INVALID_RATING_RANGE_MESSAGE),
        (11, 'abc', movie.INVALID_RATING_RANGE_MESSAGE),
        (2.5, 'abc', movie.INVALID_CHOICE_MESSAGE),
        (1, '', movie.INVALID_REVIEW_TEXT_LENGTH_MESSAGE),
        (1, 'crap', movie.REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE)
))
def test_add_review_invalid_input(client, rating, text, message):
    data = {
        'rating': rating,
        'review': text
    }

    if rating is None:
        del data['rating']

    response = client.post('/movie/1/reviews', data=data, follow_redirects=True)
    assert message.encode() in response.data

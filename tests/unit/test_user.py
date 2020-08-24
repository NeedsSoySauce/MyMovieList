import pytest

from domainmodel.user import User


def test_constructor():
    username = "  Test  User  "
    username_expected = "test  user"
    password = "abc123"
    user = User(username, password)

    assert user.user_name == username_expected
    assert user.password == password


def test_constructor_empty_string_username():
    username = ""
    password = "abc123"
    user = User(username, password)

    assert user.user_name is None
    assert user.password == password


def test_constructor_invalid_username():
    username = 42
    password = "abc123"
    user = User(username, password)

    assert user.user_name is None
    assert user.password == password


def test_constructor_empty_string_password():
    username = "  Test  User  "
    username_expected = "test  user"
    password = ""
    user = User(username, password)

    assert user.user_name == username_expected
    assert user.password == password


def test_constructor_invalid_password():
    username = "  Test  User  "
    password = 42

    with pytest.raises(TypeError):
        _ = User(username, password)


def test_repr(user):
    assert repr(user) == "<User username>"


def test_repr_no_username():
    username = None
    password = "abc123"
    user = User(username, password)

    assert repr(user) == "<User None>"


def test_equality_when_equal(user):
    assert user == user

    username = user.user_name
    password = user.password
    other = User(username, password)

    assert user == other


def test_equality_when_not_equal(user):
    # Check not equal when users are partially equal
    username = "123"
    password = user.password
    other = User(username, password)
    assert user != other

    username = user.user_name
    password = "123"
    other = User(username, password)
    assert user != other

    # Check not equal when users are completely different
    username = "123"
    password = "123"
    other = User(username, password)
    assert user != other


def test_equality_with_different_type(user):
    assert user != 123


def test_less_than_when_true():
    # Check password doesn't affect the ordering
    a = User("a", 'a')
    b = User("b", 'a')
    assert a < b

    a = User("a", 'a')
    b = User("b", 'b')
    assert a < b

    a = User("a", 'b')
    b = User("b", 'a')
    assert a < b


def test_less_than_when_false():
    a = User("a", 'a')
    b = User("a", 'a')
    assert not (a < b)

    a = User("a", 'a')
    b = User("a", 'b')
    assert not (a < b)

    a = User("a", 'b')
    b = User("a", 'a')
    assert not (a < b)

    a = User("b", 'a')
    b = User("a", 'a')
    assert not (a < b)

    a = User("b", 'a')
    b = User("a", 'b')
    assert not (a < b)

    a = User("b", 'b')
    b = User("a", 'a')
    assert not (a < b)


def test_less_than_with_different_type(user):
    with pytest.raises(TypeError):
        _ = user < 123


def test_hash(user):
    # Check hash doesn't change for the same instance
    assert hash(user) == hash(user)

    # Check hash is the same with another instance with the same properties
    username = user.user_name
    password = user.password
    other = User(username, password)
    assert hash(user) == hash(other)

    # Check password doesn't affect hash
    username = user.user_name
    password = "123"
    other = User(username, password)
    assert hash(user) == hash(other)


def test_hash_changes(user):
    username = "123"
    password = user.password
    other = User(username, password)
    assert hash(user) != hash(other)


def test_watch_movie_without_runtime_minutes(user, movie):
    user.watch_movie(movie)

    assert isinstance(user.watched_movies, list)
    assert len(user.watched_movies) == 1
    assert movie in user.watched_movies
    assert user.time_spent_watching_movies_minutes == 0


def test_watch_movie_with_runtime_minutes(user, movie):
    movie.runtime_minutes = 123
    user.watch_movie(movie)

    assert isinstance(user.watched_movies, list)
    assert len(user.watched_movies) == 1
    assert movie in user.watched_movies
    assert user.time_spent_watching_movies_minutes == movie.runtime_minutes


def test_watch_duplicate_movie(user, movie):
    movie.runtime_minutes = 123
    user.watch_movie(movie)
    user.watch_movie(movie)

    assert isinstance(user.watched_movies, list)
    assert len(user.watched_movies) == 1
    assert movie in user.watched_movies
    assert user.time_spent_watching_movies_minutes == movie.runtime_minutes


def test_watch_multiple_movies(user, movies):
    total_minutes = 0
    for i, movie in enumerate(movies):
        movie.runtime_minutes = i + 1
        total_minutes += i + 1

        user.watch_movie(movie)

    assert isinstance(user.watched_movies, list)
    assert len(user.watched_movies) == len(movies)
    assert all(movie in user.watched_movies for movie in movies)
    assert user.time_spent_watching_movies_minutes == total_minutes


def test_watch_movie_invalid_type(user):
    with pytest.raises(TypeError):
        user.watch_movie(123)


def test_add_review(user, review):
    user.add_review(review)

    assert isinstance(user.reviews, list)
    assert len(user.reviews) == 1
    assert review in user.reviews


def test_add_duplicate_review(user, review):
    review.runtime_minutes = 123
    user.add_review(review)
    user.add_review(review)

    assert isinstance(user.reviews, list)
    assert len(user.reviews) == 1
    assert review in user.reviews


def test_add_multiple_reviews(user, reviews):
    for review in reviews:
        user.add_review(review)

    assert isinstance(user.reviews, list)
    assert len(user.reviews) == len(reviews)
    assert all(review in user.reviews for review in reviews)


def test_add_review_invalid_type(user):
    with pytest.raises(TypeError):
        user.add_review(123)


def test_add_to_watchlist(user, movie):
    user.add_to_watchlist(movie)
    assert user.watchlist_size() == 1


def test_add_to_watchlist_duplicate(user, movie):
    user.add_to_watchlist(movie)
    user.add_to_watchlist(movie)
    assert user.watchlist_size() == 1


def test_add_to_watchlist_invalid_type(user):
    with pytest.raises(TypeError):
        user.add_to_watchlist(123)


def test_remove_from_empty_watchlist(user, movie):
    user.remove_from_watchlist(movie)
    assert user.watchlist_size() == 0


def test_remove_from_non_empty_watchlist(user, movie):
    user.add_to_watchlist(movie)
    user.remove_from_watchlist(movie)
    assert user.watchlist_size() == 0


def test_remove_from_watchlist_duplicate(user, movie):
    user.add_to_watchlist(movie)
    user.remove_from_watchlist(movie)
    user.remove_from_watchlist(movie)
    assert user.watchlist_size() == 0


def test_remove_from_watchlist_invalid_type(user):
    with pytest.raises(TypeError):
        user.remove_from_watchlist(123)


def test_watch_movie_updates_watchlist(user, movie):
    user.add_to_watchlist(movie)
    user.watch_movie(movie)

    assert user.watchlist_size() == 0

import pytest

from activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from domainmodel.movie import Movie


def test_constructor(populated_movies):
    # Tests fails if an exception is raised
    _ = MovieWatchingSimulation(populated_movies)


def test_constructor_invalid_movies_type():
    with pytest.raises(TypeError):
        _ = MovieWatchingSimulation(123)

    with pytest.raises(TypeError):
        _ = MovieWatchingSimulation([Movie("Test", 2020), 123])


def test_simulation(movie_watching_simulation):
    num_users = 10
    min_num_movies = 0
    max_num_movies = None
    state = movie_watching_simulation.simulate(num_users, min_num_movies, max_num_movies)

    assert len(state.users) == num_users


def test_simulation_invalid_params(movie_watching_simulation):
    with pytest.raises(TypeError):
        _ = movie_watching_simulation.simulate(num_users=1.2)

    with pytest.raises(ValueError):
        _ = movie_watching_simulation.simulate(num_users=0)

    with pytest.raises(ValueError):
        _ = movie_watching_simulation.simulate(num_users=-1)

    with pytest.raises(TypeError):
        _ = movie_watching_simulation.simulate(min_num_movies=1.2)

    with pytest.raises(ValueError):
        _ = movie_watching_simulation.simulate(min_num_movies=-1)

    with pytest.raises(TypeError):
        _ = movie_watching_simulation.simulate(max_num_movies=1.2)

    with pytest.raises(ValueError):
        _ = movie_watching_simulation.simulate(max_num_movies=-1)

    with pytest.raises(ValueError):
        _ = movie_watching_simulation.simulate(min_num_movies=1, max_num_movies=0)


def test_simulation_users_are_valid(movie_watching_simulation: MovieWatchingSimulation, populated_movies):
    state = movie_watching_simulation.simulate()

    for user in state.users:
        assert user.user_name is not None
        assert user.password is not None

        # Check that the movies this user has are in our movies
        assert all(movie in populated_movies for movie in user.watchlist)
        assert all(movie in populated_movies for movie in user.watched_movies)

        # Check that the reviews this user has are in our reviews
        assert all(review in state.reviews for review in user.reviews)

        # Check that a user hasn't written more than one review for the same movie
        movies = [review.movie for review in user.reviews]
        assert len(movies) == len(set(movies))


def test_simulation_reviews_are_valid(movie_watching_simulation: MovieWatchingSimulation, populated_movies):
    state = movie_watching_simulation.simulate()

    for review in state.reviews:
        # Check this review is linked to only one of our users
        assert sum(review in user.reviews for user in state.users) == 1

        # Check this review is linked to one of ours movies
        assert review.movie in populated_movies

        # Check this review's timestamp isn't earlier than the movie's release year
        assert review.timestamp.year >= review.movie.release_date

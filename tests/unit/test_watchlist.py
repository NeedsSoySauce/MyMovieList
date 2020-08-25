import pytest

from domainmodel.movie import Movie
from domainmodel.watchlist import WatchList


def test_add_movie(watchlist, movie):
    watchlist.add_movie(movie)

    assert watchlist.size() == 1


def test_add_duplicate_movie(watchlist, movie):
    watchlist.add_movie(movie)
    watchlist.add_movie(movie)

    assert watchlist.size() == 1


def test_add_multiple_movies(watchlist, movies):
    for movie in movies:
        watchlist.add_movie(movie)
    assert watchlist.size() == len(movies)


def test_add_movie_invalid_type(watchlist):
    with pytest.raises(TypeError):
        watchlist.add_movie(123)


def test_remove_movie(watchlist, movie):
    watchlist.add_movie(movie)
    watchlist.remove_movie(movie)
    assert watchlist.size() == 0


def test_remove_movie_not_in_watchlist(watchlist, movie):
    watchlist.remove_movie(movie)
    assert watchlist.size() == 0


def test_remove_movie_invalid_type(watchlist):
    with pytest.raises(TypeError):
        watchlist.remove_movie(123)


def test_select_movie(watchlist, movies):
    n_movies = len(movies)

    for movie in movies:
        watchlist.add_movie(movie)

    assert watchlist.select_movie_to_watch(0) == movies[0]
    assert watchlist.select_movie_to_watch(n_movies - 1) == movies[n_movies - 1]
    assert watchlist.select_movie_to_watch(-1) == movies[-1]
    assert watchlist.select_movie_to_watch(-n_movies) == movies[-n_movies]


def test_select_movie_invalid_index_value(watchlist, movies):
    n_movies = len(movies)

    for movie in movies:
        watchlist.add_movie(movie)

    # with pytest.raises(IndexError):
    #     watchlist.select_movie_to_watch(n_movies)
    #
    # with pytest.raises(IndexError):
    #     watchlist.select_movie_to_watch(-n_movies - 1)

    assert watchlist.select_movie_to_watch(n_movies) is None
    assert watchlist.select_movie_to_watch(-n_movies - 1) is None


def test_select_movie_invalid_index_type_watchlist(watchlist):
    with pytest.raises(TypeError):
        watchlist.select_movie_to_watch(1.1)


def test_size(watchlist):
    assert watchlist.size() == 0


def test_first_movie_in_watchlist(watchlist, movies):
    for movie in movies:
        watchlist.add_movie(movie)

    assert watchlist.first_movie_in_watch_list() == movies[0]


def test_first_movie_in_watchlist_when_empty(watchlist):
    assert watchlist.first_movie_in_watch_list() is None


def test_iterator(watchlist, movies):
    for movie in movies:
        watchlist.add_movie(movie)

    for i, movie in enumerate(movies):
        assert movie == movies[i]


def test_contains(watchlist, movie, movies):
    for movie in movies:
        watchlist.add_movie(movie)

    for i, movie in enumerate(movies):
        assert movie in watchlist

    assert not (Movie("test", 2020) in watchlist)
    assert not (123 in watchlist)

import pytest

from movie.adapters.memory_repository import MemoryRepository
from movie.search.services import *


def test_search_empty(memory_repository):
    results = search_movies(memory_repository, 0)
    assert len(results.movies) == 0
    assert results.hits == 0
    assert results.page == 0
    assert results.pages == 0


def test_search(populated_memory_repository):
    results = search_movies(populated_memory_repository, 0)
    assert len(results.movies) == 10
    assert results.hits == 10
    assert results.page == 0
    assert results.pages == 1


def test_search_with_filters(populated_memory_repository: MemoryRepository):
    genres = ['Action', 'Adventure']
    directors = ['James Gunn', 'David Ayer']
    actors = ['Vin Diesel']

    results = search_movies(populated_memory_repository, 0, genres=genres, directors=directors)
    assert len(results.movies) == 2
    assert results.hits == 2
    assert results.page == 0
    assert results.pages == 1

    results = search_movies(populated_memory_repository, 0, genres=genres, directors=directors, actors=actors)
    assert len(results.movies) == 1
    assert results.hits == 1
    assert results.page == 0
    assert results.pages == 1

import pytest

from movie.adapters.memory_repository import MemoryRepository


def test_constructor():
    # Fails if any exceptions are thrown
    _ = MemoryRepository()


def test_add_movie(movie, memory_repository: MemoryRepository):
    memory_repository.add_movie(movie)

    assert movie in memory_repository._movies


def test_add_movie_duplicate(movie, memory_repository: MemoryRepository):
    memory_repository.add_movie(movie)
    memory_repository.add_movie(movie)

    assert len(memory_repository._movies) == 1
    assert movie in memory_repository._movies


def test_add_movie_invalid_type(memory_repository: MemoryRepository):
    with pytest.raises(TypeError):
        memory_repository.add_movie(123)


def test_add_movies(movies, memory_repository: MemoryRepository):
    memory_repository.add_movies(movies)

    assert len(memory_repository._movies) == len(movies)
    assert all(movie in memory_repository._movies for movie in movies)


def test_add_movies_duplicates(movies, memory_repository: MemoryRepository):
    memory_repository.add_movies(movies)
    memory_repository.add_movies(movies)

    assert len(memory_repository._movies) == len(movies)
    assert all(movie in memory_repository._movies for movie in movies)


def test_add_movies_invalid_type(movie, memory_repository: MemoryRepository):
    with pytest.raises(TypeError):
        memory_repository.add_movies(123)

    with pytest.raises(TypeError):
        memory_repository.add_movies([movie, 123])


def test_get_number_of_movies(movies, memory_repository):
    memory_repository.add_movies(movies)

    n = memory_repository.get_number_of_movies()
    assert n == len(movies)


def test_get_number_of_movies_empty(memory_repository):
    n = memory_repository.get_number_of_movies()
    assert n == 0


def test_get_movies_page(populated_memory_repository):
    movies = populated_memory_repository.get_movies_page(0, page_size=2)

    assert len(movies) == 2


def test_get_movies_page_last_page(populated_memory_repository):
    movies = populated_memory_repository.get_movies_page(3, page_size=3)

    assert len(movies) == 1


def test_get_movies_invalid_page_number(populated_memory_repository):
    with pytest.raises(ValueError):
        populated_memory_repository.get_movies_page(-1)

    with pytest.raises(ValueError):
        populated_memory_repository.get_movies_page(1)

    with pytest.raises(TypeError):
        populated_memory_repository.get_movies_page(0.5)


def test_get_movies_invalid_page_size(populated_memory_repository):
    with pytest.raises(ValueError):
        populated_memory_repository.get_movies_page(0, page_size=0)

    with pytest.raises(ValueError):
        populated_memory_repository.get_movies_page(0, page_size=-1)

    with pytest.raises(TypeError):
        populated_memory_repository.get_movies_page(0, page_size=0.5)

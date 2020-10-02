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
    movies = populated_memory_repository.get_movies(0, page_size=2)

    assert len(movies) == 2


def test_get_movies_page_last_page(populated_memory_repository):
    movies = populated_memory_repository.get_movies(3, page_size=3)

    assert len(movies) == 1


def test_get_movies_invalid_page_number(populated_memory_repository):
    with pytest.raises(ValueError):
        populated_memory_repository.get_movies(-1)

    with pytest.raises(ValueError):
        populated_memory_repository.get_movies(1)

    with pytest.raises(TypeError):
        populated_memory_repository.get_movies(0.5)


def test_get_movies_invalid_page_size(populated_memory_repository):
    with pytest.raises(ValueError):
        populated_memory_repository.get_movies(0, page_size=0)

    with pytest.raises(ValueError):
        populated_memory_repository.get_movies(0, page_size=-1)

    with pytest.raises(TypeError):
        populated_memory_repository.get_movies(0, page_size=0.5)


def test_get_movies_genres_filter(genres, populated_memory_repository):
    for i in range(len(genres)):
        # The movies in our test configuration should each have one genre
        repo_movies = populated_memory_repository.get_movies(0, genres=[genres[i]])
        assert len(repo_movies) == 1
        assert genres[i] in repo_movies[0].genres


def test_get_movies_invalid_genres(genre, populated_memory_repository):
    with pytest.raises(TypeError):
        populated_memory_repository.get_movies(0, genres=123)

    with pytest.raises(TypeError):
        populated_memory_repository.get_movies(0, genres=[genre, 123])


def test_add_genre(genre, memory_repository: MemoryRepository):
    memory_repository.add_genre(genre)

    assert genre in memory_repository._genres


def test_add_genre_duplicate(genre, memory_repository: MemoryRepository):
    memory_repository.add_genre(genre)
    memory_repository.add_genre(genre)

    assert len(memory_repository._genres) == 1
    assert genre in memory_repository._genres


def test_add_genre_invalid_type(memory_repository: MemoryRepository):
    with pytest.raises(TypeError):
        memory_repository.add_genre(123)


def test_add_genres(genres, memory_repository: MemoryRepository):
    memory_repository.add_genres(genres)

    assert len(memory_repository._genres) == len(genres)
    assert all(genre in memory_repository._genres for genre in genres)


def test_add_genres_duplicates(genres, memory_repository: MemoryRepository):
    memory_repository.add_genres(genres)
    memory_repository.add_genres(genres)

    assert len(memory_repository._genres) == len(genres)
    assert all(genre in memory_repository._genres for genre in genres)


def test_add_genres_invalid_type(genre, memory_repository: MemoryRepository):
    with pytest.raises(TypeError):
        memory_repository.add_genres(123)

    with pytest.raises(TypeError):
        memory_repository.add_genres([genre, 123])


def test_get_genres(genres, memory_repository: MemoryRepository):
    repo_genres = memory_repository.get_genres()

    assert all(genre in repo_genres for genre in repo_genres)
    assert sorted(repo_genres) == repo_genres






















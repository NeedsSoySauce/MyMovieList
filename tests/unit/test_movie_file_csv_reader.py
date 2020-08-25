import pytest

from datafilereaders.movie_file_csv_reader import MovieFileCSVReader


def test_constructor_invalid_file_extension():
    with pytest.raises(ValueError):
        _ = MovieFileCSVReader('./tests/data/dummy.txt')


def test_read_csv_file(reader):
    reader.read_csv_file()

    assert len(reader.dataset_of_movies) == 1000
    assert len(reader.dataset_of_actors) == 1985
    assert len(reader.dataset_of_directors) == 644
    assert len(reader.dataset_of_genres) == 20


def test_file_not_found():
    reader = MovieFileCSVReader('filethatdoesnotexist.csv')
    with pytest.raises(FileNotFoundError):
        reader.read_csv_file()


def test_invalid_csv_file():
    reader = MovieFileCSVReader('./tests/data/invalid.csv')
    with pytest.raises(ValueError):
        reader.read_csv_file()


def test_invalid_movies_csv_file():
    reader = MovieFileCSVReader('./tests/data/invalid_movies.csv')
    reader.read_csv_file()
    assert len(reader.dataset_of_movies) == 1


def test_dataset_of_movies_is_valid(reader: MovieFileCSVReader):
    reader.read_csv_file()
    movies = reader.dataset_of_movies
    actors = reader.dataset_of_actors
    directors = reader.dataset_of_directors
    genres = reader.dataset_of_genres

    actor_ids = set()
    director_ids = set()
    genre_ids = set()

    for movie in movies:
        assert movie.title is not None

        # Check all of this movie's actors are in our dataset of actors
        assert all(actor in actors for actor in movie.actors)
        for actor in movie.actors:
            actor_ids.add(id(actor))

        # Check this movie's director is in our dataset of directors
        assert movie.director in directors
        director_ids.add(id(movie.director))

        # Check all of this movie's genres are in our dataset of genres
        assert all(genre in genres for genre in movie.genres)
        for genre in movie.genres:
            genre_ids.add(id(genre))

    # Here we are checking that two movies with the same actor/director/genre both reference the same instance.
    # Note that it is not enough to use the 'in' operator here, as that will look for an actor that is equal, but not
    # necessarily the same instance
    assert len(actor_ids) == len(actors)
    assert len(director_ids) == len(directors)
    assert len(genre_ids) == len(genres)


def test_dataset_of_actors_is_valid(reader: MovieFileCSVReader):
    reader.read_csv_file()
    actors = reader.dataset_of_actors

    actor_ids = set()

    for actor in actors:
        assert actor.actor_full_name is not None

        # Check all of this actor's colleagues are in our dataset of actors
        assert all(colleague in actors for colleague in actor.colleagues)

        # Check colleagues are valid
        actor_ids.add(id(actor))
        for colleague in actor.colleagues:
            actor_ids.add(id(colleague))

    # Check that two actors with the same colleague both reference the same instance
    assert len(actor_ids) == len(actors)


def test_dataset_of_directors_is_valid(reader: MovieFileCSVReader):
    reader.read_csv_file()
    directors = reader.dataset_of_directors

    assert all(director.director_full_name is not None for director in directors)

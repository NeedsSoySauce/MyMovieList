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

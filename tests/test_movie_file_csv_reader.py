import pytest


def test_read_csv_file(reader):
    reader.read_csv_file()

    assert len(reader.dataset_of_movies) == 1000
    assert len(reader.dataset_of_actors) == 1985
    assert len(reader.dataset_of_directors) == 644
    assert len(reader.dataset_of_genres) == 20

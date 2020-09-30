import pytest

from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie


def test_constructor():
    movie = Movie("   Movie   name  with    spaces  \n", 1900)
    assert movie.title == "Movie   name  with    spaces"


def test_constructor_empty_string_title():
    movie = Movie("", 2000)
    assert movie.title is None


def test_constructor_invalid_title():
    movie = Movie(123, 2000)
    assert movie.title is None


def test_constructor_invalid_release_date_value():
    with pytest.raises(ValueError):
        _ = Movie("Test", 1899)


def test_constructor_invalid_release_date_type():
    with pytest.raises(TypeError):
        _ = Movie("Test", 2000.9)


def test_title(movie):
    movie.title = "   Movie   name  with    spaces  \n"
    assert movie.title == "Movie   name  with    spaces"


def test_title_empty_string(movie):
    movie.title = ""
    assert movie.title is None


def test_title_invalid_type(movie):
    movie.title = 123
    assert movie.title is None


def test_description(movie):
    movie.description = "   Text   with  some   spaces  \n"
    assert movie.description == "Text   with  some   spaces"


def test_description_empty_string(movie):
    movie.description = ""
    assert movie.description is None


def test_description_invalid_type(movie):
    movie.description = 123
    assert movie.description is None


def test_director(movie, director):
    movie.director = director
    assert hash(movie.director) == hash(director)


def test_director_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.director = 123


def test_actors(movie, actors):
    movie.actors = actors
    assert isinstance(movie.actors, list)
    assert len(movie.actors) == len(actors)
    assert all(a == b for a, b in zip(movie.actors, actors))


def test_actors_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.actors = Actor("123")

    with pytest.raises(TypeError):
        movie.actors = [Actor("123"), 123]


def test_genres(movie, genres):
    movie.genres = genres
    assert isinstance(movie.genres, list)
    assert len(movie.genres) == len(genres)
    assert all(a == b for a, b in zip(movie.genres, genres))


def test_genres_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.genres = Genre("123")

    with pytest.raises(TypeError):
        movie.genres = [Genre("123"), 123]


def test_runtime_minutes(movie):
    movie.runtime_minutes = 1
    assert movie.runtime_minutes == 1


def test_runtime_minutes_invalid_value(movie):
    with pytest.raises(ValueError):
        movie.runtime_minutes = 0

    with pytest.raises(ValueError):
        movie.runtime_minutes = -1


def test_runtime_minutes_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.runtime_minutes = 1.2


def test_rating(movie):
    movie.rating = 0.0
    assert movie.rating == pytest.approx(0.0)

    movie.rating = 10.0
    assert movie.rating == pytest.approx(10.0)


def test_rating_invalid_value(movie):
    with pytest.raises(ValueError):
        movie.rating = -1.0

    with pytest.raises(ValueError):
        movie.rating = 11.0


def test_rating_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.rating = "12"


def test_votes(movie):
    movie.votes = 0
    assert movie.votes == 0

    movie.votes = 1
    assert movie.votes == 1


def test_votes_invalid_value(movie):
    with pytest.raises(ValueError):
        movie.votes = -1


def test_votes_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.votes = 12.5


def test_revenue_millions(movie):
    movie.revenue_millions = 0.0
    assert movie.revenue_millions == pytest.approx(0.0)

    movie.revenue_millions = 0.01
    assert movie.revenue_millions == pytest.approx(0.01)


def test_revenue_millions_invalid_value(movie):
    with pytest.raises(ValueError):
        movie.revenue_millions = -1.0


def test_revenue_millions_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.revenue_millions = "400"


def test_metascore(movie):
    movie.metascore = 0
    assert movie.metascore == 0

    movie.metascore = 100
    assert movie.metascore == 100


def test_metascore_invalid_value(movie):
    with pytest.raises(ValueError):
        movie.metascore = -1

    with pytest.raises(ValueError):
        movie.metascore = 101


def test_metascore_invalid_type(movie):
    with pytest.raises(TypeError):
        movie.metascore = 50.5


def test_repr(movie):
    assert repr(movie) == "<Movie TestMovie, 2020>"


def test_repr_with_no_name():
    movie = Movie("", 2020)
    assert repr(movie) == "<Movie None, 2020>"


def test_equality_when_equal(movie):
    other = Movie("TestMovie", 2020)
    assert movie == other


def test_equality_when_not_equal(movie):
    # Check not equal when partially equal
    other = Movie("TestMovie", 2000)
    assert movie != other

    other = Movie("123", 2020)
    assert movie != other

    # Check not equal when title and release date both differ
    other = Movie("123", 2000)
    assert movie != other


def test_equality_with_different_type(movie):
    assert movie != 123


def test_less_than_when_true():
    a = Movie("123", 2020)
    b = Movie("1234", 2020)
    assert a < b

    a = Movie("123", 2020)
    b = Movie("123", 2021)
    assert a < b

    a = Movie("123", 2020)
    b = Movie("1234", 2021)
    assert a < b


def test_less_than_when_false():
    a = Movie("1234", 2020)
    b = Movie("123", 2020)
    assert not (a < b)

    a = Movie("123", 2021)
    b = Movie("123", 2020)
    assert not (a < b)

    a = Movie("123", 2020)
    b = Movie("123", 2020)
    assert not (a < b)
    assert not (b < a)


def test_less_than_with_different_type(movie):
    with pytest.raises(TypeError):
        _ = movie < 123


def test_hash(movie):
    assert hash(movie) == hash(movie)


def test_hash_changes():
    a = Movie("1234", 2020)
    b = Movie("123", 2020)
    assert hash(a) != hash(b)

    a = Movie("123", 2021)
    b = Movie("123", 2020)
    assert hash(a) != hash(b)

    a = Movie("1234", 2021)
    b = Movie("123", 2020)
    assert hash(a) != hash(b)


def test_add_actor(movie, actor):
    movie.add_actor(actor)
    assert len(movie.actors) == 1
    assert movie.actors[0] == actor


def test_add_duplicate_actor(movie, actor):
    movie.add_actor(actor)
    movie.add_actor(actor)
    assert len(movie.actors) == 1
    assert movie.actors[0] == actor


def test_add_multiple_actors(movie, actors):
    for elem in actors:
        movie.add_actor(elem)
    assert len(movie.actors) == len(actors)
    assert all(elem in actors for elem in movie.actors)


def test_add_invalid_actor(movie):
    with pytest.raises(TypeError):
        movie.add_actor(123)


def test_remove_actor(movie, actor):
    movie.add_actor(actor)
    movie.remove_actor(actor)
    assert len(movie.actors) == 0


def test_remove_actor_when_no_actors(movie, actor):
    movie.actors = []
    movie.remove_actor(actor)
    assert len(movie.actors) == 0


def test_remove_actor_not_in_movie(movie, actor, actors):
    for elem in actors:
        movie.add_actor(elem)

    movie.remove_actor(actor)

    assert len(movie.actors) == len(actors)
    assert all(elem in actors for elem in movie.actors)


def test_correct_actor_is_removed(movie, actors):
    for elem in actors:
        movie.add_actor(elem)

    movie.remove_actor(actors[0])

    assert len(movie.actors) == len(actors) - 1
    assert all(elem != actors[0] for elem in movie.actors)


def test_add_genre(movie, genre):
    movie.add_genre(genre)
    assert len(movie.genres) == 1
    assert movie.genres[0] == genre


def test_add_duplicate_genre(movie, genre):
    movie.add_genre(genre)
    movie.add_genre(genre)
    assert len(movie.genres) == 1
    assert movie.genres[0] == genre


def test_add_multiple_genres(movie, genres):
    for elem in genres:
        movie.add_genre(elem)
    assert len(movie.genres) == len(genres)
    assert all(elem in genres for elem in movie.genres)


def test_add_invalid_genre(movie):
    with pytest.raises(TypeError):
        movie.add_genre(123)


def test_remove_genre(movie, genre):
    movie.add_genre(genre)
    movie.remove_genre(genre)
    assert len(movie.genres) == 0


def test_remove_genre_when_no_genres(movie, genre):
    movie.genres = []
    movie.remove_genre(genre)
    assert len(movie.genres) == 0


def test_remove_genre_not_in_movie(movie, genre, genres):
    for elem in genres:
        movie.add_genre(elem)

    movie.remove_genre(genre)

    assert len(movie.genres) == len(genres)
    assert all(elem in genres for elem in movie.genres)


def test_correct_genre_is_removed(movie, genres):
    for elem in genres:
        movie.add_genre(elem)

    movie.remove_genre(genres[0])

    assert len(movie.genres) == len(genres) - 1
    assert all(elem != genres[0] for elem in movie.genres)

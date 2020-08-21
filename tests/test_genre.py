import pytest
from domainmodel.genre import Genre


@pytest.fixture
def genre():
    return Genre("Action")


def test_constructor():
    genre = Genre("123")
    assert genre.genre_name == "123"


def test_constructor_with_empty_string_genre_name():
    genre = Genre("")
    assert genre.genre_name is None


def test_constructor_with_non_string_genre_name():
    genre = Genre(42)
    assert genre.genre_name is None


def test_constructor_strips_whitespace():
    genre = Genre("        Action      ")
    assert genre.genre_name == "Action"


def test_repr(genre):
    assert repr(genre) == "<Genre Action>"


def test_repr_with_no_name():
    genre = Genre("")
    assert repr(genre) == "<Genre None>"


def test_equality_when_equal(genre):
    other = Genre("Action")
    assert genre == other


def test_equality_when_not_equal(genre):
    other = Genre("GenreName2")
    assert genre != other


def test_equality_with_different_type(genre):
    assert genre != 123


def test_less_than_when_true(genre):
    a = Genre("a")
    b = Genre("b")
    assert a < b


def test_less_than_when_false(genre):
    a = Genre("a")
    b = Genre("b")
    assert not (b < a)


def test_less_than_with_different_type(genre):
    with pytest.raises(TypeError):
        _ = genre < 123


def test_hash(genre):
    assert hash(genre) == hash(genre)


def test_hash_changes(genre):
    other = Genre("123")
    assert hash(genre) != hash(other)

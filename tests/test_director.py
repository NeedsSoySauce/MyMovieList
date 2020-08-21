import pytest
from domainmodel.director import Director


def test_constructor():
    director = Director("123")
    assert director.director_full_name == "123"


def test_constructor_with_empty_string_full_name():
    director = Director("")
    assert director.director_full_name is None


def test_constructor_with_non_string_full_name():
    director = Director(42)
    assert director.director_full_name is None


def test_constructor_strips_whitespace():
    director = Director("        Firstname Lastname      ")
    assert director.director_full_name == "Firstname Lastname"


def test_repr(director):
    assert repr(director) == "<Director Firstname Lastname>"


def test_repr_with_no_name():
    director = Director("")
    assert repr(director) == "<Director None>"


def test_equality_when_equal(director):
    other = Director("Firstname Lastname")
    assert director == other


def test_equality_when_not_equal(director):
    other = Director("Firstname2 Lastname2")
    assert director != other


def test_equality_with_different_type(director):
    assert director != 123


def test_less_than_when_true(director):
    a = Director("a")
    b = Director("b")
    assert a < b


def test_less_than_when_false(director):
    a = Director("a")
    b = Director("b")
    assert not (b < a)


def test_less_than_with_different_type(director):
    with pytest.raises(TypeError):
        _ = director < 123


def test_hash(director):
    assert hash(director) == hash(director)


def test_hash_changes(director):
    other = Director("123")
    assert hash(director) != hash(other)

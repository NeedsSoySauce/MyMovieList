import pytest
from domainmodel.person import Person


@pytest.fixture
def person():
    return Person("Firstname Lastname")


def test_constructor():
    person = Person("123")
    assert person.full_name == "123"


def test_constructor_with_empty_string_full_name():
    person = Person("")
    assert person.full_name is None


def test_constructor_with_non_string_full_name():
    person = Person(42)
    assert person.full_name is None


def test_constructor_strips_whitespace():
    person = Person("        Firstname Lastname      ")
    assert person.full_name == "Firstname Lastname"


def test_repr(person):
    assert repr(person) == "<Person Firstname Lastname>"


def test_repr_with_no_name():
    person = Person("")
    assert repr(person) == "<Person None>"


def test_equality_when_equal(person):
    other = Person("Firstname Lastname")
    assert person == other


def test_equality_when_not_equal(person):
    other = Person("Firstname2 Lastname2")
    assert person != other


def test_equality_with_different_type(person):
    assert person != 123


def test_less_than_when_true(person):
    a = Person("a")
    b = Person("b")
    assert a < b


def test_less_than_when_false(person):
    a = Person("a")
    b = Person("b")
    assert not (b < a)


def test_less_than_with_different_type(person):
    with pytest.raises(TypeError):
        _ = person < 123


def test_hash(person):
    assert hash(person) == hash(person)


def test_hash_changes(person):
    other = Person("123")
    assert hash(person) != hash(other)

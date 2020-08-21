import pytest

from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie
from domainmodel.person import Person


@pytest.fixture
def person():
    return Person("Firstname Lastname")


@pytest.fixture
def director():
    return Director("Firstname Lastname")


@pytest.fixture
def genre():
    return Genre("Action")


@pytest.fixture
def actor():
    return Actor("Firstname Lastname")


@pytest.fixture
def movie():
    return Movie("TestMovie", 2020)


@pytest.fixture
def genres():
    return [Genre(f'Genre{i}') for i in range(10)]


@pytest.fixture
def actors():
    return [Actor(f'Actor{i}') for i in range(10)]

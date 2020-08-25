import pytest

from activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from domainmodel.actor import Actor
from domainmodel.director import Director
from domainmodel.genre import Genre
from domainmodel.movie import Movie
from domainmodel.person import Person
from domainmodel.review import Review
from domainmodel.user import User
from domainmodel.watchlist import WatchList


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
def directors():
    return [Director(f'Director{i}') for i in range(10)]


@pytest.fixture
def genres():
    return [Genre(f'Genre{i}') for i in range(10)]


@pytest.fixture
def actors():
    return [Actor(f'Actor{i}') for i in range(10)]


@pytest.fixture
def movies():
    return [Movie(f'Movie{i}', 2020) for i in range(10)]


@pytest.fixture
def reader():
    return MovieFileCSVReader('./datafiles/Data1000Movies.csv')


@pytest.fixture
def review(movie):
    return Review(movie, "Text  with  some  spaces", 1)


@pytest.fixture
def reviews(movies):
    return [Review(movie, f'Review{i}', 1) for i, movie in enumerate(movies)]


@pytest.fixture
def user():
    return User("username", "correcthorsebatterystaple")


@pytest.fixture
def watchlist():
    return WatchList()


@pytest.fixture
def populated_movies(genres, directors, actors):
    movies = []

    for i in range(10):
        movie = Movie(f'Movie{i}', 2000 + i)
        movie.genres = [genres[i]]
        movie.description = f'Description{i}'
        movie.director = directors[i]
        movie.actors = [actors[i]]
        movie.runtime_minutes = i + 1
        movie.rating = float(i)
        movie.votes = i

        if i % 2 == 0:
            movie.revenue_millions = float(i + 1)

        if i % 4 == 0:
            movie.metascore = i * 10

        movies.append(movie)

    return movies


@pytest.fixture
def movie_watching_simulation(populated_movies):
    return MovieWatchingSimulation(populated_movies)

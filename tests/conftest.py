import pytest

from movie.activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from movie.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.person import Person
from movie.domain.review import Review
from movie.domain.user import User
from movie.domain.watchlist import WatchList


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
    return MovieFileCSVReader('./movie/adapters/data/Data1000Movies.csv')


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

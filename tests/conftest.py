import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

from movie import create_app, metadata, map_model_to_tables
from movie.activitysimulations.movie_watching_simulation import MovieWatchingSimulation
from movie.adapters import database_repository
from movie.adapters.memory_repository import MemoryRepository, populate
from movie.datafilereaders.movie_file_csv_reader import MovieFileCSVReader
from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.person import Person
from movie.domain.review import Review
from movie.domain.user import User
from movie.domain.watchlist import WatchList

TEST_DATA_PATH_MEMORY = './tests/data/movies.csv'
TEST_DATA_PATH_DATABASE = './tests/data/movies.csv'

TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///test.db'


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
    return Movie("TestMovie", 2020, 0)


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
    return [Movie(f'Movie{i}', 2020, i) for i in range(10)]


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
        movie = Movie(f'Movie{i}', 2000 + i, i)
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


@pytest.fixture
def memory_repository():
    return MemoryRepository()


@pytest.fixture
def populated_memory_repository(populated_movies, genres):
    repository = MemoryRepository()
    populate(repository, TEST_DATA_PATH_MEMORY, 123)
    return repository


@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'WTF_CSRF_ENABLED': False,
        'TEST_DATA_PATH': TEST_DATA_PATH_MEMORY,
        'REPOSITORY': 'memory'
    })

    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self._client = client

    def login(self, username='testuser', password='test123A', **kwargs):
        return self._client.post('/login', data={'username': username, 'password': password}, **kwargs)

    def logout(self):
        return self._client.get('/logout')


@pytest.fixture
def auth(client):
    return AuthenticationManager(client)


@pytest.fixture
def database_engine():
    engine = create_engine(TEST_DATABASE_URI_FILE)
    clear_mappers()
    metadata.create_all(engine)  # Conditionally create database tables.
    for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
        engine.execute(table.delete())
    map_model_to_tables()
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield engine
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory()
    metadata.drop_all(engine)
    clear_mappers()


@pytest.fixture
def session_factory():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)
    metadata.create_all(engine)
    for table in reversed(metadata.sorted_tables):
        engine.execute(table.delete())
    map_model_to_tables()
    session_factory = sessionmaker(bind=engine)
    database_repository.populate(engine, TEST_DATA_PATH_DATABASE)
    yield session_factory
    metadata.drop_all(engine)
    clear_mappers()


# @pytest.fixture(autouse=True)
# def reset():
#     clear_mappers()

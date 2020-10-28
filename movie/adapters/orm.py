from datetime import datetime

from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, ForeignKey, Float, Text, func, BigInteger
from sqlalchemy.orm import mapper, relationship

from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User
from movie.domain.watchlist import WatchList
from sqlalchemy.dialects import postgresql, sqlite

# From: https://stackoverflow.com/a/23175518/11628429
BigIntegerType = BigInteger()
BigIntegerType = BigIntegerType.with_variant(postgresql.BIGINT(), 'postgresql')
BigIntegerType = BigIntegerType.with_variant(sqlite.INTEGER(), 'sqlite')

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', BigIntegerType, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, nullable=False, server_default="0"),
    Column('joined_on_utc', DateTime, nullable=False, server_default=func.now())
)

movies = Table(
    'movies', metadata,
    Column('id', BigIntegerType, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_date', Integer, nullable=False),
    Column('description', String(255)),
    Column('director_id', ForeignKey('directors.id')),
    Column('runtime_minutes', Integer),
    Column('rating', Float),
    Column('votes', Integer),
    Column('revenue_millions', Float),
    Column('metascore', Integer)
)

reviews = Table(
    'reviews', metadata,
    Column('id', BigIntegerType, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),  # This is nullable as reviews can be posted anonymously
    Column('movie_id', ForeignKey('movies.id'), nullable=False),
    Column('review_text', Text, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False, server_default=func.now())
)

genres = Table(
    'genres', metadata,
    Column('id', BigIntegerType, primary_key=True, autoincrement=True),
    Column('genre_name', String(255), unique=True, nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', BigIntegerType, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255), unique=True, nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', BigIntegerType, primary_key=True, autoincrement=True),
    Column('director_full_name', String(255), unique=True, nullable=False)
)

user_watched_movies = Table(
    'user_watched_movies', metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.id'), primary_key=True)
)

user_watchlist_movies = Table(
    'user_watchlist_movies', metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('movie_id', ForeignKey('movies.id'), primary_key=True)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', ForeignKey('actors.id'), primary_key=True)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('movie_id', ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', ForeignKey('genres.id'), primary_key=True)
)

actor_colleagues = Table(
    'actor_colleagues', metadata,
    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
    Column('colleague_id', ForeignKey('actors.id'), primary_key=True)
)


def map_model_to_tables():
    mapper(User, users, properties={
        '_id': users.c.id,
        '_mapped_username': users.c.username,
        '_mapped_password': users.c.password,
        '_time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '_joined_on_utc': users.c.joined_on_utc,
        '_watched_movies': relationship(Movie, secondary=user_watched_movies),
        '_reviews': relationship(Review, cascade='all, delete-orphan'),
        '_watchlist': relationship(Movie, secondary=user_watchlist_movies, collection_class=WatchList)
    })

    mapper(Movie, movies, properties={
        '_id': movies.c.id,
        '_mapped_title': movies.c.title,
        '_mapped_release_date': movies.c.release_date,
        '_description': movies.c.description,
        '_director': relationship(Director),
        '_actors': relationship(Actor, secondary=movie_actors),
        '_genres': relationship(Genre, secondary=movie_genres),
        '_runtime_minutes': movies.c.runtime_minutes,
        '_rating': movies.c.rating,
        '_votes': movies.c.votes,
        '_revenue_millions': movies.c.revenue_millions,
        '_metascore': movies.c.metascore
    })

    mapper(Review, reviews, properties={
        '_id': reviews.c.id,
        '_user': relationship(User),
        '_mapped_movie': relationship(Movie),
        '_mapped_review_text': reviews.c.review_text,
        '_mapped_rating': reviews.c.rating,
        '_mapped_timestamp': reviews.c.timestamp
    })

    mapper(Genre, genres, properties={
        '_id': genres.c.id,
        '_genre_name': genres.c.genre_name
    })

    mapper(Actor, actors, properties={
        '_person_full_name': actors.c.actor_full_name,
        '_colleagues': relationship(Actor,
                                    secondary=actor_colleagues,
                                    primaryjoin=(actors.c.id == actor_colleagues.c.actor_id),
                                    secondaryjoin=(actors.c.id == actor_colleagues.c.colleague_id),
                                    backref="actors",
                                    collection_class=set)
    })

    mapper(Director, directors, properties={
        '_person_full_name': directors.c.director_full_name
    })

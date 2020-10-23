from datetime import datetime

from sqlalchemy import Table, MetaData, Column, Integer, String, DateTime, ForeignKey, Float, Text, func
from sqlalchemy.orm import mapper, relationship

from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User
from movie.domain.watchlist import WatchList

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, nullable=False, server_default="0"),
    Column('joined_on_utc', DateTime, nullable=False, server_default=func.now())
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
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
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('movie_id', ForeignKey('movies.id'), nullable=False),
    Column('review_text', Text, nullable=False),
    Column('rating', Integer, nullable=False),
    Column('timestamp', DateTime, nullable=False, default=datetime.utcnow)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(255), unique=True, nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('actor_full_name', String(255), unique=True, nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('director_full_name', String(255), unique=True, nullable=False)
)

user_watched_movies = Table(
    'user_watched_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('movie_id', ForeignKey('movies.id'), nullable=False)
)

user_watchlist_movies = Table(
    'user_watchlist_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id'), nullable=False),
    Column('movie_id', ForeignKey('movies.id'), nullable=False)
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id'), nullable=False),
    Column('actor_id', ForeignKey('actors.id'), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id'), nullable=False),
    Column('genre_id', ForeignKey('genres.id'), nullable=False)
)


def map_model_to_tables():
    mapper(User, users, properties={
        '_id': users.c.id,
        '_mapped_username': users.c.username,
        '_mapped_password': users.c.password,
        '_time_spent_watching_movies_minutes': users.c.time_spent_watching_movies_minutes,
        '_joined_on_utc': users.c.joined_on_utc,
        '_watched_movies': relationship(Movie, secondary=user_watched_movies),
        '_reviews': relationship(Review),
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
        '_mapped_user': relationship(User),
        '_mapped_movie': relationship(Movie),
        '_mapped_review_text': reviews.c.review_text,
        '_mapped_rating': reviews.c.rating,
        '_mapped_timestamp': reviews.c.timestamp
    })

    mapper(Genre, genres, properties={
        '_genre_name': genres.c.name
    })

    mapper(Actor, actors, properties={
        '_person_full_name': actors.c.actor_full_name
    })

    mapper(Director, directors, properties={
        '_person_full_name': directors.c.director_full_name
    })

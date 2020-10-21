from datetime import datetime

from sqlalchemy import Table, MetaData, Column, Integer, String, Date, DateTime, ForeignKey, func, Float, Boolean, Text

from sqlalchemy.orm import mapper, relationship

from movie.domain.user import User

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False),
    Column('time_spent_watching_movies_minutes', Integer, default=0, nullable=False),
    Column('joined_on_utc', DateTime, nullable=False, default=datetime.utcnow)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('release_date', Integer, nullable=False),
    Column('description', String(255)),
    Column('director_id', Integer, ForeignKey('directors.id')),
    Column('runtime_minutes', Integer),
    Column('rating', Float),
    Column('votes', Integer),
    Column('revenue_millions', Float),
    Column('metascore', Integer)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('review_text', Text),
    Column('rating', Integer),
    Column('timestamp', DateTime, nullable=False, default=datetime.utcnow)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Integer, unique=True)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Integer, unique=True)
)

directors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', Integer, unique=True)
)

user_watched_movies = Table(
    'user_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id'))
)

user_watchlist_movies = Table(
    'user_movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('movie_id', Integer, ForeignKey('movies.id'))
)

user_reviews = Table(
    'user_reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('review_id', Integer, ForeignKey('reviews.id'))
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)


def map_model_to_tables():
    # mapper(model.User, users, properties={
    #     '_username': users.c.username,
    #     '_password': users.c.password,
    #     '_comments': relationship(model.Comment, backref='_user')
    # })
    # mapper(model.Comment, comments, properties={
    #     '_comment': comments.c.comment,
    #     '_timestamp': comments.c.timestamp
    # })
    # articles_mapper = mapper(model.Article, articles, properties={
    #     '_id': articles.c.id,
    #     '_date': articles.c.date,
    #     '_title': articles.c.title,
    #     '_first_para': articles.c.first_para,
    #     '_hyperlink': articles.c.hyperlink,
    #     '_image_hyperlink': articles.c.image_hyperlink,
    #     '_comments': relationship(model.Comment, backref='_article')
    # })
    # mapper(model.Tag, tags, properties={
    #     '_tag_name': tags.c.name,
    #     '_tagged_articles': relationship(
    #         articles_mapper,
    #         secondary=article_tags,
    #         backref="_tags"
    #     )
    # })
    mapper(User, users, properties={
        '_id': users.c.id,
        '_username': users.c.username
    })









































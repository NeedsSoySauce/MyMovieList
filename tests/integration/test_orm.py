import pytest

from datetime import datetime

from movie.domain.actor import Actor
from movie.domain.director import Director
from movie.domain.genre import Genre
from movie.domain.movie import Movie
from movie.domain.review import Review
from movie.domain.user import User


def insert_users(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO users (username, password) VALUES (:username, :password)',
                              {'username': value[0], 'password': value[1]})
    rows = empty_session.execute('SELECT id from users').fetchall()
    return [row[0] for row in rows]


def insert_movies(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO movies (title, release_date) VALUES (:title, :release_date)',
                              {'title': value[0], 'release_date': value[1]})
    rows = empty_session.execute('SELECT id from movies').fetchall()
    return [row[0] for row in rows]


def insert_reviews(empty_session, values):
    for value in values:
        empty_session.execute(
            'INSERT INTO reviews (user_id, movie_id, review_text, rating) VALUES (:user_id, :movie_id, :review_text, '
            ':rating)',
            {'user_id': value[0], 'movie_id': value[1], 'review_text': value[2], 'rating': value[3]})
    rows = empty_session.execute('SELECT id from reviews').fetchall()
    return [row[0] for row in rows]


def insert_genres(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO genres (genre_name) VALUES (:genre_name)',
                              {'genre_name': value})
    rows = empty_session.execute('SELECT id from genres').fetchall()
    return [row[0] for row in rows]


def insert_actors(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO actors (actor_full_name) VALUES (:actor_full_name)',
                              {'actor_full_name': value})
    rows = empty_session.execute('SELECT id from actors').fetchall()
    return [row[0] for row in rows]


def insert_actor_colleagues(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO actor_colleagues (actor_id, colleague_id) VALUES (:actor_id, :colleague_id)',
                              {'actor_id': value[0], 'colleague_id': value[1]})
    rows = empty_session.execute('SELECT * from actor_colleagues').fetchall()
    return [row[0] for row in rows]


def insert_directors(empty_session, values):
    for value in values:
        empty_session.execute('INSERT INTO directors (director_full_name) VALUES (:director_full_name)',
                              {'director_full_name': value})
    rows = empty_session.execute('SELECT id from directors').fetchall()
    return [row[0] for row in rows]


def test_loading_of_users(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)

    expected = [
        User("Andrew", "1234"),
        User("Cindy", "1111")
    ]
    assert empty_session.query(User).all() == expected


def test_saving_of_users(empty_session, user):
    empty_session.add(user)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT username, password FROM users'))
    assert rows == [("username", "correcthorsebatterystaple")]


def test_saving_and_loading_of_user_with_movies(empty_session, user, movies):
    empty_session.add_all(movies)

    for movie in movies:
        user.add_to_watchlist(movie)

    user.watch_movie(movies[0])
    user.watch_movie(movies[1])

    empty_session.add(user)
    empty_session.commit()

    expected = user

    result: User = empty_session.query(User).one()

    assert result == expected
    assert result.watched_movies == expected.watched_movies
    assert list(result.watchlist) == list(expected.watchlist)


def test_loading_of_movies(empty_session):
    movies = list()
    movies.append(("Andrew", 2020))
    movies.append(("Cindy", 1999))
    insert_movies(empty_session, movies)

    expected = [
        Movie("Andrew", 2020),
        Movie("Cindy", 1999)
    ]
    assert empty_session.query(Movie).all() == expected


def test_saving_of_movies(empty_session, movie):
    empty_session.add(movie)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT title, release_date FROM movies'))
    assert rows == [("TestMovie", 2020)]


def test_saving_and_loading_of_movie_with_genres_and_actors(empty_session, movie, genres, actors):
    empty_session.add_all(genres)
    empty_session.add_all(actors)

    for genre in genres:
        movie.add_genre(genre)

    for actor in actors:
        movie.add_actor(actor)

    empty_session.add(movie)
    empty_session.commit()

    expected = movie

    result: Movie = empty_session.query(Movie).one()

    assert result == expected
    assert result.genres == expected.genres
    assert result.actors == expected.actors


def test_loading_of_reviews(empty_session):
    users = list()
    users.append(("Andrew", "1234"))
    users.append(("Cindy", "1111"))
    insert_users(empty_session, users)
    users = empty_session.query(User).all()

    movies = list()
    movies.append(("Andrew", 2020))
    movies.append(("Cindy", 1999))
    insert_movies(empty_session, movies)
    movies = empty_session.query(Movie).all()

    # Precision of microseconds in the database can differ
    now = datetime.utcnow().replace(microsecond=0)

    reviews = list()
    reviews.append((users[0].id, movies[0].id, "Description 1", 7, now))
    reviews.append((users[1].id, movies[1].id, "Description 2", 1, now))

    insert_reviews(empty_session, reviews)

    expected = [
        Review(movies[0], "Description 1", 7, now),
        Review(movies[1], "Description 2", 1, now)
    ]

    assert empty_session.query(Review).all() == expected
    assert expected[0].movie == movies[0]
    assert expected[1].movie == movies[1]


def test_saving_of_reviews(empty_session, user, movie, review):
    empty_session.add_all([user, movie, review])
    empty_session.commit()

    rows = list(empty_session.execute('SELECT review_text, rating FROM reviews'))
    assert rows == [("Text  with  some  spaces", 1)]


def test_loading_of_genres(empty_session):
    genres = ["Andrew", "Cindy"]
    insert_genres(empty_session, genres)

    expected = [
        Genre("Andrew"),
        Genre("Cindy")
    ]
    assert empty_session.query(Genre).all() == expected


def test_saving_of_genres(empty_session, genre):
    empty_session.add(genre)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT genre_name FROM genres'))
    assert rows == [("Action",)]


def test_loading_of_actors(empty_session):
    actors = ["Andrew", "Cindy"]
    insert_actors(empty_session, actors)

    expected = [
        Actor("Andrew"),
        Actor("Cindy")
    ]
    assert empty_session.query(Actor).all() == expected


def test_loading_of_actors_with_colleagues(empty_session):
    actors = ["Andrew", "Cindy"]
    ids = insert_actors(empty_session, actors)

    # Create a bidirectional relationship
    actor_colleagues = [
        (ids[0], ids[1]),
        (ids[1], ids[0]),
    ]

    insert_actor_colleagues(empty_session, actor_colleagues)

    expected = [
        Actor("Andrew"),
        Actor("Cindy")
    ]
    expected[0].add_actor_colleague(expected[1])
    expected[1].add_actor_colleague(expected[0])

    results = empty_session.query(Actor).all()
    assert results == expected

    for result, actor in zip(results, expected):
        assert result.colleagues == actor.colleagues


def test_saving_of_actors(empty_session, actor):
    empty_session.add(actor)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT actor_full_name FROM actors'))
    assert rows == [(actor.actor_full_name,)]


def test_saving_of_actors_with_colleagues(empty_session, actor, actors):
    empty_session.add_all(actors)

    for colleague in actors:
        actor.add_actor_colleague(colleague)

    empty_session.add(actor)
    empty_session.commit()

    expected = [(actor.actor_full_name, colleague.actor_full_name) for colleague in actors]

    rows = list(empty_session.execute(f'SELECT a.actor_full_name, c.actor_full_name '
                                      f'FROM actors a '
                                      f'JOIN actor_colleagues b '
                                      f'ON a.id = b.actor_id '
                                      f'JOIN actors c '
                                      f'ON c.id = b.colleague_id '
                                      f'WHERE a.actor_full_name = :actor_full_name '
                                      f'ORDER BY c.actor_full_name',
                                      {
                                          'actor_full_name': actor.actor_full_name
                                      }
                                      ))
    assert rows == expected


def test_loading_of_directors(empty_session):
    directors = ["Andrew", "Cindy"]
    insert_directors(empty_session, directors)

    expected = [
        Director("Andrew"),
        Director("Cindy")
    ]
    assert empty_session.query(Director).all() == expected


def test_saving_of_directors(empty_session, director):
    empty_session.add(director)
    empty_session.commit()

    rows = list(empty_session.execute('SELECT director_full_name FROM directors'))
    assert rows == [(director.director_full_name,)]

import pytest

from movie.adapters.database_repository import SqlAlchemyRepository

# Note: for these tests it's important that the first fixture (if it's being used) is database_repository so that
# map_model_to_tables is called before any models are instantiated
from movie.domain.movie import Movie
from movie.domain.user import User


def test_constructor(session_factory):
    # Fails if any exceptions are thrown
    _ = SqlAlchemyRepository(session_factory)


def test_add_movie(database_repository: SqlAlchemyRepository, movie):
    database_repository.add_movie(movie)

    assert movie in database_repository.get_movies(0)


def test_add_movie_duplicate(database_repository: SqlAlchemyRepository, movie):
    database_repository.add_movie(movie)
    database_repository.add_movie(movie)

    assert len(database_repository.get_movies(0)) == 1
    assert movie in database_repository.get_movies(0)


def test_add_movies(database_repository: SqlAlchemyRepository, movies):
    database_repository.add_movies(movies)

    assert len(database_repository.get_movies(0)) == len(movies)
    assert all(movie in database_repository.get_movies(0) for movie in movies)


def test_add_movies_duplicates(database_repository: SqlAlchemyRepository, movies):
    database_repository.add_movies(movies)
    database_repository.add_movies(movies)

    assert len(database_repository.get_movies(0)) == len(movies)
    assert all(movie in database_repository.get_movies(0) for movie in movies)


def test_get_number_of_movies(database_repository, movies):
    database_repository.add_movies(movies)

    n = database_repository.get_number_of_movies()
    assert n == len(movies)


def test_get_number_of_movies_empty(database_repository):
    n = database_repository.get_number_of_movies()
    assert n == 0


def test_get_movies_page(populated_database_repository):
    print()
    movies = populated_database_repository.get_movies(0, page_size=2)
    print(populated_database_repository._get_all_movies())
    print(movies)
    assert len(movies) == 2


def test_get_movies_page_last_page(populated_database_repository):
    movies = populated_database_repository.get_movies(3, page_size=3)

    assert len(movies) == 1


def test_get_movies_invalid_page_number(populated_database_repository):
    with pytest.raises(ValueError):
        populated_database_repository.get_movies(-1)

    with pytest.raises(TypeError):
        populated_database_repository.get_movies(0.5)


def test_get_movies_invalid_page_size(populated_database_repository):
    with pytest.raises(ValueError):
        populated_database_repository.get_movies(0, page_size=0)

    with pytest.raises(ValueError):
        populated_database_repository.get_movies(0, page_size=-1)

    with pytest.raises(TypeError):
        populated_database_repository.get_movies(0, page_size=0.5)


def test_get_movies_genres_filter(populated_database_repository: SqlAlchemyRepository):
    genres = [genre for genre in populated_database_repository.get_genres() if
              genre.genre_name in ['Action', 'Adventure']]
    repo_movies = populated_database_repository.get_movies(0, genres=genres)
    print()
    print(genres)
    print(populated_database_repository._get_all_movies())
    print(repo_movies)
    print('-----------')
    for movie in repo_movies:
        print(movie, [genre.genre_name for genre in movie.genres])
    assert len(repo_movies) == 4
    for movie in repo_movies:
        assert all(genre in movie.genres for genre in genres)


def test_get_movies_directors_filter(populated_database_repository: SqlAlchemyRepository):
    directors = [director for director in populated_database_repository.get_directors() if
                 director.director_full_name in ['James Gunn', 'Ridley Scott']]
    repo_movies = populated_database_repository.get_movies(0, directors=directors)
    print()
    print(directors)
    print(populated_database_repository._get_all_movies())
    print(repo_movies)
    print('-----------')
    for movie in repo_movies:
        print(movie)
        print(movie.director)
    assert len(repo_movies) == 2
    assert all(movie.director in directors for movie in repo_movies)


def test_get_movies_actors_filter(populated_database_repository: SqlAlchemyRepository):
    actors = [actor for actor in populated_database_repository.get_actors() if
              actor.actor_full_name in ['TestActor1', 'TestActor2']]
    repo_movies = populated_database_repository.get_movies(0, actors=actors)
    print()
    print(actors)
    print(populated_database_repository._get_all_movies())
    print(repo_movies)
    print('-----------')
    for movie in repo_movies:
        print(movie)
        print(movie.actors)
    assert len(repo_movies) == 3
    for movie in repo_movies:
        assert all(actor in movie.actors for actor in actors)


def test_get_movies_invalid_genres(populated_database_repository, genre):
    with pytest.raises(TypeError):
        populated_database_repository.get_movies(0, genres=123)

    with pytest.raises(TypeError):
        populated_database_repository.get_movies(0, genres=[genre, 123])


def test_get_movies_query(database_repository: SqlAlchemyRepository, movie):
    database_repository.add_movie(movie)
    database_repository.add_movie(Movie("abc123", 2222))
    query = movie.title.lower()
    results = database_repository.get_movies(0, query=query)

    print()
    print(query)
    print(results)

    assert len(results) == 1
    assert movie == results[0]


def test_get_movies_query_by_genre(database_repository: SqlAlchemyRepository, movie, genre):
    database_repository.add_genre(genre)
    movie.add_genre(genre)
    database_repository.add_movie(movie)
    database_repository.add_movie(Movie("abc123", 2222))
    query = genre.genre_name.lower()
    results = database_repository.get_movies(0, query=query)

    print()
    print(query)
    print(results)

    assert len(results) == 1
    assert movie == results[0]


def test_get_movies_query_by_director(database_repository: SqlAlchemyRepository, movie, director):
    database_repository.add_director(director)
    movie.director = director
    database_repository.add_movie(movie)
    database_repository.add_movie(Movie(movie.title, movie.release_date))
    query = director.director_full_name
    results = database_repository.get_movies(0, query=query)

    print()
    print(query)
    print(results)

    assert len(results) == 1
    assert movie == results[0]


def test_get_movies_query_by_actor(database_repository: SqlAlchemyRepository, movie, actor):
    database_repository.add_actor(actor)
    movie.add_actor(actor)
    database_repository.add_movie(movie)
    database_repository.add_movie(Movie(movie.title, movie.release_date))
    query = actor.actor_full_name
    results = database_repository.get_movies(0, query=query)

    print()
    print(actor)
    print(results)

    assert len(results) == 1
    assert movie == results[0]


def test_get_movies_invalid_query(populated_database_repository):
    with pytest.raises(TypeError):
        populated_database_repository.get_movies(0, query=123)


def test_get_movies_combined_options(database_repository: SqlAlchemyRepository, genre):
    database_repository.add_genre(genre)

    # TODO - test other filtering options

    movie1 = Movie('A', 2222)
    movie1.add_genre(genre)

    movie2 = Movie('B', 2222)
    movie2.add_genre(genre)

    movie3 = Movie('B', 3333)

    database_repository.add_movies([movie1, movie2, movie3])

    query = movie2.title.lower()
    results = database_repository.get_movies(0, query=query, genres=[genre])

    print()
    print(query)
    print(results)

    assert len(results) == 1
    assert movie2 == results[0]


def test_add_genre(database_repository: SqlAlchemyRepository, genre):
    database_repository.add_genre(genre)

    assert genre in database_repository.get_genres()


def test_add_genre_duplicate(database_repository: SqlAlchemyRepository, genre):
    database_repository.add_genre(genre)
    database_repository.add_genre(genre)

    assert len(database_repository.get_genres()) == 1
    assert genre in database_repository.get_genres()


def test_add_genres(database_repository: SqlAlchemyRepository, genres):
    database_repository.add_genres(genres)

    assert len(database_repository.get_genres()) == len(genres)
    assert all(genre in database_repository.get_genres() for genre in genres)


def test_add_genres_duplicates(database_repository: SqlAlchemyRepository, genres):
    database_repository.add_genres(genres)
    database_repository.add_genres(genres)

    assert len(database_repository.get_genres()) == len(genres)
    assert all(genre in database_repository.get_genres() for genre in genres)


def test_get_genres(database_repository: SqlAlchemyRepository, genres):
    repo_genres = database_repository.get_genres()

    assert all(genre in repo_genres for genre in repo_genres)
    assert sorted(repo_genres) == repo_genres


def test_get_genre(database_repository: SqlAlchemyRepository, genre):
    database_repository.add_genre(genre)
    result = database_repository.get_genre(genre.genre_name)
    assert result == genre


def test_get_genre_not_found(database_repository: SqlAlchemyRepository, genre):
    with pytest.raises(ValueError):
        database_repository.get_genre(genre.genre_name)


def test_get_director(database_repository: SqlAlchemyRepository, director):
    database_repository.add_director(director)
    result = database_repository.get_director(director.director_full_name)
    assert result == director


def test_get_director_not_found(database_repository: SqlAlchemyRepository, director):
    with pytest.raises(ValueError):
        database_repository.get_director(director.director_full_name)


def test_get_actor(database_repository: SqlAlchemyRepository, actor):
    database_repository.add_actor(actor)
    result = database_repository.get_actor(actor.actor_full_name)
    assert result == actor


def test_get_actor_not_found(database_repository: SqlAlchemyRepository, actor):
    with pytest.raises(ValueError):
        database_repository.get_actor(actor.actor_full_name)


def test_get_user(database_repository: SqlAlchemyRepository, user):
    database_repository.add_user(user)
    result = database_repository.get_user(user.username)
    assert result == user


def test_get_user_not_found(database_repository: SqlAlchemyRepository, user):
    with pytest.raises(ValueError):
        database_repository.get_user(user.username)


def test_delete_user(database_repository: SqlAlchemyRepository, user):
    database_repository.add_user(user)

    # Confirm user has been added
    assert database_repository.get_user(user.username) == user

    database_repository.delete_user(user)

    with pytest.raises(ValueError):
        database_repository.get_user(user.username)


def test_change_username(database_repository: SqlAlchemyRepository, user):
    database_repository.add_user(user)

    # Confirm user has been added
    assert database_repository.get_user(user.username) == user

    database_repository.change_username(user, 'qwerty')

    assert database_repository.get_user('qwerty') == user


def test_change_password(database_repository: SqlAlchemyRepository, user):
    database_repository.add_user(user)

    # Confirm user has been added
    assert database_repository.get_user(user.username) == user

    database_repository.change_password(user, 'qwerty')

    assert database_repository.get_user(user.username).password == 'qwerty'


def test_get_movie_by_id(database_repository: SqlAlchemyRepository, movie):
    database_repository.add_movie(movie)
    result = database_repository.get_movie_by_id(movie.id)
    assert result == movie


def test_get_movie_by_id_not_found(database_repository: SqlAlchemyRepository, movie):
    with pytest.raises(ValueError):
        database_repository.get_movie_by_id(movie.id)


def test_get_number_of_movie_pages(populated_database_repository: SqlAlchemyRepository):
    pages = populated_database_repository.get_number_of_movie_pages()
    assert pages == 1


def test_get_number_of_movie_pages_empty(database_repository: SqlAlchemyRepository):
    pages = database_repository.get_number_of_movie_pages()
    assert pages == 0


def test_add_review(database_repository: SqlAlchemyRepository, review):
    database_repository.add_review(review)

    assert review in database_repository._get_all_reviews()


def test_add_review_with_user(database_repository, review, user):
    database_repository.add_review(review, user)

    # Check a relationship is created between the review and the user
    result = database_repository.get_review_user(review)
    assert result == user

    assert review in user.reviews


def test_get_number_of_reviews_for_movie_empty(database_repository, movie):
    assert database_repository.get_number_of_reviews_for_movie(movie) == 0


def test_get_number_of_reviews_for_movie(database_repository, review):
    database_repository.add_review(review)
    assert database_repository.get_number_of_reviews_for_movie(review.movie) == 1


def test_get_number_of_reviews_for_movie_pages(database_repository, review):
    result = database_repository.get_number_of_review_pages_for_movie(review.movie)
    assert result == 0

    database_repository.add_review(review)
    result = database_repository.get_number_of_review_pages_for_movie(review.movie)
    assert result == 1


def test_get_reviews_for_movie(database_repository: SqlAlchemyRepository, review):
    database_repository.add_review(review)
    result = database_repository.get_reviews_for_movie(review.movie, 0)

    assert result[0] == review


def test_get_review_user(database_repository: SqlAlchemyRepository, user, review):
    user.add_review(review)
    database_repository.add_user(user)
    result = database_repository.get_review_user(review)
    assert result == user


def test_get_number_of_movies_for_user_empty(database_repository: SqlAlchemyRepository, user):
    database_repository.add_user(user)

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 0


def test_get_number_of_movies_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)
    user.watch_movie(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 2


def test_get_number_of_movies_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)
    user.watch_movie(movies[0])
    user.add_to_watchlist(movies[1])

    user2 = User('abcd', '1234')
    database_repository.add_user(user2)
    user2.watch_movie(movies[0])
    user2.add_to_watchlist(movies[1])
    user2.add_to_watchlist(movies[2])

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 2

    user.add_to_watchlist(movies[3])
    user.watch_movie(movies[4])

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 4


def test_get_number_of_movie_pages_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)

    result = database_repository.get_number_of_movie_pages_for_user(user)
    assert result == 0

    user.add_to_watchlist(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_number_of_movie_pages_for_user(user, page_size=1)
    assert result == 2


def test_get_movies_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)

    result = database_repository.get_movies_for_user(user, 0)
    assert len(result) == 0

    user.watch_movie(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_movies_for_user(user, 0)
    assert len(result) == 2


def test_get_movies_per_genre(database_repository: SqlAlchemyRepository, genres):
    movies = [
        Movie('abc1', 2000),
        Movie('abc2', 2000),
        Movie('abc3', 2000),
        Movie('abc4', 2000)
    ]

    movies[0].add_genre(genres[0])
    movies[1].add_genre(genres[0])
    movies[2].add_genre(genres[0])

    movies[0].add_genre(genres[1])
    movies[1].add_genre(genres[1])

    movies[1].add_genre(genres[2])
    movies[2].add_genre(genres[2])

    database_repository.add_movies(movies)
    database_repository.add_genres(genres[:4])

    result = database_repository.get_movies_per_genre()
    print()
    print(result)

    expected = {
        genres[0]: 3,
        genres[1]: 2,
        genres[2]: 2,
        genres[3]: 0,
    }

    assert result == expected

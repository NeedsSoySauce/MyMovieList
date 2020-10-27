import pytest

from movie.adapters.database_repository import SqlAlchemyRepository

# Note: for these tests it's important that the first fixture (if it's being used) is database_repository so that
# map_model_to_tables is called before any models are instantiated
from movie.domain.movie import Movie


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
    genres = [genre for genre in populated_database_repository.get_genres() if
              genre.genre_name in ['Action', 'Adventure']]
    repo_movies = populated_database_repository.get_movies(0, genres=genres)
    print()
    print(genres)
    print(populated_database_repository._get_all_movies())
    print(repo_movies)
    print('-----------')
    for movie in repo_movies:
        print(movie)
        print(movie.genres)
    assert len(repo_movies) == 4
    for movie in repo_movies:
        assert all(genre in movie.genres for genre in genres)
    pytest.fail()


def test_get_movies_actors_filter(populated_database_repository: SqlAlchemyRepository):
    genres = [genre for genre in populated_database_repository.get_genres() if
              genre.genre_name in ['Action', 'Adventure']]
    repo_movies = populated_database_repository.get_movies(0, genres=genres)
    print()
    print(genres)
    print(populated_database_repository._get_all_movies())
    print(repo_movies)
    print('-----------')
    for movie in repo_movies:
        print(movie)
        print(movie.genres)
    assert len(repo_movies) == 4
    for movie in repo_movies:
        assert all(genre in movie.genres for genre in genres)
    pytest.fail()


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
    results = database_repository.get_movies(0, directors=[director])

    print()
    print(director)
    print(results)

    assert len(results) == 1
    assert movie == results[0]


def test_get_movies_query_by_actor(database_repository: SqlAlchemyRepository, movie, director):
    database_repository.add_director(director)
    movie.director = director
    database_repository.add_movie(movie)
    database_repository.add_movie(Movie(movie.title, movie.release_date))
    results = database_repository.get_movies(0, directors=[director])

    print()
    print(director)
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


def test_add_genre(genre, database_repository: SqlAlchemyRepository):
    database_repository.add_genre(genre)

    assert genre in database_repository._genres
    pytest.fail()


def test_add_genre_duplicate(database_repository: SqlAlchemyRepository, genre):
    database_repository.add_genre(genre)
    database_repository.add_genre(genre)

    assert len(database_repository._genres) == 1
    assert genre in database_repository._genres
    pytest.fail()


def test_add_genres(database_repository: SqlAlchemyRepository, genres):
    database_repository.add_genres(genres)

    assert len(database_repository._genres) == len(genres)
    assert all(genre in database_repository._genres for genre in genres)
    pytest.fail()


def test_add_genres_duplicates(database_repository: SqlAlchemyRepository, genres):
    database_repository.add_genres(genres)
    database_repository.add_genres(genres)

    assert len(database_repository._genres) == len(genres)
    assert all(genre in database_repository._genres for genre in genres)
    pytest.fail()


def test_get_genres(database_repository: SqlAlchemyRepository, genres):
    repo_genres = database_repository.get_genres()

    assert all(genre in repo_genres for genre in repo_genres)
    assert sorted(repo_genres) == repo_genres
    pytest.fail()


def test_get_number_of_movie_pages(populated_database_repository: SqlAlchemyRepository):
    pages = populated_database_repository.get_number_of_movie_pages()
    assert pages == 1
    pytest.fail()


def test_get_number_of_movie_pages_empty(database_repository: SqlAlchemyRepository):
    pages = database_repository.get_number_of_movie_pages()
    assert pages == 0
    pytest.fail()


def test_add_review(database_repository: SqlAlchemyRepository, review):
    database_repository.add_review(review)

    assert review in database_repository._reviews
    pytest.fail()


def test_add_review_with_user(database_repository, review, user):
    database_repository.add_review(review, user)

    # Check a relationship is created between the review and the user
    result = database_repository.get_review_user(review)
    assert result == user

    assert review in user.reviews
    pytest.fail()


def test_get_number_of_reviews_for_movie_empty(database_repository, movie):
    assert database_repository.get_number_of_reviews_for_movie(movie) == 0
    pytest.fail()


def test_get_number_of_reviews_for_movie(database_repository, review):
    database_repository.add_review(review)
    assert database_repository.get_number_of_reviews_for_movie(review.movie) == 1
    pytest.fail()


def test_get_number_of_reviews_for_movie_pages(database_repository, review):
    result = database_repository.get_number_of_review_pages_for_movie(review.movie)
    assert result == 0
    pytest.fail()

    database_repository.add_review(review)
    result = database_repository.get_number_of_review_pages_for_movie(review.movie)
    assert result == 1
    pytest.fail()


def test_get_reviews_for_movie(database_repository: SqlAlchemyRepository, review):
    database_repository.add_review(review)
    result = database_repository.get_reviews_for_movie(review.movie, 0)

    assert result[0] == review
    pytest.fail()


def test_get_review_user(database_repository: SqlAlchemyRepository, user, review):
    user.add_review(review)
    database_repository.add_user(user)
    result = database_repository.get_review_user(review)
    assert result == user
    pytest.fail()


def test_get_number_of_movies_for_user_empty(database_repository: SqlAlchemyRepository, user):
    database_repository.add_user(user)

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 0
    pytest.fail()


def test_get_number_of_movies_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)
    user.watch_movie(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 2
    pytest.fail()


def test_get_number_of_movies_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)
    user.watch_movie(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_number_of_movies_for_user(user)
    assert result == 2
    pytest.fail()


def test_get_number_of_movie_pages_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)

    result = database_repository.get_number_of_movie_pages_for_user(user)
    assert result == 0

    user.add_to_watchlist(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_number_of_movie_pages_for_user(user, 1)
    assert result == 2
    pytest.fail()


def test_get_movies_for_user(database_repository: SqlAlchemyRepository, user, movies):
    database_repository.add_user(user)

    result = database_repository.get_movies_for_user(user, 0)
    assert len(result) == 0

    user.watch_movie(movies[0])
    user.add_to_watchlist(movies[1])

    result = database_repository.get_movies_for_user(user, 0)
    assert len(result) == 2
    pytest.fail()

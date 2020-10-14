from typing import List, NamedTuple

from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, StringField

from movie.adapters.repository import AbstractRepository
from movie.domain.director import Director
from movie.domain.movie import Movie
from movie.utilities.services import get_genres, get_actors, get_directors

DEFAULT_PAGE_SIZE = 25


# Note - page numbers starts from 0.
class SearchResults(NamedTuple):
    movies: List[Movie] = []
    hits: int = 0
    page: int = 0
    pages: int = 0


def search_movies(repo: AbstractRepository,
                  page_number: int,
                  page_size: int = DEFAULT_PAGE_SIZE,
                  query: str = '',
                  genres: List[str] = [],
                  directors: List[str] = [],
                  actors: List[str] = []) -> SearchResults:
    """
    Searches for movies using the given filtering options and returns a SearchResults NamedTuple.

    Check the get_movies method in AbstractRepository for info on filtering options.
    """
    try:
        genres = [repo.get_genre(name) for name in genres]
    except ValueError:
        return SearchResults([], 0, page_number, 0)

    if directors:
        try:
            directors = [repo.get_director(name) for name in directors]
        except ValueError:
            return SearchResults([], 0, page_number, 0)

    try:
        actors = [repo.get_actor(name) for name in actors]
    except ValueError:
        return SearchResults([], 0, page_number, 0)

    movies = repo.get_movies(page_number, page_size, query, genres, directors, actors)
    hits = repo.get_number_of_movies(query, genres, directors, actors)
    pages = repo.get_number_of_movie_pages(page_size, query, genres, directors, actors)

    return SearchResults(movies, hits, page_number, pages)


def create_search_form(repo: AbstractRepository, request_args):
    """ Returns a MovieSearchForm populated with options from the given repository. """

    genres = get_genres(repo)
    directors = get_directors(repo)
    actors = get_actors(repo)

    form = MovieSearchForm(request_args, meta={'csrf': False})
    form.genre.choices = [(genre.genre_name, genre.genre_name) for genre in genres] + [('', 'Genre')]
    form.director.choices = [(director.director_full_name, director.director_full_name) for director in directors] + [
        ('', 'Director')]
    form.actor.choices = [(actor.actor_full_name, actor.actor_full_name) for actor in actors] + [('', 'Actor')]

    return form


class MovieSearchForm(FlaskForm):
    query = StringField("Query")
    genre = SelectMultipleField('Genres')
    director = SelectMultipleField('Directors')
    actor = SelectMultipleField('Actors')
    submit = SubmitField('Submit')

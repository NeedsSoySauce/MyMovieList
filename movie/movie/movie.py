from flask import Blueprint, render_template, request, abort

from .services import *

from movie.adapters.repository import instance as repo
movie_blueprint = Blueprint(
    'movie_bp', __name__)


@movie_blueprint.route('/movie/<movie_id>', methods=['GET'])
def get_movie(movie_id: int):

    try:
        movie = get_movie_by_id(repo, int(movie_id))
    except ValueError:
        abort(404)

    return render_template(
        'movie/movie.html',
        movie=movie
    )

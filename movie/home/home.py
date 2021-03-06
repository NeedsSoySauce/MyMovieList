from flask import Blueprint, render_template, request, current_app

from movie.search.services import create_search_form
from movie.utilities.services import get_number_of_movies, get_movies_per_genre

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    repo = current_app.config['REPOSITORY']
    form = create_search_form(repo, request.args)

    return render_template(
        'home/home.html',
        num_movies=get_number_of_movies(repo),
        genre_movies=get_movies_per_genre(repo),
        form=form
    )

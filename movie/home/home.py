from flask import Blueprint, render_template

from movie.adapters.repository import instance as repo

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        num_movies=repo.get_number_of_movies(),
        genres=repo.get_genres()
    )

from flask import Blueprint, render_template

import movie.adapters.repository as repo

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        num_movies=repo.instance.get_number_of_movies(),
        genres=repo.instance.get_genres()
    )

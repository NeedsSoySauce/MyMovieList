from flask import Blueprint, render_template

from movie.home.services import *

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        num_movies=get_number_of_movies(),
        genres=get_genres()
    )

from flask import Blueprint, render_template

from movie.home.services import *

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():

    genres = get_genres()
    directors = get_directors()
    actors = get_actors()

    return render_template(
        'home/home.html',
        num_movies=get_number_of_movies(),
        genres=genres,
        genre_movies=get_movies_per_genre(genres),
        directors=directors,
        director_movies=get_movies_per_director(directors),
        actors=actors,
        actor_movies=get_movies_per_actor(actors)
    )

from flask import Blueprint, render_template

from movie.adapters.repository import instance as repo
from movie.home.services import *

home_blueprint = Blueprint(
    'home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():

    genres = get_genres(repo)
    directors = get_directors(repo)
    actors = get_actors(repo)

    return render_template(
        'home/home.html',
        num_movies=get_number_of_movies(repo),
        genres=genres,
        genre_movies=get_movies_per_genre(repo, genres),
        directors=directors,
        director_movies=get_movies_per_director(repo, directors),
        actors=actors,
        actor_movies=get_movies_per_actor(repo, actors)
    )

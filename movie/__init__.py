"""Initialize Flask app."""

import os

from flask import Flask, render_template

import movie.adapters.repository as repo
from movie.adapters.memory_repository import MemoryRepository
from movie.adapters.repository import populate


def page_not_found(e):
    return render_template('404.html'), 404


def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('movie', 'adapters', 'data', 'Data1000Movies.csv')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.instance = MemoryRepository()
    populate(repo.instance, data_path)

    # Build the application - these steps require an application context.
    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .movie import movie
        app.register_blueprint(movie.movie_blueprint)

        from .auth import auth
        app.register_blueprint(auth.auth_blueprint)

        from .watchlist import watchlist
        app.register_blueprint(watchlist.watchlist_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        app.register_error_handler(404, page_not_found)

    return app

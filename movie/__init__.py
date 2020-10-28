"""Initialize Flask app."""

import os
from typing import Union

from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.pool import NullPool

from movie.adapters import database_repository, memory_repository
from movie.adapters.orm import metadata, map_model_to_tables
from movie.adapters.repository import AbstractRepository


def page_not_found(e):
    return render_template('404.html'), 404


def create_app(test_config=None):
    """ Construct the core application. """

    # Create the Flask app object.
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = os.path.join('movie', 'adapters', 'data', 'Data1000Movies.csv')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Setup our repository
    repo: Union[memory_repository.MemoryRepository, database_repository.SqlAlchemyRepository, None] = None
    repository = app.config['REPOSITORY']

    if repository == 'memory':
        # Create the MemoryRepository implementation for a memory-based repository.
        repo = memory_repository.MemoryRepository()
        memory_repository.populate(repo, data_path, 123)

    elif repository == 'database':
        # Configure database.
        database_uri = app.config['SQLALCHEMY_DATABASE_URI']

        database_echo = app.config['SQLALCHEMY_ECHO']
        database_engine = create_engine(database_uri,
                                        connect_args={"check_same_thread": False},
                                        poolclass=NullPool,
                                        echo=database_echo
                                        )

        is_testing_or_init = app.config['TESTING'] is True or len(database_engine.table_names()) == 0

        if is_testing_or_init:
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            metadata.create_all(database_engine)  # Conditionally create database tables.
            for table in reversed(metadata.sorted_tables):  # Remove any data from the tables.
                database_engine.execute(table.delete())

        # Generate mappings that map domain model classes to the database tables.
        map_model_to_tables()

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo = database_repository.SqlAlchemyRepository(session_factory)

        if is_testing_or_init:
            print("-----------------------------------------------------------")
            print("------------------ REPOPULATING DATABASE ------------------")
            print("-----------------------------------------------------------")

            database_repository.populate(repo, data_path, 123)
    else:
        raise ValueError(f"Invalid repository '{repository}', should be 'memory' or 'database'")

    app.config['REPOSITORY'] = repo

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

        from .user import user
        app.register_blueprint(user.user_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        app.register_error_handler(404, page_not_found)

        if isinstance(repo, database_repository.SqlAlchemyRepository):
            # Register a callback that associates database sessions with http requests
            # Sessions are reset inside the database repository before a new flask request is generated
            @app.before_request
            def before_flask_http_request_function():
                repo.reset_session()

            # Register a tear-down method that will be called after each request has been processed
            @app.teardown_appcontext
            def shutdown_session(exception=None):
                repo.close_session()

    return app

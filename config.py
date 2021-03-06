"""Flask configuration variables."""
from os import environ, path, getenv
from dotenv import load_dotenv

# Load environment variables from file .env, stored in this directory.
load_dotenv()


def _get_bool(key: str) -> bool:
    return environ.get(key) == 'True'


class Config:
    """Set Flask configuration from .env file."""

    # Flask configuration
    FLASK_APP = environ.get('FLASK_APP')
    FLASK_ENV = environ.get('FLASK_ENV')

    SECRET_KEY = environ.get('SECRET_KEY')
    TESTING = _get_bool('TESTING')

    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_ECHO = _get_bool('SQLALCHEMY_ECHO')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REPOSITORY = environ.get('REPOSITORY')

    # Flask-Caching configuration
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 60

    # Data file reader configuration
    MAX_LINES_TO_LOAD = int(environ.get('MAX_LINES_TO_LOAD') or 0) or None


class HerokuProductionConfig(Config):
    """Set Flask configuration from Heroku environment variables."""

    # Database configuration
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

    # Flask-Caching configuration
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = environ.get('REDIS_URL')

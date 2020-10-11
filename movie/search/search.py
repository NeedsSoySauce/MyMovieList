from flask import Blueprint, render_template, request, current_app, session, url_for
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from movie.adapters.repository import instance as repo
from .services import search_movies
from ..auth import services as auth

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    user = None

    try:
        user = auth.get_user(repo, session['username'])
    except auth.UnknownUserException:
        # invalid session
        session.clear()
        return redirect(url_for('auth_bp.login'))
    except KeyError:
        # User isn't logged in
        pass

    # Page numbers are displayed as starting from 1 so subtract 1
    try:
        page = int(request.args.get('page') or 1) - 1
        page_size = int(request.args.get('size') or 25)
    except ValueError:
        abort(404)

    query = request.args.get('query') or ''
    genres = request.args.getlist('genre')
    director = request.args.get('director') or None
    actors = request.args.getlist('actor')

    if page < 0:
        abort(404)

    results = search_movies(repo, page, page_size=page_size, query=query, genres=genres, director=director,
                            actors=actors)

    if page >= results.pages:
        abort(404)

    return render_template(
        'search/search.html',
        movies=results.movies,
        hits=results.hits,
        page=results.page,
        pages=results.pages,
        page_size=page_size,
        args={key: request.args[key] for key in request.args if key != 'page'},
        pagination_endpoint='search_bp.search',
        user=user
    )

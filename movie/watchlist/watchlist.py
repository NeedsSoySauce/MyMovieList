from typing import Union

from flask import Blueprint, render_template, session, url_for, request, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from movie.auth.auth import login_required
from movie.movie import services as movie_service
from .services import get_user_movies, DEFAULT_PAGE_SIZE, add_movie_to_watchlist, remove_movie_from_watchlist, \
    add_movie_to_watched, remove_movie_from_watched
from ..auth import services as auth
from ..movie.services import get_movie_by_id

watchlist_blueprint = Blueprint(
    'watchlist_bp', __name__)


@watchlist_blueprint.route('/watchlist', defaults={'movie_id': None})
@watchlist_blueprint.route('/watchlist/<int:movie_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def watchlist(movie_id: Union[int, None]):
    repo = current_app.config['REPOSITORY']
    username = session['username']
    try:
        user = auth.get_user(repo, username)
    except auth.UnknownUserException:
        current_app.logger.debug(f"Unknown user '{username}'")
        # invalid session
        session.clear()
        return redirect(url_for('auth_bp.login'))

    if request.method in ['POST', 'DELETE']:
        try:
            movie = get_movie_by_id(repo, movie_id)
        except ValueError:
            abort(404)

        if request.method == 'POST':
            add_movie_to_watchlist(repo, user, movie)
            return 'Created', 201
        elif request.method == 'DELETE':
            remove_movie_from_watchlist(repo, user, movie)
            return 'Deleted', 200

    # Page numbers are displayed as starting from 1 so subtract 1
    try:
        page = int(request.args.get('page') or 1) - 1
        page_size = int(request.args.get('size') or DEFAULT_PAGE_SIZE)
    except ValueError:
        abort(404)

    current_app.logger.debug(f"page = {page}")

    if page < 0:
        abort(404)

    results = get_user_movies(repo, user, page, page_size)

    # The last page can move as the user can add/remove items from their watchlist, so redirect to the new last page
    # if they request the previous one
    if page == 0:
        # First page. This page always exists.
        pass
    elif page == results.pages:
        return redirect(url_for('watchlist_bp.watchlist', page=results.pages))
    elif page > results.pages:
        abort(404)

    return render_template(
        'watchlist/watchlist.html',
        user=user,
        movies=results.movies,
        page=results.page,
        page_size=page_size,
        pages=results.pages,
        hits=results.hits,
        pagination_endpoint='watchlist_bp.watchlist',
        args={key: request.args[key] for key in request.args if key != 'page'}
    )


@watchlist_blueprint.route('/watch/<int:movie_id>', methods=['POST', 'DELETE'])
@login_required
def watch(movie_id: Union[int, None]):
    repo = current_app.config['REPOSITORY']
    username = session['username']

    try:
        user = auth.get_user(repo, username)
    except auth.UnknownUserException:
        current_app.logger.debug(f"Unknown user '{username}'")
        # invalid session
        session.clear()
        return redirect(url_for('auth_bp.login'))

    try:
        movie = get_movie_by_id(repo, movie_id)
    except ValueError:
        abort(404)

    if request.method == 'POST':
        add_movie_to_watched(repo, user, movie)
        return 'Created', 201
    else:
        remove_movie_from_watched(repo, user, movie)
        return 'Deleted', 200

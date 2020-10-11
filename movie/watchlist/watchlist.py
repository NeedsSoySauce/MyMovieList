from typing import Union

from flask import Blueprint, render_template, session, url_for, request, current_app
from werkzeug.exceptions import abort
from werkzeug.utils import redirect

from movie.adapters.repository import instance as repo
from movie.auth.auth import login_required
from movie.movie import services as movie_service
from .services import get_watchlist_movies

from ..auth import services as auth

watchlist_blueprint = Blueprint(
    'watchlist_bp', __name__)


@watchlist_blueprint.route('/watchlist', defaults={'movie_id': None})
@watchlist_blueprint.route('/watchlist/<int:movie_id>', methods=['GET', 'POST', 'DELETE'])
@login_required
def watchlist(movie_id: Union[int, None]):
    user_name = session['username']
    try:
        user = auth.get_user(repo, user_name)
    except auth.UnknownUserException:
        current_app.logger.debug(f"Unknown user 'user_name'")
        # invalid session
        session.clear()
        return redirect(url_for('auth_bp.login'))

    if request.method in ['POST', 'DELETE']:
        try:
            movie = movie_service.get_movie_by_id(repo, movie_id)
        except ValueError:
            abort(404)

        if request.method == 'POST':
            user.add_to_watchlist(movie)
            return 'Created', 201
        elif request.method == 'DELETE':
            user.remove_from_watchlist(movie)
            return 'Deleted', 200

    # Page numbers are displayed as starting from 1 so subtract 1
    try:
        page = int(request.args.get('page') or 1) - 1
        page_size = int(request.args.get('size') or 2)
    except ValueError:
        abort(404)

    current_app.logger.debug(f"page = {page}")

    if page < 0:
        abort(404)

    results = get_watchlist_movies(user, page, page_size)

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
        args={key: request.args[key] for key in request.args if key != 'page'},
    )

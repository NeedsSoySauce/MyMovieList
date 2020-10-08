from flask import Blueprint, render_template, request, current_app

from .services import search_movies

search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():
    # Page numbers are displayed as starting from 1 so subtract 1
    page = int(request.args.get('page') or 1) - 1
    page_size = int(request.args.get('size') or 25)
    query = request.args.get('query') or ''
    genres = request.args.getlist('genre')

    results = search_movies(page, page_size=page_size, query=query, genres=genres)

    current_app.logger.info(f"page = {page}, page_size = {page_size}, query = {query}, genres = {genres}")

    return render_template(
        'search/search.html',
        movies=results.movies,
        hits=results.hits,
        page=results.page,
        pages=results.pages,
        page_size=page_size,
        args={key: request.args[key] for key in request.args if key != 'page'}
    )

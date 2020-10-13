from better_profanity import profanity
from flask import Blueprint, render_template, abort, session, url_for, request, current_app
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import ValidationError, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

import movie.adapters.repository as repo
from .services import *
from ..auth import services as auth

movie_blueprint = Blueprint(
    'movie_bp', __name__)

INVALID_CHOICE_MESSAGE = 'Invalid Choice: could not coerce'

INVALID_REVIEW_TEXT_MESSAGE = 'Invalid review text.'
RATING_REQUIRED_MESSAGE = 'Ratings must be an integer between 1 and 10.'
INVALID_RATING_RANGE_MESSAGE = 'Ratings must be an integer between 1 and 10.'

REVIEW_TEXT_REQUIRED_MESSAGE = 'Reviews must be at least one character long.'
INVALID_REVIEW_TEXT_LENGTH_MESSAGE = 'Reviews must be at least one character long.'
REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE = 'Please keep it PG (no profanity!).'


@movie_blueprint.route('/movie/<int:movie_id>', methods=['GET'])
def movie(movie_id: int):
    repo = current_app.config['REPOSITORY']
    user = None

    try:
        movie = get_movie_by_id(repo, int(movie_id))
    except ValueError:
        abort(404)

    try:
        user = auth.get_user(repo, session['username'])
    except ValueError:
        # No user with the given username
        pass
    except KeyError:
        # No active session, anonymous/guest user
        pass
    except auth.UnknownUserException:
        # Invalid session
        session.clear()
        pass

    return render_template(
        'movie/summary.html',
        movie=movie,
        tab=0,
        user=user
    )


@movie_blueprint.route('/movie/<int:movie_id>/reviews', methods=['GET', 'POST'])
def reviews(movie_id: int):
    repo = current_app.config['REPOSITORY']
    user = None
    review_error_message = None

    try:
        movie = get_movie_by_id(repo, int(movie_id))
    except ValueError:
        abort(404)

    try:
        user = auth.get_user(repo, session['username'])
    except ValueError:
        # No user with the given username
        pass
    except KeyError:
        # No active session, anonymous/guest user
        pass
    except auth.UnknownUserException:
        # Invalid session
        session.clear()
        pass

    # Page numbers are displayed as starting from 1 so subtract 1
    try:
        page = int(request.args.get('page') or 1) - 1
        page_size = int(request.args.get('size') or 2)
    except ValueError:
        abort(404)

    if page < 0:
        abort(404)

    results = get_movie_reviews(repo, movie, page, page_size)

    if page >= results.pages and page != 0:
        abort(404)

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review has passed data validation.

        # Use the service layer to store the new review.
        add_review(repo, movie, form.review.data, form.rating.data, user)

        # Reload the page to show the new review
        return redirect(url_for('movie_bp.reviews', movie_id=movie.id))

    # Request is a HTTP POST where form validation has failed.
    if request.method == 'POST':
        review_error_message = 'Invalid review.'

    reviews = results.reviews
    reviews_user_map = get_reviews_user_map(repo, reviews)

    args = {key: request.args[key] for key in request.args if key != 'page'}
    args['movie_id'] = movie.id

    return render_template(
        'movie/reviews.html',
        movie=movie,
        reviews=reviews,
        reviews_user_map=reviews_user_map,
        review_error_message=review_error_message,
        form=form,
        tab=1,
        page=results.page,
        page_size=page_size,
        pages=results.pages,
        hits=results.hits,
        pagination_endpoint='movie_bp.reviews',
        args=args,
        user=user
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = INVALID_REVIEW_TEXT_MESSAGE
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    rating = SelectField('Rating',
                         [DataRequired(message=RATING_REQUIRED_MESSAGE),
                          NumberRange(min=1, max=10, message=INVALID_RATING_RANGE_MESSAGE)],
                         choices=range(1, 11),
                         coerce=int,
                         default=10,

                         )
    review = TextAreaField('Review', [
        DataRequired(message=REVIEW_TEXT_REQUIRED_MESSAGE),
        Length(min=1, message=INVALID_REVIEW_TEXT_LENGTH_MESSAGE),
        ProfanityFree(message=REVIEW_TEXT_CONTAINS_PROFANITY_MESSAGE)
    ])
    submit = SubmitField('Submit')

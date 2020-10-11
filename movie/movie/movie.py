from better_profanity import profanity
from flask import Blueprint, render_template, abort, session, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import ValidationError, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

from movie.adapters.repository import instance as repo
from .services import *
from ..auth import services as auth

movie_blueprint = Blueprint(
    'movie_bp', __name__)


@movie_blueprint.route('/movie/<movie_id>', methods=['GET'])
def movie(movie_id: int):
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

    form = ReviewForm()

    return render_template(
        'movie/summary.html',
        movie=movie,
        tab=0
    )


@movie_blueprint.route('/movie/<movie_id>/reviews', methods=['GET', 'POST'])
def reviews(movie_id: int):
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

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review has passed data validation.

        # Use the service layer to store the new review.
        add_review(repo, Review(movie, form.review.data, form.rating.data), user)

        # Reload the page to show the new review
        return redirect(url_for('movie_bp.reviews', movie_id=movie.id))

    # Request is a HTTP POST where form validation has failed.
    if request.method == 'POST':
        review_error_message = 'Invalid review.'

    reviews = get_movie_reviews(repo, movie)
    reviews_user_map = get_reviews_user_map(repo, reviews)

    return render_template(
        'movie/reviews.html',
        movie=movie,
        reviews=reviews,
        reviews_user_map=reviews_user_map,
        review_error_message=review_error_message,
        form=form,
        tab=1
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=1, message='Reviews must be at least one character long.'),
        ProfanityFree(message='Please keep it PG (no profanity!).')
    ])
    rating = SelectField('Rating',
                         validators=[DataRequired(), NumberRange(min=1, max=10)],
                         choices=range(1, 11),
                         coerce=int)
    submit = SubmitField('Submit')

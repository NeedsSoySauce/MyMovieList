from better_profanity import profanity
from flask import Blueprint, render_template, abort, session, url_for, request
from flask_wtf import FlaskForm
from werkzeug.utils import redirect
from wtforms import ValidationError, TextAreaField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange

from movie.adapters.repository import instance as repo
from .services import *
from ..utilities import services as utilities

movie_blueprint = Blueprint(
    'movie_bp', __name__)


@movie_blueprint.route('/movie/<movie_id>', methods=['GET', 'POST'])
def movie(movie_id: int):
    user = None
    review_error_message = None

    tab = int(request.args.get('tab') or 0)

    try:
        movie = get_movie_by_id(repo, int(movie_id))
    except ValueError:
        abort(404)

    try:
        user = utilities.get_user(repo, session['username'])
    except ValueError:
        # No user with the given username
        pass
    except KeyError:
        # No active session, anonymous/guest user
        pass

    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review has passed data validation.

        # Use the service layer to store the new review.
        add_review(repo, Review(movie, form.review.data, form.rating.data), user)

        # Reload the page to show the new review
        return redirect(url_for('movie_bp.movie', movie_id=movie_id, tab=1))

    # Request is a HTTP POST where form validation has failed.
    if request.method == 'POST':
        tab = 1
        review_error_message = 'Invalid review.'

    reviews = get_movie_reviews(repo, movie)
    reviews_user_map = get_reviews_user_map(repo, reviews)

    return render_template(
        'movie/movie.html',
        movie=movie,
        reviews=reviews,
        reviews_user_map=reviews_user_map,
        review_error_message=review_error_message,
        form=form,
        movie_id=movie_id,
        tab=tab
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

from urllib.parse import quote_plus

from flask import Blueprint, render_template, request, session, url_for
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

from movie.adapters.repository import instance as repo
from movie.auth import auth
from movie.auth.auth import UnknownUserException, PasswordValid, login_required, AuthenticationException, \
    NameNotUniqueException

user_blueprint = Blueprint(
    'user_bp', __name__)


@user_blueprint.route('/user/<string:username>', methods=['GET'])
def user(username: str):
    user = None

    change_password_form = ChangePasswordForm()
    change_password_error_message = None
    is_password_change_success = False

    change_username_form = ChangeUsernameForm()
    change_username_error_message = None

    # If a user's username is successfully changed they'll be redirected here under the new url for their username.
    # Within the session object we store a flag to tell us whether or not this call is the result of the above redirect.
    is_username_change_success = bool(session.get('is_username_change_success', False))
    session.pop('is_username_change_success', None)

    try:
        user = auth.get_user(repo, username)
    except UnknownUserException:
        # No user with the given username
        abort(404)

    if request.path == f'/user/{username}/password/change':
        # Request is a POST to change password
        if change_password_form.validate_on_submit():
            current_password = change_password_form.current_password.data
            new_password = change_password_form.new_password.data

            if current_password == new_password:
                change_password_error_message = "Passwords must be different."
            else:
                try:
                    # Check the current password is valid for this user
                    auth.authenticate_user(repo, username, current_password)

                    auth.change_password(repo, user, new_password)
                    is_password_change_success = True
                except AuthenticationException:
                    # Incorrect password
                    change_password_error_message = "Incorrect password - please check and try again."
                except UnknownUserException:
                    # User isn't recognized at this point (unlikely)
                    abort(404)
    elif request.path == f'/user/{username}/username/change':
        # Request is a POST to change username
        if change_username_form.validate_on_submit():
            new_username = change_username_form.new_username.data

            try:
                auth.change_username(repo, user, new_username)
                session['username'] = new_username
                is_username_change_success = True

                session['is_username_change_success'] = True
                return redirect(url_for('user_bp.user', username=quote_plus(new_username)))
            except NameNotUniqueException:
                # Incorrect password
                change_username_error_message = "Username unavailable."

    return render_template(
        'user/user.html',
        user=user,
        change_password_form=change_password_form,
        change_password_error_message=change_password_error_message,
        is_password_change_success=is_password_change_success,
        change_username_form=change_username_form,
        change_username_error_message=change_username_error_message,
        is_username_change_success=is_username_change_success
    )


@user_blueprint.route('/user/<string:username>/password/change', methods=['POST'])
@login_required
def change_password(username: str):
    return user(username)


@user_blueprint.route('/user/<string:username>/username/change', methods=['POST'])
@login_required
def change_username(username: str):
    return user(username)


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', [
        DataRequired(message='Current password required.')
    ])
    new_password = PasswordField('New password', [
        DataRequired(message='New password required.'),
        PasswordValid()])
    submit = SubmitField('Submit')


class ChangeUsernameForm(FlaskForm):
    new_username = StringField('New username', [
        DataRequired(message='New username required.'),
        Length(min=3, message='Usernames must be at least 3 characters')
    ])
    submit = SubmitField('Submit')

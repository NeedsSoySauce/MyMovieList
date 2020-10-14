from flask import Blueprint, render_template, request, session, url_for, current_app
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from werkzeug.utils import redirect
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired, Length

from movie.auth import auth
from movie.auth.auth import UnknownUserException, PasswordValid, login_required, AuthenticationException, \
    NameNotUniqueException

user_blueprint = Blueprint(
    'user_bp', __name__)

NEW_USERNAME_REQUIRED_MESSAGE = 'New username required.'

CURRENT_PASSWORD_REQUIRED_MESSAGE = 'Current password required.'
NEW_PASSWORD_REQUIRED_MESSAGE = 'New password required.'
PASSWORDS_EQUAL_MESSAGE = "Passwords must be different."

CONFIRMATION_REQUIRED_MESSAGE = 'Confirmation required.'
CONFIRMATION_FAILED_MESSAGE = "Confirmation failed - enter your username to confirm."


@user_blueprint.route('/user/<string:username>', methods=['GET'])
def user(username: str):
    repo = current_app.config['REPOSITORY']
    user = None

    change_password_form = ChangePasswordForm()
    change_password_error_message = None

    change_username_form = ChangeUsernameForm()
    change_username_error_message = None

    # If a user's username is successfully changed they'll be redirected here under the new url for their username.
    # Within the session object we store a flag to tell us whether or not this call is the result of the above redirect.
    is_username_change_success = bool(session.get('is_username_change_success', False))
    session.pop('is_username_change_success', None)

    # Same as above but for password change
    is_password_change_success = bool(session.get('is_password_change_success', False))
    session.pop('is_password_change_success', None)

    delete_account_form = DeleteAccountForm()
    delete_account_error_message = None

    try:
        user = auth.get_user(repo, username)
    except UnknownUserException:
        # No user with the given username
        abort(404)

    # User's can't take actions for other users
    if request.method == 'POST' and session['username'] != username:
        abort(401)

    if request.path == f'/user/{username}/username/change':
        # Request is a POST to change username
        if change_username_form.validate_on_submit():
            new_username = change_username_form.new_username.data

            try:
                auth.change_username(repo, user, new_username)
                session['username'] = new_username
                session['is_username_change_success'] = True
                return redirect(url_for('user_bp.user', username=new_username))
            except NameNotUniqueException:
                # Incorrect password
                change_username_error_message = auth.USERNAME_UNAVAILABLE_MESSAGE
    elif request.path == f'/user/{username}/password/change':
        # Request is a POST to change password
        if change_password_form.validate_on_submit():
            current_password = change_password_form.current_password.data
            new_password = change_password_form.new_password.data

            if current_password == new_password:
                change_password_error_message = PASSWORDS_EQUAL_MESSAGE
            else:
                try:
                    # Check the current password is valid for this user
                    auth.authenticate_user(repo, username, current_password)

                    auth.change_password(repo, user, new_password)
                    session['is_password_change_success'] = True
                    return redirect(url_for('user_bp.user', username=user.username))
                except AuthenticationException:
                    # Incorrect password
                    change_password_error_message = auth.INCORRECT_PASSWORD_MESSAGE
                except UnknownUserException:
                    # User isn't recognized at this point (unlikely)
                    abort(404)
    elif request.path == f'/user/{username}/delete':

        # Request is a POST to delete this account
        if delete_account_form.validate_on_submit():
            confirmation = delete_account_form.confirmation.data

            if confirmation != username:
                delete_account_error_message = CONFIRMATION_FAILED_MESSAGE
            else:
                auth.delete_user(repo, user)
                session.clear()
                return redirect(url_for('home_bp.home'))

    return render_template(
        'user/user.html',
        user=user,
        change_password_form=change_password_form,
        change_password_error_message=change_password_error_message,
        is_password_change_success=is_password_change_success,
        change_username_form=change_username_form,
        change_username_error_message=change_username_error_message,
        is_username_change_success=is_username_change_success,
        delete_account_form=delete_account_form,
        delete_account_error_message=delete_account_error_message
    )


@user_blueprint.route('/user/<string:username>/password/change', methods=['POST'])
@login_required
def change_password(username: str):
    return user(username)


@user_blueprint.route('/user/<string:username>/username/change', methods=['POST'])
@login_required
def change_username(username: str):
    return user(username)


@user_blueprint.route('/user/<string:username>/delete', methods=['POST'])
@login_required
def delete_account(username: str):
    return user(username)


class ChangeUsernameForm(FlaskForm):
    new_username = StringField('New username', [
        DataRequired(message=NEW_USERNAME_REQUIRED_MESSAGE),
        Length(min=3, message=auth.INVALID_USERNAME_LENGTH_MESSAGE)
    ])
    submit = SubmitField('Submit')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', [
        DataRequired(message=CURRENT_PASSWORD_REQUIRED_MESSAGE)
    ])
    new_password = PasswordField('New password', [
        DataRequired(message=NEW_PASSWORD_REQUIRED_MESSAGE),
        PasswordValid()])
    submit = SubmitField('Submit')


class DeleteAccountForm(FlaskForm):
    confirmation = StringField('Confirmation', [
        DataRequired(message=CONFIRMATION_REQUIRED_MESSAGE)
    ])
    submit = SubmitField('Submit')

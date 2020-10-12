from flask import Blueprint, render_template, current_app, request
from flask_wtf import FlaskForm
from werkzeug.exceptions import abort
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired

from movie.adapters.repository import instance as repo
from movie.auth import auth
from movie.auth.auth import UnknownUserException, PasswordValid, login_required, AuthenticationException

user_blueprint = Blueprint(
    'user_bp', __name__)


@user_blueprint.route('/user/<string:username>', methods=['GET'])
def user(username: str):
    user = None
    change_password_form = ChangePasswordForm()
    change_password_error_message = None
    is_password_change_success = False

    try:
        user = auth.get_user(repo, username)
    except UnknownUserException:
        # No user with the given username
        abort(404)

    current_app.logger.info('method = ' + request.method)
    current_app.logger.info('path = ' + request.path)

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

    return render_template(
        'user/user.html',
        user=user,
        change_password_form=change_password_form,
        change_password_error_message=change_password_error_message,
        is_password_change_success=is_password_change_success
    )


@user_blueprint.route('/user/<string:username>/password/change', methods=['POST'])
@login_required
def change_password(username: str):
    return user(username)


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', [
        DataRequired(message='Current password required.')
    ])
    new_password = PasswordField('New password', [
        DataRequired(message='New password required.'),
        PasswordValid()])
    submit = SubmitField('Submit')

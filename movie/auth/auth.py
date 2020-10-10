from flask import Blueprint, render_template, redirect, url_for, session, request

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from password_validator import PasswordValidator

from functools import wraps

import movie.auth.services as services
import movie.adapters.repository as repo

# Configure Blueprint.
auth_blueprint = Blueprint(
    'auth_bp', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    is_username_unique = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            services.add_user(form.username.data, form.password.data, repo.repo_instance)

            # All is well, redirect the user to the login page.
            return redirect(url_for('auth_bp.login'))
        except services.NameNotUniqueException:
            is_username_unique = 'Your username is already taken - please supply another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'auth/credentials.html',
        title='Register',
        form=form,
        username_error_message=is_username_unique,
        handler_url=url_for('auth_bp.register')
    )


@auth_blueprint.route('/signin', methods=['GET', 'POST'])
def signin():
    form = LoginForm()
    username_not_recognised = None
    password_does_not_match_username = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = services.get_user(form.username.data, repo.repo_instance)

            # Authenticate user.
            services.authenticate_user(user['username'], form.password.data, repo.repo_instance)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user['username']
            return redirect(url_for('home_bp.home'))

        except services.UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_not_recognised = 'Username not recognised - please supply another'

        except services.AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_does_not_match_username = 'Password does not match supplied username - please check and try again'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'auth/credentials.html',
        title='Login',
        username_error_message=username_not_recognised,
        password_error_message=password_does_not_match_username,
        form=form
    )


@auth_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home_bp.home'))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('auth_bp.login'))
        return view(**kwargs)

    return wrapped_view


class PasswordValid:
    def __init__(self, message=None):
        if not message:
            message = u'Your password must be at least 8 characters, and contain an upper case letter,\
            a lower case letter and a digit'
        self.message = message

    def __call__(self, form, field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().uppercase() \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class RegistrationForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message='Your username is required'),
        Length(min=3, message='Your username is too short')])
    password = PasswordField('Password', [
        DataRequired(message='Your password is required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Login')

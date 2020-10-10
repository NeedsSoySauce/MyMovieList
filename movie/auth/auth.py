from functools import wraps

from flask import Blueprint, render_template, redirect, url_for, session, request
from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

from movie.adapters.repository import instance as repo
from .services import *

# Configure Blueprint.
auth_blueprint = Blueprint(
    'auth_bp', __name__)


@auth_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    username_error_message = None

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to attempt to add the new user.
        try:
            add_user(repo, form.username.data, form.password.data)

            # All is well, redirect the user to the login page.
            session.clear()
            session['username'] = form.username.data
            return redirect(url_for('home_bp.home', success=True))
        except NameNotUniqueException:
            username_error_message = 'Username taken. Please supply another'

    # For a GET or a failed POST request, return the Registration Web page.
    return render_template(
        'auth/credentials.html',
        title='Register',
        form=form,
        username_error_message=username_error_message,
        handler_url=url_for('auth_bp.register'),
        is_register_form=True
    )


@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username_error_message = None
    password_error_message = None
    is_register_success = bool(request.args.get('success'))

    if form.validate_on_submit():
        # Successful POST, i.e. the username and password have passed validation checking.
        # Use the service layer to lookup the user.
        try:
            user = get_user(repo, form.username.data)

            # Authenticate user.
            authenticate_user(repo, user.user_name, form.password.data)

            # Initialise session and redirect the user to the home page.
            session.clear()
            session['username'] = user.user_name
            return redirect(url_for('home_bp.home'))

        except UnknownUserException:
            # Username not known to the system, set a suitable error message.
            username_error_message = 'Unrecognized username - please check and try again.'

        except AuthenticationException:
            # Authentication failed, set a suitable error message.
            password_error_message = 'Incorrect password - please check and try again.'

    # For a GET or a failed POST, return the Login Web page.
    return render_template(
        'auth/credentials.html',
        title='Log in',
        username_error_message=username_error_message,
        password_error_message=password_error_message,
        is_register_success=is_register_success,
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
            message = u'Your password must be at least 8 characters, contain an upper case letter,\
            a lower case letter, and a digit'
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
        DataRequired(message='Username required'),
        Length(min=3, message='Usernames must be at least 3 characters')])
    password = PasswordField('Password', [
        DataRequired(message='Password required'),
        PasswordValid()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired()])
    password = PasswordField('Password', [
        DataRequired()])
    submit = SubmitField('Log in')

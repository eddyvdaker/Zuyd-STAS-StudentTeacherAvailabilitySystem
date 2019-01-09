"""
    app.login.forms
    ===============
    Forms used to login
"""

from wtforms import BooleanField, PasswordField, StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, EqualTo


class LoginForm(FlaskForm):
    """Form for logging in"""
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Request Password Reset')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'Current Password', validators=[DataRequired()])
    new_password = PasswordField(
        'New Password', validators=[DataRequired()])
    new_password_2 = PasswordField(
        'Retype New Password',
        validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Change Password')
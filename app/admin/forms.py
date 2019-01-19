"""
    app.admin.forms
    ===============
    Forms used within the admin panel
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import ValidationError, DataRequired, EqualTo
from app.models import User, Location


class RegistrationForm(FlaskForm):
    """Form for user registration"""
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField(u'Role', choices=[('admin', 'admin'),
                                        ('teacher', 'teacher'),
                                        ('student', 'student')])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LocationForm(FlaskForm):
    """Form for adding a new location"""
    name = StringField('Name', validators=[DataRequired()])
    building = SelectField('Location',
                           choices=[('Nieuw Eyckholt', 'Nieuw Eyckholt'),
                                    ('Brightlands SSC', 'Brightlands SSC'),
                                    ('Other', 'Other')])
    submit = SubmitField('Add')

    def validate_locationname(self, name):
        location = Location.query.filter_by(Name=name.data).first()
        if location is not None:
            raise ValidationError('Please use a different location name.')

"""
    app.checkin.forms
    ===============
    Forms used for adding checkins
"""

from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, SelectField


class CheckinForm(FlaskForm):
    """Form for adding a checkin when scanning qr"""
    availability = BooleanField('Beschikbaar?')
    submit = SubmitField('Add')


class AddCheckinForm(FlaskForm):
    """Form for adding a checkin"""
    location = SelectField('Location')
    availability = BooleanField('Beschikbaar?')
    submit = SubmitField('Add')

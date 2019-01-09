"""
    app.checkin.forms
    ===============
    Forms used for adding checkins
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class CheckinForm(FlaskForm):
    """Form for adding a checkin"""
    email = StringField('Email', validators=[DataRequired()])
    availability = BooleanField('Beschikbaar?')
    submit = SubmitField('Add')
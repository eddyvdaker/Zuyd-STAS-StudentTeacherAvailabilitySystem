from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired
from app.models import Checkin


class CheckinForm(FlaskForm):
    id = StringField('ID-nummer', validators=[DataRequired()])
    availability = BooleanField('Beschikbaar?', validators=[DataRequired()])
    submit = SubmitField('Add')
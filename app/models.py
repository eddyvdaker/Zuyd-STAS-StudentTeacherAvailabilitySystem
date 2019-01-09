"""
    app.models
    ===============
    Models used to store data in the database
"""

from app import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from flask import current_app
from time import time
from datetime import datetime


class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128), index=True)
    checkins = db.relationship('Checkin', backref='User', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'. format(self.email)


    def set_password(self, password):
        """Hash password and save it to db"""
        self.password_hash = generate_password_hash(password)



    def check_password(self, password):
        """Hash password and check if it's the same as the hash in db"""
        return check_password_hash(self.password_hash, password)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                      current_app.config['SECRET_KEY'],
                      algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config['SECRET_KEY'],
                algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


class Location(UserMixin, db.Model):
    """Location model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    building = db.Column(db.String(128), index=True, unique=True)
    checkins = db.relationship('Checkin', backref='Location', lazy='dynamic')

    def __repr__(self):
        return '<Location {}>'. format(self.name)


class Checkin(UserMixin, db.Model):
    """Checkin model"""
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    availability = db.Column(db.Boolean, default=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Checkin {}>'. format(self.availability)

    def set_time(self):
        """Set the current_time"""
        return datetime.utcnow()


@login_manager.user_loader
def load_user(id):
    """Specifiy model used for login"""
    return User.query.get(int(id))

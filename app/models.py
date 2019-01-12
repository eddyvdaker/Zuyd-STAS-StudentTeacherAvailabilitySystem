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
from secrets import token_urlsafe


class User(UserMixin, db.Model):
    """User model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(128), index=True)
    checkins = db.relationship('Checkin', backref='User', lazy='dynamic')
    keys = db.relationship('Key', backref='User', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'. format(self.email)

    def to_dict(self, is_self=False, incl_checkins=False):
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role
        }
        if is_self:
            data['keys'] = [k.to_dict() for k in self.keys.all()]
        if incl_checkins:
            data['checkins'] = [c.to_dict(incl_location=True) for c in
                                self.checkins.all()]
        return data

    def generate_key(self, description=None):
        key = Key(
            key=token_urlsafe(),
            User=self
        )
        if description:
            key.description = description
        db.session.add(key)
        db.session.commit()
        return key.to_dict()

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


class Location(db.Model):
    """Location model"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    building = db.Column(db.String(128), index=True)
    checkins = db.relationship('Checkin', backref='Location', lazy='dynamic')

    def __repr__(self):
        return '<Location {}>'. format(self.name)

    def to_dict(self, incl_checkins=False):
        data = {
            'id': self.id,
            'name': self.name,
            'building': self.building,
        }
        if incl_checkins:
            data['checkins'] = [c.to_dict(incl_user=True) for c in
                                self.checkins.all()]
        return data


class Checkin(db.Model):
    """Checkin model"""
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    availability = db.Column(db.Boolean, default=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Checkin {}>'. format(self.availability)

    def to_dict(self, incl_user=False, incl_location=False):
        data = {
            'id': self.id,
            'time': self.time,
            'availability': self.availability
        }
        if incl_user:
            data['user'] = self.User.to_dict()
        if incl_location:
            data['location'] = self.Location.to_dict()
        return data

    def set_time(self):
        """Set the current_time"""
        return datetime.utcnow()


class Key(db.Model):
    """Api keys"""
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(254), index=True, unique=True)
    description = db.Column(db.String(254), default="No description")
    created_on = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def to_dict(self):
        return {
            'key': self.key,
            'description': self.description,
            'created_on': self.created_on,
            'user': self.User.email
        }


@login_manager.user_loader
def load_user(id):
    """Specifiy model used for login"""
    return User.query.get(int(id))

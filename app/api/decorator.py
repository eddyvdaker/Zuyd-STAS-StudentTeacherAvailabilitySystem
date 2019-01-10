from flask import request
from functools import wraps
from app.errors.api import unauthorized
from app.models import Key


def api_login_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        auth = request.headers.get('Authorization')
        if not auth:
            return unauthorized('missing authorization header')
        key_str = auth.replace('Bearer ', '')
        key = Key.query.filter_by(key=key_str).first()
        if not key:
            return unauthorized('invalid key')
        return func(*args, **kw)
    return wrapper

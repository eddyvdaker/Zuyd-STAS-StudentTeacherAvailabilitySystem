from flask import Blueprint

bp = Blueprint('availability', __name__)

from app.availability import routes
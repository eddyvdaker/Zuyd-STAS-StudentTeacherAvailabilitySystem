from flask import jsonify, request
from app.errors.api import bad_request, unauthorized
from app.models import User, Key, Location
from app.api import bp
from app.api.decorator import api_login_required


@bp.route('/api/v1.0/request_key', methods=['POST'])
def request_key():
    if not request.is_json:
        return bad_request('json payload expected')

    data = request.get_json()
    if not {'email', 'password'}.issubset(data.keys()):
        return bad_request('payload must include email and password fields')

    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        return jsonify(user.generate_key())
    else:
        return unauthorized('wrong emailadress or password')


@bp.route('/api/v1.0/users/<int:user_id>')
@api_login_required
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    key_str = request.headers.get('Authorization').replace('Bearer ', '')
    key = Key.query.filter_by(key=key_str).first()
    is_user = key in user.keys.all()
    return jsonify(user.to_dict(is_self=is_user, incl_checkins=True))


@bp.route('/api/v1.0/locations/<int:location_id>')
@api_login_required
def get_location(location_id):
    location = Location.query.filter_by(id=location_id).first_or_404()
    return jsonify(location.to_dict(incl_checkins=True))
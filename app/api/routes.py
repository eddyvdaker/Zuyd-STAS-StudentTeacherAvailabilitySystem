from flask import jsonify, request
from app.errors.api import bad_request, unauthorized
from app.models import User, Key
from app.api import bp


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

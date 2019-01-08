from flask_login import login_required
from app.models import User
from app.availability import bp
from flask import render_template


@bp.route('/availability/user_list', methods=['GET'])
@login_required
def user_list():
    users = User.query.all()
    return render_template(
        'availability/user_list.html', title='User list', users=users)


@bp.route('/availability/user/<user_id>', methods=['GET'])
@login_required
def user_availability(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template(
        'availability/user_availability.html', user=user,
        title='Availability'
    )
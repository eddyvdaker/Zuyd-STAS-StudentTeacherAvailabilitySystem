"""
    app.availability.routes
    ===============
    Routes used for checking availability
"""

from flask_login import login_required
from app.models import User, Checkin, Location
from app.availability import bp
from flask import render_template


@bp.route('/availability/user_list', methods=['GET'])
@login_required
def user_list():
    """Overview of all registered users"""
    users = User.query.order_by(User.name).all()
    return render_template(
        'availability/user_list.html', title='User list', users=users)


@bp.route('/availability/user/<user_id>', methods=['GET'])
@login_required
def user_availability(user_id):
    """Availability and location overview of a selected user"""
    user = User.query.filter_by(id=user_id).first()
    checkins = Checkin.query.filter_by(user_id=user_id)
    checkin = checkins[-1]
    location = Location.query.filter_by(id=checkin.location_id).first()
    availability = checkin.availability
    if availability:
        availability="Available"
    else:
        availability="Not available"
    return render_template(
        'availability/user_availability.html', user=user,
        location=location, availability=availability, title='Availability'
    )


@bp.route('/availability/location_list', methods=['GET'])
@login_required
def location_list():
    """Overview of all registered locations"""
    locations = Location.query.order_by(Location.name).all()
    return render_template(
        'availability/location_list.html', title='Location list',
        locations=locations)


@bp.route('/availability/location/<location_id>', methods=['GET'])
@login_required
def location_availability(location_id):
    """Availability overview of a specific location"""
    location = Location.query.filter_by(id=location_id).first()
    present = []

    for user in User.query.all():
        last_checkin = user.checkins.all()[-1]
        if last_checkin in location.checkins.all():
            present.append(last_checkin)
    present_nr = len(present)

    return render_template(
        'availability/location_availability.html', location=location,
        present_nr=present_nr, present=present, title='Availability')
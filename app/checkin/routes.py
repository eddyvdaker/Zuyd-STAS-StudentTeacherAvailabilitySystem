"""
    app.checkin.routes
    ===============
    Routes used for adding checkins
"""

from app import db
from app.checkin import bp
from app.checkin.forms import CheckinForm, AddCheckinForm
from app.models import Checkin, Location
from flask import flash, redirect, url_for, render_template
from datetime import datetime
from flask_login import login_required, current_user


@bp.route('/checkin/location/<location_id>', methods=['GET', 'POST'])
@login_required
def new_checkin(location_id):
    """Add new checkin when scanning qr"""
    form=CheckinForm()
    if form.validate_on_submit():
        checkin = Checkin(user_id=current_user.id,
                          availability=form.availability.data,
                          time = datetime.utcnow(),
                          location_id = location_id)
        db.session.add(checkin)
        db.session.commit()
        flash('You are now checked in.')
        return redirect(url_for('main.index'))
    return render_template('checkin/new_checkin.html', title='new checkin'
                           , form=form)


@bp.route('/checkin/add_checkin', methods=['GET', 'POST'])
@login_required
def add_checkin():
    """Add new checkin"""
    form=AddCheckinForm()
    form.location.choices = [(str(l.id), l.name) for l in Location.query.all()]
    if form.validate_on_submit():
        checkin = Checkin(user_id=current_user.id,
                          availability=form.availability.data,
                          time=datetime.utcnow(),
                          location_id=form.location.data)
        db.session.add(checkin)
        db.session.commit()
        flash('De gegevens zijn gewijzigd.')
        return redirect(url_for('main.index'))
    return render_template('checkin/add_checkin.html', title='add checkin',
                           form=form)

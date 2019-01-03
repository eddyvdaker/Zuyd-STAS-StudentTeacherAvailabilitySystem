from app import db
from app.checkin import bp
from app.checkin.forms import CheckinForm
from app.models import Checkin, Location, User
from flask import flash, redirect, url_for, render_template
from datetime import datetime
from flask_login import login_required


@bp.route('/checkin/location/<location_id>', methods=['GET', 'POST'])
@login_required
def new_checkin(location_id):
    form=CheckinForm()
    if form.validate_on_submit():
        user_id = User.query.filter_by(email=form.email.data).first().id
        checkin = Checkin(user_id=user_id,
                          availability=form.availability.data,
                          time = datetime.utcnow(),
                          location_id = location_id)
        db.session.add(checkin)
        db.session.commit()
        flash('You are now checked in.')
        return redirect(url_for('main.index'))
    return render_template('checkin/new_checkin.html', title='new checkin', form=form)
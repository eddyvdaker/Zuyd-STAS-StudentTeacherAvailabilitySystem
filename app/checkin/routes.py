from app import db
from app.checkin import bp
from app.checkin.forms import CheckinForm
from app.models import Checkin
from flask import flash, redirect, url_for, render_template
from datetime import datetime


@bp.route('/checkin/new_checkin', methods=['GET', 'POST'])
def new_checkin():
    form=CheckinForm()
    if form.validate_on_submit():
        checkin = Checkin(user_id=form.id.data,
                          availability=form.availability.data,
                          time = datetime.utcnow())
        db.session.add(checkin)
        db.session.commit()
        flash('You are now checked in.')
        return redirect(url_for('main.index'))
    return render_template('checkin/new_checkin.html', title='new checkin', form=form)
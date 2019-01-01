from app import db
from app.admin.forms import RegistrationForm, LocationForm, GenerateForm
from app.models import User, Location
from app.admin import bp
from app.admin.decorator import admin_required
from flask import flash, redirect, url_for, render_template
from flask_login import login_required
import pyqrcode
import os


@bp.route('/admin/users_overview', methods=['GET'])
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template(
        'admin/users_overview.html', title='Users overview', users=users)


@bp.route('/admin/user/<user_id>', methods=['GET'])
@login_required
@admin_required
def user_overview(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template(
        'admin/user_overview.html', user=user,
        title='Admin Panel: User ' + str(user_id)
    )


@bp.route('/admin/register', methods=['GET', 'POST'])
@login_required
@admin_required
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, role=form.role.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('The new user has been added.')
        return redirect(url_for('admin.users'))
    return render_template('admin/register.html', title='Register', form=form)


@bp.route('/admin/locations_overview', methods=['GET'])
@login_required
@admin_required
def locations():
    locations = Location.query.all()
    return render_template(
        'admin/locations_overview.html', title='Locations overview', locations=locations)


@bp.route('/admin/add_location', methods=['GET', 'POST'])
@login_required
@admin_required
def add_location():
    form=LocationForm()
    if form.validate_on_submit():
        location = Location(name=form.name.data, building=form.building.data)
        db.session.add(location)
        db.session.commit()

        qr_info = form.name.data
        qr = pyqrcode.create(qr_info)
        qr.svg("app/qr_codes/" + qr_info + ".svg", scale=6)

        flash('The new location has been added.')
        return redirect(url_for('admin.locations'))
    return render_template('admin/add_location.html', title='add_location', form=form)


@bp.route('/admin/generate_qr', methods=['GET', 'POST'])
@login_required
@admin_required
def generate_qr():
    form=GenerateForm()
    if form.validate_on_submit():
        flash('The QR-code has been generated.')
        return redirect(url_for('main.index'))
    return render_template(
        'admin/generate_qr.html', title='Generate QR-code', form=form)
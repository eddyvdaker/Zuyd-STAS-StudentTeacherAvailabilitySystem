from app import db
from app.admin.forms import RegistrationForm
from app.models import User
from app.login import bp
from flask import flash, redirect, url_for, render_template
from flask_login import login_required


@bp.route('/admin/users_overview', methods=['GET'])
@login_required
def users():
    users = User.query.all()
    return render_template(
        'admin/users_overview.html', title='Users overview', users=users)


@bp.route('/admin/register', methods=['GET', 'POST'])
@login_required
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('The new user has been added.')
        return redirect(url_for('login.register'))
    return render_template('admin/register.html', title='Register', form=form)
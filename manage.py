import coverage
import unittest

from flask.cli import FlaskGroup

from app import create_app, db
from app.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=['*.db', 'templates/*'])
COV.start()


@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def seed_db():
    password = input("Set admin password: ")
    admin = User(email="admin@mail.com", name="admin", role="admin")
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()


@cli.command()
def test():
    tests = unittest.TestLoader().discover('tests', pattern='authentication*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccesful():
        return 0
    return 1


@cli.command()
def cov():
    tests = unittest.TestLoader().discover('tests', pattern='authentication*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccesful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


if __name__ == '__main__':
    cli()
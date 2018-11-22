import coverage
import unittest

from flask.cli import FlaskGroup


from app import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)

COV = coverage.coverage(
    branch=True,
    include='app/*',
    omit=['*.db', 'templates/*'])
COV.start()


@cli.command()
def recreate_db():
    # Recreate DB code here
    pass


@cli.command()
def seed_db():
    # Seed DB code here
    pass


@cli.command()
def test():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccesful():
        return 0
    return 1


@cli.command()
def cov():
    tests = unittest.TestLoader().discover('tests', pattern='test*.py')
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
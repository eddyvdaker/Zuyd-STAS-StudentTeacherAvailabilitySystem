from flask import render_template

from app.errors import bp


@bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('error.html', title='404 - File not Found'), 404
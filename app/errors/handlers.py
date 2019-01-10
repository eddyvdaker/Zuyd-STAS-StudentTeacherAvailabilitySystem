from flask import render_template, request

from app import db
from app.errors import bp
from app.errors.api import error_response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
           request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return error_response(404)
    return render_template('error.html', title='404 - File not Found'), 404


@bp.app_errorhandler(500)
def internal_server_error(error):
    db.session.rollback()
    if wants_json_response():
        return error_response(500)
    return render_template('error.html', title='500 - Internal Server Error'),\
           500
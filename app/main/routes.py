"""
    app.main.routes
    ===============
    Routes used for the homepage
"""

from flask import render_template

from app.main import bp


@bp.route('/')
def index():
    """Indexpage/Homepage"""
    return render_template('index.html', title='Home')
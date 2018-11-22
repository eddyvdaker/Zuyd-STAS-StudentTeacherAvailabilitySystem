import logging
import os
from flask import Flask
from logging.handlers import RotatingFileHandler

from config import Config

def create_app(app_settings=Config):
    app = Flask(__name__)
    app.config.from_object(app_settings)

    # Initialize Extensions

    # Register Blueprints
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Logging
    if not app.debug and not app.config['TESTING']:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log',
                                           maxBytes=app.config['MAX_LOG_SIZE'],
                                           backupCount=app.config['MAX_LOGS'])

        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('App Startup')

    return app

from app import models
from flask_testing import TestCase

from app import create_app
from config import Config


class TestConfig(Config):
    TESTING = True


    app = create_app(app_settings=TestConfig)


    class BaseTestCase(TestCase):
        def create_app(self):
            return app

        def setUp(self):
            pass

        def tearDown(self):
            pass
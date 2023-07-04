# assist/server/tests/test_config.py


import unittest

from flask import current_app
from flask_testing import TestCase

from assist.server import app


class TestDevelopmentConfig(TestCase):
    def create_app(self):
        app.config.from_object('assist.server.config.DevelopmentConfig')
        return app

    def test_app_is_development(self):
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'mysql+mysqldb://root:root@localhost:3306/assist'
        )


class TestTestingConfig(TestCase):
    def create_app(self):
        app.config.from_object('assist.server.config.TestingConfig')
        return app

    def test_app_is_testing(self):
        self.assertTrue(app.config['DEBUG'])
        


class TestProductionConfig(TestCase):
    def create_app(self):
        app.config.from_object('assist.server.config.ProductionConfig')
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)


if __name__ == '__main__':
    unittest.main()

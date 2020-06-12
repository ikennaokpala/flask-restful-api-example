import os
import unittest

from flask import current_app
from flask_testing import TestCase

from manage import app
from app.main.environment import environments

class TestDevelopmentEnvironment(TestCase):
    def create_app(self):
        app.config.from_object(environments['development'])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'lsarp')
        self.assertTrue(app.config['DEBUG'] is True)
        self.assertFalse(current_app is None)
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://postgres:postgres@localhost:5432/lsarp_development'
        )

class TestTestingEnvironment(TestCase):
    def create_app(self):
        app.config.from_object(environments['test'])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['SECRET_KEY'] is 'lsarp')
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(
            app.config['SQLALCHEMY_DATABASE_URI'] == 'postgres://postgres:postgres@localhost:5432/lsarp_test'
        )

class TestProductionEnvironment(TestCase):
    def create_app(self):
        app.config.from_object(environments['production'])
        return app

    def test_app_is_production(self):
        self.assertTrue(app.config['DEBUG'] is False)

if __name__ == '__main__':
    unittest.main()

import os
import time
import click

from flask import Flask, current_app
from click.testing import CliRunner
from unittest.mock import patch

from app.main.config.tasks.db import create, seed, drop
from app.tests.base_test_case import BaseTestCase

database_uri = 'postgresql://postgres:postgres@localhost:5432/dummy_db'


@patch.dict(os.environ, {'FLASK_APP': 'manage'})
@patch.dict(os.environ, {'FLASK_ENV': 'test'})
@patch.dict(current_app.config, {'SQLALCHEMY_DATABASE_URI': database_uri})
class TestCommands(BaseTestCase):
    def setUp(self):
        super(TestCommands, self).setUp()
        self.app = Flask(__name__)

    def test_db_create_when_database_is_available(self):
        with self.app.app_context():
            with patch(
                'app.main.config.tasks.db.database_exists',
                return_value=True,
            ) as mocked_database_exists:
                with patch(
                    'app.main.config.tasks.db.drop_database',
                    return_value=None,
                ) as mocked_drop_database:
                    with patch(
                        'app.main.config.tasks.db.create_database',
                        return_value=None,
                    ) as mocked_create_database:
                        result = CliRunner().invoke(create, [])

                        assert '' == result.output
                        assert not result.exception

                        mocked_create_database.assert_not_called()
                        mocked_drop_database.assert_called_once()
                        mocked_database_exists.assert_called()

    def test_db_create_when_database_is_not_available(self):
        with self.app.app_context():
            with patch(
                'app.main.config.tasks.db.database_exists',
                return_value=False,
            ) as mocked_database_exists:
                with patch(
                    'app.main.config.tasks.db.drop_database',
                    return_value=None,
                ) as mocked_drop_database:
                    with patch(
                        'app.main.config.tasks.db.create_database',
                        return_value=None,
                    ) as mocked_create_database:
                        result = CliRunner().invoke(create, [])

                        assert '' == result.output
                        assert not result.exception

                        mocked_create_database.assert_called_once()
                        mocked_drop_database.assert_not_called()
                        mocked_database_exists.assert_called()

    def test_db_seed_when_database_is_not_available(self):
        with self.app.app_context():
            with patch(
                'app.main.config.tasks.db.database_exists',
                return_value=False,
            ) as mocked_database_exists:
                result = CliRunner().invoke(seed, [])

                assert 'Something went wrong\n' == result.output
                assert not result.exception

                mocked_database_exists.assert_called_once()

    def test_db_seed_when_database_is_available(self):
        with self.app.app_context():
            with patch(
                'app.main.config.tasks.db.database_exists',
                return_value=True,
            ) as mocked_database_exists:
                result = CliRunner().invoke(seed, [])

                assert '' == result.output
                assert not result.exception

                mocked_database_exists.assert_called_once()

    @patch.dict(current_app.config, {'SQLALCHEMY_DATABASE_URI': database_uri})
    def test_db_drop(self):
        with self.app.app_context():
            with patch(
                'app.main.config.tasks.db.drop_database',
                return_value=None,
            ) as mocked_drop_database:
                result = CliRunner().invoke(drop, [])

                assert '' == result.output
                assert not result.exception

                mocked_drop_database.assert_called_once()

import os
import re
import unittest

from flask import Flask, current_app
from flask_testing import TestCase
from unittest.mock import patch

from manage import app
from src.main.environment import environments

database_uri = 'postgresql://postgres:postgres@localhost:5432/lsarp_production'


class TestDevelopmentEnvironment(TestCase):
    def create_app(self):
        current_app.config.from_object(environments['development'])
        return app

    def test_app_is_development(self):
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['SECRET_KEY'] == 'lsarp')
        self.assertTrue(app.config['DEBUG'] == True)
        self.assertListEqual(app.config['LSARP_API_CORS_CLIENTS'], ['*'])
        self.assertFalse(current_app == None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'], str)
        self.assertTrue(
            re.match(
                r'(postgres|postgresql)://postgres:postgres@.*/lsarp_development',
                app.config['SQLALCHEMY_DATABASE_URI'],
            )
        )
        self.assertEqual(app.config['MZXML_FILES_KEY_PREFIX'], 'mzxml_file_')
        self.assertEqual(app.config['MZXML_FILES_UPLOAD_FOLDER'], '/tmp/')
        self.assertEqual(
            app.config['PROTOTYPE_FILES_UPLOAD_FOLDER'], '/tmp/prototypes/'
        )
        self.assertEqual(
            app.config['DATA_FORMAT_FILE_EXTENSIONS'],
            'mzXML,mzML,mzData,xlsx,csv,raw,BAF,DAT,FID,YEP,WIFF,XMS'.split(','),
        )
        self.assertEqual(app.config['SEED_DATA_COUNT'], 100)
        self.assertEqual(app.config['PAGINATION_MAX_PER_PAGE'], 100)
        self.assertEqual(
            app.config['METADATA_SHIPMENTS_FILE_COLUMNS'],
            'DATE shipped,MATRIX_BOX,MATRIX_LOCN,ORGM,ISOLATE_NBR'.split(','),
        )
        self.assertEqual(
            app.config['TEST_DATA_COLLABORATORS'],
            'dev@westgrid.ca,ikenna.okpala@computecanada.ca,patrick.mann@computecanada.ca,swacker@ucalgary.ca,snoskov@ucalgary.ca,ian.lewis2@ucalgary.ca,ian.percel@ucalgary.ca,fridman@ucalgary.ca'.split(
                ','
            ),
        )


class TestTestingEnvironment(TestCase):
    def create_app(self):
        app.config.from_object(environments['test'])
        return app

    def test_app_is_testing(self):
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['SECRET_KEY'] == 'lsarp')
        self.assertTrue(app.config['DEBUG'])
        self.assertListEqual(app.config['LSARP_API_CORS_CLIENTS'], ['*'])
        self.assertIsInstance(app.config['SQLALCHEMY_DATABASE_URI'], str)
        self.assertTrue(
            re.match(
                r'(postgres|postgresql)://postgres:postgres@.*/lsarp_test',
                app.config['SQLALCHEMY_DATABASE_URI'],
            )
        )
        self.assertEqual(app.config['MZXML_FILES_KEY_PREFIX'], 'mzxml_file_')
        self.assertEqual(app.config['MZXML_FILES_UPLOAD_FOLDER'], '/tmp/')
        self.assertEqual(
            app.config['PROTOTYPE_FILES_UPLOAD_FOLDER'], '/tmp/prototypes/'
        )
        self.assertEqual(
            app.config['DATA_FORMAT_FILE_EXTENSIONS'],
            'mzXML,mzML,mzData,xlsx,csv,raw,BAF,DAT,FID,YEP,WIFF,XMS'.split(','),
        )
        self.assertEqual(app.config['SEED_DATA_COUNT'], 100)
        self.assertEqual(app.config['PAGINATION_MAX_PER_PAGE'], 100)
        self.assertEqual(
            app.config['METADATA_SHIPMENTS_FILE_COLUMNS'],
            'DATE shipped,MATRIX_BOX,MATRIX_LOCN,ORGM,ISOLATE_NBR'.split(','),
        )
        self.assertEqual(
            app.config['TEST_DATA_COLLABORATORS'],
            'dev@westgrid.ca,ikenna.okpala@computecanada.ca,patrick.mann@computecanada.ca,swacker@ucalgary.ca,snoskov@ucalgary.ca,ian.lewis2@ucalgary.ca,ian.percel@ucalgary.ca,fridman@ucalgary.ca'.split(
                ','
            ),
        )


class TestProductionEnvironment(TestCase):
    def create_app(self):
        app.config.from_object(environments['production'])
        return app

    def test_app_is_production(self):
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertTrue(app.config['DEBUG'] == False)
        self.assertTrue(type(app.config['LSARP_API_CORS_CLIENTS']) == list)
        for index in range(len(app.config['LSARP_API_CORS_CLIENTS'])):
            self.assertTrue(type(app.config['LSARP_API_CORS_CLIENTS'][index]) == str)

        self.assertEqual(app.config['MZXML_FILES_KEY_PREFIX'], 'mzxml_file_')
        self.assertEqual(app.config['MZXML_FILES_UPLOAD_FOLDER'], '/tmp/')
        self.assertEqual(
            app.config['PROTOTYPE_FILES_UPLOAD_FOLDER'], '/tmp/prototypes/'
        )
        self.assertEqual(
            app.config['DATA_FORMAT_FILE_EXTENSIONS'],
            'mzXML,mzML,mzData,xlsx,csv,raw,BAF,DAT,FID,YEP,WIFF,XMS'.split(','),
        )
        self.assertEqual(app.config['PAGINATION_MAX_PER_PAGE'], 100)
        self.assertEqual(
            app.config['METADATA_SHIPMENTS_FILE_COLUMNS'],
            'DATE shipped,MATRIX_BOX,MATRIX_LOCN,ORGM,ISOLATE_NBR'.split(','),
        )
        self.assertEqual(app.config['TEST_DATA_COLLABORATORS'], [])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'], str)
        self.assertTrue(
            re.match(
                r'(postgres|postgresql)://postgres:postgres@.*/lsarp_production',
                app.config['SQLALCHEMY_DATABASE_URI'],
            )
        )

    @patch.dict(os.environ, {'LSARP_DATABASE_URL': database_uri})
    def test_app_is_production_and_database_uri_is_supplied(self):
        with self.app.app_context():
            self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'], str)
            self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], database_uri)


if __name__ == '__main__':
    unittest.main()

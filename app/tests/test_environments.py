import os
import re
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
        self.assertFalse(app.config['PRESERVE_CONTEXT_ON_EXCEPTION'])
        self.assertFalse(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
        self.assertFalse(app.config['SECRET_KEY'] == 'lsarp')
        self.assertTrue(app.config['DEBUG'] == True)
        self.assertListEqual(app.config['ALLOWED_CORS_CLIENTS'], ['*'])
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
        self.assertListEqual(app.config['ALLOWED_CORS_CLIENTS'], ['*'])
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
        self.assertTrue(type(app.config['ALLOWED_CORS_CLIENTS']) == list)
        for index in range(len(app.config['ALLOWED_CORS_CLIENTS'])):
            self.assertTrue(type(app.config['ALLOWED_CORS_CLIENTS'][index]) == str)

        self.assertEqual(app.config['MZXML_FILES_KEY_PREFIX'], 'mzxml_file_')
        self.assertEqual(app.config['MZXML_FILES_UPLOAD_FOLDER'], '/tmp/')
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


if __name__ == '__main__':
    unittest.main()

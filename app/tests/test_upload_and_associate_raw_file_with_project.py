import os
import re
import shutil
import unittest
import json
import factory
from freezegun import freeze_time

from werkzeug.datastructures import FileStorage

from flask import current_app

from app.tests.base_test_case import BaseTestCase
from app.main.models.project import Project
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import ProjectFactory

class TestUploadAndAssociateWithProject(BaseTestCase):
    def setUp(self):
        super(TestUploadAndAssociateWithProject, self).setUp()
        self.current_session = SessionFactory.create()
        self.project = ProjectFactory.create()
        self.email = self.current_session.tokenized_user['email']
        self.headers = { 'Authorization': 'Bearer ' + self.current_session.access_token }
        self.raw_file_path = os.path.abspath('app/tests/support/fixtures/raw_files/sample.mzXML')
        self.raw_file_full_name = os.path.basename(self.raw_file_path)
        self.raw_file_full_name_ext = self.raw_file_full_name.split('.')
        self.raw_file_name = self.raw_file_full_name_ext[0]
        self.raw_file_ext = self.raw_file_full_name_ext[1]
        self.raw_file_stores = [FileStorage(
            stream=open(self.raw_file_path, 'rb'),
            filename='sample.mzXML',
            content_type='text/xml',
        ), FileStorage(
            stream=open(self.raw_file_path, 'rb'),
            filename='another_sample.mzXML',
            content_type='text/xml',
        )]
        self.params = { 'raw_file_0': self.raw_file_stores[0] }
        self.destination = os.path.join(current_app.config['RAW_FILES_UPLOAD_FOLDER'], 'projects', self.project.slug)

    def tearDown(self):
        super(TestUploadAndAssociateWithProject, self).tearDown()
        shutil.rmtree(os.path.join(current_app.config['RAW_FILES_UPLOAD_FOLDER'], 'projects'), ignore_errors=True)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_with_project_slug_and_multiple_raw_file_are_valid(self):
        params = {'raw_file_0': self.raw_file_stores[0],
                  'raw_file_1': self.raw_file_stores[1]}
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/' + self.project.slug + '/raw_files', headers=self.headers, data=params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcomes = json.loads(response.data.decode())
            for index in range(len(outcomes)):
                outcome = outcomes[index]
                raw_file = params['raw_file_' + str(index)]
                raw_file_destination = self.destination + '/' + outcome['checksum'] + '_' + raw_file.filename

                self.assertTrue(outcome['raw_file_id'] == index + 1)
                self.assertTrue(outcome['path'] == raw_file_destination)
                self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome['checksum']))
                self.assertTrue(outcome['slug'] == self.project.slug)
                self.assertTrue(os.path.exists(raw_file_destination))

                project = Project.query.filter_by(slug=outcome['slug']).first()
                outcome = project.raw_files[index]

                self.assertTrue(outcome.location == raw_file_destination)
                self.assertTrue(outcome.extension == self.raw_file_ext)
                self.assertTrue(outcome.name == raw_file.filename.split('.')[0])
                self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome.checksum))
                self.assertTrue(outcome.project.id == project.id)
                self.assertTrue(outcome.project_id == project.id)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_with_project_slug_and_raw_file_are_valid(self):
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/' + self.project.slug + '/raw_files', headers=self.headers, data=self.params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())[0]
            raw_file_destination = self.destination + '/' + outcome['checksum'] + '_' + self.raw_file_full_name

            self.assertTrue(outcome['raw_file_id'] == 1)
            self.assertTrue(outcome['path'] == raw_file_destination)
            self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome['checksum']))
            self.assertTrue(outcome['slug'] == self.project.slug)
            self.assertTrue(os.path.exists(raw_file_destination))

            project = Project.query.filter_by(slug=outcome['slug']).first()
            outcome = project.raw_files[0]

            self.assertTrue(outcome.location == raw_file_destination)
            self.assertTrue(outcome.extension == self.raw_file_ext)
            self.assertTrue(outcome.name == self.raw_file_name)
            self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome.checksum))
            self.assertTrue(outcome.project.id == project.id)
            self.assertTrue(outcome.project_id == project.id)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_raw_file_is_not_expected(self):
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/' + self.project.slug + '/raw_file', headers=self.headers, data={ 'fake_raw_file': None }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_raw_file_has_no_name(self):
        raw_file_store =  FileStorage(
                stream=open(self.raw_file_path, 'rb'),
                filename='',
                content_type='text/xml',
            )
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/' + self.project.slug + '/raw_file', headers=self.headers, data={ 'raw_file_0': raw_file_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_raw_file_extension_is_not_mzXML(self):
        raw_file_store =  FileStorage(
                stream=open(self.raw_file_path, 'rb'),
                filename='sample.not_mzXML',
                content_type='text/xml',
            )
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/' + self.project.slug + '/raw_file', headers=self.headers, data={ 'raw_file_0': raw_file_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 422)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_none_existing_project_slug(self):
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/none-existing-project/raw_file', headers=self.headers, data=self.params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] != '')
            self.assertFalse(os.path.exists(self.destination))

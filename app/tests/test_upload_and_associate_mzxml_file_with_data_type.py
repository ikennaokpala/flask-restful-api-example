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
from app.main.models.data_type import DataType
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import ProjectFactory

class TestUploadAndAssociateWithDataType(BaseTestCase):
    def setUp(self):
        super(TestUploadAndAssociateWithDataType, self).setUp()
        self.current_session = SessionFactory.create()
        self.project = ProjectFactory.create(data_types=1)
        self.data_type = self.project.data_types[0]
        self.request_path = '/v1/projects/{0.slug}/data_types/{0.data_types[0].slug}/mzxml_files'.format(self.project)
        self.email = self.current_session.tokenized_user['email']
        self.headers = { 'Authorization': 'Bearer ' + self.current_session.access_token }
        self.mzxml_file_path = os.path.abspath('app/tests/support/fixtures/mzxml_files/sample.mzXML')
        self.mzxml_file_full_name = os.path.basename(self.mzxml_file_path)
        self.mzxml_file_full_name_ext = self.mzxml_file_full_name.split('.')
        self.mzxml_file_name = self.mzxml_file_full_name_ext[0]
        self.mzxml_file_ext = self.mzxml_file_full_name_ext[1]
        self.mzxml_file_stores = [FileStorage(
            stream=open(self.mzxml_file_path, 'rb'),
            filename='sample.mzXML',
            content_type='text/xml',
        ), FileStorage(
            stream=open(self.mzxml_file_path, 'rb'),
            filename='another_sample.mzXML',
            content_type='text/xml',
        )]
        self.params = { 'mzxml_file_0': self.mzxml_file_stores[0] }
        self.destination = os.path.join(current_app.config['MZXML_FILES_UPLOAD_FOLDER'], 'projects', self.project.slug, 'data_types', self.data_type.slug)

    def tearDown(self):
        super(TestUploadAndAssociateWithDataType, self).tearDown()
        shutil.rmtree(os.path.join(current_app.config['MZXML_FILES_UPLOAD_FOLDER'], 'projects'), ignore_errors=True)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_with_data_type_slug_and_multiple_mzxml_file_are_valid(self):
        params = {'mzxml_file_0': self.mzxml_file_stores[0], 'mzxml_file_1': self.mzxml_file_stores[1]}
        with self.client as rdbclient:
            response = rdbclient.put(self.request_path, headers=self.headers, data=params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcomes = json.loads(response.data.decode())
            for index in range(len(outcomes)):
                outcome = outcomes[index]
                mzxml_file = params['mzxml_file_' + str(index)]
                mzxml_file_destination = self.destination + '/' + outcome['checksum'] + '_' + mzxml_file.filename

                self.assertTrue(outcome['id'] == index + 1)
                self.assertTrue(outcome['name'] == [self.mzxml_file_name, 'another_sample'][index])
                self.assertTrue(outcome['extension'] == self.mzxml_file_ext)
                self.assertTrue(outcome['path'] == mzxml_file_destination)
                self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome['checksum']))
                self.assertTrue(outcome['project_slug'] == self.project.slug)
                self.assertTrue(outcome['data_type_slug'] == self.data_type.slug)
                self.assertTrue(os.path.exists(mzxml_file_destination))

                data_type = DataType.query.filter_by(slug=outcome['data_type_slug']).first()
                outcome = data_type.mzxml_files[index]

                self.assertTrue(outcome.location == mzxml_file_destination)
                self.assertTrue(outcome.extension == self.mzxml_file_ext)
                self.assertTrue(outcome.name == mzxml_file.filename.split('.')[0])
                self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome.checksum))
                self.assertTrue(outcome.data_type.id == data_type.id)
                self.assertTrue(outcome.data_type_id == data_type.id)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_with_data_type_slug_and_mzxml_file_are_valid(self):
        with self.client as rdbclient:
            response = rdbclient.put(self.request_path, headers=self.headers, data=self.params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())[0]
            mzxml_file_destination = self.destination + '/' + outcome['checksum'] + '_' + self.mzxml_file_full_name

            self.assertTrue(outcome['id'] == 1)
            self.assertTrue(outcome['name'] == self.mzxml_file_name)
            self.assertTrue(outcome['extension'] == self.mzxml_file_ext)
            self.assertTrue(outcome['path'] == mzxml_file_destination)
            self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome['checksum']))
            self.assertTrue(outcome['project_slug'] == self.project.slug)
            self.assertTrue(outcome['data_type_slug'] == self.data_type.slug)
            self.assertTrue(os.path.exists(mzxml_file_destination))

            data_type = DataType.query.filter_by(slug=outcome['data_type_slug']).first()
            outcome = data_type.mzxml_files[0]

            self.assertTrue(outcome.location == mzxml_file_destination)
            self.assertTrue(outcome.extension == self.mzxml_file_ext)
            self.assertTrue(outcome.name == self.mzxml_file_name)
            self.assertTrue(re.match(r'^[a-f0-9]{32}$', outcome.checksum))
            self.assertTrue(outcome.data_type.id == data_type.id)
            self.assertTrue(outcome.data_type_id == data_type.id)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_mzxml_file_is_not_expected(self):
        with self.client as rdbclient:
            response = rdbclient.put(self.request_path, headers=self.headers, data={ 'fake_mzxml_file': None }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_mzxml_file_has_no_name(self):
        mzxml_file_store =  FileStorage(
                stream=open(self.mzxml_file_path, 'rb'),
                filename='',
                content_type='text/xml',
            )
        with self.client as rdbclient:
            response = rdbclient.put(self.request_path, headers=self.headers, data={ 'mzxml_file_0': mzxml_file_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_mzxml_file_extension_is_not_mzXML(self):
        mzxml_file_store =  FileStorage(
                stream=open(self.mzxml_file_path, 'rb'),
                filename='sample.not_mzXML',
                content_type='text/xml',
            )
        with self.client as rdbclient:
            response = rdbclient.put(self.request_path, headers=self.headers, data={ 'mzxml_file_0': mzxml_file_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 422)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_none_existing_data_type_slug(self):
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/'+ self.project.slug +'/data_types/none-existing-data_type/mzxml_file', headers=self.headers, data=self.params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] != '')
            self.assertFalse(os.path.exists(self.destination))

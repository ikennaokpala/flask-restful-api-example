import os
import re
import shutil
import unittest
import json
import factory


from app.main import db
from flask import current_app
from unittest.mock import patch
from freezegun import freeze_time
from werkzeug.datastructures import FileStorage

from app.tests.base_test_case import BaseTestCase
from app.main.models.project import Project
from app.main.models.metadata_shipment_file import MetadataShipmentFile
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import DataTypeWithProjectFactory

class TestUploadMetadataShipmentFileAndAssociateWithDataType(BaseTestCase):
    def setUp(self):
        super(TestUploadMetadataShipmentFileAndAssociateWithDataType, self).setUp()
        self.current_session = SessionFactory.create()
        self.data_type = DataTypeWithProjectFactory.create()
        self.project = self.data_type.project
        self.test_request_path = '/v1/projects/' + self.project.slug + '/data_types/' + str(self.data_type.slug) + '/metadata_shipments'
        self.email = self.current_session.tokenized_user['email']
        self.headers = { 'Authorization': 'Bearer ' + self.current_session.access_token }
        self.metadata_shipment_path = os.path.abspath('app/tests/support/fixtures/metadata_shipments/sample_lsarp_metadata_shipment.xlsx')
        self.metadata_shipment_full_name = os.path.basename(self.metadata_shipment_path)
        self.metadata_shipment_full_name_ext = self.metadata_shipment_full_name.split('.')
        self.metadata_shipment_name = self.metadata_shipment_full_name_ext[0]
        self.metadata_shipment_ext = self.metadata_shipment_full_name_ext[1]
        self.metadata_shipment_content = { 'columns': current_app.config.get('METADATA_SHIPMENTS_FILE_COLUMNS'), 'rows': {'2019-05-07 00:00:00': [{'LSARP_SA009': [['A,1', 'SA', 'QC01'], ['D,6', 'MRSA', 'QC02'], ['A,2', 'SA', 'BI_16_3052'], ['A,3', 'SA', 'BI_16_3054'], ['A,4', 'SA', 'BI_16_3055'], ['A,5', 'SA', 'BI_16_3060']], 'LSARP_SA010': [['A,1', 'SA', 'QC01'], ['D,6', 'MRSA', 'QC02'], ['A,2', 'SA', 'BI_16_3490'], ['A,3', 'SA', 'BI_16_3499'], ['A,4', 'SA', 'BI_16_3503'], ['A,5', 'SA', 'BI_16_3520'], ['A,6', 'SA2', 'BI_16_3532'], ['A,7', 'SA', 'BI_16_3555'], ['A,8', 'SA', 'BI_16_3558'], ['A,9', 'MRSA', 'BI_17_0002'], ['A,10', 'SA', 'BI_17_0004'], ['B,1', 'SA', 'BI_17_0006']], 'LSARP_SA011': [['A,1', 'SA', 'SA_QC01'], ['D,6', 'MRSA', 'SA_QC02'], ['A,2', 'SA', 'BI_17_0470'], ['A,3', 'SA', 'BI_17_0482'], ['A,4', 'MRSA', 'BI_17_0487'], ['A,5', 'SA', 'BI_17_0499'], ['A,6', 'MRSA', 'BI_17_0508'], ['A,7', 'SA', 'BI_17_0511'], ['A,8', 'SA', 'BI_17_0512'], ['A,9', 'SA', 'BI_17_0513'], ['A,10', 'MRSA', 'BI_17_0516'], ['H,10', 'SA', 'BI_17_0918']], 'LSARP_SA012': [['A,1', 'SA', 'SA_QC01'], ['D,6', 'MRSA', 'SA_QC02'], ['A,2', 'SA', 'BI_17_0919'], ['A,3', 'SA', 'BI_17_0926'], ['A,4', 'SA', 'BI_17_0937'], ['A,5', 'SA', 'BI_17_0938'], ['A,6', 'MRSA', 'BI_17_0942'], ['A,7', 'MRSA', 'BI_17_0950'], ['A,8', 'SA', 'BI_17_0973'], ['A,9', 'SA', 'BI_17_0979'], ['A,10', 'SA', 'BI_17_0980'], ['B,1', 'SA', 'BI_17_0982']]}]}}
        self.metadata_shipment_stores = [FileStorage(
            stream=open(self.metadata_shipment_path, 'rb'),
            filename='sample_lsarp_metadata_shipment.xlsx',
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        ), FileStorage(
            stream=open(self.metadata_shipment_path, 'rb'),
            filename='sample_lsarp_metadata_shipment.xlsx',
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )]
        self.params = { 'metadata_shipment_0': self.metadata_shipment_stores[0] }
        self.destination = ''

    def tearDown(self):
        super(TestUploadMetadataShipmentFileAndAssociateWithDataType, self).tearDown()

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_with_data_type_slug_and_multiple_metadata_shipment_are_valid(self):
        params = {'metadata_shipment_0': self.metadata_shipment_stores[0], 'metadata_shipment_1': self.metadata_shipment_stores[1]}
        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data=params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcomes = json.loads(response.data.decode())

            for index in range(len(outcomes)):
                outcome = outcomes[index]

                self.assertEqual(outcome['data_type_slug'], self.data_type.slug)
                self.assertEqual(outcome['extension'], self.metadata_shipment_ext)
                self.assertEqual(outcome['name'], self.metadata_shipment_name)
                self.assertDictEqual(outcome['content'], self.metadata_shipment_content)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_with_data_type_slug_and_metadata_shipment_are_valid(self):
        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data=self.params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())[0]

            self.assertEqual(outcome['data_type_slug'], self.data_type.slug)
            self.assertEqual(outcome['extension'], self.metadata_shipment_ext)
            self.assertEqual(outcome['name'], self.metadata_shipment_name)
            self.assertDictEqual(outcome['content'], self.metadata_shipment_content)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_metadata_shipment_is_not_expected(self):
        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data={ 'fake_metadata_shipment': None }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_metadata_shipment_has_no_name(self):
        metadata_shipment_store =  FileStorage(
                stream=open(self.metadata_shipment_path, 'rb'),
                filename='',
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data={ 'metadata_shipment_0': metadata_shipment_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_metadata_shipment_extension_is_not_xlsx(self):
        metadata_shipment_store =  FileStorage(
                stream=open(self.metadata_shipment_path, 'rb'),
                filename='sample.not_xlsx',
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )
        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data={ 'metadata_shipment_0': metadata_shipment_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 422)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'DATA_FORMAT_FILE_EXTENSIONS': ['some_other_valid_data_format']})
    def test_when_user_access_token_is_valid_and_metadata_shipment_extension_is_not_xlsx(self):
        metadata_shipment_store =  FileStorage(
                stream=open(self.metadata_shipment_path, 'rb'),
                filename='sample.not_xlsx',
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

        self.data_type.data_formats = ['some_other_valid_data_format']

        db.session.flush()
        db.session.commit()

        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data={ 'metadata_shipment_0': metadata_shipment_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 422)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_metadata_shipment_file_with_wrong_column_names(self):
        metadata_shipment_path = os.path.abspath('app/tests/support/fixtures/metadata_shipments/sample_lsarp_metadata_shipment_wrong_columns.xlsx')
        metadata_shipment_store =  FileStorage(
                stream=open(metadata_shipment_path, 'rb'),
                filename='sample_lsarp_metadata_shipment_wrong_columns.xlsx',
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data={ 'metadata_shipment_0': metadata_shipment_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 422)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')
            self.assertFalse(os.path.exists(self.destination))

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_metadata_shipment_extension_is_defined_in_data_type_data_formats(self):
        metadata_shipment_store =  FileStorage(
                stream=open(self.metadata_shipment_path, 'rb'),
                filename='sample.some_other_valid_data_format',
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            )

        self.data_type.data_formats = ['some_other_valid_data_format']

        db.session.flush()
        db.session.commit()

        with self.client as rdbclient:
            response = rdbclient.put(self.test_request_path, headers=self.headers, data={ 'metadata_shipment_0': metadata_shipment_store }, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())[0]

            self.assertEqual(outcome['data_type_slug'], self.data_type.slug)
            self.assertEqual(outcome['extension'], 'some_other_valid_data_format')
            self.assertEqual(outcome['name'], 'sample')
            self.assertDictEqual(outcome['content'], self.metadata_shipment_content)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_none_existing_data_type(self):
        with self.client as rdbclient:
            response = rdbclient.put('/v1/projects/'+ self.project.slug +'/data_types/none-existing-data-type-slug/metadata_shipment', headers=self.headers, data=self.params, content_type='multipart/form-data')

            self.assertEqual(response.status_code, 404)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] != '')
            self.assertFalse(os.path.exists(self.destination))

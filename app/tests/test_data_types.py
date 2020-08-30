import re
import json
import factory
import unittest
import dataclasses

from app.main import db

from freezegun import freeze_time
from unittest.mock import patch
from flask import current_app

from app.main.models.project import Project
from app.main.models.data_type import DataType
from app.tests.base_test_case import BaseTestCase
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import ProjectFactory
from app.tests.support.factories import DataTypeWithProjectFactory


class TestDataTypeBase(BaseTestCase):
    def setUp(self):
        super(TestDataTypeBase, self).setUp()
        self.project = ProjectFactory.create(data_types=3)
        self.data_types = self.project.data_types
        self.project_path = '/v1/projects/' + self.project.slug
        self.current_session = SessionFactory.create()
        self.data_formats = ['mzXML', 'xlsx', 'csv']
        self.description = 'A particular kind of data item, as defined by the file formats (mzXML, xlsx) and values it can take in.'
        self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}
        self.params = {
            'name': 'Metabolomics DataType',
            'description': self.description,
            'data_formats': self.data_formats,
        }
        self.expected = {'slug': 'metabolomics-datatype-factory-3'}
        self.expected.update(self.params)
        self.data_formats.sort()


class TestCreateDataType(TestDataTypeBase):
    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_a_params_are_exempted(self):
        with self.client as rdbclient:
            response = rdbclient.post(
                self.project_path + '/data_types', headers=self.headers, json={}
            )

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(
                outcome['message'],
                'The browser (or proxy) sent a request that this server could not understand.',
            )

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_description_is_exempted(self):
        with self.client as rdbclient:
            params = self.params.copy()
            params.pop('description')
            response = rdbclient.post(
                self.project_path + '/data_types', headers=self.headers, json=params
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.expected.update({'description': None})
            self.assertTrue(
                re.match(r'^metabolomics-datatype-[a-f0-9]{8}$', outcome['slug'])
            )

            results = DataType.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertEqual(outcome.name, self.params['name'])
            self.assertTrue(
                re.match(r'^metabolomics-datatype-[a-f0-9]{8}$', outcome.slug)
            )
            self.assertEqual(outcome.project.slug, self.project.slug)
            self.assertEqual(outcome.description, None)
            self.assertEqual(outcome.data_formats, self.params['data_formats'])
            self.assertEqual(results.count(), 1)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_name_is_exempted(self):
        with self.client as rdbclient:
            params = self.params.copy()
            params.pop('name')
            response = rdbclient.post(
                self.project_path + '/data_types', headers=self.headers, json=params
            )

            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertEqual(
                outcome['message'],
                'The browser (or proxy) sent a request that this server could not understand.',
            )

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_data_formats_are_exempted(self):
        with self.client as rdbclient:
            params = self.params.copy()
            params.pop('data_formats')
            response = rdbclient.post(
                self.project_path + '/data_types', headers=self.headers, json=params
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(
                re.match(r'^metabolomics-datatype-[a-f0-9]{8}$', outcome['slug'])
            )

            results = DataType.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertEqual(outcome.name, self.params['name'])
            self.assertTrue(
                re.match(r'^metabolomics-datatype-[a-f0-9]{8}$', outcome.slug)
            )
            self.assertEqual(outcome.project.slug, self.project.slug)
            self.assertEqual(outcome.description, self.params['description'])
            self.assertEqual(outcome.data_formats, self.params['data_formats'])
            self.assertEqual(results.count(), 1)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_and_some_invalid_data_formats_are_sent(
        self,
    ):
        with self.client as rdbclient:
            params = {
                'name': 'Updated name',
                'description': 'Updated description',
                'data_formats': ['invalid_data_format', 'mzXML'],
            }
            response = rdbclient.post(
                self.project_path + '/data_types', headers=self.headers, json=params
            )
            params.update({'slug': 'updated-name', 'data_formats': ['mzXML']})
            self.expected.update(params)

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome['slug']))

            results = DataType.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertEqual(outcome.name, self.expected['name'])
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome.slug))
            self.assertEqual(outcome.project.slug, self.project.slug)
            self.assertEqual(outcome.description, self.expected['description'])
            self.assertEqual(outcome.data_formats, self.expected['data_formats'])
            self.assertEqual(results.count(), 1)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_user_access_token_is_valid_with_params_provided(self):
        with self.client as rdbclient:
            response = rdbclient.post(
                self.project_path + '/data_types/',
                headers=self.headers,
                json=self.params,
            )

            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(
                re.match(r'^metabolomics-datatype-[a-f0-9]{8}$', outcome['slug'])
            )

            results = DataType.query.filter_by(slug=outcome['slug'])
            outcome = results.first()
            self.assertEqual(outcome.name, self.params['name'])
            self.assertTrue(
                re.match(r'^metabolomics-datatype-[a-f0-9]{8}$', outcome.slug)
            )
            self.assertEqual(outcome.project.slug, self.project.slug)
            self.assertEqual(outcome.description, self.params['description'])
            self.assertEqual(outcome.data_formats, self.params['data_formats'])
            self.assertEqual(results.count(), 1)


class TestDataTypes(TestDataTypeBase):
    def setUp(self):
        super(TestDataTypes, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_all_data_types_without_page_and_per_page_and_direction(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                self.project_path + '/data_types', headers=self.headers
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 3)

            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_1_and_per_page_with_direction_desc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                self.project_path
                + '/data_types/'
                + '?page=1&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 3)
            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_1_and_per_page_with_direction_asc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                self.project_path + '/data_types' + '?page=1&per_page=2&direction=asc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 3)
            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_2_nd_per_page_with_direction_desc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                self.project_path
                + '/data_types/'
                + '?page=2&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 2)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 3)
            self.assertEqual(len(data_types), 1)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_2_and_per_page_with_direction_asc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                self.project_path + '/data_types' + '?page=2&per_page=2&direction=asc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 2)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 3)
            self.assertEqual(len(data_types), 1)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )


class TestDataTypesWithUser(TestDataTypeBase):
    def setUp(self):
        super(TestDataTypesWithUser, self).setUp()
        ProjectFactory.create(
            data_types=1,
            owner='another.email@test.com',
            collaborators=['none@none.com'],
        )
        ProjectFactory.create(
            data_types=1,
            owner='another.email@test.com',
            collaborators=['test@example.com'],
        )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_all_data_types_without_page_and_per_page_and_direction(self):

        with self.client as rdbclient:
            response = rdbclient.get('/v1/data_types', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 4)

            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_1_and_per_page_with_direction_desc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/data_types/' + '?page=1&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 4)
            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_1_and_per_page_with_direction_asc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/data_types' + '?page=1&per_page=2&direction=asc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 4)
            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_2_nd_per_page_with_direction_desc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/data_types/' + '?page=2&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 2)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 4)
            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_when_user_has_no_data_types(self):
        for project in Project.query.all():
            project.owner = 'not_current_user@example.com'
            project.collaborators = []

            db.session.flush()
            db.session.commit()

        with self.client as rdbclient:
            response = rdbclient.get('/v1/data_types', headers=self.headers,)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 1)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 0)
            self.assertEqual(len(data_types), 0)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_data_types_with_page_2_and_per_page_with_direction_asc(self):

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/data_types' + '?page=2&per_page=2&direction=asc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            data_types = outcome['data_types']

            self.assertEqual(outcome['page'], 2)
            self.assertEqual(outcome['per_page'], 2)
            self.assertEqual(outcome['total'], 4)
            self.assertEqual(len(data_types), 2)
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    data_types[0]['slug'],
                )
            )


class TestFetchADataType(TestDataTypeBase):
    def setUp(self):
        super(TestFetchADataType, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_a_data_type(self):
        data_type = DataTypeWithProjectFactory.create(mzxmls=1, metadata_shipments=1)
        project = data_type.project
        self.expected = dataclasses.asdict(data_type)

        with self.client as rdbclient:
            response = rdbclient.get(
                self.project_path + '/data_types/' + data_type.slug,
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertEqual(outcome, self.expected)


class TestUpdateADataType(TestDataTypeBase):
    def setUp(self):
        super(TestUpdateADataType, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_data_type(self):
        self.params = {
            'name': 'Updated name',
            'description': 'Updated description',
            'data_formats': ['mzXML'],
        }

        with self.client as rdbclient:
            response = rdbclient.put(
                self.project_path + '/data_types/' + self.data_types[0].slug,
                headers=self.headers,
                json=self.params,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome['slug']))

            outcome = DataType.query.filter_by(slug=outcome['slug']).first()

            self.assertEqual(outcome.name, self.params['name'])
            self.assertEqual(outcome.description, self.params['description'])
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome.slug))

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_data_type_when_name_has_not_changed(self):
        current_data_type = self.data_types[0]
        self.params = {
            'name': current_data_type.name,
            'description': 'Updated description',
            'data_formats': ['mzXML'],
        }

        with self.client as rdbclient:
            response = rdbclient.put(
                self.project_path + '/data_types/' + current_data_type.slug,
                headers=self.headers,
                json=self.params,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    outcome['slug'],
                )
            )

            outcome = DataType.query.filter_by(slug=outcome['slug']).first()

            self.assertEqual(outcome.name, current_data_type.name)
            self.assertEqual(outcome.description, self.params['description'])
            self.assertEqual(outcome.data_formats, self.params['data_formats'])
            self.assertTrue(
                re.match(
                    r'^metabolomics-datatype-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    outcome.slug,
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_data_type_some_invalid_data_formats_are_sent(self):
        self.params = {
            'name': 'Updated name',
            'description': 'Updated description',
            'data_formats': ['invalid_data_format', 'mzXML'],
        }

        with self.client as rdbclient:
            response = rdbclient.put(
                self.project_path + '/data_types/' + self.data_types[0].slug,
                headers=self.headers,
                json=self.params,
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome['slug']))

            outcome = DataType.query.filter_by(slug=outcome['slug']).first()

            self.assertEqual(outcome.name, self.params['name'])
            self.assertEqual(outcome.description, self.params['description'])
            self.assertEqual(outcome.data_formats, ['mzXML'])
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome.slug))


class TestDeleteADataType(TestDataTypeBase):
    def setUp(self):
        super(TestDeleteADataType, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_delete_a_data_type_without_chidren(self):
        slug = self.data_types[0].slug

        with self.client as rdbclient:
            response = rdbclient.delete(
                self.project_path + '/data_types/' + slug, headers=self.headers
            )

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')

            outcome = response.data.decode()
            self.assertEqual(outcome, '')

            outcome = DataType.query.filter_by(slug=slug).first()
            self.assertEqual(outcome, None)

    @freeze_time('2020-06-02 08:57:53')
    def test_delete_a_data_type_with_chidren(self):
        slug = DataTypeWithProjectFactory.create(mzxmls=1, metadata_shipments=1).slug

        with self.client as rdbclient:
            response = rdbclient.delete(
                self.project_path + '/data_types/' + slug, headers=self.headers
            )

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')

            outcome = response.data.decode()
            self.assertEqual(outcome, '')

            outcome = DataType.query.filter_by(slug=slug).first()
            self.assertEqual(outcome, None)

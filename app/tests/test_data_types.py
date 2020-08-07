import json
import factory
import unittest

from freezegun import freeze_time
from unittest.mock import patch
from flask import current_app

from app.main.models.data_type import DataType
from app.tests.base_test_case import BaseTestCase
from app.tests.support.factories import SessionFactory
from app.tests.support.factories import ProjectFactory


class TestDataTypeBase(BaseTestCase):
	def setUp(self):
		super(TestDataTypeBase, self).setUp()
		self.project = ProjectFactory.create(data_types=3)
		self.data_types = self.project.data_types
		self.project_path = '/v1/projects/' + self.project.slug
		self.current_session = SessionFactory.create()
		self.expected = {'slug': 'metabolomics-datatype-3'}
		self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}
		self.params = {'name': 'Metabolomics DataType', 'description': 'A particular kind of data item, as defined by the file formats (mzXML, xlsx) and values it can take in.'}

class TestCreateDataType(TestDataTypeBase):
	@freeze_time('2020-06-02 08:57:53')
	def test_when_user_access_token_is_valid_and_a_params_are_exempted(self):
		with self.client as rdbclient:
			response = rdbclient.post(self.project_path + '/data_types', headers=self.headers, json={})

			self.assertEqual(response.status_code, 400)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

	@freeze_time('2020-06-02 08:57:53')
	def test_when_user_access_token_is_valid_and_a_description_is_exempted(self):
		with self.client as rdbclient:
			response = rdbclient.post(self.project_path + '/data_types/', headers=self.headers, json={ 'name': 'Metabolomics DataType' })

			self.assertEqual(response.status_code, 201)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			self.assertTrue(outcome == self.expected)
			results = DataType.query.filter_by(slug=outcome['slug'])
			outcome = results.first()
			self.assertTrue(outcome.name == self.params['name'])
			self.assertTrue(outcome.slug == self.expected['slug'])
			self.assertTrue(outcome.project.slug == self.project.slug)
			self.assertTrue(outcome.description == None)
			self.assertTrue(results.count() == 1)

	@freeze_time('2020-06-02 08:57:53')
	def test_when_user_access_token_is_valid_and_a_name_are_exempted(self):
		with self.client as rdbclient:
			response = rdbclient.post(self.project_path + '/data_types', headers=self.headers, json={ 'description': '' })

			self.assertEqual(response.status_code, 400)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

	@freeze_time('2020-06-02 08:57:53')
	def test_when_user_access_token_is_valid_with_params_provided(self):
		with self.client as rdbclient:
			response = rdbclient.post(self.project_path + '/data_types/', headers=self.headers, json=self.params)

			self.assertEqual(response.status_code, 201)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			self.assertTrue(outcome == self.expected)

			results = DataType.query.filter_by(slug=outcome['slug'])
			outcome = results.first()
			self.assertTrue(outcome.name == self.params['name'])
			self.assertTrue(outcome.slug == self.expected['slug'])
			self.assertTrue(outcome.project.slug == self.project.slug)
			self.assertTrue(outcome.description == self.params['description'])
			self.assertTrue(results.count() == 1)

class TestDataTypes(TestDataTypeBase):
	def setUp(self):
		super(TestDataTypes, self).setUp()

	@freeze_time('2020-06-02 08:57:53')
	@patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
	def test_fetch_all_data_types_without_page_and_per_page_and_direction(self):

		with self.client as rdbclient:
			response = rdbclient.get(self.project_path + '/data_types', headers=self.headers)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			data_types = outcome['data_types']

			self.assertTrue(outcome['page'] == 1)
			self.assertTrue(outcome['per_page'] == 2)
			self.assertTrue(outcome['total'] == 3)

			self.assertTrue(len(data_types) == 2)
			self.assertEqual(data_types[0]['slug'], 'metabolomics-datatype-factory-2')

	@freeze_time('2020-06-02 08:57:53')
	@patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
	def test_fetch_data_types_with_page_1_and_per_page_with_direction_desc(self):

		with self.client as rdbclient:
			response = rdbclient.get(self.project_path + '/data_types/' + '?page=1&per_page=2&direction=desc', headers=self.headers)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			data_types = outcome['data_types']

			self.assertTrue(outcome['page'] == 1)
			self.assertTrue(outcome['per_page'] == 2)
			self.assertTrue(outcome['total'] == 3)
			self.assertTrue(len(data_types) == 2)
			self.assertEqual(data_types[0]['slug'], 'metabolomics-datatype-factory-2')

	@freeze_time('2020-06-02 08:57:53')
	@patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
	def test_fetch_data_types_with_page_1_and_per_page_with_direction_asc(self):

		with self.client as rdbclient:
			response = rdbclient.get(self.project_path + '/data_types' + '?page=1&per_page=2&direction=asc', headers=self.headers)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			data_types = outcome['data_types']

			self.assertTrue(outcome['page'] == 1)
			self.assertTrue(outcome['per_page'] == 2)
			self.assertTrue(outcome['total'] == 3)
			self.assertTrue(len(data_types) == 2)
			self.assertEqual(data_types[0]['slug'], 'metabolomics-datatype-factory')

	@freeze_time('2020-06-02 08:57:53')
	@patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
	def test_fetch_data_types_with_page_2_nd_per_page_with_direction_desc(self):

		with self.client as rdbclient:
			response = rdbclient.get(self.project_path + '/data_types/' + '?page=2&per_page=2&direction=desc', headers=self.headers)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			data_types = outcome['data_types']

			self.assertTrue(outcome['page'] == 2)
			self.assertTrue(outcome['per_page'] == 2)
			self.assertTrue(outcome['total'] == 3)
			self.assertTrue(len(data_types) == 1)
			self.assertEqual(data_types[0]['slug'], 'metabolomics-datatype-factory')

	@freeze_time('2020-06-02 08:57:53')
	@patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
	def test_fetch_data_types_with_page_2_and_per_page_with_direction_asc(self):

		with self.client as rdbclient:
			response = rdbclient.get(self.project_path + '/data_types' + '?page=2&per_page=2&direction=asc', headers=self.headers)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			data_types = outcome['data_types']

			self.assertTrue(outcome['page'] == 2)
			self.assertTrue(outcome['per_page'] == 2)
			self.assertTrue(outcome['total'] == 3)
			self.assertTrue(len(data_types) == 1)
			self.assertEqual(data_types[0]['slug'], 'metabolomics-datatype-factory-2')

class TestFetchADataType(TestDataTypeBase):
	def setUp(self):
		super(TestFetchADataType, self).setUp()

	@freeze_time('2020-06-02 08:57:53')
	def test_fetch_a_data_type(self):
		with self.client as rdbclient:
			response = rdbclient.get(self.project_path + '/data_types/' + self.data_types[0].slug, headers=self.headers)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			self.expected.update(self.params)
			self.expected.update({'name': self.data_types[0].name, 'slug': self.data_types[0].slug, 'project_id': self.project.id, 'mzxml_files': [] })
			outcome.pop('id')
			self.assertTrue(outcome == self.expected)

class TestUpdateADataType(TestDataTypeBase):
	def setUp(self):
		super(TestUpdateADataType, self).setUp()

	@freeze_time('2020-06-02 08:57:53')
	def test_update_a_data_type(self):
		self.params = { 'name': 'Updated name', 'description': 'Updated description' }

		with self.client as rdbclient:
			response = rdbclient.put(self.project_path + '/data_types/'+ self.data_types[0].slug, headers=self.headers, json=self.params)

			self.assertEqual(response.status_code, 200)
			self.assertTrue(response.content_type == 'application/json')

			outcome = json.loads(response.data.decode())
			self.assertTrue(outcome == { 'slug': 'updated-name' })

			outcome = DataType.query.filter_by(slug=outcome['slug']).first()

			self.assertTrue(outcome.name == self.params['name'])
			self.assertTrue(outcome.description == self.params['description'])

class TestDeleteADataType(TestDataTypeBase):
	def setUp(self):
		super(TestDeleteADataType, self).setUp()

	@freeze_time('2020-06-02 08:57:53')
	def test_delete_a_data_type(self):
		slug = self.data_types[0].slug

		with self.client as rdbclient:
			response = rdbclient.delete(self.project_path + '/data_types/' + slug, headers=self.headers)

			self.assertEqual(response.status_code, 204)
			self.assertTrue(response.content_type == 'application/json')

			outcome = response.data.decode()
			self.assertTrue(outcome == '')

			outcome = DataType.query.filter_by(slug=slug).first()
			self.assertTrue(outcome == None)

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
from app.tests.support.factories import DataTypeFactory


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

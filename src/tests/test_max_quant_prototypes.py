import os
import re
import json
import shutil
import factory
import unittest

from flask import current_app
from dataclasses import asdict
from unittest.mock import patch
from freezegun import freeze_time
from xml.dom.minidom import parseString
from werkzeug.datastructures import FileStorage

from src.tests.base_test_case import BaseTestCase
from src.tests.support.factories import SessionFactory
from src.tests.support.factories import MaxQuantFactory

from src.main.models.prototypes.max_quant import MaxQuant


class TestMaxQuantPrototypeBase(BaseTestCase):
    def setUp(self):
        super(TestMaxQuantPrototypeBase, self).setUp()
        self.max_quant = MaxQuantFactory.create()
        self.current_session = SessionFactory.create()
        self.destination = current_app.config['PROTOTYPE_FILES_UPLOAD_FOLDER']
        self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}
        self.max_quant_file_path = os.path.abspath(
            'src/tests/support/fixtures/max_quants/sample.xml'
        )
        self.fasta_file_path = os.path.abspath(
            'src/tests/support/fixtures/fasta_files/sample.fasta'
        )
        self.max_quant_file_store = FileStorage(
            stream=open(self.max_quant_file_path, 'rb'),
            filename='sample.xml',
            content_type='application/xml',
        )
        self.max_quant_file_content = (
            open(self.max_quant_file_path, 'rb').read().decode('utf-8')
        )
        self.fasta_file_store = FileStorage(
            stream=open(self.fasta_file_path, 'rb'),
            filename='sample.fasta',
            content_type='text/x-fasta',
        )
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

    def tearDown(self):
        super(TestMaxQuantPrototypeBase, self).tearDown()
        shutil.rmtree(
            self.destination, ignore_errors=True,
        )


class TestCreateMaxQuantPipelinePrototype(TestMaxQuantPrototypeBase):
    @freeze_time('2020-06-02 08:57:53')
    def test_when_all_params_are_supplied(self):
        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 201)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            fasta_file_destination = os.path.join(
                self.destination,
                'max_quants',
                outcome['slug'],
                outcome['content']['fasta_file']['checksum']
                + '_'
                + self.fasta_file_store.filename,
            )

            self.assertTrue(outcome['name'] == self.params['name'])
            self.assertTrue(outcome['type'] == 'MaxQuant')
            self.assertTrue(outcome['description'] == self.params['description'])
            self.assertTrue(
                re.match(
                    r'^[a-f0-9]{32}$', outcome['content']['fasta_file']['checksum']
                )
            )
            self.assertTrue(
                outcome['content']['fasta_file']['name']
                == self.max_quant_file_store.filename.split('.')[0]
            )
            self.assertTrue(
                outcome['content']['fasta_file']['extension']
                == self.fasta_file_store.filename.split('.')[-1]
            )
            self.assertTrue(os.path.exists(fasta_file_destination))
            self.assertTrue(outcome['content']['max_quant_file']['content'] != '')
            self.assertEqual(
                parseString(outcome['content']['max_quant_file']['content']).toxml(),
                parseString(self.max_quant_file_content).toxml(),
            )
            self.assertTrue(
                outcome['content']['max_quant_file']['name']
                == self.max_quant_file_store.filename.split('.')[0]
            )
            self.assertTrue(
                outcome['content']['max_quant_file']['extension']
                == self.max_quant_file_store.filename.split('.')[-1]
            )
            self.assertTrue(
                re.match(r'^max-quant-prototype-1-[a-f0-9]{8}$', outcome['slug'])
            )

    @freeze_time('2020-06-02 08:57:53')
    def test_when_name_is_sent_empty(self):
        self.params = {
            'name': '',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_name_is_missing(self):
        self.params = {
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_fasta_file_is_missing(self):
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_max_quant_file_is_missing(self):
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': self.fasta_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_fasta_filename_is_missing(self):
        fasta_file_store = FileStorage(
            stream=open(self.fasta_file_path, 'rb'),
            filename='',
            content_type='text/x-fasta',
        )
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_max_quant_filename_is_missing(self):
        max_quant_file_store = FileStorage(
            stream=open(self.max_quant_file_path, 'rb'),
            filename='',
            content_type='application/xml',
        )
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 400)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_fasta_file_extension_is_not_valid(self):
        fasta_file_store = FileStorage(
            stream=open(self.fasta_file_path, 'rb'),
            filename='sample.not_fasta',
            content_type='text/x-fasta',
        )
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 422)

    @freeze_time('2020-06-02 08:57:53')
    def test_when_max_quant_file_extension_is_not_valid(self):
        max_quant_file_store = FileStorage(
            stream=open(self.max_quant_file_path, 'rb'),
            filename='sample.not_xml',
            content_type='application/xml',
        )
        self.params = {
            'name': 'Max Quant Prototype 1',
            'description': 'Very good MaxQuant prototype based description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.post(
                '/v1/prototypes/max_quants',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 422)


class TestUpdateAMaxQuantPrototype(TestMaxQuantPrototypeBase):
    def setUp(self):
        super(TestUpdateAMaxQuantPrototype, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_max_quant_prototype(self):
        self.params = {
            'name': 'Updated Name',
            'description': 'Updated description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.put(
                '/v1/prototypes/max_quants/' + self.max_quant.slug,
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            fasta_file_destination = os.path.join(
                self.destination,
                'max_quants',
                outcome['slug'],
                outcome['content']['fasta_file']['checksum']
                + '_'
                + self.fasta_file_store.filename,
            )
            self.assertTrue(re.match(r'^updated-name-[a-f0-9]{8}$', outcome['slug']))

            self.assertEqual(outcome['name'], self.params['name'])
            self.assertEqual(outcome['description'], self.params['description'])
            self.assertEqual(outcome['type'], 'MaxQuant')
            self.assertTrue(
                re.match(
                    r'^[a-f0-9]{32}$', outcome['content']['fasta_file']['checksum']
                )
            )
            self.assertTrue(
                outcome['content']['fasta_file']['name']
                == self.max_quant_file_store.filename.split('.')[0]
            )
            self.assertTrue(
                outcome['content']['fasta_file']['extension']
                == self.fasta_file_store.filename.split('.')[-1]
            )
            self.assertTrue(os.path.exists(fasta_file_destination))
            self.assertTrue(outcome['content']['max_quant_file']['content'] != '')
            self.assertEqual(
                parseString(outcome['content']['max_quant_file']['content']).toxml(),
                parseString(self.max_quant_file_content).toxml(),
            )
            self.assertTrue(
                outcome['content']['max_quant_file']['name']
                == self.max_quant_file_store.filename.split('.')[0]
            )
            self.assertTrue(
                outcome['content']['max_quant_file']['extension']
                == self.max_quant_file_store.filename.split('.')[-1]
            )

    @freeze_time('2020-06-02 08:57:53')
    def test_update_a_max_quant_when_not_found(self):
        self.params = {
            'name': 'Updated Name',
            'description': 'Updated description',
            'fasta_file': self.fasta_file_store,
            'max_quant_file': self.max_quant_file_store,
        }

        with self.client as rdbclient:
            response = rdbclient.put(
                '/v1/prototypes/max_quants/none-existing-max-quant',
                headers=self.headers,
                data=self.params,
                content_type='multipart/form-data',
            )

            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] != '')


class TestFetchAMaxQuantPrototype(TestMaxQuantPrototypeBase):
    def setUp(self):
        super(TestFetchAMaxQuantPrototype, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_a_max_quant(self):
        self.expected = asdict(self.max_quant)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/max_quants/' + self.max_quant.slug, headers=self.headers
            )

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertEqual(outcome, self.expected)


class TestDeleteAMaxQuantPrototype(TestMaxQuantPrototypeBase):
    def setUp(self):
        super(TestDeleteAMaxQuantPrototype, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    def test_delete_a_max_quant(self):
        slug = self.max_quant.slug

        with self.client as rdbclient:
            response = rdbclient.delete(
                '/v1/prototypes/max_quants/' + slug, headers=self.headers
            )

            self.assertEqual(response.status_code, 204)
            self.assertEqual(response.content_type, 'application/json')

            outcome = response.data.decode()
            self.assertEqual(outcome, '')

            outcome = MaxQuant.query.filter_by(slug=slug).first()
            self.assertEqual(outcome, None)


class TestMaxQuantPrototypes(TestMaxQuantPrototypeBase):
    def setUp(self):
        super(TestMaxQuantPrototypes, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_all_max_quants_without_page_and_per_page_and_direction(self):
        self.max_quants = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get('/v1/prototypes/max_quants', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            max_quants = outcome['prototypes']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)

            self.assertTrue(len(max_quants) == 2)
            self.assertTrue(max_quants[0]['slug'] == self.max_quants[1].slug)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_max_quants_with_page_1_and_per_page_with_direction_desc(self):
        self.max_quants = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/max_quants?page=1&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            max_quants = outcome['prototypes']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(max_quants) == 2)
            self.assertTrue(max_quants[0]['slug'] == self.max_quants[1].slug)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_max_quants_with_page_1_and_per_page_with_direction_asc(self):
        self.max_quants = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/max_quants?page=1&per_page=2&direction=asc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            max_quants = outcome['prototypes']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(max_quants) == 2)
            self.assertTrue(
                re.match(
                    r'^meta-maxquant-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    max_quants[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_max_quants_with_page_2_nd_per_page_with_direction_desc(self):
        self.max_quants = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/max_quants?page=2&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            max_quants = outcome['prototypes']

            self.assertTrue(outcome['page'] == 2)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(max_quants) == 1)
            self.assertTrue(
                re.match(
                    r'^meta-maxquant-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    max_quants[0]['slug'],
                )
            )

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_max_quants_with_page_2_and_per_page_with_direction_asc(self):
        self.max_quants = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/max_quants?page=2&per_page=2&direction=asc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            max_quants = outcome['prototypes']

            self.assertTrue(outcome['page'] == 2)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(max_quants) == 1)
            self.assertTrue(max_quants[0]['slug'] == self.max_quants[1].slug)


if __name__ == '__main__':
    unittest.main()

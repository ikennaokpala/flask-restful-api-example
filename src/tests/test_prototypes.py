import re
import json

from flask import current_app
from unittest.mock import patch
from freezegun import freeze_time

from src.tests.base_test_case import BaseTestCase
from src.tests.support.factories import SessionFactory
from src.tests.support.factories import MaxQuantFactory


class TestPrototypeBase(BaseTestCase):
    def setUp(self):
        super(TestPrototypeBase, self).setUp()
        self.prototype = MaxQuantFactory.create()
        self.current_session = SessionFactory.create()
        self.destination = current_app.config['PROTOTYPE_FILES_UPLOAD_FOLDER']
        self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}

    def tearDown(self):
        super(TestPrototypeBase, self).tearDown()


class TestPrototypes(TestPrototypeBase):
    def setUp(self):
        super(TestPrototypes, self).setUp()

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_all_prototypes_without_page_and_per_page_and_direction(self):
        self.prototypes = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get('/v1/prototypes', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            prototypes = outcome['prototypes']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)

            self.assertTrue(len(prototypes) == 2)
            self.assertTrue(prototypes[0]['slug'] == self.prototypes[1].slug)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_prototypes_with_page_1_and_per_page_with_direction_desc(self):
        self.prototypes = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/?page=1&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            prototypes = outcome['prototypes']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(prototypes) == 2)
            self.assertTrue(prototypes[0]['slug'] == self.prototypes[1].slug)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_prototypes_with_page_1_and_per_page_with_direction_asc(self):
        self.prototypes = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes?page=1&per_page=2&direction=asc', headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            prototypes = outcome['prototypes']

            self.assertTrue(outcome['page'] == 1)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(prototypes) == 2)
            self.assertTrue(
                re.match(
                    r'^meta-maxquant-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    prototypes[0]['slug'],
                )
            )
            self.assertEqual(prototypes[0]['slug'], self.prototype.slug)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_prototypes_with_page_2_nd_per_page_with_direction_desc(self):
        self.prototypes = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes/?page=2&per_page=2&direction=desc',
                headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            prototypes = outcome['prototypes']

            self.assertTrue(outcome['page'] == 2)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(prototypes) == 1)
            self.assertTrue(
                re.match(
                    r'^meta-maxquant-factory-[0-9]{1,4}-[a-f0-9]{8}$',
                    prototypes[0]['slug'],
                )
            )
            self.assertEqual(prototypes[0]['slug'], self.prototype.slug)

    @freeze_time('2020-06-02 08:57:53')
    @patch.dict(current_app.config, {'PAGINATION_MAX_PER_PAGE': 2})
    def test_fetch_prototypes_with_page_2_and_per_page_with_direction_asc(self):
        self.prototypes = MaxQuantFactory.create_batch(size=2)

        with self.client as rdbclient:
            response = rdbclient.get(
                '/v1/prototypes?page=2&per_page=2&direction=asc', headers=self.headers,
            )

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            prototypes = outcome['prototypes']

            self.assertTrue(outcome['page'] == 2)
            self.assertTrue(outcome['per_page'] == 2)
            self.assertTrue(outcome['total'] == 3)
            self.assertTrue(len(prototypes) == 1)
            self.assertTrue(prototypes[0]['slug'] == self.prototypes[1].slug)


if __name__ == '__main__':
    unittest.main()

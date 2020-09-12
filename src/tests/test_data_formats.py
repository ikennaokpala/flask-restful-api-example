import unittest
import json

from freezegun import freeze_time

from src.tests.base_test_case import BaseTestCase
from src.tests.support.factories import SessionFactory


class TestFetchDataFormats(BaseTestCase):
    def setUp(self):
        super(TestFetchDataFormats, self).setUp()
        self.current_session = SessionFactory.create()
        self.headers = {'Authorization': 'Bearer ' + self.current_session.access_token}

    @freeze_time('2020-06-02 08:57:53')
    def test_fetch_data_formats(self):
        with self.client as rdbclient:
            response = rdbclient.get('/v1/data_formats', headers=self.headers)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content_type, 'application/json')

            self.assertEqual(
                json.loads(response.data.decode()),
                [
                    'mzXML',
                    'mzML',
                    'mzData',
                    'xlsx',
                    'csv',
                    'raw',
                    'BAF',
                    'DAT',
                    'FID',
                    'YEP',
                    'WIFF',
                    'XMS',
                ],
            )

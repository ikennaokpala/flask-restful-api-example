import unittest
import json
from freezegun import freeze_time

from app.tests.base_test_case import BaseTestCase
from app.main.config.oidc import OIDC

class TestAuthorizationCodeURL(BaseTestCase):
    def test_authorization_code_url(self):
        with self.client as rdbclient:
            response = rdbclient.get('/v1/auth/authorization_code_url')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['url'] == OIDC.authorization_code_url())

class TestAuthCallback(BaseTestCase):
    def setUp(self):
        super()
        self.expected = {
            'user': {
                'name': 'TestCase User',
                'given_name': 'TestCase',
                'family_name': 'User',
                'middle_name': 'MiddleMan',
                'nickname': 'Nickname',
                'email': 'testcase.user@testingemaildomain.txt',
                'locale': 'en',
                'access_token': type(self).OIDC_USER_ACCESS_TOKEN,
                'id_token': type(self).OIDC_USER_ID_TOKEN,
                'refresh_token': None,
                'token_type': 'bearer',
                'expires_in': 600,
                'code': type(self).OIDC_USER_AUTHORIZATION_CODE,
                'redirect_uri': type(self).OIDC_REDIRECT_URI,
            }
        }
        self.params = { 'code': type(self).OIDC_USER_AUTHORIZATION_CODE, 'redirect_uri': type(self).OIDC_REDIRECT_URI }

    @freeze_time('2020-05-09 15:04:12', tz_offset=-3)
    def test_successful_auth_with_valid_params(self):
        with self.vcr.use_cassette('v1/auth/valid_authentication_requests.yml'):
            with self.client as rdbclient:
                response = rdbclient.post('/v1/auth/callback', json=self.params)

                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.content_type == 'application/json')

                outcome = json.loads(response.data.decode())
                self.assertTrue(outcome == self.expected)
                self.assertTrue(outcome['user'] == self.expected['user'])
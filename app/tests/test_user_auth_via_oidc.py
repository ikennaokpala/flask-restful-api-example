import unittest
import json
from freezegun import freeze_time

from app.tests.base_test_case import BaseTestCase
from app.main.config.oidc import OIDC
from app.main.models.session import Session
from app.tests.support.factories import SessionFactory

class TestAuthorizationCodeURL(BaseTestCase):
    def test_authorization_code_url(self):
        with self.client as rdbclient:
            response = rdbclient.get('/v1/auth/authorization_code_url')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['url'] == OIDC.authorization_code_url())

class TestSkipAuth(BaseTestCase):
    def test_when_browser_sends_an_options_check_request(self):
        headers = { 'Access-Control-Request-Headers': 'content-type,authorization,x-access-token' }

        with self.client as rdbclient:
            response = rdbclient.options('/v1/auth/logout', headers=headers, json={})

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'text/html; charset=utf-8')
            self.assertTrue(response.headers['Access-Control-Expose-Headers'] == 'Authorization, Content-Type, X-ACCESS-TOKEN')
            self.assertTrue(response.headers['Access-Control-Allow-Origin'] == '*')
            self.assertTrue(response.headers['Allow'] == 'DELETE, OPTIONS')

class TestAuthCallback(BaseTestCase):
    def setUp(self):
        super(TestAuthCallback, self).setUp()
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
                'refresh_token': None,
                'token_type': 'bearer',
                'expires_in': 600,
                'code': type(self).OIDC_USER_AUTHORIZATION_CODE,
                'redirect_uri': type(self).OIDC_REDIRECT_URI,
            }
        }
        self.params = { 'code': type(self).OIDC_USER_AUTHORIZATION_CODE, 'redirect_uri': type(self).OIDC_REDIRECT_URI }

    @freeze_time('2020-06-02 08:57:53')
    def test_successful_auth_with_valid_params(self):
        with self.vcr.use_cassette('v1/auth/valid_authentication_requests.yml'):
            with self.client as rdbclient:
                response = rdbclient.post('/v1/auth/callback', json=self.params)

                self.assertEqual(response.status_code, 201)
                self.assertTrue(response.content_type == 'application/json')

                outcome = json.loads(response.data.decode())
                self.assertTrue(outcome == self.expected)
                self.assertTrue(outcome['user'] == self.expected['user'])

                outcome = Session.query.filter_by(access_token=outcome['user']['access_token']).first()
                outcome.tokenized_user.pop('id_token')
                self.assertTrue(outcome.tokenized_user == self.expected['user'])

    @freeze_time('2020-06-02 09:57:54') # After an hour and 1 second
    def test_when_bearer_token_has_expired(self):
        with self.vcr.use_cassette('v1/auth/valid_authentication_requests.yml'):
            with self.client as rdbclient:
                response = rdbclient.post('/v1/auth/callback', json=self.params)

                self.assertEqual(response.status_code, 422)
                self.assertTrue(response.content_type == 'application/json')

                outcome = json.loads(response.data.decode())
                self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')

    @freeze_time('2020-06-02 09:10:58')
    def test_when_authorization_code_is_expired(self):
        with self.vcr.use_cassette('v1/auth/invalid_422_authentication_requests.yml'):
            with self.client as rdbclient:
                response = rdbclient.post('/v1/auth/callback', json=self.params)

                self.assertEqual(response.status_code, 422)
                self.assertTrue(response.content_type == 'application/json')

                outcome = json.loads(response.data.decode())
                self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')

    def test_when_authorization_code_is_exempted(self):
        parameters = { 'redirect_uri': type(self).OIDC_REDIRECT_URI }
        with self.client as rdbclient:
            response = rdbclient.post('/v1/auth/callback', json=parameters)

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    def test_when_redirect_uri_is_exempted(self):
        parameters = { 'code': 'authorization_code' }
        with self.client as rdbclient:
            response = rdbclient.post('/v1/auth/callback', json=parameters)

            self.assertEqual(response.status_code, 400)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['message'] == 'The browser (or proxy) sent a request that this server could not understand.')

    def test_when_redirect_uri_is_wrong(self):
        parameters = { 'code': 'authorization_code', 'redirect_uri': 'http://wrong.url/path' }
        with self.vcr.use_cassette('v1/auth/invalid_422_authentication_requests.yml'):
            with self.client as rdbclient:
                response = rdbclient.post('/v1/auth/callback', json=parameters)

                self.assertEqual(response.status_code, 422)
                self.assertTrue(response.content_type == 'application/json')

                outcome = json.loads(response.data.decode())
                self.assertTrue(outcome['message'] == 'The request was well-formed but was unable to be followed due to semantic errors.')
        
class TestUserLogout(BaseTestCase):
    def setUp(self):
        super(TestUserLogout, self).setUp()
        self.current_session = SessionFactory.create()
        self.headers = { 'Authorization': 'Bearer ' + self.current_session.access_token }
    
    @freeze_time('2020-06-02 08:57:53')
    def test_logout(self):
        with self.client as rdbclient:
            response = rdbclient.delete('/v1/auth/logout', headers=self.headers)
            self.assertEqual(response.status_code, 202)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome == None)

            outcome = Session.query.filter_by(access_token=self.current_session.access_token).first()
            self.assertTrue(outcome == None)

if __name__ == '__main__':
    unittest.main()

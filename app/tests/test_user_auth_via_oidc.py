import unittest
import json

from app.tests.base import BaseTestCase
from app.main.config.oidc import OIDC

class TestAuthorizationCodeURL(BaseTestCase):
    def test_authorization_code_url(self):
        with self.client as rdbclient:
            response = rdbclient.get('/v1/auth/authorization_code_url')

            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.content_type == 'application/json')

            outcome = json.loads(response.data.decode())
            self.assertTrue(outcome['url'] == OIDC.authorization_code_url())



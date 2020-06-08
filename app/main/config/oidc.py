import os
import vcr

from urllib.parse import urlencode
from collections import namedtuple
from  openid_connect._oidc import OpenIDClient


class OIDC:
    ExemptedUserAttributes = [
      'sub', 'preferred_username', 'profile', 'picture', 'website', 'email_verified', 'gender', 'birthdate', 'zoneinfo',
      'phone_number', 'phone_number_verified', 'address', 'updated_at'
    ]
    OIDCTokenAttributes = ['access_token', 'id_token', 'refresh_token', 'token_type', 'expires_in']
    UserAttributes = ['name', 'given_name', 'family_name', 'middle_name', 'nickname', 'email', 'locale']
    TokenizedUserAttributes = (UserAttributes + OIDCTokenAttributes + ['code', 'redirect_uri'])
    TokenizedUser = namedtuple('TokenizedUser', TokenizedUserAttributes)

    issuer = os.getenv('OIDC_ISSUER', 'https://idp.mit.c3.ca')
    authorization_endpoint = os.getenv('OIDC_AUTHORIZATION_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/authorize')
    registration_endpoint = os.getenv('OIDC_REGISTRATION_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/register')
    token_endpoint = os.getenv('OIDC_TOKEN_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/token')
    user_info_endpoint = os.getenv('OIDC_USER_INFO_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/userinfo')
    jwks_uri_endpoint = os.getenv('OIDC_JWKS_URI', 'https://idp.mit.c3.ca/idp/profile/oidc/keyset')
    configuration_endpoint = os.getenv('OIDC_CONFIGURATION_ENDPOINT', 'https://idp.mit.c3.ca/.well-known/openid-configuration')

    response_types = os.getenv('OIDC_RESPONSE_TYPES', 'code,token,id_token').split(',')
    grant_types = os.getenv('OIDC_GRANT_TYPES', 'authorization_code,refresh_token').split(',')
    token_endpoint_method = os.getenv('OIDC_TOKEN_ENDPOINT_METHOD', 'client_secret_jwt')
    scopes = os.getenv('OIDC_SCOPES', 'openid,profile,email,ca.computecanada.userinfo').split(',')
    claims = os.getenv('OIDC_CLAIMS', 'openid,profile,email').split(',')

    client_id = os.getenv('OIDC_CLIENT_ID', 'rdb-dev-test-staging')
    client_secret = os.getenv('OIDC_CLIENT_SECRET', '46bdf96f-4cec-44b6-b6c7-e49d72f6840c')

    @classmethod
    def authorization_code_url(klazz):
        return klazz.authorization_endpoint + '?' + urlencode(klazz.__authorization_code_params())

    @classmethod
    def tokenized_user(klazz, code, redirect_uri):
        client = OpenIDClient(klazz.issuer, klazz.client_id, klazz.client_secret)
        token_response = client.request_token(redirect_uri, code)
        user_info = token_response.userinfo
        refresh_token = None

        return klazz.TokenizedUser(
          name=user_info.get('name', None),
          given_name=user_info.get('given_name', None),
          family_name=user_info.get('family_name', None),
          middle_name=user_info.get('middle_name', None),
          nickname=user_info.get('nickname', None),
          email=user_info.get('email', None),
          locale=user_info.get('locale', None),
          access_token=token_response.access_token,
          id_token=token_response.id_token,
          refresh_token=refresh_token,
          token_type='bearer',
          expires_in=600,
          redirect_uri=redirect_uri,
          code=code,
        )

    @classmethod
    def __authorization_code_params(klazz):
        return {
          'response_type': klazz.response_types[0],
          'scope': ','.join(klazz.scopes),
          'client_id': klazz.client_id,
          'grant_type': klazz.grant_types[0]
        }

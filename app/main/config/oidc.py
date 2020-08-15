import os
from dataclasses import make_dataclass


class OIDC:
    ExemptedUserAttributes = [
        'sub',
        'preferred_username',
        'profile',
        'picture',
        'website',
        'email_verified',
        'gender',
        'birthdate',
        'zoneinfo',
        'phone_number',
        'phone_number_verified',
        'address',
        'updated_at',
    ]
    OIDCTokenAttributes = [
        'access_token',
        'id_token',
        'refresh_token',
        'token_type',
        'expires_in',
    ]
    UserAttributes = [
        'name',
        'given_name',
        'family_name',
        'middle_name',
        'nickname',
        'email',
        'locale',
    ]
    TokenizedUserAttributes = (
        UserAttributes + OIDCTokenAttributes + ['code', 'redirect_uri']
    )
    TokenizedUser = make_dataclass('TokenizedUser', TokenizedUserAttributes)

    issuer = os.getenv('OIDC_ISSUER', 'https://idp.mit.c3.ca')
    authorization_endpoint = os.getenv(
        'OIDC_AUTHORIZATION_ENDPOINT',
        'https://idp.mit.c3.ca/idp/profile/oidc/authorize',
    )
    registration_endpoint = os.getenv(
        'OIDC_REGISTRATION_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/register'
    )
    token_endpoint = os.getenv(
        'OIDC_TOKEN_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/token'
    )
    user_info_endpoint = os.getenv(
        'OIDC_USER_INFO_ENDPOINT', 'https://idp.mit.c3.ca/idp/profile/oidc/userinfo'
    )
    jwks_uri_endpoint = os.getenv(
        'OIDC_JWKS_URI', 'https://idp.mit.c3.ca/idp/profile/oidc/keyset'
    )
    configuration_endpoint = os.getenv(
        'OIDC_CONFIGURATION_ENDPOINT',
        'https://idp.mit.c3.ca/.well-known/openid-configuration',
    )

    response_types = os.getenv('OIDC_RESPONSE_TYPES', 'code,token,id_token').split(',')
    grant_types = os.getenv(
        'OIDC_GRANT_TYPES', 'authorization_code,refresh_token'
    ).split(',')
    token_endpoint_method = os.getenv('OIDC_TOKEN_ENDPOINT_METHOD', 'client_secret_jwt')
    scopes = os.getenv(
        'OIDC_SCOPES', 'openid,profile,email,ca.computecanada.userinfo'
    ).split(',')
    claims = os.getenv('OIDC_CLAIMS', 'openid,profile,email').split(',')

    client_id = os.getenv('OIDC_CLIENT_ID', 'rdb-dev-test-staging')
    client_secret = os.getenv(
        'OIDC_CLIENT_SECRET', '46bdf96f-4cec-44b6-b6c7-e49d72f6840c'
    )

    @classmethod
    def authorization_code_params(klazz):
        return {
            'response_type': klazz.response_types[0],
            'scope': ','.join(klazz.scopes),
            'client_id': klazz.client_id,
            'grant_type': klazz.grant_types[0],
        }

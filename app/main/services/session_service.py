from urllib.parse import urlencode
from openid_connect._oidc import OpenIDClient
from openid_connect._verify import verify

from app.main.config.oidc import OIDC


class SessionService:
    @classmethod
    def authorization_code_url(klazz):
        return (
            OIDC.authorization_endpoint
            + '?'
            + urlencode(OIDC.authorization_code_params())
        )

    @classmethod
    def auth(klazz, code, redirect_uri):
        return klazz.__tokenized_user(code, redirect_uri)

    @classmethod
    def __tokenized_user(klazz, code, redirect_uri):
        client = OpenIDClient(OIDC.issuer, OIDC.client_id, OIDC.client_secret)
        token_response = client.request_token(redirect_uri, code)
        user_info = token_response.userinfo
        refresh_token = None

        return OIDC.TokenizedUser(
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
    def valid(klazz, id_token):
        return verify(
            OpenIDClient(OIDC.issuer, OIDC.client_id, OIDC.client_secret), id_token
        )

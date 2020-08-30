from urllib.parse import urlencode
from openid_connect._oidc import OpenIDClient
from openid_connect._verify import verify

from app.main.config.oidc import OIDC


class SessionService:
    code = None
    redirect_uri = None

    @classmethod
    def authorization_code_url(klazz):
        return (
            OIDC.authorization_endpoint
            + '?'
            + urlencode(OIDC.authorization_code_params())
        )

    @classmethod
    def auth(klazz, code, redirect_uri):
        klazz.code = code
        klazz.redirect_uri = redirect_uri

        return klazz.__authenticate()

    @classmethod
    def __authenticate(klazz):
        client = OpenIDClient(OIDC.issuer, OIDC.client_id, OIDC.client_secret)
        return klazz.__tokenized_user(
            client.request_token(klazz.redirect_uri, klazz.code)
        )

    @classmethod
    def __tokenized_user(klazz, token) -> OIDC.TokenizedUser:
        user_info = token.userinfo

        return OIDC.TokenizedUser(
            name=user_info.get('name', None),
            given_name=user_info.get('given_name', None),
            family_name=user_info.get('family_name', None),
            middle_name=user_info.get('middle_name', None),
            nickname=user_info.get('nickname', None),
            email=user_info.get('email', None),
            locale=user_info.get('locale', None),
            access_token=token.access_token,
            id_token=token.id_token,
            refresh_token=None,
            token_type='bearer',
            expires_in=600,
            redirect_uri=klazz.redirect_uri,
            code=klazz.code,
        )

    @classmethod
    def valid(klazz, id_token):
        return verify(
            OpenIDClient(OIDC.issuer, OIDC.client_id, OIDC.client_secret), id_token
        )

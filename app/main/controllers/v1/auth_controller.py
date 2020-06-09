import openid_connect

from flask_restplus import Namespace, Resource, fields
from flask import request
from werkzeug.exceptions import UnprocessableEntity
from werkzeug.exceptions import BadRequest
from requests.exceptions import HTTPError

from app.main.config.oidc import OIDC
from app.main.dao.session_dao import SessionDAO

endpoint = Namespace('auth-endpoint', description='authentication related api endpoints')

authorization_code_url_fields = endpoint.model('Resource', {
    'url': fields.String,
})
tokenized_user_fields = endpoint.model('Resource', {
    'user': {
        'name': fields.String,
        'given_name': fields.String,
        'family_name': fields.String,
        'middle_name': fields.String,
        'nickname': fields.String,
        'email': fields.String,
        'locale': fields.String,
        'access_token': fields.String,
        'refresh_token': fields.String,
        'token_type': fields.String,
        'expires_in': fields.Integer,
        'code': fields.String,
        'redirect_uri': fields.String,
    }
})

@endpoint.route('/authorization_code_url')
class AuthorizationCodeURL(Resource):
    @endpoint.expect(authorization_code_url_fields)
    def get(self):
        return { 'url': OIDC.authorization_code_url() }

@endpoint.route('/callback')
@endpoint.doc(params={'code': 'Authorization code issued by IdP from the frontend', 'redirect_uri': 'Redirect URI'})
class AuthCallback(Resource):
    @endpoint.expect(tokenized_user_fields)
    def post(self):
        try:
            outcome = lambda token_user: (token_user.pop('id_token') and token_user)
            tokenized_user = OIDC.tokenized_user(request.json['code'], request.json['redirect_uri'])
            dao = SessionDAO(tokenized_user).create()
            return { 'user': outcome(dao.tokenized_user.copy()) }, 201
        except (openid_connect.errors.Forbidden, HTTPError):
            raise UnprocessableEntity
        except (KeyError):
            raise BadRequest

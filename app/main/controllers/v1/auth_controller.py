from flask_restplus import Namespace, Resource, fields
from flask import request

from app.main.config.oidc import OIDC

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
        'id_token': fields.String,
        'refresh_token': fields.String,
        'token_type': fields.String,
        'expires_in': fields.Integer,
        'code': fields.String,
        'redirect_uri': fields.String,
    }
})

@endpoint.route('/authorization_code_url')
class AuthorizationCodeURLController(Resource):
    @endpoint.expect(authorization_code_url_fields)
    def get(self):
        return { 'url': OIDC.authorization_code_url() }

@endpoint.route('/callback')
@endpoint.doc(params={'code': 'Authorization code issued by IdP from the frontend', 'redirect_uri': 'Redirect URI'})
class AuthCallbackController(Resource):
    @endpoint.expect(tokenized_user_fields)
    def post(self):
        return { 'user': OIDC.tokenized_user(request.json)._asdict() }

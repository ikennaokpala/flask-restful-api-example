from flask_restplus import Namespace, Resource, fields
from flask import request

from app.main.config.oidc import OIDC

endpoint = Namespace('auth-endpoint', description='authentication related api endpoints')

authorization_code_url_fields = endpoint.model('Resource', {
    'url': fields.String,
})

@endpoint.route('/authorization_code_url')
class AuthorizationCodeURLController(Resource):
    @endpoint.expect([authorization_code_url_fields])
    def get(self):
        return { 'url': OIDC.authorization_code_url() }

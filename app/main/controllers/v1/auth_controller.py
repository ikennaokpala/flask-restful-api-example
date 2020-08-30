import openid_connect

from flask_restx import Namespace, Resource, fields
from flask import request, session
from werkzeug.exceptions import UnprocessableEntity
from werkzeug.exceptions import BadRequest
from requests.exceptions import HTTPError

from app.main.services.session_service import SessionService
from app.main.dao.session_dao import SessionDAO
from app.main.models.session import Session

endpoint = Namespace(
    'auth-endpoint', description='authentication related api endpoints'
)

authorization_code_url_fields = endpoint.model('Resource', {'url': fields.String,},)
tokenized_user_fields = endpoint.model(
    'Resource',
    {
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
    },
)


@endpoint.route('/authorization_code_url')
@endpoint.doc(description='Endpoint for users identity provider')
class AuthorizationCodeURL(Resource):
    @endpoint.response(
        200,
        'Success - retrieved authorizaton code url',
        url=authorization_code_url_fields,
    )
    def get(self):
        return {'url': SessionService.authorization_code_url()}


@endpoint.route('/callback')
@endpoint.doc(
    description='Endpoint to create a logged in user session',
    params={
        'code': 'Authorization code issued by IdP from the frontend',
        'redirect_uri': 'Redirect URI',
    },
    responses={201: 'Created', 403: 'Forbidden', 400: 'Bad Request',},
)
class AuthCallback(Resource):
    def post(self):
        try:
            outcome = lambda token_user: (token_user.pop('id_token') and token_user)
            tokenized_user = SessionService.auth(
                request.json['code'], request.json['redirect_uri']
            )
            dao = SessionDAO(tokenized_user).create()
            return {'user': outcome(dao.tokenized_user.copy())}, 201
        except (openid_connect.errors.Forbidden, HTTPError):
            raise UnprocessableEntity
        except (KeyError):
            raise BadRequest


@endpoint.route('/logout')
@endpoint.doc(
    description='Endpoint to log a user out',
    params={
        'token_user': 'The logged in user',
        'access_token': 'The logged in users access token',
    },
    responses={202: 'Accepted'},
)
class AuthLogout(Resource):
    def delete(self):
        Session.query.filter_by(
            access_token=session['token_user']['access_token']
        ).delete()
        session['token_user'] = None

        return None, 202

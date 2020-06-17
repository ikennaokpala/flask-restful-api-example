import openid_connect

from flask_restplus import Api
from flask import Blueprint, request, abort, session

from app.main.config.oidc import OIDC
from app.main.models.session import Session

from app.main.controllers.v1.auth_controller import endpoint as auth_endpoint
from app.main.controllers.v1.projects_controller import endpoint as projects_endpoint
from app.main.controllers.v1.project_raw_files_controller import endpoint as project_raw_files_endpoint

v1_blueprint = Blueprint('api', __name__, url_prefix='/v1')

api = Api(v1_blueprint,
          title='LSARP API',
          version='1.0',
          description='This is the backend API implementation for the LSARP project'
          )

api.add_namespace(auth_endpoint, path='/auth')
api.add_namespace(projects_endpoint, path='/projects')
api.add_namespace(project_raw_files_endpoint, path='/projects/<slug>')

NONE_AUTH_ENDPOINTS = ('/v1/auth/callback', '/v1/auth/authorization_code_url')
SKIP_OIDC_VALIDATIONS = ('/v1/auth/logout')

@v1_blueprint.before_request
def authenticate():
    if request.path.startswith(NONE_AUTH_ENDPOINTS) or request.method == 'OPTIONS': return

    try:
        access_token = access_token_from_header().split().pop()
        current_session = Session.query.filter_by(access_token=access_token).first()
        session['token_user'] = current_session.tokenized_user

        if not request.path.startswith(SKIP_OIDC_VALIDATIONS): OIDC.valid(session['token_user']['id_token'])
    except (openid_connect.errors.Forbidden, AttributeError):
        abort(401)
    except (KeyError):
        abort(400)

def access_token_from_header():
    try:
        return request.headers['Authorization']
    except (KeyError):
        return request.headers['X-ACCESS-TOKEN']

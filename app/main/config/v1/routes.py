import openid_connect

from flask_restplus import Api
from flask import Blueprint, request, abort, session

from app.main.services.session_service import SessionService
from app.main.models.session import Session

from app.main.controllers.v1.auth_controller import endpoint as auth_endpoint
from app.main.controllers.v1.projects_controller import endpoint as projects_endpoint
from app.main.controllers.v1.data_types_controller import endpoint as data_types_endpoint
from app.main.controllers.v1.data_formats_controller import endpoint as data_formats_endpoint
from app.main.controllers.v1.data_type_mzxml_files_controller import endpoint as data_type_mzxml_files_endpoint
from app.main.controllers.v1.data_type_metadata_shipments_controller import endpoint as data_types_metadata_endpoint

class RouterV1:
	def draw(klazz, api, prefix=''):
		api.add_namespace(auth_endpoint, path=prefix + '/auth')
		api.add_namespace(projects_endpoint, path=prefix + '/projects')
		api.add_namespace(data_formats_endpoint, path=prefix + '/data_formats')
		api.add_namespace(data_types_endpoint, path=prefix + '/projects/<slug>/data_types')
		api.add_namespace(data_type_mzxml_files_endpoint, path=prefix + '/projects/<slug>/data_types/<data_type_slug>')
		api.add_namespace(data_types_metadata_endpoint, path=prefix + '/projects/<slug>/data_types/<data_type_slug>')

v1_blueprint = Blueprint('api_version_one', __name__, url_prefix='/v1')
RouterV1().draw(Api(v1_blueprint))

NONE_AUTH_ENDPOINTS = ('/v1/auth/callback', '/v1/auth/authorization_code_url')
SKIP_OIDC_VALIDATIONS = ('/v1/auth/logout')

@v1_blueprint.before_request
def authenticate():
    if request.path.startswith(NONE_AUTH_ENDPOINTS) or request.method == 'OPTIONS':
        return

    try:
        access_token = access_token_from_header().split().pop()
        current_session = Session.query.filter_by(
            access_token=access_token).first()
        if not request.path.startswith(SKIP_OIDC_VALIDATIONS):
            SessionService.valid(current_session.tokenized_user['id_token'])
        session['token_user'] = current_session.tokenized_user

    except (openid_connect.errors.Forbidden, AttributeError, IndexError):
        abort(401)
    except (KeyError):
        abort(400)

def access_token_from_header():
    try:
        return request.headers['Authorization']
    except (KeyError):
        return request.headers['X-ACCESS-TOKEN']

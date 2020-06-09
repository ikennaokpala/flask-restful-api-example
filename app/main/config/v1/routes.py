import openid_connect

from flask_restplus import Api
from flask import Blueprint, request, abort, session

from app.main.config.oidc import OIDC
from app.main.models.session import Session

from app.main.controllers.v1.auth_controller import endpoint as auth_endpoint
from app.main.controllers.v1.projects_controller import endpoint as projects_endpoint

v1_blueprint = Blueprint('api', __name__, url_prefix='/v1')

api = Api(v1_blueprint,
          title='LSARP API',
          version='1.0',
          description='This is the backend API implementation for the LSARP project'
          )

api.add_namespace(auth_endpoint, path='/auth')
api.add_namespace(projects_endpoint, path='/projects')

@v1_blueprint.before_request
def authenticate():
  if request.path.startswith('/v1/auth'):
    return

  if request.headers.get('Authorization'):
    try:
      access_token = request.headers.get('Authorization').split().pop()
      current_session = Session.query.filter_by(access_token=access_token).first()
      session['token_user'] = current_session.tokenized_user

      if session['token_user'] and OIDC.valid(session['token_user']['id_token']):
        return
      else:
        abort(401)

    except (openid_connect.errors.Forbidden, AttributeError):
        abort(401)
  else:
      abort(403)

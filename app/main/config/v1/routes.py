from flask_restplus import Api
from flask import Blueprint

from app.main.controllers.v1.auth_controller import endpoint as auth_endpoint

v1_blueprint = Blueprint('api', __name__, url_prefix='/v1')

api = Api(v1_blueprint,
          title='LSARP API',
          version='1.0',
          description='This is the backend API implementation for the LSARP project'
          )

api.add_namespace(auth_endpoint, path='/auth')
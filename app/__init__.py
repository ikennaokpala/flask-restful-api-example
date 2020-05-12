from flask_restplus import Api
from flask import Blueprint

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='LSARP API',
          version='1.0',
          description='This is the backend API implementation for the LSARP project'
          )

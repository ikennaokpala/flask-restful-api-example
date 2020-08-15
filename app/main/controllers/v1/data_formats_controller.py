from flask_restx import Namespace, Resource
from flask import current_app

endpoint = Namespace(
    'data-formats-endpoint', description='Data formats related api endpoints'
)


@endpoint.route('/')
@endpoint.route('')
class DataFormats(Resource):
    @endpoint.doc('List of a allowed data formats')
    def get(self):
        return current_app.config['DATA_FORMAT_FILE_EXTENSIONS']

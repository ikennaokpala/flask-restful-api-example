from flask_restx import Namespace, Resource, fields
from flask import current_app

endpoint = Namespace(
    'data-formats-endpoint', description='Data formats related api endpoints'
)

data_formats_fields = endpoint.model('DataFormats',
{
    'data_formats': fields.List(fields.String)
})

@endpoint.route('/')
@endpoint.route('')
class DataFormats(Resource):
    @endpoint.doc(
        description='List of a allowed data formats',
        responses={
            400: 'Bad request',
            404: 'Not Found',
        },
    )
    @endpoint.response(200, 'Success - Data Formats fetched', data_formats_fields)
    def get(self):
        return current_app.config['DATA_FORMAT_FILE_EXTENSIONS']

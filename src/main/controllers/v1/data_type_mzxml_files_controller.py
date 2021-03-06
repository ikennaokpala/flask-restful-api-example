from flask_restx import Namespace, Resource, fields
from flask import request, abort
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest

from src.main.dao.data_type_mzxml_files_dao import DataTypeMZXmlFilesDAO

endpoint = Namespace(
    'project-data-type-mzxml-files-endpoint',
    description='mzXML files belonging to a project via data type group api endpoints',
)

data_type_MZXml_field = endpoint.model(
    'Resource',
    {
        'id': fields.Integer,
        'name': fields.String,
        'extension': fields.String,
        'path': fields.String,
        'checksum': fields.String,
        'project_slug': fields.String,
        'data_type_slug': fields.String,
    },
)
upload_parser = endpoint.parser()
upload_parser.add_argument('file', location='files', type='file', required=True)


@endpoint.route('/mzxml_file')
@endpoint.route('/mzxml_files')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.param('data_type_slug', 'The data type slug identifier')
@endpoint.doc(
    params={
        'mzxml_file_<index>': 'mzxml file object',
        'slug': 'The project slug identifier',
        'data_type_slug': 'The data type slug identifier',
    }
)
class MZXmlDataType(Resource):
    @endpoint.doc(
        description='Associate mzXML file(s) with a project via data type group',
        responses={400: 'Bad request', 404: 'Not Found',},
    )
    @endpoint.response(201, 'File(s) added to project', data_type_MZXml_field)
    @endpoint.expect(upload_parser)
    def put(self, slug, data_type_slug):
        try:
            return DataTypeMZXmlFilesDAO(data_type_slug, request.files).upload(), 201
        except (NotFound):
            abort(404)

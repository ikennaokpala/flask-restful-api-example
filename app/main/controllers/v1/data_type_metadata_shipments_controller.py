from flask_restx import Namespace, Resource, fields
from flask import request, abort, jsonify
from werkzeug.exceptions import NotFound

from app.main.dao.data_type_metadata_shipment_files_dao import (
    DataTypeMetadataShipmentFilesDAO,
)

endpoint = Namespace(
    'data-type-metadata-shipments-endpoint',
    description='metadata shipments belonging to a data type api endpoints',
)
xlsx_content_fields = endpoint.model(
    'XlsxContent',
    {
        'rows': fields.List(fields.String),
        'columns': fields.List(fields.String),
    },
)
data_type_xlsx_fields = endpoint.model(
    'Xlsx',
    {
        'id': fields.Integer,
        'name': fields.String,
        'extension': fields.String,
        'path': fields.String,
        'checksum': fields.String,
        'content': fields.List(fields.Nested(xlsx_content_fields)),
        'project_slug': fields.String,
        'data_type_slug': fields.String,
    },
)

upload_parser = endpoint.parser()
upload_parser.add_argument('file', location='files', type='file', required=True)


@endpoint.route('/metadata_shipment')
@endpoint.route('/metadata_shipments')
@endpoint.param('data_type_slug', 'The data_type identifier')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.doc(
    params={
        'metadata_shipment_<index>': 'Metadata Shipment object',
        'data_type_slug': 'The data type identifier',
        'slug': 'The project slug identifier',
    }
)
class DataTypeMetadataShipment(Resource):
    @endpoint.doc(
        description='Associate Metadata Shipment(s) with a data type',
        responses={
            400: 'Bad request',
            404: 'Not Found',
        },
    )
    @endpoint.expect(upload_parser)
    @endpoint.response(201, 'Success - File(s) added', data_type_xlsx_fields)
    def put(self, slug, data_type_slug):
        try:
            return (
                DataTypeMetadataShipmentFilesDAO(
                    data_type_slug, request.files
                ).upload(),
                201,
            )
        except (NotFound):
            abort(404)

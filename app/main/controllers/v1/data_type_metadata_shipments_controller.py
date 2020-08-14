from flask_restplus import Namespace, Resource, fields
from flask import request, abort, jsonify
from werkzeug.exceptions import NotFound

from app.main.dao.data_type_metadata_shipment_files_dao import DataTypeMetadataShipmentFilesDAO

endpoint = Namespace('data-type-metadata-shipments-endpoint', description='metadata shipments belonging to a data type api endpoints')

@endpoint.route('/metadata_shipment')
@endpoint.route('/metadata_shipments')
@endpoint.param('data_type_slug', 'The data_type identifier')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.doc(params={'metadata_shipment_<index>': 'Metadata Shipment object', 'data_type_slug': 'The data type identifier', 'slug': 'The project slug identifier'})
class DataTypeMetadataShipment(Resource):
	@endpoint.doc(description='Associate Metadata Shipment(s) with a data type', responses={
		400: 'Bad request',
		404: 'Not Found',
		201: 'Success - File(s) added'
	})
	def put(self, slug, data_type_slug):
		try:
			return DataTypeMetadataShipmentFilesDAO(data_type_slug, request.files).upload(), 201
		except (NameError, IndexError):
			abort(400)
		except (NotFound):
			abort(404)

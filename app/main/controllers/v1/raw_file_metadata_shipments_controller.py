from flask_restplus import Namespace, Resource, fields
from flask import request, abort, jsonify
from werkzeug.exceptions import NotFound

from app.main.dao.raw_file_metadata_shipment_dao import RawFileMetadataShipmentDAO

endpoint = Namespace('raw-files-metadata-shipments-endpoint', description='metadata shipments belonging to a raw file api endpoints')

@endpoint.route('/metadata_shipment')
@endpoint.route('/metadata_shipments')
@endpoint.param('raw_file_id', 'The raw_file identifier')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.doc(params={'metadata_shipment_<index>': 'Metadata Shipment object', 'raw_file_id': 'The raw file identifier', 'slug': 'The project slug identifier'})
class RawFileMetadataShipment(Resource):
	@endpoint.doc(description='Associate Metadata Shipment(s) with a Raw file', responses={
		400: 'Bad request',
		404: 'Not Found',
		201: 'File(s) added to Raw file'
	})
	def put(self, slug, raw_file_id):
		try:
			return RawFileMetadataShipmentDAO(raw_file_id, request.files).upload(), 201
		except (NameError, IndexError):
			abort(400)
		except (NotFound):
			abort(404)

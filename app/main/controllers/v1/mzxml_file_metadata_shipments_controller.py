from flask_restplus import Namespace, Resource, fields
from flask import request, abort, jsonify
from werkzeug.exceptions import NotFound

from app.main.dao.mzxml_file_metadata_shipment_dao import MZXmlFileMetadataShipmentDAO

endpoint = Namespace('mzxml-files-metadata-shipments-endpoint', description='metadata shipments belonging to a mzxml file api endpoints')

@endpoint.route('/metadata_shipment')
@endpoint.route('/metadata_shipments')
@endpoint.param('mzxml_file_id', 'The mzxml_file identifier')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.doc(params={'metadata_shipment_<index>': 'Metadata Shipment object', 'mzxml_file_id': 'The mzxml file identifier', 'slug': 'The project slug identifier'})
class MZXmlFileMetadataShipment(Resource):
	@endpoint.doc(description='Associate Metadata Shipment(s) with a mzXML file', responses={
		400: 'Bad request',
		404: 'Not Found',
		201: 'Success - File(s) added'
	})
	def put(self, slug, mzxml_file_id):
		try:
			return MZXmlFileMetadataShipmentDAO(mzxml_file_id, request.files).upload(), 201
		except (NameError, IndexError):
			abort(400)
		except (NotFound):
			abort(404)

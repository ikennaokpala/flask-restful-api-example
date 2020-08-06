from flask_restplus import Namespace, Resource, fields
from flask import request
from werkzeug.exceptions import BadRequest

from app.main.dao.data_type_dao import DataTypeDAO

endpoint = Namespace('data-types-endpoint', description='data-types related api endpoints')

data_type_field = endpoint.model('Resource', {
    'slug': fields.String,
})

@endpoint.route('/data_types/')  # with slash
@endpoint.route('/data_types')  # without slash
class DataTypes(Resource):
	@endpoint.doc('Create a DataType')
	@endpoint.expect(model=data_type_field, validate=True)
	def post(self, slug):
		try:
			dao = DataTypeDAO(request.json, slug).create()
			return {'slug': dao.data_type.slug}, 201
		except (KeyError):
			raise BadRequest

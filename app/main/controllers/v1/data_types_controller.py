from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from dataclasses import asdict

from app.main.dao.data_type_dao import DataTypeDAO
from app.main.dao.data_types_dao import DataTypesDAO
from app.main.models.data_type import DataType
from app.main import db

endpoint = Namespace('data-types-endpoint', description='data-types related api endpoints')

data_type_field = endpoint.model('Resource', {
	'slug': fields.String,
})
data_type_fields = endpoint.model('Resource', {
	'page': fields.Integer,
	'per_page': fields.Integer,
	'total': fields.Integer,
	'data_types': {
		'name': fields.String,
		'description': fields.String,
		'slug': fields.String,
		'project_slug': fields.String,
	}
})

@endpoint.route('/')  # with slash
@endpoint.route('')  # without slash
class DataTypes(Resource):
	@endpoint.doc('Create a DataType')
	@endpoint.expect(model=data_type_field, validate=True)
	def post(self, slug):
		try:
			dao = DataTypeDAO(request.json, slug).create()
			return {'slug': dao.data_type.slug, 'name': dao.data_type.name, 'description': dao.data_type.description, 'data_formats': dao.data_type.data_formats }, 201
		except (KeyError):
			raise BadRequest

	@endpoint.doc('List of a user\'s data_types')
	@endpoint.doc(params={'page': 'Page or Offset for data_types', 'per_page': 'Number of data_types per page', 'direction': 'Sort desc or asc'})
	@endpoint.expect(data_type_fields)
	def get(self, slug):
		data_types = DataTypesDAO.call(request.args, slug)
		return jsonify(asdict(data_types))

@endpoint.route('/<data_type_slug>')
@endpoint.param('slug', 'The project identifier')
@endpoint.param('data_type_slug', 'The DataType identifier')
@endpoint.doc(params={'name': 'Name of DataType', 'description': 'Description of the DataType'})
class ADataType(Resource):
	@endpoint.doc('Fetch a DataType by slug')
	@endpoint.expect(model=data_type_fields)
	def get(self, slug, data_type_slug):
		return jsonify(DataType.query.filter_by(slug=data_type_slug).first())

	@endpoint.doc('Update a DataType by slug')
	@endpoint.expect(model=data_type_fields)
	def put(self, slug, data_type_slug):
		dao = DataTypeDAO(request.json, data_type_slug).update_by()
		return jsonify({'slug': dao.data_type.slug})

	@endpoint.doc('Deletes a data type by slug')
	@endpoint.expect(model=data_type_field)
	def delete(self, slug, data_type_slug):
		DataType.query.filter_by(slug=data_type_slug).delete()
		db.session.commit()
		return None, 204

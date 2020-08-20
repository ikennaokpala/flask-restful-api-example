from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from werkzeug.exceptions import BadRequest
from dataclasses import asdict

from app.main.dao.data_type_dao import DataTypeDAO
from app.main.dao.data_types_dao import DataTypesDAO
from app.main.models.data_type import DataType
from app.main import db

endpoint = Namespace(
    'data-types-endpoint', description='data-types related api endpoints'
)

data_type_field = endpoint.model('Slug', {'slug': fields.String,})

data_type_create = endpoint.model('Data_Type', {
    'name': fields.String,
    'description': fields.String,
    'data_formats': fields.List(fields.String),
    }
)

data_type_created = endpoint.model(
    'DataType', 
    {
    'slug': fields.String,
    'name': fields.String,
    'description': fields.String,
    'data_formats': fields.List(fields.String),
    },
)

data_type_fields = endpoint.model('Data_Type_With_Files', {
        'id': fields.Integer,
        'name': fields.String,
        'description': fields.String,
        'slug': fields.String,
        'meta_data_shipments': fields.List(fields.String),
        'mzxml_files': fields.List(fields.String),
        'data_formats': fields.List(fields.String),
        'project_slug': fields.String,
    }
)

data_types_list = endpoint.model(
    'DataTypesList',
    {
        'page': fields.Integer,
        'per_page': fields.Integer,
        'total': fields.Integer,
        'data_types': fields.Nested(data_type_fields),
    },
)


@endpoint.route('/')  # with slash
@endpoint.route('')  # without slash
class DataTypes(Resource):
    @endpoint.doc(description='Create a DataType', params={'slug': 'The projects identifier'})
    @endpoint.expect(data_type_create)
    @endpoint.response(201, 'Created', data_type_created)
    @endpoint.response(400, 'BadRequest')
    def post(self, slug):
        try:
            dao = DataTypeDAO(request.json, slug).create()
            return (
                {
                    'slug': dao.data_type.slug,
                    'name': dao.data_type.name,
                    'description': dao.data_type.description,
                    'data_formats': dao.data_type.data_formats,
                },
                201,
            )
        except (KeyError):
            raise BadRequest

    @endpoint.doc(description='List of a user\'s project data_types', params={'slug':'The project identifier'})
    @endpoint.response(200, 'Success', data_types_list)
    def get(self, slug):
        data_types = DataTypesDAO.call(request.args, slug)
        return jsonify(asdict(data_types))


@endpoint.route('/<data_type_slug>')
@endpoint.param('slug', 'The project identifier')
@endpoint.param('data_type_slug', 'The DataType identifier')
class ADataType(Resource):
    @endpoint.doc(description='Fetch a DataType by slug')
    @endpoint.response(200, 'Success')
    def get(self, slug, data_type_slug):
        return jsonify(DataType.query.filter_by(slug=data_type_slug).first())

    @endpoint.doc(description='Update a DataType by slug')
    @endpoint.response(200, 'Success')
    def put(self, slug, data_type_slug):
        dao = DataTypeDAO(request.json, data_type_slug).update_by()
        return jsonify({'slug': dao.data_type.slug})

    @endpoint.doc(description='Deletes a data type by slug')
    @endpoint.response(204, 'Deleted')
    def delete(self, slug, data_type_slug):
        DataType.query.filter_by(slug=data_type_slug).delete()
        db.session.commit()
        return None, 204

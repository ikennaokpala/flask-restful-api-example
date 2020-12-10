from flask_restx import Namespace, Resource, fields
from werkzeug.exceptions import BadRequest
from flask import request, jsonify
from dataclasses import asdict
from src.main import db

from src.main.models.prototypes.max_quant import MaxQuant
from src.main.dao.max_quant_dao import MaxQuantDAO
from src.main.dao.max_quants_dao import MaxQuantsDAO

endpoint = Namespace(
    'max-quant-prototypes-endpoint',
    description='MaxQuant prototype related api endpoints',
)

fasta_file_fields = endpoint.model(
    'FastaFile',
    {
        'name': fields.String,
        'extension': fields.String,
        'path': fields.String,
        'checksum': fields.String,
    },
)
max_quant_file_fields = endpoint.model(
    'MaxQuantFile',
    {'name': fields.String, 'extension': fields.String, 'content': fields.String,},
)
content_file_fields = endpoint.model(
    'ContentFile',
    {
        'fasta_file': fields.Nested(fasta_file_fields),
        'max_quant_file': fields.Nested(max_quant_file_fields),
    },
)
max_quant_prototype_fields = endpoint.model(
    'MaxQuantInfo',
    {
        'name': fields.String,
        'description': fields.String,
        'type': fields.String,
        'slug': fields.String,
        'content': fields.Nested(content_file_fields),
    },
)

expected_params_parser = endpoint.parser()
expected_params_parser.add_argument(
    'name', type=str, help='The name of the MaxQuant prototypes', required=True,
)
expected_params_parser.add_argument(
    'description',
    type=str,
    help='The description for the MaxQuant prototypes',
    required=False,
)
expected_params_parser.add_argument(
    'fasta_file',
    location='files',
    type='file',
    help='The fasta file to be attached to the MaxQuant template',
    required=True,
)
expected_params_parser.add_argument(
    'max_quant_file',
    location='files',
    type='file',
    help='The MaxQuant prototypes file',
    required=True,
)


@endpoint.route('/')  # with slash
@endpoint.route('')  # without slash
class MaxQuantPrototypes(Resource):
    @endpoint.doc(
        description='Create a MaxQuant Prototype', params={},
    )
    @endpoint.response(201, 'Created', max_quant_prototype_fields)
    @endpoint.expect(expected_params_parser)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(422, 'Unprocessable Entity')
    def post(self):
        try:
            params = dict(request.form)
            params.update(dict(request.files))
            dao = MaxQuantDAO(params).create()
            return asdict(dao.max_quant), 201
        except (KeyError):
            raise BadRequest

    @endpoint.doc(
        description='List of a user\'s MaxQuant',
        params={
            'page': 'Page or Offset for MaxQuant',
            'per_page': 'Number of MaxQuant per page',
            'direction': 'Sort desc or asc',
        },
    )
    @endpoint.response(200, 'Success - MaxQuant fetched', max_quant_prototype_fields)
    @endpoint.response(400, 'Bad Request')
    def get(self):
        max_quants = MaxQuantsDAO.call(request.args)
        return jsonify(asdict(max_quants))


@endpoint.route('/<slug>')
class MaxQuantPrototype(Resource):
    @endpoint.doc(
        description='Fetch a maxquant by slug',
        params={'slug': 'The maxquant identifier'},
    )
    @endpoint.response(200, 'Success', max_quant_prototype_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def get(self, slug):
        return jsonify(MaxQuant.query.filter_by(slug=slug).first())

    @endpoint.doc(
        description='Update a MaxQuant prototype',
        params={
            'name': 'The name of the MaxQuant prototype',
            'description': 'The description for the MaxQuant prototype',
        },
    )
    @endpoint.expect(expected_params_parser)
    @endpoint.response(200, 'Success', max_quant_prototype_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(422, 'Unprocessable Entity')
    def put(self, slug):
        params = dict(request.form)
        params.update(dict(request.files))
        dao = MaxQuantDAO(params).update_by(slug)
        return asdict(dao.max_quant)

    @endpoint.doc(
        'Deletes a MaxQuant by slug', params={'slug': 'The MaxQuant identifier'}
    )
    @endpoint.response(204, 'Deleted')
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def delete(self, slug):
        MaxQuant.query.filter_by(slug=slug).delete()
        db.session.commit()
        return None, 204

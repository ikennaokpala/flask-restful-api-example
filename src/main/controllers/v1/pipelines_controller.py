from flask_restx import Namespace, Resource, fields
from flask import current_app, request, jsonify
from werkzeug.exceptions import BadRequest
from dataclasses import asdict

from src.main.lib.pipeline_input_builder import PipelineInputBuilder
from src.main.dao.pipeline_dao import PipelineDAO
from src.main.dao.pipelines_dao import PipelinesDAO
from src.main.models.pipeline import Pipeline
from src.main import db

endpoint = Namespace(
    'pipelines-endpoint', description='Pipelines related api endpoints'
)

pipeline_fields = endpoint.model(
    'Pipeline',
    {
        'id': fields.String,
        'name': fields.String,
        'description': fields.String,
        'data_type_slug': fields.String,
        'prototype_slug': fields.String,
    },
)


@endpoint.route('/')
@endpoint.route('')
class Pipelines(Resource):
    @endpoint.doc(
        description='List of a user\'s Pipeline',
        params={
            'page': 'Page or Offset for Pipeline',
            'per_page': 'Number of Pipeline per page',
            'direction': 'Sort desc or asc',
        },
    )
    @endpoint.response(200, 'Success - Pipeline fetched', pipeline_fields)
    @endpoint.response(400, 'Bad Request')
    def get(self):
        pipelines = PipelinesDAO.call(request.args)
        return jsonify(asdict(pipelines))

    @endpoint.doc(
        description='Create a pipeline',
        params={
            'name': 'The name of the pipeline',
            'description': 'The description of the pipeline',
            'data_type': 'The slug of the chosen pipeline data_type',
            'prototype': 'The slug of the chosen pipeline prototype',
        },
    )
    @endpoint.response(
        201,
        'Created',
        endpoint.model(
            'PipelineResponse', {'id': fields.String, 'name': fields.String,},
        ),
    )
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(422, 'Unprocessable Entity')
    def post(self):
        try:
            dao = PipelineDAO(request.json).create()
            return dao.payload, 201
        except (KeyError):
            raise BadRequest


@endpoint.route('/<uuid>')
class APipeline(Resource):
    @endpoint.doc(
        description='Fetch a pipeline by uuid',
        params={'uuid': 'The pipeline identifier'},
    )
    @endpoint.response(200, 'Success', pipeline_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def get(self, uuid):
        return jsonify(
            PipelineInputBuilder.call(Pipeline.query.filter_by(id=uuid).first())
        )

    @endpoint.doc(
        'Deletes a Pipeline by uuid', params={'uuid': 'The Pipeline identifier'}
    )
    @endpoint.response(204, 'Deleted')
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def delete(self, uuid):
        Pipeline.query.filter_by(id=uuid).delete()
        db.session.commit()
        return None, 204

    @endpoint.doc(
        description='Update a pipeline',
        params={
            'name': 'The name of the pipeline',
            'description': 'The description for the pipeline',
            'data_type_slug': 'The data type slug',
            'prototype_slug': 'The prototype slug',
        },
    )
    @endpoint.response(200, 'Success', pipeline_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(422, 'Unprocessable Entity')
    def put(self, uuid):
        dao = PipelineDAO(request.json).update_by(uuid)
        return jsonify(asdict(dao.pipeline))

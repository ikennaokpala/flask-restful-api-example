from flask_restx import Namespace, Resource, fields
from flask import request, session, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from requests.exceptions import HTTPError
from dataclasses import asdict

from app.main.dao.project_dao import ProjectDAO
from app.main.dao.projects_dao import ProjectsDAO
from app.main.models.project import Project
from app.main import db

endpoint = Namespace('projects-endpoint', description='projects related api endpoints')

project_field = endpoint.model('Slug', {'slug': fields.String,},)

project_create = endpoint.model(
    'CreateProject', {'name': fields.String, 'description': fields.String,},
)

project_fields = endpoint.model(
    'Project',
    {
        'name': fields.String,
        'description': fields.String,
        'slug': fields.String,
        'owner': fields.String,
        'collaboarators': fields.List(fields.String),
        'created_at': fields.String,
        'updated_at': fields.String,
        'data_types': fields.List(fields.String),
    },
)

projects_fetch_fields = endpoint.model(
    'ProjectsList',
    {
        'page': fields.Integer,
        'per_page': fields.Integer,
        'total': fields.Integer,
        'projects': fields.List(fields.Nested(project_fields)),
    },
)


@endpoint.route('/<slug>')
class AProject(Resource):
    @endpoint.doc(
        description='Fetch a projects by slug',
        params={'slug': 'The project identifier'},
    )
    @endpoint.response(200, 'Success', project_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def get(self, slug):
        return jsonify(Project.query.filter_by(slug=slug).first())

    @endpoint.doc(
        description='Update a project by slug',
        params={'slug': 'The project identifier'},
    )
    @endpoint.expect(project_fields)
    @endpoint.response(200, 'Success', project_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def put(self, slug):
        dao = ProjectDAO(request.json, session['token_user']['email']).update_by(slug)
        return jsonify({'slug': dao.project.slug})

    @endpoint.doc(
        'Deletes a projects by slug', params={'slug': 'The project identifier'}
    )
    @endpoint.response(204, 'Deleted')
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def delete(self, slug):
        Project.query.filter_by(slug=slug).delete()
        db.session.commit()
        return None, 204


@endpoint.route('/')  # with slash
@endpoint.route('')  # without slash
class Projects(Resource):
    @endpoint.doc(
        description='Create a Project',
        params={'name': 'The project name', 'description': 'The project description'},
    )
    @endpoint.response(201, 'Created', project_field)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def post(self):
        try:
            dao = ProjectDAO(request.json, session['token_user']['email']).create()
            return {'slug': dao.project.slug}, 201
        except (KeyError):
            raise BadRequest

    @endpoint.doc(
        description='List of a user\'s projects',
        params={
            'page': 'Page or Offset for projects',
            'per_page': 'Number of projects per page',
            'direction': 'Sort desc or asc',
        },
    )
    @endpoint.response(200, 'Success - Projects fetched', projects_fetch_fields)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def get(self):
        projects = ProjectsDAO.call(request.args, session['token_user']['email'])
        return jsonify(asdict(projects))

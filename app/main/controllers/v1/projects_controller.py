import openid_connect

from flask_restplus import Namespace, Resource, fields
from flask import request, session, jsonify
from werkzeug.exceptions import UnprocessableEntity
from werkzeug.exceptions import BadRequest
from requests.exceptions import HTTPError

from app.main.dao.project_dao import ProjectDAO
from app.main.models.project import Project

endpoint = Namespace('project-endpoint', description='projects related api endpoints')

project_field = endpoint.model('Resource', {
    'slug': fields.String,
})

project_fields = endpoint.model('Resource', {
    'name': fields.String,
    'description': fields.String,
    'slug': fields.String,
    'email': fields.String,
    'created_at': fields.String,
    'updated_at': fields.String,
})

@endpoint.route('/') # with slash
@endpoint.route('') # without slash
@endpoint.doc(params={'name': 'Name of project', 'description': 'Description of the project'})
class AProject(Resource):
    @endpoint.doc('Create a Project')
    @endpoint.expect(project_field, validate=True)
    def post(self):
        try:
            dao = ProjectDAO(request.json['name'], request.json['description'], session['token_user']['email']).create()
            return { 'slug': dao.project.slug }, 201
        except (KeyError):
            raise BadRequest

@endpoint.route('/') # with slash
@endpoint.route('') # without slash
class Projects(Resource):
    @endpoint.doc('List of a user\'s projects')
    @endpoint.expect(project_fields)
    def get(self):
        return jsonify(Project.query.filter_by(email=session['token_user']['email']).all())

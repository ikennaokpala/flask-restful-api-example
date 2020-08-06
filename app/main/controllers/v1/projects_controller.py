from flask_restplus import Namespace, Resource, fields
from flask import request, session, jsonify
from werkzeug.exceptions import BadRequest
from requests.exceptions import HTTPError

from app.main.dao.project_dao import ProjectDAO
from app.main.dao.projects_dao import ProjectsDAO
from app.main.models.project import Project
from app.main import db

endpoint = Namespace('projects-endpoint', description='projects related api endpoints')

project_field = endpoint.model('Resource', {
    'slug': fields.String,
})

project_fields = endpoint.model('Resource',{
    'page': fields.Integer,
    'per_page': fields.Integer,
    'total': fields.Integer,
    'projects': {
        'name': fields.String,
        'description': fields.String,
        'slug': fields.String,
        'owner': fields.String,
        'collaboarators': fields.List(fields.String),
        'created_at': fields.String,
        'updated_at': fields.String,
    }
})

@endpoint.route('/<slug>')
@endpoint.param('slug', 'The User identifier')
@endpoint.doc(params={'name': 'Name of project', 'description': 'Description of the project'})
class AProject(Resource):
    @endpoint.doc('Fetch a projects by slug')
    @endpoint.expect(model=project_fields)
    def get(self, slug):
        return jsonify(Project.query.filter_by(slug=slug).first())

    @endpoint.doc('Update a projects by slug')
    @endpoint.expect(model=project_field)
    def put(self, slug):
        dao = ProjectDAO(request.json, session['token_user']['email']).update_by(slug)
        return jsonify({ 'slug': dao.project.slug })

    @endpoint.doc('Deletes a projects by slug')
    @endpoint.expect(model=project_field)
    def delete(self, slug):
        Project.query.filter_by(slug=slug).delete()
        db.session.commit()
        return None, 204

@endpoint.route('/') # with slash
@endpoint.route('') # without slash
class Projects(Resource):
    @endpoint.doc('Create a Project')
    @endpoint.expect(model=project_field, validate=True)
    def post(self):
        try:
            dao = ProjectDAO(request.json, session['token_user']['email']).create()
            return { 'slug': dao.project.slug }, 201
        except (KeyError):
            raise BadRequest

    @endpoint.doc('List of a user\'s projects')
    @endpoint.doc(params={'page': 'Page or Offset for projects', 'per_page': 'Number of projects per page', 'direction': 'Sort desc or asc'})
    @endpoint.expect(project_fields)
    def get(self):
        projects = ProjectsDAO.call(request.args, session['token_user']['email'])
        return jsonify(projects._asdict())

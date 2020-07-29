from flask_restplus import Namespace, Resource, fields
from flask import request, abort
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest

from app.main.dao.project_mzxml_file_dao import ProjectMZXmlFileDAO

endpoint = Namespace('project-mzxml-files-endpoint', description='mzXML files belonging to a project api endpoints')

project_mzxmlfile_field = endpoint.model('Resource', {
    'id': fields.Integer,
    'name': fields.String,
    'extension': fields.String,
    'path': fields.String,
    'checksum': fields.String,
    'slug': fields.String,
})

@endpoint.route('/mzxml_file')
@endpoint.route('/mzxml_files')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.doc(params={'mzxml_file_<index>': 'mzxml file object', 'slug': 'The project slug identifier'})
class MZXmlFileProject(Resource):
    @endpoint.doc(description='Associate mzXML file(s) with a project', responses={
        400: 'Bad request',
        404: 'Not Found',
        201: 'File(s) added to project'
    })
    @endpoint.expect(model=project_mzxmlfile_field)
    def put(self, slug):
        try:
            return ProjectMZXmlFileDAO(slug, request.files).upload(), 201
        except (NameError, IndexError):
            abort(400)
        except (NotFound):
            abort(404)

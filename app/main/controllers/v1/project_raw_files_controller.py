from flask_restplus import Namespace, Resource, fields
from flask import request, abort
from werkzeug.exceptions import NotFound
from werkzeug.exceptions import BadRequest

from app.main.dao.project_raw_file_dao import ProjectRawFileDAO

endpoint = Namespace('project-raw-files-endpoint', description='raw files belonging to a project api endpoints')

project_field = endpoint.model('Resource', {
    'raw_file': fields.String,
    'checksum': fields.String,
    'slug': fields.String,
})

@endpoint.route('/raw_file')
@endpoint.route('/raw_files')
@endpoint.param('slug', 'The project slug identifier')
@endpoint.doc(params={'raw_file_<index>': 'Raw file object', 'slug': 'The project slug identifier'})
class RawFileProject(Resource):
    @endpoint.doc('Associate Raw file with a project')
    @endpoint.expect(project_field)
    def put(self, slug):
        try:
            return ProjectRawFileDAO(slug, request.files).upload(), 201
        except (NameError, IndexError):
            abort(400)
        except (NotFound):
            abort(404)

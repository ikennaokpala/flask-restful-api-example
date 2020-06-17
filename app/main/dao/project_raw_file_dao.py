import os

from werkzeug.exceptions import UnprocessableEntity
from werkzeug.exceptions import BadRequest
from flask import current_app
from collections import namedtuple
from hashlib import md5
from pathlib import Path

from app.main.models.project import Project
from app.main.models.raw_file import RawFile
from app.main import db

class ProjectRawFileDAO:
    def __init__(self, slug, raw_file, filename):
        self.slug = slug
        self.raw_file = raw_file
        self.filename = filename
        self.path_to_raw_file = None
        self.file_name_ext = filename.split('.')
        self.file_name = self.file_name_ext[0]
        self.file_extension = self.file_name_ext[1]
        self.project_raw_file = namedtuple('ProjectRawFile', ['path', 'checksum', 'slug'])
        self.raw_files_projects_directory = os.path.join(current_app.config['RAW_FILES_UPLOAD_FOLDER'], 'projects')
        self.allowed_raw_file_extensions = [element.lower() for element in current_app.config['ALLOWED_RAW_FILE_EXTENSIONS']]

    def upload(self):
        self.validate_raw_file()

        project = Project.query.filter_by(slug=self.slug).first_or_404()
        destination = os.path.join(self.raw_files_projects_directory, project.slug)

        checksum = md5(self.filename.encode('utf-8')).hexdigest()
        self.path_to_raw_file = os.path.join(destination, checksum + '_' + self.filename)
        Path(destination).mkdir(parents=True, exist_ok=True)

        self.raw_file.save(self.path_to_raw_file)
        self.raw_file = RawFile(name=self.file_name, extension=self.file_extension, location=self.path_to_raw_file, checksum=checksum, project_id=project.id)
        db.session.add(self.raw_file)
        db.session.commit()

        return self.project_raw_file(path=self.path_to_raw_file, checksum=checksum, slug=self.slug)

    def validate_raw_file(self):
        if self.filename == '': raise BadRequest
        if not ('.' in self.filename and self.file_extension.lower() in self.allowed_raw_file_extensions): raise UnprocessableEntity

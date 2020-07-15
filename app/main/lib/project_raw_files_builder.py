import os

from hashlib import md5
from flask import current_app
from collections import namedtuple
from contextlib import contextmanager

from app.main.models.raw_file import RawFile
from app.main.lib.raw_file_validator import RawFileValidator

class ProjectRawFilesBuilder:
    def __init__(self, project, raw_files, validator=RawFileValidator):
        self.project_raw_files = []
        self.project = project
        self.validator = validator
        self.raw_files = raw_files
        self.raw_files_values = [*raw_files.to_dict().values()]
        self.raw_files_keys = [*raw_files.to_dict().keys()]
        self.raw_files_projects_directory = os.path.join(
            current_app.config['RAW_FILES_UPLOAD_FOLDER'], 'projects')
        self.destination = os.path.join(
            self.raw_files_projects_directory, project.slug)
        self.location = namedtuple('ProjectRawFileLocation', [
                                   'path', 'checksum', 'slug'])
        self.raw_files_key_prefix = current_app.config['RAW_FILES_KEY_PREFIX']
        self.project_raw_file = namedtuple('ProjectRawFile', [
                                           'model', 'location', 'raw_file', 'filename', 'name_extension', 'name', 'extension', 'destination'])

    def map(self):
        for index in range(len(self.raw_files_values)):
            raw_file = self.raw_files[self.raw_files_key_prefix + str(index)]
            file_name = raw_file.filename
            name_extension = file_name.split('.')
            checksum = md5(name_extension[0].encode('utf-8')).hexdigest()
            path_to_raw_file = os.path.join(self.destination, checksum + '_' + file_name)
            model = RawFile(name=name_extension[0], extension=name_extension[1],
                            location=path_to_raw_file, checksum=checksum, project_id=self.project.id)
            location = self.location(
                path=path_to_raw_file, checksum=checksum, slug=self.project.slug)

            project_raw_file = self.project_raw_file(
                model=model,
                location=location,
                raw_file=raw_file,
                filename=file_name,
                name_extension=name_extension,
                name=name_extension[0],
                extension=name_extension[1],
                destination=self.destination
            )
            self.validator(project_raw_file).call()
            self.project_raw_files.append(project_raw_file)

        return self.project_raw_files


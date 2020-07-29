import os

from hashlib import md5
from flask import current_app
from collections import namedtuple
from contextlib import contextmanager

from app.main.models.mzxml_file import MzxmlFile
from app.main.validators.mzxml_file_validator import MzxmlFileValidator

class ProjectMzxmlFilesBuilder:
    def __init__(self, project, mzxml_files, validator=MzxmlFileValidator):
        self.project_mzxml_files = []
        self.project = project
        self.validator = validator
        self.mzxml_files = mzxml_files
        self.mzxml_files_values = [*mzxml_files.to_dict().values()]
        self.mzxml_files_keys = [*mzxml_files.to_dict().keys()]
        self.mzxml_files_projects_directory = os.path.join(
            current_app.config['MZXML_FILES_UPLOAD_FOLDER'], 'projects')
        self.destination = os.path.join(
            self.mzxml_files_projects_directory, project.slug)
        self.location = namedtuple('ProjectMzxmlFileLocation', [
                                    'name', 'extension', 'path', 'checksum', 'slug'])
        self.mzxml_files_key_prefix = current_app.config['MZXML_FILES_KEY_PREFIX']
        self.project_mzxml_file = namedtuple('ProjectMzxmlFile', [
                                           'model', 'location', 'mzxml_file', 'filename', 'name_extension', 'name', 'extension', 'destination'])

    def map(self):
        for index in range(len(self.mzxml_files_values)):
            mzxml_file = self.mzxml_files[self.mzxml_files_key_prefix + str(index)]
            file_name = mzxml_file.filename
            name_extension = file_name.split('.')
            checksum = md5(name_extension[0].encode('utf-8')).hexdigest()
            path_to_mzxml_file = os.path.join(self.destination, checksum + '_' + file_name)
            model = MzxmlFile(name=name_extension[0], extension=name_extension[1],
                            location=path_to_mzxml_file, checksum=checksum, project_id=self.project.id)
            location = self.location(
                name=name_extension[0], extension=name_extension[1], path=path_to_mzxml_file, checksum=checksum, slug=self.project.slug)

            project_mzxml_file = self.project_mzxml_file(
                model=model,
                location=location,
                mzxml_file=mzxml_file,
                filename=file_name,
                name_extension=name_extension,
                name=name_extension[0],
                extension=name_extension[1],
                destination=self.destination
            )
            self.validator(project_mzxml_file).call()
            self.project_mzxml_files.append(project_mzxml_file)

        return self.project_mzxml_files


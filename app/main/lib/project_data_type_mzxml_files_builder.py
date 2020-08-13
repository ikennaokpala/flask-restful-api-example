import os

from hashlib import md5
from flask import current_app
from collections import namedtuple
from contextlib import contextmanager

from app.main.models.mzxml import MZXml
from app.main.validators.mzxml_file_validator import MZXmlValidator

class ProjectDataTypeMZXmlsBuilder:
	def __init__(self, data_type, mzxml_files, validator=MZXmlValidator):
		self.project_mzxml = None
		self.data_type = data_type
		self.project = data_type.project
		self.validator = validator
		self.mzxml_files = mzxml_files
		self.mzxml_files_values = [*mzxml_files.to_dict().values()]
		self.mzxml_files_keys = [*mzxml_files.to_dict().keys()]
		self.mzxml_files_projects_data_type_directory = os.path.join(
			current_app.config['MZXML_FILES_UPLOAD_FOLDER'], 'projects', self.project.slug, 'data_types')
		self.destination = os.path.join(self.mzxml_files_projects_data_type_directory, self.data_type.slug)
		self.location = namedtuple('ProjectDataTypeMZXmlLocation', ['name', 'extension', 'path', 'checksum', 'project_slug', 'data_type_slug'])
		self.mzxml_files_key_prefix = current_app.config['MZXML_FILES_KEY_PREFIX']
		self.project_mzxml_file = namedtuple('ProjectDataTypeMZXml', ['model', 'location', 'mzxml_file', 'filename', 'name_extension', 'name', 'extension', 'destination'])
		self.counter = 0
		self.total = len(self.mzxml_files_values)

	def __iter__(self):
		return self
	
	def __next__(self):
		if self.counter >= self.total: raise StopIteration
		self.next()
		self.counter += 1
		return self.project_mzxml

	def next(self):
		mzxml_file = self.mzxml_files[self.mzxml_files_key_prefix + str(self.counter)]
		file_name = mzxml_file.filename
		name_extension = file_name.split('.')
		checksum = md5(name_extension[0].encode('utf-8')).hexdigest()
		path_to_mzxml_file = os.path.join(self.destination, checksum + '_' + file_name)
		model = MZXml(name=name_extension[0], extension=name_extension[1], location=path_to_mzxml_file, checksum=checksum, data_type_id=self.data_type.id)
		location = self.location(name=name_extension[0], extension=name_extension[1], path=path_to_mzxml_file, checksum=checksum, project_slug=self.project.slug, data_type_slug=self.data_type.slug)

		self.project_mzxml = self.project_mzxml_file(
			model=model,
			location=location,
			mzxml_file=mzxml_file,
			filename=file_name,
			name_extension=name_extension,
			name=name_extension[0],
			extension=name_extension[1],
			destination=self.destination
		)

		self.validator(self.project_mzxml).call()

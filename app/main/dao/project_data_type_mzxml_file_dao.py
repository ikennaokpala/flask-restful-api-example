import os

from collections import namedtuple
from flask import current_app, abort
from pathlib import Path

from app.main import db
from app.main.models.data_type import DataType
from app.main.lib.project_data_type_mzxml_files_builder import ProjectDataTypeMZXmlsBuilder

class ProjectDataTypeMZXmlDAO:
	def __init__(self, slug, mzxml_files, builder=ProjectDataTypeMZXmlsBuilder):
		self.slug = slug
		self.locations = []
		self.builder = builder
		self.mzxml_files = mzxml_files

	def upload(self):
		if len(self.mzxml_files) == 0: abort(400)

		data_type = DataType.query.filter_by(slug=self.slug).first_or_404()

		for project_data_type_mzxml in self.builder(data_type, self.mzxml_files):
			location = project_data_type_mzxml.location

			Path(project_data_type_mzxml.destination).mkdir(parents=True, exist_ok=True)
			project_data_type_mzxml.mzxml_file.save(location.path)

			db.session.add(project_data_type_mzxml.model)
			db.session.commit()

			location = location._asdict()
			location.update({ 'id': project_data_type_mzxml.model.id })

			self.locations.append(location)

		return self.locations

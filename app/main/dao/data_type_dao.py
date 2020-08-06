from werkzeug.exceptions import UnprocessableEntity
from app.main.models.data_type import DataType
from app.main.models.project import Project
from app.main.lib.slugifier import Slugifier
from app.main import db

class DataTypeDAO:
	def __init__(self, params, slug):
		self.name = params['name']
		self.description = params.get('description', None)
		self.slug = slug
		self.data_type = None

	def create(self):
		project = Project.query.filter_by(slug=self.slug).first_or_404()

		self.data_type = DataType(name=self.name, description=self.description, project_id=project.id)

		db.session.add(self.data_type)
		db.session.commit()

		return self

	def update_by(self):
		try:
			self.data_type = DataType.query.filter_by(slug=self.slug).first()
			self.data_type.name = self.name
			self.data_type.description = self.description
			self.data_type.slug = self.slug = Slugifier(self.data_type, self.name).call()

			db.session.flush()
			db.session.commit()

			return self
		except:
			raise UnprocessableEntity

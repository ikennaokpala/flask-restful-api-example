from sqlalchemy import or_

from app.main.models.project import Project
from app.main import db

class ProjectsDAO:
	def __init__(self, owner):
		self.owner = owner

	def fetch(self):
		return Project.query \
			.filter(
				or_(
					Project.owner == self.owner,
					Project.collaborators.any(self.owner)
				)
			).all()

from collections import namedtuple
from sqlalchemy import or_, desc, asc
from flask import current_app

from app.main.models.project import Project
from app.main import db

class ProjectsDAO:
	@classmethod
	def call(klazz, params, owner):
		return klazz(params, owner).fetch()

	@staticmethod
	def projects_decorator(callable):
		projects_info = namedtuple('ProjectsInfo', ['page', 'per_page', 'total', 'projects'])

		def wrapper(*args, **kwargs):
			projects = callable(*args, **kwargs).__dict__

			return projects.pop('query') \
				and projects_info(
					page=projects.get('page'), 
					per_page=projects.get('per_page'), 
					total=projects.get('total'),
					projects=projects.get('items'))

		return wrapper

	def __init__(self, params, owner):
		self.owner = owner
		self.error_out = False
		self.page = int(params.get('page', 1))
		self.per_page = int(params.get('per_page', 25))
		self.direction = params.get('direction', 'desc')
		self.max_per_page = int(current_app.config['PAGINATION_MAX_PER_PAGE'])

	@projects_decorator.__func__ # accessing the underlying static projects_decorator method directly with the __func__ attribute else staticmethod isn't callable
	def fetch(self):
		return Project.query \
			.filter(
				or_(
					Project.owner == self.owner,
					Project.collaborators.any(self.owner)
				)
			) \
			.order_by(self.ranker()) \
			.paginate(self.page, self.per_page, self.error_out, self.max_per_page)

	def ranker(self):
		if self.direction == 'asc': return asc(Project.created_at)
		return desc(Project.created_at)

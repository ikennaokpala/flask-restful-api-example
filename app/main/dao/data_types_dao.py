from collections import namedtuple
from sqlalchemy import or_, desc, asc
from flask import current_app

from app.main.models.data_type import DataType
from app.main.models.project import Project
from app.main import db

class DataTypesDAO:
	@classmethod
	def call(klazz, params, slug):
		return klazz(params, slug).fetch()

	@staticmethod
	def data_types_decorator(callable):
		data_types_info = namedtuple('DataTypesInfo', ['page', 'per_page', 'total', 'data_types'])

		def wrapper(*args, **kwargs):
			data_types = callable(*args, **kwargs).__dict__

			return data_types.pop('query') \
				and data_types_info(
					page=data_types.get('page'), 
					per_page=data_types.get('per_page'), 
					total=data_types.get('total'),
					data_types=data_types.get('items'))

		return wrapper

	def __init__(self, params, slug):
		self.slug = slug
		self.error_out = False
		self.page = int(params.get('page', 1))
		self.per_page = int(params.get('per_page', 25))
		self.direction = params.get('direction', 'desc')
		self.max_per_page = int(current_app.config['PAGINATION_MAX_PER_PAGE'])

	@data_types_decorator.__func__ # accessing the underlying static data_types_decorator method directly with the __func__ attribute else staticmethod isn't callable
	def fetch(self):
		return db.session.query(
				DataType
			).join(Project) \
			.filter(Project.slug == self.slug) \
			.order_by(self.ranker()) \
			.paginate(self.page, self.per_page, self.error_out, self.max_per_page)

	def ranker(self):
		if self.direction == 'asc': return asc(DataType.created_at)
		return desc(DataType.created_at)

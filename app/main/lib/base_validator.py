from flask import current_app
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import UnprocessableEntity

class BaseValidator:
	def __init__(self, derived_file_object, allowed_file_extensions=[]):
		self.derived_file_object = derived_file_object
		self.allowed_file_extensions = [element.lower() for element in allowed_file_extensions]

	def call(self):
		if self.derived_file_object.name == '': raise BadRequest
		if not ('.' in self.derived_file_object.filename and self.derived_file_object.extension.lower() in self.allowed_file_extensions):
				raise UnprocessableEntity

from flask import current_app
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import UnprocessableEntity

class DataFormatFileValidator:
	def __init__(self, data_format_file_object, allowed_data_formats = None):
		self.data_format_file_object = data_format_file_object
		self.data_format_file_extension = [element.lower() for element in (allowed_data_formats or current_app.config['DATA_FORMAT_FILE_EXTENSIONS'])]

	def call(self):
		if self.data_format_file_object.name == '': raise BadRequest
		if not ('.' in self.data_format_file_object.filename and self.data_format_file_object.extension.lower() in self.data_format_file_extension):
				raise UnprocessableEntity

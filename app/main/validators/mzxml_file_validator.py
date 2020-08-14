from flask import current_app

from app.main.validators.data_format_file_validator import DataFormatFileValidator

class MZXmlValidator(DataFormatFileValidator):
	def __init__(self, mzxml_file, allowed_data_formats = None):
		super().__init__(mzxml_file, allowed_data_formats)

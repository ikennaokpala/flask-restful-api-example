from flask import current_app

from app.main.validators.base_file_validator import BaseFileValidator

class MZXmlFileValidator(BaseFileValidator):
	def __init__(self, mzxml_file):
		super().__init__(mzxml_file, current_app.config['ALLOWED_MZXML_FILE_EXTENSIONS'])

from flask import current_app

from app.main.validators.base_file_validator import BaseFileValidator

class RawFileValidator(BaseFileValidator):
	def __init__(self, raw_file):
		super().__init__(raw_file, current_app.config['ALLOWED_RAW_FILE_EXTENSIONS'])
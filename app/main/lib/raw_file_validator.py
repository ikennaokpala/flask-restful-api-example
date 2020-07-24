from flask import current_app

from app.main.lib.base_validator import BaseValidator

class RawFileValidator(BaseValidator):
	def __init__(self, raw_file):
		super().__init__(raw_file, current_app.config['ALLOWED_RAW_FILE_EXTENSIONS'])
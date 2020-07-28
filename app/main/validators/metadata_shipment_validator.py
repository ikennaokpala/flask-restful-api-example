from flask import current_app

from app.main.validators.base_file_validator import BaseFileValidator

class MetadataShipmentValidator(BaseFileValidator):
	def __init__(self, metadata_shipments_file):
		super().__init__(metadata_shipments_file, current_app.config['ALLOWED_METADATA_SHIPMENTS_EXTENSIONS'])

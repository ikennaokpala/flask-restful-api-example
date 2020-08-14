from flask import current_app

from app.main.validators.data_format_file_validator import DataFormatFileValidator

class MetadataShipmentValidator(DataFormatFileValidator):
	def __init__(self, metadata_shipments_file, allowed_data_formats = None):
		super().__init__(metadata_shipments_file, allowed_data_formats)

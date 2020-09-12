from flask import current_app
from werkzeug.exceptions import UnprocessableEntity

from src.main.validators.data_format_file_validator import DataFormatFileValidator


class MetadataShipmentValidator(DataFormatFileValidator):
    def __init__(self, metadata_shipments_file, columns=[], allowed_data_formats=None):
        self.columns = columns
        super().__init__(metadata_shipments_file, allowed_data_formats)

    def call(self):
        super().call()
        if self.columns != current_app.config.get('METADATA_SHIPMENTS_FILE_COLUMNS'):
            raise UnprocessableEntity

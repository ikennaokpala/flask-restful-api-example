from flask import current_app

from src.main.validators.data_format_file_validator import DataFormatFileValidator


class MaxQuantFilesValidator(DataFormatFileValidator):
    def __init__(self, max_quant_file, allowed_data_formats=None):
        super().__init__(
            max_quant_file,
            allowed_data_formats or current_app.config['MAXQUANT_FILE_EXTENSIONS'],
        )

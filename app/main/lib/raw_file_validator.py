from flask import current_app
from werkzeug.exceptions import BadRequest
from werkzeug.exceptions import UnprocessableEntity

class RawFileValidator:
    def __init__(self, raw_file):
        self.raw_file = raw_file
        self.allowed_raw_file_extensions = [
            element.lower() for element in current_app.config['ALLOWED_RAW_FILE_EXTENSIONS']]

    def call(self):
        if self.raw_file.name == '': raise BadRequest
        if not ('.' in self.raw_file.filename and self.raw_file.extension.lower() in self.allowed_raw_file_extensions):
            raise UnprocessableEntity

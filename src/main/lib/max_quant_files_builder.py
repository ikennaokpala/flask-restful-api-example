import os

from hashlib import md5
from pathlib import Path
from flask import current_app
from dataclasses import make_dataclass

from src.main.validators.max_quant_files_validator import MaxQuantFilesValidator

TempFile = make_dataclass('TempFile', ['file', 'filename', 'name', 'extension'])


class MaxQuantFilesBuilder:
    @classmethod
    def call(klazz, max_quant, fasta_file, max_quant_file):
        return klazz(max_quant, fasta_file, max_quant_file).run()

    def __init__(
        self, max_quant, fasta_file, max_quant_file, validator=MaxQuantFilesValidator
    ):
        self.max_quant_file = TempFile(
            max_quant_file,
            max_quant_file.filename,
            max_quant_file.filename.split('.')[0],
            max_quant_file.filename.split('.')[-1],
        )
        self.fasta_file = TempFile(
            fasta_file,
            fasta_file.filename,
            fasta_file.filename.split('.')[0],
            fasta_file.filename.split('.')[-1],
        )
        self.validator = validator
        self.destination = os.path.join(
            current_app.config['PROTOTYPE_FILES_UPLOAD_FOLDER'],
            'max_quants',
            max_quant.slug,
        )

    def run(self):
        self.validator(self.max_quant_file).call()
        self.validator(self.fasta_file).call()

        Path(self.destination).mkdir(parents=True, exist_ok=True)

        return {
            'fasta_file': self.__fasta_file(),
            'max_quant_file': self.__max_quant_file(),
        }

    def __max_quant_file(self):
        return {
            'name': self.max_quant_file.name,
            'extension': self.max_quant_file.extension,
            'content': self.max_quant_file.file.stream.read().decode('utf-8'),
        }

    def __fasta_file(self):
        checksum = md5(self.fasta_file.name.encode('utf-8')).hexdigest()
        path_to_mzxml_file = os.path.join(
            self.destination, checksum + '_' + self.fasta_file.filename
        )

        self.fasta_file.file.save(path_to_mzxml_file)

        return {
            'name': self.fasta_file.name,
            'extension': self.fasta_file.extension,
            'path': path_to_mzxml_file,
            'checksum': checksum,
        }

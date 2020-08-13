import datetime

from dataclasses import dataclass

from app.main.models.data_format import DataFormat
from app.main import db

@dataclass
class MZXml(DataFormat):
	MNEMONIC = 'mzxmls'

	location: str
	checksum: str

	location = db.Column(db.TEXT)
	checksum = db.Column(db.String)

	__mapper_args__ = {
		'polymorphic_identity': 'MZXml'
	}

	@classmethod
	def compose(klazz, info, data_type_id):
		return klazz(name=info.name, extension=info.extension, location=info.path, checksum=info.checksum, data_type_id=data_type_id)
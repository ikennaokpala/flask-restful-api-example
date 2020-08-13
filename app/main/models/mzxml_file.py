import datetime

from dataclasses import dataclass

from app.main.models.data_format import DataFormat
from app.main import db

@dataclass
class MZXmlFile(DataFormat):
	location: str
	checksum: str

	location = db.Column(db.TEXT)
	checksum = db.Column(db.String)

	__mapper_args__ = {
		'polymorphic_identity': 'mzxml'
	}

import datetime

from dataclasses import dataclass

from app.main.models.data_format import DataFormat
from app.main import db

@dataclass
class MZXml(DataFormat):
	location: str
	checksum: str

	location = db.Column(db.TEXT)
	checksum = db.Column(db.String)
	data_type = db.relationship('DataType', back_populates='mzxmls')

	__mapper_args__ = {
		'polymorphic_identity': 'MZXml'
	}

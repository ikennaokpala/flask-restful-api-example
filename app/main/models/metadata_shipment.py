import datetime

from app.main import db

from dataclasses import dataclass
from sqlalchemy.dialects import postgresql as pg


@dataclass
class MetadataShipment(db.Model):
	EXCEL_FILE_COLUMNS = ['DATE shipped', 'MATRIX_BOX', 'MATRIX_LOCN', 'ORGM', 'ISOLATE_NBR']
	__tablename__ = 'metadata_shipments'

	id: int
	file_name: str
	extension: str
	mzxml_file_id: str
	content: dict

	id = db.Column(db.Integer, primary_key=True)
	file_name = db.Column(db.TEXT, index=True, nullable=False)
	extension = db.Column(db.String, nullable=False)
	mzxml_file_id = db.Column(db.Integer, db.ForeignKey('mzxml_files.id'), index=True, nullable=False)
	mzxml_file = db.relationship('MZXmlFile', back_populates='metadata_shipments', lazy='joined')
	content = db.Column(pg.JSON, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

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
	data_type_id: int
	content: dict

	id = db.Column(db.Integer, primary_key=True)
	file_name = db.Column(db.TEXT, index=True, nullable=False)
	extension = db.Column(db.String, nullable=False)
	data_type_id = db.Column(db.Integer, db.ForeignKey('data_types.id'), index=True, nullable=False)
	data_type = db.relationship('DataType', back_populates='metadata_shipments')
	content = db.Column(pg.JSON, nullable=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, index=True)

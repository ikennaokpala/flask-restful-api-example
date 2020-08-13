import datetime

from dataclasses import dataclass, field
from sqlalchemy import orm, types

from app.main import db

@dataclass
class DataFormat(db.Model):
	__tablename__ = 'data_formats'

	id: int
	name: str
	extension: str
	type: str
	data_type_slug: str = field(init=False)

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.TEXT, index=True, nullable=False)
	extension = db.Column(db.String, index=True, nullable=False)
	type = db.Column(db.String)
	data_type_id = db.Column(db.Integer, db.ForeignKey('data_types.id'), index=True, nullable=False)
	data_type = db.relationship('DataType')
	created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, index=True)

	@property
	def data_type_slug(self) -> str:
		return self.data_type.slug

	__mapper_args__ = {
		'polymorphic_on': type,
		'polymorphic_identity': 'DataFormat'
	}



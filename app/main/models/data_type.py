import datetime

from dataclasses import dataclass

from app.main.lib.slugifier import Slugifier
from app.main import db

@dataclass
class DataType(db.Model):
	__tablename__ = 'data_types'

	id: int
	name: str
	slug: str
	description: str
	project_slug: str
	mzxmls: list
	metadata_shipments: list

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, index=True, nullable=False)
	description = db.Column(db.TEXT)
	slug = db.Column(db.TEXT, index=True, unique=True, nullable=False)
	project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), index=True, nullable=False)
	project = db.relationship('Project', back_populates='data_types')
	mzxmls = db.relationship('MZXml', cascade='all,delete', backref='data_types', lazy='joined')
	metadata_shipments = db.relationship('MetadataShipment', cascade='all,delete', backref='data_types', lazy='joined')
	created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, index=True)

	def __init__(self, *args, **kwargs):
		super(DataType, self).__init__(*args, **kwargs)
		self.slug = Slugifier(self, self.name).call()

	@property
	def project_slug(self) -> str:
		return self.project.slug

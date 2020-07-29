import datetime

from dataclasses import dataclass
from app.main import db

@dataclass
class MZXmlFile(db.Model):
    __tablename__ = 'mzxml_files'

    id: int
    name: str
    extension: str
    location: str
    checksum: str
    project_id: str
    metadata_shipments: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT, index=True, nullable=False)
    extension = db.Column(db.String, index=True, nullable=False)
    location = db.Column(db.TEXT, index=True, nullable=False)
    checksum = db.Column(db.String, index=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', back_populates='mzxml_files')
    metadata_shipments = db.relationship('MetadataShipment', cascade='all,delete', lazy='joined')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

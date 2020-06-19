import datetime

from dataclasses import dataclass
from app.main import db

@dataclass
class RawFile(db.Model):
    __tablename__ = 'raw_files'

    name: str
    extension: str
    location: str
    checksum: str
    project_id: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT, index=True, nullable=False)
    extension = db.Column(db.String, index=True, nullable=False)
    location = db.Column(db.TEXT, index=True, nullable=False)
    checksum = db.Column(db.String, index=True, nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    project = db.relationship('Project', back_populates='raw_files')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

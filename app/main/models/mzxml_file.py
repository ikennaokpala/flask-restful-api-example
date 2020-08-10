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
    data_type_id: int

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT, index=True, nullable=False)
    extension = db.Column(db.String, index=True, nullable=False)
    location = db.Column(db.TEXT, index=True, nullable=False)
    checksum = db.Column(db.String, index=True, nullable=False)
    data_type_id = db.Column(db.Integer, db.ForeignKey('data_types.id'), index=True, nullable=False)
    data_type = db.relationship('DataType', back_populates='mzxml_files')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

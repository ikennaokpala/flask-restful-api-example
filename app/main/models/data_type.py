import datetime

from sqlalchemy.dialects import postgresql as pg
from dataclasses import dataclass

from app.main import db


@dataclass
class DataType(db.Model):
    __tablename__ = 'data_types'

    name: str
    slug: str
    description: str
    project_slug: str
    data_formats: list
    mzxml_files: list
    metadata_shipment_files: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.TEXT)
    slug = db.Column(db.TEXT, index=True, unique=True, nullable=False)
    project_id = db.Column(
        db.Integer, db.ForeignKey('projects.id'), index=True, nullable=False
    )
    project = db.relationship('Project', back_populates='data_types')
    data_formats = db.Column(pg.ARRAY(db.String))
    data_format_files = db.relationship(
        'DataFormatFile', cascade='all,delete-orphan', lazy='joined'
    )
    mzxml_files = db.relationship(
        'MZXmlFile', cascade='all,delete-orphan', backref='data_types', lazy='joined'
    )
    metadata_shipment_files = db.relationship(
        'MetadataShipmentFile',
        cascade='all,delete-orphan',
        backref='data_types',
        lazy='joined',
    )
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        index=True,
    )

    @property
    def project_slug(self) -> str:
        return self.project.slug

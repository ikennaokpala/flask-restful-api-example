import datetime

from sqlalchemy.dialects import postgresql as pg
from dataclasses import dataclass

from src.main import db


@dataclass
class Project(db.Model):
    __tablename__ = 'projects'

    name: str
    description: str
    slug: str
    owner: str
    collaborators: list
    data_types: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.TEXT)
    slug = db.Column(db.TEXT, index=True, unique=True, nullable=False)
    owner = db.Column(db.String, index=True, nullable=False)
    collaborators = db.Column(pg.ARRAY(db.String))
    data_types = db.relationship(
        'DataType', cascade='all,delete-orphan', backref='projects', lazy='joined'
    )
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        index=True,
    )

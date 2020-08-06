import re
import unidecode
import datetime

from sqlalchemy.dialects import postgresql as pg
from dataclasses import dataclass

from app.main.lib.slugifier import Slugifier
from app.main import db

@dataclass
class Project(db.Model):
    __tablename__ = 'projects'

    id: int
    name: str
    description: str
    slug: str
    owner: str
    collaborators: list
    mzxml_files: list

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.TEXT)
    slug = db.Column(db.TEXT, index=True, unique=True, nullable=False)
    owner = db.Column(db.String, index=True, nullable=False)
    collaborators = db.Column(pg.ARRAY(db.String))
    data_types = db.relationship('DataType', cascade='all,delete', backref='projects', lazy='joined')
    mzxml_files = db.relationship('MZXmlFile', cascade='all,delete', backref='projects', lazy='joined')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.slug = Slugifier(self, self.name).call()

import re
import unidecode
import datetime

from dataclasses import dataclass
from app.main import db

@dataclass
class Project(db.Model):
    __tablename__ = 'projects'

    name: str
    description: str
    slug: str
    owner: str

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    description = db.Column(db.TEXT)
    slug = db.Column(db.TEXT, index=True)
    owner = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)

    def __init__(self, *args, **kwargs):
        super(Project, self).__init__(*args, **kwargs)
        self.slug = self.slugify(self.name)

    def slugify(self, name):
        return re.sub(r'[\W_]+', '-', unidecode.unidecode(name).lower())

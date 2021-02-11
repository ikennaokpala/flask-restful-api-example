import datetime

from dataclasses import dataclass
from sqlalchemy.dialects import postgresql as pg

from src.main import db


@dataclass
class Prototype(db.Model):
    __tablename__ = 'prototypes'

    name: str
    description: str
    type: str
    slug: str
    content: dict

    def __init__(self, *args, **kwargs):
        super(Prototype, self).__init__(*args, **kwargs)
        self.type = 'Prototype'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT, unique=True, nullable=False)
    description = db.Column(db.TEXT, nullable=True)
    type = db.Column(db.String, index=True, nullable=False)
    slug = db.Column(db.TEXT, index=True, unique=True, nullable=False)
    content = db.Column(pg.JSON, nullable=True, default={})
    pipelines = db.relationship(
        'Pipeline', cascade='all,delete-orphan', backref='prototypes', lazy='joined'
    )
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        index=True,
    )

    __mapper_args__ = {
        'polymorphic_on': type,
        'polymorphic_identity': 'Prototype',
    }

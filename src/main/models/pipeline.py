import uuid
import datetime

from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.dialects.postgresql import UUID
from dataclasses import dataclass, field
from src.main import db


@dataclass
class Pipeline(db.Model):
    __tablename__ = 'pipelines'

    id: str
    name: str
    description: str
    data_type_slug: str = field(init=False)
    prototype_slug: str = field(init=False)

    id = db.Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True
    )
    name = db.Column(db.String, index=True, nullable=False)
    description = db.Column(db.TEXT, nullable=True)
    data_type_id = db.Column(
        db.Integer,
        db.ForeignKey('data_types.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    data_type = db.relationship('DataType', back_populates='pipelines')
    prototype_id = db.Column(
        db.Integer,
        db.ForeignKey('prototypes.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    prototype = db.relationship('Prototype', back_populates='pipelines')
    created_at = db.Column(db.DateTime, default=datetime.datetime.now, index=True)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.datetime.now,
        onupdate=datetime.datetime.now,
        index=True,
    )

    @property
    def data_type_slug(self) -> str:
        return self.data_type.slug

    @property
    def prototype_slug(self) -> str:
        return self.prototype.slug

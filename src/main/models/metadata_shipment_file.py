import datetime

from src.main.models.data_format_file import DataFormatFile
from src.main import db

from dataclasses import dataclass, field
from sqlalchemy.dialects import postgresql as pg


@dataclass
class MetadataShipmentFile(DataFormatFile):
    MNEMONIC = 'metadata_shipments'

    content: dict

    content = db.Column(pg.JSON, nullable=False, default={})

    __mapper_args__ = {'polymorphic_identity': 'MetadataShipment'}

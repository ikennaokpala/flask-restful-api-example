import datetime

from app.main.models.data_format import DataFormat
from app.main import db

from dataclasses import dataclass, field
from sqlalchemy.dialects import postgresql as pg


@dataclass
class MetadataShipment(DataFormat):
	EXCEL_FILE_COLUMNS = ['DATE shipped', 'MATRIX_BOX', 'MATRIX_LOCN', 'ORGM', 'ISOLATE_NBR']

	content: dict

	content = db.Column(pg.JSON, nullable=False, default={})

	__mapper_args__ = {
		'polymorphic_identity': 'metadata_shipment'
	}

from flask import abort
from dataclasses import asdict

from app.main.lib.metadata_shipment_file_content_extractor import MetadataShipmentFileContentExtractor
from app.main.models.metadata_shipment_file import MetadataShipmentFile
from app.main.models.data_type import DataType
from app.main import db

class DataTypeMetadataShipmentFilesDAO:
	def __init__(self, data_type_slug, metadata_shipment_files, file_content_extractor=MetadataShipmentFileContentExtractor):
		self.shipments = []
		self.data_type_slug = data_type_slug
		self.file_content_extractor = file_content_extractor
		self.metadata_shipment_files = [*metadata_shipment_files.to_dict().values()]

	def upload(self):
		if len(self.metadata_shipment_files) == 0: abort(400)

		data_type = DataType.query.filter_by(slug=self.data_type_slug).first_or_404()

		for file_detail in self.file_content_extractor.call(self.metadata_shipment_files, data_type):
			metadata_shipment_file = MetadataShipmentFile(name=file_detail.name, extension=file_detail.extension, data_type_id=data_type.id, content=file_detail.content)

			db.session.add(metadata_shipment_file)
			db.session.commit()

			self.shipments.append(asdict(metadata_shipment_file))

		return self.shipments

from flask import abort
from dataclasses import asdict

from app.main.lib.metadata_shipment_file_content_extractor import MetadataShipmentFileContentExtractor
from app.main.models.metadata_shipment import MetadataShipment
from app.main.models.raw_file import RawFile
from app.main import db

class RawFileMetadataShipmentDAO:
	def __init__(self, raw_file_id, metadata_shipment_files, file_content_extractor=MetadataShipmentFileContentExtractor):
		self.shipments = []
		self.raw_file_id = raw_file_id
		self.file_content_extractor = file_content_extractor
		self.metadata_shipment_files = [*metadata_shipment_files.to_dict().values()]

	def upload(self):
		if len(self.metadata_shipment_files) == 0: abort(400)

		raw_file = RawFile.query.filter_by(id=self.raw_file_id).first_or_404()

		for raw_file_metadata_shipment_file in self.metadata_shipment_files:
			file_content = self.file_content_extractor(raw_file_metadata_shipment_file).call()
			file_detail = file_content.detail
			metadata_shipment = MetadataShipment(
				file_name=file_detail.name, extension=file_detail.extension, raw_file_id=raw_file.id, content=file_content.content)

			db.session.add(metadata_shipment)
			db.session.commit()

			self.shipments.append(asdict(metadata_shipment))

		return self.shipments

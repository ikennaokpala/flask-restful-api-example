from flask import abort
from dataclasses import asdict

from app.main.lib.metadata_shipment_file_content_extractor import MetadataShipmentFileContentExtractor
from app.main.models.metadata_shipment import MetadataShipment
from app.main.models.mzxml_file import MZXmlFile
from app.main import db

class MZXmlFileMetadataShipmentDAO:
	def __init__(self, mzxml_file_id, metadata_shipment_files, file_content_extractor=MetadataShipmentFileContentExtractor):
		self.shipments = []
		self.mzxml_file_id = mzxml_file_id
		self.file_content_extractor = file_content_extractor
		self.metadata_shipment_files = [*metadata_shipment_files.to_dict().values()]

	def upload(self):
		if len(self.metadata_shipment_files) == 0: abort(400)

		mzxml_file = MZXmlFile.query.filter_by(id=self.mzxml_file_id).first_or_404()

		for mzxml_file_metadata_shipment_file in self.metadata_shipment_files:
			file_content = self.file_content_extractor(mzxml_file_metadata_shipment_file).call()
			file_detail = file_content.detail
			metadata_shipment = MetadataShipment(
				file_name=file_detail.name, extension=file_detail.extension, mzxml_file_id=mzxml_file.id, content=file_content.content)

			db.session.add(metadata_shipment)
			db.session.commit()

			self.shipments.append(asdict(metadata_shipment))

		return self.shipments

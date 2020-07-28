import pandas as pd

from collections import namedtuple

from app.main.models.metadata_shipment import MetadataShipment
from app.main.validators.metadata_shipment_validator import MetadataShipmentValidator

class MetadataShipmentFileContentExtractor:
	def __init__(self, metdata_shipment_file, validator=MetadataShipmentValidator):
		self.file_detail = namedtuple('FileDetail', ['name', 'extension', 'filename'])
		self.file_content = namedtuple('FileContent', ['detail', 'content'])
		self.metdata_shipment_file = metdata_shipment_file
		self.file_name = metdata_shipment_file.filename
		name_extension = self.file_name.split('.')
		self.extension = name_extension[1]
		self.filename = name_extension[0]
		self.columns = MetadataShipment.EXCEL_FILE_COLUMNS
		self.current = {}
		self.current_child = {}
		self.validator = validator

	def call(self):
		file_detail = self.file_detail(name=self.filename, extension=self.extension, filename=self.file_name)
		self.validator(file_detail).call()

		metdata_shipments = pd.read_excel(self.metdata_shipment_file)
		groups = metdata_shipments.groupby(self.columns[0])

		for parent_child_node, _collection in groups:
			parent_node_key = str(parent_child_node)
			if self.valid_new_parent_node(parent_child_node, parent_node_key): self.current[parent_node_key] = []

			for _index, row in metdata_shipments.iterrows():
				child_node_key = str(row[self.columns[1]])
				if self.valid_new_child_node(child_node_key): self.current_child[child_node_key] = []
				self.current_child[child_node_key].append([*row.values[-3:]]) 

			self.current[parent_node_key].append(self.current_child)

		return self.file_content(detail=file_detail, content=self.current)

	def	valid_new_parent_node(self, node, node_key):
		try:
			return type(node) is pd.Timestamp and [*self.current.keys()][-1] != node_key
		except(IndexError):
			return True

	def	valid_new_child_node(self, node_key):
		try:
			return [*self.current_child.keys()][-1] != node_key
		except(IndexError):
			return True
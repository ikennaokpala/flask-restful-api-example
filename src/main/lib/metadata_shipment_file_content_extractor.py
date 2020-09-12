import pandas as pd

from dataclasses import make_dataclass

from src.main.models.metadata_shipment_file import MetadataShipmentFile
from src.main.validators.metadata_shipment_validator import MetadataShipmentValidator


class MetadataShipmentFileContentExtractor:
    @classmethod
    def call(klazz, metdata_shipment_files, data_type):
        for metdata_shipment_file in metdata_shipment_files:
            yield klazz(metdata_shipment_file, data_type).each()

    def __init__(
        self, metdata_shipment_file, data_type, validator=MetadataShipmentValidator
    ):
        self.file_detail = make_dataclass(
            'FileDetail', ['name', 'extension', 'filename', 'content']
        )
        self.metdata_shipment_file = metdata_shipment_file
        self.file_name = metdata_shipment_file.filename
        name_extension = self.file_name.split('.')
        self.extension = name_extension[-1]
        self.filename = name_extension[0]
        self.columns = None
        self.current = {}
        self.current_child = {}
        self.validator = validator
        self.data_type = data_type

    def each(self):
        file_detail = self.file_detail(
            name=self.filename,
            extension=self.extension,
            filename=self.file_name,
            content={},
        )
        metdata_shipments = pd.read_excel(self.metdata_shipment_file)
        self.columns = list(metdata_shipments.columns)
        self.validator(file_detail, self.columns, self.data_type.data_formats).call()

        groups = metdata_shipments.groupby(self.columns[0])

        for parent_child_node, _collection in groups:
            parent_node_key = str(parent_child_node)
            if self.valid_new_parent_node(parent_child_node, parent_node_key):
                self.current[parent_node_key] = []

            for _, row in metdata_shipments.iterrows():
                child_node_key = str(row[self.columns[1]])
                if self.valid_new_child_node(child_node_key):
                    self.current_child[child_node_key] = []
                self.current_child[child_node_key].append([*row.values[-3:]])

            self.current[parent_node_key].append(self.current_child)
            file_detail.content = {'columns': self.columns, 'rows': self.current}
        return file_detail

    def valid_new_parent_node(self, node, node_key):
        try:
            return type(node) is pd.Timestamp and [*self.current.keys()][-1] != node_key
        except (IndexError):
            return True

    def valid_new_child_node(self, node_key):
        try:
            return [*self.current_child.keys()][-1] != node_key
        except (IndexError):
            return True

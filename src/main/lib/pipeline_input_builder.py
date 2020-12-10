from dataclasses import asdict
import xml.etree.ElementTree as ET


class PipelineInputBuilder:
    @classmethod
    def call(klazz, pipeline):
        return klazz(pipeline).render()

    def __init__(self, pipeline):
        self.pipeline = pipeline
        self.raw_file_paths = list(
            map(
                lambda mzxml_file: mzxml_file.location,
                self.pipeline.data_type.mzxml_files,
            )
        )

    def render(self):

        return {
            'id': str(self.pipeline.id),
            'name': self.pipeline.name,
            'description': self.pipeline.description,
            'project': {
                'name': self.pipeline.data_type.project.name,
                'description': self.pipeline.data_type.project.description,
                'slug': self.pipeline.data_type.project.slug,
                'data_type': {
                    'name': self.pipeline.data_type.name,
                    'description': self.pipeline.data_type.description,
                    'slug': self.pipeline.data_type.slug,
                    'raw_files': self.raw_file_paths,
                },
            },
            'prototype': self.__compose_prototype(),
        }

    def __compose_prototype(self):
        prototype = self.pipeline.prototype
        document = ET.fromstring(prototype.content['max_quant_file']['content'])
        document.findall('./fastaFiles/FastaFileInfo[1]/fastaFilePath')[
            0
        ].text = prototype.content['fasta_file']['path']

        for raw_file_path in self.raw_file_paths:
            raw_file_tag = ET.Element('string')
            raw_file_tag.text = raw_file_path
            document.findall('./filePaths')[0].append(raw_file_tag)

        return {
            'name': prototype.name,
            'slug': prototype.slug,
            'type': prototype.type,
            'content': ET.tostring(document).decode('utf-8'),
        }

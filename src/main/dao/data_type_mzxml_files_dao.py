import os

from dataclasses import make_dataclass, asdict
from flask import current_app, abort
from pathlib import Path

from src.main import db
from src.main.models.mzxml_file import MZXmlFile
from src.main.models.data_type import DataType
from src.main.lib.mzxml_files_info_builder import MZXmlFilesInfoBuilder


class DataTypeMZXmlFilesDAO:
    def __init__(self, slug, mzxml_files, builder=MZXmlFilesInfoBuilder):
        self.slug = slug
        self.locations = []
        self.builder = builder
        self.mzxml_files = mzxml_files

    def upload(self):
        if len(self.mzxml_files) == 0:
            abort(400)

        data_type = DataType.query.filter_by(slug=self.slug).first_or_404()

        for info in self.builder(data_type, self.mzxml_files):
            Path(info.destination).mkdir(parents=True, exist_ok=True)
            info.mzxml_file.save(info.path)
            model = MZXmlFile.compose(info, data_type.id)

            db.session.add(model)
            db.session.commit()

            self.locations.append(
                {
                    'id': model.id,
                    'name': info.name,
                    'extension': info.extension,
                    'path': info.path,
                    'checksum': info.checksum,
                    'project_slug': data_type.project.slug,
                    'data_type_slug': data_type.slug,
                }
            )

        return self.locations

from flask import current_app
from werkzeug.exceptions import UnprocessableEntity

from app.main.models.data_type import DataType
from app.main.models.project import Project
from app.main import db


class DataTypeDAO:
    DEFAULT_DATA_FORMATS = ['mzXML', 'xlsx', 'csv']

    def __init__(self, params, slug):
        self.name = params['name']
        self.description = params.get('description', None)
        self.data_formats = (
            params.get('data_formats', DataTypeDAO.DEFAULT_DATA_FORMATS)
            or DataTypeDAO.DEFAULT_DATA_FORMATS
        )
        self.slug = slug
        self.data_type = None

    def create(self):
        project = Project.query.filter_by(slug=self.slug).first_or_404()

        self.data_type = DataType(
            name=self.name,
            description=self.description,
            data_formats=self.__valid_data_formats(),
            project_id=project.id,
        )

        db.session.add(self.data_type)
        db.session.commit()

        return self

    def update_by(self):
        self.data_type = DataType.query.filter_by(slug=self.slug).first_or_404()
        self.data_type.name = self.name
        self.data_type.description = self.description
        self.data_type.data_formats = self.__valid_data_formats()

        db.session.flush()
        db.session.commit()

        return self

    def __valid_data_formats(self):
        valid_data_formats = list(
            set(current_app.config['DATA_FORMAT_FILE_EXTENSIONS']).intersection(
                self.data_formats
            )
        )
        valid_data_formats.sort()
        return valid_data_formats

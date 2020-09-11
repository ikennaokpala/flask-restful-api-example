from dataclasses import make_dataclass
from sqlalchemy import or_, desc, asc
from flask import current_app

from src.main.dao.data_types_dao import DataTypesDAO
from src.main.models.data_type import DataType
from src.main.models.project import Project
from src.main import db


class DataTypesWithUserDAO(DataTypesDAO):
    @staticmethod
    def data_types_decorator(callable):
        return DataTypesDAO.data_types_decorator(callable)

    def __init__(self, params, owner):
        super(DataTypesWithUserDAO, self).__init__(params, None)
        self.owner = owner

    @data_types_decorator.__func__
    def fetch(self):
        return (
            db.session.query(DataType)
            .join(Project)
            .filter(
                or_(Project.owner == self.owner, Project.collaborators.any(self.owner))
            )
            .order_by(self.ranker())
            .paginate(self.page, self.per_page, self.error_out, self.max_per_page)
        )

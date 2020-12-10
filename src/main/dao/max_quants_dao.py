from dataclasses import make_dataclass
from sqlalchemy import or_, desc, asc
from flask import current_app

from src.main.models.prototypes.max_quant import MaxQuant
from src.main import db


class MaxQuantsDAO:
    @classmethod
    def call(klazz, params):
        return klazz(params).fetch()

    @staticmethod
    def max_quants_decorator(callable):
        max_quants_info = make_dataclass(
            'PrototypeInfo', ['page', 'per_page', 'total', 'prototypes']
        )

        def wrapper(*args, **kwargs):
            max_quants = callable(*args, **kwargs).__dict__

            return max_quants.pop('query') and max_quants_info(
                page=max_quants.get('page'),
                per_page=max_quants.get('per_page'),
                total=max_quants.get('total'),
                prototypes=max_quants.get('items'),
            )

        return wrapper

    def __init__(self, params):
        self.error_out = False
        self.page = int(params.get('page', 1))
        self.per_page = int(params.get('per_page', 25))
        self.direction = params.get('direction', 'desc')
        self.max_per_page = int(current_app.config['PAGINATION_MAX_PER_PAGE'])

    @max_quants_decorator.__func__  # accessing the underlying static max_quants_decorator method directly with the __func__ attribute else staticmethod isn't callable
    def fetch(self):
        return (
            MaxQuant.query.filter()
            .order_by(self.ranker())
            .paginate(self.page, self.per_page, self.error_out, self.max_per_page)
        )

    def ranker(self):
        if self.direction == 'asc':
            return asc(MaxQuant.created_at)
        return desc(MaxQuant.created_at)

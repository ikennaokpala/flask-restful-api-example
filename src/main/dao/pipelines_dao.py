from dataclasses import make_dataclass
from sqlalchemy import or_, desc, asc
from flask import current_app

from src.main.models.pipeline import Pipeline
from src.main import db


class PipelinesDAO:
    @classmethod
    def call(klazz, params):
        return klazz(params).fetch()

    @staticmethod
    def pipelines_decorator(callable):
        pipelines_info = make_dataclass(
            'PipelineInfo', ['page', 'per_page', 'total', 'pipelines']
        )

        def wrapper(*args, **kwargs):
            pipelines = callable(*args, **kwargs).__dict__

            return pipelines.pop('query') and pipelines_info(
                page=pipelines.get('page'),
                per_page=pipelines.get('per_page'),
                total=pipelines.get('total'),
                pipelines=pipelines.get('items'),
            )

        return wrapper

    def __init__(self, params):
        self.error_out = False
        self.page = int(params.get('page', 1))
        self.per_page = int(params.get('per_page', 25))
        self.direction = params.get('direction', 'desc')
        self.max_per_page = int(current_app.config['PAGINATION_MAX_PER_PAGE'])

    @pipelines_decorator.__func__  # accessing the underlying static pipelines_decorator method directly with the __func__ attribute else staticmethod isn't callable
    def fetch(self):
        return (
            Pipeline.query.filter()
            .order_by(self.ranker())
            .paginate(self.page, self.per_page, self.error_out, self.max_per_page)
        )

    def ranker(self):
        if self.direction == 'asc':
            return asc(Pipeline.created_at)
        return desc(Pipeline.created_at)

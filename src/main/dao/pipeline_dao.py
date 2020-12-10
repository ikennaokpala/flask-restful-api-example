from src.main.lib.pipeline_input_builder import PipelineInputBuilder
from src.main.models.pipeline import Pipeline
from src.main.models.data_type import DataType
from src.main.models.prototype import Prototype
from src.main import db


class PipelineDAO:
    def __init__(self, params, builder=PipelineInputBuilder):
        self.payload = None
        self.pipeline = None
        self.builder = builder
        self.data_type = params['data_type']
        self.name = params['name'].strip()
        self.prototype = params['prototype']
        self.description = params.get('description', '').strip()

    def create(self):
        if self.name == '' or self.name == None:
            raise KeyError

        data_type = DataType.query.filter_by(slug=self.data_type).first_or_404()
        prototype = Prototype.query.filter_by(slug=self.prototype).first_or_404()

        self.pipeline = Pipeline(
            name=self.name,
            description=self.description,
            data_type_id=data_type.id,
            prototype_id=prototype.id,
        )

        db.session.add(self.pipeline)
        db.session.commit()

        self.payload = self.builder.call(self.pipeline)

        return self

    def update_by(self, uuid):
        self.pipeline = Pipeline.query.filter_by(id=uuid).first_or_404()
        self.pipeline.name = self.name
        self.pipeline.description = self.description
        self.pipeline.data_type_id = (
            DataType.query.filter_by(slug=self.data_type).first_or_404().id
        )
        self.pipeline.prototype_id = (
            Prototype.query.filter_by(slug=self.prototype).first_or_404().id
        )

        db.session.flush()
        db.session.commit()

        return self

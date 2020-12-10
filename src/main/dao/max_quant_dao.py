from src.main.lib.max_quant_files_builder import MaxQuantFilesBuilder
from src.main.models.prototypes.max_quant import MaxQuant
from src.main import db


class MaxQuantDAO:
    def __init__(self, params, builder=MaxQuantFilesBuilder):
        self.builder = builder
        self.name = params['name'].strip()
        self.max_quant = None
        self.max_quant_file = params['max_quant_file']
        self.fasta_file = params['fasta_file']
        self.description = params.get('description', None).strip()

    def after_initial_commit(callable):
        def wrapper(*args, **kwargs):
            this = callable(*args, **kwargs)

            this.max_quant.content = this.builder.call(
                this.max_quant, this.fasta_file, this.max_quant_file
            )

            db.session.flush()
            db.session.commit()

            return this

        return wrapper

    @after_initial_commit
    def create(self):
        if self.name == '' or self.name == None:
            raise KeyError

        self.max_quant = MaxQuant(name=self.name, description=self.description,)

        db.session.add(self.max_quant)
        db.session.commit()

        return self

    @after_initial_commit
    def update_by(self, slug):
        self.max_quant = MaxQuant.query.filter_by(slug=slug).first_or_404()
        self.max_quant.name = self.name
        self.max_quant.description = self.description

        db.session.flush()
        db.session.commit()

        return self

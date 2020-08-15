from app.main.models.project import Project
from app.main import db


class ProjectDAO:
    def __init__(self, params, owner):
        self.name = params['name']
        self.description = params.get('description', None)
        self.collaborators = params.get('collaborators', [])
        self.owner = owner
        self.project = None

    def create(self):
        self.project = Project(
            name=self.name,
            description=self.description,
            collaborators=self.collaborators,
            owner=self.owner,
        )
        db.session.add(self.project)
        db.session.commit()
        return self

    def update_by(self, slug):
        self.project = Project.query.filter_by(slug=slug).first_or_404()
        self.project.name = self.name
        self.project.description = self.description
        self.project.collaborators = self.collaborators

        db.session.flush()
        db.session.commit()

        return self

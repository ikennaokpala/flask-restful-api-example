from werkzeug.exceptions import UnprocessableEntity
from app.main.models.project import Project
from app.main import db

class ProjectDAO:
    def __init__(self, params, owner):
        self.name = params['name']
        self.description = params['description']
        self.collaborators = params['collaborators']
        self.owner = owner
        self.project = None

    def create(self):
        self.project = Project(name=self.name, description=self.description, collaborators=self.collaborators, owner=self.owner)
        db.session.add(self.project)
        db.session.commit()
        return self

    def update_by(self, slug):
        try:
            self.project = Project.query.filter_by(slug=slug).first()
            self.project.name = self.name
            self.project.description = self.description
            self.project.collaborators = self.collaborators

            db.session.flush()
            db.session.commit()
            return self
        except:
            raise UnprocessableEntity
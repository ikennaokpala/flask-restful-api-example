from app.main.models.project import Project
from app.main import db

class ProjectDAO:
    def __init__(self, name, description, email):
        self.name = name
        self.description = description
        self.email = email
        self.project = None

    def create(self):
        self.project = Project(name=self.name, description=self.description, email=self.email)
        db.session.add(self.project)
        db.session.commit()
        return self

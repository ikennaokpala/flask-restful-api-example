import os

from collections import namedtuple
from flask import current_app, abort
from pathlib import Path

from app.main import db
from app.main.models.project import Project
from app.main.lib.project_mzxml_files_builder import ProjectMzxmlFilesBuilder

class ProjectMzxmlFileDAO:
    def __init__(self, slug, mzxml_files, builder=ProjectMzxmlFilesBuilder):
        self.slug = slug
        self.locations = []
        self.builder = builder
        self.mzxml_files = mzxml_files

    def upload(self):
        if len(self.mzxml_files) == 0: abort(400)

        project = Project.query.filter_by(slug=self.slug).first_or_404()
        project_mzxml_files = self.builder(project, self.mzxml_files).map()

        for project_mzxml_file in project_mzxml_files:
            location = project_mzxml_file.location

            Path(project_mzxml_file.destination).mkdir(parents=True, exist_ok=True)
            project_mzxml_file.mzxml_file.save(location.path)

            db.session.add(project_mzxml_file.model)
            db.session.commit()

            location = location._asdict()
            location.update({ 'id': project_mzxml_file.model.id })

            self.locations.append(location)

        return self.locations

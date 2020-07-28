import os

from collections import namedtuple
from flask import current_app, abort
from pathlib import Path

from app.main import db
from app.main.models.project import Project
from app.main.lib.project_raw_files_builder import ProjectRawFilesBuilder

class ProjectRawFileDAO:
    def __init__(self, slug, raw_files, builder=ProjectRawFilesBuilder):
        self.slug = slug
        self.locations = []
        self.builder = builder
        self.raw_files = raw_files

    def upload(self):
        if len(self.raw_files) == 0: abort(400)

        project = Project.query.filter_by(slug=self.slug).first_or_404()
        project_raw_files = self.builder(project, self.raw_files).map()

        for project_raw_file in project_raw_files:
            location = project_raw_file.location

            Path(project_raw_file.destination).mkdir(parents=True, exist_ok=True)
            project_raw_file.raw_file.save(location.path)

            db.session.add(project_raw_file.model)
            db.session.commit()

            location = location._asdict()
            location.update({ 'raw_file_id': project_raw_file.model.id })

            self.locations.append(location)

        return self.locations

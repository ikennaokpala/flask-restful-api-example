from sqlalchemy import event

from app.main.models.project import Project
from app.main.lib.slugifier import Slugifier


@event.listens_for(Project, 'before_insert')
@event.listens_for(Project, 'before_update')
@event.listens_for(Project, 'after_update')
def slugify_before_save(mapper, connection, project):
    project.slug = Slugifier(project, project.name).call()

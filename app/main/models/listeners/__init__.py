from uuid import uuid4
from slugify import slugify
from sqlalchemy import event

from app.main.models.data_type import DataType
from app.main.models.project import Project


def slugifier(target, value, oldvalue, initiator):
    if value != oldvalue:
        target.slug = slugify(value + ' ' + str(uuid4())[:8])


event.listen(Project.name, 'set', slugifier, retval=False)
event.listen(DataType.name, 'set', slugifier, retval=False)

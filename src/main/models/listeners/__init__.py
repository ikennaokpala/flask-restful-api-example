from uuid import uuid4
from slugify import slugify
from sqlalchemy import event

from src.main.models.prototypes.max_quant import MaxQuant
from src.main.models.prototype import Prototype
from src.main.models.data_type import DataType
from src.main.models.project import Project


def slugifier(target, value, oldvalue, initiator):
    if value != oldvalue:
        target.slug = slugify(value + ' ' + str(uuid4())[:8])


event.listen(MaxQuant.name, 'set', slugifier, retval=False)
event.listen(Prototype.name, 'set', slugifier, retval=False)
event.listen(Project.name, 'set', slugifier, retval=False)
event.listen(DataType.name, 'set', slugifier, retval=False)

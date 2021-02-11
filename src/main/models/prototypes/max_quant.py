from src.main.models.prototype import Prototype
from dataclasses import dataclass


@dataclass
class MaxQuant(Prototype):
    def __init__(self, *args, **kwargs):
        super(MaxQuant, self).__init__(*args, **kwargs)
        self.type = 'MaxQuant'

    __mapper_args__ = {'polymorphic_identity': 'MaxQuant'}

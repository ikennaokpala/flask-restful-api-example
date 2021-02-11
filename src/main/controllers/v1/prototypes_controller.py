from flask_restx import Namespace
from src.main.controllers.v1.max_quant_prototypes_controller import (
    MaxQuantPrototypes,
    MaxQuantPrototype,
)


endpoint = Namespace(
    'prototypes-endpoint',
    description='Prototype related api endpoints (for now this will be very similar to and reuse maxquant endpoints pending further clarification)',
)

endpoint.add_resource(MaxQuantPrototypes, '', '/')
endpoint.add_resource(MaxQuantPrototype, '/<slug>')

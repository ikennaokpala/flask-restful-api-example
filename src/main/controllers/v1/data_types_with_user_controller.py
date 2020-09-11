from flask_restx import Namespace, Resource
from flask import session, request, jsonify
from dataclasses import asdict


from src.main.controllers.v1.data_types_controller import data_types_list
from src.main.dao.data_types_with_user_dao import DataTypesWithUserDAO

endpoint = Namespace(
    'data-types-associated-with-current-user-endpoint',
    description='Endpoint for retrieving data types associated with current user',
)


@endpoint.route('/')  # with slash
@endpoint.route('')  # without slash
class DataTypesWithUser(Resource):
    @endpoint.doc(description='List of a data_types associated with current user')
    @endpoint.response(200, 'Success', data_types_list)
    @endpoint.response(400, 'Bad Request')
    @endpoint.response(404, 'Not Found')
    def get(self):
        data_types = DataTypesWithUserDAO.call(
            request.args, session['token_user']['email']
        )
        return jsonify(asdict(data_types))

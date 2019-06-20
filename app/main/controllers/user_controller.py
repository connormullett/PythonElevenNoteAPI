
from flask import request
from flask_restplus import Resource

from ..utils.dto import UserDto
from ..services import user_service
from ..utils.decorator import Authenticate

api = UserDto.api
_user = UserDto.user

# TODO: User CRUD


@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    @Authenticate
    def get(self):
        return user_service.get_all_users()

    @api.response(201, 'User created')
    @api.doc('create new user')
    @api.expect(_user, validate=True)
    def post(self):
        data = request.json
        return user_service.create_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'users public id')
@api.response(404, 'User not found')
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        user = user_service.get_a_user(public_id)
        if not user:
            api.abort(404)
        else:
            return user

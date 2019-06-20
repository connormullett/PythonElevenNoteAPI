
from flask import request, g
from flask_restplus import Resource

from ..utils.dto import UserDto, UserCreateDto, UserDetailDto, UserUpdateDto
from ..services import user_service
from ..utils.decorator import Authenticate

api = UserDto.api
user = UserDto.user
user_create = UserCreateDto.user
user_detail = UserDetailDto.user
user_update = UserUpdateDto.user

# TODO: User CRUD


@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(user, envelope='data')
    def get(self):
        return user_service.get_all_users()

    @api.response(201, 'User created')
    @api.doc('create new user')
    @api.expect(user_create, validate=True)
    def post(self):
        data = request.json
        return user_service.create_user(data=data)


@api.route('/<public_id>')
@api.param('public_id', 'users public id')
@api.response(404, 'User not found')
class User(Resource):

    @api.doc('get a user')
    @api.marshal_with(user_detail)
    def get(self, public_id):
        user = user_service.get_a_user(public_id)
        if not user:
            api.abort(404)
        return user


@api.route('/me')
@api.response(401, 'unauthorized')
class UserMe(Resource):

    @api.doc('update users account')
    @api.expect(user_update)
    @Authenticate
    def put(self):
        data = request.json
        user_id = g.user.get('owner_id')
        return user_service.update_user(user_id, data)

    @api.doc('get account associated with token')
    @api.marshal_with(user_detail)
    @Authenticate
    def get(self):
        user_id = g.user.get('owner_id')
        return user_service.get_a_user(user_id)

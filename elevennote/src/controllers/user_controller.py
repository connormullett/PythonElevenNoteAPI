
from flask import request, g
from flask_restplus import Resource

from ..utils.dto import UserDto, UserCreateDto, UserDetailDto, UserUpdateDto, UserMe
from ..services import user_service
from ..utils.decorator import Authenticate

api = UserDto.api
user = UserDto.user
user_create = UserCreateDto.user
user_detail = UserDetailDto.user
user_update = UserUpdateDto.user
user_me = UserMe.user

# TODO: User CRUD


@api.route('/')
class UserList(Resource):

    @api.response(201, 'User created')
    @api.doc('create new user')
    @api.expect(user_create, validate=True)
    def post(self):
        data = request.json
        return user_service.create_user(data=data)


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
    @api.marshal_with(user_me)
    @Authenticate
    def get(self):
        user_id = g.user.get('owner_id')
        return user_service.get_a_user(user_id)

    @api.doc('delete account')
    @Authenticate
    def delete(self):
        user_id = g.user.get('owner_id')
        return user_service.delete_user(user_id)

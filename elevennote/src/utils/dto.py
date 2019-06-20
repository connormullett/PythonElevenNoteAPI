
from flask_restplus import Namespace, fields


### USER DTO'S ###

class UserDto:  # List item
    api = Namespace('user', description='user related ops')
    user = api.model('user', {
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier'),
    })


class UserDetailDto:
    api = UserDto.api
    user = api.model('user_detail', {
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier'),
        'registered_on': fields.DateTime(description='time of registration'),
        'modified_at': fields.DateTime(description='time of revision'),
    })


class UserMe:
    api = UserDto.api
    user = api.model('user_detail', {
        'email': fields.String(required=True, description='users email'),
        'username': fields.String(required=True, description='user username'),
        'public_id': fields.String(description='user Identifier'),
        'registered_on': fields.DateTime(description='time of registration'),
        'modified_at': fields.DateTime(description='time of revision'),
    })
    


class UserCreateDto:
    api = UserDto.api
    user = api.model('user_create', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'confirm_password': fields.String(required=True, description='users confirmation of password')
    })


class UserUpdateDto:
    api = UserDto.api
    user = api.model('user_update', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
    })



### TOKEN DTOS ###

class AuthDto:
    api = Namespace('auth', description='authentication')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


### NOTES DTOS ###

class NoteDto:  # List Dto
    api = Namespace('note', description='notes')
    note = api.model('note', {
        'id': fields.Integer(required=True, description='id of note'),
        'title': fields.String(required=True, description='title'),
        'owner_id': fields.String(required=True, description='id of owner'),
        'created_at': fields.DateTime(required=True, description='when note was created')
    })


class NoteDetailDto:
    api = NoteDto.api
    note = api.model('note_detail', {
        'id': fields.Integer(required=True, description='id of note'),
        'title': fields.String(required=True, description='title'),
        'content': fields.String(required=True, description='content of note'),
        'owner_id': fields.String(required=True, description='id of owner'),
        'created_at': fields.DateTime(description='when note was created'),
        'modified_at': fields.DateTime(description='last revision of note')
    })
    

class NoteCreateDto:
    api = NoteDto.api
    note = api.model('note', {
        'title': fields.String(required=True, description='title of note'),
        'content': fields.String(required=True, description='content of note')
    })


class NoteUpdateDto:
    api = NoteDto.api
    note = api.model('note', {
        'title': fields.String(required=True, description='title of note'),
        'content': fields.String(required=True, description='content of note')
    })
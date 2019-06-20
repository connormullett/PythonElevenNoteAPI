
from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related ops')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class NoteDto:
    api = Namespace('note', description='notes')
    note = api.model('note', {
        'title': fields.String(required=True, description='title of note'),
        'content': fields.String(required=True, description='content of note')
    })

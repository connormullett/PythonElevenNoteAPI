
from datetime import datetime

from elevennote.src import db
from elevennote.src.models.user import User


def create_user(data):

    if not data['password'] or not data['confirm_password']:
        return {
            'status': 'fail',
            'message': 'password fields missing'
        }, 400

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.utcnow(),
        )
        save_changes(new_user)
        return generate_token(new_user)
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(id=id).first()


def update_user(id, data):
    user = get_a_user(id)
    for key, item in data.items():
        setattr(user, key, item)
    user.modified_at = datetime.utcnow()
    db.session.commit()
    response = {'status': 'updated user'}
    return response, 200


def delete_user(id):
    user = User.query.filter_by(public_id=id).first()
    db.session.delete(user)
    db.session.commit()
    return None, 204


def save_changes(data):
    db.session.add(data)
    db.session.commit()


def generate_token(user):
    try:
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
    
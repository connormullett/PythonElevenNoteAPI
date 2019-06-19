
from flask_restplus import Api
from flask import Blueprint

from .main.controllers.user_controller import api as user_ns

user_api = Blueprint('api', __name__)

api = Api(user_api,
        title='Basic API with Flask RestPLUS',
        version='1.0',
        description='basic api'
    )

api.add_namespace(user_ns, path='/users')
from flask import Flask
from flask_restful import Api
from restdemo.settings import config
from restdemo.extensions import db, jwt

from restdemo.resource.user import User, Users
from restdemo.resource.tweet import Tweet
# from restdemo.resource.auth import Login

from flask_migrate import Migrate



def create_app(config_name=None):
    if config_name is None:
        # config_name = os.get_env('FLASK_CONFIG', 'development')
        config_name = 'development'

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)

    return app


def register_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)

    api.add_resource(Users, '/users')
    api.add_resource(User, '/user/<string:username>')
    # api.add_resource(Login, '/auth/login')
    api.add_resource(Tweet, '/tweet/<string:username>')

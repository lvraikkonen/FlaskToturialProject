from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT


db = SQLAlchemy()

from restdemo.model.user import User as UserModel

jwt = JWT(None, UserModel.authenticate, UserModel.identity)

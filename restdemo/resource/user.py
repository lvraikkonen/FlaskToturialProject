from restdemo.model.user import User as UserModel
from flask_restful import Resource, reqparse
from restdemo.extensions import db


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="{error_msg}")

    def get(self, username):
        """
        get user detail information by username
        :param username:
        :return:
        """
        user = db.session.query(UserModel).filter(UserModel.username==username).first()
        if user:
            return user.as_dict()
        # user not found
        return {'message': f"user {username} not found"}


class Users(Resource):

    def get(self):
        users = db.session.query(UserModel).all()
        return [u.as_dict() for u in users]
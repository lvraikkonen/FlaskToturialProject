from restdemo.model.user import User as UserModel
from flask_restful import Resource, reqparse
from flask import request
import jwt


class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="{error_msg}")
    parser.add_argument(
        'email', type=str, required=True, help='required email'
    )

    def get(self, username):
        """
        get user detail information by username
        :param username:
        :return:
        """
        user = UserModel.get_by_username(username)
        if user:
            return user.as_dict()
        # user not found
        return {'message': f"user {username} not found"}, 404

    def post(self, username):
        """
        create a user
        :param username:
        :return:
        """
        data = User.parser.parse_args()
        user = UserModel.get_by_username(username)
        if user:
            return {'message': f"user {username} already exist."}
        user = UserModel(
            username=username,
            email=data.get('email')
        )
        user.set_password(data.get('password'))
        user.add()
        return user.as_dict(), 201

    def delete(self, username):
        """
        delete a user by username
        :param username:
        :return:
        """
        user = UserModel.get_by_username(username)
        if user:
            user.delete()
            return {'message': f"user {username} deleted."}
        else:
            return {'message': f"user {username} not found."}, 204

    def put(self, username):
        """
        update a user password
        :param username:
        :return:
        """
        user = UserModel.get_by_username(username)
        if user:
            data = User.parser.parse_args()
            user.password_hash = data.get('password')
            user.update()
            return user.as_dict()
        else:
            return {'message': f"user {username} not found."}, 204


class Users(Resource):

    def get(self):
        token = request.headers.get('Authorization_token')
        try:
            jwt.decode(
                token,
                'secret_key',
                algorithms='HS256'
            )
        except jwt.ExpiredSignature:
            # the token is expired
            return {"message": "Token expired, please login to get a new token"}
        except jwt.InvalidTokenError:
            return {"message": "Invalid token, please register or login"}
        # using valid token to get all user
        users = UserModel.get_user_list()
        return [u.as_dict() for u in users]
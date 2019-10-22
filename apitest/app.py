from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse


app = Flask(__name__)
api = Api(app)


# sample user data list
user_list = [{'username': "aaa", "password": "123"}]


class Users(Resource):

    def get(self):
        return user_list

class User(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('password', type=str, required=True, help="{error_msg}")

    def get(self, username):
        """
        get user detail information by username
        :return:
        """
        for user in user_list:
            if user['username'] == username:
                return user
        # not found
        return {'message': f'user {username} not found.'}, 404

    def post(self, username):
        """
        create a user
        :return:
        """
        print(request.get_json())
        data = User.parser.parse_args()
        user = {
            'username': username,
            'password': data.get('password')
        }
        for u in user_list:
            if u['username'] == username:
                return {'message': f"user {username} already exist."}
        user_list.append(user)
        return user, 201

    def delete(self, username):
        """
        delete a user by username
        :param username:
        :return:
        """
        user_find = None
        for user in user_list:
            if user['username'] == username:
                user_find = user
        if user_find:
            user_list.remove(user_find)
            return user_find
        else:
            return {'message': f"user {username} not found."}, 204

    def put(self, username):
        """
        update a user password
        :param username:
        :return:
        """
        user_find = None
        for user in user_list:
            if user['username'] == username:
                user_find = user
        if user_find:
            data = User.parser.parse_args()
            user_list.remove(user_find)
            user_find['password'] = data.get('password')
            user_list.append(user_find)
            return user_find
        else:
            return {'message': f"user {username} not found."}, 204


api.add_resource(Users, '/users')
api.add_resource(User, '/user/<string:username>')


if __name__ == '__main__':
    app.run()

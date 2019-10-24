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
        return {'message': f"user {username} not found"}, 404

    def post(self, username):
        """
        create a user
        :param username:
        :return:
        """
        data = User.parser.parse_args()
        user = db.session.query(UserModel).filter(UserModel.username==username).first()
        if user:
            return {'message': f"user {username} already exist."}
        user = UserModel(
            username=username,
            password_hash=data.get('password')
        )
        db.session.add(user)
        db.session.commit()
        return user.as_dict(), 201

    def delete(self, username):
        """
        delete a user by username
        :param username:
        :return:
        """
        user = db.session.query(UserModel).filter(UserModel.username==username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': f"user {username} deleted."}
        else:
            return {'message': f"user {username} not found."}, 204

    def put(self, username):
        """
        update a user password
        :param username:
        :return:
        """
        user = db.session.query(UserModel).filter(
            UserModel.username == username
        ).first()
        if user:
            data = User.parser.parse_args()
            user.password_hash = data.get('password')
            db.session.commit()
            return user.as_dict()
        else:
            return {'message': f"user {username} not found."}, 204


class Users(Resource):

    def get(self):
        users = db.session.query(UserModel).all()
        return [u.as_dict() for u in users]
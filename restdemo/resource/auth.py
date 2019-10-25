from flask_restful import Resource, reqparse
from restdemo.model.user import User as UserModel


class Login(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="required username")
    parser.add_argument('password', type=str, required=True, help="required password")

    def post(self):
        """"""
        data = Login.parser.parse_args()
        user = UserModel.get_by_username(username=data.get('username'))
        if user:
            if not user.check_password(data.get('password')):
                return {
                    "message": "Login failed, please input the right username and password."
                }
            return {
                "message": "Login success.",
                "token": user.generate_token() # generate user token
            }
        else:
            return {"message": f"user {data.get('username')} doesn't exist."}

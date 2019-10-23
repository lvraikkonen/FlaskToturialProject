from flask import Flask
from flask_restful import Api
from resource.user import User, Users


app = Flask(__name__)
api = Api(app)


api.add_resource(Users, '/users')
api.add_resource(User, '/user/<string:username>')


if __name__ == '__main__':
    app.run()

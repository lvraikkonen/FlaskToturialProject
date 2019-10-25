from restdemo.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from restdemo.model.base import Base


from datetime import datetime, timedelta


class User(Base):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)

    tweet = db.relationship('Tweet')

    def __repr__(self):
        return f"id={self.id}, username={self.username}"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_username(username):
        return db.session.query(User).filter(
            User.username==username
        ).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.query(User).filter(
            User.id == user_id
        ).first()

    @staticmethod
    def get_user_list():
        return db.session.query(User).all()

    def generate_token(self):
        """
        generate the access token
        :return:
        """
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': self.username
            }
            # create the byte token
            jwt_token = jwt.encode(
                payload,
                'secret_key',
                algorithm='HS256'
            )
            return jwt_token.decode()
        except Exception as e:
            # return error
            return str(e)

    @staticmethod
    def authenticate(username, password):
        user = User.get_by_username(username)
        if user:
            # check password
            if user.check_password(password):
                return user
            # else auth failed

    @staticmethod
    def identity(payload):
        user_id = payload['identity']
        user = User.get_by_id(user_id)
        return user

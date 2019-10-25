from restdemo.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from datetime import datetime, timedelta


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f"id={self.id}, username={self.username}"

    def as_dict(self):
        return {u.name: getattr(self, u.name) for u in self.__table__.columns}

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    @staticmethod
    def get_by_username(username):
        return db.session.query(User).filter(
            User.username==username
        ).first()

    @staticmethod
    def get_by_id(user_id):
        return db.session.query(User).filter(
            User.id==user_id
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
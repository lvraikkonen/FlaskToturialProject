from restdemo.extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return f"id={self.id}, username={self.username}"

    def as_dict(self):
        return {u.name: getattr(self, u.name) for u in self.__table__.columns}
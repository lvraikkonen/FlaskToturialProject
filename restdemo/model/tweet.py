from restdemo.model.base import Base
from restdemo.extensions import db
from sqlalchemy import func


class Tweet(Base):

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    created_on = db.Column(db.DateTime, server_default=func.now())

    def __repr__(self):
        return f"user_id={self.user_id}, tweet={self.body}"

    def as_dict(self):
        t = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        t['created_on'] = t['created_on'].isoformat()
        return t

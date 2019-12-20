from sqlalchemy.sql import func

from project import db


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, email=""):
        self.email = email

    def __repr__(self):
        return f"<User id: {self.id}, email: {self.email}>"

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "active": self.active,
        }

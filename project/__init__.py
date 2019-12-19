import os
from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

# import sys
# print(app.config, file=sys.stderr)

from project.api.hello import api as hello_api

app = Flask(__name__)


api = Api(
    app,
    doc="/swagger",
    title="Wakemaps API",
    version="0.1",
    description="Wakepark listing directory",
)

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(255), nullable=False)
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


app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)

api.add_namespace(hello_api)

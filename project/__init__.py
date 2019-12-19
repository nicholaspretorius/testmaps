from flask import Flask
from flask_restplus import Api

from project.api.hello import api as hello_api

app = Flask(__name__)
api = Api(
    app,
    doc="/swagger",
    title="Wakemaps API",
    version="0.1",
    description="Wakepark listing directory",
)

app.config.from_object("project.config.DevelopmentConfig")

api.add_namespace(hello_api)

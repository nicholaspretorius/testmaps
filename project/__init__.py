from flask import Flask
from flask_restplus import Api
import os

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

app_settings = os.getenv("APP_SETTINGS")
app.config.from_object(app_settings)

api.add_namespace(hello_api)

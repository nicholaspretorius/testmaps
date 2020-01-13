from flask import Blueprint
from flask_restplus import Api

from project.apis.auth import api as auth_api
from project.apis.hello import api as hello_api
from project.apis.users.views import api as users_api
from project.apis.wakeparks.views import api as wakeparks_api
from project.apis.sanity import api as sanity_api

blueprint = Blueprint("api", __name__)
api = Api(
    blueprint,
    doc="/docs",
    title="Wakemaps API",
    version="0.1",
    description="Wakepark listing directory",
)

api.add_namespace(hello_api)
api.add_namespace(users_api)
api.add_namespace(wakeparks_api)
api.add_namespace(auth_api, path="/auth")
api.add_namespace(sanity_api, path="/sanity")

from flask import Blueprint, jsonify
from flask_restplus import Api
from ..utils.logger import log
from webargs import ValidationError

from .hello import api as hello_api
from .users import api as users_api

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


@api.errorhandler
def default_error_handler(err):
    message = "An unhandled error occurred."
    log.error(message)

    return {"message": message}, 500


@api.errorhandler(ValidationError)
def invalid_payload(err):
    headers = err.data.get("headers", None)
    messages = err.data.get("messages", ["Invalid payload."])
    if headers:
        return jsonify({"errors": messages}), err.code, headers
    else:
        return jsonify({"errors": messages}), err.code

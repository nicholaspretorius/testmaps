from flask import Blueprint
from flask_restplus import Api

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


# @api.errorhandler
# def default_error_handler(err):
#     message = "An unhandled error occurred."
#     log.error(message)

#     return {"message": message}, 500


# @api.errorhandler(BadRequest)
# def invalid_payload(err):
#     """Invalid payload provided"""
#     log("Error: ", err)
#     return jsonify({"status": "fail", "error": 400, "message": "Invalid payload"}), 400

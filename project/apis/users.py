import re

from flask import request
from flask_restplus import Namespace, Resource, fields

from project.apis.services import (create_user, get_user_by_email,
                                   get_user_by_id, get_users)

api = Namespace("users", description="Users resource")

EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")

# flask_resplus models
USER = api.model(
    "User",
    {
        "id": fields.String(
            readOnly=True, description="The user identifier", example="1"
        ),
        "email": fields.String(
            required=True,
            description="A valid email address",
            example="test@domain.com",
        ),
    },
)

# Not used at present
error = api.model(
    "Error",
    {
        "success": fields.Boolean(default=False),
        "error": fields.Integer(description="The HTTP error code", example=400),
        "message": fields.String(
            description="The associated error message", example="Invalid payload"
        ),
    },
)


@api.route("/")
class UserList(Resource):
    @api.marshal_with(USER, as_list=True)
    def get(self):
        """List all users"""
        return get_users(), 200

    @api.expect(USER, validate=False)
    @api.response(201, "<user_email> was added!")
    @api.response(400, "invalid payload")
    def post(self):
        """Create user"""
        post_data = request.get_json()
        email = post_data.get("email")
        res = {"status": False, "message": "Invalid payload"}

        if email is None:
            return res, 400

        valid_email = EMAIL_REGEX.match(email)

        if valid_email is None:
            res["message"] = "Please provide a valid email address"
            return res, 400

        current_user = get_user_by_email(email)
        if current_user:
            res["message"] = "Sorry, that email already exists."
            return res, 400

        new_user = create_user(email)
        res["status"] = True
        res["message"] = f"{email} was added!"
        res["user"] = new_user.to_json()
        return res, 201


@api.route("/<int:user_id>")
class Users(Resource):
    @api.marshal_with(USER)
    @api.response(200, "Success")
    @api.response(404, "Resource not found")
    def get(self, user_id):
        """Returns a single user"""
        user = get_user_by_id(user_id)

        if user is None:
            api.abort(404, "Resource not found", status=False)
        else:
            return user, 200

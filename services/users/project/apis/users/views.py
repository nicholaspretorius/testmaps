import re

from flask import request
from flask_restplus import Namespace, Resource, fields

from project.apis.users.services import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    get_users,
    update_user,
)

api = Namespace("users", description="Users resource")

EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")

# flask_resplus models
USER = api.model(
    "USER",
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

USER_FULL = api.inherit(
    "USER_FULL",
    USER,
    {
        "password": fields.String(
            required=True, description="A strong password", example="Xy67!abc"
        )
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

    # TODO: Refactor validation
    @api.expect(USER_FULL, validate=False)
    @api.response(201, "<user_email> was added!")
    @api.response(400, "invalid payload")
    def post(self):
        """Create user"""
        post_data = request.get_json()
        email = post_data.get("email")
        password = post_data.get("password")
        res = {"status": False, "message": "Invalid payload"}

        if email is None or password is None:
            return res, 400

        valid_email = EMAIL_REGEX.match(email)

        if valid_email is None:
            res["message"] = "Please provide a valid email address"
            return res, 400

        current_user = get_user_by_email(email)
        if current_user:
            res["message"] = "Sorry, that email already exists."
            return res, 400

        new_user = create_user(email, password)
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

    @api.response(200, "Success")
    @api.response(404, "Resource not found")
    def delete(self, user_id):
        """Deletes a single user"""
        user = get_user_by_id(user_id)

        if user is None:
            api.abort(404, "Resource not found", status=False)
        else:
            delete_user(user)
            return {
                "status": True,
                "message": "User was deleted.",
                "user": user.to_json(),
            }

    # TODO: Refactor validation
    @api.expect(USER, validate=False)
    @api.response(200, "Success")
    @api.response(400, "Invalid payload")
    @api.response(404, "Resource not found")
    def put(self, user_id):
        """Updates a single user"""
        post_data = request.get_json()
        email = post_data.get("email")
        res = {"status": False, "message": "Invalid payload"}

        user = get_user_by_id(user_id)

        if user is None:
            api.abort(404, "Resource not found", status=False)

        if email is None:
            return res, 400

        valid_email = EMAIL_REGEX.match(email)

        if valid_email is None:
            res["message"] = "Please provide a valid email address"
            return res, 400
        else:
            updated_user = update_user(user, email)
            res["status"] = True
            res["message"] = "User successfully updated."
            res["user"] = updated_user.to_json()
            return res, 200

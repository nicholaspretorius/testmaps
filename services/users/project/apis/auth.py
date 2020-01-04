import re

from flask import request
from flask_restplus import Namespace, Resource, fields

from project import bcrypt
from project.apis.users.services import create_user, get_user_by_email

api = Namespace("auth", description="Authorisation resource")

EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")

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

USER_POST = api.inherit(
    "User Post",
    USER,
    {
        "password": fields.String(
            required=True, description="A strong password", example="Xy67!abc"
        )
    },
)

REFRESH = api.model(
    "Refresh",
    {"refresh_token": fields.String(required=True, description="JWT Refresh token")},
)

TOKENS = api.inherit(
    "Refresh",
    REFRESH,
    {"access_token": fields.String(required=True, description="JWT Access token")},
)


@api.route("/register")
class Register(Resource):
    # @api.marshal_with(USER)
    @api.expect(USER_POST, validate=False)
    @api.response(201, "Success")
    # @api.response(400, "Sorry, that email already exists.")
    @api.response(400, "Invalid payload")
    def post(self):
        """Register user"""
        post_data = request.get_json()
        print("post_data", post_data)
        print("post_data type", type(post_data))
        print("email", post_data.get("email"))
        print("password", post_data.get("password"))
        email = post_data.get("email")
        password = post_data.get("password")
        res = {"status": False, "message": "Invalid payload"}

        if email is None or password is None:
            return res, 400

        valid_email = EMAIL_REGEX.match(email)

        if valid_email is None:
            res["message"] = "Please provide a valid email address."
            return res, 400

        current_user = get_user_by_email(email)
        print("User:", current_user)
        if current_user:
            res["message"] = "Sorry, that email already exists."
            return res, 400

        new_user = create_user(email, password)
        return new_user.to_json(), 201


@api.route("/login")
class Login(Resource):
    # @api.marshal_with(TOKENS)
    @api.expect(USER_POST, validate=False)
    @api.response(200, "Success")
    @api.response(400, "Invalid payload")
    # @api.response(400, "Please provide a valid email address")
    @api.response(404, "User does not exist.")
    def post(self):
        """Login user"""
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
        if current_user is None or bcrypt.check_password_hash(
            current_user.password, password
        ):
            res["message"] = "User does not exist."
            return res, 400

        access_token = current_user.encode_token(current_user.id, "access")
        refresh_token = current_user.encode_token(current_user.id, "refresh")

        res = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return res, 200


@api.route("/refresh")
class Refresh(Resource):
    def post(self):
        pass


@api.route("/status")
class Status(Resource):
    def get(self):
        pass


api.add_resource(Register)
api.add_resource(Login)
api.add_resource(Refresh)
api.add_resource(Status)

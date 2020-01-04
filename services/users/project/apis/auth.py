import re

import jwt
from flask import request
from flask_restplus import Namespace, Resource, fields

from project import bcrypt
from project.apis.users.models import User
from project.apis.users.services import create_user, get_user_by_email, get_user_by_id

api = Namespace("auth", description="Authorisation resource")

EMAIL_REGEX = re.compile(r"\S+@\S+\.\S+")

REGISTER = api.model(
    "REGISTER",
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

LOGIN = api.inherit(
    "LOGIN",
    REGISTER,
    {
        "password": fields.String(
            required=True, description="A strong password", example="Xy67!abc"
        )
    },
)

REFRESH = api.model(
    "REFRESH",
    {"refresh_token": fields.String(required=True, description="JWT Refresh token")},
)

TOKENS = api.inherit(
    "TOKENS",
    REFRESH,
    {"access_token": fields.String(required=True, description="JWT Access token")},
)

parser = api.parser()
parser.add_argument("Authorization", location="headers")


@api.route("/register")
class Register(Resource):
    # @api.marshal_with(USER)
    @api.expect(LOGIN, validate=False)
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
    @api.expect(LOGIN, validate=False)
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
        if current_user is None or not bcrypt.check_password_hash(
            current_user.password, password
        ):
            res["message"] = "User does not exist."
            return res, 404

        access_token = current_user.encode_token(current_user.id, "access")
        refresh_token = current_user.encode_token(current_user.id, "refresh")

        res = {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode(),
        }

        return res, 200


@api.route("/refresh")
class Refresh(Resource):
    @api.expect(REFRESH, validate=False)
    @api.response(200, "Success")
    @api.response(400, "Invalid payload")
    @api.response(401, "Invalid (token)")
    def post(self):
        """Refresh token"""
        post_data = request.get_json()
        refresh_token = post_data.get("refresh_token")
        res = {"status": False, "message": "Invalid payload."}

        if refresh_token is None:
            return res, 400

        try:
            resp = User.decode_token(refresh_token)
            user = get_user_by_id(resp)

            if not user:
                res["message"] = "Invalid token."
                return res, 400

            access_token = user.encode_token(user.id, "access")
            refresh_token = user.encode_token(user.id, "refresh")

            res = {
                "access_token": access_token.decode(),
                "refresh_token": refresh_token.decode(),
            }

            return res, 200

        except jwt.ExpiredSignatureError:
            res["message"] = "Signature expired. Please login again."
            return res, 401
        except jwt.InvalidTokenError:
            res["message"] = "Invalid token. Please login again."
            return res, 401


@api.route("/status")
class Status(Resource):
    # @api.marshal_with(REGISTER)
    @api.response(200, "Success")
    @api.response(401, "Invalid token")
    @api.response(403, "Access token required")
    @api.expect(parser)
    def get(self):
        """Get user status"""
        auth_header = request.headers.get("Authorization")
        res = {"status": False, "message": "Invalid payload."}

        if auth_header:
            try:
                access_token = auth_header.split(" ")

                if len(access_token) > 1:
                    access_token = auth_header.split(" ")[1]
                    resp = User.decode_token(access_token)
                    user = get_user_by_id(resp)
                else:
                    res["message"] = "Invalid header."
                    return res, 401

                if not user:
                    res["message"] = "Invalid token. Please login."
                    return res, 401

                return user.to_json(), 200
            except jwt.ExpiredSignatureError:
                res["message"] = "Signature expired. Please login again."
                return res, 401
            except jwt.InvalidTokenError:
                res["message"] = "Invalid token. Please login again."
                return res, 401
        else:
            res["message"] = "Access token required."
            return res, 403


api.add_resource(Register)
api.add_resource(Login)
api.add_resource(Refresh)
api.add_resource(Status)

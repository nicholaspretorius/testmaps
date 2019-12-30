from flask import request
from flask_restplus import fields, Namespace, Resource
from project.apis.services import get_users, create_user, get_user_by_email
from project.utils.logger import log

api = Namespace("users", description="Users resource")

# TODO: extract to openapi.models file

# flask_resplus models
user = api.model(
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

# TODO: extract to openapi.models file
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
    @api.marshal_with(user, as_list=True)
    def get(self):
        """List all users"""
        return get_users(), 200

    @api.expect(user, validate=True)
    @api.response(201, "<user_email> was added!")
    @api.response(400, "invalid payload")
    def post(self):
        """Create user"""
        post_data = request.get_json()
        email = post_data.get("email")
        print("Email: ", email)
        log.debug(f"Email: {email}")
        res = {}

        # if not email:
        #     res["message"] = "Email is required"
        #     return res, 400

        user = get_user_by_email(email)
        if user:
            res["message"] = "Sorry, that email already exists."
            return res, 400

        new_user = create_user(email)
        res["message"] = f"{email} was added!"
        res["user"] = new_user.to_json()
        return res, 201

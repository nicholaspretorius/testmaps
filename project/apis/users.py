from flask import request
from flask_restplus import fields, Namespace, Resource
from project import db
from project.apis.models import User

api = Namespace("users", description="Users resource")

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


def get_users():
    return [user.to_json() for user in User.query.all()]


def create_user(data):
    email = data.get("email")
    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user


@api.route("/")
class UserList(Resource):
    @api.doc("get_users")
    @api.marshal_with(user, as_list=True)
    def get(self):
        """List all users"""
        return get_users()

    @api.doc("create_user")
    @api.expect(user)
    @api.marshal_with(user, code=201)
    @api.response(400, "invalid payload", error)
    def post(self):
        """Create user"""
        new_user = create_user(request.json)
        return new_user, 201

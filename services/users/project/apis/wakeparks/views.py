# from flask import request
from flask_restplus import Namespace, Resource, fields

from project.apis.wakeparks.services import get_wakeparks

# from project.apis.auth0 import AuthError, requires_auth

api = Namespace("wakeparks", description="Wakeparks resource")

location_fields = {}
location_fields["lat"] = fields.Float(
    required=True,
    description="The latitude co-ordinates of the wakepark location",
    example="-25.952558",
)
location_fields["lng"] = fields.Float(
    required=True,
    description="The longitude co-ordinates of the wakepark location",
    example="28.185543",
)

social_fields = {}
social_fields["instagram"] = fields.String(
    required=False,
    description="The official Instragram handle for the wakepark. ONLY the handle. (Do not include https://instagram.com)",
)

WAKEPARK = api.model(
    "WAKEPARK",
    {
        "id": fields.String(
            readOnly=True, description="The wakepark identifier", example="1"
        ),
        "name": fields.String(
            required=True,
            description="The name of the wakepark",
            example="Stoke City Wakepark",
        ),
        "description": fields.String(
            required=True,
            description="A short (less than 255 characters) description of the wakepark",
            example="Stoke City Wakepark",
        ),
        "location": fields.Nested(location_fields),
        "social": fields.Nested(social_fields),
    },
)


@api.route("/")
class WakeparkList(Resource):
    @api.marshal_with(WAKEPARK, as_list=True)
    def get(self):
        """List all wakeparks"""
        return get_wakeparks(), 200

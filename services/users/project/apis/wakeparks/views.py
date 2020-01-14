from flask import abort, request
from flask_restplus import Namespace, Resource, fields

from project.apis.auth0 import AuthError, requires_auth
from project.apis.wakeparks.services import (
    get_wakeparks,
    get_wakepark_by_id,
    create_wakepark,
    delete_wakepark,
    update_wakepark,
    patch_wakepark,
)

# from project.apis.auth0 import AuthError, requires_auth

api = Namespace("wakeparks", description="Wakeparks resource")


LOCATION = api.model(
    "LOCATION",
    {
        "lat": fields.Float(
            required=True,
            description="The latitude co-ordinates of the wakepark location",
            example=-25.952558,
        ),
        "lng": fields.Float(
            required=True,
            description="The longitude co-ordinates of the wakepark location",
            example=28.185543,
        ),
    },
)


SOCIAL = api.model(
    "SOCIAL",
    {
        "instagram": fields.String(
            required=False,
            description="The official Instragram handle for the wakepark. ONLY the handle. (Do not include https://instagram.com)",
            example="stok-ed-wakepark",
        )
    },
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
            example="Stok-ed Wakepark",
        ),
        "description": fields.String(
            required=True,
            description="A short (less than 255 characters) description of the wakepark",
            example="Some awesome wakepark description!",
        ),
        "location": fields.Nested(LOCATION),
        "social": fields.Nested(SOCIAL),
    },
)

UPDATE_WAKEPARK = api.model(
    "UPDATE_WAKEPARK",
    {
        "name": fields.String(
            description="The name of the wakepark", example="Stok-ed Wakepark"
        ),
        "description": fields.String(
            description="A short (less than 255 characters) description of the wakepark",
            example="Some awesome wakepark description!",
        ),
        "lat": fields.Float(
            description="The latitude co-ordinates of the wakepark location",
            example=-25.952558,
        ),
        "lng": fields.Float(
            description="The longitude co-ordinates of the wakepark location",
            example=28.185543,
        ),
        "instagram_handle": fields.String(
            description="The official Instragram handle for the wakepark. ONLY the handle. (Do not include https://instagram.com)",
            example="stok-ed-wakepark",
        ),
    },
)

parser = api.parser()
parser.add_argument("Authorization", location="headers", help="Bearer token required")


@api.route("/")
class WakeparkList(Resource):
    @api.marshal_with(WAKEPARK, as_list=True)
    def get(self):
        """List all wakeparks"""
        return get_wakeparks(), 200

    @api.expect(parser, WAKEPARK, validate=True)
    @api.response(201, "Wakepark was added!")
    @api.response(400, "Invalid payload")
    @api.response(401, "Unauthorised")
    @api.response(403, "Forbidden")
    @requires_auth("post:cableparks")
    def post(self, payload):
        """Create Wakepark"""
        try:
            post_data = request.get_json()
            name = post_data.get("name")
            description = post_data.get("description")

            if post_data.get("location"):
                lat = post_data.get("location")["lat"]
                lng = post_data.get("location")["lng"]

            if post_data.get("social"):
                instagram_handle = post_data.get("social")["instagram"]

            res = {"status": False, "message": "Invalid payload"}

            if name is None or description is None:
                return res, 400

            new_wakepark = create_wakepark(
                name, description, lat, lng, instagram_handle
            )
            res = new_wakepark.to_json()
            return res, 201
        except AuthError:
            return abort(401)


@api.route("/<int:wakepark_id>")
class Wakeparks(Resource):
    @api.marshal_with(WAKEPARK)
    @api.response(200, "Success")
    @api.response(404, "Resource not found")
    def get(self, wakepark_id):
        """Returns a single wakepark"""
        wakepark = get_wakepark_by_id(wakepark_id)

        if wakepark is None:
            api.abort(404, "Resource not found", status=False)
        else:
            return wakepark.to_json(), 200

    @api.expect(parser)
    @api.response(200, "Success")
    @api.response(401, "Unauthorised")
    @api.response(403, "Forbidden")
    @api.response(404, "Resource not found")
    @requires_auth("delete:cableparks")
    def delete(self, wakepark_id, payload):
        """Deletes a single wakepark"""
        try:
            wakepark = get_wakepark_by_id(wakepark_id)

            if wakepark is None:
                api.abort(404, "Resource not found", status=False)
            else:
                delete_wakepark(wakepark)
                res = {
                    "status": True,
                    "message": "Wakepark was deleted",
                    "wakepark": wakepark.to_json(),
                }
                return res, 200
        except AuthError:
            return abort(401)

    # TODO: Need to refactor how this route selects what to update and what not to
    @api.expect(parser, WAKEPARK, validate=True)
    @api.response(200, "Success")
    @api.response(400, "Invalid payload")
    @api.response(401, "Unauthorised")
    @api.response(403, "Forbidden")
    @api.response(404, "Resource not found")
    @requires_auth("put:cableparks")
    def put(self, wakepark_id):
        """Update a single wakepark"""
        try:
            wakepark = get_wakepark_by_id(wakepark_id)

            if wakepark is None:
                api.abort(404, "Resource not found", status=False)

            post_data = request.get_json()
            name = post_data.get("name")
            description = post_data.get("description")

            if post_data.get("location"):
                lat = post_data.get("location")["lat"]
                lng = post_data.get("location")["lng"]

            if post_data.get("social"):
                instagram_handle = post_data.get("social")["instagram"]

            updated_wakepark = update_wakepark(
                wakepark, name, description, lat, lng, instagram_handle
            )

            res = {
                "status": True,
                "message": "Wakepark successfully updated",
                "wakepark": updated_wakepark.to_json(),
            }
            return res, 200
        except AuthError:
            return abort(401)

    @api.expect(parser, UPDATE_WAKEPARK, validate=True)
    @api.response(200, "Success")
    @api.response(400, "Invalid payload")
    @api.response(401, "Unauthorised")
    @api.response(403, "Forbidden")
    @api.response(404, "Resource not found")
    @requires_auth("put:cableparks")
    def patch(self, wakepark_id):
        """Update a single wakepark - check expected payload shape!"""
        try:
            wakepark = get_wakepark_by_id(wakepark_id)

            if wakepark is None:
                api.abort(404, "Resource not found", status=False)

            post_data = request.get_json()

            for field in post_data:
                if field not in wakepark.to_dict():
                    api.abort(400, "Invalid payload", status=False)

            updated_wakepark = patch_wakepark(wakepark, post_data)

            res = {
                "status": True,
                "message": "Wakepark successfully updated",
                "wakepark": updated_wakepark.to_json(),
            }
            return res, 200
        except AuthError:
            return abort(401)

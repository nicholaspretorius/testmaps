from flask import abort
from flask_restplus import Namespace, Resource
from project.apis.auth0 import AuthError, requires_auth

api = Namespace("sanity", description="Auth sanity check routes")


@api.route("/")
class SanityAll(Resource):
    @requires_auth("get:auth-rider-sanity")
    def get(self, payload):
        """Hello all!"""
        try:
            return {"status": "success", "hello": "Riders!"}
        except AuthError:
            return abort(401)


@api.route("/park")
class SanitySuperPark(Resource):
    @requires_auth("get:auth-park-sanity")
    def get(self, payload):
        """Hello parkadmin!"""
        try:
            return {"status": "success", "hello": "Parkadmin!"}
        except AuthError:
            return abort(401)


@api.route("/super")
class SanitySuper(Resource):
    @requires_auth("get:auth-super-sanity")
    def get(self, payload):
        """Hello superadmin!"""
        try:
            return {"status": "success", "hello": "Superadmin!"}
        except AuthError:
            abort(401)

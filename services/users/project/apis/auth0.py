import json
import os
import time
from functools import wraps
from urllib.request import urlopen

from flask import abort, request
from jose import jwt

from project.apis.wakeparks.services import get_wakepark_by_id

AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
ALGORITHMS = os.environ.get("ALGORITHMS")

# AuthError Exception
"""
AuthError Exception
A standardized way to communicate auth failure modes
"""


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header


def get_token_auth_header():
    if "Authorization" not in request.headers:
        raise AuthError(
            {
                "code": "authorisation_header_not_found",
                "description": "Authorisation header not found.",
            },
            401,
        )

    auth_header = request.headers["Authorization"]
    header_parts = auth_header.split(" ")

    if len(header_parts) != 2:
        raise AuthError(
            {
                "code": "authorisation_header_invalid",
                "description": "Authorisation header invalid.",
            },
            401,
        )
    elif header_parts[0].lower() != "bearer":
        raise AuthError(
            {
                "code": "authorisation_header_invalid",
                "description": "Authorisation header type invalid.",
            },
            401,
        )

    return header_parts[1]


def check_permissions(permission, payload, id):

    superadmins = [
        "auth0|5e329997b5be300ef6889c4c",
        "google-oauth2|104755831296456998532",
    ]

    user_id = payload["sub"]

    if id:
        wakepark = get_wakepark_by_id(id)
        if wakepark:
            owner_id = wakepark.owner_id
            print("Owner ID: ", owner_id)
            print("User ID: ", user_id)
            print("Superadmins", superadmins)
            if owner_id != user_id and user_id not in superadmins:
                raise AuthError(
                    {"code": "forbidden", "description": "Not resource owner."}, 403
                )

    if permission == "":
        return True

    if "permissions" not in payload or user_id is None:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT.",
            },
            400,
        )

    if permission not in payload["permissions"]:
        raise AuthError(
            {"code": "forbidden", "description": "Permission not found."}, 403
        )

    return True


def verify_decode_jwt(token):
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())

    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.JWTError:
        raise AuthError(
            {"code": "invalid_token", "description": "Token is invalid."}, 401
        )

    rsa_key = {}
    # check for kid (Auth0 key id)
    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        # check that JWT is valid
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=AUTH0_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            # determine if expired
            diff = payload["exp"] - int(time.time())

            if diff < 0:
                raise jwt.ExpiredSignatureError

            return payload
        # if not valid
        except jwt.ExpiredSignatureError:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            )

        except jwt.JWTClaimsError:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": """Incorrect claims. Please check the
                audience and issuer.""",
                },
                401,
            )
        except Exception:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            )
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


def requires_auth(permission=""):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            resource_id = kwargs.get("wakepark_id")
            try:
                payload = verify_decode_jwt(token)
            except ():
                abort(401)

            check_permissions(permission, payload, resource_id)

            return f(payload, *args, **kwargs)

        return wrapper

    return requires_auth_decorator

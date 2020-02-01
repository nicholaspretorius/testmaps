import json
import os

import requests

from project import db
from project.apis.users.models import User
from project.apis.wakeparks.models import Wakepark


def add_user(email, password):
    # deprectaed in favour of add_user pytest fixture
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_cablepark(name, description, lat, lng, instagram_handle):
    wakepark = Wakepark(
        name=name,
        description=description,
        lat=lat,
        lng=lng,
        instagram_handle=instagram_handle,
    )
    db.session.add(wakepark)
    db.session.commit()
    return wakepark


def recreate_db():
    db.session.remove()
    db.drop_all()
    db.create_all()


def get_auth0_access_token():
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_TEST_ID")
    secret = os.environ.get("AUTH0_SECRET")
    audience = os.environ.get("AUTH0_AUDIENCE")

    payload = {
        "client_id": client_id,
        "client_secret": secret,
        "audience": audience,
        "grant_type": "client_credentials",
    }

    headers = {"content-type": "application/json"}

    res = requests.post(
        f"https://{domain}/oauth/token",
        data=json.dumps(payload),
        headers=headers,
    )

    access_token = res.json()["access_token"]

    return access_token

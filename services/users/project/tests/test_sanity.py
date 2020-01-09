# import http.client
import json
import os
import requests

# import pytest


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
        f"https://{domain}/oauth/token", data=json.dumps(payload), headers=headers
    )

    access_token = res.json()["access_token"]

    return access_token


def test_sanity_check_all(test_app):
    access_token = get_auth0_access_token()
    client = test_app.test_client()

    res = client.get(
        f"/sanity/",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    print("Data: ", data)
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert "Riders!" in data["hello"]

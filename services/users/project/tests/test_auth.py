import json

import pytest
from flask import current_app

from project.tests.utils import recreate_db

# import time


def test_user_registration(test_app, test_db, add_user):
    client = test_app.test_client()

    res = client.post(
        f"/auth/register",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert res.content_type == "application/json"
    assert "test@test.com" in data["email"]
    assert "password" not in data


def test_user_registration_duplicate_email(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")

    client = test_app.test_client()
    res = client.post(
        f"/auth/register",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert res.content_type == "application/json"
    assert "Sorry, that email already exists." in data["message"]
    assert not data["status"]


@pytest.mark.parametrize(
    "payload, message",
    [
        ({}, "Invalid payload"),
        (
            {"email": "test", "password": "password"},
            "Please provide a valid email address",
        ),
        ({"email": "test@test.com"}, "Invalid payload"),
        ({"password": "password"}, "Invalid payload"),
        ({"email_address": "test@test.com"}, "Invalid payload"),
        ({"email": "test@test.com", "pass": "password"}, "Invalid payload"),
    ],
)
def test_user_registration_invalid_payload(test_app, test_db, payload, message):
    recreate_db()
    client = test_app.test_client()
    py = payload
    print("Payload: ", py)
    res = client.post(
        f"/auth/register", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert res.content_type == "application/json"
    assert message in data["message"]
    assert not data["status"]


def test_user_login(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")

    client = test_app.test_client()
    res = client.post(
        f"/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_user_login_not_registered(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"/auth/login",
        data=json.dumps({"email": "whaddayaknow@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert res.content_type == "application/json"
    assert "User does not exist." in data["message"]
    assert not data["status"]


def test_valid_refresh(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")
    client = test_app.test_client()

    res_login = client.post(
        f"/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res_login.data.decode())
    refresh_token = json.loads(res_login.data.decode())["refresh_token"]

    res = client.post(
        f"/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert data["access_token"]
    assert data["refresh_token"]


def test_invalid_refresh_expired_token(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")
    current_app.config["REFRESH_TOKEN_EXPIRATION"] = -1
    client = test_app.test_client()

    res_login = client.post(
        f"/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    # time.sleep(4)
    data = json.loads(res_login.data.decode())
    refresh_token = json.loads(res_login.data.decode())["refresh_token"]

    res_refresh = client.post(
        f"/auth/refresh",
        data=json.dumps({"refresh_token": refresh_token}),
        content_type="application/json",
    )

    data = json.loads(res_refresh.data.decode())
    assert res_refresh.status_code == 401
    assert res_refresh.content_type == "application/json"
    assert "Signature expired. Please login again." in data["message"]


def test_invalid_refresh_invalid_token(test_app, test_db, add_user):
    recreate_db()
    client = test_app.test_client()

    res_refresh = client.post(
        f"/auth/refresh",
        data=json.dumps({"refresh_token": "invalid"}),
        content_type="application/json",
    )

    data = json.loads(res_refresh.data.decode())
    assert res_refresh.status_code == 401
    assert res_refresh.content_type == "application/json"
    assert "Invalid token. Please login again." in data["message"]


def test_invalid_refresh_invalid_payload(test_app, test_db, add_user):
    recreate_db()
    client = test_app.test_client()

    res_refresh = client.post(
        f"/auth/refresh", data=json.dumps({}), content_type="application/json"
    )

    data = json.loads(res_refresh.data.decode())
    assert res_refresh.status_code == 400
    assert res_refresh.content_type == "application/json"
    assert "Invalid payload." in data["message"]


def test_user_status_valid(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")
    client = test_app.test_client()
    res_login = client.post(
        f"/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res_login.data.decode())
    access_token = json.loads(res_login.data.decode())["access_token"]

    res_status = client.get(
        f"/auth/status",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res_status.data.decode())
    assert res_status.status_code == 200
    assert res_status.content_type == "application/json"
    assert "test@test.com" in data["email"]
    assert "password" not in data


def test_user_status_invalid(test_app, test_db):
    recreate_db()
    client = test_app.test_client()

    res = client.get(
        f"/auth/status",
        headers={"Authorization": f"Bearer invalid"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert "Invalid token. Please login again." in data["message"]
    assert not data["status"]


def test_user_status_invalid_no_bearer(test_app, test_db):
    recreate_db()
    client = test_app.test_client()

    res = client.get(
        f"/auth/status",
        headers={"Authorization": f"invalid"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert "Invalid header." in data["message"]
    assert not data["status"]


def test_user_status_no_token(test_app, test_db):
    recreate_db()
    client = test_app.test_client()

    res = client.get(f"/auth/status", content_type="application/json")

    data = json.loads(res.data.decode())
    assert res.status_code == 403
    assert res.content_type == "application/json"
    assert "Access token required." in data["message"]
    assert not data["status"]


def test_user_status_expired_token(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")
    current_app.config["ACCESS_TOKEN_EXPIRATION"] = -1
    client = test_app.test_client()

    res_login = client.post(
        f"/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res_login.data.decode())
    access_token = json.loads(res_login.data.decode())["access_token"]

    res = client.get(
        f"/auth/status",
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert "Signature expired. Please login again." in data["message"]

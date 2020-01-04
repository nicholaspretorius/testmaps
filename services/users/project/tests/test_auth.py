import json
import pytest

from project.tests.utils import recreate_db

prefix = "/api/1"


def test_user_registration(test_app, test_db, add_user):
    client = test_app.test_client()

    res = client.post(
        f"{prefix}/auth/register",
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
        f"{prefix}/auth/register",
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
        f"{prefix}/auth/register",
        data=json.dumps(payload),
        content_type="application/json",
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
        f"{prefix}/auth/login",
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
        f"{prefix}/auth/login",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert res.content_type == "application/json"
    assert "User does not exist." in data["message"]
    assert not data["status"]

import json

from project import db
from project.apis.models import User

prefix = "/api/1"


def test_add_user(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert "test@test.com was added" in data["message"]
    assert "success" in data["status"]


def test_add_user_no_post_data(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/", data=json.dumps({}), content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "fail" in data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_no_email(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"website": "test@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "fail" in data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_duplicate_email(test_app, test_db):
    client = test_app.test_client()

    client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test@test.com"}),
        content_type="application/json",
    )

    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "fail" in data["status"]
    assert "Sorry, that email already exists." in data["message"]


def test_add_user_invalid_email(test_app, test_db):
    client = test_app.test_client()

    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert "fail" in data["status"]
    assert "Please provide a valid email address" in data["message"]


def test_single_user(test_app, test_db):
    user = User(email="test@test.com")
    db.session.add(user)
    db.session.commit()

    client = test_app.test_client()
    res = client.get(f"{prefix}/users/{user.id}")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert str(user.id) in data["id"]
    assert "test@test.com" in data["email"]


def test_single_user_not_found(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"{prefix}/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]


def test_single_user_no_id(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"{prefix}/users/test")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert "fail" in data["status"]
    assert "User does not exist" in data["message"]

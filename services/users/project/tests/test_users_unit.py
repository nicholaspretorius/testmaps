import json
from datetime import datetime

import pytest

import project.apis.users.views

prefix = "/api/1"


def test_add_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_create_user(email, password):
        return True

    monkeypatch.setattr(
        project.apis.users.views, "get_user_by_email", mock_get_user_by_email
    )
    monkeypatch.setattr(project.apis.users.views, "create_user", mock_create_user)

    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test1@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert "test1@test.com was added" in data["message"]
    assert data["status"]


def test_add_user_no_post_data(test_app, monkeypatch):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/", data=json.dumps({}), content_type="application/json"
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_no_email(test_app, monkeypatch):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"website": "website@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_duplicate_email(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return True

    def mock_create_user(email, password):
        return True

    monkeypatch.setattr(
        project.apis.users.views, "get_user_by_email", mock_get_user_by_email
    )
    monkeypatch.setattr(project.apis.users.views, "create_user", mock_create_user)

    client = test_app.test_client()

    client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Sorry, that email already exists." in data["message"]


def test_add_user_invalid_email(test_app, monkeypatch):
    client = test_app.test_client()

    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Please provide a valid email address" in data["message"]


def test_single_user(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return {
            "id": 1,
            "email": "test@test.com",
            "created_date": datetime.now(),
            "active": True,
        }

    monkeypatch.setattr(project.apis.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    res = client.get(f"{prefix}/users/1")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert "1" in data["id"]
    assert "test@test.com" in data["email"]


def test_single_user_not_found(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.apis.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    res = client.get(f"{prefix}/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_single_user_no_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.apis.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    res = client.get(f"{prefix}/users/test")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_get_all_users(test_app, monkeypatch):
    pass


def test_delete_user(test_app, monkeypatch):
    pass


def test_delete_user_not_found(test_app, monkeypatch):
    pass


def test_update_user(test_app, monkeypatch):
    pass


@pytest.mark.parametrize(
    "user_id, payload, status_code, message",
    [
        [1, {}, 400, "Invalid payload"],
        [1, {"blah": "test@test.com"}, 400, "Invalid payload"],
        [999, {"email": "test_updated@test.com"}, 404, "Resource not found"],
    ],
)
def test_update_user_invalid(
    test_app, monkeypatch, user_id, payload, status_code, message
):
    pass

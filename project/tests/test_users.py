import json

from project.tests.utils import add_user, recreate_db

prefix = "/api/1"


def test_add_user(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test1@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert "test1@test.com was added" in data["message"]
    assert data["status"]


def test_add_user_no_post_data(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/", data=json.dumps({}), content_type="application/json"
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_no_email(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"website": "website@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_duplicate_email(test_app, test_db):
    recreate_db()
    client = test_app.test_client()

    client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test2@test.com"}),
        content_type="application/json",
    )

    res = client.post(
        f"{prefix}/users/",
        data=json.dumps({"email": "test2@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
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
    assert not data["status"]
    assert "Please provide a valid email address" in data["message"]


def test_single_user(test_app, test_db):
    recreate_db()
    user = add_user("test3@test.com")

    client = test_app.test_client()
    res = client.get(f"{prefix}/users/{user.id}")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert str(user.id) in data["id"]
    assert "test3@test.com" in data["email"]


def test_single_user_not_found(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"{prefix}/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_single_user_no_id(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"{prefix}/users/test")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_get_all_users(test_app, test_db):
    recreate_db()
    client = test_app.test_client()
    add_user("test4@test.com")
    add_user("test5@test.com")

    res = client.get(f"{prefix}/users/")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert len(data) == 2
    assert "test4@test.com" in data[0]["email"]
    assert "test5@test.com" in data[1]["email"]

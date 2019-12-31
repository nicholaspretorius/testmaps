import json

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

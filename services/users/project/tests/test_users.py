import json

from project.tests.utils import recreate_db


def test_add_user(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"/users/",
        data=json.dumps({"email": "test1@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert "test1@test.com was added" in data["message"]
    assert data["status"]


def test_add_user_no_post_data(test_app, test_db):
    client = test_app.test_client()
    res = client.post(f"/users/", data=json.dumps({}), content_type="application/json")

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_no_email(test_app, test_db):
    client = test_app.test_client()
    res = client.post(
        f"/users/",
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
        f"/users/",
        data=json.dumps({"email": "test2@test.com", "password": "password"}),
        content_type="application/json",
    )

    res = client.post(
        f"/users/",
        data=json.dumps({"email": "test2@test.com", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Sorry, that email already exists." in data["message"]


def test_add_user_invalid_email(test_app, test_db):
    client = test_app.test_client()

    res = client.post(
        f"/users/",
        data=json.dumps({"email": "test", "password": "password"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Please provide a valid email address" in data["message"]


def test_single_user(test_app, test_db, add_user):
    recreate_db()
    user = add_user("test3@test.com", "password")

    client = test_app.test_client()
    res = client.get(f"/users/{user.id}")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert str(user.id) in data["id"]
    assert "test3@test.com" in data["email"]
    assert "password" not in data


def test_single_user_not_found(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_single_user_no_id(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"/users/test")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_get_all_users(test_app, test_db, add_user):
    recreate_db()
    client = test_app.test_client()
    add_user("test4@test.com", "password")
    add_user("test5@test.com", "password")

    res = client.get(f"/users/")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert len(data) == 2
    assert "test4@test.com" in data[0]["email"]
    assert "test5@test.com" in data[1]["email"]
    assert "password" not in data[0]
    assert "password" not in data[1]


def test_delete_user(test_app, test_db, add_user):
    recreate_db()
    add_user("test@test.com", "password")
    client = test_app.test_client()
    res_one = client.get(f"/users/")
    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 200
    assert len(data) == 1

    res_two = client.delete(f"/users/1")
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 200
    assert data["status"]
    assert "User was deleted." in data["message"]

    res_three = client.get(f"/users/")
    data = json.loads(res_three.data.decode())
    assert res_three.status_code == 200
    assert len(data) == 0


def test_delete_user_not_found(test_app, test_db):
    client = test_app.test_client()
    res = client.delete(f"/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_update_user(test_app, test_db, add_user):
    recreate_db()
    user = add_user("test@test.com", "password")
    client = test_app.test_client()
    res_one = client.put(
        f"/users/{user.id}",
        data=json.dumps({"email": "test_updated@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 200
    assert data["status"]
    assert "User successfully updated." in data["message"]
    assert data["user"]

    res_two = client.get(f"/users/{user.id}")
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 200
    assert "test_updated@test.com" in data["email"]


def test_update_user_not_found(test_app, test_db):
    recreate_db()
    client = test_app.test_client()
    res = client.put(
        f"/users/999",
        data=json.dumps({"email": "test_updated@test.com"}),
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_update_user_invalid_json(test_app, test_db, add_user):
    recreate_db()
    user = add_user("test@test.com", "password")
    client = test_app.test_client()
    res = client.put(
        f"/users/{user.id}", data=json.dumps({}), content_type="application/json"
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_update_user_invalid_json_keys(test_app, test_db, add_user):
    recreate_db()
    user = add_user("test@test.com", "password")
    client = test_app.test_client()
    res = client.put(
        f"/users/{user.id}",
        data=json.dumps({"blah": "test_updated@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]

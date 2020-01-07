import json
from datetime import datetime

import project.apis.users.views
from project import bcrypt
from project.apis.users.services import get_user_by_id


class MockResponsePost:
    @staticmethod
    def to_json():
        return {"id": 1, "email": "test@test.com"}


class MockResponsePut:
    @staticmethod
    def to_json():
        return {"id": 1, "email": "update@test.com"}


def test_add_user(test_app, monkeypatch):
    def mock_get_user_by_email(email):
        return None

    def mock_create_user(email, password):
        return MockResponsePost()

    monkeypatch.setattr(
        project.apis.users.views, "get_user_by_email", mock_get_user_by_email
    )
    monkeypatch.setattr(project.apis.users.views, "create_user", mock_create_user)

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


def test_add_user_no_post_data(test_app, monkeypatch):
    client = test_app.test_client()
    res = client.post(f"/users/", data=json.dumps({}), content_type="application/json")

    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert not data["status"]
    assert "Invalid payload" in data["message"]


def test_add_user_no_email(test_app, monkeypatch):
    client = test_app.test_client()
    res = client.post(
        f"/users/",
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
        f"/users/",
        data=json.dumps({"email": "test@test.com", "password": "password"}),
        content_type="application/json",
    )

    res = client.post(
        f"/users/",
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
        f"/users/",
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
    res = client.get(f"/users/1")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert "1" in data["id"]
    assert "test@test.com" in data["email"]
    assert "password" not in data


def test_single_user_not_found(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.apis.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    res = client.get(f"/users/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_single_user_no_id(test_app, monkeypatch):
    def mock_get_user_by_id(user_id):
        return None

    monkeypatch.setattr(project.apis.users.views, "get_user_by_id", mock_get_user_by_id)

    client = test_app.test_client()
    res = client.get(f"/users/test")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_get_all_users(test_app, test_db, monkeypatch, add_user):
    def mock_get_users():
        return [
            {"id": "1", "email": "test@test.com"},
            {"id": "2", "email": "test1@test.com"},
        ]

    monkeypatch.setattr(project.apis.users.views, "get_users", mock_get_users)

    client = test_app.test_client()
    add_user("test@test.com", "password")
    add_user("test1@test.com", "password")

    res = client.get(f"/users/")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert len(data) == 2
    assert "test@test.com" in data[0]["email"]
    assert "test1@test.com" in data[1]["email"]
    assert "password" not in data[0]
    assert "password" not in data[1]


def test_delete_user(test_app, monkeypatch):
    pass


def test_delete_user_not_found(test_app, monkeypatch):
    pass


def test_update_user(test_app, monkeypatch):
    class AttrDict(dict):
        def __init__(self, *args, **kwargs):
            super(AttrDict, self).__init__(*args, **kwargs)
            self.__dict__ = self

    def mock_get_user_by_id(user_id):
        d = AttrDict()
        # TODO: Need to check whether this is *really* testing update...
        d.update({"id": 1, "email": "update@test.com"})
        return d

    def mock_update_user(user, email):
        return MockResponsePut()

    monkeypatch.setattr(project.apis.users.views, "get_user_by_id", mock_get_user_by_id)
    monkeypatch.setattr(project.apis.users.views, "update_user", mock_update_user)

    client = test_app.test_client()
    res_one = client.put(
        f"/users/1",
        data=json.dumps({"email": "update@test.com"}),
        content_type="application/json",
    )
    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 200
    assert data["status"]
    assert "User successfully updated." in data["message"]
    assert data["user"]

    res_two = client.get(f"/users/1")
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 200
    assert "update@test.com" in data["email"]


def test_update_user_with_password(test_app, test_db, add_user):
    # check password is NOT updated when updating user
    password_one = "password"
    password_two = "something"

    user = add_user("test@test.com", password_one)
    assert bcrypt.check_password_hash(user.password, password_one)

    client = test_app.test_client()
    res = client.put(
        f"/users/{user.id}",
        data=json.dumps({"email": "update@test.com", "password": password_two}),
        content_type="application/json",
    )

    assert res.status_code == 200

    user = get_user_by_id(user.id)
    assert bcrypt.check_password_hash(user.password, password_one)
    assert not bcrypt.check_password_hash(user.password, password_two)


# @pytest.mark.parametrize(
#     "user_id, payload, status_code, message",
#     [
#         [1, {}, 400, "Invalid payload"],
#         [1, {"blah": "test@test.com"}, 400, "Invalid payload"],
#         [999, {"email": "test_updated@test.com"}, 404, "Resource not found"],
#     ],
# )
# def test_update_user_invalid(
#     test_app, monkeypatch, user_id, payload, status_code, message
# ):
#     pass

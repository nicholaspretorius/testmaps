import json

prefix = "/api/1"


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    res = client.post(
        f"{prefix}/users",
        data=json.dumps({"email": "test@test.com"}),
        content_type="application/json",
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert "test@test.com was added" in data["message"]
    assert "success" in data["status"]

import json


def test_hello(test_app):
    client = test_app.test_client()
    res = client.get(f"/hello/")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert "success" in data["status"]
    assert "world!" in data["hello"]

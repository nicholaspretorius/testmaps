import json
import pytest

from project.tests.utils import recreate_db


def test_get_all_wakeparks(test_app, test_db, add_wakepark):
    recreate_db()
    client = test_app.test_client()
    add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )
    add_wakepark(
        "Blue Rock",
        "Awesome 5-Tower cablepark with Unit Parktech features!",
        -25.952558,
        28.185543,
        "blue_rock_waterski",
    )

    res = client.get(f"/wakeparks/")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert len(data) == 2


def test_get_single_wakepark(test_app, test_db, add_wakepark):
    recreate_db()
    client = test_app.test_client()
    wakepark = add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )
    client = test_app.test_client()
    id = wakepark.id
    print("Id: ", id)
    res = client.get(f"/wakeparks/{wakepark.id}")
    data = json.loads(res.data.decode())
    assert res.status_code == 200
    assert res.content_type == "application/json"
    assert "Stoke City Wakepark" in data["name"]
    assert 1 == int(data["id"])


def test_get_single_wakepark_not_found(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"/wakeparks/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_single_wakepark_no_id(test_app, test_db):
    client = test_app.test_client()
    res = client.get(f"/wakeparks/test")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]


def test_add_wakepark(test_app, test_db):
    client = test_app.test_client()

    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only cablepark in Gauteng!",
        "location": {"lat": -25.952558, "lng": 28.185543},
        "social": {"instagram": "stokecitywake"},
    }

    res = client.post(
        "/wakeparks/", data=json.dumps(wakepark), content_type="application/json"
    )

    data = json.loads(res.data.decode())
    assert res.status_code == 201
    assert wakepark["name"] in data["name"]


@pytest.mark.parametrize(
    "payload, message",
    [
        ({}, "Input payload validation failed"),
        (
            {"description": "Cool wakepark!", "location": {"lat": 23, "lng": 99}},
            "Input payload validation failed",
        ),
    ],
)
def test_create_wakepark_invalid_payload(test_app, test_db, payload, message):
    recreate_db()
    client = test_app.test_client()
    res = client.post(
        "/wakeparks/", data=json.dumps(payload), content_type="application/json"
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert res.content_type == "application/json"
    assert message in data["message"]
    assert data["errors"]


def test_delete_wakepark(test_app, test_db, add_wakepark):
    recreate_db()
    add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )
    client = test_app.test_client()
    res_one = client.get("/wakeparks/")
    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 200
    assert res_one.content_type == "application/json"
    assert len(data) == 1

    res_two = client.delete(f"/wakeparks/1")
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 200
    assert res_two.content_type == "application/json"
    assert data["status"]
    assert "Wakepark was deleted" in data["message"]
    assert data["wakepark"]

    res_three = client.get("/wakeparks/")
    data = json.loads(res_three.data.decode())
    assert res_three.status_code == 200
    assert res_three.content_type == "application/json"
    assert len(data) == 0


def test_delete_wakepark_not_found(test_app, test_db):
    client = test_app.test_client()
    res = client.delete(f"/wakeparks/999")
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert not data["status"]
    assert "Resource not found" in data["message"]

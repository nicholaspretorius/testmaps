import json
import pytest

from project.tests.utils import get_auth0_access_token, recreate_db


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


access_token = get_auth0_access_token()  # get access_token for requires_auth routes


def test_add_wakepark(test_app, test_db):

    client = test_app.test_client()

    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only cablepark in Gauteng!",
        "location": {"lat": -25.952558, "lng": 28.185543},
        "social": {"instagram": "stokecitywake"},
    }

    res = client.post(
        "/wakeparks/",
        data=json.dumps(wakepark),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
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
        "/wakeparks/",
        data=json.dumps(payload),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 400
    assert res.content_type == "application/json"
    assert message in data["message"]
    assert data["errors"]


new_wakepark = {
    "name": "Stoke City Wakepark",
    "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
    "location": {"lat": -25.952558, "lng": 28.185543},
    "social": {"instagram": "stokecitywake"},
}


@pytest.mark.parametrize(
    "payload, headers, code, description",
    [
        (new_wakepark,
            {},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        (new_wakepark,
            {"X-Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        (new_wakepark,
            {"Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        (new_wakepark,
            {"Authorisation": f"Bearer invalid"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        (new_wakepark,
            {"Authorisation": f"Bearer"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        (new_wakepark,
            {"Authorisation": f"Token {access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
    ],
)
def test_create_wakepark_unauthorised(test_app,
                                      test_db, payload, headers, code, description):
    recreate_db()

    client = test_app.test_client()
    res = client.post(
        "/wakeparks/",
        data=json.dumps(payload),
        headers=headers,
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 401
    assert res.content_type == "application/json"
    assert description in data["description"]
    assert code in data["code"]


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

    res_two = client.delete(
        f"/wakeparks/1", headers={"Authorization": f"Bearer {access_token}"}
    )
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
    res = client.delete(
        f"/wakeparks/999", headers={"Authorization": f"Bearer {access_token}"}
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert res.content_type == "application/json"
    assert not data["status"]
    assert "Resource not found" in data["message"]


@pytest.mark.parametrize(
    "headers, code, description",
    [
        ({},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"X-Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Bearer invalid"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Bearer"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Token {access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
    ],
)
def test_delete_wakepark_unauthorised(test_app, test_db,
                                      add_wakepark, headers, code, description):
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

    res_two = client.delete(
        f"/wakeparks/1", headers=headers
    )
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 401
    assert res_two.content_type == "application/json"
    assert description in data["description"]
    assert code in data["code"]


def test_update_wakepark(test_app, test_db, add_wakepark):
    recreate_db()

    # initial wakepark
    new_wakepark = add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )

    # updated wakepark
    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
        "location": {"lat": -25.952558, "lng": 28.185543},
        "social": {"instagram": "stokecitywake"},
    }

    client = test_app.test_client()
    res_one = client.put(
        f"/wakeparks/{new_wakepark.id}",
        data=json.dumps(wakepark),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 200
    assert res_one.content_type == "application/json"
    assert data["status"]
    assert "Wakepark successfully updated" in data["message"]
    assert data["wakepark"]

    res_two = client.get(f"/wakeparks/{new_wakepark.id}")
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 200
    assert res_two.content_type == "application/json"
    assert "The only 5 Tower and 2 Tower cablepark in Gauteng!" in data["description"]


def test_update_wakepark_not_found(test_app, test_db):

    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
        "location": {"lat": -25.952558, "lng": 28.185543},
        "social": {"instagram": "stokecitywake"},
    }

    recreate_db()
    client = test_app.test_client()
    res = client.put(
        f"/wakeparks/999",
        data=json.dumps(wakepark),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert res.content_type == "application/json"
    assert not data["status"]
    assert "Resource not found" in data["message"]


@pytest.mark.parametrize(
    "headers, code, description",
    [
        ({},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"X-Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Bearer invalid"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Bearer"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Token {access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
    ],
)
def test_update_wakepark_unauthorised(test_app, test_db,
                                      add_wakepark, headers, code, description):
    recreate_db()

    # initial wakepark
    new_wakepark = add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )

    # updated wakepark
    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
        "location": {"lat": -25.952558, "lng": 28.185543},
        "social": {"instagram": "stokecitywake"},
    }

    client = test_app.test_client()
    res_one = client.put(
        f"/wakeparks/{new_wakepark.id}",
        data=json.dumps(wakepark),
        headers=headers,
        content_type="application/json",
    )

    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 401
    assert res_one.content_type == "application/json"
    assert description in data["description"]
    assert code in data["code"]


def test_patch_wakepark(test_app, test_db, add_wakepark):
    recreate_db()

    # initial wakepark
    new_wakepark = add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )

    # updated wakepark
    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
        "lat": -25.952558,
        "lng": 28.185543,
        "instagram_handle": "stokecitywake",
    }

    client = test_app.test_client()
    res_one = client.patch(
        f"/wakeparks/{new_wakepark.id}",
        data=json.dumps(wakepark),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )

    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 200
    assert res_one.content_type == "application/json"
    assert data["status"]
    assert "Wakepark successfully updated" in data["message"]
    assert data["wakepark"]

    res_two = client.get(f"/wakeparks/{new_wakepark.id}")
    data = json.loads(res_two.data.decode())
    assert res_two.status_code == 200
    assert res_two.content_type == "application/json"
    assert "The only 5 Tower and 2 Tower cablepark in Gauteng!" in data["description"]


def test_patch_wakepark_not_found(test_app, test_db):

    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
        "location": {"lat": -25.952558, "lng": 28.185543},
        "social": {"instagram": "stokecitywake"},
    }

    recreate_db()
    client = test_app.test_client()
    res = client.patch(
        f"/wakeparks/999",
        data=json.dumps(wakepark),
        headers={"Authorization": f"Bearer {access_token}"},
        content_type="application/json",
    )
    data = json.loads(res.data.decode())
    assert res.status_code == 404
    assert res.content_type == "application/json"
    assert not data["status"]
    assert "Resource not found" in data["message"]


@pytest.mark.parametrize(
    "headers, code, description",
    [
        ({},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"X-Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"{access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Bearer invalid"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Bearer"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
        ({"Authorisation": f"Token {access_token}"},
            "authorisation_header_not_found",
            "Authorisation header not found."),
    ],
)
def test_patch_wakepark_unauthorised(test_app, test_db,
                                     add_wakepark, headers, code, description):
    recreate_db()

    # initial wakepark
    new_wakepark = add_wakepark(
        "Stoke City Wakepark",
        "The only cablepark in Gauteng!",
        -25.952558,
        28.185543,
        "stokecitywake",
    )

    # updated wakepark
    wakepark = {
        "name": "Stoke City Wakepark",
        "description": "The only 5 Tower and 2 Tower cablepark in Gauteng!",
        "lat": -25.952558,
        "lng": 28.185543,
        "instagram_handle": "stokecitywake",
    }

    client = test_app.test_client()
    res_one = client.patch(
        f"/wakeparks/{new_wakepark.id}",
        data=json.dumps(wakepark),
        headers=headers,
        content_type="application/json",
    )

    data = json.loads(res_one.data.decode())
    assert res_one.status_code == 401
    assert res_one.content_type == "application/json"
    assert description in data["description"]
    assert code in data["code"]

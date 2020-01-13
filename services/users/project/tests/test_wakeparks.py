import json

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
    assert len(data) == 2

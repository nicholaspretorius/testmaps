def test_repr(test_app, test_db, add_cablepark):
    cablepark = add_cablepark(
        name="Stoke City Wakepark",
        description="The only cable wakepark in Gauteng!",
        lat=-25.952558,
        lng=28.185543,
        instagram_handle="stokecitywake",
    )
    val = repr(cablepark)
    assert (
        val
        == "<Cablepark id: 1, name: Stoke City Wakepark lat: -25.952558, lng: 28.185543 >"
    )

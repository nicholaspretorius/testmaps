def test_repr(test_app, test_db, add_wakepark):
    wakepark = add_wakepark(
        name="Stoke City Wakepark",
        description="The only cable wakepark in Gauteng!",
        lat=-25.952558,
        lng=28.185543,
        instagram_handle="stokecitywake",
        owner_id="google-oauth2|104755831296456998532",
    )
    val = repr(wakepark)
    assert (
        val
        == """<Wakepark id: 1,
              name: Stoke City Wakepark
              owner_id: google-oauth2|104755831296456998532>"""
    )

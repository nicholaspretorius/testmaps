prefix = "/api/1"


def test_password_are_random(test_app, test_db, add_user):
    user_one = add_user("test@test.com", "password")
    user_two = add_user("test2@test.com", "password")
    assert user_one.password != user_two.password

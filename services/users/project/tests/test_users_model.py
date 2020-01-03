from project.apis.users.models import User

prefix = "/api/1"


def test_password_are_random(test_app, test_db, add_user):
    user_one = add_user("test@test.com", "password")
    user_two = add_user("test2@test.com", "password")
    assert user_one.password != user_two.password


def test_encode_token(test_app, test_db, add_user):
    user = add_user("test@test.com", "password")
    token = user.encode_token(user.id, "access")
    assert isinstance(token, bytes)


def test_decode_token(test_app, test_db, add_user):
    user = add_user("test@test.com", "password")
    token = user.encode_token(user.id, "access")
    assert isinstance(token, bytes)
    assert User.decode_token(token) == user.id

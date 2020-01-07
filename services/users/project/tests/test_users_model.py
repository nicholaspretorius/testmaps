from project.apis.users.models import User


def test_repr(test_app, test_db, add_user):
    user = add_user(email="test@test.com", password="password")
    val = repr(user)
    assert val == "<User id: 1, email: test@test.com>"


def test_password_are_random(test_app, test_db, add_user):
    user_one = add_user("test@test.com", "password")
    user_two = add_user("test2@test.com", "password")
    assert user_one.password != user_two.password


def test_encode_token(test_app, test_db, add_user):
    user = add_user("test@test.com", "password")
    token = user.encode_token(user.id, "access")
    assert isinstance(token, bytes)

    token_two = user.encode_token(user.id, "refresh")
    assert isinstance(token_two, bytes)


def test_decode_token(test_app, test_db, add_user):
    user = add_user("test@test.com", "password")
    token = user.encode_token(user.id, "access")
    assert isinstance(token, bytes)
    assert User.decode_token(token) == user.id

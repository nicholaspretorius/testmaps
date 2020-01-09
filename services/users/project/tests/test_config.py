import os


def test_development_config(test_app):
    test_app.config.from_object("project.config.DevelopmentConfig")
    assert test_app.config["SECRET_KEY"] == os.environ.get("SECRET_KEY")
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000
    assert test_app.config["AUTH0_DOMAIN"] == os.environ.get("AUTH0_DOMAIN")
    assert test_app.config["AUTH0_AUDIENCE"] == os.environ.get("AUTH0_AUDIENCE")
    assert test_app.config["ALGORITHMS"] == ["RS256"]


def test_testing_config(test_app):
    test_app.config.from_object("project.config.TestingConfig")
    assert test_app.config["SECRET_KEY"] == os.environ.get("SECRET_KEY")
    assert test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get(
        "DATABASE_TEST_URL"
    )
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 4
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 3
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 3
    assert test_app.config["AUTH0_DOMAIN"] == os.environ.get("AUTH0_DOMAIN")
    assert test_app.config["AUTH0_AUDIENCE"] == os.environ.get("AUTH0_AUDIENCE")
    assert test_app.config["AUTH0_SECRET"] == os.environ.get("AUTH0_SECRET")
    assert test_app.config["AUTH0_CLIENT_TEST_ID"] == os.environ.get(
        "AUTH0_CLIENT_TEST_ID"
    )
    assert test_app.config["ALGORITHMS"] == ["RS256"]


def test_production_config(test_app):
    test_app.config.from_object("project.config.ProductionConfig")
    assert test_app.config["SECRET_KEY"] == os.environ.get("SECRET_KEY")
    assert not test_app.config["TESTING"]
    assert test_app.config["SQLALCHEMY_DATABASE_URI"] == os.environ.get("DATABASE_URL")
    assert test_app.config["BCRYPT_LOG_ROUNDS"] == 13
    assert test_app.config["ACCESS_TOKEN_EXPIRATION"] == 900
    assert test_app.config["REFRESH_TOKEN_EXPIRATION"] == 2592000
    assert test_app.config["AUTH0_DOMAIN"] == os.environ.get("AUTH0_DOMAIN")
    assert test_app.config["AUTH0_AUDIENCE"] == os.environ.get("AUTH0_AUDIENCE")
    assert test_app.config["ALGORITHMS"] == ["RS256"]

# project/config.py
import os


class BaseConfig:
    """Base config"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ERROR_404_HELP = False
    # remove auto extra wording at end of abort() response
    BCRYPT_LOG_ROUNDS = 13
    ACCESS_TOKEN_EXPIRATION = 900  # 15 minutes
    REFRESH_TOKEN_EXPIRATION = 2592000  # 30 days
    # set Auth0
    AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
    AUTH0_AUDIENCE = os.environ.get("AUTH0_AUDIENCE")
    ALGORITHMS = ["RS256"]


class DevelopmentConfig(BaseConfig):
    """Development config"""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    BCRYPT_LOG_ROUNDS = 4


class TestingConfig(BaseConfig):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")
    BCRYPT_LOG_ROUNDS = 4
    ACCESS_TOKEN_EXPIRATION = 3
    REFRESH_TOKEN_EXPIRATION = 3
    AUTH0_SECRET = os.environ.get("AUTH0_SECRET")
    AUTH0_CLIENT_TEST_ID = os.environ.get("AUTH0_CLIENT_TEST_ID")


class ProductionConfig(BaseConfig):
    """Production config"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

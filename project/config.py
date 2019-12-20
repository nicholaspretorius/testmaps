# project/config.py
import os


class BaseConfig:
    """Base config"""

    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "test"


class DevelopmentConfig(BaseConfig):
    """Development config"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class TestingConfig(BaseConfig):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_TEST_URL")


class ProductionConfig(BaseConfig):
    """Production config"""

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")

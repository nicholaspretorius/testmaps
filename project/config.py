# project/config.py


class BaseConfig:
    """Base config"""

    TESTING = False


class DevelopmentConfig(BaseConfig):
    """Development config"""

    pass


class TestingConfig(BaseConfig):
    """Testing config"""

    TESTING = True


class ProductionConfig(BaseConfig):
    pass

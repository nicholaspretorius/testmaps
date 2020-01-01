import pytest

from project import create_app, db


# everything before yield is 'setup' and after yield is 'teardown'
@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app  # testing happens here


@pytest.fixture(scope="module")
def test_db():
    db.create_all()
    yield db  # testing happens here
    db.session.remove()
    db.drop_all()
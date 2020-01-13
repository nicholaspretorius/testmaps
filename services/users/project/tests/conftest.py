import pytest

from project import create_app, db
from project.apis.users.models import User
from project.apis.wakeparks.models import Wakepark


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


@pytest.fixture(scope="module")
def add_user():
    def _add_user(email, password):
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user

    return _add_user


@pytest.fixture(scope="module")
def add_wakepark():
    def _add_wakepark(name, description, lat, lng, instagram_handle):
        wakepark = Wakepark(
            name=name,
            description=description,
            lat=lat,
            lng=lng,
            instagram_handle=instagram_handle,
        )
        db.session.add(wakepark)
        db.session.commit()
        return wakepark

    return _add_wakepark

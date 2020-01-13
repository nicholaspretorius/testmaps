from project import db
from project.apis.users.models import User
from project.apis.wakeparks.models import Wakepark


def add_user(email, password):
    # deprectaed in favour of add_user pytest fixture
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def add_cablepark(name, description, lat, lng, instagram_handle):
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


def recreate_db():
    db.session.remove()
    db.drop_all()
    db.create_all()

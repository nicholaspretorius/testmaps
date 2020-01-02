from project import db
from project.apis.users.models import User


def add_user(email, password):
    # deprectaed in favour of add_user pytest fixture
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return user


def recreate_db():
    db.session.remove()
    db.drop_all()
    db.create_all()

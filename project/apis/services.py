from project import db
from project.apis.models import User


def get_users():
    return [user.to_json() for user in User.query.all()]


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def create_user(email):
    new_user = User(email=email)
    db.session.add(new_user)
    db.session.commit()
    return new_user

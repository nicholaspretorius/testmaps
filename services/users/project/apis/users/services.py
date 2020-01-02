from project import db
from project.apis.users.models import User


def get_users():
    return [user.to_json() for user in User.query.all()]


def get_user_by_email(email):
    return User.query.filter_by(email=email).first()


def get_user_by_id(id):
    user = User.query.filter_by(id=int(id)).first()
    return user


def delete_user(user):
    db.session.delete(user)
    db.session.commit()
    return user


def update_user(user, email):
    user.email = email
    db.session.commit()
    return user


def create_user(email, password):
    new_user = User(email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

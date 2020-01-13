from flask.cli import FlaskGroup

from project import create_app, db

from project.apis.users.models import User
from project.apis.wakeparks.models import Wakepark

app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    """Recreates the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    """Seeds the database."""
    db.session.add(User(email="test@test.com", password="password"))
    db.session.add(User(email="another@test.com", password="password"))
    db.session.add(
        Wakepark(
            name="Stoke City Wakepark",
            description="The only cable wakepark in Gauteng!",
            lat=-25.952558,
            lng=28.185543,
            instagram_handle="stokecitywake",
        )
    )
    db.session.commit()


@cli.command("reset_db")
def reset_db():
    """Recreates and seeds the database."""
    db.drop_all()
    db.create_all()
    db.session.add(User(email="test@test.com", password="password"))
    db.session.add(User(email="another@test.com", password="password"))
    db.session.commit()


if __name__ == "__main__":
    cli()

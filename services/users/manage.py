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
            owner_id="google-oauth2|104755831296456998532",
        )
    )
    db.session.add(
        Wakepark(
            name="Blue Rock",
            description="Wakepark in Cape Town with Unit Parktech features!",
            lat=-34.126774,
            lng=18.901148,
            instagram_handle="blue_rock_waterski",
            owner_id="auth0|5ddb7e53ecc37b0ef0912ab8",
        )
    )
    db.session.add(
        Wakepark(
            name="Forever Resorts",
            description="Beginner friendly wakepark in Bela-Bela.",
            lat=-24.889612,
            lng=28.290278,
            instagram_handle="forever-resorts",
            owner_id="google-oauth2|104755831296456998532",
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

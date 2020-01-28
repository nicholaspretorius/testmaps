from sqlalchemy.sql import func

from project import db


class Wakepark(db.Model):

    __tablename__ = "wakeparks"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    lat = db.Column(db.Float(), nullable=True)
    lng = db.Column(db.Float(), nullable=True)
    instagram_handle = db.Column(db.String(128), nullable=True)
    owner_id = db.Column(db.String(), default=True, nullable=False)

    def __init__(
        self,
        name="",
        lat="",
        lng="",
        description="",
        instagram_handle="",
        owner_id="google-oauth2|104755831296456998532",
    ):
        self.name = name
        self.description = description
        self.lat = lat
        self.lng = lng
        self.instagram_handle = instagram_handle
        self.owner_id = owner_id

    def __repr__(self):
        return f"<Wakepark id: {self.id}, name: {self.name} owner_id: {self.owner_id}>"

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_id": self.owner_id,
            "location": {"lat": self.lat, "lng": self.lng},
            "description": self.description,
            "social": {
                "instagram": f"https://www.instagram.com/{self.instagram_handle}"
            },
        }

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
            "description": self.description,
            "instagram_handle": self.instagram_handle,
            "owner_id": self.owner_id,
        }

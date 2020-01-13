from project import db
from project.apis.wakeparks.models import Wakepark


def get_wakeparks():
    return [wakepark.to_json() for wakepark in Wakepark.query.all()]


def get_wakepark_by_id(id):
    wakepark = Wakepark.query.filter_by(id=int(id)).first()
    if wakepark is None:
        return None

    return wakepark.to_json()


def create_wakepark(name, description, lat, lng, instagram_handle):
    new_wakepark = Wakepark(
        name=name,
        description=description,
        lat=lat,
        lng=lng,
        instagram_handle=instagram_handle,
    )
    db.session.add(new_wakepark)
    db.session.commit()
    return new_wakepark

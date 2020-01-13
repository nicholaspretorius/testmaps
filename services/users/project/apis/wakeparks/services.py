# from project import db
from project.apis.wakeparks.models import Wakepark


def get_wakeparks():
    return [wakepark.to_json() for wakepark in Wakepark.query.all()]


def get_wakepark_by_id(id):
    wakepark = Wakepark.query.filter_by(id=int(id)).first()
    if wakepark is None:
        return None

    return wakepark.to_json()

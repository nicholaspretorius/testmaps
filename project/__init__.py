import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# import sys
# print(app.config, file=sys.stderr)


db = SQLAlchemy()


def create_app(script_info=None):

    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)

    from project.apis import blueprint as api

    app.register_blueprint(api, url_prefix="/api/1")

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app


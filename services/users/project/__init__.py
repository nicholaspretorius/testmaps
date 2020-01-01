import os
from flask import Flask, jsonify
from flask_admin import Admin
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# import sys
# print(app.config, file=sys.stderr)


db = SQLAlchemy()
cors = CORS()
admin = Admin(template_mode="bootstrap3")


def create_app(script_info=None):

    app = Flask(__name__)

    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})

    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    from project.apis import blueprint as api

    app.register_blueprint(api, url_prefix=app.config["API_PREFIX"])

    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": False, "message": "Resource not found"}), 404

    return app
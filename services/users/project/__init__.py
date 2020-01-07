import os
from flask import Flask, jsonify
from flask_admin import Admin
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

# import sys
# print(app.config, file=sys.stderr)

db = SQLAlchemy()
cors = CORS()
bcrypt = Bcrypt()
admin = Admin(name="Testmaps", template_mode="bootstrap3")


def create_app(script_info=None):

    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # setup extensions
    db.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    bcrypt.init_app(app)

    if os.getenv("FLASK_ENV") == "development":
        admin.init_app(app)

    # register api
    from project.apis import blueprint as api

    app.register_blueprint(api)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    # error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": False, "message": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"status": False, "message": f"Internal error: {error}"}), 500

    return app

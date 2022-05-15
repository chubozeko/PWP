import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from credentials import get_db_credentials
from eathelp.api import api

db = SQLAlchemy()

# Based on http://flask.pocoo.org/docs/1.0/tutorial/factory/#the-application-factory
# Modified to use Flask SQLAlchemy
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "development.db"),
        SQLALCHEMY_DATABASE_URI = "mysql+pymysql://" + \
                                                get_db_credentials()["user"] + \
                                                ":" + get_db_credentials()["password"] + \
                                                "@" + get_db_credentials()["port"] + \
                                                "/" + get_db_credentials()["database_name"],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(api.blueprint)
    return app
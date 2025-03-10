##
#   This code was developed by the EatHelp API team,
#       with some code references from the following resources:
#
# - Code from PWP Lectures and Exercises:
#   (https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2022/)
# - Python REST API Tutorial - Building a Flask REST API
#   (https://www.youtube.com/watch?v=GMppyAPbLYk)
# - Build Modern APIs using Flask (playlist)
#   (https://www.youtube.com/playlist?list=PLMOobVGrchXN5tKYdyx-d2OwwgxJuqDVH)
#
#   MIT License. 2022 (c) All Rights Reserved.
##

import os

from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flasgger import Swagger
from credentials import get_db_credentials
from eathelp.db.load_database import db_connection_mysql

db = SQLAlchemy()
cache = Cache()


def create_app(test_config=None, init_db=False):
    app = Flask(__name__,
                static_url_path='/static',
                instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="mysql+pymysql://" +
                                get_db_credentials()["user"] +
                                ":" + get_db_credentials()["password"] +
                                "@" + get_db_credentials()["host"] +
                                ":" + get_db_credentials()["port"] +
                                "/" + get_db_credentials()["database_name"] +
                                get_db_credentials()["query_params"],
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )
    app.config["CACHE_TYPE"] = "SimpleCache"
    app.config["CACHE_DIR"] = os.path.join(app.instance_path, "cache")
    app.config["SWAGGER"] = {
        "title": "EatHelp API",
        "openapi": "3.0.3",
        "uiversion": 3,
    }
    swagger = Swagger(app, template_file="doc/eathelp.yaml")

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    db_connection_mysql(init_db)
    cache.init_app(app)
    from eathelp.api import api
    app.register_blueprint(api.blueprint)
    CORS(app)
    return app

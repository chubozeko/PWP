from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp import db
from eathelp.models import Cookbook

JSON = "application/json"

# TODO: CookbookItem [PWP-50]
    # TODO: SQL Query to SELECT a CookbookItem [PWP-16]
    # TODO: SQL Query to INSERT a CookbookItem [PWP-16]
    # TODO: SQL Query to DELETE a CookbookItem [PWP-16]

# TODO: CookbookCollection [PWP-50]
    # TODO: SQL Query to SELECT a CookbookCollection [PWP-16]
    # TODO: SQL Query to INSERT into a CookbookCollection [PWP-16]
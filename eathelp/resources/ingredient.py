from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp import db
from eathelp.models import Ingredient

JSON = "application/json"

# TODO: *IngredientItem

# TODO: *IngredientCollection
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

# TODO: IngredientItem [PWP-50]
    # TODO: SQL Query to SELECT an IngredientItem [PWP-16]
    # TODO: SQL Query to INSERT an IngredientItem [PWP-16]
    # TODO: SQL Query to DELETE an IngredientItem [PWP-16]

# TODO: IngredientCollection [PWP-50]
    # TODO: SQL Query to SELECT an IngredientCollection [PWP-16]
    # TODO: SQL Query to INSERT into an IngredientCollection [PWP-16]
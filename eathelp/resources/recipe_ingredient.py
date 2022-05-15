from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp import db
from eathelp.models import RecipeIngredient

JSON = "application/json"

# TODO: *RecipeIngredientItem [PWP-50]
    # TODO: SQL Query to SELECT a RecipeIngredientItem [PWP-16]
    # TODO: SQL Query to INSERT a RecipeIngredientItem [PWP-16]
    # TODO: SQL Query to DELETE a RecipeIngredientItem [PWP-16]

# TODO: *RecipeIngredientCollection [PWP-50]
    # TODO: SQL Query to SELECT a RecipeIngredientCollection [PWP-16]
    # TODO: SQL Query to INSERT into a RecipeIngredientCollection [PWP-16]
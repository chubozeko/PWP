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

# TODO: RecipeIngredientItem [PWP-50]
class RecipeIngredientItem(Resource):
    def get(self, r_ingredient):
        # TODO: SQL Query to SELECT a RecipeIngredientItem [PWP-16]
        body = r_ingredient.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, r_ingredient):
        if not request.json:
            raise UnsupportedMediaType
        # try:
        #     validate(request.json, RecipeIngredient.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        r_ingredient.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT a RecipeIngredientItem [PWP-16]
            db.session.add(r_ingredient)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, r_ingredient):
        # TODO: SQL Query to DELETE a RecipeIngredientItem [PWP-16]
        db.session.delete(r_ingredient)
        db.session.commit()
        return Response(status=204)

# TODO: RecipeIngredientCollection [PWP-50]
class RecipeIngredientCollection(Resource):
    def get(self):
        body = {"items": []}
        # TODO: SQL Query to SELECT a RecipeIngredientCollection [PWP-16]
        for db_r_ingredient in RecipeIngredient.query.all():
            item = db_r_ingredient.serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, RecipeIngredient.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        r_ingredient = RecipeIngredient()
        r_ingredient.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT into a RecipeIngredientCollection [PWP-16]
            db.session.add(r_ingredient)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )
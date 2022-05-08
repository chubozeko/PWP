from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp import db
from eathelp.models import Recipe

JSON = "application/json"

# TODO: RecipeItem
class RecipeItem(Resource):
    def get(self, recipe):
        body = recipe.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, recipe):
        if not request.json:
            raise UnsupportedMediaType
        # try:
        #     validate(request.json, Recipe.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        recipe.deserialize(request.json)
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, recipe):
        db.session.delete(recipe)
        db.session.commit()
        return Response(status=204)

# TODO: RecipeCollection
class RecipeCollection(Resource):
    def get(self):
        body = {"items": []}
        for db_recipe in Recipe.query.all():
            item = db_recipe.serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Recipe.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        recipe = Recipe()
        recipe.deserialize(request.json)
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )
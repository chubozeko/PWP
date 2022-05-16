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
class IngredientItem(Resource):
    def get(self, ingredient):
        # TODO: SQL Query to SELECT an IngredientItem [PWP-16]
        body = ingredient.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, ingredient):
        if not request.json:
            raise UnsupportedMediaType
        # try:
        #     validate(request.json, Ingredient.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        ingredient.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT an IngredientItem [PWP-16]
            db.session.add(ingredient)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, ingredient):
        # TODO: SQL Query to DELETE an IngredientItem [PWP-16]
        db.session.delete(ingredient)
        db.session.commit()
        return Response(status=204)

# TODO: IngredientCollection [PWP-50]
class IngredientCollection(Resource):
    def get(self):
        body = {"items": []}
        # TODO: SQL Query to SELECT an IngredientCollection [PWP-16]
        for db_ingre in Ingredient.query.all():
            item = db_ingre.serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Ingredient.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        ingredient = Ingredient()
        ingredient.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT into an IngredientCollection [PWP-16]
            db.session.add(ingredient)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )
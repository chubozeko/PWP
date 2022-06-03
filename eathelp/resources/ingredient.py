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

from flask import Response, request
from flask_restful import Resource
import json
from jsonschema import validate, ValidationError
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, Conflict
from werkzeug.exceptions import BadRequest, BadRequestKeyError

from eathelp import cache, api
from eathelp.db.load_database import db_connection_mysql
from eathelp.models import Ingredient

JSON = "application/json"


def parse_row(row):
    return Ingredient(
        ingredient_id=row[0],
        name=row[1]
    )


class IngredientItem(Resource):
    @cache.cached()
    def get(self, ingredient):
        # description: GET an ingredient with the given id
        # parameters:
        #   - ingredient = Selected ingredient's unique id [int]
        # responses:
        #   type: application/json
        #   - 200: "Ingredient found"
        #   - 400: "Cannot find ingredient with given id {ingredient}:
        #           list index out of range"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM ingredient WHERE ingredient_id=" + str(ingredient)
        try:
            cursor.execute(sql)
            ingredients = cursor.fetchall()
            body = parse_row(ingredients[0]).serialize()
        except IndexError as e:
            raise BadRequestKeyError(
                description="""Cannot find ingredient with given id {ingredient}
                : """ + str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, ingredient):
        # description: Update an ingredient
        # parameters:
        #   - ingredient = Selected ingredient's unique id [int]
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 204: Ingredient updated
        #   - 400: Invalid request body
        #   - 409: Ingredient with name {name} already exists for this chef
        #   - 415: Unsupported media type

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Ingredient.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        i = Ingredient()
        i.deserialize(request.json)
        try:
            sql = """UPDATE ingredient SET name=%s WHERE ingredient_id=""" + \
                  str(ingredient)
            cursor.execute(sql, (i.name,))
            conn.commit()
            self._clear_cache()
        except IntegrityError:
            raise Conflict(
                "Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, ingredient):
        # description: DELETE an ingredient
        # parameters:
        #   - ingredient = Selected ingredient's unique id [int]
        # responses:
        #   type: application/json
        #   - 204: No content

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM ingredient WHERE ingredient_id=" + str(ingredient)
        cursor.execute(sql)
        conn.commit()
        self._clear_cache()
        return Response(status=204)

    def _clear_cache(self):
        # clears the cache of the Ingredients
        ic_path = api.url_for(IngredientCollection)
        cache.delete_many((
            ic_path,
            request.path,
        ))


class IngredientCollection(Resource):
    def get(self):
        # description: GET a list of all ingredients
        # parameters: none
        # responses:
        #   type: application/json
        #   - 200: returns an array list of ingredients
        #   - 400: "Cannot find any ingredients"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM ingredient"
        cursor.execute(sql)
        ingredients = cursor.fetchall()
        body = {"items": []}
        for i in ingredients:
            item = parse_row(i).serialize()
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        # description: Add a new cookbook by chef
        # parameters: none
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 201: Ingredient created
        #   - 400: Invalid request body
        #   - 409: "Ingredient with the name '{name}' already exists"
        #   - 415: Unsupported media type

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Ingredient.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        ingredient = Ingredient()
        ingredient.deserialize(request.json)
        try:
            sql = """INSERT INTO ingredient (name) VALUES (%s)"""
            cursor.execute(sql, (ingredient.name,))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Ingredient with the name '{name}' already exists."
                .format(**request.json)
            )
        return Response(status=201, headers={})

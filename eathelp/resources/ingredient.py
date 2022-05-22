from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp.db.load_database import db_connection_mysql
from eathelp.models import Ingredient

JSON = "application/json"

def parse_row(row):
    return Ingredient(
        ingredient_id=row[0],
        name=row[1]
    )

class IngredientItem(Resource):
    def get(self, ingredient):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM ingredient WHERE ingredient_id=" + str(ingredient)
        cursor.execute(sql)
        ingredients = cursor.fetchall()
        body = parse_row(ingredients[0]).serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, ingredient):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        # TODO: json_schema() validation [PWP-17]
        # try:
        #     validate(request.json, Ingredient.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        i = Ingredient()
        i.deserialize(request.json)
        try:
            sql = """UPDATE ingredient SET name = %s WHERE ingredient_id = """ + str(ingredient)
            cursor.execute(sql, (i.name,))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, ingredient):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM ingredient WHERE ingredient_id=" + str(ingredient)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)

class IngredientCollection(Resource):
    def get(self):
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
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        # TODO: json_schema() validation [PWP-17]
        # try:
        #     validate(request.json, Ingredient.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        ingredient = Ingredient()
        ingredient.deserialize(request.json)
        try:
            sql = """INSERT INTO ingredient (name) VALUES (%s)"""
            cursor.execute(sql, (ingredient.name,))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Ingredient with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=201, headers={})
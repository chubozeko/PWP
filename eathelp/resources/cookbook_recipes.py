from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict, BadRequestKeyError

from eathelp.db.load_database import db_connection_mysql
from eathelp.models import CookbookRecipes

JSON = "application/json"

def parse_row(row):
    return CookbookRecipes(
        cookbook_id=row[0],
        recipe_id=row[1]
    )


class CookbookRecipesItem(Resource):
    def get(self, cookbook, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        try:
            sql = """SELECT * FROM cookbook_recipes
                    WHERE recipe_id = """ + str(recipe) + """ AND cookbook_id = """ + str(cookbook)
            ### Version 2 = More complex query to show more data:
            # sql = """SELECT c.cookbook_id, c.name, r.recipe_id, r.recipe_name
            # FROM recipe r JOIN cookbook_recipes cr ON r.recipe_id = cr.recipe_id
            # JOIN cookbook c ON c.cookbook_id = cr.cookbook_id
            # WHERE r.recipe_id = """ + str(recipe) + """ AND cr.cookbook_id = """ + str(cookbook)
            cursor.execute(sql)
            cb_recipes = cursor.fetchall()
            body = parse_row(cb_recipes[0]).serialize()
        except IndexError as e:
            raise BadRequestKeyError(
                description="Cannot find recipe with id {recipe} in cookbook with id {cookbook}: " + str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def delete(self, cookbook, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM cookbook_recipes WHERE cookbook_id=" + str(cookbook) + " AND recipe_id=" + str(recipe)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)


class CookbookRecipesCollection(Resource):
    def get(self, cookbook):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = """SELECT r.* FROM recipe r JOIN cookbook_recipes cr ON r.recipe_id = cr.recipe_id 
        WHERE cr.cookbook_id = """ + str(cookbook)
        cursor.execute(sql)
        cookbook_recipes = cursor.fetchall()
        body = {"items": []}
        for cbr in cookbook_recipes:
            item = parse_row(cbr).serialize()
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self, cookbook):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, CookbookRecipes.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        cbr = CookbookRecipes()
        cbr.deserialize(request.json)
        try:
            if cookbook == cbr.cookbook_id:
                sql = """INSERT INTO cookbook_recipes (cookbook_id, recipe_id) VALUES (%s,%s)"""
                cursor.execute(sql, (cbr.cookbook_id, cbr.recipe_id))
                conn.commit()
            else:
                return Response(status=405, headers={})
        except IntegrityError:
            raise Conflict(
                "Cookbook with id '{cookbook}' already contains Recipe with id {cbr.recipe_id}.".format(**request.json)
            )
        return Response(status=201, headers={})

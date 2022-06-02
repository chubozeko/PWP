from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict, BadRequestKeyError

from eathelp.db.load_database import db_connection_mysql
from eathelp.models import RecipeIngredient

JSON = "application/json"

def parse_row(row):
    return RecipeIngredient(
        rec_ing_id=row[0],
        recipe_id=row[1],
        ingredient_id=row[2],
        amount=row[3],
        unit=row[4]
        # ingredient_name=row[5]
    )


class RecipeIngredientItem(Resource):
    def get(self, recipe, r_ingredient):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM recipe_ingredient WHERE rec_ing_id=" + str(r_ingredient) + " AND recipe_id=" + str(recipe)
        try:
            cursor.execute(sql)
            recipe_ingredients = cursor.fetchall()
            body = parse_row(recipe_ingredients[0]).serialize(short_form=False)
        except IndexError as e:
            raise BadRequestKeyError(
                description="Cannot find ingredient with id {recipe_ingredient} in recipe with id {recipe}: " + str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, recipe, r_ingredient):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, RecipeIngredient.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        ri = RecipeIngredient()
        ri.deserialize(request.json)
        try:
            sql = """UPDATE recipe_ingredient SET ingredient_id = %s, amount = %s, unit = %s 
            WHERE recipe_id = """ + str(recipe) + """ AND rec_ing_id = """ + str(r_ingredient)
            cursor.execute(sql, (ri.ingredient_id, ri.amount, ri.unit,))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Ingredient with id '{rec_ing_id}' already exists in Recipe {recipe_id}.".format(**request.json)
            )
        return Response(status=204)

    def delete(self, recipe, r_ingredient):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM recipe_ingredient WHERE rec_ing_id=" + str(r_ingredient) + " AND recipe_id=" + str(recipe)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)

class RecipeIngredientCollection(Resource):
    def get(self, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM recipe_ingredient WHERE recipe_id=" + str(recipe)
        # sql = """SELECT ri.rec_ing_id, ri.recipe_id, i.ingredient_id, ri.amount, ri.unit, i.name
        #     FROM recipe_ingredient ri JOIN ingredient i
        #     ON ri.ingredient_id = i.ingredient_id
        #     WHERE ri.recipe_id=""" + str(recipe)
        cursor.execute(sql)
        recipe_ingredients = cursor.fetchall()
        body = {"items": []}
        for ri in recipe_ingredients:
            item = parse_row(ri).serialize(short_form=False)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, RecipeIngredient.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        # try:
        #     # POSTing an array of RecipeIngredient Items
        #     for ing in request.json['ingredients']:
        #         r_ingredient = RecipeIngredient()
        #         r_ingredient.deserialize(ing)
        #         try:
        #             sql = """INSERT INTO recipe_ingredient
        #                                 (recipe_id, ingredient_id, amount, unit)
        #                                 VALUES (%s,%s,%s,%s)"""
        #             cursor.execute(sql, (str(recipe), r_ingredient.ingredient_id, r_ingredient.amount, r_ingredient.unit,))
        #         except IntegrityError:
        #             raise Conflict(
        #                 "Recipe Ingredient with id '{rec_ing_id}' already exists.".format(
        #                     **request.json
        #                 )
        #             )
        #     conn.commit()
        #     return Response(status=201, headers={})
        # except KeyError:
        # POSTing a singular RecipeIngredient Item
        r_ingredient = RecipeIngredient()
        r_ingredient.deserialize(request.json)
        try:
            sql = """INSERT INTO recipe_ingredient 
                                (recipe_id, ingredient_id, amount, unit) 
                                VALUES (%s,%s,%s,%s)"""
            cursor.execute(sql, (str(recipe), r_ingredient.ingredient_id, r_ingredient.amount, r_ingredient.unit,))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe Ingredient with id '{rec_ing_id}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=201, headers={})


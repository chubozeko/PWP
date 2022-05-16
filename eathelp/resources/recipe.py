from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp.models import Recipe
from app import db_connection_mysql

JSON = "application/json"

class RecipeItem(Resource):
    def parse_row(self, row):
        return Recipe(
            recipe_id=row[0],
            recipe_name=row[1],
            prep_time=row[2],
            cooking_time=row[3],
            meal_type=row[4],
            calories=row[5],
            servings=row[6],
            instructions=row[7],
            creator_id=row[8]
        )

    def get(self, chef, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if chef is not None:
            sql = "SELECT * FROM recipe WHERE creator_id=" + str(chef) + " AND recipe_id=" + str(recipe)
        else:
            sql = "SELECT * FROM recipe WHERE recipe_id=" + str(recipe)
        cursor.execute(sql)
        recipes = cursor.fetchall()
        body = self.parse_row(recipes[0]).serialize(short_form=False)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, chef, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        # TODO: json_schema() validation [PWP-17]
        # try:
        #     validate(request.json, Recipe.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        r = Recipe()
        r.deserialize(request.json)
        try:
            if chef is not None:
                sql = """UPDATE recipe SET recipe_name = %s, prep_time = %s, cooking_time = %s, meal_type = %s, calories = %s, 
                servings = %s, instructions = %s WHERE recipe_id = """ + str(recipe) + """ AND creator_id = """ + str(chef)
                cursor.execute(sql, (r.recipe_name, r.prep_time, r.cooking_time, r.meal_type, r.calories, r.servings,
                        '\n'.join(r.instructions)))
            else:
                sql = """UPDATE recipe SET recipe_name = %s, prep_time = %s, cooking_time = %s, meal_type = %s, calories = %s, 
                                servings = %s, creator_id = %s, instructions = %s WHERE recipe_id = """ + str(recipe)
                cursor.execute(sql, (r.recipe_name, r.prep_time, r.cooking_time, r.meal_type, r.calories, r.servings,
                                     r.creator_id, '\n'.join(r.instructions)))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with name '{recipe_name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, chef, recipe):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if chef is not None:
            sql = "DELETE FROM recipe WHERE recipe_id=" + str(recipe) + " AND creator_id=" + str(chef)
        else:
            sql = "DELETE FROM recipe WHERE recipe_id=" + str(recipe)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)

class RecipeCollection(Resource):
    def parse_row(self, row):
        return Recipe(
            recipe_id=row[0],
            recipe_name=row[1],
            prep_time=row[2],
            cooking_time=row[3],
            meal_type=row[4],
            calories=row[5],
            servings=row[6],
            instructions=row[7],
            creator_id=row[8]
        )

    def get(self, chef):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if chef is not None:
            sql = "SELECT * FROM recipe WHERE creator_id=" + str(chef)
        else:
            sql = "SELECT * FROM recipe"
        cursor.execute(sql)
        recipes = cursor.fetchall()
        body = {"items": []}
        for r in recipes:
            item = self.parse_row(r).serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self, chef):
        conn = db_connection_mysql()
        cursor = conn.cursor()

        if not request.json:
            raise UnsupportedMediaType
        # TODO: json_schema() validation [PWP-17]
        # try:
        #     validate(request.json, Recipe.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        recipe = Recipe()
        recipe.deserialize(request.json)
        try:
            sql = """INSERT INTO recipe 
            (recipe_name, prep_time, cooking_time, meal_type, calories, servings, creator_id, instructions) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            if chef is not None:
                cursor.execute(sql, (recipe.recipe_name, recipe.prep_time, recipe.cooking_time, recipe.meal_type,
                                     recipe.calories, recipe.servings, str(chef),
                                     '\n'.join(recipe.instructions)))
            else:
                cursor.execute(sql, (recipe.recipe_name, recipe.prep_time, recipe.cooking_time, recipe.meal_type,
                                     recipe.calories, recipe.servings, recipe.creator_id,
                                     '\n'.join(recipe.instructions)))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with name '{recipe_name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )
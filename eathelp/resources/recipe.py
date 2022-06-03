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

from eathelp.models import Recipe
from eathelp.db.load_database import db_connection_mysql

JSON = "application/json"


def parse_row(row):
    return Recipe(
        recipe_id=row[0],
        recipe_name=row[1],
        description=row[2],
        prep_time=row[3],
        cooking_time=row[4],
        meal_type=row[5],
        calories=row[6],
        servings=row[7],
        instructions=row[8],
        creator_id=row[9]
    )


class RecipeItem(Resource):
    def get(self, recipe, chef=None):
        # description: GET a recipe (from a specific chef if chef != None)
        # parameters:
        #   - recipe = Selected recipe's unique id [int]
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/recipes/{recipe}"
        # responses:
        #   type: application/json
        #   - 200: "Recipe found"
        #   - 400: "Cannot find recipe with given id {recipe}:
        #           list index out of range"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if chef is not None:
            sql = "SELECT * FROM recipe WHERE creator_id=" + str(chef) + \
                  " AND recipe_id=" + str(recipe)
        else:
            sql = "SELECT * FROM recipe WHERE recipe_id=" + str(recipe)
        try:
            cursor.execute(sql)
            recipes = cursor.fetchall()
            body = parse_row(recipes[0]).serialize(short_form=False)
        except IndexError as e:
            raise BadRequestKeyError(
                description="Cannot find recipe with given id {recipe}: "+str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, recipe, chef=None):
        # description: Update a recipe from a specific chef (if chef != None)
        # parameters:
        #   - recipe = Selected recipe's unique id [int]
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/recipes/{recipe}"
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 204: Recipe updated
        #   - 400: Invalid request body
        #   - 409: Recipe with name {name} already exists for this chef
        #   - 415: Unsupported media type

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Recipe.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        r = Recipe()
        r.deserialize(request.json)
        try:
            if chef is not None:
                sql = """UPDATE recipe SET recipe_name = %s, description = %s,
                      prep_time = %s, cooking_time = %s, meal_type = %s,
                      calories = %s, servings = %s, instructions = %s
                      WHERE recipe_id = """ + str(recipe) + \
                      """ AND creator_id = """ + str(chef)
                cursor.execute(sql, (r.recipe_name, r.description, r.prep_time,
                                     r.cooking_time, r.meal_type, r.calories,
                                     r.servings, '\n'.join(r.instructions)))
            else:
                sql = """UPDATE recipe SET recipe_name = %s, description = %s,
                      prep_time = %s, cooking_time = %s, meal_type = %s,
                      calories = %s, servings = %s, creator_id = %s,
                      instructions = %s WHERE recipe_id = """ + str(recipe)
                cursor.execute(sql, (r.recipe_name, r.description, r.prep_time,
                                     r.cooking_time, r.meal_type, r.calories,
                                     r.servings, r.creator_id,
                                     '\n'.join(r.instructions)))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with the name '{recipe_name}' already exists."
                .format(**request.json)
            )
        return Response(status=204)

    def delete(self, recipe, chef=None):
        # description: DELETE a recipe of a chef (user) using its id
        # parameters:
        #   - recipe = Selected recipe's unique id [int]
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/recipes/{recipe}"
        # responses:
        #   type: application/json
        #   - 204: No content

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if chef is not None:
            sql = "DELETE FROM recipe WHERE recipe_id=" + str(recipe) + \
                  " AND creator_id=" + str(chef)
        else:
            sql = "DELETE FROM recipe WHERE recipe_id=" + str(recipe)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)


class RecipeCollection(Resource):
    def get(self, chef=None):
        # description: GET a list of all recipes (from a chef if chef != None)
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/recipes/"
        # responses:
        #   type: application/json
        #   - 200: returns an array list of cookbooks (can be an empty list)
        #   - 400: "Cannot find any recipes [from chef]"

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
            item = parse_row(r).serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self, chef=None):
        # description: Add a new recipe [by chef]
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/recipes/"
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 201: Recipe created
        #   - 400: Invalid request body
        #   - 409: "Recipe with the name '{name}' [from chef] already exists"
        #   - 415: Unsupported media type
        #   - 405: Method not allowed [for route /recipes/]

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Recipe.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        recipe = Recipe()
        recipe.deserialize(request.json)
        try:
            sql = """INSERT INTO recipe (recipe_name, description, prep_time,
                  cooking_time, meal_type, calories, servings, creator_id,
                  instructions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
            if chef is not None:
                cursor.execute(sql, (recipe.recipe_name, recipe.description,
                                     recipe.prep_time, recipe.cooking_time,
                                     recipe.meal_type, recipe.calories,
                                     recipe.servings, str(chef),
                                     '\n'.join(recipe.instructions)))
            else:
                cursor.execute(sql, (recipe.recipe_name, recipe.description,
                                     recipe.prep_time, recipe.cooking_time,
                                     recipe.meal_type, recipe.calories,
                                     recipe.servings, recipe.creator_id,
                                     '\n'.join(recipe.instructions)))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with the name '{recipe_name}' already exists."
                .format(**request.json)
            )
        return Response(status=201, headers={})

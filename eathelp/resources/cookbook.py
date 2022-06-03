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

from eathelp.db.load_database import db_connection_mysql
from eathelp.models import Cookbook

JSON = "application/json"


# Parse row from SQL query before serializing it
def parse_row(row):
    return Cookbook(
        cookbook_id=row[0],
        name=row[1],
        description=row[2],
        user_id=row[3]
    )


class CookbookItem(Resource):
    def get(self, chef, cookbook):
        # description: GET a cookbook from a specific chef (user)
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/cookbooks/{cookbook}"
        #   - cookbook = Selected cookbook's unique id [int]
        # responses:
        #   type: application/json
        #   - 200: "Cookbook found"
        #   - 400: "Cannot find cookbook with given id {cookbook}:
        #       list index out of range"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM cookbook WHERE user_id=" + str(chef) + \
              " AND cookbook_id=" + str(cookbook)
        try:
            cursor.execute(sql)
            cookbooks = cursor.fetchall()
            body = parse_row(cookbooks[0]).serialize(short_form=False)
        except IndexError as e:
            raise BadRequestKeyError(
                description="Cannot find a cookbook from chef: " + str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, chef, cookbook):
        # description: Update a cookbook from a specific chef (if chef != None)
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/cookbooks/{cookbook}"
        #   - cookbook = Selected cookbook's unique id [int]
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 204: Cookbook updated
        #   - 400: Invalid request body
        #   - 409: Cookbook with name {name} already exists for this chef
        #   - 415: Unsupported media type

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Cookbook.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        cb = Cookbook()
        cb.deserialize(request.json)
        try:
            sql = """UPDATE cookbook SET name = %s, description = %s
            WHERE cookbook_id = """ + str(cookbook) + \
                  """ AND user_id = """ + str(chef)
            cursor.execute(sql, (cb.name, cb.description))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Cookbook with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, chef, cookbook):
        # description: DELETE a cookbook of a chef (user) using its id
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/cookbooks/{cookbook}"
        #   - cookbook = Selected cookbook's unique id [int]
        # responses:
        #   type: application/json
        #   - 204: No content

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM cookbook WHERE cookbook_id=" + str(cookbook) + \
              " AND user_id=" + str(chef)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)


class CookbookCollection(Resource):
    def get(self, chef=None):
        # description: GET a collection of all the cookbooks
        #               created by a specific chef (user)
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/cookbooks/"
        # responses:
        #   type: application/json
        #   - 200: returns an array list of cookbooks (can be an empty list)
        #   - 400: "Cannot find any cookbooks from chef"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if chef is not None:
            sql = "SELECT * FROM cookbook WHERE user_id=" + str(chef)
        else:
            sql = "SELECT * FROM cookbook"
        cursor.execute(sql)
        cookbooks = cursor.fetchall()
        body = {"items": []}
        for cb in cookbooks:
            item = parse_row(cb).serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self, chef=None):
        # description: Add a new cookbook by chef
        # parameters:
        #   - chef = Selected chef's unique id [int]
        #       -> only for route "/chefs/{chef}/cookbooks/"
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 201: Cookbook created
        #   - 400: Invalid request body
        #   - 409: "Cookbook with the name '{name}' from chef already exists"
        #   - 415: Unsupported media type
        #   - 405: Method not allowed [for route /cookbooks/]

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Cookbook.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        cookbook = Cookbook()
        cookbook.deserialize(request.json)
        try:
            if chef is not None:
                sql = """INSERT INTO cookbook (name, description, user_id)
                VALUES (%s,%s,%s)"""
                cursor.execute(sql,
                               (cookbook.name, cookbook.description, str(chef)))
            else:
                return Response(status=405, headers={})
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Cookbook with the name '{name}' by this user already exists."
                .format(**request.json)
            )
        return Response(status=201, headers={})

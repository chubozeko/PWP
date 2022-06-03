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
from eathelp.models import User

JSON = "application/json"


def parse_row(row):
    return User(
        user_id=row[0],
        username=row[1]
    )


class UserItem(Resource):
    @cache.cached()
    def get(self, chef):
        # description: GET a single chef (user) using its id
        # parameters:
        #   - chef = Selected chef's unique id [int]
        # responses:
        #   type: application/json
        #   - 200: returns a chef item
        #   - 400: "Cannot find chef with given id {chef}:
        #           list index out of range"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE user_id=" + str(chef)
        try:
            cursor.execute(sql)
            chefs = cursor.fetchall()
            body = parse_row(chefs[0]).serialize()
        except IndexError as e:
            raise BadRequestKeyError(
                description="Cannot find chef with given id {chef}: " + str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, chef):
        # description: Update a chef
        # parameters:
        #   - chef = Selected chef's unique id [int]
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 204: Chef updated
        #   - 400: Invalid request body
        #   - 409: Chef with username {username} already exists
        #   - 415: Unsupported media type

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        c = User()
        c.deserialize(request.json)
        try:
            sql = """UPDATE user SET username = %s WHERE user_id = """ + \
                  str(chef)
            cursor.execute(sql, (c.username, ))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Chef with username '{username}' already exists."
                .format(**request.json)
            )
        return Response(status=204)

    def delete(self, chef):
        # description: DELETE a chef
        # parameters:
        #   - chef = Selected chef's unique id [int]
        # responses:
        #   type: application/json
        #   - 204: No content

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM user WHERE user_id=" + str(chef)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)

    def _clear_cache(self):
        # clears the cache of the Chefs
        user_path = api.url_for(UserCollection)
        cache.delete_many((
            user_path,
            request.path,
        ))


class UserCollection(Resource):
    def get(self):
        # description: GET a list of all chefs (users)
        # parameters:
        #   - chef = Selected chef's unique id [int]
        # responses:
        #   type: application/json
        #   - 200: returns an array list of chefs (can be an empty list)
        #   - 400: "Unable to retrieve any chefs"

        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM user"
        cursor.execute(sql)
        chefs = cursor.fetchall()
        body = {"items": []}
        for c in chefs:
            item = parse_row(c).serialize()
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        # description: Add a new chef
        # parameters:
        #   - chef = Selected chef's unique id [int]
        # requestBody: application/json
        # responses:
        #   type: application/json
        #   - 201: Chef created
        #   - 400: Invalid request body
        #   - 409: "Chef already exists"
        #   - 415: Unsupported media type

        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        chef = User()
        chef.deserialize(request.json)
        try:
            sql = """INSERT INTO user (username) VALUES (%s)"""
            cursor.execute(sql, (chef.username, ))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Chef with username '{username}' already exists."
                .format(**request.json)
            )
        return Response(status=201, headers={})

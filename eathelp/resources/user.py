import werkzeug.exceptions
from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict, BadRequestKeyError

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
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM user WHERE user_id=" + str(chef)
        try:
            cursor.execute(sql)
            chefs = cursor.fetchall()
            body = parse_row(chefs[0]).serialize()
        except IndexError as e:
            raise BadRequestKeyError(
                description="Cannot find chef with given id {" + str(chef) + "}: " + str(e)
            )
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, chef):
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
            sql = """UPDATE user SET username = %s WHERE user_id = """ + str(chef)
            cursor.execute(sql, (c.username, ))
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Chef with username '{username}' already exists.".format(**request.json)
            )
        return Response(status=204)

    def delete(self, chef):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM user WHERE user_id=" + str(chef)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)

    def _clear_cache(self):
        user_path = api.url_for(UserCollection)
        cache.delete_many((
            user_path,
            request.path,
        ))


class UserCollection(Resource):
    def get(self):
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
                "Chef with username '{username}' already exists.".format(**request.json)
            )
        return Response(status=201, headers={})

from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp.db.load_database import db_connection_mysql
from eathelp.models import Cookbook

JSON = "application/json"

def parse_row(row):
    return Cookbook(
        cookbook_id=row[0],
        name=row[1],
        description=row[2],
        user_id=row[3]
    )

class CookbookItem(Resource):
    def get(self, chef, cookbook):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "SELECT * FROM cookbook WHERE user_id=" + str(chef) + " AND cookbook_id=" + str(cookbook)
        cursor.execute(sql)
        cookbooks = cursor.fetchall()
        body = parse_row(cookbooks[0]).serialize(short_form=False)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, chef, cookbook):
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        # TODO: json_schema() validation [PWP-17]
        try:
            validate(request.json, Cookbook.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        cb = Cookbook()
        cb.deserialize(request.json)
        try:
            sql = """UPDATE cookbook SET name = %s, description = %s 
            WHERE cookbook_id = """ + str(cookbook) + """ AND user_id = """ + str(chef)
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
        conn = db_connection_mysql()
        cursor = conn.cursor()
        sql = "DELETE FROM cookbook WHERE cookbook_id=" + str(cookbook) + " AND user_id=" + str(chef)
        cursor.execute(sql)
        conn.commit()
        return Response(status=204)


class CookbookCollection(Resource):
    def get(self, chef=None):
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
        conn = db_connection_mysql()
        cursor = conn.cursor()
        if not request.json:
            raise UnsupportedMediaType
        # TODO: json_schema() validation [PWP-17]
        try:
            validate(request.json, Cookbook.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        cookbook = Cookbook()
        cookbook.deserialize(request.json)
        try:
            if chef is not None:
                sql = """INSERT INTO cookbook (name, description, user_id) VALUES (%s,%s,%s)"""
                cursor.execute(sql, (cookbook.name, cookbook.description, str(chef)))
            else:
                return Response(status=405, headers={})
            conn.commit()
        except IntegrityError:
            raise Conflict(
                "Cookbook with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=201, headers={})
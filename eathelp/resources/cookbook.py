from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp import db
from eathelp.models import Cookbook

JSON = "application/json"

# TODO: CookbookItem [PWP-50]
class CookbookItem(Resource):
    def get(self, cookbook):
        # TODO: SQL Query to SELECT a CookbookItem [PWP-16]
        body = cookbook.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, cookbook):
        if not request.json:
            raise UnsupportedMediaType
        # try:
        #     validate(request.json, Cookbook.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        cookbook.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT a CookbookItem [PWP-16]
            db.session.add(cookbook)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Cookbook with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, cookbook):
        # TODO: SQL Query to DELETE a CookbookItem [PWP-16]
        db.session.delete(cookbook)
        db.session.commit()
        return Response(status=204)

# TODO: CookbookCollection [PWP-50]
class CookbookCollection(Resource):
    def get(self):
        body = {"items": []}
        # TODO: SQL Query to SELECT a CookbookCollection [PWP-16]
        for db_cookbook in Cookbook.query.all():
            item = db_cookbook.serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Cookbook.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        cookbook = Cookbook()
        cookbook.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT into a CookbookCollection [PWP-16]
            db.session.add(cookbook)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Cookbook with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )
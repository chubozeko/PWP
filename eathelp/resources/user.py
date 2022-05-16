from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

from eathelp import db
from eathelp.models import User

JSON = "application/json"

# TODO: UserItem [PWP-50]
class UserItem(Resource):
    def get(self, chef):
        # TODO: SQL Query to SELECT a UserItem [PWP-16]
        body = chef.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, chef):
        if not request.json:
            raise UnsupportedMediaType
        # try:
        #     validate(request.json, User.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        chef.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT a UserItem [PWP-16]
            db.session.add(chef)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Chef with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, chef):
        # TODO: SQL Query to DELETE a UserItem [PWP-16]
        db.session.delete(chef)
        db.session.commit()
        return Response(status=204)

# TODO: UserCollection [PWP-50]
class UserCollection(Resource):
    def get(self):
        body = {"items": []}
        # TODO: SQL Query to SELECT a UserCollection [PWP-16]
        for db_chefs in User.query.all():
            item = db_chefs.serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, User.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        chef = User()
        chef.deserialize(request.json)
        try:
            # TODO: SQL Query to INSERT into a UserCollection [PWP-16]
            db.session.add(chef)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Chef with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )
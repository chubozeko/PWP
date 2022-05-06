from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import json
from jsonschema import validate, ValidationError, draft7_format_checker
from pymysql import IntegrityError
from werkzeug.exceptions import UnsupportedMediaType, BadRequest, Conflict

JSON = "application/json"

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/pwp_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), nullable=False)

    cookbooks = db.relationship("Cookbook", cascade="all, delete-orphan", back_populates="user")
    recipes = db.relationship("Recipe", cascade="all, delete-orphan", back_populates="user")

    def serialize(self):
        return {
            "username": self.username
        }

    def deserialize(self, doc):
        self.username = doc["username"]


class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

    recipe_ingredients = db.relationship("RecipeIngredient", cascade="all, delete-orphan", back_populates="ingredient")

    def serialize(self):
        return {
            "name": self.name
        }

    def deserialize(self, doc):
        self.name = doc["name"]

# TODO: *IngredientItem
# TODO: *IngredientCollection

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    meal_type = db.Column(db.String(20), nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.String(2000), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="SET NULL"))

    user = db.relationship("User", back_populates="recipes")
    collections = db.relationship("Collections", cascade="all, delete-orphan", back_populates="recipe")
    ingredients = db.relationship("RecipeIngredient", cascade="all, delete-orphan", back_populates="recipe")

    def serialize(self, short_form=False):
        doc = {
            "recipe_name": self.recipe_name,
            "user": self.user and self.user.serialize()
        }
        if not short_form:
            doc["prep_time"] = self.prep_time
            doc["cooking_time"] = self.cooking_time
            doc["meal_type"] = self.meal_type
            doc["calories"] = self.calories
            doc["servings"] = self.servings
            doc["instructions"] = self.instructions
        return doc

    def deserialize(self, doc):
        self.recipe_name = doc["recipe_name"]
        self.prep_time = doc["prep_time"]
        self.cooking_time = doc["cooking_time"]
        self.meal_type = doc["meal_type"]
        self.calories = doc["calories"]
        self.servings = doc["servings"]
        self.instructions = doc["instructions"]
        self.user = doc["user"]

# TODO: RecipeItem
class RecipeItem(Resource):
    def get(self, recipe):
        body = recipe.serialize()
        return Response(json.dumps(body), 200, mimetype=JSON)

    def put(self, recipe):
        if not request.json:
            raise UnsupportedMediaType
        # try:
        #     validate(request.json, Recipe.json_schema())
        # except ValidationError as e:
        #     raise BadRequest(description=str(e))
        recipe.deserialize(request.json)
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(status=204)

    def delete(self, recipe):
        db.session.delete(recipe)
        db.session.commit()
        return Response(status=204)

# TODO: RecipeCollection
class RecipeCollection(Resource):
    def get(self):
        body = {"items": []}
        for db_recipe in Recipe.query.all():
            item = db_recipe.serialize(short_form=True)
            body["items"].append(item)
        return Response(json.dumps(body), 200, mimetype=JSON)

    def post(self):
        if not request.json:
            raise UnsupportedMediaType
        try:
            validate(request.json, Recipe.json_schema())
        except ValidationError as e:
            raise BadRequest(description=str(e))
        recipe = Recipe()
        recipe.deserialize(request.json)
        try:
            db.session.add(recipe)
            db.session.commit()
        except IntegrityError:
            raise Conflict(
                "Recipe with name '{name}' already exists.".format(
                    **request.json
                )
            )
        return Response(
            status=201, headers={}
        )


class RecipeIngredient(db.Model):
    rec_ing_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", ondelete="SET NULL"))
    ingredient_id = db.Column(db.Integer, db.ForeignKey("ingredient.ingredient_id", ondelete="SET NULL"))
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(255), nullable=False)

    recipe = db.relationship("Recipe", back_populates="ingredients")
    ingredient = db.relationship("Ingredient", back_populates="recipe_ingredients")

    def serialize(self, short_form=False):
        return {
            "amount": self.amount,
            "unit": self.unit,
            "ingredient": self.ingredient and self.ingredient.serialize(short_form=short_form),
            "recipe": self.recipe and self.recipe.serialize(short_form=short_form)
        }

    def deserialize(self, doc):
        self.amount = doc["amount"]
        self.unit = doc["unit"]
        self.ingredient = doc["ingredient"]
        self.recipe = doc["recipe"]


class Cookbook(db.Model):
    cookbook_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="SET NULL"))

    user = db.relationship("User", back_populates="cookbooks")
    collections = db.relationship("Collections", cascade="all, delete-orphan", back_populates="cookbook")

    def serialize(self, short_form=False):
        doc = {
            "name": self.name,
            "user": self.user and self.user.serialize()
        }
        if not short_form:
            doc["description"] = self.description
        return doc

    def deserialize(self, doc):
        self.name = doc["name"]
        self.user = doc["user"]
        self.description = doc["description"]

# TODO: CookbookItem
# TODO: CookbookCollection

class Collections(db.Model):
    cookbook_id = db.Column(db.Integer, db.ForeignKey("cookbook.cookbook_id", ondelete="SET NULL"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", ondelete="SET NULL"))

    cookbook = db.relationship("Cookbook", back_populates="collections")
    recipe = db.relationship("Recipe", back_populates="collections")



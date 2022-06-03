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

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)

    cookbooks = db.relationship(
        "Cookbook", cascade="all, delete-orphan", back_populates="user")
    recipes = db.relationship(
        "Recipe", cascade="all, delete-orphan", back_populates="user")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username
        }

    def deserialize(self, doc):
        self.username = doc["username"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["username"]
        }
        props = schema["properties"] = {}
        props["username"] = {
            "description": "The chef's unique username",
            "type": "string"
        }
        return schema


class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)

    recipe_ingredients = db.relationship(
        "RecipeIngredient",
        cascade="all, delete-orphan", back_populates="ingredient")

    def serialize(self):
        return {
            "ingredient_id": self.ingredient_id,
            "name": self.name
        }

    def deserialize(self, doc):
        self.name = doc["name"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "The ingredient's name",
            "type": "string"
        }
        return schema


class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(280), nullable=True)
    prep_time = db.Column(db.Integer, nullable=False)
    cooking_time = db.Column(db.Integer, nullable=False)
    meal_type = db.Column(db.String(20), nullable=True)
    calories = db.Column(db.Integer, nullable=False)
    servings = db.Column(db.Integer, nullable=False)
    instructions = db.Column(db.String(2000), nullable=False)
    creator_id = db.Column(db.Integer,
                           db.ForeignKey("user.user_id", ondelete="SET NULL"))

    user = db.relationship("User", back_populates="recipes")
    ingredients = db.relationship("RecipeIngredient",
                                  cascade="all, delete-orphan",
                                  back_populates="recipe")
    recipe_collection = db.relationship("CookbookRecipes",
                                        cascade="all, delete-orphan",
                                        back_populates="recipe")

    def serialize(self, short_form=False):
        doc = {
            "recipe_id": self.recipe_id,
            "recipe_name": self.recipe_name,
            "description": self.description,
            "creator_id": self.creator_id  # and self.user.serialize()
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
        self.description = doc["description"]
        self.prep_time = doc["prep_time"]
        self.cooking_time = doc["cooking_time"]
        self.meal_type = doc["meal_type"]
        self.calories = doc["calories"]
        self.servings = doc["servings"]
        self.instructions = doc["instructions"]
        self.creator_id = doc["creator_id"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["recipe_name", "prep_time", "cooking_time",
                         "calories", "servings", "instructions"]
        }
        props = schema["properties"] = {}
        props["recipe_name"] = {
            "description": "Name of the recipe",
            "type": "string"
        }
        props["description"] = {
            "description": "A short description of the recipe",
            "type": "string"
        }
        props["prep_time"] = {
            "description": "Time required to prepare the meal (in minutes)",
            "type": "number"
        }
        props["cooking_time"] = {
            "description": "Time required to cook the meal (in minutes)",
            "type": "number"
        }
        props["meal_type"] = {
            "description": "The type of meal",
            "type": "string"
        }
        props["calories"] = {
            "description": "The amount of calories in the meal",
            "type": "number"
        }
        props["servings"] = {
            "description": "The number of servings that the recipe produces",
            "type": "number"
        }
        props["instructions"] = {
            "description": "The steps taken to prepare the meal",
            "type": "array",
            "items": {
                "type": "string"
            }
        }
        props["ingredients"] = {
            "description": "The ingredients used in the recipe",
            "type": "array"
        }
        return schema


class RecipeIngredient(db.Model):
    __table_args__ = (db.UniqueConstraint("recipe_id",
                                          "ingredient_id",
                                          name="_ingredient_in_recipe_uc"),)

    rec_ing_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer,
                          db.ForeignKey("recipe.recipe_id",
                                        ondelete="SET NULL"))
    ingredient_id = db.Column(db.Integer,
                              db.ForeignKey("ingredient.ingredient_id",
                                            ondelete="SET NULL"))
    amount = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(255), nullable=False)

    recipe = db.relationship("Recipe", back_populates="ingredients")
    ingredient = db.relationship("Ingredient",
                                 back_populates="recipe_ingredients")

    def serialize(self, short_form=False):
        return {
            "id": self.rec_ing_id,
            "amount": self.amount,
            "unit": self.unit,
            "ingredient_id": self.ingredient_id,
            "recipe_id": self.recipe_id,
        }

    def deserialize(self, doc):
        self.amount = doc["amount"]
        self.unit = doc["unit"]
        self.ingredient_id = doc["ingredient_id"]
        self.recipe_id = doc["recipe_id"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["amount", "unit", "ingredient_id", "recipe_id"]
        }
        props = schema["properties"] = {}
        props["amount"] = {
            "description": "The measurable amount of the ingredient",
            "type": "number"
        }
        props["unit"] = {
            "description": "The measuring unit for the ingredient (e.g. grams, ml, teaspoons, etc.)",
            "type": "string"
        }
        props["ingredient_id"] = {
            "description": "The ID of the ingredient used",
            "type": "number"
        }
        props["recipe_id"] = {
            "description": "The ID of the recipe where the ingredient is used",
            "type": "number"
        }
        return schema


class Cookbook(db.Model):
    __table_args__ = (db.UniqueConstraint("name", "user_id",
                                          name="_user_cb_name_uc"),)

    cookbook_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("user.user_id", ondelete="SET NULL"))

    user = db.relationship("User", back_populates="cookbooks")
    recipe_collection = db.relationship("CookbookRecipes",
                                        cascade="all, delete-orphan",
                                        back_populates="cookbook")

    def serialize(self, short_form=False):
        doc = {
            "cookbook_id": self.cookbook_id,
            "name": self.name,
            "user_id": self.user_id
        }
        if not short_form:
            doc["description"] = self.description
        return doc

    def deserialize(self, doc):
        self.name = doc["name"]
        self.description = doc["description"]
        self.user_id = doc["user_id"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["name", "description"]
        }
        props = schema["properties"] = {}
        props["name"] = {
            "description": "Name of the cookbook",
            "type": "string"
        }
        props["description"] = {
            "description": "The description of the cookbook",
            "type": "string"
        }
        # props["user_id"] = {
        #     "description": "The ID of the cookbook's creator",
        #     "type": "number"
        # }
        return schema


class CookbookRecipes(db.Model):
    __tablename__ = "cookbook_recipes"

    col_id = db.Column(db.Integer, primary_key=True)
    cookbook_id = db.Column(db.Integer, db.ForeignKey("cookbook.cookbook_id",
                                                      ondelete="CASCADE"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id",
                                                    ondelete="CASCADE"))

    cookbook = db.relationship("Cookbook", back_populates="recipe_collection")
    recipe = db.relationship("Recipe", back_populates="recipe_collection")

    def serialize(self):
        return {
            "cookbook_id": self.cookbook_id,
            "recipe_id": self.recipe_id
        }

    def deserialize(self, doc):
        self.cookbook_id = doc["cookbook_id"]
        self.recipe_id = doc["recipe_id"]

    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["cookbook_id", "recipe_id"]
        }
        props = schema["properties"] = {}
        props["cookbook_id"] = {
            "description": "The ID of the cookbook",
            "type": "number"
        }
        props["recipe_id"] = {
            "description": "The ID of the recipe within the cookbook",
            "type": "number"
        }
        return schema

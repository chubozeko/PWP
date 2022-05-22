from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)

    cookbooks = db.relationship("Cookbook", cascade="all, delete-orphan", back_populates="user")
    recipes = db.relationship("Recipe", cascade="all, delete-orphan", back_populates="user")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "username": self.username
        }

    def deserialize(self, doc):
        self.username = doc["username"]

    # TODO: Implement JSON schema for Models [PWP-17]
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": [""]
        }
        props = schema["properties"] = {}
        props[""] = {
            "description": "",
            "type": ""
        }
        return schema

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False, unique=True)

    recipe_ingredients = db.relationship("RecipeIngredient", cascade="all, delete-orphan", back_populates="ingredient")

    def serialize(self):
        return {
            "ingredient_id": self.ingredient_id,
            "name": self.name
        }

    def deserialize(self, doc):
        self.name = doc["name"]

    # TODO: Implement JSON schema for Models [PWP-17]
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": [""]
        }
        props = schema["properties"] = {}
        props[""] = {
            "description": "",
            "type": ""
        }
        return schema

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(50), nullable=False, unique=True)
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
            "recipe_id": self.recipe_id,
            "recipe_name": self.recipe_name,
            "creator_id": self.creator_id # and self.user.serialize()
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
        self.creator_id = doc["creator_id"]

    # TODO: Implement JSON schema for Models [PWP-17]
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": [""]
        }
        props = schema["properties"] = {}
        props[""] = {
            "description": "",
            "type": ""
        }
        return schema

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
            "id": self.rec_ing_id,
            "amount": self.amount,
            "unit": self.unit,
            "ingredient_id": self.ingredient_id,
            "recipe_id": self.recipe_id,
            # "name": self.ingredient and self.ingredient.serialize(short_form=short_form),
            # "ingredient": self.ingredient and self.ingredient.serialize(short_form=short_form),
            # "recipe": self.recipe and self.recipe.serialize(short_form=short_form)
        }

    def deserialize(self, doc):
        self.amount = doc["amount"]
        self.unit = doc["unit"]
        self.ingredient_id = doc["ingredient_id"]
        self.recipe_id = doc["recipe_id"]

    # TODO: Implement JSON schema for Models [PWP-17]
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": [""]
        }
        props = schema["properties"] = {}
        props[""] = {
            "description": "",
            "type": ""
        }
        return schema

class Cookbook(db.Model):
    cookbook_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id", ondelete="SET NULL"))

    user = db.relationship("User", back_populates="cookbooks")
    collections = db.relationship("Collections", cascade="all, delete-orphan", back_populates="cookbook")

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

    # TODO: Implement JSON schema for Models [PWP-17]
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": [""]
        }
        props = schema["properties"] = {}
        props[""] = {
            "description": "",
            "type": ""
        }
        return schema

class Collections(db.Model):
    col_id = db.Column(db.Integer, primary_key=True)
    cookbook_id = db.Column(db.Integer, db.ForeignKey("cookbook.cookbook_id", ondelete="SET NULL"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", ondelete="SET NULL"))

    cookbook = db.relationship("Cookbook", back_populates="collections")
    recipe = db.relationship("Recipe", back_populates="collections")



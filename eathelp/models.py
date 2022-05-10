from eathelp import db

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
    name = db.Column(db.String(255), nullable=False)

    recipe_ingredients = db.relationship("RecipeIngredient", cascade="all, delete-orphan", back_populates="ingredient")

    def serialize(self):
        return {
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
    cookbook_id = db.Column(db.Integer, db.ForeignKey("cookbook.cookbook_id", ondelete="SET NULL"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", ondelete="SET NULL"))

    cookbook = db.relationship("Cookbook", back_populates="collections")
    recipe = db.relationship("Recipe", back_populates="collections")



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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

class Ingredient(db.Model):
    ingredient_id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    # sensor = db.Column(db.String(20), nullable=False)
    # value = db.Column(db.Float, nullable=False)
    # time = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="recipes")
    collections = db.relationship("Collections", cascade="all, delete-orphan", back_populates="recipe")

class RecipeIngredient(db.Model):
    rec_ing_id = db.Column(db.Integer, primary_key=True)
    # sensor = db.Column(db.String(20), nullable=False)
    # value = db.Column(db.Float, nullable=False)
    # time = db.Column(db.DateTime, nullable=False)

class Cookbook(db.Model):
    cookbook_id = db.Column(db.Integer, primary_key=True)
    # sensor = db.Column(db.String(20), nullable=False)
    # value = db.Column(db.Float, nullable=False)
    # time = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="cookbooks")
    collections = db.relationship("Collections", cascade="all, delete-orphan", back_populates="cookbook")

class Collections(db.Model):
    cookbook_id = db.Column(db.Integer, db.ForeignKey("cookbook.cookbook_id", ondelete="SET NULL"))
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipe.recipe_id", ondelete="SET NULL"))

    cookbook = db.relationship("Cookbook", back_populates="collections")
    recipe = db.relationship("Recipe", back_populates="collections")



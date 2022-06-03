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

from flask import Blueprint
from flask_restful import Api

from eathelp.resources.cookbook_recipes import CookbookRecipesItem
from eathelp.resources.cookbook_recipes import CookbookRecipesCollection
from eathelp.resources.recipe import RecipeCollection, RecipeItem
from eathelp.resources.cookbook import CookbookCollection, CookbookItem
from eathelp.resources.ingredient import IngredientCollection, IngredientItem
from eathelp.resources.recipe_ingredient import RecipeIngredientCollection
from eathelp.resources.recipe_ingredient import RecipeIngredientItem
from eathelp.resources.user import UserCollection, UserItem

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(UserCollection, "/chefs/")
api.add_resource(UserItem, "/chefs/<int:chef>")
api.add_resource(
    CookbookCollection, "/chefs/<int:chef>/cookbooks/", "/cookbooks/")
api.add_resource(CookbookItem, "/chefs/<int:chef>/cookbooks/<int:cookbook>")
api.add_resource(RecipeCollection, "/chefs/<int:chef>/recipes/", "/recipes/")
api.add_resource(RecipeItem, "/chefs/<int:chef>/recipes/<int:recipe>",
                 "/recipes/<int:recipe>")
api.add_resource(
    RecipeIngredientCollection, "/recipes/<int:recipe>/ingredients/")
api.add_resource(RecipeIngredientItem,
                 "/recipes/<int:recipe>/ingredients/<int:r_ingredient>")
api.add_resource(IngredientCollection, "/ingredients/")
api.add_resource(IngredientItem, "/ingredients/<int:ingredient>")
api.add_resource(
    CookbookRecipesCollection, "/cookbooks/<int:cookbook>/recipes")
api.add_resource(
    CookbookRecipesItem, "/cookbooks/<int:cookbook>/recipes/<int:recipe>")

# Parameters used:
# - <int:chef> = User.user_id OR <string:chef> = User.username
# - <int:cookbook> = Cookbook.cookbook_id
# - <int:recipe> = Recipe.recipe_id
# - <int:ingredient> [from /ingredients/<int:ingredient>]
#   = Ingredient.ingredient_id
# - <int:ingredient> [from /recipes/<int:recipe>/ingredients/<int:ingredient>]
#   = RecipeIngredient.rec_ing_id
# #

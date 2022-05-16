from flask import Blueprint
from flask_restful import Api

from eathelp.resources.recipe import RecipeCollection, RecipeItem
from eathelp.resources.cookbook import CookbookCollection, CookbookItem
from eathelp.resources.ingredient import IngredientCollection, IngredientItem
from eathelp.resources.recipe_ingredient import RecipeIngredientCollection, RecipeIngredientItem
from eathelp.resources.user import UserCollection, UserItem

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

api.add_resource(UserCollection, "/chefs/")
api.add_resource(UserItem, "/chefs/<chef>")     # "/chefs/<int:chef>"
api.add_resource(CookbookCollection, "/chefs/<chef>/cookbooks/", "/cookbooks/")     # "/chefs/<int:chef>"
api.add_resource(CookbookItem, "/chefs/<chef>/cookbooks/<int:cookbook>")    # "/chefs/<int:chef>"
api.add_resource(RecipeCollection, "/chefs/<int:chef>/recipes/", "/recipes/")
api.add_resource(RecipeItem, "/chefs/<int:chef>/recipes/<int:recipe>", "/recipes/<int:recipe>")
api.add_resource(RecipeIngredientCollection, "/recipes/<int:recipe>/ingredients/")
api.add_resource(RecipeIngredientItem, "/recipes/<int:recipe>/ingredients/<int:ingredient>")
api.add_resource(IngredientCollection, "/ingredients/")
api.add_resource(IngredientItem, "/ingredients/<int:ingredient>")

# Parameters used:
# - <int:chef> = User.user_id OR <chef> = User.username
# - <int:cookbook> = Cookbook.cookbook_id
# - <int:recipe> = Recipe.recipe_id
# - <int:ingredient> [from URI "/ingredients/<int:ingredient>" ] = Ingredient.ingredient_id
# - <int:ingredient> [from URI "/recipes/<int:recipe>/ingredients/<int:ingredient>" ] = RecipeIngredient.rec_ing_id
# #

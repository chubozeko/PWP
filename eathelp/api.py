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
api.add_resource(UserItem, "/chefs/{chef}")
api.add_resource(CookbookCollection, "/chefs/{chef}/cookbooks/", "/cookbooks/")
api.add_resource(CookbookItem, "/chefs/{chef}/cookbooks/{cookbook}")
api.add_resource(RecipeCollection, "/chefs/{chef}/recipes/", "/recipes/")
api.add_resource(RecipeItem, "/chefs/{chef}/recipes/{recipe}", "/recipes/{recipe}")
api.add_resource(RecipeIngredientCollection, "/recipes/{recipe}/ingredients/")
api.add_resource(RecipeIngredientItem, "/recipes/{recipe}/ingredients/{ingredient}")
api.add_resource(IngredientCollection, "/ingredients/")
api.add_resource(IngredientItem, "/ingredients/{ingredient}")
from flask import Blueprint
from flask_restful import Api

from eathelp.resources.recipe import RecipeCollection, RecipeItem

blueprint = Blueprint("api", __name__, url_prefix="/api")
api = Api(blueprint)

# TODO: add resource routes [PWP-18]
api.add_resource(RecipeCollection, "/recipes/")
# api.add_resource(RecipeItem, "/recipes/{recipe_id}/")
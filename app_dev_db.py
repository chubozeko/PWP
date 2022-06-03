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

import os

# starts the EatHelp API app
from eathelp import create_app
app = create_app(init_db=True)
port = os.environ.get("PORT", 5000)

"""For development server:"""
app.run(debug=True)


@app.route("/")
def home_documentation():
    return "<h1>EatHelp API</h1>" \
           "<p>Usage of the API will be included here.</p>", 200


@app.route("/favicon.ico")
def favicon():
    return "<h1>EatHelp API: favicon.ico</h1> ", 200

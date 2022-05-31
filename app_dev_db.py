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
           "<p>Documentation and Usage of the API will be included here.</p>", 200

@app.route("/favicon.ico")
def favicon():
    return "<h1>EatHelp API: favicon.ico</h1> ", 200



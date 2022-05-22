# starts the EatHelp API app
from eathelp import create_app
app = create_app()
app.run()
# app.run(debug=True)

@app.route("/")
def home_documentation():
    return "<h1>EatHelp API</h1> " \
           "<p>*Documentation and Usage of the API will be included here.</p>"

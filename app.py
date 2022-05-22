# starts the EatHelp API app
from eathelp import create_app
app = create_app()
app.run(host="0.0.0.0", port=5000)
# app.run(debug=True)

@app.route("/")
def home_documentation():
    return "<h1>EatHelp API</h1> " \
           "<p>*Documentation and Usage of the API will be included here.</p>"

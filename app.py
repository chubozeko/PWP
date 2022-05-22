# starts the EatHelp API app
from eathelp import create_app
app = create_app()
# app.run(debug=True)

@app.route("/")
def home_documentation():
    return "<h1>EatHelp API</h1>" \
           "<p>Documentation and Usage of the API will be included here.</p>", 200

@app.route("/favicon.ico")
def favicon():
    return "<h1>EatHelp API: favicon.ico</h1> ", 200

app.run(host="0.0.0.0", port=5000)
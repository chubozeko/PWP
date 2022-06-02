##
# !! This is intended of the STAGING DEPLOYMENT of EatHelp API on Heroku. !!
##

import os
# starts the EatHelp API app
from eathelp import create_app
app = create_app(init_db=True)
port = os.environ.get("PORT", 5000)

"""For staging/production server:"""
app.run(debug=False, host="0.0.0.0", port=port)

@app.route("/")
def home_documentation():
    return "<h1>EatHelp API</h1>" \
           "<p>Documentation and Usage of the API will be included here.</p>", 200

@app.route("/favicon.ico")
def favicon():
    return "<h1>EatHelp API: favicon.ico</h1> ", 200 



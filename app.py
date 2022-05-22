# starts the EatHelp API app
from eathelp import create_app
app = create_app()
app.run(debug=False)

# app.run(debug=True)

# EatHelp API (v.0.0.3)

## Setting up the Environment:

To run the EatHelp API locally, you would need to install Python and the required libraries in a virtual environment.
1. Create a virtual environment: 
   ```commandline
   python -m venv /path/to/new/virtual/environment
   ```
2. Run the virtual environment:
   1. Linux (bash)
   ```commandline
   source /path/to/new/virtual/environment/bin/activate
   ```
   2. Windows
   ```commandline
   .\Scripts\activate.bat
   ```
3. Install the required libraries from the `requirements.txt` file:
   ```commandline
   pip install -r requirements.txt
   ```

## Configuring and Running the RESTful API 
To run the EatHelp API, you can either run the API only or initialize the MySQL database and run the API, depending on if the MySQL database has already been set up.
The MySQL database credentials found in `credentials.py` need to be entered before running the API. Make sure your MySQL database is already up and running.
To setup and populate the database, refer to [db/README.md](https://github.com/chubozeko/PWP/tree/master/eathelp/db)

Use the following commands to start your local API server:
- Run the API only:
   ```commandline
   python app_dev.py
   ```
- Initialize database and Run the API:
   ```commandline
   python app_dev_db.py
   ```

## EatHelp API Usage
Once the API server is up and running, you can use the following like to run the API requests: 
http://localhost:5000/

To see all the full EatHelp API documentation, refer to http://eathelp-api.herokuapp.com/apidocs/.

### EatHelp API deployed on Heroku
This API has been uploaded to Heroku and can be accessed from the following website:
https://eathelp-api.herokuapp.com/



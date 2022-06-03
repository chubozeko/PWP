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

##
# This is the function that gets the database credentials.
# The database used for this API is 'pwp_db'.
#
# The credential data should be entered according to the MySQL database setup.
# Important credentials:
#   - user (default: root)
#   - password
#   - host (default: 127.0.0.1 -> localhost)
#   - port (MySQL default: 3306)
# ##


def get_db_credentials():
    return {
        "user": "",
        "password": "",
        "host": "",
        "port": "",
        "database_name": "",
        "query_params": ""
    }

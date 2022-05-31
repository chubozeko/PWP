##
# This is the function that gets the database credentials. The database used for this API is 'pwp_db'.
#
# The credential data can be filled in according to how the MySQL database was set up.
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
        "database_name": "pwp_db",
        "query_params": ""
    }

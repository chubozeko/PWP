# Local db server credentials (Docker)
# def get_db_credentials():
#     return {
#         "user": "root",
#         "password": "password",
#         "host": "127.0.0.1",
#         "port": "5306",
#         "database_name": "pwp_db",
#         "query_params": ""
#     }

# Online db server credentials (Heroku)
def get_db_credentials():
    return {
        "user": "b051e6fbeb1906",
        "password": "0d656e0b",
        "host": "eu-cdbr-west-02.cleardb.net",
        "port": "3306",
        "database_name": "heroku_5fc161546536f99",
        "query_params": "?reconnect=true"
    }
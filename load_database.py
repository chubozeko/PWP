import mysql.connector
import json

# Load database credentials
fd = open('db/credentials.json')
credData = json.load(fd)
fd.close()

pwp_db = mysql.connector.connect(
    host=credData['dbCredentials']['host'],
    port=str(credData['dbCredentials']['port']),
    user=credData['dbCredentials']['user'],
    passwd=credData['dbCredentials']['password']
)

def executeSql(sqlFile, db_cursor):
    fd = open(sqlFile, 'r')
    sql_db_create = fd.read()
    fd.close()
    sqlCmds = sql_db_create.split(';')
    for command in sqlCmds:
        try:
            db_cursor.fetchall()
            db_cursor.execute(command)
        except ():
            print("Command skipped: ")

db_cursor = pwp_db.cursor()
db_cursor.execute("SET foreign_key_checks = 0;")
executeSql('db/pwp_db_create.sql', db_cursor)
db_cursor.execute("SET foreign_key_checks = 1;")
executeSql('db/pwp_db_insert.sql', db_cursor)

# db_cursor.execute("SELECT * FROM recipe WHERE recipe_id=1;")
# for db in db_cursor:
#     print(db)
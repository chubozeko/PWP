
import mysql.connector

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="5306",
    user="root",
    passwd="password"
)

my_cursor = mydb.cursor()

my_cursor.execute("SHOW DATABASES")
for db in my_cursor:
    print(db)
import mysql.connector
from pymysql import Error

from credentials import get_db_credentials

def db_connection_mysql(init_db=False):
    conn = None
    try:
        # Connect to MySQL database
        mysql_db = MySQLDatabase()
        conn = mysql_db.connect()
        mysql_db.initialize(conn, init_db)
    except Error as e:
        print('Error: ', e)
    except Exception as e:
        print('Exception: ', e)
    return conn

def initialize_db_cursor(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("USE " + get_db_credentials()["database_name"])
    except Error as e:
        print('Error: ', e)
    except Exception as e:
        print('Exception: ', e)
    return cursor


class MySQLDatabase:
    # Load database credentials
    credentials = get_db_credentials()

    def connect(self):
        conn = None
        # Connect to MySQL database
        try:
            conn = mysql.connector.connect(
                host = self.credentials['host'],
                port = str(self.credentials['port']),
                user = self.credentials['user'],
                passwd = self.credentials['password']
            )
        except Error as e:
            print('Error: ', e)
        except Exception as e:
            print('Exception: ', e)
        return conn

    def initialize(self, connection, init_db: bool):
        # Initialize DB cursor
        db_cursor = connection.cursor()
        db_cursor.execute("USE " + get_db_credentials()["database_name"])
        db_cursor.execute("SET foreign_key_checks = 0;")
        # Initialize DB from SQL
        if init_db:
            self.executeSql('eathelp/db/pwp_db_create.sql', db_cursor)
            connection.commit()
            print(" * Database '" + get_db_credentials()["database_name"] + "' created!")
            db_cursor.execute("SET foreign_key_checks = 1;")
            self.executeSql('eathelp/db/pwp_db_insert.sql', db_cursor)
            connection.commit()
            print(" * Database '" + get_db_credentials()["database_name"] + "' populated!")

    def executeSql(self, sqlFile, db_cursor):
        fd = open(sqlFile, 'r')
        sql_db_create = fd.read()
        fd.close()
        sqlCmds = sql_db_create.split(';')
        for command in sqlCmds:
            try:
                sql = command + ";"
                db_cursor.execute(command)
                db_cursor.fetchall()
                print("sql cmd: " + sql)
            except ():
                print("Command skipped: ")

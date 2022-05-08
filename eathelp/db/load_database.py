import mysql.connector
import json
import pymysql
from pymysql import Error

from credentials import get_db_credentials


class MySQLDatabase:
    # Load database credentials
    credentials = get_db_credentials()
    # fd = open('db/credentials.json', 'r')
    # credentials = json.load(fd)
    # fd.close()

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
        db_cursor.execute("USE pwp_db;")
        db_cursor.execute("SET foreign_key_checks = 0;")
        # Initialize DB from SQL
        if init_db:
            self.executeSql('pwp_db_create.sql', db_cursor)
            # db_cursor.execute("SET foreign_key_checks = 1;")
            self.executeSql('pwp_db_insert.sql', db_cursor)

    def executeSql(self, sqlFile, db_cursor):
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

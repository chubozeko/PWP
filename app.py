from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from pymysql import Error

from credentials import get_db_credentials
from eathelp.db.load_database import MySQLDatabase

# app = Flask(__name__, static_folder="static")
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://" + \
#                                         get_db_credentials()["user"] + \
#                                         ":" + get_db_credentials()["password"] + \
#                                         "@" + get_db_credentials()["port"] + \
#                                         "/" + get_db_credentials()["database_name"]
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# api = Api(app)
# db = SQLAlchemy(app)

def db_connection_mysql():
    conn = None
    try:
        # Connect to MySQL database
        mysql_db = MySQLDatabase()
        conn = mysql_db.connect()
        mysql_db.initialize(conn, False)
    except Error as e:
        print('Error: ', e)
    except Exception as e:
        print('Exception: ', e)
    return conn

def initialize_db_cursor(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("USE pwp_db")
    except Error as e:
        print('Error: ', e)
    except Exception as e:
        print('Exception: ', e)
    return cursor

#
# @app.route("/api/recipe", methods=['GET', 'POST'])
# def recipes():
#     conn = db_connection_mysql()
#     cursor = conn.cursor()
#
#     if request.method == 'GET':
#         cursor.execute("SELECT * FROM recipe")
#         rows = cursor.fetchall()
#         recipes = []
#         for row in rows:
#             recipes.append(
#                 dict(
#                     recipe_id = row[0],
#                     recipe_name = row[1],
#                     prep_time = row[2],
#                     cooking_time = row[3],
#                     meal_type = row[4],
#                     calories = row[5],
#                     servings = row[6],
#                     instructions = row[7],
#                     creator_id = row[8]
#                 )
#             )
#         if recipes is not None:
#             return jsonify(recipes), 200
#         else:
#             return 'Nothing Found', 404
#
#     if request.method == 'POST':
#         recipe_name = request.json['recipe_name']
#         prep_time = request.json['prep_time']
#         cooking_time = request.json['cooking_time']
#         meal_type = request.json['meal_type']
#         calories = request.json['calories']
#         servings = request.json['servings']
#         instructions = request.json['instructions']
#         creator_id = request.json['creator_id']
#
#         sql = """INSERT INTO recipe (recipe_name, prep_time, cooking_time, meal_type, calories, servings, creator_id, instructions) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
#         cursor.execute(sql, (recipe_name, prep_time, cooking_time, meal_type, calories, servings, creator_id, '\n'.join(instructions)))
#         conn.commit()
#         return f"Recipe created successfully!", 200
#

# from eathelp import create_app
# app = create_app
# app.run()

# if __name__ == '__main__':
#     app.run()


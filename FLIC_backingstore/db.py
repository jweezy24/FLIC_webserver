from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2
import os
import time

class database:
    def __init__(self):
        self.connect_str = f"dbname='flicdb' user='flic' host='localhost' password='{os.environ['FLIC_PASS']}'"

    def create_db(self):
        try:
            # use our connection values to establish a connection
            conn = psycopg2.connect(self.connect_str)
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            # create a new table with a single column called "name"
            cursor.execute("""CREATE TABLE data (key integer, val double precision, node char(40), created_seconds double precision, recieved_seconds double precision, difference double precision, );""")
            # run a SELECT statement - no data in there, but we can try it
            cursor.execute("""SELECT * from data""")
            conn.commit() # <--- makes sure the change is shown in the database
            rows = cursor.fetchall()
            print(rows)
            cursor.close()
            conn.close()
        except Exception as e:
            print("Password wrong or db already created.")
            print(e)

    def insert_data(self,data):
        conn = psycopg2.connect(self.connect_str)
        cursor = conn.cursor()
        query = f"INSERT INTO data VALUES ({data[0]}, {data[1]}, '{data[2]}', {data[3]}, {time.time()} );"
        cursor.execute(query)
        conn.commit()

    def get_data(self, node,key,val):
        conn = psycopg2.connect(self.connect_str)
        cursor = conn.cursor()
        query = f"SELECT * FROM data WHERE key={key} and val={val} and node='{node}';"
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows

if __name__ == '__main__':
    create_db()

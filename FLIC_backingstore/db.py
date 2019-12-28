from flask import current_app, g
from flask.cli import with_appcontext
import psycopg2
import os
import time

class database:
    def __init__(self,drop_data):
        self.connect_str = f"dbname='flicdb' user='flic' host='localhost' password='{os.environ['FLIC_PASS']}'"
        if self.create_dbs() and drop_data:
            pass
        elif not self.create_dbs() and drop_data:
            self.clear_dbs()
            self.create_dbs()

        self.test_num = self.get_increment()
            

    def create_dbs(self):
        try:
            # use our connection values to establish a connection
            conn = psycopg2.connect(self.connect_str)
            # create a psycopg2 cursor that can execute queries
            cursor = conn.cursor()
            # DB for main data
            cursor.execute("""CREATE TABLE data (key integer, val double precision, node char(40), created_on_node double precision, 
            flic_recieved_time double precision,ttl double precision, write_manager_recived_time double precision, 
            write_manager_send_time double precision, db_write_time double precision, test_number integer);""")
            
            conn.commit() # <--- makes sure the change is shown in the database

            #DB for basic node info
            cursor.execute("""CREATE TABLE nodes (mac unique char(40), node char(40), ip char(40) );""")

            conn.commit() # <--- makes sure the change is shown in the database
            cursor.close()
            conn.close()
            return True
        except Exception as e:
            print("Password wrong or db already created.")
            print(e)
            return False

    def clear_dbs(self):
        # use our connection values to establish a connection
        conn = psycopg2.connect(self.connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
        # create a new table with a single column called "name"
        cursor.execute("""drop table if exists data;""")
        conn.commit()
        cursor.execute("""drop table if exists nodes;""")
        conn.commit()
        with open("./FLIC_backingstore","w") as f:
            f.write("1")
        cursor.close()
        conn.close()

    def init_node(self,data):
        conn = psycopg2.connect(self.connect_str)
        cursor = conn.cursor()
        query = f"INSERT INTO nodes VALUES ('{data[0]}', '{data[1]}', '{data[2]}');"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def insert_data(self,data):
        conn = psycopg2.connect(self.connect_str)
        cursor = conn.cursor()
        recieved = time.time()
        query = f"INSERT INTO data VALUES ({data[0]}, {data[1]}, '{data[2]}', {data[3]}, {data[4]}, {data[5]}, {data[6]}, {data[7]}, {recieved}, {self.test_num});"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()

    def get_data(self,key,val,node):
        conn = psycopg2.connect(self.connect_str)
        cursor = conn.cursor()
        query = f"SELECT * FROM data WHERE key={key} and val={val} and node='{node}';"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    def get_increment(self):
        with open('./FLIC_backingstore/test_iter.txt', 'r') as f:
            for lines in f:
                test_num = int(lines)

        return test_num

    def set_iter(self):
        with open('./FLIC_backingstore/test_iter.txt', 'r') as f:
            for lines in f:
                test_num = int(lines)
        with open('./FLIC_backingstore/test_iter.txt', 'w') as f:
            f.write(str(test_num+1))
        
        self.test_num = test_num+1

    def get_all(self, experiment_number):
        conn = psycopg2.connect(self.connect_str)
        cursor = conn.cursor()
        query = f"SELECT * FROM data where test_number={experiment_number};"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

if __name__ == '__main__':
    create_db()

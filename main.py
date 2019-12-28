import os
import sys
from flask import Flask
sys.path.insert(1, './FLIC_backingstore')
import db
import json
from flask import request
from flask import jsonify

#If the user would like to clear data change to True
database = db.database(False)

app = Flask(__name__)

@app.route('/insert', methods=['POST'])
def insert_data():
    data = json.loads(request.data)
    database.insert_data(data)
    return 'success'

@app.route('/getter', methods=['POST'])
def get_data():
    print(json.loads(request.data))
    val = json.loads(request.data)['val']
    got_data = database.get_data(val[0], val[1], val[3])
    ret_val = json.dumps({'data':got_data})
    return ret_val

@app.route('/all', methods=['POST'])
def get_all():
    got_data = database.get_all()
    ret_val = json.dumps({'data':got_data})
    return ret_val

@app.route('/init', methods=['POST'])
def init_data():
    data = json.loads(request.data)
    mac = data['mac']
    ip = data['ip']
    name = data['name']
    database.init_node([mac, name, ip])
    return 'success'

@app.route('/iterate', methods=['POST'])
def increase_test():
    return database.set_iter()


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=7745)

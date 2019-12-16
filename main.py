import os
import sys
from flask import Flask
sys.path.insert(1, './FLIC_backingstore')
import db
import json
from flask import request
from flask import jsonify

database = db.database()

app = Flask(__name__)

@app.route('/hello')
def test():
    return 'Hello, World!'

@app.route('/insert', methods=['POST'])
def insert_data():
    key = json.loads(request.data)['key']
    val = json.loads(request.data)['val']
    node = json.loads(request.data)['node']
    created = json.loads(request.data)['created']
    data = [key, val, node, created]
    database.insert_data(data)
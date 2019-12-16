import requests
import json
import os
import time

if os.environ.get('LOCALENVHOST') is None:
    local_env_host = "localhost"
else:
    local_env_host = os.environ['LOCALENVHOST']

base_url = "http://" + local_env_host + ":5000/"


def init_process_emulatation():
    vals = {'key':1, 'val':2.0,'node':'test','created':time.time()}
    r3 = requests.post(url=base_url + "insert",
                           data=json.dumps(vals))


if __name__ == '__main__':
    init_process_emulatation()

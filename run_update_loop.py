import os
from time import sleep

import requests
from requests.auth import HTTPBasicAuth

from src import utils
from src.functions import update_commissions_information

cfg = utils.load_config()
host = cfg.get("Settings", "host")
port = cfg.get("Settings", "port")
url = f"http://{host}:{port}/send_to_websockets"


print("Starting update thread")
while True:
    try:
        if update_commissions_information():
            r = requests.get(url, auth=HTTPBasicAuth('unassigned', os.environ["SERVICE_ACCOUNT_PASSWORD"]))
            print(r.status_code)
            print(r.content)
    except Exception as e:
        print(e)
    sleep(60)

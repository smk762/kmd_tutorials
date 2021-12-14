#!/usr/bin/env python3
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()
MM2_USERPASS = os.getenv("MM2_USERPASS")
MM2_IP = "http://127.0.0.1:7783"

def mm2_proxy(params):
  params.update({"userpass": MM2_USERPASS})
  #print(json.dumps(params))
  r = requests.post(MM2_IP, json.dumps(params))
  return r.json()

def get_activate_command(coin)
  return requests.get(f"http://stats.kmd.io/api/atomicdex/activation_commands/?coin={coin}").json()

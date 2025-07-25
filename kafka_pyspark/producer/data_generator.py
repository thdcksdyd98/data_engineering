import json
import requests
import time

def generate_random_user_data():
    res=requests.get('https://randomuser.me/api/')
    res=res.json()
    res=res['results'][0]
    return res

def stream_data(interval_seconds=1):
    while True:
        yield generate_random_user_data()
        time.sleep(interval_seconds)
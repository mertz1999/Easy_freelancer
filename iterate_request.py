import requests
import time

while(True):
    req = requests.get('http://127.0.0.1:5000?start=True')
    print("Itrate tools: ", req.status_code)
    time.sleep(150)
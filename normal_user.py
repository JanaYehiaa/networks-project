import requests
import time

while True:
    try:
        requests.get("http://127.0.0.1:5000")
        print("Normal request")
        time.sleep(20)
    except:
        print("Server down")

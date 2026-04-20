import requests
import time

TARGET = "http://127.0.0.1:5001"

while True:
    try:
        requests.get(TARGET)
        print("Normal request")
        time.sleep(1)
    except:
        print("Server down")

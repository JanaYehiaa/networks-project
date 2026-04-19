import requests
import time
import csv

THRESHOLD = 50  # requests in last 10 seconds

while True:
    try:
        r = requests.get("http://127.0.0.1:5000/stats").json()
        count = r["requests_last_10_sec"]

        print(f"Traffic (10s window): {count}")

        if count > THRESHOLD:
            print("🚨 DDoS ATTACK DETECTED!")

        with open("traffic_log.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    time.strftime("%H:%M:%S"),
                    count,
                    "ATTACK" if count > THRESHOLD else "NORMAL",
                ]
            )

        time.sleep(1)

    except:
        print("Detector cannot reach server")
        time.sleep(1)

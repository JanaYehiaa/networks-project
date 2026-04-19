from flask import Flask, jsonify
import time

app = Flask(__name__)

request_times = []


@app.route("/")
def home():
    global request_times
    now = time.time()
    request_times.append(now)

    # keep only last 10 seconds
    request_times = [t for t in request_times if now - t < 10]

    return "OK"


@app.route("/stats")
def stats():
    return jsonify({"requests_last_10_sec": len(request_times)})


if __name__ == "__main__":
    app.run(port=5000)

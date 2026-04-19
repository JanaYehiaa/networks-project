from flask import Flask, jsonify, request, abort
import time
from collections import defaultdict

app = Flask(__name__)

request_times = []
ip_request_times = defaultdict(list)

RATE_LIMIT = 10  # max requests per IP per 10 seconds


@app.route("/")
def home():
    global request_times
    now = time.time()
    ip = request.remote_addr

    # Per-IP rate limiting
    ip_request_times[ip] = [t for t in ip_request_times[ip] if now - t < 10]
    if len(ip_request_times[ip]) >= RATE_LIMIT:
        abort(429)  # Too Many Requests

    ip_request_times[ip].append(now)
    request_times.append(now)
    request_times = [t for t in request_times if now - t < 10]

    return "OK"


@app.route("/stats")
def stats():
    return jsonify({"requests_last_10_sec": len(request_times)})


if __name__ == "__main__":
    app.run(port=5001)  # different port from unprotected

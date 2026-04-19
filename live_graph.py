import matplotlib.pyplot as plt
import matplotlib.animation as animation
import requests
import time

unprotected_data = []
protected_data = []
time_labels = []
start_time = time.time()

fig, ax = plt.subplots()


def update(frame):
    try:
        u = requests.get("http://127.0.0.1:5000/stats", timeout=1).json()[
            "requests_last_10_sec"
        ]
    except:
        u = 0
    try:
        p = requests.get("http://127.0.0.1:5001/stats", timeout=1).json()[
            "requests_last_10_sec"
        ]
    except:
        p = 0

    elapsed = round(time.time() - start_time)
    time_labels.append(elapsed)
    unprotected_data.append(u)
    protected_data.append(p)

    # keep only last 60 seconds on screen
    display_limit = 60
    t = time_labels[-display_limit:]
    ud = unprotected_data[-display_limit:]
    pd_ = protected_data[-display_limit:]

    ax.clear()
    ax.plot(t, ud, label="Unprotected Server (port 5000)", color="red", linewidth=2)
    ax.plot(t, pd_, label="Protected Server (port 5001)", color="green", linewidth=2)
    ax.axhline(
        y=50, color="orange", linestyle="--", label="Detection Threshold (50 req/10s)"
    )
    ax.set_title("Live DDoS Traffic: Unprotected vs Protected Server")
    ax.set_xlabel("Time (seconds since start)")
    ax.set_ylabel("Requests per 10-second window")
    ax.legend(loc="upper left")
    ax.set_ylim(bottom=0)


ani = animation.FuncAnimation(fig, update, interval=1000)
plt.tight_layout()
plt.show()

# DDoS Attack & Mitigation — Local Simulation

A localhost simulation of an HTTP GET flood DDoS attack. Demonstrates the difference between an unprotected and rate-limited server under coordinated botnet traffic, with live detection and traffic visualization.

---

## What This Simulates

- An **HTTP GET flood** attack (Layer 7)
- A **botnet** of up to 100 concurrent threads ramping up gradually
- **Threshold-based detection** flagging the attack in real time
- **Rate limiting** as a mitigation technique
- Side-by-side comparison of an unprotected vs. protected server

All traffic stays on `127.0.0.1`.

---

## Project Structure
```text
project/
├── unprotected_server.py   # Flask server with no defenses (port 5000)
├── protected_server.py     # Flask server with rate limiting (port 5001)
├── attacker.py             # Botnet simulation (HTTP GET flood)
├── normal_user.py          # Legitimate user (1 request/sec)
├── detector.py             # Real-time attack detection + CSV logging
├── live_graph.py           # Live traffic visualization (matplotlib)
├── traffic_log.csv         # Auto-generated log file
├── requirements.txt        # Project dependencies
└── Makefile                # Automation scripts
```
---

## Requirements

- Python 3.8+
- On Windows: run commands manually (see below) or install `make` via Chocolatey

Install dependencies:

```bash
# Mac/Linux
make setup

# Windows
python -m venv .venv
.venv\Scripts\pip install flask requests matplotlib
```

---

## How to Run

Open a **separate terminal for each component** and run in this order:

| Step | Mac/Linux | Windows |
|------|-----------|---------|
| 1. Unprotected server | `make server` | `.venv\Scripts\python server_unprotected.py` |
| 2. Protected server | `make protected` | `.venv\Scripts\python server_protected.py` |
| 3. Live graph | `make graph` | `.venv\Scripts\python live_graph.py` |
| 4. Detector | `make detector` | `.venv\Scripts\python detector.py` |
| 5. Legitimate user | `make user` | `.venv\Scripts\python legitimate_user.py` |
| 6. Attacker | `make attack` | `.venv\Scripts\python attacker.py` |

Wait a few seconds after starting the servers before launching anything else.

---

## Demo Procedure

### Phase 1 — Baseline
With everything running except the attacker, observe:
- Detector: `Traffic (10s window): 1` — calm baseline
- Graph: both lines flat and low
- Legitimate user: `Normal request` every second

### Phase 2 — Attack on Unprotected Server
Ensure `attacker.py` has:
```python
TARGET = "http://127.0.0.1:5000"
```
Launch the attacker and observe:
- Attacker ramps from 5 → 100 threads over ~40 seconds
- Detector crosses threshold and prints `🚨 DDoS ATTACK DETECTED!`
- Graph: red line spikes to 1000–3000+ requests per 10-second window
- Legitimate user: `Server down` — denied service
- Eventually: `Detector cannot reach server` — server fully overwhelmed

### Phase 3 — Attack on Protected Server
Stop the attacker, change target and relaunch:
```python
TARGET = "http://127.0.0.1:5001"
```
Observe:
- Graph: green line holds flat at ~10 (rate limit ceiling)
- Detection threshold never crossed
- Legitimate user: `Normal request` — service maintained
- Wireshark: flood of `HTTP 429 Too Many Requests` responses

---

## Wireshark

Start Wireshark **before** launching any scripts. Select the **loopback interface** (`lo` on Mac/Linux, `Loopback Adapter` on Windows).

### Useful filters:

#### All traffic to both servers
```text
tcp.port == 5000 or tcp.port == 5001
```
#### GET flood on unprotected server
```text
http.request.method == "GET" and tcp.port == 5000
```
#### Rate limiter rejecting botnet on protected server
```text
http.response.code == 429 and tcp.port == 5001
```
---

## Detection Logic

The detector polls `/stats` every second. If requests in the last 10-second window exceed **50**, an attack is flagged. Every reading (NORMAL or ATTACK) is logged to `traffic_log.csv` with a timestamp.

---

## Rate Limiting (Protected Server)

Each IP is allowed a maximum of **10 requests per 10-second window**. Requests beyond this receive an `HTTP 429` response immediately, before any server-side processing occurs. The legitimate user (1 req/sec) stays well under this limit and is never affected.

---

## Notes

- `Detector cannot reach server` during the attack is expected and intentional — it means the server is fully overwhelmed, which is the definition of a successful DDoS
- The attacker uses random jitter (0.01–0.2s delay per thread) to simulate realistic distributed traffic rather than perfectly uniform mechanical requests
- Each thread in the attacker represents one bot in the simulated botnet

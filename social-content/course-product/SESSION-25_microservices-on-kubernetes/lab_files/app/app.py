"""One small image that plays every Atithi service. SERVICE_NAME picks the role."""
import json
import os
import time
import urllib.request

from flask import Flask, jsonify

SERVICE = os.environ.get("SERVICE_NAME", "rooms")
MODE = os.environ.get("APP_MODE", "unset")          # from the ConfigMap
PER_PAGE = os.environ.get("ROOMS_PER_PAGE", "10")   # from the ConfigMap
ROOMS_URL = os.environ.get("ROOMS_URL", "http://rooms-service:5000")

app = Flask(__name__)
_leak = []


@app.get("/health")
def health():
    return "ok"


@app.get(f"/api/{SERVICE}/health")
def health_prefixed():
    return "ok"


@app.get(f"/api/{SERVICE}/")
def home():
    body = {"service": SERVICE, "mode": MODE, "per_page": PER_PAGE}
    if SERVICE == "bookings":
        # a service-to-service call with a timeout and two short retries
        last = None
        for attempt in range(2):
            try:
                with urllib.request.urlopen(f"{ROOMS_URL}/api/rooms/", timeout=2) as r:
                    body["rooms"] = json.loads(r.read())
                    return jsonify(body)
            except Exception as exc:  # noqa: BLE001
                last = str(exc)
                time.sleep(0.2 * (attempt + 1))
        body["error"] = f"rooms-service unavailable: {last}"
        return jsonify(body), 503
    return jsonify(body)


@app.get("/leak")
def leak():
    """Allocate 10 MB per call, to show a memory limit (OOMKilled, exit 137)."""
    _leak.append(bytearray(10 * 1024 * 1024))
    return f"holding {len(_leak) * 10} MB\n"

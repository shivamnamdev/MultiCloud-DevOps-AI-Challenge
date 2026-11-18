import os
import time

from flask import Flask, Response, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest

app = Flask(__name__)

REQUESTS = Counter("http_requests_total", "HTTP requests", ["method", "path", "status"])
LATENCY = Histogram("http_request_duration_seconds", "Request time in seconds", ["path"])


@app.before_request
def start_timer():
    request._started = time.perf_counter()


@app.after_request
def record(resp):
    # label by the route template (for example /rooms/<room_id>), never by the real id
    path = request.url_rule.rule if request.url_rule else "unmatched"
    if path != "/metrics":
        REQUESTS.labels(request.method, path, str(resp.status_code)).inc()
        LATENCY.labels(path).observe(time.perf_counter() - request._started)
    return resp


@app.get("/")
def home():
    if os.environ.get("BREAK") == "1":      # practice switch for the alert lab
        return "broken on purpose", 500
    return "Atithi rooms-service"


@app.get("/health")
def health():
    return "ok"


@app.get("/rooms/<room_id>")
def room(room_id):
    return f"room {room_id}"


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

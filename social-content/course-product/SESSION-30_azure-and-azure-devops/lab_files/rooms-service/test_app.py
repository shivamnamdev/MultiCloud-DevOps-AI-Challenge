import json
import threading
import urllib.request
from http.server import HTTPServer

import app


def test_health_and_rooms():
    srv = HTTPServer(("127.0.0.1", 0), app.Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{srv.server_port}"
    assert json.load(urllib.request.urlopen(base + "/health")) == {"status": "ok"}
    assert len(json.load(urllib.request.urlopen(base + "/rooms"))) == 2
    srv.shutdown()

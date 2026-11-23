"""Tiny rooms-service for the Session 30 labs. Standard library only."""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOMS = [{"id": 101, "type": "deluxe", "free": True}, {"id": 102, "type": "suite", "free": False}]


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body):
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok"})
        elif self.path == "/rooms":
            self._send(200, ROOMS)
        else:
            self._send(404, {"error": "not found"})

    def log_message(self, *args):  # keep container logs quiet
        pass


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8080), Handler).serve_forever()

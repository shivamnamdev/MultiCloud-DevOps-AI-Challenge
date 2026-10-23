"""Local study web app server (stdlib only). See architecture/webapp.md.

    python3 tools/server.py [--port 8765]
Open http://127.0.0.1:8765
"""
import argparse
import datetime
import json
import mimetypes
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPT_STATUSES = {"not_started", "read", "lab_done", "mastered"}
QUESTION_STATUSES = {"not_started", "known", "review"}
CSP = ("default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; "
       "style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'")
MAX_BODY = 10_000


class Store:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with self._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS progress "
                      "(item_id TEXT PRIMARY KEY, status TEXT NOT NULL, updated_at TEXT NOT NULL)")

    def _conn(self):
        return sqlite3.connect(self.path)

    def all(self):
        c = self._conn()
        try:
            return {r[0]: r[1] for r in c.execute("SELECT item_id, status FROM progress")}
        finally:
            c.close()

    def set(self, item_id, status):
        c = self._conn()
        try:
            with c:
                c.execute("INSERT INTO progress VALUES (?,?,?) ON CONFLICT(item_id) DO UPDATE "
                          "SET status=excluded.status, updated_at=excluded.updated_at",
                          (item_id, status, datetime.datetime.utcnow().isoformat() + "Z"))
        finally:
            c.close()


class Content:
    def __init__(self, content_dir):
        self.dir = content_dir

    def units(self):
        out = []
        if not os.path.isdir(self.dir):
            return out
        for name in sorted(os.listdir(self.dir)):
            p = os.path.join(self.dir, name, "unit.json")
            if os.path.isfile(p):
                with open(p, encoding="utf-8") as f:
                    out.append(json.load(f))
        return out

    def unit(self, unit_id):
        for u in self.units():
            if u["id"] == unit_id:
                for c in u["concepts"]:
                    c["diagram_src"] = self._diagram(c.get("diagram"))
                return u
        return None

    def _diagram(self, d):
        if not d:
            return None
        base = os.path.realpath(self.dir)
        p = os.path.realpath(os.path.join(os.path.dirname(self.dir), d["path"]))
        if not p.startswith(base + os.sep) or not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8") as f:
            return f.read()

    def item_kinds(self):
        kinds = {}
        for u in self.units():
            for c in u["concepts"]:
                kinds[c["id"]] = "concept"
            for q in u["questions"]:
                kinds[q["id"]] = "question"
        return kinds


def make_handler(content, store, web_dir):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            pass

        def _send(self, code, body, ctype="application/json"):
            if not isinstance(body, bytes):
                body = json.dumps(body).encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Content-Security-Policy", CSP)
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path == "/api/units":
                prog = store.all()
                out = []
                for u in content.units():
                    cids = [c["id"] for c in u["concepts"]]
                    qids = [q["id"] for q in u["questions"]]
                    out.append({
                        "id": u["id"], "title": u["title"], "subtitle": u.get("subtitle", ""),
                        "concepts": len(cids), "questions": len(qids),
                        "diagrams": sum(1 for c in u["concepts"] if c.get("diagram")),
                        "concepts_studied": sum(1 for i in cids if prog.get(i, "not_started") != "not_started"),
                        "questions_known": sum(1 for i in qids if prog.get(i) == "known"),
                    })
                return self._send(200, out)
            if path.startswith("/api/units/"):
                u = content.unit(path[len("/api/units/"):])
                return self._send(200, u) if u else self._send(404, {"error": "unknown unit"})
            if path == "/api/progress":
                return self._send(200, store.all())
            return self._static(path)

        def do_POST(self):
            if self.path != "/api/progress":
                return self._send(404, {"error": "not found"})
            try:
                n = int(self.headers.get("Content-Length", "0"))
                if n <= 0 or n > MAX_BODY:
                    raise ValueError("bad length")
                req = json.loads(self.rfile.read(n))
                item_id, status = req["item_id"], req["status"]
            except (ValueError, KeyError, TypeError):
                return self._send(400, {"error": "expected JSON {item_id, status}"})
            kind = content.item_kinds().get(item_id)
            allowed = CONCEPT_STATUSES if kind == "concept" else QUESTION_STATUSES
            if kind is None:
                return self._send(404, {"error": "unknown item"})
            if status not in allowed:
                return self._send(400, {"error": "status not allowed for %s" % kind})
            store.set(item_id, status)
            return self._send(200, {"item_id": item_id, "status": status})

        def _static(self, path):
            if path in ("", "/"):
                path = "/index.html"
            elif path.startswith("/static/"):
                path = path[len("/static"):]
            else:
                return self._send(404, {"error": "not found"})
            base = os.path.realpath(web_dir)
            p = os.path.realpath(os.path.join(base, path.lstrip("/")))
            if not p.startswith(base + os.sep) or not os.path.isfile(p):
                return self._send(404, {"error": "not found"})
            ctype = mimetypes.guess_type(p)[0] or "application/octet-stream"
            if p.endswith(".js"):
                ctype = "text/javascript"
            with open(p, "rb") as f:
                return self._send(200, f.read(), ctype + ("; charset=utf-8" if ctype.startswith("text/") else ""))

    return Handler


def make_server(host="127.0.0.1", port=8765, app_dir=APP, db_path=None):
    content = Content(os.path.join(app_dir, "content"))
    store = Store(db_path or os.path.join(app_dir, "data", "progress.sqlite"))
    return ThreadingHTTPServer((host, port), make_handler(content, store, os.path.join(app_dir, "web")))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--port", type=int, default=int(os.environ.get("PORT", 8765)))
    args = p.parse_args()
    srv = make_server(port=args.port)
    print("Study app running at http://127.0.0.1:%d  (Ctrl+C to stop)" % args.port, flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())

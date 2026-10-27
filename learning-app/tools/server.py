"""Local study web app server (stdlib only). See architecture/webapp.md.

    python3 tools/server.py [--port 8765]
Open http://127.0.0.1:8765
"""
import argparse
import datetime
import json
import mimetypes
import os
import re
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from search import SearchIndex

APP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONCEPT_STATUSES = {"not_started", "read", "lab_done", "mastered"}
QUESTION_STATUSES = {"not_started", "known", "review"}
CSP = ("default-src 'self'; script-src 'self' https://cdn.jsdelivr.net; "
       "style-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'")
MAX_BODY = 20_000
MAX_NOTE = 5000


class Store:
    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with self._conn() as c:
            c.execute("CREATE TABLE IF NOT EXISTS progress "
                      "(item_id TEXT PRIMARY KEY, status TEXT NOT NULL, updated_at TEXT NOT NULL)")
            c.execute("CREATE TABLE IF NOT EXISTS notes "
                      "(item_id TEXT PRIMARY KEY, text TEXT NOT NULL, updated_at TEXT NOT NULL)")
            c.execute("CREATE TABLE IF NOT EXISTS bookmarks "
                      "(item_id TEXT PRIMARY KEY, created_at TEXT NOT NULL)")

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


    def _rows(self, sql):
        c = self._conn()
        try:
            return c.execute(sql).fetchall()
        finally:
            c.close()

    def notes(self):
        return {r[0]: r[1] for r in self._rows("SELECT item_id, text FROM notes")}

    def set_note(self, item_id, text):
        c = self._conn()
        try:
            with c:
                if text.strip():
                    c.execute("INSERT INTO notes VALUES (?,?,?) ON CONFLICT(item_id) DO UPDATE "
                              "SET text=excluded.text, updated_at=excluded.updated_at",
                              (item_id, text, datetime.datetime.utcnow().isoformat() + "Z"))
                else:
                    c.execute("DELETE FROM notes WHERE item_id=?", (item_id,))
        finally:
            c.close()

    def bookmarks(self):
        return [r[0] for r in self._rows("SELECT item_id FROM bookmarks ORDER BY created_at")]

    def set_bookmark(self, item_id, on):
        c = self._conn()
        try:
            with c:
                if on:
                    c.execute("INSERT OR IGNORE INTO bookmarks VALUES (?,?)",
                              (item_id, datetime.datetime.utcnow().isoformat() + "Z"))
                else:
                    c.execute("DELETE FROM bookmarks WHERE item_id=?", (item_id,))
        finally:
            c.close()


class Content:
    def __init__(self, content_dir):
        self.dir = content_dir
        self._kinds = None
        self._meta = None
        self._index = None
        self._sig = None

    def _paths(self):
        if not os.path.isdir(self.dir):
            return []
        return [os.path.join(self.dir, n, "unit.json") for n in sorted(os.listdir(self.dir))
                if os.path.isfile(os.path.join(self.dir, n, "unit.json"))]

    def units(self):
        out = []
        for p in self._paths():
            with open(p, encoding="utf-8") as f:
                out.append(json.load(f))
        out.sort(key=lambda u: (u.get("order", 0), u["id"]))
        return out

    def unit(self, unit_id):
        if not re.fullmatch(r"[\w-]+", unit_id or ""):
            return None
        p = os.path.join(self.dir, unit_id, "unit.json")
        if not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8") as f:
            u = json.load(f)
        for c in u["concepts"]:
            c["diagram_src"] = self._diagram(c.get("diagram"))
        return u

    def _diagram(self, d):
        if not d:
            return None
        base = os.path.realpath(self.dir)
        p = os.path.realpath(os.path.join(os.path.dirname(self.dir), d["path"]))
        if not p.startswith(base + os.sep) or not os.path.isfile(p):
            return None
        with open(p, encoding="utf-8") as f:
            return f.read()

    def _refresh(self):
        """Rebuild kinds, item metadata and the search index when any unit.json changed."""
        sig = tuple((p, os.stat(p).st_mtime) for p in self._paths())
        if sig != self._sig:
            units = self.units()
            kinds, meta = {}, {}
            for u in units:
                for c in u["concepts"]:
                    kinds[c["id"]] = "concept"
                    meta[c["id"]] = {"unit_id": u["id"], "unit_title": u["title"], "kind": "concept", "title": c["title"]}
                for q in u["questions"]:
                    kinds[q["id"]] = "question"
                    meta[q["id"]] = {"unit_id": u["id"], "unit_title": u["title"], "kind": "question", "title": q["title"]}
            self._kinds, self._meta, self._index, self._sig = kinds, meta, SearchIndex(units), sig

    def item_kinds(self):
        self._refresh()
        return self._kinds

    def item_meta(self):
        self._refresh()
        return self._meta

    def index(self):
        self._refresh()
        return self._index


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

        def _json_body(self):
            try:
                n = int(self.headers.get("Content-Length", "0"))
                if n <= 0 or n > MAX_BODY:
                    return None
                req = json.loads(self.rfile.read(n))
                return req if isinstance(req, dict) else None
            except (ValueError, TypeError):
                return None

        def do_GET(self):
            parsed = urlparse(self.path)
            path = parsed.path
            if path == "/api/search":
                qs = parse_qs(parsed.query)
                try:
                    limit = int(qs.get("limit", ["25"])[0])
                except ValueError:
                    limit = 25
                return self._send(200, content.index().search(qs.get("q", [""])[0][:200], limit))
            if path == "/api/notes":
                return self._send(200, store.notes())
            if path == "/api/bookmarks":
                return self._send(200, store.bookmarks())
            if path == "/api/mine":
                meta, notes, marks = content.item_meta(), store.notes(), store.bookmarks()
                ids = list(dict.fromkeys(marks + list(notes)))
                return self._send(200, [dict(meta[i], item_id=i, note=notes.get(i, ""), bookmarked=i in marks)
                                        for i in ids if i in meta])
            if path == "/api/units":
                prog = store.all()
                out = []
                for u in content.units():
                    cids = [c["id"] for c in u["concepts"]]
                    qids = [q["id"] for q in u["questions"]]
                    out.append({
                        "id": u["id"], "title": u["title"], "subtitle": u.get("subtitle", ""),
                        "module": u.get("module", ""), "status": u.get("status", ""),
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
            req = self._json_body()
            if req is None:
                return self._send(400, {"error": "expected a JSON object"})
            item_id = req.get("item_id")
            if not isinstance(item_id, str):
                return self._send(400, {"error": "item_id (string) required"})
            kind = content.item_kinds().get(item_id)
            if self.path not in ("/api/progress", "/api/notes", "/api/bookmarks"):
                return self._send(404, {"error": "not found"})
            if kind is None:
                return self._send(404, {"error": "unknown item"})
            if self.path == "/api/progress":
                status = req.get("status")
                allowed = CONCEPT_STATUSES if kind == "concept" else QUESTION_STATUSES
                if status not in allowed:
                    return self._send(400, {"error": "status not allowed for %s" % kind})
                store.set(item_id, status)
                return self._send(200, {"item_id": item_id, "status": status})
            if self.path == "/api/notes":
                text = req.get("text")
                if not isinstance(text, str) or len(text) > MAX_NOTE:
                    return self._send(400, {"error": "text (string, max %d chars) required" % MAX_NOTE})
                store.set_note(item_id, text)
                return self._send(200, {"item_id": item_id, "saved": bool(text.strip())})
            on = req.get("on")
            if not isinstance(on, bool):
                return self._send(400, {"error": "on (boolean) required"})
            store.set_bookmark(item_id, on)
            return self._send(200, {"item_id": item_id, "bookmarked": on})

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

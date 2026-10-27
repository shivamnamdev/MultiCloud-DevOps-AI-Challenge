import json
import os
import shutil
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import server  # noqa: E402


class ServerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        cls.srv = server.make_server(port=0, db_path=os.path.join(cls.tmp, "p.sqlite"))
        cls.base = "http://127.0.0.1:%d" % cls.srv.server_port
        threading.Thread(target=cls.srv.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.srv.shutdown()
        shutil.rmtree(cls.tmp)

    def call(self, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method="POST" if data else "GET",
                                     headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, r.read(), r.headers
        except urllib.error.HTTPError as e:
            return e.code, e.read(), e.headers

    def test_units_and_unit(self):
        code, body, _ = self.call("/api/units")
        units = json.loads(body)
        self.assertEqual(code, 200)
        self.assertEqual(units[0]["id"], "fw1")
        self.assertEqual(units[0]["questions"], 50)
        code, body, _ = self.call("/api/units/fw1")
        u = json.loads(body)
        withd = [c for c in u["concepts"] if c.get("diagram_src")]
        self.assertEqual(len(withd), 18)
        self.assertTrue(all(c["diagram_src"].split()[0] in ("graph", "sequenceDiagram") for c in withd))
        self.assertEqual(self.call("/api/units/nope")[0], 404)

    def test_progress_roundtrip_and_validation(self):
        self.assertEqual(self.call("/api/progress", {"item_id": "fw1-provider", "status": "read"})[0], 200)
        self.assertEqual(json.loads(self.call("/api/progress")[1])["fw1-provider"], "read")
        self.assertEqual(self.call("/api/progress", {"item_id": "fw1-provider", "status": "known"})[0], 400)
        self.assertEqual(self.call("/api/progress", {"item_id": "fw1-q01", "status": "mastered"})[0], 400)
        self.assertEqual(self.call("/api/progress", {"item_id": "fw1-q01", "status": "known"})[0], 200)
        self.assertEqual(self.call("/api/progress", {"item_id": "nope", "status": "read"})[0], 404)
        self.assertEqual(self.call("/api/progress", {"bad": 1})[0], 400)

    def test_static_and_traversal(self):
        code, body, h = self.call("/")
        self.assertEqual(code, 200)
        self.assertIn(b"Cloud DevOps Study", body)
        self.assertIn("script-src", h["Content-Security-Policy"])
        self.assertEqual(self.call("/static/app.js")[0], 200)
        self.assertEqual(self.call("/static/../tools/server.py")[0], 404)
        self.assertEqual(self.call("/static/%2e%2e/tools/server.py")[0], 404)
        self.assertEqual(self.call("/content/fw1/unit.json")[0], 404)

    def test_search_endpoint(self):
        code, body, _ = self.call("/api/search?q=terraform%20state")
        hits = json.loads(body)
        self.assertEqual(code, 200)
        self.assertTrue(hits)
        self.assertEqual(set(hits[0]), {"item_id", "unit_id", "unit_title", "kind", "title", "snippet"})
        self.assertEqual(json.loads(self.call("/api/search?q=")[1]), [])
        self.assertEqual(self.call("/api/search?q=%22%20OR%20NEAR(&limit=abc")[0], 200)
        self.assertEqual(self.call("/api/search?q=" + "a" * 5000)[0], 200)

    def test_notes_roundtrip_and_validation(self):
        self.assertEqual(self.call("/api/notes", {"item_id": "fw1-provider", "text": "my note"})[0], 200)
        self.assertEqual(json.loads(self.call("/api/notes")[1])["fw1-provider"], "my note")
        mine = json.loads(self.call("/api/mine")[1])
        row = [m for m in mine if m["item_id"] == "fw1-provider"][0]
        self.assertEqual((row["note"], row["unit_id"], row["bookmarked"]), ("my note", "fw1", False))
        self.assertEqual(self.call("/api/notes", {"item_id": "fw1-provider", "text": "x" * 5001})[0], 400)
        self.assertEqual(self.call("/api/notes", {"item_id": "fw1-provider", "text": 5})[0], 400)
        self.assertEqual(self.call("/api/notes", {"item_id": "nope", "text": "a"})[0], 404)
        self.call("/api/notes", {"item_id": "fw1-provider", "text": "   "})  # blank deletes
        self.assertNotIn("fw1-provider", json.loads(self.call("/api/notes")[1]))

    def test_bookmarks(self):
        self.assertEqual(self.call("/api/bookmarks", {"item_id": "fw1-q01", "on": True})[0], 200)
        self.assertIn("fw1-q01", json.loads(self.call("/api/bookmarks")[1]))
        row = [m for m in json.loads(self.call("/api/mine")[1]) if m["item_id"] == "fw1-q01"][0]
        self.assertTrue(row["bookmarked"])
        self.assertEqual(self.call("/api/bookmarks", {"item_id": "fw1-q01", "on": "yes"})[0], 400)
        self.assertEqual(self.call("/api/bookmarks", {"item_id": "fw1-q01", "on": False})[0], 200)
        self.assertNotIn("fw1-q01", json.loads(self.call("/api/bookmarks")[1]))

    def test_post_rejects_non_objects_and_unknown_paths(self):
        self.assertEqual(self.call("/api/notes", [1, 2])[0], 400)
        self.assertEqual(self.call("/api/other", {"item_id": "fw1-q01"})[0], 404)


if __name__ == "__main__":
    unittest.main()

import json
import os
import sys
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import ollama_handshake  # noqa: E402
from ollama_client import OllamaClient, OllamaError, model_matches  # noqa: E402

INSTALLED = ["llama3.2:latest"]  # codellama deliberately missing


class FakeOllama(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/api/tags":
            self._send(200, {"models": [{"name": n} for n in INSTALLED]})
        else:
            self._send(404, {"error": "nope"})

    def do_POST(self):
        req = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        if self.path == "/api/generate" and req["model"] in INSTALLED:
            self._send(200, {"response": "ready"})
        else:
            self._send(404, {"error": "model not found"})


class OllamaClientTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 0), FakeOllama)
        cls.url = "http://127.0.0.1:%d" % cls.server.server_port
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_model_matches(self):
        self.assertTrue(model_matches("llama3.2", "llama3.2:latest"))
        self.assertTrue(model_matches("llama3.2:latest", "llama3.2:latest"))
        self.assertFalse(model_matches("llama3.2:1b", "llama3.2:latest"))

    def test_list_and_generate(self):
        c = OllamaClient(self.url)
        self.assertEqual(c.list_models(), INSTALLED)
        self.assertEqual(c.generate("llama3.2:latest", "hi"), "ready")

    def test_unknown_model_raises(self):
        with self.assertRaises(OllamaError):
            OllamaClient(self.url).generate("codellama:latest", "hi")

    def test_unreachable_raises(self):
        with self.assertRaises(OllamaError):
            OllamaClient("http://127.0.0.1:1").list_models()

    def test_handshake_reports_missing_model(self):
        self.assertEqual(ollama_handshake.main(["--url", self.url]), 1)

    def test_handshake_passes_when_all_present(self):
        self.assertEqual(ollama_handshake.main(["--url", self.url, "--model", "llama3.2"]), 0)

    def test_handshake_fails_when_server_down(self):
        self.assertEqual(ollama_handshake.main(["--url", "http://127.0.0.1:1"]), 1)


if __name__ == "__main__":
    unittest.main()

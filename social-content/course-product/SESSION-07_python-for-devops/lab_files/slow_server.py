import http.server, time
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        time.sleep(8); self.send_response(200); self.end_headers(); self.wfile.write(b"late")
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", 8099), H).serve_forever()

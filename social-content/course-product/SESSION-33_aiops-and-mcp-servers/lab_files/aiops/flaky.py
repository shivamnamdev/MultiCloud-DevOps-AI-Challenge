import random, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
C = {"200": 0, "500": 0}; ERR = [0.02]
class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_GET(self):
        if self.path.startswith("/metrics"):
            b = "".join(f'http_requests_total{{status="{k}"}} {v}\n' for k, v in C.items()).encode()
        elif self.path.startswith("/err/"):
            ERR[0] = float(self.path.split("/")[-1]); b = b"ok"
        else:
            s = "500" if random.random() < ERR[0] else "200"; C[s] += 1; b = s.encode()
        self.send_response(200); self.send_header("content-type", "text/plain; version=0.0.4"); self.send_header("content-length", str(len(b))); self.end_headers(); self.wfile.write(b)
def traffic():
    import urllib.request
    while True:
        try: urllib.request.urlopen("http://127.0.0.1:8080/work").read()
        except Exception: pass
        time.sleep(0.05)
threading.Thread(target=traffic, daemon=True).start()
ThreadingHTTPServer(("0.0.0.0", 8080), H).serve_forever()

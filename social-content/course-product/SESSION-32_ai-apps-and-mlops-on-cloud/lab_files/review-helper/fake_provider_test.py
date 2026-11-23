import json, threading, time, os, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer as HTTPServer

PLAN = []          # list of (status, delay_seconds) used in order
HITS = []

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        n = int(self.headers.get("content-length", 0)); self.rfile.read(n)
        status, delay = PLAN.pop(0) if PLAN else (200, 0)
        HITS.append((round(time.time() - T0, 2), status, self.headers.get("x-api-key", "")[:6]))
        time.sleep(delay)
        body = json.dumps({"id": "msg_1", "type": "message", "role": "assistant", "model": "fake",
                           "content": [{"type": "text", "text": "- a\n- b\n- c"}], "stop_reason": "end_turn",
                           "stop_sequence": None, "usage": {"input_tokens": 10, "output_tokens": 5}}
                          if status == 200 else {"type": "error", "error": {"type": "api_error", "message": f"fake {status}"}}).encode()
        try:
            self.send_response(status); self.send_header("content-type", "application/json")
            self.send_header("content-length", str(len(body))); self.end_headers(); self.wfile.write(body)
        except BrokenPipeError:
            pass

srv = HTTPServer(("127.0.0.1", 8999), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
os.environ["ANTHROPIC_BASE_URL"] = "http://127.0.0.1:8999"; os.environ["ANTHROPIC_API_KEY"] = "sk-ant-FAKEKEY"
os.environ["MODEL_NAME"] = "claude-haiku-5-5"; os.environ["EXPERT_TIMEOUT"] = "1"
import anthropic; print("anthropic SDK", anthropic.__version__)
from real_expert import RealExpert

def case(name, plan, retries=2):
    global T0, HITS
    PLAN[:] = plan; HITS[:] = []; T0 = time.time(); os.environ["EXPERT_RETRIES"] = str(retries)
    try:
        out = RealExpert("claude-haiku-5-5").summarize("hi"); res = "OK " + repr(out[:9])
    except Exception as e:
        res = type(e).__name__
    print(f"{name:34} -> {res:28} attempts={len(HITS)} timeline={[(t, s) for t, s, _ in HITS]}")
case("200 first time", [(200, 0)])
case("429 then 200", [(429, 0), (200, 0)])
case("500, 500, 200 (2 retries)", [(500, 0), (500, 0), (200, 0)])
case("500 x3 (gives up after 3 tries)", [(500, 0)] * 3)
case("400 bad request", [(400, 0), (200, 0)])
case("401 bad key", [(401, 0), (200, 0)])
case("slow answer (3s, timeout 1s)", [(200, 3)] * 3)
case("retries=0 and a 429", [(429, 0), (200, 0)], retries=0)
case("slow answer then fast (retry helps)", [(200, 3), (200, 0)])
t=time.time(); case("always slow, retries=2", [(200, 3)] * 3); print("   wall time:", round(time.time()-t, 1), "s")
t=time.time(); case("always slow, retries=0", [(200, 3)], retries=0); print("   wall time:", round(time.time()-t, 1), "s")

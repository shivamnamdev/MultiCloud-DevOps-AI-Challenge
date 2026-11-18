import json, os, time, yaml, requests
from pathlib import Path

print("--- json")
data = {"booking": 101, "guest": "Asha", "rooms": [1, 2]}
Path("b.json").write_text(json.dumps(data, indent=2))
with open("b.json") as f:
    print(json.load(f)["guest"])
print(json.dumps(data, indent=2).splitlines()[0:3])

print("--- yaml")
text = "services:\n  - name: a\n    url: http://x\n"
print(yaml.safe_load(text))
try:
    print(yaml.load(text))
except TypeError as e:
    print("yaml.load without a Loader:", e)
evil = "!!python/object/apply:os.getcwd []"
try:
    print("safe_load of a python tag:", yaml.safe_load(evil))
except yaml.YAMLError as e:
    print("safe_load refused:", e.__class__.__name__)
print("yaml.load(FullLoader) of the same:", end=" ")
try:
    print(yaml.load(evil, Loader=yaml.FullLoader))
except Exception as e:
    print("refused:", e.__class__.__name__)
print("yaml.load(UnsafeLoader):", yaml.load(evil, Loader=yaml.UnsafeLoader))

print("--- environment secret")
try:
    os.environ["TOKEN"]
except KeyError as e:
    print("KeyError", e)
os.environ["TOKEN"] = "abc"; print("TOKEN found:", bool(os.environ["TOKEN"]))

print("--- pathlib")
Path("logs").mkdir(exist_ok=True)
Path("logs/a.log").write_text("INFO ok\nERROR boom\n")
Path("logs/b.log").write_text("INFO fine\n")
for p in sorted(Path("logs").glob("*.log")):
    errs = [l for l in p.read_text().splitlines() if "ERROR" in l]
    print(p.name, p.stat().st_size, "bytes", errs)
print(Path.home() / "atithi-booking")

print("--- with closes the file")
with open("r.txt", "w") as f:
    f.write("x")
print("closed after with:", f.closed)

print("--- requests timeout")
t = time.time()
try:
    requests.get("http://127.0.0.1:8099", timeout=2)
except requests.RequestException as e:
    print(e.__class__.__name__, f"after {time.time()-t:.1f}s")
r = requests.get("https://example.com/missing", timeout=5)
print("status", r.status_code)
try:
    r.raise_for_status()
except requests.HTTPError as e:
    print("raise_for_status:", str(e)[:60])

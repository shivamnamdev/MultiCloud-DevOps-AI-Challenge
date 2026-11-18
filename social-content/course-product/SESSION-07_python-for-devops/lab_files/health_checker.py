import time
import requests
import yaml

with open("services.yaml") as f:
    cfg = yaml.safe_load(f)

for s in cfg["services"]:
    start = time.time()
    try:
        r = requests.get(s["url"], timeout=5)
        r.raise_for_status()
        print(f'UP   {s["name"]} {time.time() - start:.2f}s')
    except requests.RequestException as e:
        print(f'DOWN {s["name"]} {e.__class__.__name__}')

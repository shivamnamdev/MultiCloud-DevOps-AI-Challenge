import argparse
import json
import logging
import shutil
import sys


def is_ok(pct, limit):
    return pct < limit


def main():
    p = argparse.ArgumentParser(description="Disk check for one building")
    p.add_argument("--path", default="/")
    p.add_argument("--threshold", type=int, default=90)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    total, used, _ = shutil.disk_usage(a.path)
    pct = round(used / total * 100, 1)
    ok = is_ok(pct, a.threshold)

    if a.json:
        print(json.dumps({"path": a.path, "used_percent": pct,
                          "threshold": a.threshold, "ok": ok}))
    log = logging.info if ok else logging.error
    log("disk %s used %.1f%% (limit %d%%)", a.path, pct, a.threshold)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

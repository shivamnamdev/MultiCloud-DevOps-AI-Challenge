"""Restart helper, hardened: absolute paths, every attempt logged, distinct exit codes.
exit 0 = restarted | 2 = dry run (nothing done) | 3 = refused | 4 = kubectl failed"""
import argparse, os, pathlib, subprocess, sys, time

HOME = pathlib.Path(os.environ.get("AIOPS_DIR", pathlib.Path(__file__).resolve().parent))   # same files from any folder
LOG, KILL = HOME / "aiops-actions.log", HOME / "KILL"
ALLOWED = {("atithi", "rooms-service"), ("atithi", "bookings-service")}
COOLDOWN = 1800


def log(ns, dep, outcome, who):
    with LOG.open("a") as f:
        f.write(f"{time.time()},{ns},{dep},{outcome},{who}\n")


def refuse(msg):
    print(msg, file=sys.stderr); sys.exit(3)


def recently_done(ns, dep):
    if not LOG.exists():
        return False
    for line in LOG.read_text().splitlines():
        parts = line.split(",")
        if len(parts) >= 4 and (parts[1], parts[2]) == (ns, dep) and parts[3] == "done" and time.time() - float(parts[0]) < COOLDOWN:
            return True
    return False


ap = argparse.ArgumentParser()
ap.add_argument("namespace"); ap.add_argument("deployment")
ap.add_argument("--approve", action="store_true")
ap.add_argument("--by", default=os.environ.get("USER", "unknown"), help="who approves (goes to the audit log)")
a = ap.parse_args()
ns, dep = a.namespace, a.deployment

if (ns, dep) not in ALLOWED:
    log(ns, dep, "refused-allowlist", a.by); refuse("not on the allow-list")
if KILL.exists():
    log(ns, dep, "refused-kill", a.by); refuse("kill switch is on")
if recently_done(ns, dep):
    log(ns, dep, "refused-recent", a.by); refuse("restarted recently, ask a human")
cmd = ["kubectl", "rollout", "restart", f"deployment/{dep}", "-n", ns]
print("PLAN:", " ".join(cmd), flush=True)
if not a.approve:
    log(ns, dep, "dry-run", a.by); print("dry run only, add --approve"); sys.exit(2)
try:
    subprocess.run(cmd, check=True, timeout=30)
except Exception as e:
    log(ns, dep, "failed", a.by); print("kubectl failed:", e); sys.exit(4)
log(ns, dep, "done", a.by)

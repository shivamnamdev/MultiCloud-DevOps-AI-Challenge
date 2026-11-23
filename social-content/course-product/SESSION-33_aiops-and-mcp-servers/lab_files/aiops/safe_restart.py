import argparse, subprocess, sys, time, pathlib
ALLOWED = {("atithi", "rooms-service"), ("atithi", "bookings-service")}
LOG = pathlib.Path("aiops-actions.log")

ap = argparse.ArgumentParser()
ap.add_argument("namespace"); ap.add_argument("deployment")
ap.add_argument("--approve", action="store_true")
a = ap.parse_args()

if (a.namespace, a.deployment) not in ALLOWED:
    sys.exit("not on the allow-list")
if pathlib.Path("KILL").exists():
    sys.exit("kill switch is on")
recent = [l for l in LOG.read_text().splitlines()] if LOG.exists() else []
now = time.time()
for l in recent:
    t, ns, dep, outcome = l.split(",")
    if (ns, dep) == (a.namespace, a.deployment) and outcome == "done" and now - float(t) < 1800:
        sys.exit("restarted recently, ask a human")
cmd = ["kubectl", "rollout", "restart", f"deployment/{a.deployment}", "-n", a.namespace]
print("PLAN:", " ".join(cmd))
if not a.approve:
    sys.exit("dry run only, add --approve")
subprocess.run(cmd, check=True, timeout=30)
LOG.open("a").write(f"{now},{a.namespace},{a.deployment},done\n")

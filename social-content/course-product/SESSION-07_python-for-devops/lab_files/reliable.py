import logging
import subprocess
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")


def retry(func, attempts=4, first_wait=1):
    wait = first_wait
    for n in range(1, attempts + 1):
        try:
            return func()
        except ConnectionError as e:
            if n == attempts:
                raise
            logging.warning("attempt %d failed (%s), waiting %ds", n, e, wait)
            time.sleep(wait)
            wait *= 2


calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("phone line dropped")
    return "answered"


t = time.time()
print(retry(flaky), f"after {time.time() - t:.1f}s and {calls['n']} calls")

calls["n"] = -100
t = time.time()
try:
    retry(flaky, attempts=3)
except ConnectionError as e:
    print("gave up and let the error out:", e, f"after {time.time() - t:.1f}s")

print("--- try / except / else / finally")
for value in ("5", "x"):
    try:
        n = int(value)
    except ValueError as e:
        print("except:", e)
    else:
        print("else: no error, n =", n)
    finally:
        print("finally: always runs")

print("--- a bare except hides a typo")
try:
    reslt = 1 / 1
    print(rezult)          # typo
except:
    print("bare except swallowed:", "NameError (we never find out)")

print("--- subprocess")
r = subprocess.run(["systemctl", "is-active", "nginx"], capture_output=True, text=True)
print("nginx:", r.returncode, repr(r.stdout.strip()))
r = subprocess.run(["systemctl", "is-active", "nosuchservice"], capture_output=True, text=True)
print("missing service:", r.returncode, repr(r.stdout.strip()))
try:
    subprocess.run(["systemctl", "is-active", "--quiet", "nosuchservice"], check=True)
except subprocess.CalledProcessError as e:
    print("CalledProcessError, returncode", e.returncode)

user_input = "hello; echo INJECTED"
print("shell=True with joined text:")
subprocess.run(f"echo {user_input}", shell=True)
print("list form, no shell:")
subprocess.run(["echo", user_input])

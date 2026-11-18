# Session 07 lab guide: Python for DevOps

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in dates, IDs, sizes and timings.

> **Important about Episode 3 (boto3):** we did **not** use a real AWS account. We ran the lab against `moto`, a free program that imitates the AWS EC2 API on your own machine. It is good for learning the code and for the shapes of the answers, but it is **not** AWS. Real permissions (`UnauthorizedOperation`), real timing of waiters, real regions and real IAM roles were **not** tested. Redo Episode 3's lab on a real account, read-only, after Sessions 8 and 9.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 40 min, Part C 40 min, Part D 45 min |
| **Cost** | Free. Parts A, B and D need only internet for `example.com`. Part C runs on your own machine against `moto`. |
| **Skill check before you start** | Session 6 (exit codes, `cron`, `set -euo pipefail`), and the basics from the "Think in Python" course. |

## Before you start

Use an Ubuntu 24.04 machine, or the practice container from Sessions 5 and 6 (its Dockerfile is in `lab_files/`):

```bash
docker build -t atithi-ubuntu:lab -f lab_files/Dockerfile.ubuntu lab_files
docker run -d --name atithi-web1 --hostname atithi-web1 --privileged --tmpfs /run --tmpfs /run/lock atithi-ubuntu:lab
docker cp lab_files atithi-web1:/home/ubuntu/s07
docker exec -u root atithi-web1 chown -R ubuntu:ubuntu /home/ubuntu/s07
docker exec -it -u ubuntu -w /home/ubuntu/s07 atithi-web1 bash
```

We tested with Python `3.12.3`, `requests 2.34.2`, `PyYAML 6.0.3`, `boto3 1.44.6`, `pytest 9.2.0` and `moto 5.2.5`. `lab_files/requirements.txt` lists the exact versions we installed.

---

## Part A: from the slip to the officer (Episode 1)

### A1. Why a virtual environment

On a fresh Ubuntu 24.04 (we used a plain container with only `python3` and `python3-pip`):

```bash
pip install requests
python3 -m venv /tmp/v
```

What we saw:

- `pip install requests` stopped with **`error: externally-managed-environment`** and "To install Python packages system-wide, try apt install python3-xyz". That is the "naye Ubuntu par pip mana kar dega" of the script.
- `python3 -m venv` without the `python3-venv` package said "The virtual environment was not created successfully because ensurepip is not available" and told us to run `apt install python3.12-venv`. (The script's `python3-venv` also works, because it is the general package name.)

Then, the right way:

```bash
sudo apt install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
which python
python3 -m pip install requests boto3 pyyaml pytest
pip freeze > requirements.txt
deactivate
which python3
```

Expected (ours): the prompt gains `(.venv)`, `which python` says `.../.venv/bin/python`, `pip freeze` gives about 17 lines, and after `deactivate` `which python3` says `/usr/bin/python3`. Add `.venv` to `.gitignore`.

### A2. The first officer's report

```bash
python sysinfo.py; echo "exit=$?"
sed 's/pct > 90/pct > 1/' sysinfo.py > sysinfo1.py
python sysinfo1.py; echo "exit=$?"
```

Expected (ours): `Building: atithi-web1  OS: Linux`, `Disk used: 5.9%`, `exit=0`; and the second run adds `FAIL: disk almost full` with **`exit=1`**. `raise SystemExit("...")` prints to the error stream and exits non-zero, which is what `cron` and pipelines read.

**Check yourself:**

- [ ] You saw both errors (system-wide `pip` and missing `venv`).
- [ ] `which python` points inside `.venv` while it is active.

---

## Part B: data, files and HTTP (Episode 2)

`lab_files/misc.py` runs all of this section's small checks in one go; read it and run `python misc.py`. To make the timeout test work, start the slow server first in the background: `python slow_server.py &` (and stop it afterwards with its PID, `kill %1`. **Do not** use `pkill -f slow_server.py` from the same shell line: the pattern also matches your own command and kills your shell. We did that by mistake.)

### B1. JSON and YAML

What we saw:

- `json.load` read `b.json`; `json.dumps(data, indent=2)` printed `{`, `"booking": 101,`, `"guest": "Asha",`...
- `yaml.safe_load("services:\n  - name: a\n    url: http://x\n")` gave `{'services': [{'name': 'a', 'url': 'http://x'}]}`.
- **`yaml.load(text)` without a Loader now fails**: `TypeError: load() missing 1 required positional argument: 'Loader'` (PyYAML 6). The script describes the old dangerous behaviour, and it is gone by default.
- But the danger exists if you ask for it. We fed this YAML: `!!python/object/apply:os.getcwd []`. `yaml.safe_load` refused it (`ConstructorError`), `yaml.load(..., Loader=yaml.FullLoader)` also refused, and `yaml.load(..., Loader=yaml.UnsafeLoader)` **ran the call and returned `/home/ubuntu/s07`**. Use `safe_load`, always.

### B2. `requests`

```python
requests.get("http://127.0.0.1:8099", timeout=2)   # the slow server waits 8 seconds
r = requests.get("https://example.com/missing", timeout=5); r.raise_for_status()
```

Expected (ours): `ReadTimeout after 2.0s` (we did not run it without a `timeout`, which would simply wait for the slow server's full 8 seconds, or for ever if a server never answers); `status 404`; and `raise_for_status: 404 Client Error: Not Found for url: https://example.com/mis...`.

Secrets from the environment: `os.environ["TOKEN"]` raised `KeyError 'TOKEN'` until we set it, so a missing secret stops the script early.

### B3. Files and `pathlib`

We made `logs/a.log` (`INFO ok` and `ERROR boom`) and `logs/b.log`, then looped `Path("logs").glob("*.log")`, read each file and kept the ERROR lines. We saw `a.log 19 bytes ['ERROR boom']` and `b.log 10 bytes []`. `Path.home() / "atithi-booking"` printed `/home/ubuntu/atithi-booking`, and a file opened with `with` showed `closed after with: True`.

### B4. The health checker lab

```bash
python health_checker.py
```

(`services.yaml` is the one in the script: `example.com`, `example.com/missing`, and a `.invalid` name.) Expected (ours):

```
UP   booking-home 0.06s
DOWN booking-api HTTPError
DOWN not-a-site ConnectionError
```

Exactly the three outcomes the script predicts. (It needs internet. Without it, the first line would also be DOWN.)

**Check yourself:**

- [ ] You saw `safe_load` refuse the Python tag and `UnsafeLoader` run it.
- [ ] You can say what happens to a request without `timeout`.
- [ ] The checker printed UP, then two kinds of DOWN.

---

## Part C: boto3 (Episode 3, against `moto`)

### C1. Start the emulator

`moto` goes in its **own** virtual environment, so it does not mix with your project's packages:

```bash
python3 -m venv ~/moto-venv
~/moto-venv/bin/python -m pip install "moto[server]"
~/moto-venv/bin/moto_server -H 127.0.0.1 -p 5555 &
```

(The `&` keeps it in the background. Stop it later with `kill %1`.) In the project venv, point boto3 at it with `AWS_ENDPOINT_URL`. The keys are fake: moto accepts anything.

```bash
source .venv/bin/activate
export AWS_ENDPOINT_URL=http://127.0.0.1:5555
```

### C2. The two errors a beginner meets

```bash
python aws-emulator/list_instances.py
export AWS_DEFAULT_REGION=us-east-1
python aws-emulator/list_instances.py
```

Expected (ours): first `botocore.exceptions.NoRegionError: You must specify a region.`, then, with a region but no credentials, `botocore.exceptions.NoCredentialsError: Unable to locate credentials`. Both match the script's advice (`aws configure`). Then set fake keys: `export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test`. A first run of the no-credentials case once took very long in our container, and we could not repeat it (the next runs failed instantly). We think boto3 was searching for an instance role, but we did not prove it.

The search order, tested:

```python
boto3.Session().get_credentials().method
```

With the two environment variables set, it said `env` (key `test`). After we unset them and wrote `~/.aws/credentials`, it said `shared-credentials-file` (key `FILEKEY`). So environment variables win over the file. (We did not test the third source, an instance role.)

### C3. The lab report

Seed three practice buildings (two tagged `Env=dev`, one `prod`; one has no `Owner` tag), then run the lab script:

```bash
python aws-emulator/list_instances.py       # empty account: prints nothing
python aws-emulator/seed.py
python aws-emulator/list_instances.py
```

Expected (ours): `seeded 3`, then three lines like `i-1d25...7c8 t3.small running web2   <- no Owner tag`, with the flag only on the one building that has no `Owner`. An empty account prints nothing, as the script says.

### C4. Filters, pages, `DryRun` and waiters

```bash
python aws-emulator/mutate.py
```

What we saw:

- A tag filter (`Env=dev`) returned `dev buildings: 2`.
- A paginator with `PageSize 1` returned `3` pages for three buildings (pagination works, even for a tiny account).
- `create_tags(..., DryRun=True)` raised `ClientError` with code **`DryRunOperation`**. So did `stop_instances(..., DryRun=True)`, and the building was still `running` afterwards.
- The real `stop_instances` followed by `get_waiter("instance_stopped").wait(...)` returned, and both buildings showed `stopped`. (On real AWS the waiter would take a while. On `moto` it was instant.)
- A real `create_tags` then changed the report.

The script's other `DryRun` outcome, **`UnauthorizedOperation`** ("you are not allowed"), could **not** be tested: `moto` does not enforce IAM. Try it on a real account with a read-only user.

Stop the emulator when finished (`kill %1`) and `unset AWS_ENDPOINT_URL`, or your next real-AWS script would silently talk to the emulator.

**Check yourself:**

- [ ] You hit `NoRegionError` and `NoCredentialsError` and can fix each.
- [ ] You saw a `DryRunOperation` error and know that it means "this would have worked".
- [ ] You know which parts of this section need a real account.

---

## Part D: reliable automation (Episode 4)

### D1. `try`, retry and a bare `except`

`lab_files/reliable.py` runs all of this. What we saw:

- A function that fails twice and then answers, wrapped in a retry with waits of 1 s then 2 s: warnings `attempt 1 failed (phone line dropped), waiting 1s`, `attempt 2 ... waiting 2s`, then `answered after 3.0s and 3 calls`.
- With only 3 attempts and a function that always fails: `gave up and let the error out: phone line dropped after 3.0s` (the last error is raised, not hidden).
- `try / except / else / finally`: for `"5"`, `else` and `finally` ran; for `"x"`, `except` printed `invalid literal for int() with base 10: 'x'` and `finally` still ran.
- A **bare `except:`** swallowed a `NameError` caused by a typo (`rezult`) and printed nothing useful. Catch only the error you have a plan for.

### D2. Logging and options

```bash
python check.py --path / --threshold 99; echo "exit=$?"
python check.py --threshold 1 --json; echo "exit=$?"
python check.py --threshold 1 --json 2>/dev/null | jq .
python check.py --help | head -4
```

Expected (ours): the first printed only a log line (`... INFO disk / used 5.9% (limit 99%)`) and `exit=0`; the second printed the log line (`ERROR`, to the error stream) **and** `{"path": "/", "used_percent": 5.9, "threshold": 1, "ok": false}`, with `exit=1`; the third showed only the JSON, formatted by `jq`, because `2>/dev/null` dropped the log. Logging goes to stderr and the real output to stdout, so they can be piped apart, as the script says.

### D3. `subprocess`

```python
subprocess.run(["systemctl", "is-active", "nginx"], capture_output=True, text=True)
```

We saw `returncode 0` and `'active'` for a running service. For `nosuchservice` it was `returncode 4` and `'inactive'`: systemd uses different non-zero codes (3 for stopped, 4 for unknown), so test `== 0`, not "any non-zero is the same". With `check=True` a failure raised `CalledProcessError` with `returncode 4`.

The injection example, with a harmless command:

```python
user_input = "hello; echo INJECTED"
subprocess.run(f"echo {user_input}", shell=True)    # prints hello  and  INJECTED
subprocess.run(["echo", user_input])                # prints hello; echo INJECTED  (one string)
```

With `shell=True` the second command **ran**. With the list form the whole text is just one argument.

### D4. A test for your tool: `pytest`

**The lab code in the first version of the script did not work with the test.** `check.py` had no `is_ok` function, and it ended with a bare `main()`. When we ran `pytest` with a test that did `from check import is_ok`, importing `check` ran the whole script, argparse read pytest's own arguments, and pytest crashed with `INTERNALERROR ... SystemExit: 2` and "no tests ran". The fixed `lab_files/check.py` has an `is_ok(pct, limit)` function and ends with `if __name__ == "__main__": main()`. Then:

```bash
pytest -q
python check.py --threshold 1 --json 2>/dev/null; echo "exit=$?"
```

Expected: `2 passed in 0.01s` (`test_pass` and `test_fail`), and the tool still prints its JSON and exits 1.

**Check yourself:**

- [ ] You can name what each of `try`, `except`, `else` and `finally` does.
- [ ] You saw JSON go through a pipe while the log went to the screen.
- [ ] You saw `shell=True` run an injected command.
- [ ] Your `pytest` shows two passes.

---

## Clean up

```bash
kill %1                       # the moto server, if still running
unset AWS_ENDPOINT_URL AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY AWS_DEFAULT_REGION
deactivate
docker rm -f atithi-web1
docker rmi atithi-ubuntu:lab
```

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `externally-managed-environment` | `pip` outside a venv | Make and activate a venv |
| `ensurepip is not available` | No `python3-venv` | `sudo apt install python3-venv` |
| `NoRegionError` | No default region | `export AWS_DEFAULT_REGION=...` or `aws configure` |
| `NoCredentialsError` | No keys found | Set env vars, or `~/.aws/credentials` |
| Script talks to the wrong place | `AWS_ENDPOINT_URL` left set | `unset AWS_ENDPOINT_URL` |
| `pytest` crashes with `SystemExit: 2` | Script runs on import | Add `if __name__ == "__main__":` |
| Your shell exits after `pkill -f` | The pattern matched your own command | Use `kill` with a PID |
| `requests` call hangs | No `timeout` | Always pass `timeout=` |

## What we did not test

- **A real AWS account:** real credentials and IAM roles, `UnauthorizedOperation`, real waiter delays, regions, and `aws configure`.
- **Sessions' assumptions about `Owner` tags** in a shared account.
- **YAML written by someone else** (anchors, multiple documents).
- **A rate-limited API** (HTTP 429) and real retry timing under load.
- **Running the tool from `cron`** (Session 6's guide covers `cron` itself).
- **A cloud-hosted Python** (Lambda, Session 15).

# Session 31 lab guide: the capstone CI/CD pipeline

Companion to `02_script.md`. The script tells the story; this guide is the hands-on sheet to keep next to your terminal and browser. Commands and outputs below come from a real end-to-end run (Jenkins 2.580 LTS, Docker 27.5, Trivy 0.76.2, Python 3.12 image, a private registry, and a separate "app building" reached over SSH). Your hashes, IDs and timings will differ.

| | |
|---|---|
| **Time** | Part A 30 min, Part B 40 min, Part C 60 min, Part D 60 min |
| **Cost** | **Docker practice: free** (it needs about 3 GB of free memory and a few GB of disk). For the real version: two small cloud buildings (Jenkins and the app), a GitHub account (free), and a package depot (GHCR is free for public images). Stop or delete the buildings when you finish. |
| **Skill check** | You finished Sessions 16B (pull requests), 17 to 19 (Jenkins, multibranch, credentials), 21 and 22 (Docker, Dockerfile) and 26 (health and metrics). |

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  atithi-rooms/   the service and conveyor: app.py, tests/, pytest.ini, Dockerfile, .dockerignore, .gitignore,
                  .github/CODEOWNERS, Jenkinsfile, Jenkinsfile.deploy, deploy/deploy.sh
  docker/         a practice stack: compose.yml, Dockerfile.jenkins, Dockerfile.app, app-start.sh, plugins.txt, jenkins.yaml
```

## Before you start

**Option 1: Docker (free, self-contained).** The practice stack has four containers, none of which touch your own Docker: **jenkins** (the foreman, with Docker CLI, Trivy and Python), **builder** (a separate Docker engine where images are built and scanned), **registry** (the depot, protected by a user and password, standing in for GHCR), and **app** (the app building: its own Docker engine and an SSH door).

```bash
cp -R lab_files/atithi-rooms ~/atithi-rooms
cd ~/atithi-rooms && git init -b main && git add . && git commit -m "atithi-rooms: first service"
cd /path/to/lab_files/docker
mkdir -p keys auth
ssh-keygen -t ed25519 -N "" -f keys/app_key                                   # the key Jenkins uses to reach the app building
docker run --rm --entrypoint htpasswd httpd:2 -Bbn atithi practice-pass > auth/htpasswd   # the depot's user and password
ATITHI_REPO=~/atithi-rooms docker compose up -d --build
```

The first build downloads several images and takes a few minutes. Open `http://localhost:8080` and log in as **admin** / **practice** (lab only). Port busy? Put `JENKINS_PORT=18080` in front. The app, when deployed, answers on `http://localhost:8081`.

Practice shortcuts (never on a real server): no setup wizard, a folder path works as a repository URL, the depot has no HTTPS, `docker` runs as root, and the SSH door accepts a known key and `accept-new` host keys.

Remove everything at the end: `docker compose down -v` from `lab_files/docker`, then delete the `keys/` and `auth/` folders (the first holds a private key).

**Option 2: the real thing**, as in the script: your Jenkins and an app building from Sessions 17 to 19, GitHub, and `ghcr.io`. Use the same files with `REGISTRY = 'ghcr.io/YOUR_ORG'` and `docker login ghcr.io`. We tested Option 1 only.

---

## Part A: the repo and its rules (Episode 1)

**Goal:** a repository where nothing reaches `main` without a pull request, a review and a green check.

This part is done in GitHub's web pages, so we could not run it here. The steps follow the script:

1. Create a GitHub repository `atithi-rooms` and push the starter files.
2. **Settings, Branches, Add rule** for `main`: require a pull request before merging, require **1 approval**, require status checks to pass (you add the Jenkins check in Part C), and do not allow force pushes. Do not let your own admin account bypass the rules, or write down why it must.
3. Look at `.gitignore` (it keeps `__pycache__/`, `.venv/` and `.env` out of Git) and `.github/CODEOWNERS` (replace `@YOUR_GITHUB_USER` with your own login: now changes to `Jenkinsfile` and `deploy/` need your review).
4. Test the rule: make a branch, add a line to `README.md`, push it, open a pull request. The **Merge** button must stay disabled until a review (and, later, the Jenkins check) is in.

Then try to push straight to `main`: Git must refuse.

### Check yourself

- [ ] A direct push to `main` was refused.
- [ ] A pull request could not be merged without a review.
- [ ] You can say who owns `Jenkinsfile` and `deploy/`.

---

## Part B: the service and its truck (Episode 2)

**Goal:** a small web service with tests, a safe Dockerfile, and a build you can reproduce on any machine. Do this part on your laptop first, as the script says ("local first, then the pipeline").

### B1. Look at the service

`app.py` has two routes: `/rooms` (a list of rooms) and `/health` (a light check that does **not** touch a database, so a database problem does not make the whole fleet look sick). `tests/test_app.py` calls both through Flask's test client. `requirements.txt` lists `flask`, `gunicorn`, `prometheus-client`, `pytest`.

### B2. Run the tests

```bash
cd ~/atithi-rooms
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -q
```

Expected: `2 passed`.

### Deliberate break: tests that cannot find the app

Our first attempt, without `pytest.ini`, failed:

```
    from app import app
E   ModuleNotFoundError: No module named 'app'
ERROR tests/test_app.py
```

pytest does not put the repository's top folder on the import path when the tests live in `tests/`. The starter files include the fix, a two-line `pytest.ini`:

```ini
[pytest]
pythonpath = .
```

### B3. Build and run the truck

```bash
docker build -t rooms-local:test .
docker run -d --name rooms-local -p 15000:5000 rooms-local:test
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:15000/rooms     # 200
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:15000/health    # 200
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:15000/nothing   # 404
curl -s http://localhost:15000/rooms
```

Expected: `200`, `200`, `404`, then `[{"free":4,"id":1,"type":"deluxe"},{"free":1,"id":2,"type":"suite"}]`. The third `curl` proves a wrong address gives a clean 404, not a crash.

### B4. Check the truck is safe

```bash
docker exec rooms-local sh -c 'id; ls -a /app'
```

Expected: `uid=10001(app)`: the service does **not** run as root; `/app` holds only `app.py`. Prove the `.dockerignore` works: create a file `.env` with `SECRET=should-not-be-in-image` in the repo, build again and run `ls -a /app`. The `.env` file must **not** be there (delete it afterwards, and never commit it). After 30 seconds:

```bash
docker inspect -f '{{.State.Health.Status}}' rooms-local      # healthy
```

### B5. Reproduce on a clean copy

`git clone` your repo into a new folder and run `docker build .` there. It must build with nothing from your laptop. If it does not, a file did not get committed: fix it now, it is cheap.

### Cleanup

```bash
docker rm -f rooms-local && docker image rm rooms-local:test
```

### Check yourself

- [ ] 2 tests passed after adding `pytest.ini`.
- [ ] `/rooms` and `/health` gave 200, and a wrong path gave 404.
- [ ] The container runs as `app`, has no `.env`, and reports `healthy`.
- [ ] A fresh clone builds the same truck.

---

## Part C: the conveyor with its gates (Episode 3)

**Goal:** every pull request is tested, built and scanned; only `main` pushes a truck to the depot, tagged with the commit id.

### C1. Read the Jenkinsfile

Four stations: **Test**, **Build image**, **Scan**, and **Push** (with `when { branch 'main' }`). The tag is the first 7 characters of the commit id. Credentials open only inside the Push station. For the practice depot the registry is `registry:5000/atithi`; for GHCR use `ghcr.io/YOUR_ORG` and `docker login ghcr.io`.

### C2. Credentials and the project

In Jenkins, **Credentials, Add**:

- kind **Username with password**, ID **`ghcr`**, username `atithi`, password `practice-pass` (a real GHCR token needs only the right to write packages),
- kind **SSH Username with private key**, ID **`app-server-key`**, username `ubuntu`, key: the contents of `keys/app_key` (used in Part D).

Then **New Item**, `rooms-multi`, **Multibranch Pipeline**, branch source **Git**, repository `/repos/atithi-rooms` (practice) or your GitHub URL (Option 2), script path `Jenkinsfile`. Make a second branch so you can compare:

```bash
cd ~/atithi-rooms
git checkout -b feature/first-service && echo "# practice" >> README.md && git add -A && git commit -m "feature: readme" && git checkout main
```

Scan the repository. Expected: two branch jobs, `main` and `feature/first-service`.

### C3. What the first run looks like

Expected on `main`: **Test, Build image, Scan, Push** all `SUCCESS` (our run took under a minute). On `feature/first-service`: Test, Build image and Scan succeed and the log says `Stage "Push" skipped due to when conditional`. A pull request must never push a truck.

Check the depot:

```bash
docker compose exec jenkins sh -c 'curl -s -u atithi:practice-pass http://registry:5000/v2/atithi/rooms-service/tags/list'
```

Expected: `{"name":"atithi/rooms-service","tags":["4e0e175"]}`: one tag, equal to the first 7 characters of `main`'s commit id (`git rev-parse --short=7 main`).

### Deliberate break 0: two branches scan at once, the first time

In our first run both branches built together and the feature branch's **Scan** crashed with a Go runtime error (`fatal error: fault`, `signal SIGBUS`). Trivy downloads its vulnerability database on first use, and two scans were sharing that one cache while it was being written. It is not a security finding. **Build the failed branch again** and it passes. To avoid it, let one build finish first, or run `trivy image --download-db-only` once on the build machine.

### Drill 1: break a test

On the feature branch, change `assert len(r.get_json()) >= 1` to `>= 5` in `tests/test_app.py`, commit, and scan the repository again. Expected in the log:

```
>       assert len(r.get_json()) >= 5
E       AssertionError: assert 2 >= 5
FAILED tests/test_app.py::test_rooms_returns_list - AssertionError: assert 2 >= 5
1 failed, 1 passed
```

`Test` is red and no later station runs: no truck is built. Revert the commit (`git revert --no-edit HEAD`).

### Drill 2: an old base image

Change the last stage of the `Dockerfile` to `FROM python:3.12.0-slim-bookworm` and delete the `apt-get update && apt-get upgrade -y ...` line. Commit and rebuild. Expected: **Test and Build image pass, Scan fails.** Trivy reports `debian 12.2` with about **90** fixable HIGH or CRITICAL findings, and the build stops there. Nothing after Scan runs, so this truck never reaches the depot. Find where the reason is written: the **Report Summary** table in the Scan log. Restore the original `Dockerfile`.

Why the real Dockerfile passes: `python:3.12-slim` is current, and its `apt-get upgrade -y` line picks up fixes that have already been released. `--ignore-unfixed` skips only findings for which no fix exists yet (our first scan of an unpatched `python:3.12-slim` found 48, of which one was fixable). Add a short, dated ignore list only with a written reason.

### Drill 3: the wrong depot password

Edit the `ghcr` credential and set a wrong password. Commit a small change on `main` (for example a line in `README.md`), scan the repository. Expected: Test, Build image and Scan succeed and **Push fails**:

```
Error response from daemon: login attempt to http://registry:5000/v2/ failed with status: 401 Unauthorized
```

Fix the credential and **Build Now**: Push succeeds and the depot lists a second tag, the new commit id. Note a small oddity in the log: Jenkins masks the username too, so `registry:5000/atithi/rooms-service` appears as `registry:5000/****/rooms-service`. Anything that equals a credential value is hidden, including common words used as usernames.

### The bell and the required check (GitHub; tested on a temporary public repository, 2026-11-24)

Add the webhook (`/github-webhook/`, Session 18), and then in branch protection mark the Jenkins check as **required**. A pull request now needs the review and a green conveyor. Keep the fork trust setting at the strict choice (Session 19).

### Check yourself

- [ ] `main` pushed one truck tagged with the commit id; the feature branch pushed none.
- [ ] You triggered each drill and found the reason in the right log place.
- [ ] You can say why a "Synced"-looking Push of a bad image is not yet a release (Part D shows it).

---

## Part D: deliver, check, roll back (Episode 4)

**Goal:** the new truck reaches the app building, is checked, and rolls back by itself if it is sick.

### D1. The deploy script and the Deploy station

`deploy/deploy.sh` (run on the app building): remember the current truck's image, pull the new one, replace the container, then check `/health` up to 20 times, 3 seconds apart. If it never answers, it logs `FAILED`, removes the new truck, restarts the previous one, and exits with an error so the Jenkins station turns red. `Jenkinsfile.deploy` is the same conveyor plus a **Deploy** station, `when { branch 'main' }`, that sends the script over SSH:

```groovy
sshagent(['app-server-key']) {
  sh 'ssh -o StrictHostKeyChecking=accept-new ubuntu@app "bash -s" -- "$IMAGE:$TAG" < deploy/deploy.sh'
}
```

`accept-new` trusts the building's host key the first time: a build cannot answer a "continue connecting?" question. Copy it over `Jenkinsfile`, add the `deploy/` folder, commit on `main`, and scan the repository.

### Deliberate break: the app building cannot pull

Expected on the first deploy: everything up to Push is green and **Deploy fails**:

```
Error response from daemon: Head "http://registry:5000/v2/atithi/rooms-service/manifests/<tag>": no basic auth credentials
ERROR: script returned exit code 1
```

Jenkins pushed with a password; the app building has none. Log in **once** on the app building (a real building pulling from GHCR needs the same, unless the package is public):

```bash
docker compose exec jenkins ssh -i /keys/app_key ubuntu@app \
  'echo practice-pass | docker login registry:5000 -u atithi --password-stdin'
```

Expected: `Login Succeeded`. **Build Now** again.

### D2. The first deploy

Expected: all five stations green. On the app building:

```bash
docker compose exec jenkins ssh -i /keys/app_key ubuntu@app 'cat /var/log/atithi-deploys.log'
```

```
2026-11-18T07:47:23+00:00 deployed registry:5000/atithi/rooms-service:5d1341b (was none)
```

From your laptop: `curl http://localhost:8081/rooms` returns the two rooms, and `/health` returns `200`.

### D3. An upgrade

Add a third room to `ROOMS` in `app.py`:

```python
{"id": 3, "type": "family", "free": 2}
```

Commit it on `main` (in real life: a pull request, a review, a merge) and scan the repository. Expected: five green stations, a new log line `deployed ...:eb987f3 (was ...:5d1341b)`, and `curl http://localhost:8081/rooms` now lists the `family` room. The old tag stays in the depot.

### D4. A release that looks fine and is not

Make a release that every earlier gate accepts. In `app.py` add, near the top:

```python
import json
EXTRA = json.load(open("rooms.json"))      # read at start-up
```

and create `rooms.json` containing `{"extra": []}`. Commit both on `main`. This is the classic "works on my machine": the file is in the repository, so the **tests pass**; but the Dockerfile copies only `app.py`, so it is not in the **image**. Scan the repository.

Expected:

```
Test SUCCESS, Build image SUCCESS, Scan SUCCESS, Push SUCCESS, Deploy FAILED
```

Every earlier gate was green; only the real health check in the app building caught it. Look at the deploy log on the app building:

```
... deployed registry:5000/atithi/rooms-service:eb987f3 (was ...)
... FAILED registry:5000/atithi/rooms-service:d368f0c, rolling back to registry:5000/atithi/rooms-service:eb987f3
```

and the site never went down:

```bash
curl -s http://localhost:8081/rooms        # still lists the family room
```

(Right after a rollback, `docker ps` can show `(health: starting)` for a few seconds on the old truck: give it a moment, as the script says.) Three things to notice:

1. The bad image is **already in the depot** (Push happened before Deploy). A pushed image is not a released image.
2. The site stayed up, because the script restored the previous truck.
3. The Jenkins log says the deploy failed, but **not why**, because the script removes the failed container. Add one line before `docker rm -f "$NAME"` in the failure path of `deploy/deploy.sh`:

```bash
docker logs --tail 20 "$NAME" || true
```

Commit it and build again. The Deploy station log now ends with the cause:

```
    EXTRA = json.load(open("rooms.json"))
FileNotFoundError: [Errno 2] No such file or directory: 'rooms.json'
```

(The build still fails, correctly: the bad release is still on `main`. Notice the log also shows a second `FAILED` line for the new commit, with the same rollback.)

### D5. Fix with `git revert`

```bash
git revert --no-edit <the bad commit id>
```

Commit stays in history, as Session 16B taught. Scan the repository. Expected: all five green and a log line `deployed ...:<new id> (was ...:eb987f3)`, with the family room still served. The rollback layers are: the script (seconds), re-deploying an older tag by hand (minutes), and `git revert` so the history is honest. A database change cannot be undone by swapping trucks, so keep database changes small and backward compatible.

### Staging and approval (described, not run)

The script describes staging first, a smoke test, an `input` approval with a timeout (with `agent none` so no machine is held, Session 18), then production. In our lab there is one app building, so we did not run it. It is the same script with a different address.

### Cleanup and review (do not skip)

- **Docker:** `docker compose down -v` from `lab_files/docker`, `docker image rm docker-jenkins docker-app`, and delete `keys/` and `auth/`.
- **Real setup:** stop or terminate the two buildings; revoke the depot token; delete the `ghcr` and `app-server-key` credentials in Jenkins and the key from the app building's `authorized_keys`; delete test images from the depot; check for leftover volumes, public IPs and security group rules; keep a budget alert.
- **Blameless review:** write four lines: what happened (a release passed every gate but crashed in the image), what the checks caught (the health check and the rollback), what they missed (a file not copied into the image), and one change for next time (a Test or Build step that runs the container and checks `/health` before Push).

### Check yourself

- [ ] The first deploy log said `(was none)`; the upgrade said `(was <old tag>)`.
- [ ] The broken release failed at Deploy, the old truck came back, and `/rooms` kept answering.
- [ ] You read the cause (`FileNotFoundError`) in the Jenkins log after adding the `docker logs` line.
- [ ] A `git revert` brought a green, deployed fix.
- [ ] Everything is cleaned up.

---

## Final checklist for Session 31

- [ ] Part A: protected `main`, `CODEOWNERS`, a pull request that cannot merge without review
- [ ] Part B: tests pass (with `pytest.ini`), a non-root, healthy truck, a clean clone builds
- [ ] Part C: a multibranch conveyor; `main` pushed a tagged truck, a branch did not; three drills read in the logs
- [ ] Part D: first deploy, an upgrade, a broken release rolled back automatically, a `git revert` fix
- [ ] Practice stack, keys and password file removed (or the buildings stopped and tokens revoked)

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `ModuleNotFoundError: No module named 'app'` | No `pytest.ini` | Add `[pytest]` and `pythonpath = .` |
| Scan crashes with `fatal error: fault` / `SIGBUS` on the first run | Two scans writing Trivy's database cache | Build again; or download the database once first |
| Scan fails with many findings | Old or unpatched base image | Use a current base image and keep `apt-get upgrade -y`; read the Report Summary |
| Push fails with `401 Unauthorized` | Wrong or expired depot credential | Fix the `ghcr` credential |
| Deploy fails with `no basic auth credentials` | The app building is not logged in to the depot | `docker login` once on the app building |
| Deploy fails with `Host key verification failed` | First SSH connection, strict checking | Use `-o StrictHostKeyChecking=accept-new` or add the key to `known_hosts` |
| Deploy fails at health check, cause unknown | The script removed the failed container | Add `docker logs --tail 20 "$NAME" \|\| true` before the removal |
| The site is down after a deploy | No previous truck to roll back to (first deploy) | Fix and redeploy; keep the previous tag available |
| Jenkins hides part of a log line as `****` | The text equals a credential value | Expected; use a unique username |

## Real GitHub results (temporary public repository, deleted afterwards)

- **The bell:** `/github-webhook/` works once the GitHub plugin is installed; a push started the build in about 11 seconds (details in the Session 18 guide, "Real webhook results").
- **CODEOWNERS + branch protection** (`require_code_owner_reviews: true`, 1 approving review, required status check `jenkins/hook-build`, `strict: true`, `enforce_admins: false`): a pull request showed `mergeStateStatus BLOCKED`, `reviewDecision REVIEW_REQUIRED`.
  - **Approving your own pull request is refused:** `Review Can not approve your own pull request`. A one-person team therefore cannot get past a required review; use a second account, or the admin override.
  - `gh pr merge` without override: `the base branch policy prohibits the merge`.
  - A passing status named exactly like the required check (we posted it through the API as stand-in for Jenkins) turned the check green, but the PR stayed `BLOCKED` until the review rule was met. Both rules apply at once.
  - **Admin override:** `gh pr merge --admin` merged it (the owner is allowed because `enforce_admins` was `false`). With the same setting, an owner can even **push straight to `main`**; GitHub only prints `Required status check ... is expected` and lets it through. Turn on **Do not allow bypassing** (`enforce_admins: true`) for a real protection.
- The check name must match **exactly** what Jenkins reports (`jenkins/hook-build` here). A wrong name leaves the PR waiting forever.
- **Not run:** Jenkins posting the real status back, fork pull requests and fork trust, a Jenkins push to GHCR (a manual `docker push` and a GitHub Actions publish to GHCR were tested on 25 November 2026, see Session 22; the Jenkins credential path was not).

## What we did not test

Part B and the whole conveyor ran in the Docker practice stack (Jenkins 2.580.2 LTS, a private registry with a password instead of GHCR, a Docker-in-Docker build machine and app building). The jobs and credentials were created through the Jenkins command line with the settings the browser forms would save; we did not click through the web pages. We did not run: GitHub's fork trust and Jenkins posting the real status (branch protection, `CODEOWNERS`, reviews, the bell and a required check were tested on a temporary repo), GHCR and its tokens, real cloud buildings and security groups, the staging, smoke test and approval stages, Prometheus and Grafana on the deployed app, rolling or blue-green deploys, or HTTPS. The practice app building runs its Docker engine inside a container, which is not how a real server works.

# Session 22 lab guide: Dockerfile and registries

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in IDs, sizes, versions and times.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 25 min, Part C 40 min, Part D 30 min (plus the GitHub part, if you do it) |
| **Cost** | Parts A to D run on your laptop and cost nothing. The GitHub Actions part uses GitHub's free allowance for a small repository. Do not push anything with a secret in it to any registry. |
| **Skill check before you start** | You did Session 21 (`docker run`, images, layers, volumes) and can read a Python file. |

## Before you start

You need Docker (Engine or Desktop) with BuildKit, which is the default builder in current Docker. Check:

```bash
docker version --format 'client {{.Client.Version}} server {{.Server.Version}} {{.Server.Os}}/{{.Server.Arch}}'
docker buildx version
```

On our test machine (Docker Desktop on an M-series Mac): client and server `29.8.2`, `linux/arm64`, buildx `v0.37.2`. For the optional scan in Part C you need nothing extra: we run Trivy as a container.

All the files are in `lab_files/rooms-service/`. Copy that folder somewhere and work inside it:

```bash
cp -R lab_files/rooms-service ~/rooms-lab && cd ~/rooms-lab
ls -a
```

You should see `app.py`, `requirements.txt`, `.dockerignore`, `.github/workflows/image.yml`, and eight Dockerfiles named after what they teach (`Dockerfile.v1`, `Dockerfile.gunicorn`, `Dockerfile.badorder`, `Dockerfile.slim`, `Dockerfile.full`, `Dockerfile.ep`, `Dockerfile.leak`, `Dockerfile.secret`). Use `docker build -f <file>` to pick one.

> **Mac users, read this first.** On a Mac, **port 5000 is taken by AirPlay Receiver** (a macOS service). We ran into it: `docker run -p 5000:5000` failed with `address already in use`, and `curl localhost:5000` answered `403 Forbidden` from `AirTunes`. Everywhere this guide says `5000` on the left side of `-p`, use `5050:5000` instead, and call `localhost:5050`. (Or turn off AirPlay Receiver in System Settings. Pick one, do not do both.)
>
> The tests below used `5050`.

---

## Part A: the first fit-out sheet (Episode 1)

**Goal:** build the rooms-service as a truck, see why the dev server is not for production, and see why the listening address matters.

### A1. The first Dockerfile (dev server)

`Dockerfile.v1` is exactly Scene 3 of the script, with `CMD ["python", "app.py"]`.

```bash
docker build -f Dockerfile.v1 -t rooms:1.0 .
docker run -d -p 5050:5000 --name rooms rooms:1.0
curl -s localhost:5050/
curl -s localhost:5050/health
docker logs rooms
```

Expected: `Atithi rooms-service`, then `ok`, then the log, which includes the line `WARNING: This is a development server. Do not use it in a production deployment.` and `Running on all addresses (0.0.0.0)`. That is Flask telling you in plain words that this is a designer's test server. (In our test, `pip` installed Flask 3.1.3 and gunicorn 27.0.1.)

`docker rm -f rooms` before moving on.

### A2. `CMD` against `ENTRYPOINT`

```bash
docker run --rm rooms:1.0 python -c 'print("CMD replaced by args")'
echo 'print("other.py ran")' > other.py
docker build -f Dockerfile.ep -t rooms:ep .
docker run --rm rooms:ep other.py
docker run --rm rooms:ep -V
```

Expected: `CMD replaced by args` (anything after the image name replaced the whole `CMD`). Then `other.py ran`, then `Python 3.12.16` (ours). In `Dockerfile.ep`, `ENTRYPOINT ["python"]` stays and what you type becomes its arguments. Create `other.py` before you build, because `COPY . .` copies it into the image.

Clean up: `rm other.py`.

### A3. A real server and a health check

`Dockerfile.gunicorn` swaps in gunicorn and adds `HEALTHCHECK`:

```bash
docker build -f Dockerfile.gunicorn -t rooms:g .
docker run -d -p 5050:5000 --name rooms --health-interval 3s rooms:g
sleep 6
curl -s localhost:5050/health
docker ps --format '{{.Names}} {{.Status}}'
docker logs rooms | head -4
```

Expected: `ok`, then `rooms Up 6 seconds (healthy)`, then gunicorn's start lines (`Starting gunicorn 27.0.1`, `Listening at: http://0.0.0.0:5000`, `Using worker: sync`, `Booting worker with pid: 7`). We shortened the check interval with `--health-interval 3s` so you do not wait 30 seconds. The `HEALTHCHECK` in the file says `30s`.

### A4. Make the health check fail

The check only sees what it asks about. Run the same image with a check that points at a route that does not exist:

```bash
docker rm -f rooms
docker run -d -p 5050:5000 --name rooms \
  --health-interval 2s --health-timeout 2s --health-retries 2 \
  --health-cmd "python -c \"import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/nope')\" || exit 1" rooms:g
sleep 9
docker ps --format '{{.Names}} {{.Status}}'
docker inspect rooms --format '{{.State.Health.Status}} streak={{.State.Health.FailingStreak}}'
curl -s -o /dev/null -w 'app still answers: %{http_code}\n' localhost:5050/
```

Expected (ours): `health: starting` at first, then `rooms Up 6 seconds (unhealthy)`, then `unhealthy streak=4`, and `app still answers: 200`. `unhealthy` is a verdict about the **check**, not about the app. In our run nothing restarted the container, it just kept the `unhealthy` label. (We did not test what happens with a restart policy or in an orchestrator.)

> **A trap we tried and do not recommend:** `docker pause rooms` does not make a clean "unhealthy" demo. The status line says `(Paused)` and `.State.Health.FailingStreak` stayed `0`. Use the wrong-route trick above.

### A5. The wrong listening address

```bash
docker rm -f rooms
sed 's/0.0.0.0:5000/127.0.0.1:5000/' Dockerfile.gunicorn > Dockerfile.loop
docker build -f Dockerfile.loop -t rooms:loop .
docker run -d -p 5050:5000 --name rooms --health-interval 2s rooms:loop
sleep 5
curl -s -m 3 localhost:5050/health; echo "curl exit=$?"
docker ps --format '{{.Names}} {{.Status}}'
docker exec rooms python -c "import urllib.request;print(urllib.request.urlopen('http://127.0.0.1:5000/health').read())"
docker logs rooms | grep Listening
```

Expected (ours): `curl exit=56` (the connection is reset), **but** `rooms Up 5 seconds (healthy)`, and from inside the truck `b'ok'`, and the log says `Listening at: http://127.0.0.1:5000`. The app is fine from the inside, and unreachable from the outside, and the health check is blind to it, because the check also runs inside. A green health status does **not** prove the serving window works.

Clean up: `docker rm -f rooms`.

### A6. Why the exec form matters

```bash
sed 's|^CMD .*|CMD gunicorn -b 0.0.0.0:5000 -w 2 app:app|' Dockerfile.gunicorn > Dockerfile.shell
docker build -f Dockerfile.shell -t rooms:shell .
docker run -d --name sh1 rooms:shell
docker run -d --name ex1 rooms:g
sleep 3
docker top sh1 -o pid,args
for n in sh1 ex1; do /usr/bin/time -p docker stop $n 2>&1 | grep real; docker inspect $n --format "$n exit={{.State.ExitCode}}"; done
docker rm -f sh1 ex1
```

Expected (ours):

```
PID                 COMMAND
70051               /bin/sh -c gunicorn -b 0.0.0.0:5000 -w 2 app:app
70064               /usr/local/bin/python3.12 /usr/local/bin/gunicorn -b 0.0.0.0:5000 -w 2 app:app
real 3.16
sh1 exit=137
real 0.31
ex1 exit=0
```

In shell form, `sh` is PID 1 and gunicorn is its child. `docker stop` sends the signal to `sh`, which does not pass it on, so Docker waits out the grace period and then kills it (exit 137). In exec form, gunicorn is PID 1, gets the signal, finishes cleanly in a third of a second, and exits 0. (On `/usr/bin/time` and the 3 second wait: see the note in the Session 21 guide about how long `docker stop` waits on your machine.)

**Check yourself:**

- [ ] You can show the dev-server warning in the log.
- [ ] You made a container show `unhealthy` while the app still answered.
- [ ] You can explain why a healthy container may still be unreachable from outside.

---

## Part B: build speed, `.dockerignore` and secrets (Episode 2)

**Goal:** measure the cache for yourself, see how much a `.dockerignore` saves, and see a secret leak and not leak.

### B1. Cache order, measured

`Dockerfile.gunicorn` copies `requirements.txt` first and installs, then copies the code. `Dockerfile.badorder` copies everything first.

```bash
/usr/bin/time -p docker build --no-cache --progress=plain -f Dockerfile.gunicorn -t rooms:cache . 2>&1 | grep -E '^real|CACHED'
echo '# change 1' >> app.py
/usr/bin/time -p docker build --progress=plain -f Dockerfile.gunicorn -t rooms:cache . 2>&1 | grep -E '^real|CACHED'
/usr/bin/time -p docker build --no-cache --progress=plain -f Dockerfile.badorder -t rooms:bad . 2>&1 | grep -E '^real'
echo '# change 2' >> app.py
/usr/bin/time -p docker build --progress=plain -f Dockerfile.badorder -t rooms:bad . 2>&1 | grep -E '^real|pip install'
```

What we saw with only `flask` and `gunicorn` (a tiny app):

| Build | Time |
|---|---|
| good order, cold (`--no-cache`) | 3.0 s |
| good order, after a one-line change (install layer `CACHED`) | 0.6 s |
| bad order, cold | 2.4 s |
| bad order, after a one-line change (`pip install` runs again) | 2.2 s |

The gap is real, but small, because Flask installs fast. Make it visible: put `numpy` and `pandas` into `requirements.txt` and repeat (both orders, cold, then change one line):

| Build (with `numpy` and `pandas`) | Time |
|---|---|
| good order, cold | 13.7 s |
| good order, after a one-line change | **0.7 s** (the install step says `CACHED`) |
| bad order, after a one-line change | **12.4 s** |

Image size was the same either way (about 427 MB with those packages). Put `requirements.txt` back to two lines afterwards. A project with heavy dependencies and thirty pushes a day is where this adds up. The script's "three minutes per build" is that heavier case. Ours were seconds.

### B2. Build context and `.dockerignore`

Make a heavy folder and a fake secret file, then build twice:

```bash
mkdir -p data .git && head -c 150000000 /dev/zero > data/big.bin && echo "SECRET=abc" > .env
mv .dockerignore .dockerignore.off
docker build --progress=plain -f Dockerfile.gunicorn -t rooms:ctx . 2>&1 | grep 'transferring context'
docker run --rm rooms:ctx ls -a /app
mv .dockerignore.off .dockerignore
docker build --progress=plain -f Dockerfile.gunicorn -t rooms:ctx . 2>&1 | grep 'transferring context'
docker run --rm rooms:ctx ls -a /app
```

What we saw:

- Without `.dockerignore`: `transferring context: 150.04MB 0.8s done`, and `ls -a /app` lists `.env`, `.git` and `data`. **The fake secret is inside the image.**
- With `.dockerignore`: `transferring context: 474B 0.0s done`, and none of those three are in `/app`.

Clean up: `rm -rf data .git .env; docker rmi rooms:ctx`.

### B3. A secret in a layer, and a secret that stays out

```bash
docker build --build-arg TOKEN=hunter2-VALUE -f Dockerfile.leak -t rooms:leak .
docker history --no-trunc rooms:leak --format '{{.CreatedBy}}' | grep -i hunter2
```

Expected: two lines. `RUN |1 TOKEN=hunter2-VALUE /bin/sh -c echo "using token $TOKEN" > /dev/null` and `ARG TOKEN=hunter2-VALUE`. Anyone who can pull the image can read the token.

Now the safe way:

```bash
echo "TOKEN-VALUE-12345" > pip.conf
docker build --progress=plain --secret id=pipcred,src=pip.conf -f Dockerfile.secret -t rooms:secret . 2>&1 | grep 'secret was readable'
docker history --no-trunc rooms:secret --format '{{.CreatedBy}}' | grep -c 'TOKEN-VALUE'
docker run --rm rooms:secret ls /run/secrets
```

Expected: `secret was readable in this step, bytes: 18` (the step could read it), then `0` (not in the history), then `ls: cannot access '/run/secrets': No such file or directory` (not in the final image). We also searched the image's real folders (`/usr /etc /app /root /var /opt /home`) for the value and found nothing.

Two notes:

- Without the `--secret` flag, a **cold** build fails: `RUN test -s /run/secrets/pipcred ... did not complete successfully: exit code: 1`. But if the layer is already **cached** from the earlier run, BuildKit reuses it and the build "passes" without reading the secret. If you test this, add `--no-cache`.
- An unbounded search such as `grep -r TOKEN-VALUE /` inside a container wanders into `/proc` and takes minutes. Search real folders only.

Clean up: `docker rmi rooms:leak rooms:secret; rm pip.conf`.

**Check yourself:**

- [ ] You have a build time for good order and bad order on your own machine.
- [ ] You saw the fake `.env` inside an image, then not inside it.
- [ ] You can say which of the two build commands above leaks the token, and how you proved it.

---

## Part C: small and safe (Episode 3)

**Goal:** compare image sizes and scan results, run as a non-root user, harden the run, and see the architecture trap.

### C1. Three designs, three sizes

`Dockerfile.full` is the same service on the full `python:3.12` base. `Dockerfile.gunicorn` is on `slim`. `Dockerfile.slim` is the multi-stage, non-root one from the script.

```bash
docker build -f Dockerfile.full -t rooms:full .
docker build -f Dockerfile.gunicorn -t rooms:single .
docker build -f Dockerfile.slim -t rooms:slim .
docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}' | grep -E '^rooms:(full|single|slim)'
```

What we saw:

| Image | Size |
|---|---|
| `rooms:full` (full Python base) | 1.63 GB |
| `rooms:single` (slim base, one stage) | 227 MB |
| `rooms:slim` (slim base, multi-stage, non-root) | 228 MB |

The big saving is the **base image**: 1.63 GB down to 227 MB. The multi-stage build did **not** make this service smaller (228 against 227 MB), exactly as the script says for a pure-Python service with no compiler. Where it pays is Go, Java, or Python with C extensions that need `gcc`.

One more thing in the multi-stage file: the line `rm -rf /wheels` does not shrink the image. The wheels were already added by the earlier `COPY --from=build` layer (about 926 kB in `docker history rooms:slim`), and a later `rm` only hides them. For a big dependency set, install straight from the build stage with a bind mount instead of copying.

### C2. Non-root, and what the user can write

```bash
docker run --rm rooms:slim id
docker run --rm rooms:slim touch /etc/x
docker run --rm rooms:slim touch /app/x
docker run --rm -u 0 rooms:slim sh -c 'ls /wheels 2>&1 | head -1'
```

Expected: `uid=10001(app) gid=10001(app) groups=10001(app)`, then `touch: cannot touch '/etc/x': Permission denied`, then `touch: cannot touch '/app/x': Permission denied`, then `ls: cannot access '/wheels'`.

`/app` is not writable even by `app`: Docker created the folder (`WORKDIR`) as root before the files were copied in as `app`. The files are owned by `app`, the folder is not. That is a good default for this service. If your app needs to write there, make that a deliberate choice.

### C3. Scan both designs with Trivy

We ran Trivy as a container, on image files saved to disk, so we did not give it access to the Docker socket:

```bash
mkdir -p tar && docker save rooms:slim -o tar/slim.tar && docker save rooms:full -o tar/full.tar
docker run --rm -v trivycache:/root/.cache -v "$PWD/tar":/t aquasec/trivy:0.76.2 \
  image --quiet --input /t/slim.tar --severity HIGH,CRITICAL
```

The first run downloads Trivy's vulnerability database and takes longer. We counted the findings (`--format json`) for both:

| Image | HIGH | CRITICAL | Total | Of those, a fix is available |
|---|---|---|---|---|
| `rooms:full` | 487 | 15 | **502** | 108 |
| `rooms:slim` | 48 | 0 | **48** | 1 |

(Debian 13.7 base, Trivy 0.76.2. Your numbers change every day as the database changes.) The point is the order of magnitude: about **ten times fewer** findings from the base change alone. Only 1 of the 48 on `slim` had a fix available, which is the kind of finding a gate with `--ignore-unfixed` would let through (as in Session 20).

Clean up: `docker volume rm trivycache; rm -r tar`.

### C4. Hardened run flags

```bash
docker run -d --name hard -p 5050:5000 --read-only --tmpfs /tmp --cap-drop ALL \
  --security-opt no-new-privileges --memory 256m --pids-limit 100 rooms:slim
sleep 3
docker ps --format '{{.Names}} {{.Status}}'
curl -s -m 3 localhost:5050/health; echo
docker logs hard | head -8
docker inspect hard --format 'readonly={{.HostConfig.ReadonlyRootfs}} capdrop={{.HostConfig.CapDrop}} secopt={{.HostConfig.SecurityOpt}} pids={{.HostConfig.PidsLimit}}'
docker exec hard sh -c 'touch /app/x; touch /tmp/ok && echo "/tmp writable"; touch /usr/x'
docker exec hard sh -c 'grep -E "^Cap(Eff|Bnd)" /proc/self/status'
```

What we saw:

- The service answered `ok`, but the log had this line, exactly as the script warned: `[ERROR] Control server error: [Errno 30] Read-only file system: '/home/app/.gunicorn'`. Gunicorn 27.0.1 tries to create a control socket in its home folder.
- `readonly=true capdrop=[ALL] secopt=[no-new-privileges] pids=100`.
- `touch /app/x` and `touch /usr/x` fail with `Read-only file system`, and `/tmp writable` works.
- `CapEff` and `CapBnd` were all zeros: no special Linux powers left.

Two fixes, both tested by us (0 errors in the log afterwards, `ok` from `/health`):

```bash
# A: give it a writable place for the control socket
docker run -d --name h2 -p 5050:5000 --read-only --tmpfs /tmp \
  --tmpfs /home/app/.gunicorn:uid=10001,gid=10001 --cap-drop ALL --security-opt no-new-privileges rooms:slim

# B: point the control socket at /tmp
docker run -d --name h3 -p 5050:5000 --read-only --tmpfs /tmp --cap-drop ALL rooms:slim \
  gunicorn -b 0.0.0.0:5000 -w 2 --control-socket /tmp/gunicorn.ctl app:app
```

(`docker rm -f hard h2 h3` between runs, since they use the same host port.) `gunicorn --help` also lists a `--no-control-socket` switch, which the script mentions as another way. We saw it in the help but did **not** run it.

### C5. The architecture trap (our machine could not do this part)

```bash
docker image inspect rooms:slim --format '{{.Os}}/{{.Architecture}}'
docker build --platform linux/amd64 -f Dockerfile.slim -t rooms:amd .
```

Expected on an M-series Mac with working emulation: `linux/arm64`, and then the amd64 build finishes (slowly). **What happened to us:** the first command said `linux/arm64`, and the amd64 build **failed** at its first `RUN` step with `exec /bin/sh: exec format error`. Running `docker run --platform linux/amd64 alpine uname -m` failed the same way. That is the very error the script warns about, hit from the other direction: this Docker Desktop had no working amd64 emulation. `docker buildx ls` still listed `linux/amd64` as a supported platform, so listing is not proof.

To fix it on your Mac you need to enable emulation (Docker Desktop settings) or build on an amd64 machine or CI runner. We did not change our machine's emulation setup, so:

> **Not tested by us:** a working `--platform linux/amd64` build on an arm64 laptop, and a multi-platform build with `docker buildx build --platform linux/amd64,linux/arm64`. We saw the failure, not the success.

**Check yourself:**

- [ ] You can show the 1.6 GB against 227 MB difference and the roughly tenfold scan difference.
- [ ] You can say, for this service, why multi-stage did not shrink the image.
- [ ] You can name what each of `--read-only`, `--cap-drop ALL`, `no-new-privileges` and `--pids-limit` does.

---

## Part D: labels, a depot and the conveyor (Episode 4)

**Goal:** push a design to a registry with two labels, see that a tag can move and a digest cannot, produce a parts list, and read the CI workflow.

### D1. A depot on your laptop

We used the plain `registry:2` image, bound to the loopback only. It has no login, so it is for practice only.

```bash
docker run -d --name depot -p 127.0.0.1:5055:5000 registry:2
docker tag rooms:slim localhost:5055/atithi/rooms-service:1.4.2
docker tag rooms:slim localhost:5055/atithi/rooms-service:1.4.2-a1b2c3d
docker push localhost:5055/atithi/rooms-service:1.4.2
docker push localhost:5055/atithi/rooms-service:1.4.2-a1b2c3d
curl -s localhost:5055/v2/_catalog
curl -s localhost:5055/v2/atithi/rooms-service/tags/list
```

What we saw: the first push listed `Pushed` for each layer and ended with `1.4.2: digest: sha256:76319cc1...b65 size: 856`. The second push said `Layer already exists` and printed **the same digest**. The catalog was `{"repositories":["atithi/rooms-service"]}` and the tags were `{"name":"atithi/rooms-service","tags":["1.4.2-a1b2c3d","1.4.2"]}`. Two labels, one design.

(The `1.4.2-a1b2c3d` shape here is a label we typed by hand. The workflow in D4 produces `sha-a1b2c3d`, see below.)

### D2. Pull by digest, and watch a tag move

```bash
OLD=sha256:<the digest your first push printed>
docker rmi localhost:5055/atithi/rooms-service:1.4.2 localhost:5055/atithi/rooms-service:1.4.2-a1b2c3d
docker pull localhost:5055/atithi/rooms-service@$OLD
docker run --rm localhost:5055/atithi/rooms-service@$OLD id
```

Expected: `Status: Downloaded newer image ...@sha256:...` and `uid=10001(app) ...`. Now break the rule on purpose: change the greeting in `app.py`, rebuild as the **same tag**, push again:

```bash
sed -i.bak 's/Atithi rooms-service/Atithi rooms-service v2/' app.py
docker build -f Dockerfile.slim -t localhost:5055/atithi/rooms-service:1.4.2 .
docker push localhost:5055/atithi/rooms-service:1.4.2
docker run -d --rm -p 5051:5000 --name old localhost:5055/atithi/rooms-service@$OLD
docker run -d --rm -p 5052:5000 --name new localhost:5055/atithi/rooms-service:1.4.2
sleep 2
echo "by old digest: $(curl -s localhost:5051/)"; echo "by tag 1.4.2:  $(curl -s localhost:5052/)"
docker rm -f old new; mv app.py.bak app.py
```

Expected (ours): the push printed a **different** digest (`sha256:5d4d46fa...`), then `by old digest: Atithi rooms-service` and `by tag 1.4.2:  Atithi rooms-service v2`. The tag `1.4.2` quietly pointed to new content, and the old digest still gave the old design. A registry like this one lets you overwrite a tag. That is why you deploy by digest or immutable tag, and why real registries offer "tag immutability".

### D3. A parts list (SBOM) with Trivy

```bash
docker save rooms:slim -o slim.tar
docker run --rm -v trivycache:/root/.cache -v "$PWD":/t aquasec/trivy:0.76.2 \
  image --quiet --format cyclonedx --input /t/slim.tar --output /t/slim.cdx.json
```

What we saw: a CycloneDX 1.7 file with **97 components**, of which **9 Python packages**: Flask 3.1.3, Jinja2 3.1.6, MarkupSafe 3.0.4, Werkzeug 3.1.9, blinker 1.9.0, click 8.5.1, gunicorn 27.0.1, itsdangerous 2.2.0, pip 25.0.1. Next time a library is in the news, you search these files and know which images contain it.

> **Not tested by us:** image **signing** (for example with `cosign`) and a deploy gate that checks the signature. The script presents these as a habit to grow into, not a lab, and we did not run them either.

### D4. The workflow: read it, check it, then run it on GitHub

`.github/workflows/image.yml` is the script's workflow, with one change we made after checking the tag rules (next paragraph). Read it first. We linted it with `actionlint` (clean, no errors), and we confirmed with GitHub that the action versions it uses exist: `actions/checkout@v7`, `docker/metadata-action@v6`, `docker/login-action@v4` and `docker/build-push-action@v7` all resolve to real releases.

**The change:** the script's first version used `docker/metadata-action` with only `images:`. According to that action's own documentation, with no `tags:` input it creates `main` for a push to `main`, **`v1.0.0` (not `1.0.0`)** for a tag push, **and `latest`**. That would contradict the script's own rule "never deploy `latest`". So the workflow now says:

```yaml
        with:
          images: "ghcr.io/${{ github.repository }}"
          tags: |
            type=semver,pattern={{version}}
            type=sha
            type=ref,event=branch
          flavor: latest=false
```

By the same documentation, a push of the Git tag `v1.0.0` should give the image tags `1.0.0` and `sha-` plus the first seven characters of the commit, and a push to `main` gives `main` and `sha-...`.

> **Tested on real GitHub (25 November 2026, a temporary private repository, deleted afterwards).** We ran this exact workflow. Results:
> - **First run failed, and it was our fault:** `failed to read dockerfile: open Dockerfile: no such file or directory`. The folder has only `Dockerfile.slim`, `Dockerfile.v1` and so on, and `build-push-action` looks for a file called `Dockerfile`. We added `file: Dockerfile.slim` to the build step in `lab_files/rooms-service/.github/workflows/image.yml`. Everything before the build (checkout, metadata, the login to `ghcr.io` with `GITHUB_TOKEN`) had worked.
> - **Push to `main`** gave the image tags `main` and `sha-0c3a5b8`. **Pushing the Git tag `v1.0.0`** gave `1.0.0` (no `v`) and `sha-0c3a5b8`. This matches the description above.
> - **The package linked itself to the repository** and was **private** (the repository was private; the package inherits that at first). No token was created by hand.
> - **Without `packages: write`** the login still succeeds, but the push fails: `failed to push ghcr.io/...: unexpected status from HEAD request ... 403 Forbidden`. If you see a 403 on a GHCR push from a workflow, check `permissions:` first.
> - **Deleting the repository does not delete its package.** The package stayed, with no repository attached. Delete packages yourself (the package's settings page, or the API with `delete:packages`).
> - Not tested: making the package public, pulling it from a server with a read-only token, and the signing step.

### D5. ECR: immutable tags, lifecycle rule, scan on push (tested on real AWS, 2026-11-24)

Run with the CLI login (not a role). The repository was created, used and deleted the same day; cost: cents.

```bash
aws ecr create-repository --repository-name atithi-rooms --image-tag-mutability IMMUTABLE \
  --image-scanning-configuration scanOnPush=true --tags Key=Project,Value=atithi-lab
aws ecr put-lifecycle-policy --repository-name atithi-rooms --lifecycle-policy-text file://lifecycle.json
aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com
docker buildx build --provenance=false --sbom=false -t ACCOUNT.dkr.ecr.REGION.amazonaws.com/atithi-rooms:1.0.0 --push .
```

- **Immutability works.** Pushing **different content** under the same tag was refused: `error from registry: The image tag '1.0.0' already exists in the 'atithi-rooms' repository and cannot be overwritten because the tag is immutable.` A new tag (`1.0.1`) went in. This is the safe answer to the "same tag, new content" problem of Part D4.
- **Lifecycle rule accepted** (rule 1: `untagged`, `sinceImagePushed`, 7 days, expire; rule 2: `tagged`, `tagPrefixList`, `imageCountMoreThan` 20, expire). `start-lifecycle-policy-preview` finished `COMPLETE` with `expiringImageTotalCount: 0` (nothing was old enough). The policy takes effect over days; we did not wait.
- **Trap: scan on push did nothing with Docker's default build.** Docker 29 (BuildKit) pushes an **OCI index** that carries provenance attestations. `describe-image-scan-findings` said `ScanNotFoundException`, and `start-image-scan` said `UnsupportedImageTypeException: ... application/vnd.oci.image.index.v1+json cannot be scanned`. Each push also left **two untagged child manifests** in the repository (`imageTags: None`), which is what the "untagged older than 7 days" rule exists to clean up. **Fix:** build with `--provenance=false --sbom=false` so the tag points to a plain image manifest. Then the scan ran by itself: `COMPLETE`, **12 HIGH, 15 MEDIUM, 3 LOW** for our `python` based image.
- Login: `Login Succeeded`; the token lasts 12 hours. Log out and delete the repository when you are done: `aws ecr delete-repository --repository-name atithi-rooms --force`.
- Still **not run:** login with an IAM role (instead of the user), image signing, and a deploy gate. **GHCR was run for real on 25 November 2026** (a tiny `atithi-ghcr-test:1.0` image pushed from a laptop; the workflow route is in D4): the `gh` login needed `gh auth refresh -s write:packages` (approved in the browser with a one-time code); `gh auth token | docker login ghcr.io -u USER --password-stdin` worked and the push succeeded. A new package is **private by default** (an anonymous pull gives `401`/`403`, a logged-in pull works). Unlike ECR with immutable tags, **GHCR lets you push the same tag again**: the old image stays as an untagged version. Deleting a package by API needs `delete:packages` and `read:packages` as well (we had only `write:packages`, so the package was deleted in the web page instead). Run `docker logout ghcr.io` when done. Not tested: making a package public.

## Clean up

```bash
docker rm -f rooms hard h2 h3 sh1 ex1 old new depot 2>/dev/null
docker rmi rooms:1.0 rooms:g rooms:cache rooms:bad rooms:loop rooms:shell rooms:ep rooms:full rooms:single rooms:slim 2>/dev/null
docker rmi localhost:5055/atithi/rooms-service:1.4.2 2>/dev/null
docker volume rm trivycache 2>/dev/null
docker system df
```

If you wrote real secrets into any test image, delete the image, and if you pushed it anywhere other than the practice depot, treat the secret as leaked and replace it. Delete lab repositories and packages from ECR or GHCR the same day.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `address already in use` on port 5000, or `403` from `AirTunes` | macOS AirPlay Receiver | Use `-p 5050:5000`, or turn AirPlay Receiver off |
| `curl: (56)` or empty reply, but the container is `healthy` | App listens on `127.0.0.1` | Bind to `0.0.0.0` (A5) |
| `ModuleNotFoundError` or `flask: command not found` when you run | Dependencies not installed in the image, or built from the wrong Dockerfile | Check `-f` and `docker history` |
| Build passes on one machine, `exec format error` on another | CPU architecture mismatch, or no emulation | C5 |
| `Read-only file system` error in gunicorn's log | Control socket path not writable | C4, fix A or B |
| `docker build` is slow at "transferring context" | No `.dockerignore`, big folders | B2 |
| `--secret` build says "did not complete successfully" | The secret file path is wrong, or it is empty | Check `src=` and run with `--no-cache` |
| `docker push` to `localhost:5055` is refused | The depot is not running, or the port is in use | `docker ps`, change the port |
| `unauthorized` pushing to GHCR from your laptop | You need a token with package rights | Use the workflow, or `docker login ghcr.io` with a token |

## What we did not test

- **The GitHub workflow run itself**, and the `docker/metadata-action` tag output. Syntax and action versions were checked; tag behaviour is from the action's documentation.
- **A working `--platform linux/amd64` build** and multi-platform `buildx` (our Docker Desktop had no amd64 emulation).
- **ECR** (login with a role, immutability, lifecycle policy), **GHCR** with a real token, registry scan on push, image **signing** and a deploy gate.
- **`--no-control-socket`** for gunicorn (listed in its help, not run).
- **Build-time `pip` against a real private index** with a secret mount (we tested the mount mechanism with a stand-in file).
- **Real three-minute builds.** Ours took seconds; the heavy-dependency case took 12 to 14 seconds.
- **Java or Go multi-stage builds** from the script's narration.

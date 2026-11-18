# Session 21 lab guide: Docker fundamentals

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real, and the outputs shown are what we saw. Yours will differ in IDs, sizes, IPs and times.

| | |
|---|---|
| **Time** | Part A 15 min, Part B 15 min, Part C 40 min, Part D 40 min |
| **Cost** | Free. Everything runs on your own laptop or on a building you already have. If you use a cloud building, stop it when you finish. |
| **Skill check before you start** | You can use a terminal, and you know what a process and a signal are (Session 5). |

## Before you start

You need Docker Engine (Linux) or Docker Desktop (Mac, Windows), and a terminal. Check:

```bash
docker version
```

Expected: a `Client` block and a `Server` block. On our test machine (Docker Desktop on an M-series Mac) both said version `29.8.2` and the server said `linux/arm64`. If you only see the Client block and an error about the daemon, Docker is not running yet.

Files for this guide are in `lab_files/` next to it: `compose.yaml` (Part D), `src/index.html` (Part D), `prod.env.example` (Part C).

Two things to know about where this was tested:

- **We tested on Docker Desktop (a Mac), not on a fresh Ubuntu building.** The commands are the same on Ubuntu with Docker Engine, but a few defaults differ, and we point out where. The Ubuntu install steps from the script (Scene 5 of Episode 1) were **not** run by us.
- **Names used below are plain on purpose** (`web`, `db`, `bad`, `lim`, `appnet`, `pgdata`). If you already have containers, volumes or networks with these names, stop and rename before you copy and paste.

> **Tip:** port `8080` must be free on your machine. Check with `lsof -iTCP:8080 -sTCP:LISTEN` (Mac, Linux). Empty output means free.

---

## Part A: what a truck really is (Episode 1)

**Goal:** see with your own eyes that a container is a process with a limited view and a limited budget.

### A1. First truck

```bash
docker run --rm hello-world
```

Expected, near the top: `Hello from Docker!` and a numbered list of what Docker did (the client contacted the daemon, the daemon pulled the image, created a container, streamed the output). The first time, you also see a `Pulling from library/hello-world` line. That list is the whole client, daemon and depot story in six lines.

Look at the engine's own summary:

```bash
docker info --format 'driver={{.Driver}} log={{.LoggingDriver}} containers={{.Containers}} images={{.Images}}'
```

Ours: `driver=overlayfs log=local containers=11 images=36`. Your numbers will differ. Note the `log=` value, we come back to it in Part C.

### A2. The truck is a process

```bash
docker run -d --name ps1 --memory 64m --cpus 0.5 alpine sleep 300
docker top ps1 -o pid,ppid,args
docker exec ps1 ps
```

Expected: `docker top` lists one process, `sleep 300`, with a large host PID (ours: `68740`). Inside, `ps` shows the same process as **PID 1** and the `ps` command itself as PID 7. That is a namespace at work: the truck can only see its own processes.

Now the cgroup limits, read from inside the truck:

```bash
docker exec ps1 sh -c 'cat /sys/fs/cgroup/memory.max; cat /sys/fs/cgroup/cpu.max'
```

Expected: `67108864` (that is 64 MiB in bytes) and `50000 100000` (half a CPU: 50,000 microseconds of every 100,000). These are the numbers you gave with `--memory 64m --cpus 0.5`.

And the shared kernel:

```bash
docker exec ps1 uname -r
docker run --rm alpine uname -r
```

Expected: the same kernel version twice (ours: `7.0.14-linuxkit`). Two different trucks, one kernel. On Docker Desktop that kernel belongs to a small hidden Linux VM, so it will not match your Mac's own `uname -r`. On Ubuntu it matches the building's kernel.

Clean up: `docker rm -f ps1`.

> **Not tested here:** on a Linux building you can also find the process in the host's own `ps aux | grep "sleep 300"`. We ran on a Mac, where the host is not Linux, so we did not see that line ourselves.

**Check yourself:** you can say why `docker top` shows a different PID from `docker exec ps1 ps`.

---

## Part B: designs, layers, tags and digests (Episode 2)

**Goal:** read an image's size, layers and identity, and see why `latest` is a moving label.

```bash
docker pull nginx:alpine
docker pull nginx:latest
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep '^nginx'
```

Expected (ours): `nginx:alpine  94.1MB` and `nginx:latest  261MB`. Same web server, almost three times the size, because the base is bigger. Sizes differ between setups and versions. The ratio is what matters.

```bash
docker history nginx:alpine --format '{{.Size}}\t{{.CreatedBy}}' | head -6
docker image inspect nginx:alpine --format '{{.Id}} {{.Size}}'
```

Expected: the history lists layers newest first, with one big layer (ours: `51.5MB` from a long `RUN ... apkArch` install step) and many `0B` lines for `ENV`, `CMD` and similar. Zero-size lines are settings, not files. The inspect line prints the design's long `sha256:...` ID and its size in bytes (ours: `93194623`).

Now the digest, the part that does not move:

```bash
docker inspect nginx:alpine --format '{{index .RepoDigests 0}}'
D=$(docker inspect nginx:alpine --format '{{index .RepoDigests 0}}')
docker run --rm --entrypoint nginx $D -v
```

Expected: a `nginx@sha256:...` line, then `nginx version: nginx/1.31.9` (ours). Running by digest asks for that exact design, whatever the `alpine` tag points to next month.

See how much space Docker is using:

```bash
docker system df
```

Expected: four rows (Images, Containers, Local Volumes, Build Cache) with a RECLAIMABLE column. This is the number to watch on a long-lived building.

> **Careful with prune.** `docker image prune` deletes dangling (untagged, unused) images. On a machine where you keep other work, run `docker images -f dangling=true` first and look at what it would remove. During our test we ran `docker image prune -f` without looking first, and it removed about 46 MB of dangling images that were already on the machine. They were untagged leftovers, not tagged images, but check first anyway.

**Check yourself:**

- [ ] You can explain why `latest` is not a safe thing to deploy.
- [ ] You can find a layer's size and the command that made it.
- [ ] You can run a design by digest.

---

## Part C: running, breaking and reading trucks (Episode 3)

**Goal:** use the main `docker run` flags, watch the writable layer disappear, read exit codes, and see the port and log traps for yourself.

### C1. A web server in one command

```bash
docker run -d --name web -p 8080:80 nginx:alpine
curl -s localhost:8080 | head -4
```

Expected: the start of the nginx welcome page (`<!DOCTYPE html>`, `<title>Welcome to nginx!</title>`).

Now change the page from inside, then replace the truck:

```bash
docker exec web sh -c 'echo changed > /usr/share/nginx/html/index.html'
curl -s localhost:8080
docker rm -f web
docker run -d --name web -p 8080:80 nginx:alpine
curl -s localhost:8080 | head -3
```

Expected: `changed`, then after the new truck, the welcome page is back. The edit lived only in the old truck's thin writable layer. Fix changes in the design or the parameters, never inside a running truck.

`docker rm -f web` to clean up.

### C2. The full set of flags

```bash
docker run -d --name web -p 8080:80 -e GREETING=hi \
  --memory 256m --cpus 0.5 --restart unless-stopped \
  --log-opt max-size=10m --log-opt max-file=3 nginx:alpine

docker inspect web --format 'mem={{.HostConfig.Memory}} nano={{.HostConfig.NanoCpus}} restart={{.HostConfig.RestartPolicy.Name}} logcfg={{.HostConfig.LogConfig.Config}}'
docker exec web sh -c 'echo GREETING=$GREETING'
docker stats --no-stream --format '{{.Name}} cpu={{.CPUPerc}} mem={{.MemUsage}}' web
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'
```

Expected (ours): `mem=268435456 nano=500000000 restart=unless-stopped logcfg=map[max-file:3 max-size:10m]`, then `GREETING=hi`, then a stats line like `web cpu=0.00% mem=11.38MiB / 256MiB`, then a table where the web port shows as `0.0.0.0:8080->80/tcp, [::]:8080->80/tcp`.

Every flag you typed shows up in `inspect`. When you are unsure what a truck was started with, ask it.

### C3. Why `--log-opt` matters

The script says logs are not rotated by default. That is true for the **Linux Engine default**, which is the `json-file` driver. It was **not** true on our Docker Desktop: `log=local` (Part A) is a different driver that rotates by itself. To see the real problem on any machine, ask for `json-file` explicitly:

```bash
docker run -d --name spam1 --log-driver json-file alpine sh -c 'i=0; while [ $i -lt 40000 ]; do echo "line $i padding padding padding padding padding"; i=$((i+1)); done'
docker run -d --name spam2 --log-driver json-file --log-opt max-size=200k --log-opt max-file=3 alpine sh -c 'i=0; while [ $i -lt 40000 ]; do echo "line $i padding padding padding padding padding"; i=$((i+1)); done'
sleep 6
```

On a Linux building you can then look at the files:

```bash
sudo ls -l /var/lib/docker/containers/$(docker inspect spam1 --format '{{.Id}}')/
```

What we saw (we read the files through a read-only mount on Docker Desktop):

- `spam1`: one file, `...-json.log`, **4,828,890 bytes** and still growing with every line.
- `spam2`: three files, `...-json.log` (28,435 bytes), `.log.1` and `.log.2` (200,013 bytes each). Old lines were dropped to stay inside the cap.

That is 4.8 MB from forty thousand short lines. A busy service writes that in an afternoon. Clean up with `docker rm -f spam1 spam2`.

### C4. The port and firewall trap

```bash
docker run -d --name pub -p 8080:80 nginx:alpine
docker run -d --name loop -p 127.0.0.1:8081:80 nginx:alpine
```

Find your machine's address on the network (Mac: `ipconfig getifaddr en0`; Linux: `hostname -I`). Call it `LAN`. Then:

```bash
for p in 8080 8081; do
  echo "localhost:$p -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 3 localhost:$p)"
  echo "$LAN:$p -> $(curl -s -o /dev/null -w '%{http_code}' --max-time 3 $LAN:$p)"
done
```

Expected (ours):

```
localhost:8080 -> 200
192.168.0.104:8080 -> 200
localhost:8081 -> 200
192.168.0.104:8081 -> 000
```

`-p 8080:80` answers on every address of the machine. `-p 127.0.0.1:8081:80` answers only on the machine itself (`000` means no connection at all). Clean up: `docker rm -f pub loop`.

> **Not tested:** the script's main point, that Docker's own firewall rules run *before* `ufw` on Linux, needs an Ubuntu building with `ufw` enabled. We ran on a Mac with no `ufw`, so we saw the two binding behaviours above but **not** the `ufw` bypass. Test that one yourself on your Ubuntu building: run `sudo ufw deny 8080`, publish a truck with `-p 8080:80`, and call it from another machine.

### C5. Exit codes

```bash
docker run --name bad alpine sh -c 'echo oops; exit 1'
docker ps -a --filter name=bad --format '{{.Names}} {{.Status}}'
docker logs bad
docker inspect bad --format 'exit={{.State.ExitCode}} oom={{.State.OOMKilled}}'
```

Expected: `oops`, then `bad Exited (1) Less than a second ago`, then `oops` again from the logs, then `exit=1 oom=false`.

Now the memory kill:

```bash
docker run --name lim --memory 32m alpine sh -c 'tail /dev/zero'
echo "client exit: $?"
docker inspect lim --format 'exit={{.State.ExitCode}} oom={{.State.OOMKilled}}'
```

Expected: `client exit: 137`, then `exit=137 oom=true`. `tail /dev/zero` reads forever without a newline, so it grows without limit until the 32 MB cap kills it. Exit 137 alone could be several things. `OOMKilled=true` is what says "memory".

### C6. What `docker stop` really does (our own finding)

The script says `docker stop` sends SIGTERM and waits, then sends SIGKILL, and that exit 143 means "stopped by SIGTERM". When we tested it, the picture was more interesting:

```bash
docker run -d --name s1 alpine sleep 1000
time docker stop s1
docker inspect s1 --format 'exit={{.State.ExitCode}}'

docker run -d --init --name s2 alpine sleep 1000
time docker stop s2
docker inspect s2 --format 'exit={{.State.ExitCode}}'

docker run -d --name s3 alpine sleep 1000
time docker stop -t 2 s3
docker inspect s3 --format 'exit={{.State.ExitCode}}'
```

What we saw:

| Truck | `docker stop` took | Exit code | Why |
|---|---|---|---|
| `s1`: `sleep` as PID 1 | about 3 s | **137** | PID 1 has no signal handler, so SIGTERM is ignored. Docker waited, then sent SIGKILL. |
| `s2`: same, with `--init` | 0.08 s | **143** | A tiny init process forwards SIGTERM, `sleep` dies of it, 143. |
| `s3`: `-t 2` | about 2.1 s | **137** | Same as `s1`, with our own 2 second wait. |
| `web` (nginx, from C2) | under 0.2 s | **0** | The nginx image sets its own stop signal, `SIGQUIT`, and it shuts down cleanly. |

Two honest notes:

- **The wait was about 3 seconds for us, not 10.** Docker's documentation says the default is 10 seconds. When we asked for `-t 10` explicitly, it took 10 seconds. We could not find out why the plain `docker stop` waited less on this machine, because looking inside the Docker Desktop VM was not something we could do. So **measure yours** with `time docker stop`, and if the exact wait matters to your service, set it: `docker stop -t 30`, or `--stop-timeout 30` when you run the truck.
- **A shell-form `CMD`** makes `sh` PID 1 and your app its child, and the same thing happens: SIGTERM never reaches the app. We test this properly in the Session 22 guide.

Clean up: `docker rm -f bad lim s1 s2 s3 web`.

### C7. Settings from outside

```bash
cp lab_files/prod.env.example prod.env
docker run --rm --env-file prod.env alpine sh -c 'echo $ENV $GREETING'
```

Expected: `prod hello`. One design, many settings. Add `prod.env` to `.gitignore`. It stays on the building and out of the vault.

### C8. Gordon, Docker's AI assistant

**Not tested by us.** `docker ai` is installed on our machine (`docker ai --help` works), but using it needs a signed-in Docker account, and a question to it goes to Docker's service under your account. We did not want to do that on your behalf. If you try it: break a truck as in C5, ask "why did this die?", and compare its answer with the exit code and `OOMKilled` value you read yourself. Read what it proposes before you approve, every time.

**Check yourself:**

- [ ] You can name the cause of an exit 1, 137 and 143 truck from `docker inspect` and `docker logs`.
- [ ] You can say what `-p 127.0.0.1:8081:80` does differently from `-p 8081:80`.
- [ ] You know your own `docker stop` wait, measured, not assumed.

---

## Part D: locker rooms, roads and compose (Episode 4)

**Goal:** keep data across trucks, make trucks talk by name, back a volume up, and run the whole thing from one file.

### D1. The database truck, as in the script

```bash
docker network create appnet
docker run -d --name db --network appnet \
  -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
until docker exec db pg_isready -h 127.0.0.1 -U postgres; do sleep 1; done
docker run --rm -e PGPASSWORD=secret --network appnet postgres:16 \
  psql -h db -U postgres -c 'create table if not exists t(x int); insert into t values (1); select * from t;'
```

Expected (ours): a few `... - no response` lines, then `... - accepting connections`, then:

```
CREATE TABLE
INSERT 0 1
 x
---
 1
(1 row)
```

**The `-h 127.0.0.1` matters (a bug we found in the first version of the script).** On a brand-new volume, Postgres starts a small temporary server first, only on a local socket, to set itself up. Without `-h`, `pg_isready` asks that socket and answers "accepting connections" while the real server is still not listening on the network. We tried it six times with a new volume each time and a 0.2 s check loop:

| Wait line | Result of the `psql` right after |
|---|---|
| `pg_isready -U postgres` (no `-h`) | 3 out of 3 times: `Connection refused` |
| `pg_isready -h 127.0.0.1 -U postgres` | 3 out of 3 times: worked |

With a slow 1 second loop the no-`-h` version happened to pass once, which is exactly why this bug hides. The container log shows why: the temporary server reports "ready" at one moment, "shutting down" less than a tenth of a second later, and the real server starts after that.

### D2. The truck dies, the data stays

```bash
docker rm -f db
docker run -d --name db --network appnet \
  -e POSTGRES_PASSWORD=secret -v pgdata:/var/lib/postgresql/data postgres:16
until docker exec db pg_isready -h 127.0.0.1 -U postgres >/dev/null; do sleep 1; done
docker run --rm -e PGPASSWORD=secret --network appnet postgres:16 psql -h db -U postgres -c 'select * from t;'
docker volume inspect pgdata --format '{{.Name}} driver={{.Driver}} mountpoint={{.Mountpoint}}'
```

Expected: the row `1` is still there, and the volume line is `pgdata driver=local mountpoint=/var/lib/docker/volumes/pgdata/_data`. On Docker Desktop that path is inside the hidden VM, so you cannot open it from your Mac. On Ubuntu you can (with `sudo`). Either way: **if the building goes, the volume goes with it.**

### D3. Backing up and restoring the volume

Stop the database first, so the files are not changing while we copy them:

```bash
docker rm -f db
docker run --rm -v pgdata:/data -v "$PWD":/backup alpine \
  tar czf /backup/pgdata-$(date +%Y%m%d).tgz -C /data .
ls -l pgdata-*.tgz
```

Expected: one `.tgz` file (ours: `4606232` bytes, about 4.6 MB). Now restore it into a **new** volume and prove it works:

```bash
docker run --rm -v pgdata2:/data -v "$PWD":/backup alpine \
  tar xzf /backup/pgdata-$(date +%Y%m%d).tgz -C /data
docker run -d --name db2 --network appnet -e POSTGRES_PASSWORD=secret \
  -v pgdata2:/var/lib/postgresql/data postgres:16
until docker exec db2 pg_isready -h 127.0.0.1 -U postgres >/dev/null; do sleep 1; done
docker run --rm -e PGPASSWORD=secret --network appnet postgres:16 psql -h db2 -U postgres -c 'select * from t;'
docker run --rm -v pgdata2:/data alpine ls -ln /data | head -4
```

Expected: the row `1` comes back from the restored volume, and the file listing shows owner `999 999` and `drwx------` on the data directories. The ownership came through the tar intact, which is why the database accepted the files.

This copy was safe because the database was stopped. Copying a **running** database's folder can give you a half-written snapshot. For a live database use its own dump tool (`pg_dump`), as the script says. We did not test a backup of a running database.

### D4. Trucks find each other by name

```bash
docker run --rm --network appnet alpine nslookup db2 | grep -E 'Name|Address'
docker run -d --name nodns alpine sleep 60
docker run --rm alpine ping -c1 -W2 db2
docker run --rm alpine ping -c1 -W2 nodns
```

Expected (ours): on `appnet`, the name `db2` resolves to an address (`172.21.0.2`). On the **default** network, both `ping` lines say `ping: bad address 'db2'` and `ping: bad address 'nodns'`. Names only work on a network you created.

Check that the database port was never opened to the outside:

```bash
docker ps --filter name=db2 --format '{{.Names}} ports=[{{.Ports}}]'
```

Expected: `db2 ports=[5432/tcp]`. There is no `0.0.0.0:...->` part, so nothing is published. Other trucks on `appnet` can reach it anyway. That is the point.

### D5. Bind mounts and tmpfs

```bash
docker run -d --name bm -p 8082:80 -v "$PWD/lab_files/src:/usr/share/nginx/html:ro" nginx:alpine
curl -s localhost:8082
echo v2 > lab_files/src/index.html
curl -s localhost:8082
docker exec bm sh -c 'echo x > /usr/share/nginx/html/a'
```

Expected: `v1`, then `v2` right after you edit the file on your machine (no restart), then `Read-only file system` from the last line, because of `:ro`. Put `v1` back afterwards: `echo v1 > lab_files/src/index.html`. Then `docker rm -f bm`.

```bash
docker run --rm --tmpfs /scratch:rw,size=16m alpine sh -c 'echo secret > /scratch/k; cat /scratch/k; mount | grep scratch | cut -c1-70'
```

Expected: `secret`, then a `tmpfs on /scratch type tmpfs (rw,nosuid,nodev,noexec,...` line. It exists only in memory and vanishes with the truck.

### D6. Compose: the same thing from one file

`lab_files/compose.yaml` has a `db` service, an `app` service that waits for the database to be healthy, a network and a volume. The `app` here is only a stand-in: it uses the Postgres image to run `psql`, insert a booking row and count the rows. Read the file, then:

```bash
cd lab_files
docker compose up -d
docker compose ps --format 'table {{.Service}}\t{{.Status}}\t{{.Ports}}'
docker compose logs app
```

Expected (ours):

```
SERVICE   STATUS                   PORTS
app       Up Less than a second    5432/tcp
db        Up 2 seconds (healthy)   5432/tcp
```

and in the `app` log: `CREATE TABLE`, `INSERT 0 1`, then a count of `1`. The `app` waited for `db` to be healthy, using the same `-h 127.0.0.1` check as D1.

**Data survives `down`, not `down -v`:**

```bash
docker compose down
docker volume ls --format '{{.Name}}' | grep atithi
docker compose up -d
sleep 5
docker compose exec db psql -U postgres -c 'select count(*) from bookings;'
```

Expected: after `down`, the volume `atithi-lab_pgdata` is still listed. After `up` again, the count is **2**. Each start of the `app` added one booking, and the first one was still there.

```bash
docker compose down -v
docker volume ls --format '{{.Name}}' | grep atithi || echo "volume gone"
```

Expected: `volume gone`. `-v` removed the locker room, and every booking with it.

**Check yourself:**

- [ ] You can explain why the wait line needs `-h 127.0.0.1`.
- [ ] You restored a backup into a new volume and saw the data.
- [ ] You can say what `down -v` deletes that `down` does not.

---

## Clean up

```bash
docker rm -f db db2 nodns 2>/dev/null
docker volume rm pgdata pgdata2
docker network rm appnet
rm -f pgdata-*.tgz prod.env
docker system df
```

Expected: no errors, and `docker system df` shows the space coming back as you remove images (`docker image rm nginx:latest nginx:alpine alpine hello-world` if you want them gone). Check what each remove will delete before you run it, especially on a shared machine. If you used a cloud building, stop it now.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `Cannot connect to the Docker daemon` | Docker is not running, or your user is not in the `docker` group | Start Docker; on Linux, `sudo usermod -aG docker $USER`, then log out and in |
| `port is already allocated` | Something else uses that host port | Pick another port or stop the other thing (`lsof -iTCP:8080 -sTCP:LISTEN`) |
| `Conflict. The container name "/web" is already in use` | An old container with that name exists | `docker rm -f web` |
| `psql: error: connection ... Connection refused` right after starting the database | The wait line has no `-h 127.0.0.1`, or the database is not up yet | Use the D1 wait line |
| `bad address 'db'` | The two trucks are not on the same user-created network | Add `--network appnet` to both |
| A restored database will not start | Data folder ownership or permissions changed in the copy | Restore with `tar` inside a truck, as in D3, and check `ls -ln /data` shows owner `999` |
| `curl` from another machine times out | Security group, firewall, or you bound to `127.0.0.1` | Check the binding in `docker ps`, then the cloud firewall |

## What we did not test

- **Docker install on Ubuntu.** We used Docker Desktop on a Mac. The install steps and the `docker` group step are from the script, unrun.
- **The `ufw` bypass.** No `ufw` on a Mac. Try it yourself on Ubuntu (C4).
- **Gordon / `docker ai`.** Needs a signed-in account and sends data to Docker's service. Not run.
- **The 10 second stop default.** We measured about 3 seconds on Docker Desktop 29.8.2 and could not find the reason (C6).
- **Host `ps aux` showing the container process.** Mac host, not Linux (A2).
- **Backing up a running database,** and **Compose on several buildings.** Single machine only.
- **An exact match of sizes and IDs.** Image sizes and versions move; the ratios and behaviours are what to check.

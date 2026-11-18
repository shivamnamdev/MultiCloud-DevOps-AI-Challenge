# Session 19 lab guide: Jenkins advanced and distributed

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal and browser. Commands and outputs below come from real runs (Jenkins 2.580 LTS on Java 21, Maven 3.9, AWS CLI 1.x against a local S3 emulator). Your IDs, sizes and timings will differ.

| | |
|---|---|
| **Time** | Part A 35 min, Part B 35 min, Part C 40 min, Part D 40 min |
| **Cost** | **Docker practice: free** (the workbench and an S3 emulator are containers too). On real servers: one extra small VM for the workbench, one for the restore test, and S3 storage for the backups (about 200 MB per backup in our test). Stop the VMs when you finish and set the lifecycle rule from Part C. |
| **Skill check** | You finished Sessions 17 and 18 (a working Jenkins, `booking-service`, a Jenkinsfile) and Session 6 (scripts and cron). |

You continue with `~/booking-service` from Session 17.

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  docker/       Dockerfile.jenkins  Dockerfile.workbench  workbench-start.sh  plugins.txt  jenkins.yaml  compose.yml
  jenkinsfiles/ Jenkinsfile.multibranch  Jenkinsfile.secret  Jenkinsfile.secret-leaks  Jenkinsfile.workbench
  backup/       jenkins-backup.sh
```

## Before you start

**Option 1: Docker (free).**

```bash
cd ~/booking-service
cp /path/to/lab_files/jenkinsfiles/Jenkinsfile.multibranch Jenkinsfile
cp /path/to/lab_files/jenkinsfiles/Jenkinsfile.secret /path/to/lab_files/jenkinsfiles/Jenkinsfile.secret-leaks \
   /path/to/lab_files/jenkinsfiles/Jenkinsfile.workbench .
git add -A && git commit -m "Session 19 lab pipelines"
git checkout -b feature/demo && echo "// demo" >> src/main/java/atithi/Booking.java && git commit -am "feature: small change" && git checkout main

cd /path/to/lab_files
mkdir -p docker/keys && ssh-keygen -t ed25519 -N "" -f docker/keys/agent_key      # the pair Jenkins uses to reach the workbench
BOOKING_REPO=~/booking-service docker compose -f docker/compose.yml up -d --build
```

Wait about 40 seconds, open `http://localhost:8080`, log in as **admin** / **practice** (lab only). If port 8080 is busy, put `JENKINS_PORT=18080` in front.

You get three containers: Jenkins (with Maven, Git, the AWS CLI and the plugins for this session), a **workbench** (a second machine with SSH, Java, Git and Maven), and an S3 emulator. Practice shortcuts (never on a real server): no setup wizard, a folder path works as a repository URL, the repo is mounted into both Jenkins and the workbench, and the workbench's host key is not verified.

Remove everything at the end: `docker compose -f docker/compose.yml down -v`, and delete `docker/keys`.

**Option 2: real servers**, as in the script: your Jenkins, a second Ubuntu VM in the private wing with Java, Git and Maven installed, and S3. We tested Option 1 only.

---

## Part A: one conveyor per branch (Episode 1)

**Goal:** make Jenkins find every branch by itself, build each one, and drop a conveyor when its branch is deleted.

`Jenkinsfile.multibranch` is the Session 17 conveyor with two changes: `Package` and `Deploy` carry `when { branch 'main' }`, so only `main` packages and deploys.

### A1. Create the Multibranch Pipeline

**New Item**, name `booking-multi`, type **Multibranch Pipeline**. Under **Branch Sources** add **Git**, repository `/repos/booking-service` (Option 1) or your GitHub URL with credentials (Option 2). Keep the default **Discover branches**. Script path `Jenkinsfile`. Save. Jenkins scans the repository.

Expected in the **Scan Repository Log**:

```
Checking branch main
    Met criteria
Scheduled build for branch: main
Checking branch feature/demo
    Met criteria
Scheduled build for branch: feature/demo
```

and two sub-jobs in the folder, `main` and `feature%2Fdemo`, each building.

Expected stages. `main`:

```
Build SUCCESS, Test SUCCESS, Package SUCCESS, Deploy SUCCESS
```

`feature/demo`: `Build` and `Test` succeed, `Package` and `Deploy` are **not executed**. The same Jenkinsfile gave each branch its own behaviour.

### A2. Deliberate break: delete a branch

```bash
cd ~/booking-service
git branch -D feature/demo
```

In Jenkins, **Scan Repository Now**. Expected in the log:

```
Evaluating orphaned items in booking-multi
Will remove feature/demo
```

and the `feature/demo` conveyor disappears from the folder at once. In our test it vanished at the very next scan. (The default orphaned-item rule removes it immediately; you can change that under the job's **Orphaned Item Strategy** if you want a grace period.)

### A3. Pull requests and the fork warning (GitHub only, not tested)

The script's second half needs a GitHub repository: add the **GitHub Branch Source** discovery of pull requests, open a pull request from `feature/demo`, and watch a check appear on it; break a test and watch it turn red; then require that check in branch protection (Session 16B). Two cautions from the script: a pull request from a **fork** runs code written by someone you may not trust, so trust forks only from people you know; and Jenkins should never hand secrets to an untrusted pull request.

### Check yourself

- [ ] Two branches, two conveyors, created without you making a job for each.
- [ ] `feature/demo` skipped Package and Deploy; `main` ran them.
- [ ] A deleted branch's conveyor was removed on the next scan.

### Cleanup

Delete `booking-multi` when you finish, or keep it for later.

---

## Part B: the key cabinet (Episode 2)

**Goal:** use a secret in a pipeline without printing it, see what masking does not protect, and see how an administrator can read every secret.

### B1. Create a secret

**Manage Jenkins, Credentials, System, Global credentials, Add Credentials**: kind **Secret text**, Secret `S3cr3tV4lue123`, ID `demo-token`, description "practice secret". (You choose the ID; the pipeline refers to it by that name.)

### B2. Use it safely

Create a Pipeline job `secret` with Script Path `Jenkinsfile.secret`. The stage is:

```groovy
withCredentials([string(credentialsId: 'demo-token', variable: 'TOKEN')]) {
  sh 'echo "Token length: ${#TOKEN}"'
  sh 'echo "$TOKEN"'
}
```

(Single quotes around the `sh` text matter: Session 17's rule. The shell reads `$TOKEN`, Groovy never sees the value.) **Build Now.** Expected in the log:

```
+ echo Token length: 14
Token length: 14
+ echo ****
****
```

The length is visible and the value is replaced by `****`.

### Deliberate break: disguise the secret

Create a job `secret-leaks` with Script Path `Jenkinsfile.secret-leaks`. It prints the secret in five forms. Expected:

```
plain:   ****
base64:  ****
reverse: 321eul4Vt3rc3S
spaced:  S 3 c r 3 t V 4 l u e 1 2 3
hex:     53336372337456346c7565313233
```

Jenkins hides the plain value and its base64 copy, but a **reversed**, **spaced-out** or **hex** copy prints in full. Masking is a courtesy, not a guarantee: never run code you do not trust with a real secret, and never print one on purpose.

### Deliberate break: an administrator sees everything

**Manage Jenkins, Script Console** (or, for a command-line test, the `groovy` command) prints every credential in the clear. Our test:

```
demo-token = S3cr3tV4lue123
```

Anyone with administrator rights, and anyone who can read the Jenkins home folder together with its `secrets/` folder, can read every credential. That is why the next episode's backup rule matters, and why you want few administrators and short-lived badges instead of long-lived keys (Session 9).

### B3. No executors on the controller

**Manage Jenkins, Nodes, Built-In Node, Configure**: set **Number of executors** to `0`. Run `secret` again. Expected: the build waits. In the build queue the reason reads **`Waiting for next available executor`**. This is the setting you want on a real controller: it should not run builds, only manage them. Leave it at 0, because the build will run as soon as Part D gives it a workbench.

### Check yourself

- [ ] The log showed the length and `****` and never the value.
- [ ] You saw reverse, spaced and hex copies print in full.
- [ ] A build waited with `Waiting for next available executor`.

---

## Part C: backup, and the restore test that proves it (Episode 3)

**Goal:** back up Jenkins' home folder to S3, then restore it onto a second, empty Jenkins and check that everything is back.

### C1. What is in the home folder

Jenkins keeps its whole life in one folder, `JENKINS_HOME` (`/var/lib/jenkins` on a real server, `/var/jenkins_home` in Docker). The important parts: `jobs/` (your jobs and their build history), `credentials.xml` and `secrets/` (the encrypted credentials and the key that decrypts them), `nodes/`, `users/`, `plugins/` and `config.xml`. The `workspace/` folders (checked-out code) and caches are big and can be rebuilt, so the backup skips them.

### C2. Make the bucket and run the backup

Practice (Option 1), from `lab_files/docker`:

```bash
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 s3 mb s3://jenkins-backups
docker compose -f compose.yml cp ../backup/jenkins-backup.sh jenkins:/tmp/jenkins-backup.sh
docker compose -f compose.yml exec -e JENKINS_HOME=/var/jenkins_home -e BUCKET=jenkins-backups \
  -e ENDPOINT="--endpoint-url http://floci:4566" jenkins bash /tmp/jenkins-backup.sh
```

Real server: run the script as the user that can read the folder, with `JENKINS_HOME=/var/lib/jenkins BUCKET=your-backup-bucket`, from a building whose duty badge allows writing to that bucket (no access keys in the script). The script is the one from the script's lab: `set -euo pipefail`, a timestamped name, `tar --exclude=workspace --exclude=caches`, `aws s3 cp --sse AES256`, then it deletes the local copy.

Expected: `upload: ... to s3://jenkins-backups/jenkins/jenkins-<timestamp>.tgz` and `backup done: <timestamp>`. List it:

```bash
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 s3 ls s3://jenkins-backups/jenkins/
```

Expected: one file of about **190 MB** (ours: 199,830,733 bytes). Most of that is the plugins; your jobs are tiny. Look inside it: `tar -tzf` shows `jenkins_home/secrets/master.key`, `jenkins_home/credentials.xml`, `jenkins_home/jobs/...`, `jenkins_home/nodes/...` and `jenkins_home/users/...`, and **no** `workspace` entries. Schedule it with `cron` and `flock` like Session 6, and add an S3 **lifecycle rule** that deletes backups after 14 days.

### C3. The restore test

A backup you have never restored is only a hope. Download the archive, extract it into a brand-new, empty home folder, and start a second Jenkins from it. In Docker:

```bash
# 1. download from S3 and copy it out of the container
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 s3 cp s3://jenkins-backups/jenkins/FILE.tgz /tmp/restore.tgz
docker compose -f compose.yml cp jenkins:/tmp/restore.tgz ./restore.tgz

# 2. extract into a new volume (as root, then give it back to the jenkins user)
docker volume create restorevol
docker run --rm -u root -v restorevol:/var/jenkins_home -v "$PWD/restore.tgz":/b.tgz:ro --entrypoint sh docker-jenkins \
  -c 'tar -xzf /b.tgz --strip-components=1 -C /var/jenkins_home && chown -R jenkins:jenkins /var/jenkins_home'

# 3. start a second Jenkins on the restored volume, on another port
docker run -d --name jenkins-restore --network docker_default -p 18081:8080 \
  -v restorevol:/var/jenkins_home -v ~/booking-service:/repos/booking-service docker-jenkins
```

(`docker-jenkins` is the image name compose gave it; check with `docker images`. The network name is the folder name plus `_default`.) On a real server this is the script's recipe: install the same Jenkins version on a second building, `sudo systemctl stop jenkins`, extract into `/var/lib`, `sudo chown -R jenkins:jenkins /var/lib/jenkins`, `sudo systemctl start jenkins`.

Open `http://localhost:18081` and check. In our test the restored Jenkins had:

- all four jobs (`booking-multi`, `secret`, `secret-leaks`, `workbench`),
- the full build history of `secret` (builds 3, 2 and 1),
- the node `linux-agent`, back online,
- the credential `demo-token`, **still decrypting** to its value.

### Deliberate break: a backup without `secrets/`

Extract the same archive into another empty volume, but add `--exclude=jenkins_home/secrets` to the `tar` command, and start Jenkins on it. Expected:

- the **jobs come back**,
- but the credential is now an unreadable encrypted blob (`demo-token = {AQAAABAAAAAQ...}`),
- and the SSH node cannot start: `This agent is offline because Jenkins failed to launch the agent process on it.`

`secrets/master.key` is the key that decrypts every credential. Back up `secrets/` and keep the backup as protected as the server itself. Without it, you rebuild every credential by hand.

### Upgrade habit

Before upgrading Jenkins or plugins: take a backup, upgrade a copy (your restored test instance is exactly that), read the upgrade notes, and keep a note of the previous version so you can go back. Jenkins' long-term-support line moves forward every few months.

### Cleanup

Remove the test Jenkins and volume: `docker rm -f jenkins-restore; docker volume rm restorevol`. Delete the downloaded `restore.tgz` (it holds your secrets). On real AWS, terminate the restore-test building (do not just stop it) and check for leftover disks.

### Check yourself

- [ ] The backup listed `master.key` and `credentials.xml` and had no `workspace`.
- [ ] The restored Jenkins had your jobs, history, node and a working credential.
- [ ] You saw what happens to credentials when `secrets/` is missing.

---

## Part D: a workbench over SSH (Episode 4)

**Goal:** add a second machine, make a pipeline run there, and see what happens when it goes offline.

Practice: the workbench container is already running. Its public key is in `docker/keys/agent_key.pub`; Jenkins needs the matching private key as a credential.

### D1. A credential for the workbench

**Credentials, Add Credentials**: kind **SSH Username with private key**, ID `agent-key`, username `jenkins`, **Enter directly** the private key (the contents of `docker/keys/agent_key`). Real servers: the key pair belongs to the workbench's user, and the public key goes into that user's `~/.ssh/authorized_keys`.

### D2. Add the node

**Manage Jenkins, Nodes, New Node**: name `linux-agent`, **Permanent Agent**. Number of executors 2 (about one per CPU core), Remote root directory `/home/jenkins`, Labels `linux-agent`, Launch method **Launch agents via SSH**, Host `workbench` (a real VM: its private IP), Credentials `agent-key`, Host Key Verification Strategy: choose **Known hosts file** or **Manually trusted** on a real server (the practice setup uses **Non verifying**, which is not safe for real life). Save.

Expected within about 25 seconds: the node turns **online**, assigned label `linux-agent`, 2 executors. The queued `secret` build from Part B starts running on it.

Two things the SSH launch needs from the workbench: **Java on the PATH of an SSH session** (not just in the image's environment: the practice image adds it to `/etc/profile.d` and `.bashrc`; a missing Java gives `java: command not found`), and the right user and key.

### D3. Run a pipeline on it

Create a job `workbench` with Script Path `Jenkinsfile.workbench`:

```groovy
pipeline {
  agent { label 'linux-agent' }
  stages { stage('Where am I') { steps { sh 'hostname; whoami; mvn -v | head -1' } } }
}
```

Expected in the log: `Running on linux-agent in /home/jenkins/workspace/workbench`, then `workbench`, `jenkins` and a Maven version. The hostname is the workbench's, not the controller's. With the controller at 0 executors, every build now runs here.

**A practice trap you will meet:** Declarative pipelines check out the code **on the workbench**. In our first attempt the build failed with `fatal: '/repos/booking-service' does not appear to be a git repository`, because the workbench could not see a folder path that only existed inside the Jenkins container. In real life you use a Git URL that both machines can reach (GitHub, with credentials). In practice we mounted the repo into both containers.

### Deliberate break: the workbench goes offline

```bash
docker stop docker-workbench-1        # the name may differ: docker ps
```

Start a `workbench` build. Expected: it does not fail, it **waits**. In the queue the reason is:

```
‘linux-agent’ is offline
```

Start the workbench again (`docker start docker-workbench-1`). In our test Jenkins reconnected after about 30 seconds and the waiting build ran and succeeded. No human touched Jenkins. If you have more than one workbench with the same label, work moves to the other one.

### Labels and executors

Labels decide **where** work may go (`linux`, `maven`, `docker`); executors decide **how much** runs at once (about one per CPU core: more makes builds slow and memory tight). `agent { docker { image 'maven:3-eclipse-temurin-17' } }` gives each build a clean container if the workbench has Docker and the Docker Pipeline plugin; we did not test it.

### Cleanup (do not skip)

- Docker: `docker compose -f docker/compose.yml down -v`, `docker image rm docker-jenkins docker-workbench`, and delete `docker/keys` (it holds a private key).
- Real servers: terminate the workbench and restore-test VMs, delete their keys and security groups' extra rules, and check for leftover volumes and Elastic IPs.
- In Jenkins, delete the credentials you created if the controller will be used for anything else.

### Check yourself

- [ ] The node `linux-agent` was online and your pipeline ran on it (hostname `workbench`).
- [ ] An offline workbench made the build wait with `‘linux-agent’ is offline`, and it ran after reconnecting.
- [ ] You can say why `java` must be on the PATH of an SSH session.

---

## Final checklist for Session 19

- [ ] Part A: a Multibranch Pipeline; `main` ran all stages, a feature branch skipped two; a deleted branch vanished
- [ ] Part B: a secret used safely; reverse, spaced and hex copies printed in full; builds waited with 0 executors
- [ ] Part C: a backup with `master.key`, a restore test that worked, and the no-`secrets/` failure seen
- [ ] Part D: an SSH workbench online, a pipeline running there, an offline workbench handled
- [ ] Practice containers, volumes, the restored archive and the private key removed

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| No branches appear after a scan | Wrong repository URL, or no `Jenkinsfile` in the branch | Read the Scan Repository Log; check the file name |
| Branch builds fail at checkout on the workbench | The workbench cannot read the repository URL | Use a Git URL reachable from both machines |
| Build waits with `Waiting for next available executor` | The controller has 0 executors and no workbench is online | Bring a workbench online, or give the controller an executor while learning |
| Node offline: `Failed to launch the agent process` | Java missing on the SSH PATH, wrong key or user, or port 22 blocked | Test `ssh jenkins@workbench` by hand, then `java -version` in that session |
| `Host key verification failed` for the node | Strategy is stricter than the hosts known to Jenkins | Add the host key, or pick **Manually trusted** the first time |
| Restored Jenkins shows jobs but credentials are blobs | `secrets/` missing from the backup | Restore from a backup that includes `secrets/`; otherwise recreate the credentials |
| Restored files are owned by the wrong user | Extracted as root without `chown` | `chown -R jenkins:jenkins` the home folder |
| `BucketNotEmpty` or lifecycle surprises | Versioned bucket | Remember old versions count (Session 28 cleanup loop) |

## What we did not test

Everything ran on Jenkins 2.580.2 LTS in Docker with a local S3 emulator and a container as the workbench. The jobs, credentials and node were created through the Jenkins command line with the settings the browser forms would save; we did not click through the web pages. We did not run: GitHub pull-request discovery and checks, branch protection with a required Jenkins check, fork-trust settings, real S3 (including `--sse AES256`, bucket lifecycle rules, and a duty badge instead of keys), a real second VM in a private wing and its security groups, the Known-hosts and Manually-trusted host key strategies, `agent { docker { ... } }`, cron with `flock`, a real Jenkins upgrade, or the Stage View colours.

# Session 17 lab guide: Jenkins foundations

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal and browser. Commands and outputs below come from real runs (Jenkins 2.580 LTS on Java 21, Maven 3.9.9, Git 2.47). Your hostnames, build numbers and timings will differ.

| | |
|---|---|
| **Time** | Part A 20 min, Part B 25 min, Part C 40 min, Part D 40 min |
| **Cost** | **Docker practice: free.** On a **cloud server** (a `t3.small` with at least 2 GB RAM, as in the script) a few cents per hour: stop the instance when you finish, do not leave it running. |
| **Skill check** | You can use Git and GitHub (Sessions 16 and 16B), Linux users (Session 4) and the AWS console (Session 8). |

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  docker/            Dockerfile  plugins.txt  jenkins.yaml  compose.yml     <- a practice Jenkins in Docker
  booking-service/   a small Maven project with two unit tests and a Jenkinsfile
```

## Before you start: get a Jenkins

**Option 1: Docker (free, recommended for practice).**

```bash
cd lab_files
cp -R booking-service ~/booking-service              # your own copy, outside this folder
cd ~/booking-service
git init -b main && git add . && git commit -m "booking-service: first version"
cd - && cd docker
BOOKING_REPO=~/booking-service docker compose -f compose.yml up -d --build
```

Wait about 30 seconds, then open `http://localhost:8080` and log in as **admin** with password **practice** (lab only: these are practice credentials, never use them for anything real). Port 8080 busy? Add `JENKINS_PORT=18080` in front of the command and use that port.

What this gives you: Jenkins LTS on Java 21, Maven and Git inside the container, and the plugins this session uses (Git, Pipeline, JUnit, Stage View, Timestamper). Three practice shortcuts: the setup wizard is skipped, the admin user is created for you, and a Git repository can be given as a folder path (`/repos/booking-service`), which is your `~/booking-service` folder seen from inside the container. In real life you would use a GitHub URL.

To stop and delete everything afterwards: `docker compose -f compose.yml down -v` (from `lab_files/docker`, with the same `BOOKING_REPO` variable).

**Option 2: a real server**, as in the script: an Ubuntu 22.04 or 24.04 machine with at least 2 GB RAM, a `Name` tag of `jenkins-lab`, and port 8080 open **only to your own IP** (Session 14's rule). Install Java, Git and Maven:

```bash
sudo apt update && sudo apt install -y openjdk-17-jre git maven
java -version
mvn -v
```

Then install Jenkins by following the official Linux instructions at jenkins.io (versions and repository keys change, so we do not copy them here), open `http://SERVER_IP:8080`, unlock it with the initial password from `/var/lib/jenkins/secrets/initialAdminPassword`, and choose "Install suggested plugins". We did not test the real-server install in this guide: the steps in Parts B to D were tested with Option 1. Use a Git URL from GitHub (your fork of a small Maven project) instead of `/repos/booking-service`.

---

## Part A: check that the foreman's office is ready (Episode 1)

**Goal:** confirm the tools and understand what runs where.

For Option 1:

```bash
docker compose -f compose.yml exec jenkins bash -c 'java -version 2>&1 | head -1; mvn -v | head -1; git --version; whoami; hostname'
```

Expected: `openjdk version "21...` (or 17 on a real server), `Apache Maven 3.9.9`, `git version 2.4x`, user **`jenkins`**, and the container's hostname. Remember `whoami`. Jenkins does not run as `root`, and in Part B you will see why that is good.

In the browser, open **Manage Jenkins** and look at the system message ("Atithi practice foreman"), the number of executors (2) and the list of installed plugins. Each executor can run one build at a time.

### Check yourself

- [ ] You can open Jenkins in the browser and log in.
- [ ] `mvn -v` and `git --version` work inside Jenkins' own machine.
- [ ] You know that `whoami` prints `jenkins`, not your own username.

---

## Part B: the first job, a parameter, a permission wall (Episode 2)

**Goal:** make a freestyle job, run it with a parameter, read the log, and see failure on purpose.

### B1. Create the job

In the browser: **New Item**, name `hello-job`, type **Freestyle project**, OK. Tick **This project is parameterized**, add a **String Parameter** named `NAME` with default `Atithi`. Under **Build Steps** add **Execute shell** with:

```bash
echo "Hello, $NAME"; hostname; whoami
```

Save, then **Build with Parameters**, enter your name, **Build**.

Open the build, then **Console Output**. Expected (shortened):

```
Building in workspace /var/jenkins_home/workspace/hello-job
+ echo Hello, Shivam
Hello, Shivam
+ hostname
35a652c33501
+ whoami
jenkins
Finished: SUCCESS
```

The hostname is the Jenkins machine's, and the user is `jenkins`: the job ran as the service user, not as you.

### Deliberate break 1: the permission wall

Edit the shell step so it ends with `; ls /root`, save and build.

Expected, at the bottom of the log:

```
+ ls /root
ls: cannot open directory '/root': Permission denied
Build step 'Execute shell' marked build as failure
Finished: FAILURE
```

The `jenkins` user is not allowed into `/root`. That is least privilege (Session 4) working for you. Do **not** "fix" this by running Jenkins as root.

### Deliberate break 2: your own failure

Replace the step with:

```bash
echo "about to fail"; exit 1
```

Build. Expected: the build is red and the log ends with `+ exit 1`, `Build step 'Execute shell' marked build as failure`, `Finished: FAILURE`. Practise reading it: start at the **bottom**, find the line just above `Finished`, then read upward to the first error.

**Exit codes decide everything:** a step that exits 0 is green, anything else is red.

### Check yourself

- [ ] You ran the job with a parameter and saw `Hello, <your name>` in the log.
- [ ] You saw `Permission denied` for `/root` and can explain why that is correct.
- [ ] A build with `exit 1` turned red.

### Cleanup

Keep this job for reference or delete it (**Delete Project**). On a real cloud server, **stop** the instance when you finish for the day (stop, not terminate: you will use it again).

---

## Part C: your first fabrication, and a deliberately broken test (Episode 3)

**Goal:** have Jenkins fetch code from Git, build it with Maven, run the tests, keep the jar, and catch a broken test.

Look at `~/booking-service`. It has `pom.xml`, `src/main/java/atithi/Booking.java` (a function that counts the nights between check-in and check-out) and `src/test/java/atithi/BookingTest.java` (two tests).

### C1. Create the job

**New Item**: `booking-build`, **Freestyle project**.

- **Source Code Management**: Git. Repository URL: `/repos/booking-service` (Option 1) or your GitHub URL (Option 2). Branch: `*/main`.
- **Build Steps**: Execute shell: `mvn -B clean package`
- **Post-build Actions**: **Publish JUnit test result report** with `target/surefire-reports/*.xml`, and **Archive the artifacts** with `target/*.jar`.

Save and **Build Now**. The first build downloads Maven dependencies from the internet, so it takes a minute or two.

Expected in the log: `Cloning the remote Git repository`, `Checking out Revision ...`, `Tests run: 2, Failures: 0`, `BUILD SUCCESS`. On the build page: **Test Result** with 2 tests passed and the jar `booking-service-1.0.0.jar` under Last Successful Artifacts.

### Deliberate break: a wrong expectation

In `~/booking-service/src/test/java/atithi/BookingTest.java` change the first test from `assertEquals(3, ...)` to `assertEquals(4, ...)`. Commit it (in Option 2, push it):

```bash
cd ~/booking-service
git commit -am "break a test on purpose"
```

**Build Now** again. Expected: the build is red. In the **Console Output**:

```
[ERROR] Tests run: 2, Failures: 1, Errors: 0, Skipped: 0
[ERROR] atithi.BookingTest.threeNights -- Time elapsed: 0.024 s <<< FAILURE!
org.opentest4j.AssertionFailedError: expected: <4> but was: <3>
	at atithi.BookingTest.threeNights(BookingTest.java:12)
[INFO] BUILD FAILURE
```

and on the build page, **Test Result** says 1 failed, 1 passed, with `threeNights` listed. The test name, the line and the numbers are all there. This is why CI exists: your mistake is caught minutes after the commit, not on Friday evening.

### Fix

Undo your commit and build again:

```bash
git revert --no-edit HEAD
```

Expected: the build is green again with 2 tests passing. (Reverting rather than editing keeps the mistake and its fix in the history, as in Session 16B.)

### Check yourself

- [ ] The first build gave `BUILD SUCCESS`, 2 tests, and an archived jar.
- [ ] The broken build named the failing test, the line and `expected: <4> but was: <3>`.
- [ ] A later commit turned it green again.

---

## Part D: the conveyor written down as a Jenkinsfile (Episode 4)

**Goal:** move the instructions out of the web page and into the repository, so changes to the conveyor go through Git like any other change.

Open `~/booking-service/Jenkinsfile`:

```groovy
pipeline {
  agent any
  options { timeout(time: 15, unit: 'MINUTES') }
  stages {
    stage('Build')   { steps { sh 'mvn -B -DskipTests clean compile' } }
    stage('Test')    { steps { sh 'mvn -B test' } }
    stage('Package') { steps { sh 'mvn -B -DskipTests package' } }
  }
  post {
    always  { junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml' }
    success { archiveArtifacts artifacts: 'target/*.jar', fingerprint: true }
    failure { echo 'Build failed. Look at the red stage first.' }
  }
}
```

It is already committed in your repository. In the browser: **New Item**, name `booking-pipeline`, type **Pipeline**. Under **Pipeline**, choose **Pipeline script from SCM**, SCM **Git**, the same repository URL as before, branch `*/main`, Script Path `Jenkinsfile`. Save and **Build Now**.

Expected: **Stage View** shows `Checkout SCM`, `Build`, `Test`, `Package`, all green with timings. After a successful run the jar is attached to the build as an archived artifact.

### Deliberate break: a broken test in the pipeline

Again change `assertEquals(3` to `assertEquals(4` in the test, commit it, and **Build Now**.

Expected in the **Console Output**:

```
[Pipeline] { (Build)
[Pipeline] { (Test)
[ERROR] Tests run: 2, Failures: 1 ...
[Pipeline] { (Package)
Stage "Package" skipped due to earlier failure(s)
Build failed. Look at the red stage first.
Finished: FAILURE
```

`Build` passes, `Test` fails, `Package` does not run (so you never package something that fails its tests), and the `post failure` message is printed. We checked the log text, not the colours Stage View uses, so rely on the log for what ran and what was skipped.

### Fix

`git revert --no-edit HEAD`, build again, and watch all stages go green.

### Why the Jenkinsfile lives in the repository

Edit the `Jenkinsfile` (for example, add `timestamps()` or change the timeout), commit, and build. The next run uses the new version, with no click in the Jenkins UI. Nobody can change the conveyor silently: the change is a commit with an author, a message and a place in the history. In real life you open a pull request for it (Session 16B).

### Cleanup (do not skip)

- **Docker:** `docker compose -f compose.yml down -v` (from `lab_files/docker`, with the same `BOOKING_REPO` variable) removes Jenkins and its data. `docker image rm docker-jenkins` also removes the image.
- **Cloud server:** stop the instance (not terminate if you will continue to Session 18). Check the 8080 rule still allows only your IP. When the course is over, terminate it and check for leftover disks and Elastic IPs.
- Your `~/booking-service` folder is yours: keep it for Sessions 18 and 19.

### Check yourself

- [ ] `booking-pipeline` ran Build, Test and Package from the `Jenkinsfile`.
- [ ] A broken test stopped the pipeline at Test and `Package` was skipped.
- [ ] You changed the pipeline by committing the `Jenkinsfile`, not by clicking.

---

## Final checklist for Session 17

- [ ] Part A: Jenkins reachable; Java, Maven and Git work; you know the user is `jenkins`
- [ ] Part B: a parameterized job; `Permission denied` and `exit 1` read correctly
- [ ] Part C: Git, Maven, tests and an archived jar; a deliberately broken test caught
- [ ] Part D: a Pipeline from SCM; failure stops at Test; change by commit
- [ ] Practice Jenkins removed (or the cloud server stopped)

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| Browser cannot reach port 8080 | Container not started, wrong port, or security group closed | `docker compose ps`; try `JENKINS_PORT=18080`; check your IP in the security group |
| Jenkins will not check out a folder path given as the repository URL | Jenkins blocks local paths by default | Use the Docker practice setup (it allows it), or use a Git URL |
| `fatal: detected dubious ownership` | The repo folder belongs to another user | Already handled in the practice image; on a real server run `git config --global --add safe.directory '*'` as the `jenkins` user only if you understand the risk |
| First Maven build is slow | Downloads dependencies | Wait; later builds are fast |
| `mvn: command not found` | Maven not installed on the Jenkins machine | `apt install maven` (real server) |
| Pipeline fails at "Checkout SCM" | Wrong URL, branch or Script Path | Check the three fields; the branch is `*/main` |
| Build red with `Permission denied` | The job touches a path `jenkins` cannot use | Use the workspace, not `/root` |
| You cannot find the failing line | Reading from the top | Read the console from the bottom up |

## What we did not test

Parts B to D were run on Jenkins 2.580.2 LTS in Docker, with the jobs created through the Jenkins command line using the same settings the browser forms would save (we did not click through the web pages). We did not run: the real-server install steps on Ubuntu, the setup wizard and its "suggested plugins", GitHub URLs and webhooks, the exact colours of Stage View, Jenkins as a systemd service, or HTTPS. The quote-and-secret trap from Scene 4 of the script (`sh "..."` against `sh '...'`) was checked earlier but is not part of this lab.

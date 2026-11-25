# Session 18 lab guide: Jenkins pipelines and plugins

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal and browser. Commands and outputs below come from real runs (Jenkins 2.580 LTS on Java 21, Maven 3.9.9, AWS CLI 1.46 against a local AWS emulator). Your build numbers, IDs and timings will differ.

| | |
|---|---|
| **Time** | Part A 45 min, Part B 30 min, Part C 35 min, Part D 35 min |
| **Cost** | **Docker practice: free** (including the AWS emulator, so no AWS account is needed). On a real Jenkins server and real AWS, publishing a few SNS messages costs a tiny fraction of a cent, but the server itself bills by the hour: stop it when you finish. |
| **Skill check** | You finished Session 17 (a working Jenkins, the `booking-service` repo with its Jenkinsfile) and Session 15 (SNS and permissions). |

You continue with the `~/booking-service` repository from Session 17. If you do not have it, copy it from Session 17's `lab_files/booking-service` and run `git init -b main && git add . && git commit -m "first version"` in it.

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  docker/       Dockerfile  plugins.txt  jenkins.yaml  compose.yml   <- practice Jenkins + AWS emulator
  jenkinsfiles/ Jenkinsfile.smart  Jenkinsfile.alerts  Jenkinsfile.lib
  ci-lib/       vars/notifyBuild.groovy                               <- the shared library, to become its own repo
```

## Before you start

**Option 1: Docker (free).** Make the shared-library repository, then start everything:

```bash
cp -R lab_files/ci-lib ~/ci-lib
cd ~/ci-lib && git init -b main && git add . && git commit -m "ci-lib: notifyBuild" && git tag v1.0
cd -  # back to the guide's folder
cd lab_files/docker
BOOKING_REPO=~/booking-service CI_LIB_REPO=~/ci-lib docker compose -f compose.yml up -d --build
```

Wait about 40 seconds, then open `http://localhost:8080` and log in as **admin** with password **practice** (lab only). If port 8080 is busy, add `JENKINS_PORT=18080` in front of the command. Jenkins has Maven, Git, the AWS CLI and the plugins for this session. A small AWS emulator runs next to it, so the AWS CLI inside Jenkins talks to the emulator and not to real AWS.

Practice shortcuts in this setup (never copy them to a real server): the setup wizard is skipped, a folder path works as a repository URL, and the Git "bell" accepts calls without a token (Part B explains why that matters). Remove everything at the end with `docker compose -f compose.yml down -v` (same variables).

**Option 2: your own Jenkins and AWS** from Session 17. You need the plugins Pipeline, Pipeline: Stage View, JUnit, Timestamper, Workspace Cleanup, Pipeline: Input Step and Git; the AWS CLI on the Jenkins machine; and an SNS topic `ops-alerts` with permission to publish. We tested Option 1 only.

---

## Part A: a smarter conveyor (Episode 1)

**Goal:** add a choice parameter, environment and options, parallel stations, a human approval gate and a conditional deploy, then catch a typo before building.

### A1. The Jenkinsfile

Copy `lab_files/jenkinsfiles/Jenkinsfile.smart` over `~/booking-service/Jenkinsfile`, commit it, and create a **Pipeline** job named `smart` with **Pipeline script from SCM**, your repo, branch `*/main`, Script Path `Jenkinsfile` (as in Session 17).

Read the file first. The parts to notice:

- `agent none` at the top: no machine is reserved for the whole run. Each stage that needs one asks for `agent any`.
- `parameters { choice(name: 'ENV', ...) }`, `environment { APP_NAME = ... }`, and `options { timeout, timestamps, disableConcurrentBuilds, buildDiscarder }`.
- `failFast true` on the stage with `parallel`, and two parallel branches, `Unit` and `Lint`.
- An `Approval` stage with `input` inside a `timeout` and **no agent**, and a `Deploy` stage guarded by `when`.
- `checkout scm` inside `Unit`: with no top-level agent, nothing fetches your code for you.

### Deliberate break 1: the wrong place for `agent`

Declarative Pipeline refuses `agent` on a stage that also has `parallel`. If you put `agent any` on the `Checks` stage, the build stops immediately with:

```
WorkflowScript: 13: "agent" is not allowed in stage "Checks" as it contains parallel or matrix stages
```

The fix, already in the file: put `agent any` on each parallel branch, not on the parent.

### A2. First run: no parameters yet

**Build Now** (no parameters appear yet). Expected: `SUCCESS`, with `Approval` and `Deploy` both **not executed**, because `params.ENV` is empty on the very first run. After this first run Jenkins has read the Jenkinsfile and registered the parameter, and the button becomes **Build with Parameters**.

(In the command line a brand-new job shows the same rule: `ERROR: smart is not parameterized but the -p option was specified.`)

### A3. Run with `dev`

**Build with Parameters**, `ENV = dev`. Expected stages: `Checks` (with `Unit` and `Lint`), then `Approval` and `Deploy` skipped. In the **Console Output**:

```
Stage "Approval" skipped due to when conditional
Stage "Deploy" skipped due to when conditional
```

Check the timestamps: the line `lint ok` and the start of the Maven test appear within the same second. The two branches ran side by side.

### A4. Run with `staging` and approve

**Build with Parameters**, `ENV = staging`. Expected: after `Checks`, the build **pauses** at `Approval` waiting for you. Look at **Manage Jenkins, Nodes** (or the executor panel on the left): **0 busy executors**. Waiting for a person holds no machine, because the `Approval` stage has no agent.

Click the **Approval** step in the build page and press **Deploy**. Expected: the log shows `Approved by admin`, then `deploying booking-service to staging`, and the build is `SUCCESS`.

(Our command-line stand-in: `POST /job/smart/<n>/input/<id>/proceedEmpty`, the same URL the button uses.)

### Deliberate break 2: hold the executor by mistake

If you change the top of the file to `agent any` (and keep the rest), the pause at `Approval` still holds one executor, even though the stage itself has no agent. In our test `busyExecutors` went from 0 to 1. With only two executors, two people waiting for approval would stop all other builds. Put `agent none` back.

### A5. Catch the typo before you push

In the Jenkinsfile, change `stages {` to `stage {` (do not commit). Ask Jenkins to validate it, using the pipeline linter. It needs your user and a token or password (and a crumb when using a password): `curl -s -X POST -u USER:API_TOKEN -F "jenkinsfile=<Jenkinsfile" "http://localhost:8080/pipeline-model-converter/validate"`. Expected:

```
Errors encountered validating Jenkinsfile:
WorkflowScript: 11: Undefined section "stage" @ line 11, column 3.
     stage {
     ^

WorkflowScript: 1: Missing required section "stages" @ line 1, column 1.
```

With the typo fixed: `Jenkinsfile successfully validated.` Note what the linter does not catch: the `agent`-with-`parallel` mistake from Break 1 appears only when the build starts. Always do one real run.

### Check yourself

- [ ] The first run skipped `Approval` and `Deploy`; the second showed the parameter button.
- [ ] `Unit` and `Lint` ran side by side.
- [ ] The paused `staging` build held 0 executors, and approval let it finish.
- [ ] The linter gave you a line number for the typo.

### Cleanup

Delete the `smart` job when you no longer need it (Delete Pipeline).

---

## Part B: the bell, not the finger (Episode 2)

**Goal:** make a commit start a build by itself, and see why the door must be guarded.

The script uses a GitHub webhook. Jenkins here is on your laptop and GitHub cannot reach it, so we test the same mechanism with a Git **post-commit hook** in your local repository ringing Jenkins' own endpoint, `/git/notifyCommit`. The idea is identical: the repository tells Jenkins "something changed, please look".

### B1. A job that listens

Create a Pipeline job `bell` (SCM: your repo, `Jenkinsfile`), and under **Build Triggers** tick **Poll SCM** with an **empty schedule** (no timer: it only polls when the bell rings). Run it once by hand so it has a first build.

### Deliberate break: ring the bell without a token

```bash
curl -s -w ' [http %{http_code}]\n' "http://localhost:8080/git/notifyCommit?url=/repos/booking-service"
```

On a normal Jenkins the answer is `401 An access token is required`. That is the safe default: anybody who can reach the bell could otherwise trigger polling. On a real server, create a token under **Manage Jenkins, Security** (Git plugin notifyCommit access tokens) and add `&token=YOUR_TOKEN` to the URL. The practice Jenkins relaxes this (and only this) so you can see the mechanism. Never do that on a server people can reach.

### B2. Ring it, with and without a change

With the practice setting, ring the bell with nothing new:

```
Scheduled polling of bell
```

Expected response `[http 200]`, but **no new build** (nothing changed). Now install a hook in your repo, `.git/hooks/post-commit`, and make it executable:

```sh
#!/bin/sh
curl -s "http://localhost:8080/git/notifyCommit?url=/repos/booking-service" >/dev/null
```

```bash
chmod +x .git/hooks/post-commit
echo "more" >> README.md && git add -A && git commit -m "docs: second change"
```

Expected within seconds: a new build of `bell`, and the first line of its log says **`Started by an SCM change`**. No one pressed a button.

### B3. The real webhook (GitHub)

**Tested for real on 2026-11-24** (results right below this paragraph). To do the GitHub version: install the **GitHub** plugin (it is **not** in this session's `plugins.txt`; add `github` to it, we used `github 1.47.0`), tick **GitHub hook trigger for GITScm polling** in the job, and in the GitHub repository add a webhook with payload URL `http://YOUR_JENKINS:8080/github-webhook/`, content type `application/json`, event "Just the push event". Then a push starts a build whose log begins `Started by GitHub push by ...`. If it does not fire, check in this order (Session 14): the webhook's **Recent Deliveries** response code in GitHub, then your security group or firewall (GitHub publishes the address ranges it uses; do not simply open the port to the whole world), then the trailing slash in the URL, then the plugin. When you finish, delete the webhook and close the firewall rule.

### Check yourself

- [ ] You saw `401` without a token (on a normal Jenkins) and understand why it is the right default.
- [ ] A commit started a build by itself and the log said `Started by an SCM change`.
- [ ] You can name the four things to check, in order, when a webhook does not fire.

### Cleanup

Delete the `bell` job and remove `.git/hooks/post-commit` from your repository.

---

## Part C: tell me when it breaks, and when it is fixed (Episode 3)

**Goal:** send a message to a topic on failure and on recovery, with a link to the build.

Practice setup (Option 1): create a topic and a queue that stands in for "the phone", and subscribe the queue to the topic:

```bash
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 sns create-topic --name ops-alerts
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 sqs create-queue --queue-name phone
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:000000000000:ops-alerts --protocol sqs \
  --notification-endpoint arn:aws:sqs:us-east-1:000000000000:phone
```

Note the explicit `--endpoint-url` on every command: with this AWS CLI version the environment variable alone reached the emulator for SNS but sent SQS calls to real AWS, which rejected the fake keys with `InvalidClientTokenId`. (On real AWS you use no endpoint option and a real topic ARN.)

Copy `lab_files/jenkinsfiles/Jenkinsfile.alerts` into your repository as `Jenkinsfile.alerts` and commit. Create a Pipeline job `alerts` with Script Path `Jenkinsfile.alerts`. It runs `mvn -B test` and, in `post`, publishes on `failure` and on `fixed` with the build link.

### Run the cycle

1. **Build Now**: green. No message (nothing failed).
2. Break a test as in Session 17 (`assertEquals(3` to `assertEquals(4`), commit, build: **FAILURE**.
3. `git revert --no-edit HEAD`, build: **SUCCESS**.

Read the "phone":

```bash
docker compose -f compose.yml exec jenkins aws --endpoint-url http://floci:4566 sqs receive-message \
  --queue-url http://floci:4566/000000000000/phone --max-number-of-messages 10 --query 'Messages[].Body'
```

Expected, two messages:

```
FAILED alerts #6 http://localhost:8080/job/alerts/6/
FIXED alerts #7 http://localhost:8080/job/alerts/7/
```

(Each arrives wrapped in a JSON envelope; the `Message` field holds the text above.) The `fixed` condition fires only when a build succeeds right after a failed one, so a long green streak is silent.

### Deliberate break: no permission

On real AWS, give the Jenkins server a duty badge (a role) that allows only `sns:Publish` on the one topic, and try publishing to a different topic. Expected: an `AuthorizationError` / `AccessDenied` in the build log. That is least privilege (Session 9). **Tested on real AWS (2026-11-24):** with a role that allowed `sns:Publish` on one topic, publishing there returned a MessageId; publishing to another topic gave `AuthorizationError ... is not authorized to perform: SNS:Publish on resource ... because no identity-based policy allows the SNS:Publish action`; `sns:CreateTopic` gave the same error. (S3 says `AccessDenied` instead; SNS says `AuthorizationError`.)

### Optional: SonarQube and the plugin habit

SonarQube and its quality gate are optional here and we did not test them. A habit worth building now: **Manage Jenkins, Plugins, Installed plugins**, look at how many plugins have pending updates and which ones you no longer use. Our practice Jenkins had 75 plugins and no pending updates, because it was freshly built. A server that has run for a year will not look like that.

### Check yourself

- [ ] A failed build sent a `FAILED` message with a working link.
- [ ] A later green build sent `FIXED`, and the green baseline sent nothing.
- [ ] You know why the Jenkins badge should publish to one topic only.

### Cleanup

Delete the `alerts` job. On real AWS, delete the topic and the badge if nothing else uses them (an unused topic costs nothing, but an unused broad permission is a risk). Practice: they disappear with `docker compose down -v`.

---

## Part D: one shared binder for every conveyor (Episode 4)

**Goal:** put the notification code in one repository, pin each Jenkinsfile to a version, and see that a library change does not touch pinned pipelines.

Your library repository is `~/ci-lib` (made in "Before you start"), tagged `v1.0`. It contains `vars/notifyBuild.groovy`:

```groovy
def call(Map cfg = [:]) {
  def status = cfg.status ?: 'UNKNOWN'
  def line = "[${status}] ${env.JOB_NAME} #${env.BUILD_NUMBER} ${env.BUILD_URL}"
  echo line
  if (cfg.topic) {
    sh "aws sns publish --topic-arn '${cfg.topic}' --message '${line}'"
  }
}
```

The practice Jenkins already knows the library: **Manage Jenkins, System, Global Pipeline Libraries** shows `ci-lib`, default version `main`, source `/repos/ci-lib` (on a real Jenkins you add it yourself, with your Git URL).

Copy `lab_files/jenkinsfiles/Jenkinsfile.lib` into your repository as `Jenkinsfile.lib`, commit, and create a Pipeline job `lib` with Script Path `Jenkinsfile.lib`. The file starts with `@Library('ci-lib@v1.0') _` and calls `notifyBuild(...)` in `post { always { ... } }`.

### Run it

**Build Now**. Expected in the log:

```
Loading library ci-lib@v1.0
[SUCCESS] lib #1 http://localhost:8080/job/lib/1/
+ aws sns publish --topic-arn arn:aws:sns:us-east-1:000000000000:ops-alerts --message [SUCCESS] lib #1 ...
"MessageId": "..."
```

and the message reaches the "phone" queue from Part C. The `sh` line uses double quotes safely here because the string holds only a topic ARN and build information, no secrets (Session 17's quote rule still applies to anything secret).

### Change the library, and watch the pinned pipeline ignore it

Edit `~/ci-lib/vars/notifyBuild.groovy`: change `"[${status}] ..."` to `"BUILD RESULT: ${status} ..."`. Commit and tag it `v1.1`. Build `lib` again.

Expected: the log still says `Loading library ci-lib@v1.0` and the message keeps the old `[SUCCESS]` format. Pinning protects you: a change in the library cannot suddenly break a conveyor that did not ask for it.

Now change your Jenkinsfile to `@Library('ci-lib@v1.1') _`, commit, build. Expected: `Loading library ci-lib@v1.1` and the message `BUILD RESULT: SUCCESS lib #3 ...`. You updated one place (the library) and moved each conveyor deliberately by changing one line.

### Deliberate break: a version that does not exist

Change the line to `@Library('ci-lib@v9.9') _`, commit, build. Expected:

```
ERROR: Could not resolve v9.9
ERROR: No version v9.9 found for library ci-lib
Finished: FAILURE
```

Set it back to a real tag.

### Check yourself

- [ ] The log said `Loading library ci-lib@v1.0` and the message arrived.
- [ ] Changing `main` did not change the pinned pipeline; moving to `v1.1` did.
- [ ] You can read the `No version ... found` error and fix it.

### Cleanup (do not skip)

- Docker: `docker compose -f compose.yml down -v` from `lab_files/docker`, with the same `BOOKING_REPO` and `CI_LIB_REPO` variables. `docker image rm docker-jenkins` removes the image too.
- Real server: stop the instance, delete the webhook and its firewall rule, and delete any SNS topic or permission you created only for this lab.
- Keep `~/booking-service` and `~/ci-lib`: you use them again in Session 19.

---

## Final checklist for Session 18

- [ ] Part A: parameters, parallel stations, approval gate (0 executors held), conditional deploy, linter
- [ ] Part B: a commit started a build by itself; you know why the bell needs a token
- [ ] Part C: `FAILED` then `FIXED` messages with working links
- [ ] Part D: a pinned shared library, a new tag, and the unknown-version error
- [ ] Practice Jenkins and emulator removed (or the server stopped)

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `"agent" is not allowed in stage ... as it contains parallel` | `agent` on a stage that has `parallel` | Put `agent` on each parallel branch |
| No `Build with Parameters` button | The parameters appear only after the first run | Run once, then reload |
| Approval waits forever | Nobody pressed the button | Open the build, press Deploy; the `timeout` ends it after an hour |
| The build holds an executor while waiting | Top-level `agent any` | Use `agent none` at the top |
| `401 An access token is required` from `notifyCommit` | The safe default | Use a token (real server), or the practice setting |
| The hook runs but no build starts | Job has no Poll SCM trigger, or the URL does not match the job's repository URL | Tick Poll SCM (empty schedule) and make `url=` match exactly |
| `InvalidClientTokenId` for SQS in the emulator | Environment endpoint not used for SQS | Add `--endpoint-url http://floci:4566` |
| No `FIXED` message | The build before it did not fail | `fixed` needs a failure followed by a success |
| `No version vX found for library` | The tag does not exist | `git tag` in the library repo; push the tag |
| `Library ci-lib is not defined` | Library not configured in Jenkins | Add it in Manage Jenkins, System, Global Pipeline Libraries |

## Real webhook results (GitHub to a Jenkins on your laptop, 2026-11-24)

Setup we used, and a safe way to do it. A temporary **public** repository, the practice Jenkins with the **GitHub** plugin added, a freestyle job with **GitHub hook trigger for GITScm polling** (`com.cloudbees.jenkins.GitHubPushTrigger`) cloning the repository over HTTPS, and a free **Cloudflare quick tunnel** for the public address.

- **Do not put the whole Jenkins on the tunnel.** Anyone who can reach the login page can try passwords. We put a tiny nginx in front that forwards only `POST /github-webhook/` and answers `404` to everything else (`GET /` and `/login` gave `404`, `POST /script` gave `404`, a `GET` of the webhook path gave `403`), kept Jenkins itself on `127.0.0.1`, and used a random admin password. The tunnel and the repository were removed afterwards (the public address then answered `530`).
- **The ping:** adding the webhook sent a `ping`; GitHub's Recent Deliveries showed `200`.
- **A push starts a build by itself:** from the `git push` to build #1 starting took **about 11 seconds**. The build page said `Started by GitHub push by <your login>` (cause class `GitHubPushCause`), the log began with `Cloning the remote Git repository` and checked out the pushed commit. A second push, and the merge of a pull request later, rang the bell again: **six push deliveries, all `200`, three builds.**
- **Trap:** without the **GitHub** plugin the path `/github-webhook/` does not exist (Session 17's plugin list only has Git). The `Git` plugin's own bell is `/git/notifyCommit` (Part B2).
- A Jenkins API call that creates a job needs the **crumb from the same session cookie** (`curl -c cookiejar` then `-b cookiejar`), or you get `403`.
- **Not run:** the `githubNotify` step (Jenkins sending the build status back to GitHub through the `github-branch-source` plugin **was** tested for real, see the Session 31 guide), a webhook **secret**, a private repository.

## What we did not test

Everything ran on Jenkins 2.580.2 LTS in Docker with a local AWS emulator. The jobs were created through the Jenkins command line with the settings the browser forms would save; we did not click through the web pages, and the approval was done with the same URL the button uses. We did not run: the `notifyCommit` access-token configuration page, real AWS apart from SNS publishing with a role (tested), SonarQube and `waitForQualityGate`, Slack or email plugins, and the Stage View colours.

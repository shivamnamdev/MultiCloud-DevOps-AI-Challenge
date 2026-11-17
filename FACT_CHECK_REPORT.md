# Fact-check pass: DevOps course lab commands (2026-11-17)

Scope: the 50 fenced code blocks in sessions 00 to 33 (Python 18, Bash 13, YAML 9, Groovy 4, Dockerfile 3, others), plus the highest-risk facts from each batch.
Environment: macOS, Python 3.9, no Docker daemon run, no cloud accounts, no Terraform or shellcheck. So cloud, Docker and Kubernetes commands could **not** be executed.

## 1. Syntax checks (all blocks)
- Python (18): all parse (`ast`). Bash (13): all pass `bash -n`. YAML (9) and JSON (1): all parse.

## 2. Executed locally
| Session | What ran | Result |
|---|---|---|
| 07 | Disk and host script | runs |
| 14 | `ipaddress` CIDR script | correct (128 addresses; overlap check) |
| 15 | Lambda greeting handler with a fake event | correct response |
| 31 | `rooms-service` app and 2 pytest tests | 2 passed |
| 32 | `review-helper` with `FakeExpert` (injection line, phone scrubbed, empty list gives 422) | correct |
| 32 | `train.py` (made-up data) | precision 0.70, recall 0.83, gate (0.6) passes; writes `risk.joblib`, `risk.json` |
| 32 | model server `/health`, `/predict`, bad input | `{"cancel_risk": 0.87, "brain": "v1"}`, 422 on bad input |
| 33 | z-score detector | flags the spike (3 points in a row), ignores a flat series |
| 33 | restart helper with a stub `kubectl` | dry run, allow-list refusal, approve, rate limit and kill switch all work |

## 3. Could not run here
- Docker builds for Session 32, Terraform (27, 28), Ansible (29), Jenkins (17 to 19, 31), AWS, Azure and GCP commands.
- Terraform HCL (S27) only checked for syntax by eye; run `terraform fmt` and `validate` once.

## 3b. MCP server (Session 33), run in a `python:3.12-slim` Docker container (round 2)
A venv would not help: it reuses the interpreter it was made from (3.9 here). A throwaway container gave Python 3.12 with nothing installed on the Mac. A stdio client called the server with a stub `kubectl`.
| Check | `mcp<2` (FastMCP) | `mcp` 2.3.0 (MCPServer) |
|---|---|---|
| Tools listed (`list_pods`, `get_pod_logs`) | pass | pass |
| `list_pods("atithi")` | pass | pass |
| `list_pods("kube-system")` | refused | refused |
| `get_pod_logs` with `password=abc123` in the log | redacted, "UNTRUSTED LOG TEXT" prefix | same |
| Pod name `x; rm -rf /` | refused | refused |
**Finding:** a fresh `pip install "mcp[cli]"` now installs 2.x, where `from mcp.server.fastmcp import FastMCP` fails (renamed to `MCPServer`, import `mcp.server.mcpserver`). The script originally said "check docs". Now it explains both versions and the lab pins `mcp[cli]<2`. Only the import and class name differ.
Not tested: the `query_prometheus` tool (described in the script, not coded) and a real cluster with the read-only Role.

## 3c. Docker checks (round 3), run on the local Docker engine
| Session | What ran | Result |
|---|---|---|
| 22 | naive Dockerfile (`python app.py`) | builds and serves; prints the Flask development-server warning, runs as root |
| 22 | multi-stage, non-root Dockerfile with gunicorn | builds, serves `/health` and `/rooms`, `uid=10001(app)` |
| 31 | Dockerfile with `HEALTHCHECK` | builds, status becomes `healthy`, non-root |
| 22 | `--read-only --tmpfs /tmp --cap-drop ALL --security-opt no-new-privileges --memory 256m --pids-limit 100` | serves, but gunicorn 27 logs `Read-only file system: /home/app/.gunicorn` (control server). Script now warns |
| 21 | Postgres on a user network, volume, `psql` | **failed as written** (`Connection refused`: no wait for startup). Works with `pg_isready` loop; script fixed |
| 31 | `deploy.sh` in an Alpine container with the Docker socket, a local registry, three releases | first deploy, upgrade, broken release: rollback to the previous label, log lines correct, exit 1 |
Size findings (Session 22 chart): `python:3.12` 1.62 GB, `python:3.12-slim` 205 MB, our Flask image 214 to 228 MB; multi-stage gave no saving for a pure Python service (the old chart claimed about 60 MB). Script corrected: multi-stage helps when the build needs a compiler, and for Java or Go.
Not tested: Docker `ufw` bypass claim, `docker buildx` multi-platform, Trivy scan, GHCR push, the Session 22 Actions workflow, `kind`.

## 3d. Kubernetes checks (round 4), on a local `kind` cluster (kind 0.34, Kubernetes 1.37, kubectl 1.36, Helm 4.3)
Tools were downloaded into the scratchpad only; the cluster used its own kubeconfig and was deleted afterwards.
| Session | What ran | Result |
|---|---|---|
| 23 | kube-system pod list; Deployment, delete pod, scale, relabel a pod; `kind load docker-image` plus `imagePullPolicy: IfNotPresent` plus port-forward | all as scripted (self-healing, orphan pod after relabel, `/health` ok) |
| 24 | five sick pods | `ImagePullBackOff`, `Error` (exit 1), `OOMKilled` (137), `Pending` (`Insufficient cpu`), `Error` (127): matches the script |
| 24 | bad image rollout, `rollout undo`, good tag, history | as scripted; `rollout status` hangs on the bad image; undo prints a `last-applied` annotation warning |
| 24 | two namespaces, cross-namespace DNS, empty endpoints after a bad selector | as scripted; `get endpoints` prints a deprecation warning (EndpointSlice), note added |
| 25 | ConfigMap, Secret, LimitRange, ResourceQuota (`pods: 4`), probe, scale to 5 | 5th pod refused (`FailedCreate`); **`rollout restart` then stalls** because the quota has no room for the surge pod. Script now says to scale back first |
| 25 | PV, PVC (`Retain`), data survives a new pod, PV goes `Released`; default StorageClass `standard` creates a PV dynamically | as scripted |
| 25 | default-deny NetworkPolicy and allow rules | enforced on this kind version (reachable, blocked, reachable). Script no longer says local clusters may not enforce |
| 25 | `kubectl auth can-i` as a ServiceAccount; `helm create` plus `helm template` | work |
| 25 | Ingress with three paths via Traefik (Helm) | routes work. **Findings:** `ingress-nginx` was retired in March 2026, so the lab no longer uses it; the path prefix is passed unchanged (`/api/rooms/health` hits the service as that path, 404 for `rooms-service`). Both added to the script |
| 26 | `kube-prometheus-stack` install, ServiceMonitor with and without `release: monitoring`, PrometheusRule, firing alert in Alertmanager | label gotcha confirmed (no target without it; target appears 1 to 2 minutes after adding it). Alert `RoomsHighErrorRate` fired and reached Alertmanager. Grafana password command verified. Notes added: job label comes from the Service name, gunicorn multi-worker counters, noisy control-plane alerts on kind |
Not tested: GKE (Session 24 episode 4), Grafana panels in a browser, blackbox probe, burn-rate rules, Alertmanager routing to a receiver, `helm` v3 (the course may be run with either; install and `template` worked on v4), `metrics-server` and HPA, minikube.

## 4. Verified against docs (web)
- Terraform `use_lockfile`: added in 1.10; DynamoDB arguments deprecated but still working. Script text updated (S28).
- RDS `manage_master_user_password`: valid for `aws_db_instance`, excludes `password`; secret ARN at `master_user_secret[0].secret_arn`.
- `az storage account create --allow-blob-public-access false`, `--sku Standard_LRS`, `--kind StorageV2`: all valid. `az aks create --attach-acr`, `az acr build`: valid.
- `kind load docker-image` plus `imagePullPolicy: IfNotPresent`: correct.
- Jenkins: supports Java 17 or 21 on current releases; S17 note added.
- kube-prometheus-stack: ServiceMonitor must carry the chart's `release` label (value follows the Helm release name; check the rendered Prometheus object).
- MCP: `pip install "mcp[cli]"` and `from mcp.server.fastmcp import FastMCP` are the official SDK; the standalone `fastmcp` package is separate; Python 3.10+. S33 text updated.

## 5. Status of the remaining facts (final, 2026-11-17)

Verified by running or by reading current official docs (sections 3b to 3i above, and this list):
- GitHub Action versions and inputs, trivy-action, gitleaks flags, `.trivyignore` expiry: 3i. AWS provider major (6.x): 3f. Trivy flags: 3f, 3h, 3i.
- GKE Autopilot behaviour and flags: 3e (live run).
- Ansible install, collection names (`community.general.ufw`, `amazon.aws.aws_ec2`): 3g, plus the `aws_ec2` dynamic inventory run against the emulator on 2026-11-17: the tag filter `Env: dev` excluded the prod instance, `keyed_groups` gave `role_web` and `role_db`, config file name must end in `aws_ec2.yml`, needs boto3 and botocore. The key `tags.Role` is deprecated in favour of `ec2_tags.Role` (script updated).
- Grafana admin password step: 3d.
- Google Cloud free trial: 90 days and $300 credit for new customers, no billing until upgrade, not usable for Gemini API in AI Studio (matches S00).
- Azure DevOps free tier: one free Microsoft-hosted parallel job with 1,800 minutes a month, up to 10 free parallel jobs for public projects, and new private organizations may need to request the free grant (matches S30).
- AKS: `az aks create --attach-acr`, `--node-count`, `--generate-ssh-keys`, `--tier {free,standard,premium}` exist; `az aks update --attach-acr` exists and `az aks check-acr` verifies it; the script's commands are valid (not run: no Azure subscription).
- ECR lifecycle policy: rules need `tagStatus` and, for tagged images, a `tagPatternList` or `tagPrefixList` (not both); `imageCountMoreThan` keeps the newest N and `sinceImagePushed` expires by age; changes apply within 24 hours; preview first. The S22 sentence (keep the last twenty tagged, expire untagged after seven days) is achievable.
- GHCR from Actions: `permissions: packages: write` plus `GITHUB_TOKEN` with `docker/login-action` is the documented path (matches S22).
- Jenkins `sshagent(['credential-id'])`: step exists; private-key credentials only; the `ssh-agent` executable must exist on the agent (matches S31). Not run end to end.

Not applicable (the scripts deliberately avoid the claim, so there is nothing to verify): AWS free tier and NAT, ALB, RDS prices; Lambda and S3 limits and storage-class minimums; AKS pricing numbers; Azure free account terms; LLM provider SDK, model names and prices (S32 uses an interface with `FakeExpert` and tells students to use their own provider's SDK). These lines tell students to read the live pages, which stays correct as prices change.

Not verified at all (needs access I do not have, or is outside what can run locally): real AWS and Azure behaviour and billing, GitHub-hosted runs, GHCR pushes with a real token, webhooks, SonarQube, Docker Engine install steps (the scripts defer to the official docs), Standard-mode GKE, third-party Galaxy roles.


## 3e. GKE lab (Session 24), run LIVE on a real GCP project (us-central1, Autopilot)

Run on 2026-11-17 with gcloud 593.0.0 in an isolated scratchpad config. Everything created was deleted afterwards (cluster, load balancer, Artifact Registry repo, local images); a post-delete check found no forwarding rules, target pools, health checks, firewall rules, disks or instances left.

Measured:
- `create-auto` took about 7.5 min; cluster starts with 0 nodes; it also writes the kubeconfig entry itself. Delete took about 5.5 min and removed the load balancer too.
- First deploy: pods Pending about 2.5 min (Autopilot opens a node), EXTERNAL-IP about 3.5 min after apply.
- **ImagePullBackOff with `403 Forbidden`** on the first pull: in a new project the default Compute service account has no roles. Fix that worked: `gcloud artifacts repositories add-iam-policy-binding REPO --location=REGION --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/artifactregistry.reader`.
- Apple Silicon: image built with `--platform linux/amd64` ran fine (already covered in S22).
- Rolling update to a new tag, `rollout history` and `rollout undo` worked. `rollout undo` prints a warning about `last-applied-configuration`.
- Autopilot kept requests 250m/512Mi as written and added 1Gi ephemeral storage. A pod with no requests got a default CPU (loadgen).
- **metrics-server is preinstalled** on Autopilot (confirmed; `kubectl top pods` worked).
- **`kubectl autoscale --cpu-percent` is deprecated**: new form is `--cpu=50%`. Both forms worked on kubectl 1.36; script now uses the new one.
- HPA with load: CPU 121% then 2 to 5 replicas in about 40 s. After the load stopped: 5 to 3 after about 9 min, 3 to 2 after about 13 min (slow, staggered).
- Docs gap closed: deleting the cluster removed the Service's load balancer, forwarding rule and firewall rules without deleting the Service first.
- Side effect to remember: `gcloud auth configure-docker` edits `~/.docker/config.json` (adds a credHelpers line). Removed after the test.
- A tooling slip of mine: `kubectl run --requests` does not exist (cost a 6-minute idle wait, no effect on conclusions).

Script fixes applied (S24): auth plugin, `--location`, API enable, repo create + configure-docker, node service account role command and the 403 symptom, Autopilot defaults, `--cpu=50%`, timings, LB cleanup check. Trimmed to about 2,999 spoken words.

Not tested: Standard mode, Artifact Registry in another region, the console views, real billing amounts (not visible to me).

## 3f. Terraform (Sessions 27 and 28), run for real against the floci AWS emulator and in Docker

Terraform v1.17.2 (hashicorp/terraform image), AWS provider 5.100.0 and 6.73.0, emulator floci 2.4.0 (fresh container, separate from the author's old ones). No real cloud was used, so nothing billed.

S27 results (all matched the script):
- `local_file` lab: init, plan, apply; changing content gives `-/+ must be replaced`; deleting the file by hand gives `+ create`; destroy clean.
- AWS lab (VPC, `cidrsubnet` subnet, IGW, route table + association, security group, `for_each` ingress rules, `data.aws_ami`, instance, `merge` tags): `fmt`, `validate`, `plan -out`, `apply tfplan` (10 resources), second plan "no differences". `terraform console` gives `cidrsubnet("10.0.0.0/16", 8, 2)` = `10.0.2.0/24`.
- State: `state list`, `state show`; console tag change shows `~ update in-place` in plan; `plan -refresh-only` shows "Objects have changed outside of Terraform"; apply restores.
- Rename a resource: plan wants destroy + create; with a `moved` block: "has moved", 0 changes.
- `import` block: plan says "1 to import", apply imports, next plan clean. Variable `validation` error text appears. `lifecycle { prevent_destroy = true }` blocks destroy with "Instance cannot be destroyed". `terraform graph` works (needs Graphviz `dot` for PNG; not installed here).
- Script fixes: (1) the `count` removal claim was too absolute. Removing the middle item shifted items; for a field that can change in place Terraform updated in place and destroyed the last index; only replace-forcing fields recreate. Reworded. (2) Added that AWS provider is now on 6 and the lab passed on both 5 and 6.

S28 results:
- Bootstrap bucket with versioning, public access block, encryption: worked. `us-east-1` create-bucket without LocationConstraint worked.
- `backend "s3"` with `use_lockfile = true` and `-backend-config=file`: `init -migrate-state` moved local state into the bucket.
- Two concurrent applies: lock object `terraform.tfstate.tflock` appears; second apply fails with "Error acquiring the state lock" (HTTP 412) showing lock ID and Who. No DynamoDB needed. Lock object removed after the first apply. 4 object versions kept; `terraform state pull > backup.json` works.
- Modules: `modules/network` called twice (dev, staging), `init` loads both, plan 6 to add; bad CIDR stopped by `can(cidrhost(...))` validation. Renaming a resource inside the module planned 6 destroy + 6 add; a `moved` block inside the module made it 0 changes.
- `validate` passed for aws_db_instance (`manage_master_user_password`, `multi_az`, `deletion_protection`, `prevent_destroy`), ALB, target group, listener, launch template, ASG, EIP + NAT gateway, `assume_role`, `default_tags`, aws_eks_cluster, google_container_cluster (autopilot), azurerm_kubernetes_cluster, helm provider. `init -backend=false` + `validate` as in the pipeline snippet works.
- Trivy `config --severity HIGH,CRITICAL --exit-code 1` runs and reports findings (e.g. GCP master authorized networks), so the pipeline step works as described.

Open items from this round:
- GitHub Action pins in the course are behind: checkout v4 (latest v7.0.1), setup-terraform v3 (v4.0.1), aws-actions/configure-aws-credentials v4 (v6.3.0), trivy-action latest v0.36.0 (2026-11-17 check). Also docker/* and setup-python pins. To be handled in the GHCR/Actions round, with a "check the latest version" line.
- Not tested: real AWS behaviour (public IP, real ALB/RDS/NAT creation and cost), OIDC role trust for the pipeline, cost tools, policy as code, workspaces, `force-unlock`, the real EKS/GKE/AKS creation.

## 3g. Ansible (Session 29), run for real in Docker (control + web1, web2, db1)

Setup: Ubuntu 24.04 containers with systemd and sshd as targets; control node on Python 3.12 with `pipx install ansible-core` (core 2.21.6), `ansible-lint` 26.11.0. Everything local, no cloud.

Matched the script:
- `ansible.cfg` with `inventory = inventory.ini`; inventory with groups; `ansible-inventory --graph`; `ansible all -m ping` gives pong; `uptime` ad-hoc; `setup` with `filter=ansible_distribution*`.
- `apt` ad-hoc: first `changed: true`, second `changed: false`. `service` module: second run `changed: false`; with nginx stopped by hand on web2, only web2 changes. `shell` module shows `CHANGED` every time.
- `site.yml` (the S29 playbook): `--check --diff` shows the diff; on a fresh building the first run is `changed=4` (install, page, ufw rule, handler reload), the second `changed=0`; each page says which building served it.
- `--limit web1`, `--tags page`, wrong package name error ("No package matching 'nginxx' is available"), `--syntax-check`.
- Role from `ansible-galaxy init`, `template` with `app_port`/`server_name`, `-e app_port=8080` re-renders and reloads (health `ok` on 8080).
- Vault: `encrypt_string` + password file works; `no_log: true` hides the value, a task without it prints it; running without the vault password fails clearly.
- `ProxyJump` via `ansible_ssh_common_args` reaches a host through another (db1 via web1).

Script fixes (all applied):
1. `ansible-core` has no `community.general`, so the `ufw` task fails with "couldn't resolve module/action". Added `ansible-galaxy collection install community.general` to the lab.
2. With `host_key_checking = True`, the first Ansible connection fails with "Host key verification failed" unless the student has already run `ssh` once; added the reason to the lab step.
3. Drift on web2: editing only the page gives `changed=2` (page + reload handler), not `changed=1`. Fixed in the visual and voiceover.
4. Role lab: `curl /health` on port 80 returns 404, because Ubuntu's default nginx site wins. Verified: the Host header works, and removing `/etc/nginx/sites-enabled/default` makes plain curl return `ok`. Lab now says to add that task. (`default_server` in the template conflicts with the default site and breaks nginx reload.)
5. `ansible-lint` on the `ansible-galaxy init` skeleton fails on meta/tests files, and wants role variables prefixed (`var-naming[no-role-prefix]`, e.g. `nginx_app_port`). Added a note. Session length now about 2,991 words.

Container artefacts, not script bugs: my minimal image had no `ufw` (real Ubuntu cloud images have it); `ufw` could be installed and the rule added, but the firewall was left inactive.

Not tested: the `amazon.aws.aws_ec2` dynamic inventory (needs real or emulated EC2 instances), `ssh-copy-id` with a password prompt, Molecule, Galaxy roles from third parties, Ansible in a Jenkins/Actions pipeline, Windows targets.

## 3h. Jenkins (Sessions 17, 18, 19, 31), run for real in Docker

Setup: Jenkins 2.580.2 LTS (jenkins/jenkins:lts-jdk21, Java 21.0.13) with the plugins named in the scripts (git, workflow-aggregator, junit, credentials-binding, pipeline-stage-view, configuration-as-code, ssh-slaves, multibranch, timestamper, docker-workflow, ssh-agent...), Maven 3.9.9, Trivy 0.76.2, Docker CLI 27.5.1 (host daemon), AWS CLI against the floci emulator for SNS and S3, a local registry:2, and an SSH agent container. Everything local; nothing billed; all containers, volumes and images removed afterwards.

S17 (matches): the Jenkinsfile (Build, Test, Package, junit, archiveArtifacts) runs as "Pipeline script from SCM"; a failing test turns Test red and the log says `Stage "Package" skipped due to earlier failure(s)`; the `post failure` message prints. `sh "echo $TOKEN"` with double quotes prints the exact warning "A secret was passed to "sh" using Groovy String interpolation, which is insecure."

S18 (matches, one addition): parameters, environment, options (timeout, timestamps, disableConcurrentBuilds, buildDiscarder), `parallel` with `failFast` (5 s total for two 3 s branches), `when` skipping stages, `input` pausing the build and approval via the input URL, `input` under `agent none` holds no executor (busy 0; with top-level `agent any` it holds one). `pipeline-model-converter/validate` prints "Jenkinsfile successfully validated." and a precise error with a line number for a typo. Shared library `@Library('ci-lib@v1.0') _` with `vars/notifyBuild.groovy` loads from Git by tag; an unknown version fails with "No version v9.9 found for library ci-lib"; the SNS publish from the library reached a subscribed queue with the build link in the message.
- Added: declarative `parameters {}` only register after the first run (first build has no parameters; `-p` fails with "is not parameterized").

S19 (one claim corrected): `withCredentials` masking prints `****` and the length works (14 chars). Jenkins now also masks base64 and URL-encoded copies of the secret; reversed, spaced-out and hex copies print in full. The script said base64 breaks the masking; fixed to say reverse or hex. Script Console prints every credential in clear text for an admin. Setting built-in node executors to 0 leaves builds queued with "Waiting for next available executor" (text updated). Multibranch: `main` runs all stations and `feature/demo` skips Package and Deploy via `when`. SSH agent node with label works (`hostname` shows the workbench, user `jenkins`); the SSH session needs Java on its PATH (matches the script's `apt install openjdk-17-jre`; a base image that only sets PATH via Docker ENV fails with "java: command not found"). The backup script, run as written against S3, excludes workspace and caches and includes `secrets/master.key`, `credentials.xml` and the jobs (fresh backup about 175 MB mostly plugins and war).

S31 (one real failure fixed): Test, Build image, Scan, Push run in a Multibranch Pipeline; the Push stage runs only on `main`, the image is tagged with the 7-character commit id; the feature branch runs the first three stations and skips Push. The Scan stage as written FAILS on the first run: Trivy 0.76.2 found 48 HIGH/CRITICAL in `python:3.12-slim` (Debian 13.7), 47 with no fix yet and 1 fixable (zlib1g). `--ignore-unfixed` alone still failed (exit 1); adding `apt-get update && apt-get upgrade -y` to the final stage of the Dockerfile plus `--ignore-unfixed` made the scan pass (exit 0). Script updated (Dockerfile line, Jenkinsfile flag, explanation). First Trivy run downloads its database (about 1 minute).
- `agent any` ran a build on the SSH workbench when it was online. In the course setup this is expected, but it is worth knowing when workbenches lack Docker.

Not tested: GHCR itself (no token; the registry was local), GitHub webhooks and the GitHub plugin, SonarQube and `waitForQualityGate`, Slack and Email plugins, `agent { docker { image ... } }` (needs Docker paths that work when Jenkins itself is in a container), Windows agents, Jenkins on a real EC2 server, Config as Code beyond the basics, role-based authorization, HTTPS reverse proxy.

## 3i. GitHub Actions, DevSecOps tools (S20, S22, S28) and the S33 `query_prometheus` tool

GitHub Actions cannot be run without GitHub, so this round used actionlint, each action's own `action.yml`, and the real command-line tools in Docker.

Actions and workflows:
- `actionlint` (latest, in Docker) accepted all workflows from the scripts (CI, image push to GHCR with `permissions: packages: write`, matrix with `exclude`, `concurrency`, `workflow_dispatch` inputs, `needs` and `if`, `environment`, OIDC `id-token: write`, reusable `workflow_call` and its caller). It flagged exactly one thing, the deliberately unsafe `run: echo "${{ github.event.pull_request.title }}"`, and accepted the `env:` version, so the script's injection lesson is right.
- Pins in the scripts were 2 to 3 majors behind. Latest on 2026-11-17: checkout v7.0.1, setup-python v7.1.0, cache v6.1.0, upload-artifact v7.0.2, download-artifact v8.0.2, docker/metadata-action v6.2.0, docker/login-action v4.8.0, docker/build-push-action v7.4.0, setup-buildx-action v4.4.1, setup-terraform v4.0.1, aws-actions/configure-aws-credentials v6.3.0, trivy-action v0.36.0, gitleaks-action v3.0.0. For every input the course uses (python-version, cache, images, registry, username, password, push, tags, labels, role-to-assume, aws-region, name, path and others) I confirmed the input still exists in the latest `action.yml`, and that the moving major tags (`@v7`, `@v4`, `@v6`) exist. `checkout@v4` still runs on node20, the new majors on node24. Fix applied: all 10 pins in S20, S22 and S28 updated, plus a line that version numbers change and the releases page should be checked.
- Not run: the workflows on GitHub itself (needs a repo and runners), GHCR push with `GITHUB_TOKEN`, OIDC trust with a real AWS role.

DevSecOps tools (all matched the script):
- `gitleaks protect --staged` (gitleaks 8.30.1) found both planted secrets (access key and secret key), printed file and line, and exited 1. The newer form `gitleaks git --staged` behaves the same; mentioned in the script.
- `pip-audit -r requirements.txt` lists vulnerabilities for old pins (flask 0.12.2, jinja2 2.10, requests 2.19.0).
- `trivy fs --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 .` failed with 5 HIGH on the old pins and passed (exit 0) after upgrading to flask 3.1.3, jinja2 3.1.6 and requests 2.32.5.
- `.trivyignore` with a comment line and `CVE-ID exp:2026-12-31` suppresses the findings (exit 0); with `exp:2026-01-01` (already expired) the findings come back (exit 1). The YAML form `.trivyignore.yaml` is not read by default (needs `--ignorefile`), which the script does not use.

S33 `query_prometheus` (new code added to the script, 3 tools now in the hatch):
- Standard library only (urllib), URL from the `PROM_URL` environment variable (never an argument), query 1 to 300 characters, 10 second timeout, response read capped at 20,000 bytes and returned capped at 4,000 characters with a prefix saying it is data.
- Run through a real MCP client (SDK 1.x, Python 3.12 container) against a real Prometheus container: `up` returns data; `sum(rate(...[1m]))` returns a value; a syntax error returns Prometheus' own error text as data; a 301-character or blank query is rejected; a huge `{__name__=~".+"}` result is cut to 4,044 characters; an unreachable server gives `Name or service not known` without leaking the URL.
- S33 trimmed back to about 2,996 spoken words after the additions.

Cleanup: Prometheus container and network, the actionlint, gitleaks, trivy and Prometheus images and the trivy cache volume were removed.

## 3j. Session 31B (GitOps with Argo CD), tested on a local kind cluster (2026-11-17)

Argo CD 3.6.1 (latest release that day), Kubernetes 1.37 on kind, `argocd` CLI 3.6.1 in `--core` mode. Git source: a small in-cluster Git server (nginx + git-http-backend), because I did not push to any GitHub account. Everything deleted afterwards (cluster and its Git server).

Verified live:
- Plain `kubectl apply` of `install.yaml` fails with `applicationsets.argoproj.io ... Too long: may not be more than 262144 bytes`; `kubectl apply --server-side --force-conflicts` works. All pods Running in about a minute.
- First login: initial admin password from the `argocd-initial-admin-secret` (16 characters) or `argocd admin initial-password -n argocd`; UI through `kubectl port-forward svc/argocd-server 8443:443` answered HTTP 200; CLI `argocd login ... --insecure` worked.
- A new Application starts `OutOfSync` and `Missing`; after `argocd app sync` it is `Synced` and goes `Progressing` then `Healthy`; `CreateNamespace=true` created the wing; Argo CD adds the annotation `argocd.argoproj.io/tracking-id`.
- Auto-sync pickup time with default polling: 282 seconds for one commit (about 4m42s), so "about three minutes, sometimes longer" is the honest wording. Hard refresh and webhooks are the fast paths.
- With `automated` but `selfHeal` off: a hand `kubectl scale` to 5 stays, Application stays `OutOfSync`. With `selfHeal: true`: reverted in 2 to 3 seconds; a hand-deleted Service came back in 4 seconds.
- Bad release (image tag that does not exist): Application is `Synced` (matches Git) but `Progressing`; the new pod is `ImagePullBackOff` and the old pods keep serving. `git revert` plus push healed it in 1 second after the refresh. `argocd app rollback rooms 1` with auto-sync on fails with "rollback cannot be initiated when auto-sync is enabled". `argocd app history` lists the syncs.
- Kustomize `base` plus `overlays/dev` (1 replica, wing atithi-dev) and `overlays/prod` (3 replicas, wing atithi-prod) as two Applications: both Synced and Healthy. `argocd app diff rooms-prod --refresh` showed exactly the one-line image change.
- `AppProject` with allowed repo and `atithi-*` wings: an Application aimed at `kube-system` gets `InvalidSpecError: application destination server ... and namespace 'kube-system' do not match any of the allowed destinations in project 'atithi'`.
- `ApplicationSet` with a list generator created `rooms-dev` and `rooms-prod`, both Synced and Healthy.

Not tested: `prune` removing a manifest deleted from Git (my test command was blocked by a safety check on a `git rm` and I did not work around it; this is documented Argo CD behaviour and stated in the script as such), webhooks, SSO with Dex, private-repo deploy keys, the secrets tools (Sealed Secrets, External Secrets, SOPS), a GitHub-hosted config repo, a cloud cluster, Argo Rollouts and Flux. The Jenkins "update config vault" stage was described, not run; only the `sed`, commit and push lines were run.

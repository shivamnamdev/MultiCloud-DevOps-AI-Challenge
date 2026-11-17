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

## 5. Still to verify before recording (not checked)
Action versions (`checkout`, `setup-python`, `docker/*`, `setup-terraform`, Trivy); AWS provider major version; Trivy and gitleaks flags; ECR lifecycle fields; AWS free tier and NAT, ALB, RDS pricing; GKE Autopilot behaviour and flags; AKS pricing tiers and `az aks create` flags and VM sizes; Azure free account terms; Azure DevOps free parallel jobs; GHCR token scopes; Docker Engine install steps; Ansible install and collection names (`community.general.ufw`, `amazon.aws.aws_ec2`); `sshagent` plugin; Grafana admin password step for the chart version; LLM provider SDK, model names and pricing; Lambda limits; S3 limits and storage-class minimum durations.

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

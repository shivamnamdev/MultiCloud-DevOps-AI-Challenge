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

## 3e. GKE lab (Session 24), docs check only, NOT run live (no gcloud/GCP access yet)

Verified against Google's docs (now at docs.cloud.google.com):
- `gcloud container clusters create-auto NAME --region=REGION` is valid; `--location` is also accepted (region or zone). Only NAME is required.
- `get-credentials` docs now use `--location`; `gke-gcloud-auth-plugin` is mandatory for kubectl (`gcloud components install gke-gcloud-auth-plugin`).
- Autopilot: pods get default 0.5 vCPU / 2 GiB if unset; requests below minimum (250m CPU) are raised; billing is by Pod requests; nodes autoscale by pod count (can be zero).
- HPA: `kubectl autoscale ... --cpu-percent=50` needs a CPU request. Docs do not say metrics-server is preinstalled; the script's "already there on GKE" claim needs a live check.
- Artifact Registry: `gcloud artifacts repositories create REPO --repository-format=docker --location=REGION`, `gcloud auth configure-docker REGION-docker.pkg.dev`, tag `REGION-docker.pkg.dev/PROJECT/REPO/IMAGE:TAG`.
- Service type LoadBalancer creates a regional external passthrough Network Load Balancer; "wait a minute" for EXTERNAL-IP. Docs say nothing about leftovers after cluster delete.

Script fixes applied: plugin install, `--location` note, API enable command, repo create + configure-docker, Autopilot defaults/minimums, LB leftover check.

Still needs a live run: whether the default node service account can pull from Artifact Registry with no extra role, metrics-server on Autopilot, real EXTERNAL-IP timing, HPA scale-up under load, and what is left after `clusters delete`.

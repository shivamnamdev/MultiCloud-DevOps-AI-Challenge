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
- Docker builds (22, 31, 32), Kubernetes (23 to 26, 32), Terraform (27, 28), Ansible (29), Jenkins (17 to 19, 31), AWS, Azure and GCP commands.
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

# Kubernetes extras tested on a local kind cluster (27 November 2026)

Tools: kind v0.33.0 (checksum verified), kubectl client v1.36.1, node image Kubernetes v1.37.0, metrics-server v0.9.1 (with `--kubelet-insecure-tls`, needed on kind only). Cluster: 1 control plane + 3 workers (`kind-4nodes.yaml`). Everything was deleted afterwards.

| File | Test |
|---|---|
| `a-drain-pdb.yaml`, `a-emptydir.yaml` | cordon, drain, uncordon, PodDisruptionBudget |
| `b-toleration.yaml`, `b-nodeselector.yaml` | taints, tolerations, nodeSelector |
| `c-php-apache.yaml`, `c-hpa-run.sh` | HPA scale-up, scale-down stabilization window |
| `d-blue-green.yaml` | blue-green switch and canary by replica ratio on a plain Service |
| `e-sidecar.yaml`, `e-sidecar-job.yaml` | classic sidecar, native sidecar, sidecar in a Job |

Results are in `findings.md` (root of the course) under "Kind tests, 27 November 2026".

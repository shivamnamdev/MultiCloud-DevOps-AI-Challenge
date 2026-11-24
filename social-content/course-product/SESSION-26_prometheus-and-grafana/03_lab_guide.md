# Session 26 lab guide: Prometheus and Grafana

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in names, IPs, hashes and times.

| | |
|---|---|
| **Time** | Part A 15 min, Part B 30 min, Part C 45 min, Part D 45 min (the alert needs about 10 minutes of waiting) |
| **Cost** | Free on your laptop, but the monitoring stack is heavy: give Docker at least 6 GB of memory (our Docker had 7.7 GB and the cluster used about 2.2 GB with the stack running). Delete the cluster at the end. |
| **Skill check before you start** | Sessions 21 to 25: Docker networks, Deployments, Services, Helm. |

## Before you start

You need Docker, `kubectl`, `kind` and `helm`. We tested with Docker `29.8.2` (Docker Desktop, Mac, arm64), `kubectl` `v1.36.1`, `kind` `v0.33.0` (Kubernetes `v1.37.0`), Helm `v4.3.2`, chart `kube-prometheus-stack-93.4.0` (operator `v0.95.2`), Prometheus `3.16.0`, Alertmanager `0.35.0` and Grafana `13.3.1`.

Files are in `lab_files/`:

- `rooms-service/`: the `rooms-service` with a `/metrics` page (`prometheus_client`), a `BREAK=1` switch that makes `/` answer 500, and a Dockerfile.
- `prometheus.yml`: the two-job config from the script (Part B).
- `k8s/`: `rooms.yaml`, `servicemonitor.yaml`, `prometheusrule.yaml`.
- `dashboard.json`: a one-panel dashboard for the ConfigMap exercise.
- `stack-values.yaml`: lighter settings for a laptop. `stack-values-storage.yaml`: adds a volume claim for Prometheus' data.

Build the image once:

```bash
docker build -t atithi-rooms-metrics:1.0 lab_files/rooms-service
```

> **Mac users:** port `5000` on the Mac is taken by AirPlay Receiver (see the Session 22 guide). The Docker lab below publishes the app on **`5050`**.

---

## Part A: paper SLI and SLO (Episode 1)

No cluster needed. For `rooms-service` and `bookings-service`, write one SLI, one SLO and the error budget in minutes. The budget is `(1 − target) × minutes in the period`, and 30 days is `30 × 24 × 60 = 43,200` minutes:

| Target over 30 days | Allowed failure |
|---|---|
| 99.0 % | 432 minutes (about 7 hours) |
| 99.5 % | 216 minutes (about 3.6 hours) |
| 99.9 % | 43.2 minutes |
| 99.99 % | 4.3 minutes |

That is where the script's "about 43 minutes" comes from. Then write who looks at each SLO and what the team does when the budget is gone.

---

## Part B: the inspector, on your laptop (Episode 2)

**Goal:** let Prometheus read your service, ask it questions in PromQL, and watch `up` fall.

### B1. The service and its meters

```bash
docker network create appnet
docker run -d --name rooms --network appnet -p 5050:5000 atithi-rooms-metrics:1.0
for i in $(seq 200); do curl -s localhost:5050/ >/dev/null; done
for i in $(seq 20); do curl -s localhost:5050/rooms/$i >/dev/null; done
curl -s localhost:5050/nope >/dev/null
curl -s localhost:5050/metrics | grep -E '^http_requests_total|^http_request_duration_seconds_(count|sum)'
```

Expected (ours):

```
http_requests_total{method="GET",path="/",status="200"} 200.0
http_requests_total{method="GET",path="/rooms/<room_id>",status="200"} 20.0
http_requests_total{method="GET",path="unmatched",status="404"} 1.0
http_request_duration_seconds_count{path="/"} 200.0
...
```

Look at the second line: twenty different room numbers produced **one** series, labelled with the route template `/rooms/<room_id>`. That is the cardinality rule from the script: label by route, never by the real id. (The `/metrics` page itself is not counted, so scraping does not inflate the numbers.)

### B2. Prometheus reads it

```bash
docker run -d --name prom --network appnet -p 9090:9090 \
  -v "$PWD/lab_files/prometheus.yml:/etc/prometheus/prometheus.yml" prom/prometheus
sleep 20
curl -s localhost:9090/api/v1/targets | python3 -c "import sys,json; [print(t['labels']['job'], t['health'], t['scrapeUrl']) for t in json.load(sys.stdin)['data']['activeTargets']]"
```

Expected: `prometheus up http://localhost:9090/metrics` and `rooms up http://rooms:5000/metrics`. Open `http://localhost:9090` in a browser, then **Status → Targets**: both `UP`. (The container name `rooms` is the host name in the config, which is why both containers share a user-defined network.)

### B3. PromQL

Keep traffic flowing for a minute, a mix of good and not-found calls, then ask the questions. You can type them into the browser at `http://localhost:9090`, or use the API like we did:

```bash
end=$((SECONDS+45)); while [ $SECONDS -lt $end ]; do curl -s localhost:5050/ >/dev/null; curl -s localhost:5050/rooms/7 >/dev/null; curl -s localhost:5050/missing >/dev/null; sleep 0.1; done
q(){ curl -s --data-urlencode "query=$1" localhost:9090/api/v1/query | python3 -c "import sys,json; d=json.load(sys.stdin); print([(r['metric'], r['value'][1]) for r in d['data']['result']])"; }
q 'up'
q 'sum by (status)(rate(http_requests_total[1m]))'
q 'histogram_quantile(0.95, sum by (le)(rate(http_request_duration_seconds_bucket[1m])))'
q 'http_requests_total'
```

What we saw: `up` was `1` for both jobs. The rate by status was about `10.85` per second for `200` and `4.80` for `404`. The 95th percentile was about `0.0047` seconds (4.7 ms). And the plain `http_requests_total` returned **raw, ever-growing counters** (`458`, `278`, `259`), which is why you wrap a counter in `rate()`.

**The empty-answer trap.** The error-ratio query from the script:

```
sum(rate(http_requests_total{status=~"5.."}[1m])) / sum(rate(http_requests_total[1m]))
```

returned **an empty result, not zero**, while the service had no 5xx at all. (There is no 5xx series, so there is nothing to divide.) In an alert that is fine. In a Grafana stat panel it shows "No data". Add `or vector(0)` at the end (put brackets around the division first). We tested it on the healthy service: it returned `0.0`. When we turned on `BREAK=1` the same query returned `0.5` (half the calls were failing).

### B4. `up` goes to zero

```bash
docker stop rooms
sleep 35
q 'up'
```

Expected: `rooms` shows `0`, `prometheus` still `1`. About 35 seconds was enough for us (the scrape interval is 15 s).

### B5. Several workers, wrong counters

The script warns that each gunicorn worker keeps its own counters. We checked:

```bash
docker rm -f rooms
docker run -d --name rooms2 -p 5051:5000 atithi-rooms-metrics:1.0 gunicorn -b 0.0.0.0:5000 -w 2 app:app
sleep 3
for i in $(seq 30); do curl -s localhost:5051/ >/dev/null; done
for i in 1 2 3 4 5 6; do curl -s localhost:5051/metrics | grep '^http_requests_total{method="GET",path="/"'; done
docker rm -f rooms2
```

What we saw: after exactly 30 requests, all six reads said `17.0`, not `30`. Each read hit the same worker, which had seen 17 of the 30. Prometheus would graph a counter that is too low, or one that jumps as scrapes land on different workers. The lab image uses **one** worker (`-w 1`) for this reason. For several workers use the library's multiprocess mode (the script points to the docs; we did not run it).

Clean up: `docker rm -f prom rooms; docker network rm appnet`.

**Check yourself:**

- [ ] Both targets were `UP`, then `rooms` went to `0` when stopped.
- [ ] You can say why the query for the 95th percentile uses `_bucket` and `le`.
- [ ] You saw the empty result and fixed it with `or vector(0)`.

---

## Part C: the franchise kit and the screens (Episode 3)

**Goal:** install the whole control room with one command, then add your service to it.

### C1. The cluster, the image, and the stack

```bash
kind create cluster --name lab26
kind load docker-image atithi-rooms-metrics:1.0 --name lab26
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace \
  -f lab_files/stack-values.yaml --wait --timeout 600s
```

Expected: the install ended with `STATUS: deployed` in **2 minutes 46 seconds** for us (images had to be pulled). Check:

```bash
kubectl get pods -n monitoring
kubectl wait -n monitoring --for=condition=Ready pod/prometheus-monitoring-kube-prometheus-prometheus-0 --timeout=240s
```

Our pods: `alertmanager-...-0 2/2`, `monitoring-grafana-... 3/3`, `monitoring-kube-prometheus-operator 1/1`, `monitoring-kube-state-metrics 1/1`, `monitoring-prometheus-node-exporter 1/1` and `prometheus-...-0` (two containers). Note that the install can report success while the Prometheus pod is still `PodInitializing`, so wait for it as above.

**Where is Prometheus' data? Not on a volume, by default.**

```bash
kubectl get pvc -n monitoring
kubectl get pod prometheus-monitoring-kube-prometheus-prometheus-0 -n monitoring \
  -o jsonpath='{.spec.volumes[?(@.name=="prometheus-monitoring-kube-prometheus-prometheus-db")]}{"\n"}'
```

Expected (ours): `No resources found in monitoring namespace.` and `{"emptyDir":{},"name":"prometheus-monitoring-kube-prometheus-prometheus-db"}`. The first version of the script said the data sits on a PVC. In this chart it **does not** unless you ask: an `emptyDir` is wiped when the pod goes away. To keep it, add `lab_files/stack-values-storage.yaml` (a `storageSpec` with a `2Gi` claim) with a second `-f`. We tried that: a claim `prometheus-monitoring-kube-prometheus-prometheus-db-prometheus-monitoring-kube-prometheus-prometheus-0` appeared, `Bound` on class `standard`.

Reach the three web pages (each in its own terminal, or in the background):

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-alertmanager 9093:9093
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

### C2. The Grafana password

```bash
kubectl get secret -n monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode; echo
```

That is the script's command, and it worked for us. The chart's own install notes print a different one (`kubectl get secret --namespace monitoring -l app.kubernetes.io/component=admin-secret -o jsonpath="{.items[0].data.admin-password}" | base64 --decode`), which also worked. The user is `admin`. Change this password if the cluster is ever shared.

### C3. Put `rooms` in the stack, and meet the label trap

```bash
kubectl apply -f lab_files/k8s/rooms.yaml
kubectl rollout status deployment/rooms -n atithi
```

`lab_files/k8s/rooms.yaml` makes the namespace `atithi`, a Deployment `rooms` with two pods (limits and a readiness probe), and a Service named **`rooms`** with a port **named `http`** and the label `app: rooms`. The Service name matters: Prometheus builds the `job` label from it.

First the ServiceMonitor **without** the label the operator wants:

```bash
sed '/release: monitoring/d; s/^  labels:$/  labels: {}/' lab_files/k8s/servicemonitor.yaml | kubectl apply -f -
sleep 75
curl -s localhost:9090/api/v1/targets | python3 -c "import sys,json; print([(x['labels']['job'],x['health']) for x in json.load(sys.stdin)['data']['activeTargets'] if x['labels'].get('job')=='rooms'])"
```

Expected (ours): `[]`. After 75 seconds there was still **no `rooms` target**, and no error anywhere. Now apply the real file, `lab_files/k8s/servicemonitor.yaml`, which carries `release: monitoring`:

```bash
kubectl apply -f lab_files/k8s/servicemonitor.yaml
```

The target appeared **56 seconds** later, two of them (one per pod), `up`, at `http://10.244.0.12:5000/metrics` and `http://10.244.0.13:5000/metrics`, with labels `job=rooms`, `namespace=atithi`. We also read the rule from the other side: the Prometheus object has `serviceMonitorSelector: {matchLabels: {release: monitoring}}` and an empty namespace selector, so it accepts monitors with that label from any namespace.

### C4. Traffic, a panel query, and Grafana

Start some steady traffic from inside the cluster:

```bash
kubectl run load -n atithi --image=busybox:1.36 --restart=Never -- sh -c 'while true; do wget -qO- http://rooms:5000/ >/dev/null; wget -qO- http://rooms:5000/rooms/1 >/dev/null; wget -qO- http://rooms:5000/nothing >/dev/null 2>&1; sleep 0.2; done'
```

After a minute or so, the script's panel query `sum by (status)(rate(http_requests_total{namespace="atithi"}[5m]))` gave us `200: 9.6` and `404: 4.8` per second. `up{job="rooms"}` was `1` for both pods.

In the browser, open `http://localhost:3000` (user `admin`). We checked through Grafana's API that the Prometheus data source exists (`http://monitoring-kube-prometheus-prometheus.monitoring:9090/`), that there are **29 built-in dashboards** including **Kubernetes / Compute Resources / Namespace (Pods)**, and that a query sent through Grafana to Prometheus returned data. **We did not click in the Grafana screen**, so building your own panel in the UI is yours to do: *Dashboards → New → New dashboard → Add visualization → Prometheus*, paste the query above, and choose *Time series*.

**Dashboards as code.** The script says to keep dashboards in a ConfigMap. We tried it: a ConfigMap in the `monitoring` namespace with the label `grafana_dashboard: "1"` and a small dashboard JSON as its data. The dashboard showed up in Grafana's search on our first check, a few seconds after we created it.

```bash
kubectl create configmap atithi-rooms-dashboard -n monitoring --from-file=atithi-rooms.json=lab_files/dashboard.json
kubectl label configmap atithi-rooms-dashboard -n monitoring grafana_dashboard=1
```

**Check yourself:**

- [ ] You saw no target without the label, and a target with it.
- [ ] You can name where Prometheus' data lives in the default install.
- [ ] You ran the panel query and saw a number per status.

---

## Part D: the alarm desk (Episode 4)

**Goal:** make an alert fire for a real reason, find it at the alarm desk, silence it, and fix the cause.

### D1. What rings before you do anything

```bash
kubectl apply -f lab_files/k8s/prometheusrule.yaml
sleep 20
curl -s localhost:9090/api/v1/alerts | python3 -c "import sys,json; print(sorted(set((x['labels']['alertname'], x['state']) for x in json.load(sys.stdin)['data']['alerts'])))"
curl -s localhost:9093/api/v2/alerts | python3 -c "import sys,json; print(sorted(set(x['labels']['alertname'] for x in json.load(sys.stdin))))"
```

What we saw, on a healthy fresh kind cluster, **with nothing broken**:

- In Prometheus: `Watchdog` firing, `etcdInsufficientMembers` firing, and pending: `KubeControllerManagerInstanceUnreachable`, `KubeProxyInstanceUnreachable`, `KubeSchedulerInstanceUnreachable`, `NodeClockNotSynchronising`, `PrometheusMissingRuleEvaluations`, `TargetDown`, `etcdMembersDown`.
- In Alertmanager: `Watchdog` and `etcdInsufficientMembers`.

`Watchdog` is meant to always fire (the dead man's switch of the script). The others are noise on kind: the control-plane parts are not scraped from outside. That is the alert fatigue from Episode 4, on day one. Do not treat them as problems with your lab.

### D2. Break the service on purpose

`lab_files/k8s/prometheusrule.yaml` has this alert (read it, it is the script's):

```yaml
expr: sum(rate(http_requests_total{job="rooms",status=~"5.."}[5m])) / sum(rate(http_requests_total{job="rooms"}[5m])) > 0.05
for: 2m
labels: {severity: page}
annotations: {summary: "rooms errors above 5%", runbook_url: "https://example.com/runbooks/rooms-high-error-rate"}
```

Keep the `load` pod from C4 running, then break `/`:

```bash
kubectl set env deployment/rooms -n atithi BREAK=1
kubectl rollout status deployment/rooms -n atithi
```

Poll the alert state every 10 seconds (we did, with the API):

```bash
for i in $(seq 1 40); do sleep 10; curl -s localhost:9090/api/v1/alerts | python3 -c "import sys,json; a=[x['state'] for x in json.load(sys.stdin)['data']['alerts'] if x['labels']['alertname']=='RoomsHighErrorRate']; print(a[0] if a else 'inactive')"; done
```

What we saw, from the moment the broken pods were rolled out:

| Time | `RoomsHighErrorRate` |
|---|---|
| 0 to about 170 s | `inactive` |
| about **181 s** | **`pending`** |
| about **302 s** | **`firing`** |

Why so slow? The rule looks at a **5 minute** window, so the 5xx share has to climb above 5% over that window first (about 3 minutes). Then the `for: 2m` must pass. Plan for about five minutes. A 1 minute window would be faster and noisier.

At the alarm desk:

```bash
curl -s localhost:9093/api/v2/alerts | python3 -c "
import sys,json
for x in json.load(sys.stdin):
    if x['labels']['alertname']=='RoomsHighErrorRate':
        print(x['labels'], x['annotations'], x['status']['state'])"
```

Expected (ours): the labels held only `alertname` and `severity: page` (no `job` or `namespace`, because the expression sums them away), and the annotations had the `summary` and the `runbook_url`. Open `http://localhost:9093` to see the same.

### D3. Silence it

In the Alertmanager page use *Silence*. We did it with the API, matching `alertname=RoomsHighErrorRate` for one hour:

```bash
curl -s -X POST localhost:9093/api/v2/silences -H 'Content-Type: application/json' -d "{\"matchers\":[{\"name\":\"alertname\",\"value\":\"RoomsHighErrorRate\",\"isRegex\":false,\"isEqual\":true}],\"startsAt\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"endsAt\":\"$(date -u -v+1H +%Y-%m-%dT%H:%M:%SZ)\",\"createdBy\":\"lab\",\"comment\":\"maintenance practice\"}"
```

(`date -v+1H` is the Mac form. On Linux use `date -u -d '+1 hour' +%Y-%m-%dT%H:%M:%SZ`.) Expected: a `silenceID`. Afterwards, `?silenced=true&active=false` listed `RoomsHighErrorRate`, and the not-silenced list showed only `TargetDown`, `Watchdog` and `etcdInsufficientMembers`. The alert still fires in Prometheus. The silence only stops it from being sent on.

### D4. The runbook step: roll back

```bash
kubectl rollout undo deployment/rooms -n atithi
kubectl rollout status deployment/rooms -n atithi
kubectl get deploy rooms -n atithi -o jsonpath='{.spec.template.spec.containers[0].env}{"\n"}'
```

Expected: `deployment.apps/rooms rolled back` (with the usual warning about the `last-applied-configuration` annotation), and an empty `env`. The service was healthy again at once. **The alert took about 291 seconds to go back to `inactive`**, for the same reason as before: the 5 minute window is still full of old errors. A fixed system can look broken on the screens for several minutes. Write that in the runbook.

### D5. Not tested

The **blackbox exporter** probe of the public address and its certificate expiry (Scene 5), **burn-rate alerts** (Scene 4), **routing and grouping to chat or a pager**, **inhibition**, and **recording rules** were not run. We only used the default Alertmanager, with silences.

**Check yourself:**

- [ ] You saw `RoomsHighErrorRate` go pending, then firing, and can say what each wait was for.
- [ ] You saw it in Alertmanager with its runbook link.
- [ ] You silenced it, then rolled back, and watched it resolve.

---

## Clean up

```bash
pkill -f 'port-forward -n monitoring'
kubectl delete pod load -n atithi --wait=false
helm uninstall monitoring -n monitoring
kubectl get pvc -A
kubectl get crd | grep -c monitoring.coreos.com
kind delete cluster --name lab26
docker rm -f rooms rooms2 prom 2>/dev/null; docker network rm appnet 2>/dev/null
docker rmi atithi-rooms-metrics:1.0
```

What we found after `helm uninstall`:

- **With the storage values** the claim `prometheus-...-db-...-0` was **still there and `Bound`**, and its volume with it. Helm does not delete claims made by a StatefulSet. Delete them yourself (`kubectl delete pvc -n monitoring --all`), and on a cloud cluster this is a disk that keeps billing.
- **Without them** there was no claim at all.
- **10 custom resource definitions** (`*.monitoring.coreos.com`) **stay behind** after uninstall, and some Secrets did too (the Alertmanager ones). Deleting the cluster removes everything. On a real cluster, remove the CRDs deliberately, because deleting them deletes every monitor and rule in every namespace.

Deleting the cluster in a few seconds is the easy cleanup here.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| No `rooms` target in Prometheus | ServiceMonitor lacks `release: monitoring`, or its selector does not match the **Service's** labels, or the port name differs | Check labels first, then wait one to two minutes |
| Target `down` with "connection refused" | Wrong port name or number | Compare the Service port name with `endpoints: port:` |
| Stat panel says "No data" for an error ratio | No 5xx series exists, so the division is empty | `or vector(0)` |
| Counter looks too low | Several gunicorn workers, each with its own counters | One worker, or multiprocess mode |
| Alert never fires | The rate window is not yet full, or `job` does not match the Service name | Wait, and check `job` in the query |
| The stack install hangs | Not enough memory for Docker | Give Docker 6 GB or more, or lower the requests in `stack-values.yaml` |
| `kubectl port-forward` stops | The pod restarted | Run it again |
| Port 9090 or 3000 in use | Another container still running | `docker ps`, then remove it |

## Real GKE Autopilot results (2026-11-24; cluster deleted the same day)

Image pushed to Artifact Registry; Helm 4.3.2.

- **The stack does not install on Autopilot as it is.** The first `helm install` failed: `cannot patch resource "services" in API group "" in the namespace "kube-system"` (the chart's etcd, scheduler, controller-manager, kube-proxy and coredns Services) and `GKE Warden rejected the request ... hostPID / hostNetwork / hostPath volume proc` (the **node-exporter** DaemonSet). Autopilot hides those parts and forbids host access. Fix: run `helm uninstall monitoring -n monitoring`, then install again with an extra values file:
  ```yaml
  kubeEtcd: {enabled: false}
  kubeScheduler: {enabled: false}
  kubeControllerManager: {enabled: false}
  kubeProxy: {enabled: false}
  coreDns: {enabled: false}
  kubeDns: {enabled: false}
  nodeExporter: {enabled: false}
  ```
  (`-f lab_files/stack-values.yaml -f autopilot-values.yaml`). The second install was ready in **1m36s**.
- Targets (all `up`): `rooms` x2, `kube-state-metrics`, Grafana, the operator, Alertmanager, Prometheus, and the `apiserver`. No node-exporter or kubelet targets. Grafana 13.3.1 showed **19** built-in dashboards (29 on kind, because the hidden parts have no data).
- Panel query `sum by (status)(rate(http_requests_total{namespace="atithi"}[1m]))`: `200` about **9.2**, `404` about **4.4** per second. `up{job="rooms"}` was `1` for both.
- **Alert timing (load pod running, `BREAK=1` rolled out):** `pending` after **50 s**, `firing` after **161 s** (kind: 181 s and 302 s). The timing depends on how much traffic is already in the 5 minute window, so plan for two to five minutes.
- Alertmanager held the alert with labels `alertname`, `prometheus`, `severity` and annotations `runbook_url`, `summary`. A silence made through the API (`POST /api/v2/silences`) turned it `suppressed`. `kubectl rollout undo deployment/rooms -n atithi` brought back healthy pods.
- Prometheus data still sits on an `emptyDir` with this values file (no PVC); a real long-term setup needs `storageSpec` (see `stack-values-storage.yaml`), not run here.


## What we did not test

- **Real long-term storage** (`stack-values-storage.yaml` on a cloud disk), and **node-exporter and kubelet metrics on a managed cluster** (Autopilot blocks them; a Standard GKE or EKS cluster was not tried).
- **Clicking through Grafana.** We used its API (data source, built-in dashboard list, one query, a dashboard from a ConfigMap) and did not use the screens.
- **Blackbox probes, burn-rate alerts, Alertmanager routing to a receiver, grouping, inhibition, recording rules, Thanos, Mimir or Loki.**
- **Multi-process counters** (the library's multiprocess mode).
- **Any other Grafana version.** We used 13.3.1.

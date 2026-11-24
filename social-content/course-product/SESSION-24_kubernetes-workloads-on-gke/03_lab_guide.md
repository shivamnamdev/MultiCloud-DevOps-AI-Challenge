# Session 24 lab guide: Kubernetes workloads on GKE

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real, and the outputs shown are what we saw. Yours will differ in names, IPs and times.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 25 min, Part C 25 min, Part D 60 to 90 min (cluster creation and deletion alone take about 13 min) |
| **Cost** | Parts A to C: free (they run on your laptop). Part D: uses a real Google Cloud project. Autopilot bills by the CPU and memory your pods request, and the load balancer costs money while it exists. Do the cleanup in Part D the same day. |
| **Skill check before you start** | You can run `docker run`, read a YAML file, and you have done Session 23 (kubectl and a first pod). |

## Before you start

You need, for Parts A to C:

- Docker running (Docker Desktop, or Docker Engine on Linux).
- `kubectl` (Session 23) and `kind` for a local cluster. Check: `kubectl version --client` and `kind version`.

For Part D only:

- A Google Cloud project with billing enabled, the `gcloud` CLI, and the GKE auth plugin: `gcloud components install gke-gcloud-auth-plugin`.
- The `rooms-service` image from Session 22 on your laptop.

Create the practice cluster once and reuse it for Parts A to C:

```bash
kind create cluster --name lab24
kubectl get nodes
```

Expected: one node named `lab24-control-plane` with STATUS `Ready` (about 20 seconds to a minute).

> **Tip:** if you use more than one cluster, run `kubectl config current-context` before every destructive command. It must say `kind-lab24` for Parts A to C.

---

## Part A: five sick pods (Episode 1)

**Goal:** read a pod's status, `describe` events and exit code, and name the cause without guessing.

Save this as `sick-pods.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata: {name: sick-1-badimage}
spec:
  containers:
  - {name: app, image: "nginx:doesnotexist"}
---
apiVersion: v1
kind: Pod
metadata: {name: sick-2-exit1}
spec:
  containers:
  - {name: app, image: "busybox:1.36", command: ["sh","-c","exit 1"]}
---
apiVersion: v1
kind: Pod
metadata: {name: sick-3-oom}
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sh","-c","tail /dev/zero"]
    resources:
      limits: {memory: 32Mi}
---
apiVersion: v1
kind: Pod
metadata: {name: sick-4-cpu}
spec:
  containers:
  - name: app
    image: busybox:1.36
    command: ["sleep","3600"]
    resources:
      requests: {cpu: "100"}
---
apiVersion: v1
kind: Pod
metadata: {name: sick-5-nocmd}
spec:
  containers:
  - {name: app, image: "busybox:1.36", command: ["sh","-c","nosuchcmd"]}
```

Create them and wait two minutes:

```bash
kubectl apply -f sick-pods.yaml
kubectl get pods
```

Expected (after about two minutes):

```
NAME              READY   STATUS         RESTARTS      AGE
sick-1-badimage   0/1     ErrImagePull   0             111s
sick-2-exit1      0/1     Error          4 (69s ago)   111s
sick-3-oom        0/1     OOMKilled      4 (71s ago)   111s
sick-4-cpu        0/1     Pending        0             111s
sick-5-nocmd      0/1     Error          4 (64s ago)   111s
```

Now diagnose each pod with the same order, every time: **status, then `describe` Events, then logs, then exit code.**

```bash
kubectl describe pod sick-1-badimage     # read the Events at the bottom
kubectl describe pod sick-4-cpu
kubectl get pod sick-2-exit1 -o jsonpath='{.status.containerStatuses[0].lastState.terminated.exitCode}{"\n"}'
kubectl logs sick-5-nocmd
```

Fill in this table as you go. The answers we got are below it, so cover them first.

| Pod | Status | Exit code | The most important word in Events | Cause |
|---|---|---|---|---|
| sick-1-badimage | | | | |
| sick-2-exit1 | | | | |
| sick-3-oom | | | | |
| sick-4-cpu | | | | |
| sick-5-nocmd | | | | |

<details>
<summary>Answers</summary>

| Pod | Status | Exit code | Key word | Cause |
|---|---|---|---|---|
| sick-1-badimage | ErrImagePull, then ImagePullBackOff | none (never started) | `not found` | The tag does not exist: `docker.io/library/nginx:doesnotexist: not found` |
| sick-2-exit1 | Error (then CrashLoopBackOff) | 1 | `Exit Code: 1` | The program exited with an error |
| sick-3-oom | OOMKilled | 137 | `OOMKilled` | The container used more than its 32Mi memory limit and was killed (137 is 128 + signal 9) |
| sick-4-cpu | Pending | none | `FailedScheduling`, `Insufficient cpu` | `0/1 nodes are available: 1 Insufficient cpu`. No node has 100 CPUs, so the pod can never be placed |
| sick-5-nocmd | Error | 127 | `Exit Code: 127` | Command not found. `kubectl logs` shows `sh: nosuchcmd: not found` |

</details>

### Deliberate break: READY `1/2`

A pod's READY column counts containers. Prove it. Save as `two.yaml`:

```yaml
apiVersion: v1
kind: Pod
metadata: {name: two-trucks}
spec:
  containers:
  - {name: web, image: "nginx:alpine"}
  - {name: sidecar, image: "busybox:1.36", command: ["sh","-c","exit 1"]}
```

```bash
kubectl apply -f two.yaml
kubectl get pods
```

Expected: `two-trucks   1/2   Error   2 (17s ago)`. One of two containers is ready. Pods do not count the pod, they count the trucks inside it.

### Known quirk on kind

`kubectl logs <pod> --previous` can answer `unable to retrieve container logs for containerd://...` on a kind cluster, even though plain `kubectl logs <pod>` works. On a real cluster `--previous` is the right way to read the crashed container's last run. If it fails here, use plain `kubectl logs`.

### Check yourself

- [ ] You can name the status of every pod without looking.
- [ ] You can say why `sick-4-cpu` shows no exit code (it never started).
- [ ] You can explain why 137 means "killed", not "the program chose to exit".

### Cleanup

```bash
kubectl delete pod --all
kubectl get pods        # expect: No resources found in default namespace.
```

---

## Part B: a standing order, a bad release, a rollback (Episode 2)

**Goal:** create a Deployment, break a release on purpose, see that guests are protected, and roll back.

```bash
kubectl create deployment rooms --image=nginx:1.26-alpine --replicas=3 --dry-run=client -o yaml > rooms.yaml
kubectl apply -f rooms.yaml
kubectl rollout status deploy/rooms
kubectl get pods
```

Expected: `deployment "rooms" successfully rolled out`, and three pods `1/1 Running` named `rooms-<hash>-<id>`.

**Self-healing.** Delete one pod and look at the list straight away:

```bash
kubectl delete pod $(kubectl get pod -l app=rooms -o name | head -1)
kubectl get pods
```

Expected: still three pods, one of them only a few seconds old.

### Deliberate break: a bad image tag

`kubectl create deployment` named the container `nginx` (after the image), so that is the name to use:

```bash
kubectl set image deploy/rooms nginx=nginx:doesnotexist
kubectl get pods
kubectl rollout status deploy/rooms --timeout=20s
kubectl get deploy rooms
```

Expected:

```
rooms-5866578b77-sftwr   0/1     ImagePullBackOff   0   20s     <- the new pod is stuck
rooms-75bcb7d657-...     1/1     Running            0   31s     <- the three old pods still serve guests
...
error: timed out waiting for the condition
NAME    READY   UP-TO-DATE   AVAILABLE   AGE
rooms   3/3     1            3           31s
```

The rollout is stuck, but `AVAILABLE` stays 3. The Deployment will not remove an old pod until a new one is ready, so guests feel nothing. Note `--timeout=20s`: without it `rollout status` waits forever (and macOS has no `timeout` command to stop it for you).

### Fix: roll back

```bash
kubectl rollout undo deploy/rooms
kubectl rollout status deploy/rooms --timeout=60s
```

Expected: `deployment.apps/rooms rolled back`, then `successfully rolled out`. You will also see a warning that the resource was "previously managed with 'kubectl apply'" and that the `last-applied-configuration` annotation is not updated. That is normal for `rollout undo` on an applied object. For a permanent fix, put the right tag in `rooms.yaml` and `kubectl apply` it.

### Now release properly

```bash
kubectl set image deploy/rooms nginx=nginx:1.27-alpine
kubectl rollout status deploy/rooms --timeout=120s
kubectl rollout history deploy/rooms
kubectl get rs
```

Expected: pods are replaced one at a time (the status lines count `1 out of 3 new replicas have been updated`, then 2, then `old replicas are pending termination`). History after the earlier undo:

```
REVISION  CHANGE-CAUSE
2         <none>
3         <none>
4         <none>
```

Revision 1 is gone: when you undo to revision 1, Kubernetes re-labels it as revision 3. `kubectl get rs` shows three ReplicaSets, two at 0 desired and the active one at 3. Those old ReplicaSets are what make rollback possible.

**Optional (a standard command that we did not run in our test):** record why a release happened, so history says more than `<none>`:

```bash
kubectl annotate deploy/rooms kubernetes.io/change-cause="nginx 1.27 upgrade"
kubectl rollout history deploy/rooms
```

### Check yourself

- [ ] You saw `READY 3/3` and `AVAILABLE 3` while a bad release was stuck.
- [ ] You can say what `maxSurge` and `maxUnavailable` do, and why only one new pod appeared.
- [ ] You rolled back, then released a good tag.

### Cleanup

```bash
kubectl delete deploy rooms
```

---

## Part C: two wings and one name (Episode 3)

**Goal:** use namespaces to separate environments, call a service across them, and see what an empty endpoint list looks like.

```bash
kubectl create namespace dev
kubectl create namespace staging
for ns in dev staging; do
  kubectl create deployment rooms --image=nginx:alpine --replicas=2 -n $ns
  kubectl expose deployment rooms --port=80 -n $ns
done
kubectl get pods -A | grep rooms
```

Expected: two `rooms` pods in `dev` and two in `staging`, all `1/1 Running`. Same names, different wings.

**Call across wings** from a throwaway pod in `staging`:

```bash
kubectl run tmp -n staging --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- rooms.dev.svc.cluster.local
```

Expected: the nginx page (`<title>Welcome to nginx!</title>`). The name pattern is `<service>.<namespace>.svc.cluster.local`. From inside `dev`, plain `rooms` would be enough.

**See where the Service sends traffic:**

```bash
kubectl get endpoints rooms -n dev
kubectl get endpointslices -n dev
```

Expected: two pod IPs on port 80. `get endpoints` also prints `Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice`. That warning is expected on current Kubernetes. EndpointSlice is the newer object.

### Deliberate break: a wrong selector

```bash
kubectl patch svc rooms -n dev -p '{"spec":{"selector":{"app":"roomz"}}}'
kubectl get endpoints rooms -n dev
kubectl get endpointslices -n dev
```

Expected: `ENDPOINTS   <none>` and `<unset>`. There is no error message. The Service simply finds no pods, because the label does not match. This is the classic "nothing is happening" failure. Rule: when a Service has no endpoints, compare its `selector` with the pod labels (`kubectl get pods --show-labels`).

### Fix

```bash
kubectl patch svc rooms -n dev -p '{"spec":{"selector":{"app":"rooms"}}}'
kubectl get endpoints rooms -n dev
```

The two IPs are back.

### Check yourself

- [ ] You reached a Service in another namespace by its full name.
- [ ] You can explain why a wrong selector shows no error.
- [ ] You know where to look first when a Service answers nothing.

### Cleanup

```bash
kubectl delete namespace dev staging
kubectl get ns          # only default, kube-system, kube-public, kube-node-lease and local-path-storage remain
```

When Parts A to C are done and you do not need the practice cluster any more:

```bash
kind delete cluster --name lab24
```

---

## Part D: the real thing on GKE Autopilot (Episode 4)

**Goal:** run the same standing order on a real managed cluster, reach it from the internet, scale it automatically, and then delete everything.

> **Money and safety.** This part creates a billable cluster and a load balancer. Use a fresh or practice project, finish in one sitting, and do the cleanup at the end even if something fails midway. Replace `PROJECT_ID`, `REGION` (for example `us-central1`) and `PROJECT_NUMBER` with your own values. The project number is on the project's dashboard page. Never paste your real project ID into a public repo.

### D1. Prepare the project

```bash
gcloud config set project PROJECT_ID
gcloud services enable container.googleapis.com artifactregistry.googleapis.com
gcloud artifacts repositories create atithi --repository-format=docker --location=REGION
gcloud auth configure-docker REGION-docker.pkg.dev
```

Side effect to know: `configure-docker` edits `~/.docker/config.json` (adds a `credHelpers` line). Remove that line after the lab if you do not want it.

**Second run (November 2026, region `asia-south1`, Mumbai, a new project):** we used a short-lived token instead, which leaves your Docker config alone: `gcloud auth print-access-token | docker login -u oauth2accesstoken --password-stdin https://asia-south1-docker.pkg.dev`, and `docker logout asia-south1-docker.pkg.dev` at the end. **That token lasts one hour.** When we came back to the lab hours later, `docker push` said `error from registry: authentication failed`: log in again first.

### D2. Push your image

On an Apple Silicon Mac, build for the cloud's CPU type, as in Session 22. (Session 22's `lab_files/rooms-service/` has only `Dockerfile.*` variants and no plain `Dockerfile`: add `-f Dockerfile.full`, or use the file you built in that session.)

```bash
docker build --platform linux/amd64 -f Dockerfile.full -t REGION-docker.pkg.dev/PROJECT_ID/atithi/rooms-service:1.0.0 .
docker push REGION-docker.pkg.dev/PROJECT_ID/atithi/rooms-service:1.0.0
```

### D3. Create the cluster

```bash
gcloud container clusters create-auto atithi-lab --region=REGION
gcloud container clusters get-credentials atithi-lab --region=REGION
kubectl config current-context
```

It took about 7 to 8 minutes the first time, and **4 minutes 34 seconds** in `asia-south1` the second time. A new Autopilot cluster starts with 0 nodes, and `create-auto` writes your kubeconfig entry itself. The context should be `gke_PROJECT_ID_REGION_atithi-lab`. If it is not, stop and fix that before applying anything.

**Homebrew `gcloud` trap (tested):** `kubectl` needs `gke-gcloud-auth-plugin`. On a Homebrew install it was missing; `gcloud components install gke-gcloud-auth-plugin` worked, but the plugin landed in `/opt/homebrew/share/google-cloud-sdk/bin`, which is **not on your PATH**, so `kubectl` would still say the plugin is not found. Add that folder to your PATH (`export PATH=/opt/homebrew/share/google-cloud-sdk/bin:$PATH`, and put it in `~/.zshrc`).

### D4. Deploy

Save as `deploy.yaml` (put your image path in `image`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata: {name: rooms}
spec:
  replicas: 2
  selector: {matchLabels: {app: rooms}}
  template:
    metadata: {labels: {app: rooms}}
    spec:
      containers:
      - name: rooms
        image: REGION-docker.pkg.dev/PROJECT_ID/atithi/rooms-service:1.0.0
        ports: [{containerPort: 5000}]
        resources:
          requests: {cpu: 250m, memory: 512Mi}
          limits: {cpu: 500m, memory: 512Mi}
        readinessProbe: {httpGet: {path: /health, port: 5000}}
```

Save as `svc.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata: {name: rooms}
spec:
  type: LoadBalancer
  selector: {app: rooms}
  ports: [{port: 80, targetPort: 5000}]
```

```bash
kubectl apply -f deploy.yaml -f svc.yaml
kubectl get pods
kubectl get svc -w
```

What we measured the first time (`us-central1`): pods stay `Pending` for about 2.5 minutes (Autopilot is opening a node), and `EXTERNAL-IP` appears about 3.5 minutes after the apply. Press Ctrl+C when the IP shows, then open `http://EXTERNAL-IP/` in a browser. In the second run `curl http://EXTERNAL-IP/` returned `Atithi rooms-service` and `/health` returned `ok`, both with status 200.

### Deliberate break you should expect: `ImagePullBackOff` with `403 Forbidden`

In a new project the nodes' default service account has no roles, so the first image pull can fail. In our second run both pods sat in `ImagePullBackOff` until we applied the fix below (we came back to them hours later, so the exact `403` text had already left the event list; the first run recorded it):

```bash
kubectl get pods
kubectl get events --sort-by=.lastTimestamp | tail
```

Look for `403 Forbidden` in the events. Fix: let the nodes read the registry (the same lesson as Session 9, who may do what):

```bash
gcloud artifacts repositories add-iam-policy-binding atithi --location=REGION \
  --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
  --role=roles/artifactregistry.reader
kubectl rollout restart deploy/rooms
```

Both pods were `Running` about 45 seconds after the grant and restart. (`PROJECT_NUMBER` is `gcloud projects describe PROJECT_ID --format="value(projectNumber)"`.)

### D5. Roll out, roll back, then scale

Rolling update and rollback work exactly as in Part B (build and push a `1.0.1` tag, then `kubectl set image deploy/rooms rooms=REGION-docker.pkg.dev/PROJECT_ID/atithi/rooms-service:1.0.1`, then `kubectl rollout undo deploy/rooms`).

**A real bad release (second run, by accident):** our push of `1.0.1` failed (the token had expired), but we ran `kubectl set image` anyway. The rollout stalled with `1 out of 2 new replicas have been updated`, the old pod kept serving, and `kubectl rollout status --timeout=240s` ended with `error: timed out waiting for the condition`. `kubectl rollout undo deploy/rooms` fixed it, and the Deployment's image was back to `1.0.0`. This is exactly the Part B lesson on a real cluster.

Now autoscale. Metrics server is already installed on Autopilot, so `kubectl top pods` works with no setup:

```bash
kubectl autoscale deployment rooms --cpu=50% --min=2 --max=5
kubectl get hpa
```

On older kubectl versions the flag is `--cpu-percent=50`. Both work today, but `--cpu=50%` is the new form.

Create load. Save as `loadgen.yaml` (replace `rooms` with the Service name if you changed it):

```yaml
apiVersion: v1
kind: Pod
metadata: {name: loadgen}
spec:
  restartPolicy: Never
  containers:
  - name: loadgen
    image: busybox:1.36
    command: ["sh","-c","while true; do wget -q -O- http://rooms > /dev/null; done"]
    resources:
      requests: {cpu: 100m}
```

```bash
kubectl apply -f loadgen.yaml
kubectl get hpa -w
```

What we saw the first time: CPU at 121 percent, then replicas went from 2 to 5 in about 40 seconds. **How hard you push decides the numbers.** In the second run one load pod gave only `cpu: 31%/50%` and the replicas stayed at 2. With three load pods the HPA showed `57%/50%` and the Event `SuccessfulRescale ... New size: 3; reason: cpu resource utilization (percentage of request) above target`. If your HPA does not move, add more load pods (`loadgen2`, `loadgen3`). After stopping the load (`kubectl delete pod loadgen`), the replicas came back down slowly: 5 to 3 after about 9 minutes and 3 to 2 after about 13. Scale-down is slow on purpose, so a brief dip in traffic does not make Kubernetes throw capacity away. You do not need to wait for it. Go straight to the cleanup.

### Cleanup (do not skip)

```bash
kubectl delete -f svc.yaml          # optional: deleting the cluster also removes the load balancer
gcloud container clusters delete atithi-lab --region=REGION
gcloud artifacts repositories delete atithi --location=REGION
```

Deleting the cluster took about 5 to 6 minutes (6 minutes 16 seconds in the second run). Then check that nothing is left that could bill you:

```bash
gcloud compute forwarding-rules list
gcloud compute target-pools list
gcloud compute health-checks list
gcloud compute firewall-rules list --filter="name~gke"
gcloud compute disks list
gcloud compute instances list
gcloud artifacts repositories list
```

Every list should be empty (or contain only things that were there before the lab). **Tooling:** `_lab_tools/gcp/gcp_leftovers.sh` runs all of these checks (read-only), and `_lab_tools/gcp/gcp_cleanup_atithi.sh` plans, and with `--yes` deletes, clusters, Artifact Registry repos, Cloud Run services and buckets whose names start with `atithi`.

**Do not leave the cluster over lunch.** In our second run the session paused after the deploy and the cluster and load balancer stayed up for about 10 hours before we deleted them. The cost was small, but it is billed all the time. Also remove local copies of the image if you want the space back (`docker image rm ...`).

### Check yourself

- [ ] You opened the app from the internet at the load balancer's IP.
- [ ] You fixed the `403 Forbidden` pull error (or understand why it did not happen in your project).
- [ ] You saw the HPA add pods under load.
- [ ] The cleanup checks above all came back empty.

---

## Final checklist for Session 24

- [ ] Part A: five pods diagnosed, with status, exit code and cause written down
- [ ] Part B: a bad release did not hurt `AVAILABLE`, and you rolled back
- [ ] Part C: a call across namespaces worked, and a wrong selector showed `<none>`
- [ ] Part D: deployed to GKE, scaled, and the project is clean again
- [ ] `kind delete cluster --name lab24` done

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `kubectl` talks to the wrong cluster | Several contexts | `kubectl config get-contexts`, then `kubectl config use-context NAME` |
| `rollout status` never returns | The new pods cannot start | Add `--timeout=...`, then `kubectl describe pod` on the new pod |
| `logs --previous` says `unable to retrieve container logs` | kind quirk | Use plain `kubectl logs` |
| Pod stays `Pending` on GKE for a few minutes | Autopilot is creating a node | Wait up to about 3 minutes, then `kubectl describe pod` |
| `ImagePullBackOff` and `403` on GKE | Nodes cannot read Artifact Registry | The `add-iam-policy-binding` command in D4 |
| `gke-gcloud-auth-plugin` not found | Auth plugin missing | `gcloud components install gke-gcloud-auth-plugin` | (on Homebrew also add `/opt/homebrew/share/google-cloud-sdk/bin` to PATH) |
| `docker push` says `authentication failed` hours after login | the access token lasts 1 hour | log in to the registry again |
| Service has `<none>` endpoints | Selector does not match labels | Compare `kubectl get svc -o yaml` with `kubectl get pods --show-labels` |

## What we did not test

Parts A to C were run on kind 0.34 (Kubernetes 1.37) with kubectl 1.36. Part D was run twice on live GKE Autopilot: first in `us-central1`, then in November 2026 in `asia-south1` on a new project (GKE 1.36.4). **Not re-measured in the second run:** the time the pods stay `Pending`, the time to the external IP, the exact `403` text, and the HPA scale-down delay (those numbers come from the first run). Not tested: GKE Standard mode, other regions, and the real bill amount; check the billing page in your own project for the true cost.

# Session 23 lab guide: Kubernetes architecture

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in names, IPs, hashes and times.

| | |
|---|---|
| **Time** | Part A 10 min, Part B 20 min, Part C 30 min, Part D 30 min, plus 10 min of waiting in the optional node-failure exercise |
| **Cost** | Free. The cluster runs inside Docker on your laptop and needs a few GB of memory. Delete it at the end. |
| **Skill check before you start** | You did Sessions 21 and 22 (containers, the `rooms:slim` image) and can read YAML. |

## Before you start

You need Docker, `kubectl` and `kind`. Check:

```bash
docker version --format '{{.Server.Version}}'
kubectl version --client
kind version
```

We tested with Docker `29.8.2` (Docker Desktop, Mac, arm64), `kubectl` `v1.36.1`, `kind` `v0.33.0`, which created Kubernetes `v1.37.0` nodes running `containerd` 2.3.4. If you do not have `kind`, install it from its official page (kind.sigs.k8s.io). We downloaded the release binary and checked its SHA-256 against the published value.

You also need the `rooms:slim` image from the Session 22 guide (`Dockerfile.slim`). Check: `docker images rooms:slim`.

Files for this guide are in `lab_files/`: `kind-3nodes.yaml`, `rooms-pod.yaml`, `two-containers.yaml`, `watch-node-failure.sh`.

> **Mac users:** the script's last lab uses `kubectl port-forward pod/rooms 8080:5000`. That is fine on a Mac, because the forward uses local port `8080` and the pod's port `5000`. (Port `5000` on the Mac itself belongs to AirPlay Receiver, but the forward does not touch it.)

---

## Part A: feel the pain first (Episode 1)

**Goal:** see exactly what plain Docker does not do for you.

```bash
for i in 1 2 3 4 5; do docker run -d --name w$i nginx:alpine; done
docker kill w3
docker ps --filter name='^w[1-5]$' --format '{{.Names}} {{.Status}}' | sort
```

Expected (ours): `w1`, `w2`, `w4`, `w5`, all `Up`. Four are left, and nothing brings `w3` back. Clean up: `docker rm -f w1 w2 w3 w4 w5`.

### A2. What `--restart unless-stopped` really does (a correction to the first script)

The first version of the script said this flag brings back a killed truck. We tested three cases:

```bash
# 1. killed with docker kill
docker run -d --name r1 --restart unless-stopped nginx:alpine
docker kill r1; sleep 5
docker ps -a --filter name=r1 --format '{{.Names}} {{.Status}}'

# 2. the app itself crashes (exit code 1)
docker run -d --name r2 --restart unless-stopped alpine sh -c 'sleep 3; exit 1'
sleep 9
docker ps -a --filter name=r2 --format '{{.Names}} {{.Status}}'
docker inspect r2 --format 'restarts={{.RestartCount}}'

docker rm -f r1 r2
```

What we saw:

- **`docker kill`:** `r1 Exited (137) 5 seconds ago`, `restarts=0`. **Not brought back.** Docker treats a `docker kill` like a manual stop.
- **A crash:** `r2 Up 2 seconds` and `restarts=2` after 9 seconds. **Brought back, again and again.**

So the flag helps with crashes, on this one machine only. It does nothing for a machine that is gone, which is the real point of the episode.

(We also tried `docker exec r3 sh -c 'kill -9 1'` on an nginx container. Nothing happened: a process cannot kill PID 1 of its own container with a signal from inside. Do not use that to simulate a crash.)

**Check yourself:** you can say what a restart policy fixes and what it cannot.

---

## Part B: look inside the command (Episode 2)

**Goal:** make a cluster with a control plane and two nodes, and find every part the script names.

Create the cluster from the file in `lab_files/`:

```bash
kind create cluster --name lab23 --config lab_files/kind-3nodes.yaml
kubectl config current-context
kubectl get nodes -o wide
```

The file asks for one `control-plane` and two `worker` nodes. Creating took about 21 seconds for us. Expected: context `kind-lab23`, and three nodes, all `Ready`, version `v1.37.0`, runtime `containerd://2.3.4`. (If you only want one node, `kind create cluster --name lab` as in the script works too. You will not be able to do the node-failure exercise on it.)

### B1. The parts, by name

```bash
kubectl get pods -n kube-system -o wide | awk '{print $1,$2,$3,$7}' | column -t
```

Ours:

```
coredns-...-8qth7                             1/1  Running  lab23-control-plane
coredns-...-f7tcf                             1/1  Running  lab23-control-plane
etcd-lab23-control-plane                      1/1  Running  lab23-control-plane
kindnet-56mk6                                 1/1  Running  lab23-worker2
kindnet-crpsp                                 1/1  Running  lab23-worker
kindnet-n5g95                                 1/1  Running  lab23-control-plane
kube-apiserver-lab23-control-plane            1/1  Running  lab23-control-plane
kube-controller-manager-lab23-control-plane   1/1  Running  lab23-control-plane
kube-proxy-...                                1/1  Running  (one on each node)
kube-scheduler-lab23-control-plane            1/1  Running  lab23-control-plane
```

All four control-plane parts (`kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`) run on the control-plane node. `kube-proxy` and `kindnet` run on **every** node. `kindnet` is not in the script's list: it is kind's network plugin (the CNI), the thing that gives each pod an address.

### B2. A node's capacity

```bash
kubectl describe node lab23-worker | sed -n '/^Capacity/,/^System Info/p'
kubectl describe node lab23-worker | grep -A6 'Non-terminated'
```

We saw `cpu: 12`, `memory: 8124256Ki` and `pods: 110` under **both** `Capacity` and `Allocatable`. In kind they are equal. (On a managed cluster such as GKE they differ, as the script says.) All kind nodes also report the laptop's Docker VM total, not a slice of it, because they are just containers on it. The pod list on a fresh worker showed only `kindnet` and `kube-proxy`.

### B3. Optional: what a dead node looks like (10 minutes of waiting)

First a Deployment with four pods:

```bash
kubectl create deployment rooms --image=nginx:alpine --replicas=4
kubectl rollout status deployment/rooms
kubectl get pods -o wide
```

Then run the helper (it stops `lab23-worker2` and reports every 10 seconds for about 8 minutes):

```bash
./lab_files/watch-node-failure.sh
```

What we saw (times from the moment of `docker stop`):

| Time | Node | The two pods on that node |
|---|---|---|
| +10 s to +41 s | `Ready` | `Running` |
| **+51 s** | **`NotReady`** | still `Running` (a stale status) |
| +51 s to +345 s | `NotReady` | still `Running` |
| **+356 s** | `NotReady` | **`Terminating`**, and **two new pods** `Running` on the other worker |
| +366 s onwards | `NotReady` | old pods stay `Terminating` (the node cannot confirm) |

So: about **50 seconds** for the cluster to mark the node `NotReady`, then about **five more minutes** before the pods are replaced elsewhere. The five minutes look like the default Kubernetes wait of 300 seconds before pods are evicted from an unreachable node. We did not check that setting on the pods, and we did not try changing it. After `docker start lab23-worker2` the node became `Ready`, the stuck old pods disappeared, and **all four pods ended up on `lab23-worker`**. Nothing moved back to the returning node by itself.

Notice the whole story: nobody typed a command to heal anything.

### B4. What the control plane going away does

```bash
IP=$(kubectl get pods -o wide --no-headers | awk 'NR==1{print $6}')
docker stop lab23-control-plane
kubectl get pods --request-timeout=4s
docker exec lab23-worker curl -s -m3 -o /dev/null -w "pod $IP answers: %{http_code}\n" http://$IP
docker start lab23-control-plane
```

Expected (ours): `kubectl` says `The connection to the server 127.0.0.1:... was refused`, and the pod still answers **200** from the worker, with the control plane stopped. After `docker start`, wait until `kubectl get nodes` works again (under a minute).

In a first attempt we also stopped one nginx container directly on the worker with `crictl stop`, while the control plane was down. The kubelet restarted it on its own: the pod showed `RESTARTS 1` after the control plane came back. So the resident manager does not need reception to restart a truck in a bay it already runs. What we did **not** do is prove that a pod deleted while the control plane is down is *not* replaced. `kubectl` cannot delete anything at that moment, so it is obvious but untested.

**Check yourself:**

- [ ] You can point to the four control-plane parts and the two things that run on every node.
- [ ] You saw a pod answer while the control plane was off.
- [ ] You can say, from the table, how long a dead node takes to be noticed and to be replaced.

---

## Part C: desired state, objects and labels (Episode 3)

**Goal:** watch the reconciliation loop work, read an object's shape, and meet the label trap.

Delete the B3 Deployment first if it still exists: `kubectl delete deployment rooms`.

### C1. Pod mara, naya aaya

```bash
kubectl create deployment rooms --image=nginx:alpine --replicas=3
kubectl rollout status deployment/rooms
kubectl get pods -o wide --show-labels | awk '{print $1,$2,$3,$7,$NF}' | column -t
```

Expected: three pods, `Running`, spread over the workers, each with labels `app=rooms,pod-template-hash=...`. Now delete one and watch:

```bash
P=$(kubectl get pods -o name | head -1)
kubectl delete $P --wait=false
for i in 1 2 3 4; do sleep 1; kubectl get pods --no-headers | awk '{print $1,$3}' | tr '\n' ';'; echo; done
kubectl get events --sort-by=.lastTimestamp | tail -6 | cut -c1-140
```

What we saw: the first line already had the old pod as `Completed` (nginx shut down cleanly in under a second, so you may miss `Terminating`) and a **new pod `Running`**, still three in total. The events show the chain: `Killing` (stop the old container), `SuccessfulCreate` from the **ReplicaSet** (create a pod), `Scheduled` (the allocation officer picked a node), then the kubelet's `Created` and `Started`. That is Scene 4 of Episode 2, live. (The new pod started at once because that node already had the nginx image. On a node without it you also see `Pulling`.)

### C2. Scale, and break the label

```bash
kubectl scale deployment rooms --replicas=5
kubectl get deployment rooms
P=$(kubectl get pods -o name | head -1 | cut -d/ -f2)
kubectl label pod $P app=other --overwrite
sleep 3
kubectl get pods --show-labels --no-headers | awk '{print $1,$2,$3,$NF}' | column -t
kubectl get deployment rooms
```

Expected (ours): `rooms 5/5 ... 5 5`, then after relabelling, **six** pods: the relabelled one now says `app=other` and the Deployment started a new pod to make five again. The Deployment no longer counts the relabelled pod, and nothing tells you. (That orphan keeps running until you delete it.) Clean up: `kubectl delete pod $P; kubectl delete deployment rooms`.

### C3. `create`, `apply`, `replace`, `diff`

```bash
kubectl run rooms --image=nginx:alpine --dry-run=client -o yaml > rooms-pod.yaml
cat rooms-pod.yaml
kubectl create -f rooms-pod.yaml
kubectl create -f rooms-pod.yaml
kubectl apply -f rooms-pod.yaml
kubectl delete pod rooms
kubectl replace -f rooms-pod.yaml
kubectl apply -f rooms-pod.yaml
sed -i.bak 's/image: nginx:alpine/image: nginx:1.27-alpine/' rooms-pod.yaml
kubectl diff -f rooms-pod.yaml | grep -E '^[+-] '
kubectl apply -f rooms-pod.yaml
```

What we saw, line by line:

- The generated YAML has `apiVersion: v1`, `kind: Pod`, a `metadata` with `labels: {run: rooms}`, a `spec`, plus `resources: {}` and `status: {}` that `--dry-run` adds. It is a starting point, not a finished file.
- First `create`: `pod/rooms created`. Second `create`: `Error from server (AlreadyExists): ... pods "rooms" already exists`.
- `apply` on the existing pod: a **warning** that it is "missing the `kubectl.kubernetes.io/last-applied-configuration` annotation" (because the pod was made with `create`, not `apply`), and `pod/rooms configured`. It worked, and patched the annotation.
- `replace` when the pod is gone: `Error from server (NotFound)`. Then `apply` creates it: `pod/rooms created`.
- `diff` printed `-  generation: 1` / `+  generation: 2` and `-  - image: nginx:alpine` / `+  - image: nginx:1.27-alpine`. Then `apply` said `pod/rooms configured`.

Clean up: `kubectl delete pod rooms`.

### C4. `explain` and `api-resources`

```bash
kubectl explain pod.spec.containers.imagePullPolicy | head -8
kubectl api-resources | grep -E '^(replicasets|deployments|pods|services) '
```

Expected: `explain` shows `KIND: Pod`, `VERSION: v1`, the field, and the allowed values `Always`, `IfNotPresent`, `Never`. `api-resources` shows `pods po v1`, `services svc v1`, `deployments deploy apps/v1`, `replicasets rs apps/v1`.

### C5. A selector that matches nothing

```bash
kubectl run rooms --image=nginx:alpine
kubectl expose pod rooms --port=80 --name=rooms-svc --selector=app=roomz
kubectl get svc rooms-svc -o jsonpath='{.spec.selector}'; echo
kubectl get endpointslices -l kubernetes.io/service-name=rooms-svc
```

Expected: `{"app":"roomz"}`, and an EndpointSlice with `ENDPOINTS <unset>`. The label on the pod is `run=rooms`, so `app=roomz` matches nothing, and **no error was shown anywhere**. (We also tried `kubectl get endpoints`, the older object. It works but prints a warning that `v1 Endpoints is deprecated in v1.33+; use EndpointSlice`, so prefer EndpointSlice in new notes.) Clean up: `kubectl delete svc rooms-svc; kubectl delete pod rooms`.

**Check yourself:**

- [ ] You can name the objects the events show between "delete a pod" and "new pod Running".
- [ ] You saw an empty endpoint list with no error.
- [ ] You can say what `create`, `apply` and `replace` each did in C3.

---

## Part D: the remote control and your first pod (Episode 4)

**Goal:** run the `rooms:slim` image as a pod, read the pod, and see the four traps.

### D1. A local image does not magically reach the cluster

```bash
kubectl config current-context
kubectl run rooms --image=rooms:slim
sleep 15
kubectl get pod rooms
kubectl describe pod rooms | sed -n '/^Events/,$p' | cut -c1-170
```

Expected (ours): `rooms   0/1   ImagePullBackOff`. The events say `Failed to pull image "rooms:slim"` (it tried `docker.io/library/rooms`, which does not exist), then `ErrImagePull`, `Back-off pulling image`, `ImagePullBackOff`. The cluster's nodes have their own image store; your laptop's `rooms:slim` is not in it. Delete it: `kubectl delete pod rooms`.

### D2. Load the image and run the pod

```bash
kind load docker-image rooms:slim --name lab23
```

Expected: a line per node, `Image: "rooms:slim" ... not yet present on node ..., loading...`, done in about 2.5 seconds for us. Now the pod from `lab_files/rooms-pod.yaml` (it is `kubectl run rooms --image=rooms:slim --dry-run=client -o yaml` with `imagePullPolicy: IfNotPresent` added):

```bash
kubectl apply -f lab_files/rooms-pod.yaml
kubectl wait --for=condition=Ready pod/rooms --timeout=60s
kubectl get pods -o wide | awk '{print $1,$2,$3,$6,$7}' | column -t
kubectl port-forward pod/rooms 8080:5000
```

In a second terminal: `curl localhost:8080/health` and `curl localhost:8080/`.

Expected (ours): `rooms 1/1 Running 10.244.2.8 lab23-worker`, `Forwarding from 127.0.0.1:8080 -> 5000`, then `ok` and `Atithi rooms-service`. Stop the forward with `Ctrl+C`. In `kubectl describe pod rooms`, the Events read `Scheduled`, then `Container image "rooms:slim" already present on machine`, `Created`, `Started`.

### D3. The `latest` trap

```bash
docker tag rooms:slim rooms:latest
kind load docker-image rooms:latest --name lab23
kubectl run rl --image=rooms:latest
kubectl run rl2 --image=rooms:latest \
  --overrides='{"spec":{"containers":[{"name":"rl2","image":"rooms:latest","imagePullPolicy":"IfNotPresent"}]}}'
sleep 15
kubectl get pods rl rl2
```

Expected (ours): `rl 0/1 ImagePullBackOff` and `rl2 1/1 Running`. The image was loaded onto the nodes in both cases. With the tag `latest` and no policy, Kubernetes insists on pulling from a registry. With `imagePullPolicy: IfNotPresent` it uses the loaded image. Clean up: `kubectl delete pod rl rl2 rooms; docker rmi rooms:latest`.

### D4. Change a pod in place, and what cannot change

```bash
kubectl run web --image=nginx:alpine
kubectl wait --for=condition=Ready pod/web --timeout=60s
kubectl edit pod web
```

In the editor change `image: nginx:alpine` to `image: nginx:1.27-alpine` and save. Expected: `pod/web edited`. A few seconds later:

```bash
kubectl get pod web -o jsonpath='{.spec.containers[0].image} restarts={.status.containerStatuses[0].restartCount}{"\n"}'
```

We saw `nginx:1.27-alpine restarts=1`: the **same pod** restarted its container with the new image. Now `kubectl edit pod web` again and add an `env:` entry to the container. We tried this with a helper that edited the file and got `error: pods "web" is invalid` followed by `Edit cancelled, no valid changes were saved.` Only a few pod fields (the image among them) can change in place. Anything else means a new pod, which is why you use a Deployment. Clean up: `kubectl delete pod web`.

### D5. READY `1/2`

```bash
kubectl apply -f lab_files/two-containers.yaml
sleep 12
kubectl get pod two
kubectl describe pod two | grep -E '^\s+(web|bad):|State:|Ready:|Image:'
```

Expected (ours): `two   1/2   CrashLoopBackOff   1`. In `describe`: container `web` is `Running`, `Ready: True`; container `bad` is `Waiting`, `Last State: Terminated`, `Ready: False`. `READY 1/2` counts containers inside the pod, not pods. Clean up: `kubectl delete pod two`.

---

## Clean up

```bash
kubectl delete deployment rooms 2>/dev/null
kind delete cluster --name lab23
docker rm -f $(docker ps -aq --filter name='^w[1-5]$') 2>/dev/null
docker images rooms
```

Expected from the delete: `Deleted nodes: [...]` with the three node names. Your `rooms:slim` image stays on your laptop.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `kubectl` talks to the wrong cluster | Another context is current | `kubectl config use-context kind-lab23` (check with `current-context` first, every time) |
| Pod `ImagePullBackOff` for a local image | Image not loaded, or tag is `latest` | `kind load docker-image ...`, set `imagePullPolicy: IfNotPresent` (D1, D3) |
| `kind create cluster` fails or hangs | Docker is short of memory, or a cluster with that name exists | Give Docker more memory; `kind delete cluster --name lab23` |
| `kubectl get nodes` refused after `docker start` of the control plane | It is still starting | Wait up to a minute, retry |
| Service has no endpoints, no error | Selector and pod labels differ | Compare `kubectl get pods --show-labels` with the Service selector (C5) |
| `kubectl apply` warns about `last-applied-configuration` | Object was made with `create` | Harmless, it patches the annotation |
| Port `8080` in use for the forward | Another program on that port | Use another local port, `kubectl port-forward pod/rooms 8081:5000` |

## Real GKE Autopilot results (2026-11-24, asia-south1, cluster deleted the same day)

- Cluster ready in **4m33s**. `kubectl get nodes` was empty at first: **Autopilot starts with 0 nodes and creates them when a pod needs one.** A new pod sat `Pending` for about a minute (`FailedScheduling: no nodes available`), then two nodes appeared (Container-Optimized OS, containerd 2.2.7, 8 vCPU, about 31 GB; allocatable cpu `7910m`).
- **The control plane is hidden.** `kubectl get pods -n kube-system` shows no `etcd`, `kube-apiserver`, scheduler or controller-manager pods (only add-ons such as `kube-dns`). `kubectl get componentstatuses` lists only `scheduler` and `controller-manager`, no `etcd`. So B1's "look at the control plane pods" works on kind, not on a managed cluster, and you cannot back up `etcd` there (the provider does it).
- **D1 on a real cluster:** `image: rooms:slim` gave `ImagePullBackOff` / `ErrImagePull` (`docker.io/library/rooms:slim: not found`). A local image never reaches a managed cluster; push it to a registry (we used Artifact Registry) and give the nodes' service account `roles/artifactregistry.reader`.
- Autopilot adds default CPU requests to pods that do not set any (a harmless warning).


## What we did not test

- **EKS and AKS** (GKE Autopilot was tested; see above). **Backing up `etcd`:** not possible on a managed cluster, and not tried on kind.
- **`minikube` and Docker Desktop's built-in Kubernetes.** The script mentions them as alternatives. We only used kind.
- **Changing the five-minute node tolerance,** and **what happens to pods if a node comes back before the five minutes.**
- **A pod deleted while the control plane is down.** Not possible to type, so not run.
- **A cluster with three control-plane nodes.** Ours had one.

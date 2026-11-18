# Session 25 lab guide: Microservices on Kubernetes

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in names, IPs, hashes and times.

| | |
|---|---|
| **Time** | Part A 15 min, Part B 60 min, Part C 40 min, Part D 60 min |
| **Cost** | Free. A local `kind` cluster plus a few small containers. Delete the cluster at the end. |
| **Skill check before you start** | Sessions 21 to 24: images, pods, Deployments, Services, namespaces, `kubectl apply`. |

## Before you start

You need Docker, `kubectl`, `kind` and `helm`. We tested with Docker `29.8.2` (Docker Desktop, Mac, arm64), `kubectl` `v1.36.1`, `kind` `v0.33.0` (Kubernetes `v1.37.0` nodes) and Helm `v4.3.2`. Check: `kind version`, `helm version --short`.

Files are in `lab_files/`:

- `app/`: one small Flask image that plays every Atithi service (`SERVICE_NAME` picks the role). Routes: `/health`, `/api/<service>/`, `/api/<service>/health`, and `/leak` (allocates 10 MB per call, to show a memory limit). The `bookings` role calls `rooms-service` with a 2 second timeout and two short retries.
- `k8s/`: numbered manifests `00` to `60`.
- `chart/atithi/`: a small Helm chart.
- `kind-3nodes.yaml`: one control plane and two workers, cluster name `lab25`.

Build the image, make the cluster, load the image:

```bash
docker build -t atithi-demo:1.0 lab_files/app
kind create cluster --name lab25 --config lab_files/kind-3nodes.yaml
kind load docker-image atithi-demo:1.0 --name lab25
kubectl config current-context
```

Expected: context `kind-lab25`, three nodes `Ready`. The `atithi-demo:1.0` image is built from `python:3.12-slim` and does **not** contain `wget` or `curl`, so for HTTP checks from inside the cluster we use a separate busybox pod (called `tester` below).

> **A `kind load` problem we hit.** `kind load docker-image postgres:16` (and `nginx:alpine`) **failed** with `ctr: content digest sha256:...: not found`. Images you build yourself load fine, but multi-platform images pulled from Docker Hub failed on our Docker setup (the one that uses Docker's containerd image store). You do not need to load them: the cluster nodes pull `postgres:16`, `nginx:alpine` and `busybox:1.36` themselves.

Make the namespace and the test pod:

```bash
kubectl apply -f lab_files/k8s/00-namespace.yaml
kubectl run tester -n atithi --image=busybox:1.36 --restart=Never -- sleep 3600
```

---

## Part A: design exercise (Episode 1)

No commands. Fill the table from the script for five services (`web`, `rooms`, `bookings`, `payments`, `notifications`): port, depends on, stateful or not, what breaks if it is down. Then tick the three 12-factor rules for each one. Check your answers against the lab app: it reads its settings from environment variables, writes its logs to the console and not to a file (gunicorn does this), and keeps nothing in the process that it cannot lose (the `/leak` route is the deliberate exception).

---

## Part B: config, budget, probes and calls (Episode 2)

**Goal:** give the trucks settings and limits, then break each one on purpose and read what Kubernetes says.

### B1. ConfigMap and Secret

```bash
kubectl create configmap rooms-config -n atithi --from-literal=APP_MODE=demo --from-literal=ROOMS_PER_PAGE=20
kubectl create secret generic bookings-db -n atithi --from-literal=POSTGRES_PASSWORD=practice-only
kubectl get secret bookings-db -n atithi -o jsonpath='{.data.POSTGRES_PASSWORD}'; echo
kubectl get secret bookings-db -n atithi -o jsonpath='{.data.POSTGRES_PASSWORD}' | base64 --decode; echo
```

Expected: `cHJhY3RpY2Utb25seQ==` and then `practice-only`. That is "encoding, not encryption" in two lines: anyone who may read the Secret can decode it. The password here is practice-only; never put a real one in a file you commit.

### B2. `rooms-service` with config, resources and probes

```bash
kubectl apply -f lab_files/k8s/10-rooms.yaml
kubectl rollout status deployment/rooms-service -n atithi
kubectl wait -n atithi --for=condition=Ready pod/tester --timeout=90s
kubectl exec -n atithi tester -- wget -qO- http://rooms-service:5000/api/rooms/
kubectl exec -n atithi tester -- wget -qO- http://rooms-service.atithi.svc.cluster.local:5000/health
```

Expected (ours): `{"mode":"demo","per_page":"20","service":"rooms"}` (the ConfigMap values came in through `envFrom`), then `ok`. Both the short and the full DNS name work from inside the same wing. Read `lab_files/k8s/10-rooms.yaml` once: `envFrom`, `resources` (requests and limits), a `readinessProbe` and a `livenessProbe`, both on `/health`.

### B3. A changed ConfigMap does not change running pods

```bash
P=$(kubectl get pods -n atithi -l app=rooms -o name | head -1)
echo "pod env now: $(kubectl exec -n atithi $P -- printenv APP_MODE)"
kubectl patch configmap rooms-config -n atithi --type merge -p '{"data":{"APP_MODE":"holiday"}}'
sleep 10
echo "ConfigMap says: $(kubectl get cm rooms-config -n atithi -o jsonpath='{.data.APP_MODE}')"
echo "same pod, env after 10 s: $(kubectl exec -n atithi $P -- printenv APP_MODE)"
kubectl rollout restart deployment/rooms-service -n atithi
kubectl rollout status deployment/rooms-service -n atithi
for p in $(kubectl get pods -n atithi -l app=rooms --no-headers | awk '$3=="Running"{print $1}'); do echo "$p $(kubectl exec -n atithi $p -- printenv APP_MODE)"; done
```

Expected (ours): the ConfigMap says `holiday`, the same pod still says the old value, and after the restart the new pods say `holiday`. **Check pods by name after the restart.** In our first attempt we picked "the first running pod" right after the rollout and read an old pod that was still terminating. It showed the old value, and we nearly drew the wrong conclusion.

The same change as a **mounted file** is different. We mounted `rooms-config` into a busybox pod at `/config` and changed the value: the file showed the new value within **about 5 seconds**. (The script says "kuch der mein". Ours was fast. The application still has to re-read the file.)

### B4. Memory limit: `OOMKilled`, exit 137

The Deployment has a 128 MiB limit. Call `/leak` until the pod dies:

```bash
P=$(kubectl get pods -n atithi -l app=rooms --no-headers | awk '$3=="Running"{print $1}' | head -1)
IP=$(kubectl get pod $P -n atithi -o jsonpath='{.status.podIP}')
for i in $(seq 1 16); do kubectl exec -n atithi tester -- wget -qO- -T3 http://$IP:5000/leak || break; done
sleep 5
kubectl get pod $P -n atithi
kubectl get pod $P -n atithi -o jsonpath='{.status.containerStatuses[0].lastState.terminated.reason} exit={.status.containerStatuses[0].lastState.terminated.exitCode}{"\n"}'
```

Expected (ours): `holding 10 MB` up to `holding 90 MB`, then the next call fails (`command terminated with exit code 1`, the connection died). Then `1/1 Running 1` (the same pod name, one restart) and `OOMKilled exit=137`. The process reached the limit at roughly 90 to 100 MB of leaks plus Python's own baseline.

### B5. LimitRange and ResourceQuota

```bash
kubectl apply -f lab_files/k8s/20-limitrange.yaml
kubectl run noresources -n atithi --image=busybox:1.36 -- sleep 600
kubectl get pod noresources -n atithi -o jsonpath='{.spec.containers[0].resources}'; echo
kubectl delete pod noresources -n atithi --wait=false
```

Expected: `{"limits":{"cpu":"500m","memory":"256Mi"},"requests":{"cpu":"100m","memory":"64Mi"}}`. The pod asked for nothing and got the LimitRange defaults.

Now the budget, a quota of four pods in the wing:

```bash
kubectl apply -f lab_files/k8s/21-quota.yaml
kubectl describe quota wing-budget -n atithi | tail -4
kubectl scale deployment rooms-service -n atithi --replicas=5
sleep 6
kubectl get deploy rooms-service -n atithi
RS=$(kubectl get rs -n atithi -l app=rooms -o jsonpath='{.items[?(@.spec.replicas==5)].metadata.name}')
kubectl describe rs $RS -n atithi | grep -E 'FailedCreate|Warning'
kubectl scale deployment rooms-service -n atithi --replicas=2
```

What we saw: `pods 3 4` before the scale; then `rooms-service 3/5 3 3` (only three of five pods exist, because the `tester` pod uses one of the four), a `ReplicaFailure True FailedCreate` condition, and this event: `Error creating: pods "rooms-service-..." is forbidden: exceeded quota: wing-budget, requested: pods=1, used: pods=4, limited: pods=4`. The pods were never created, so there is nothing `Pending` to look at. The error is on the **ReplicaSet**, not on a pod.

The rule about requests, tested the other way round: remove the LimitRange and quota (`kubectl delete limitrange per-truck -n atithi; kubectl delete quota wing-budget -n atithi`), then create a quota on CPU and memory and try a pod with no `resources`:

```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: ResourceQuota
metadata: {name: cpu-budget, namespace: atithi}
spec: {hard: {requests.cpu: "2", limits.cpu: "4", requests.memory: 2Gi, limits.memory: 4Gi}}
EOF
kubectl run bare -n atithi --image=busybox:1.36 -- sleep 600
kubectl delete quota cpu-budget -n atithi
```

Expected: `Error from server (Forbidden): pods "bare" is forbidden: failed quota: cpu-budget: must specify limits.cpu for: bare; limits.memory for: bare; requests.cpu for: bare; requests.memory for: bare`. With a CPU and memory quota, every pod must declare requests and limits (or get them from a LimitRange).

### B6. Probes

A readiness probe that never passes:

```bash
kubectl patch deployment rooms-service -n atithi --type json \
  -p '[{"op":"replace","path":"/spec/template/spec/containers/0/readinessProbe/httpGet/path","value":"/nope"}]'
sleep 20
kubectl get pods -n atithi -l app=rooms
kubectl get deploy rooms-service -n atithi
kubectl get endpointslices -n atithi -l kubernetes.io/service-name=rooms-service \
  -o jsonpath='{range .items[*].endpoints[*]}{.addresses[0]} ready={.conditions.ready}{"\n"}{end}'
kubectl rollout undo deployment/rooms-service -n atithi
```

What we saw: the new pod sat at `0/1 Running`, the two old pods stayed `1/1`, the Deployment said `READY 2/2, UP-TO-DATE 1, AVAILABLE 2`, and the endpoint list had two `ready=true` and one `ready=false`. The rollout did not take down the working pods: that is the "readiness protects rolling updates" claim, observed. `rollout undo` printed a warning that rolling back does not update the `last-applied-configuration` annotation of an object managed with `kubectl apply`. It worked, but re-apply your YAML afterwards.

A liveness probe that never passes (we patched path `/nope` and a 3 second period, waited 25 seconds): both pods showed `RESTARTS 2` and one flipped to `0/1`. Same undo afterwards.

### B7. A service calls a service, and fails fast

```bash
kubectl apply -f lab_files/k8s/60-rbac.yaml
kubectl apply -f lab_files/k8s/11-bookings.yaml -f lab_files/k8s/12-web.yaml
kubectl rollout status deployment/bookings-service -n atithi
kubectl exec -n atithi tester -- wget -qO- http://bookings-service:5000/api/bookings/
```

Expected (ours): `{"mode":"holiday","per_page":"20","rooms":{"mode":"holiday","per_page":"20","service":"rooms"},"service":"bookings"}`. The booking answer contains the rooms answer: `bookings` called `http://rooms-service:5000/api/rooms/` by DNS name.

Now take `rooms` away:

```bash
kubectl scale deployment rooms-service -n atithi --replicas=0
sleep 4
kubectl exec -n atithi tester -- sh -c 'time wget -qO- -T10 http://bookings-service:5000/api/bookings/'
kubectl scale deployment rooms-service -n atithi --replicas=2
```

Expected (ours): `wget: server returned error: HTTP/1.1 503 SERVICE UNAVAILABLE` after **0.6 seconds**. A Service with no pods behind it refuses at once, and the app's two short retries (0.2 s and 0.4 s of waiting) add up to 0.6 s. The caller got a clean, small error and not a hang. In Part D you will see the harsher case: a blocked path does not refuse, it silently times out.

**Check yourself:**

- [ ] You saw an environment variable stay old after a ConfigMap change, and a restart fix it.
- [ ] You can name the error that shows a quota being hit, and where it appears.
- [ ] You saw an old pod keep serving while a new pod failed its readiness probe.

---

## Part C: lockers (Episode 3)

**Goal:** make storage three ways and meet every trap in the script.

### C1. Dynamic provisioning: Postgres with a claim

```bash
kubectl get storageclass
kubectl apply -f lab_files/k8s/13-postgres.yaml
kubectl rollout status deployment/postgres -n atithi
kubectl get pv,pvc -n atithi
```

Expected (ours): one StorageClass, `standard (default)`, provisioner `rancher.io/local-path`, reclaim `Delete`, binding `WaitForFirstConsumer`, expansion not allowed. After the Postgres pod starts, a `postgres-data` claim shows `Bound` to a volume named `pvc-<uuid>` of `1Gi`, class `standard`. Nobody created that volume by hand. In kind a claim stays `Pending` until a pod uses it (`WaitForFirstConsumer`), then the volume appears.

Put some data in, delete the pod, and check:

```bash
until kubectl exec -n atithi deploy/postgres -- pg_isready -h 127.0.0.1 -U postgres >/dev/null 2>&1; do sleep 2; done
kubectl exec -n atithi deploy/postgres -- psql -U postgres -tA -c 'create table if not exists bookings(id serial, guest text); insert into bookings(guest) values ($$asha$$),($$ravi$$); select count(*) from bookings;'
kubectl delete pod -n atithi -l app=postgres
kubectl rollout status deployment/postgres -n atithi
until kubectl exec -n atithi deploy/postgres -- pg_isready -h 127.0.0.1 -U postgres >/dev/null 2>&1; do sleep 2; done
kubectl exec -n atithi deploy/postgres -- psql -U postgres -tA -c 'select count(*) from bookings;'
```

Expected: `2`, then after the new pod starts, `2` again. (We use `-h 127.0.0.1` for the readiness check for the reason in the Session 21 guide.) The records survived the pod.

### C2. Two things a claim will refuse

```bash
kubectl patch pvc postgres-data -n atithi -p '{"spec":{"resources":{"requests":{"storage":"2Gi"}}}}'
kubectl patch pvc postgres-data -n atithi -p '{"spec":{"accessModes":["ReadWriteMany"]}}'
```

Expected (ours): the first says `Forbidden: only dynamically provisioned pvc can be resized and the storageclass that provisions the pvc must support resize`. kind's default class does not allow expansion, so on this cluster you cannot see a resize succeed (the script's `allowVolumeExpansion` rule, confirmed by its absence). The second says `spec is immutable after creation except resources.requests and volumeAttributesClassName for bound claims`.

### C3. A manual locker, and the default-class trap

The script's lab makes a PV (`hostPath`) and a PVC and expects them to bind. **They do not, if you leave out `storageClassName`.** We tried it:

```bash
kubectl apply -f - <<'EOF'
apiVersion: v1
kind: PersistentVolume
metadata: {name: locker-0}
spec:
  capacity: {storage: 1Gi}
  accessModes: [ReadWriteOnce]
  persistentVolumeReclaimPolicy: Retain
  hostPath: {path: /tmp/data}
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: claim-0, namespace: atithi}
spec:
  accessModes: [ReadWriteOnce]
  resources: {requests: {storage: 500Mi}}
EOF
sleep 3
kubectl get pvc claim-0 -n atithi -o jsonpath='class={.spec.storageClassName} status={.status.phase}{"\n"}'
kubectl get pv locker-0
```

Expected (ours): `class=standard status=Pending`, and `locker-0 ... Retain Available`. The claim picked up the cluster's default class, so it looked for a `standard` volume (and waited for a pod), and ignored our class-less volume. Clean up: `kubectl delete pvc claim-0 -n atithi; kubectl delete pv locker-0`.

The fix is to give both a class name (`manual`, which does not need to exist as a StorageClass). `lab_files/k8s/30-pv-pvc-pod.yaml` does that:

```bash
kubectl apply -f lab_files/k8s/30-pv-pvc-pod.yaml
kubectl wait -n atithi --for=condition=Ready pod/locker-user --timeout=90s
kubectl get pv,pvc -n atithi | grep locker
kubectl exec -n atithi locker-user -- sh -c 'echo hi > /data/a; cat /data/a'
```

Expected (ours): `persistentvolume/locker-1 1Gi RWO Retain Bound atithi/locker-claim` and `persistentvolumeclaim/locker-claim Bound locker-1 1Gi RWO manual`, then `hi`. The claim asked for `500Mi` and shows `1Gi`: it got the whole volume.

Delete the pod and make another with the same claim (apply the file again, it recreates the pod and leaves the PV and PVC alone):

```bash
kubectl delete pod locker-user -n atithi
kubectl apply -f lab_files/k8s/30-pv-pvc-pod.yaml
kubectl wait -n atithi --for=condition=Ready pod/locker-user --timeout=90s
kubectl exec -n atithi locker-user -- cat /data/a
```

Expected: `hi`. The data outlived the pod.

### C4. Deleting the claim

```bash
kubectl delete pvc locker-claim -n atithi --wait=false
sleep 3
kubectl get pvc locker-claim -n atithi
kubectl delete pod locker-user -n atithi
sleep 4
kubectl get pvc locker-claim -n atithi
kubectl get pv locker-1
```

What we saw: while the pod used it, the claim sat in **`Terminating`**. After the pod was gone, the claim was gone, and the volume read `locker-1 ... Retain Released atithi/locker-claim manual`. The file was still on the node's disk (we read `hi` from `/tmp/data/a` inside the kind worker). Then we applied the file again to make a **new** claim for the same volume: it stayed **`Pending`** and the volume stayed `Released`. A released volume is not handed to a new claim by itself: someone has to clean it up on purpose.

### C5. Size and mode must match

With a fresh `manual` volume (`1Gi`, `ReadWriteOnce`), we made one claim asking for `ReadWriteMany` and another asking for `2Gi`. Both stayed `Pending` (the volume stayed `Available`). The event on the claim also said `storageclass.storage.k8s.io "manual" not found`: that is only noise from the cluster trying to provision for a class name that has no provisioner. Clean up all test volumes and claims before moving on: `kubectl delete pvc --all -n atithi` would also delete Postgres' claim, so delete by name and check with `kubectl get pv,pvc -A`.

**Check yourself:**

- [ ] You saw a PV appear on its own after a claim was used by a pod.
- [ ] You saw the manual claim stay `Pending` without a class, and `Bound` with one.
- [ ] You can say what `Released` means, and why the new claim stayed `Pending`.

---

## Part D: concierge, locks and the franchise kit (Episode 4)

**Goal:** one entrance, a closed wing, a limited duty badge and a packaged release.

### D1. The concierge

The script warns that `ingress-nginx` is retired, so we used Traefik, installed with Helm:

```bash
helm repo add traefik https://traefik.github.io/charts
helm repo update
helm install traefik traefik/traefik -n traefik --create-namespace --wait --timeout 180s
kubectl get pods -n traefik
kubectl get ingressclass
```

Expected (ours, took about 20 seconds): chart `traefik-42.4.1`, Traefik `v3.7.19`, one pod `1/1 Running`, and the class `traefik (default)`. The Traefik Service is a `LoadBalancer` with `EXTERNAL-IP <pending>`: on kind nothing hands out a public address, so we reach it with a port-forward.

```bash
kubectl apply -f lab_files/k8s/40-ingress.yaml
kubectl port-forward -n traefik svc/traefik 8081:80
```

In a second terminal:

```bash
curl -s localhost:8081/ | head -c 100
curl -s localhost:8081/api/rooms/
curl -s localhost:8081/api/bookings/
curl -s -o /dev/null -w '%{http_code}\n' localhost:8081/api/nothing
```

Expected (ours): the nginx welcome page for `/`; `{"mode":"holiday","per_page":"20","service":"rooms"}`; the bookings JSON containing the rooms JSON; and `404`, which is nginx's own 404 page: the unknown path matched the `/` rule, so it went to `web`.

### D2. The path trap, and its fix

The ingress sends the path to the service **unchanged**. We deployed the plain `rooms:slim` image (Session 22), which only knows `/health`, behind the path `/plain` (`kind load docker-image rooms:slim --name lab25` first, and `imagePullPolicy: IfNotPresent`):

```bash
curl -s -o /dev/null -w '%{http_code}\n' localhost:8081/plain/health
```

Expected (ours): **`404`**. The app received `/plain/health`, which it does not have. Now strip the prefix with a Traefik middleware:

```yaml
apiVersion: traefik.io/v1alpha1
kind: Middleware
metadata: {name: strip-plain, namespace: atithi}
spec:
  stripPrefix: {prefixes: [/plain]}
```

and add the annotation `traefik.ingress.kubernetes.io/router.middlewares: atithi-strip-plain@kubernetescrd` to the Ingress. Then `curl localhost:8081/plain/health` printed **`ok` with 200**. (That annotation is Traefik's own. A different controller has its own way, and Gateway API has another.) The lab image `atithi-demo` avoids the problem by serving its routes under `/api/<service>/`.

### D3. A closed wing

First, what is reachable with no policy:

```bash
kubectl exec -n atithi deploy/web -- sh -c 'nc -zv -w3 postgres 5432'
kubectl exec -n atithi tester -- sh -c 'nc -zv -w3 rooms-service 5000'
```

Expected (ours): both say `open`. Now default-deny only:

```bash
kubectl apply -f - <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny-ingress, namespace: atithi}
spec: {podSelector: {}, policyTypes: [Ingress]}
EOF
sleep 4
kubectl exec -n atithi deploy/web -- sh -c 'nc -zv -w3 postgres 5432'
kubectl exec -n atithi tester -- sh -c 'nc -zv -w3 rooms-service 5000'
curl -s -m6 -o /dev/null -w '%{http_code}\n' localhost:8081/api/rooms/
```

What we saw: `Operation timed out` and `Connection timed out`, and the concierge call returned `000` (curl gave up). **kind's network plugin (kindnet) did enforce the policy** on our version, which the script's handout says to check. Two lessons: a blocked path does not say "refused", it hangs; and the closed wing also closed the **front door**: Traefik lives in another namespace, so default-deny cut it off too.

The service call under default-deny: we ran the bookings call to `rooms-service` from inside the `bookings` pod with a 3 second timeout. It failed after **4 seconds** with `URLError <urlopen error timed out>`. Through the concierge, `/api/bookings/` gave `000` after the 12 seconds we allowed. This is the timeout lesson of Episode 2, live: a timeout in the code is what turns a hang into an answer.

Now apply the real set, `lab_files/k8s/50-netpol.yaml`. It has five policies: default-deny, allow the concierge's namespace to `web`/`rooms`/`bookings`, `web` and `bookings` to `rooms` on 5000, `web` to `bookings` on 5000, and only `bookings` to `postgres` on 5432.

```bash
kubectl apply -f lab_files/k8s/50-netpol.yaml
sleep 5
kubectl exec -n atithi deploy/web -- sh -c 'nc -zv -w3 rooms-service 5000'
kubectl exec -n atithi deploy/web -- sh -c 'nc -zv -w3 bookings-service 5000'
kubectl exec -n atithi deploy/web -- sh -c 'nc -zv -w3 postgres 5432'
kubectl exec -n atithi tester -- sh -c 'nc -zv -w3 rooms-service 5000'
kubectl exec -n atithi deploy/bookings-service -- python -c "import socket; socket.create_connection(('postgres',5432),3); print('open')"
for p in / /api/rooms/ /api/bookings/; do curl -s -m6 -o /dev/null -w "$p %{http_code}\n" localhost:8081$p; done
```

Expected (ours): `web -> rooms` open, `web -> bookings` open, **`web -> postgres` timed out**, the unlabelled `tester -> rooms` timed out, `bookings -> postgres` open, and all three concierge paths `200`. Only the paths we named exist. (We did not add egress rules, so DNS needed no special rule. If you add egress deny, open DNS.)

### D4. A limited duty badge

```bash
SA=system:serviceaccount:atithi:bookings-sa
kubectl auth can-i list secrets --as=$SA -n atithi
kubectl auth can-i get configmaps --as=$SA -n atithi
kubectl auth can-i delete pods --as=$SA -n atithi
kubectl auth can-i get configmaps --as=$SA -n default
kubectl auth can-i list secrets -n atithi
```

Expected (ours): `no`, `yes`, `no`, `no`, `yes` (the last one is you, the cluster admin). The service account can read ConfigMaps in its own wing and nothing else, not even the same thing in another wing. We did **not** test the `securityContext` hardening the script mentions (non-root, read-only filesystem) on these pods.

### D5. The franchise kit

```bash
helm lint lab_files/chart/atithi
helm template atithi lab_files/chart/atithi | grep -E '^kind|replicas'
helm install atithi lab_files/chart/atithi -n helmtest --create-namespace --wait --timeout 120s
kubectl get deploy -n helmtest
helm upgrade atithi lab_files/chart/atithi -n helmtest -f lab_files/chart/atithi/values-prod.yaml --wait --timeout 120s
kubectl get deploy -n helmtest
helm history atithi -n helmtest
helm rollback atithi 1 -n helmtest --wait --timeout 120s
kubectl get deploy -n helmtest
helm uninstall atithi -n helmtest
kubectl delete ns helmtest
```

What we saw: `helm lint` passed (only an "icon is recommended" note). Install: `STATUS: deployed`, `REVISION: 1`, with `bookings-service 1/1` and `rooms-service 2/2`. Upgrade with the prod values: `REVISION: 2`, `bookings 2/2` and `rooms 3/3`. `helm history` listed revision 1 `superseded` and revision 2 `deployed`. Rollback printed `Rollback was a success!`, the counts went back to `1/1` and `2/2`, and history then showed **three** revisions: a rollback is a new revision, not a rewind. (This is Helm 4. We did not test Helm 3.)

### D6. The search order

We exercised most rows of the script's table during this guide: `Pending` (quota and claims, B5, C3, C5), `CrashLoopBackOff` and `ImagePullBackOff` (Sessions 23 and 24), empty endpoints (Session 23), `ingress 404` (D2), `PVC Pending` (C3, C5). Practise the table by breaking things one at a time and answering with `kubectl describe` and `kubectl get events --sort-by=.lastTimestamp` before you change anything.

**Check yourself:**

- [ ] All three concierge paths answer 200.
- [ ] You saw the closed wing close the front door too, and fixed it with the allow policy.
- [ ] You can show with `can-i` that the service account cannot list secrets.
- [ ] You rolled back a Helm release and saw the revision number go up.

---

## Clean up

```bash
pkill -f 'port-forward -n traefik'
kind delete cluster --name lab25
docker rmi atithi-demo:1.0
docker images | grep -E 'rooms|atithi'
```

Expected from the delete: `Deleted nodes: [...]` with three names. Deleting the cluster removes the volumes, the claims and the files under `/tmp/data` inside the node containers.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `kind load ... ctr: content digest ... not found` | Multi-platform image pulled from a registry (Docker's containerd image store) | Do not load it; let the nodes pull it, or load only images you built |
| `exec: "wget": executable file not found` in an app pod | The slim image has no `wget` | Use the `tester` pod, or `python -c` |
| Env var still old after a ConfigMap change | Env is read at start | `kubectl rollout restart`, then check pods by name |
| `FailedCreate ... exceeded quota` on the ReplicaSet | The wing's budget is full | Scale down, or raise the quota |
| Manual PVC stays `Pending`, PV `Available` | No `storageClassName`, so the default class was used | Same class name on both |
| New claim for a `Released` volume stays `Pending` | Released volumes are not reused automatically | Clean up and re-create the volume on purpose |
| Ingress works, then everything times out after default-deny | The concierge's namespace is blocked too | Allow it (policy 2 in `50-netpol.yaml`) |
| 404 from the app behind an Ingress path | The prefix is passed on unchanged | Strip it (D2) or serve the prefix |
| `pg_isready` passes but `psql` is refused on a new volume | Postgres' temporary start-up server | `-h 127.0.0.1` (Session 21 guide) |

## What we did not test

- **A managed cluster** (GKE) and its built-in ingress controller, TLS on the Ingress, and Gateway API.
- **`ingress-nginx`.** We followed the script and used Traefik. We did not check the retirement date given in the script.
- **A successful PVC resize.** kind's default class does not allow it.
- **A StatefulSet** (`pg-0`, `pg-1`) and a real cloud disk (EBS, Persistent Disk).
- **Pod `securityContext` hardening,** and **egress** policies.
- **Metrics-based scaling (HPA),** which belongs to a later session.
- **CPU throttling** from a CPU limit. We tested the memory limit only.
- **Helm 3.** Everything used Helm 4.3.2.

# Kubernetes: Class Notes (from handwritten `K8 Notes.pdf`)

> Transcribed from 25 handwritten pages and organised by topic. Hindi/Hinglish remarks are translated into English.
> Items marked **⚠️ Correction** are places where the handwritten note was ambiguous or technically off. I've written the correct version.
> The PDF contains Kubernetes only. It has no Docker section.

## Contents
1. [Pods](#1-pods)
2. [Pod states and container exit codes](#2-pod-states-and-container-exit-codes)
3. [ReplicaSets](#3-replicasets)
4. [Deployments](#4-deployments)
5. [Namespaces](#5-namespaces)
6. [ResourceQuota and LimitRange](#6-resourcequota-and-limitrange)
7. [Services](#7-services)
8. [Persistent Volumes (PV)](#8-persistent-volumes-pv)
9. [Persistent Volume Claims (PVC)](#9-persistent-volume-claims-pvc)
10. [StorageClass](#10-storageclass)
11. [Horizontal and vertical scaling](#11-horizontal-and-vertical-scaling)
12. [Cheat sheet](#12-command-cheat-sheet)

---

## 1. Pods

### Everyday commands
```bash
kubectl get pods                         # how many pods are present
kubectl run nginx --image=nginx          # create a pod: "nginx" is the pod name, --image is the image name
kubectl describe pod <pod-name>          # detailed info about one pod
kubectl describe pod                     # details of ALL pods (includes the node of each)
kubectl get pods -o wide                 # the quickest way to see which node each pod is on
kubectl delete pod <pod-name>
kubectl explain pod                      # full reference for any resource type: what to write for kind, labels, etc. in YAML
```

`kubectl describe pod` shows the image used, image ID, container ID, state, mounts, conditions and volumes. At the bottom is the **Events** table (Type, Reason, Age, From, Message), which is where you look when something is wrong.

`kubectl get pods -o wide` columns:
```
NAME   READY   STATUS   RESTARTS   AGE   IP   NODE
```

### Questions answered with `describe`
| Question | Where to look |
|---|---|
| Which node is the pod on? | `kubectl get pods -o wide`, or the `Node:` line in `describe` |
| How many containers are in the pod? | `Containers:` section |
| Which images does the pod use? | `Image:` under each container |
| What state is container "agentx" in pod "webapp"? | `State:` under that container |
| Why is that container in error? | The **Events** section at the bottom |

### The READY column
`READY` shows **running containers / total containers** in the pod. It does not count pods.
Example: `1/2` means the pod has 2 containers and 1 is running.

### Creating a pod from YAML
A YAML file is also called a **manifest**.

If you have the image, the direct way is:
```bash
kubectl run redis --image=redis123
```
If you want a YAML file but don't want to write it by hand, let kubectl generate it:
```bash
kubectl run redis --image=redis123 --dry-run=client -o yaml > redis-def.yaml
```
- `--dry-run=client` builds the object without creating it.
- `-o yaml` prints it as YAML, which is redirected into a file.

Then create the pod from that file:
```bash
kubectl create -f redis-def.yaml
```

### Changing the image of a pod
Two ways:
1. Edit the image name in the YAML file, then:
   ```bash
   kubectl apply -f <yaml-file>
   ```
2. Edit the live object:
   ```bash
   kubectl edit pod redis
   ```
   This opens the pod's YAML. Change it and save, and the change is applied automatically. The output is `pod/redis edited`.

### Logs from a container that already crashed
How do you find out why a pod restarted at midnight, when the current container has no logs of it?
```bash
kubectl logs <pod-name> -c <container> --previous
```
`--previous` shows the logs of the previous instance of the container, the one that crashed or exited.

---

## 2. Pod states and container exit codes

| State | Meaning | Typical reasons |
|---|---|---|
| **Pending** | The pod has been created but has not started running | Kubernetes can't find enough CPU or memory on a node to schedule it; the node doesn't have the storage or volume the pod needs |
| **Running** | The pod is scheduled to a node and at least one container is running | One container may still be starting while others are already running |
| **Succeeded** | All containers completed successfully; the work is done | Normal for jobs and one-off tasks |
| **Failed** | One or more containers terminated with a non-zero exit code | The container hit an error and stopped; a problem with the script or application running in it |
| **CrashLoopBackOff** | The pod keeps crashing and restarting; Kubernetes brings it back and it fails again | A bug or misconfiguration that crashes the app on startup (for example, connecting to a database that isn't ready); a missing environment variable, ConfigMap or Secret |
| **Unknown** | The state can't be determined | The node can't be reached: it may be down, or there is a network issue |
| **Terminating** | Kubernetes is shutting the pod down gracefully and waiting for its containers to stop | Seen after `kubectl delete pod` |

> **⚠️ Correction:** the five official pod *phases* are Pending, Running, Succeeded, Failed and Unknown. `CrashLoopBackOff` and `Terminating` are statuses that `kubectl get pods` displays in the STATUS column; they are not phases. They belong in this table because they are what you actually see.

### Container exit codes
| Code | Meaning |
|---|---|
| `0` | Successful execution (normal termination) |
| `1` | General error, e.g. a web server failed to start because of missing config |
| `126` | Permission denied (the file is not executable; a `chmod` issue) |
| `127` | Command not found (the container tried to run a command that doesn't exist) |
| `137` | OOMKilled (the container was killed for using too much memory) |

137 is 128 + 9, meaning the process received signal 9 (SIGKILL). Running out of memory is the most common cause.

---

## 3. ReplicaSets

```bash
kubectl get replicaset          # or: kubectl get rs
```
Output columns:
```
NAME   DESIRED   CURRENT   READY   AGE
```
- **DESIRED**: how many pods the ReplicaSet should have.
- **READY**: how many are ready right now.

| Task | Command |
|---|---|
| Image used by the pods of a ReplicaSet | `kubectl describe replicaset <name>`, then look under `Containers:` |
| How many pods are ready | `kubectl get rs <name>`, READY column |
| Why pods are not ready | `kubectl describe pods`, then read the Events section of the pod |
| Delete one pod | `kubectl delete pod <pod-name>` |

> **⚠️ Correction:** the note has `kubectl get new-replica-set`. The resource type is required: `kubectl get rs new-replica-set`.

**Why are there still 4 pods after deleting one?** Because the ReplicaSet makes sure the desired number of pods always exists. It creates a replacement immediately.

### apiVersion of a resource
```bash
kubectl api-resources | grep replicaset     # answer: apps/v1
kubectl api-resources                       # apiVersion of every kind
```

### Create, update, delete
```bash
kubectl create -f <yaml-file>          # create a ReplicaSet from YAML
kubectl apply -f <yaml-file>           # after updating the YAML
kubectl replace -f <yaml-file>         # another way to push an updated YAML
kubectl delete rs <replicaset-name>
kubectl delete -f <yaml-file>          # deleting by file also deletes the ReplicaSet
```
> **⚠️ Correction:** the note has `kubectl delete <replicaset name>`. It needs the type: `kubectl delete rs <name>`.

### Scaling a ReplicaSet to 5 pods
Two ways:
```bash
kubectl edit replicaset <name>                     # opens the YAML; change `replicas` under spec and save
kubectl scale rs new-replica-set --replicas=5
```

---

## 4. Deployments

```bash
kubectl get deployment                       # how many deployments exist
kubectl describe deployment <name>           # image is under the Containers section
kubectl create -f <yaml-file>                # create a deployment from YAML
```

**Why would a deployment not be ready?** Example: READY shows `0/4`. That means 4 pods are expected and none is ready. A common cause is that the image used to create the containers doesn't exist. Find the reason by describing one of its pods and reading the Events.

> **⚠️ Correction:** the note says "4 containers". For a deployment, READY counts **pods** (ready replicas / desired replicas). For a pod, READY counts containers.

---

## 5. Namespaces

A namespace is a separate space inside the cluster where you organise and manage resources such as pods and services. It keeps different projects and teams from mixing with each other.

Example:

| Namespace 1: development | Namespace 2: testing |
|---|---|
| Pod: frontend | Pod: frontend |
| Service: backend | Service: backend |

Both have `frontend` and `backend`, but they don't interfere with each other because they are in different namespaces.

### Why use namespaces
- **Avoid name conflicts.** If two teams use the same names for their resources, namespaces stop them clashing.
- **Resource management.** You can assign different amounts of CPU and memory to each namespace.
- When several teams work on one cluster, namespaces let them work in an organised way without getting in each other's way.

**Analogy from the notes:** think of the cluster as a library and each namespace as a separate bookshelf. On each shelf you place different kinds of books (pods, services). Two shelves can hold books with the same name, and there is no confusion because they are on different shelves.

### YAML
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: my-namespace
  labels:
    environment: development
```
> **⚠️ Correction:** the note writes the name as `my_namespace`. Kubernetes names can't contain underscores, so use `my-namespace`. Labels go under `metadata`, as `labels:`.

### Commands
```bash
kubectl create -f <yaml-file>                       # create from YAML
kubectl create namespace <name>                     # create without YAML
kubectl get namespaces                              # list all
kubectl describe namespace <name>                   # details
kubectl delete namespace <name>                     # deletes ALL resources inside it too

kubectl get pods --namespace=<name>                 # pods in one namespace
kubectl get <resource-type> --namespace=<name>      # any resource in one namespace
kubectl run redis --image=redis -n finance          # create a pod in a namespace
kubectl create -f <yaml-file> --namespace=<name>    # create a resource from YAML in a namespace

kubectl get pods --all-namespaces                   # which namespace is pod "blue" in?
kubectl get pods --all-namespaces | grep blue
```
> **⚠️ Correction:** the flag is `--all-namespaces` (short form `-A`), not `--all-namespace`.

### Switching to a namespace
```bash
kubectl config set-context --current --namespace=<namespace-name>
```
After this, commands run in that namespace by default.

### Can a pod in one namespace talk to a pod in another?
Yes, through the service's fully qualified domain name:
```
<service-name>.<namespace>.svc.cluster.local
backend.dev.svc.cluster.local
```

---

## 6. ResourceQuota and LimitRange

To control how much CPU, memory and other resources a namespace can use, Kubernetes has two objects.

### ResourceQuota
Limits the **total** resources used by all pods and objects in a namespace.

**Analogy from the notes:** a team has a total budget of $100. The whole team together cannot spend more than that.

```yaml
apiVersion: v1
kind: ResourceQuota
metadata:
  name: namespace-quota
  namespace: my-namespace
spec:
  hard:
    requests.cpu: "4"        # total CPU requests for all pods
    requests.memory: 8Gi     # total memory requests for all pods
    limits.cpu: "10"         # total CPU limit for all pods
    limits.memory: 16Gi      # total memory limit for all pods
    pods: "10"               # maximum number of pods in the namespace
```
```bash
kubectl create -f <resource-quota.yml>
```

### LimitRange
Sets defaults and minimum/maximum values for **each individual** pod or container in a namespace. It makes sure no single pod asks for more than is allowed.

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: limitrange-quota
  namespace: my-namespace
spec:
  limits:
    - type: Container
      default:               # default LIMIT for each container
        cpu: 500m
        memory: 512Mi
      defaultRequest:        # default REQUEST for each container
        cpu: 200m
        memory: 256Mi
```
```bash
kubectl create -f <limit-range.yml>
```

| | ResourceQuota | LimitRange |
|---|---|---|
| Applies to | The namespace as a whole | Each pod or container |
| Controls | Total CPU, memory, pod count | Default, minimum and maximum per container |

---

## 7. Services

`kubernetes` is the default service that every cluster has.

```bash
kubectl get services               # how many services exist; the TYPE column shows the type
kubectl describe service <name>    # TargetPort, Labels, Endpoints
```

| Question | Where to look |
|---|---|
| Type of the default `kubernetes` service | `kubectl get services`, TYPE column |
| Its target port | `kubectl describe service kubernetes`, `TargetPort:` |
| Its labels | same output, `Labels:` |
| Endpoints attached to it | same output, `Endpoints:` |

### Exposing a pod
Create a service `redis-service` that exposes the redis application inside the cluster on port 6379:
```bash
kubectl expose pod redis --port=6379 --name redis-service
```

---

## 8. Persistent Volumes (PV)

### Why PVs exist
- A container can have a volume of its own, but when the container dies the data goes with it.
- Even if the data is made persistent on a node, it is not centralised: it lives on that one node.
- A **Persistent Volume** is central storage for the whole cluster, available to all nodes. Pods use it through a **Persistent Volume Claim (PVC)**.
- When several pods attach to it, they all see the same storage, in sync.
- A PV is independent of any pod's life cycle.

### Access modes
| Mode | Meaning |
|---|---|
| `ReadOnlyMany` | Many can mount it, read only |
| `ReadWriteOnce` | Read and write by one at a time |
| `ReadWriteMany` | Many can read and write at the same time |

> **⚠️ Correction:** the note describes these per pod. `ReadWriteOnce` actually means one **node** at a time, so several pods on the same node can share it. The mode that restricts to a single pod is `ReadWriteOncePod`.

### PV definition
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-vol
spec:
  accessModes:
    - ReadWriteOnce                       # access policy
  capacity:
    storage: 1Gi                          # size
  persistentVolumeReclaimPolicy: Retain   # what happens when the claim is deleted
  hostPath:
    path: /tmp/data                       # where it lives on the node
```
For a volume created in the cloud, replace the `hostPath` block with the details of that cloud volume.

### How binding works
- When a claim finds a PV, its status becomes **Bound**. If none is found, the claim stays **Pending**.
- If a pod asks for 5 GB, Kubernetes looks for a 5 GB PV. If there is none, it gives a **larger** one, never a smaller one.
- If a 7 GB PV is given, the whole PV is tied to that claim. The extra space is reserved for it whether the pod uses it or not.

> **⚠️ Correction:** the note says "one PV is used by only one pod". More precisely, one PV binds to exactly one **PVC**. Several pods can use the same PVC, if the access mode allows.

### Reclaim policy (what happens when the PVC is deleted)
| Policy | Result |
|---|---|
| **Retain** | The PV and its data remain. You clean it up or reuse it manually |
| **Delete** | The PV and its underlying storage are deleted |
| **Recycle** | The PV is wiped and made available for a new claim. **Deprecated** |

When the PVC bound to a PV is deleted, the PV's status changes from **Bound** to **Released**.

### What happens to the data
- **Pod detached from the PV:** the data stays. The PV is not deleted and the data is still accessible. This is the whole purpose of persistent storage.
- **PVC deleted:** depends on the reclaim policy above.
- Detaching a pod never deletes data. Data is deleted only when the PV's policy is `Delete` and its PVC is removed.

---

## 9. Persistent Volume Claims (PVC)

A PVC is how an application requests storage. When the application makes a claim, Kubernetes looks through all PVs for one that can fulfil it.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 5Gi
```

### Rules worth remembering
- **Access modes must match.** A PV with `ReadWriteMany` and a PVC with `ReadWriteOnce` will not bind.
- **A PVC's access mode can't be edited after creation.** Delete the PVC and create it again with the mode you need.
- **Deleting a PVC that a pod is using gets stuck.** The PVC stays in `Terminating` until the pod is deleted.
- **Before deleting a PV, make sure no PVC is using it.**

### PVC statuses
| Status | Meaning |
|---|---|
| **Pending** | Waiting to be bound to a PV |
| **Bound** | Successfully bound to a PV |
| **Lost** | The PV it was bound to is no longer available |

### Commands
```bash
kubectl create -f pvc.yml              # or: kubectl apply -f pvc.yml
kubectl get pv                         # list all PVs
kubectl get pvc                        # list all PVCs
kubectl describe pv <pv-name>          # status, reclaim policy, access mode, capacity
kubectl describe pvc <pvc-name>        # which PV it is bound to, claim status, storage requested
kubectl get pvc <pvc-name> -o wide     # which PV a PVC is bound to
kubectl get pvc <pvc-name> -o yaml     # YAML of an existing PVC
kubectl get pv -o wide                 # PVs with extra columns
kubectl edit pvc <pvc-name>
kubectl delete pvc <pvc-name>
kubectl delete pv <pv-name>
kubectl get events                     # recent events in the namespace
```

### Expanding a PVC
```bash
kubectl patch pvc <pvc-name> -p '{"spec":{"resources":{"requests":{"storage":"10Gi"}}}}'
```
This works only if the StorageClass supports volume expansion.

> **⚠️ Correction:** the note writes `"request"` in this command. The field is `"requests"`.

> **⚠️ Correction:** the note also patches `storageClassName` on an existing PVC. That field can't be changed once it is set, so Kubernetes rejects the patch. To move to another StorageClass, create a new PVC.

### Binding a PVC to a specific PV
In the PVC's `spec`, add:
```yaml
spec:
  volumeName: my-pv
```
The PVC's requested storage and access mode must still match that PV.

---

## 10. StorageClass

A StorageClass defines the **type** of storage (SSD, HDD and so on) available for **dynamic provisioning** of PVs.

When a PVC is created, it can name a StorageClass. Kubernetes then creates a PV with those properties automatically, so nobody has to create the PV by hand first.

```bash
kubectl get storageclass     # list all storage classes
```

---

## 11. Horizontal and vertical scaling

Scaling means adjusting resources to handle more or less traffic or workload.

| | Horizontal scaling (out / in) | Vertical scaling (up / down) |
|---|---|---|
| What changes | The **number of copies** (pods) of the app | The **CPU and memory** given to the existing pod |
| Out / up | Traffic increases, so add more pods | Give the pod more resources |
| In / down | Traffic decreases, so remove pods | Reduce resources when not needed |
| When to use | The app can be split into independent copies: web servers, microservices | The app does heavy processing and more copies won't help |

### Horizontal example
**Scenario:** an e-commerce website during a big sale. Many more people visit, creating heavy traffic.
**Solution:** add more pods (web server instances). Each pod serves part of the traffic, and the load is spread evenly.
**Why horizontal:** web requests are easily split among pods. Different users can be served by different pods without any problem.

### Vertical example
**Scenario:** the same site's database. Queries get more complex at peak hours (searching, filtering products), and the server needs more CPU and memory.
**Solution:** instead of adding copies of the database, which are hard to keep in sync, increase the CPU and memory of the existing pod.
**Why vertical:** a database needs one strong instance to process large tasks quickly. Multiple copies can cause data-sync problems.

---

## 12. Command cheat sheet

| Task | Command |
|---|---|
| List pods (with node and IP) | `kubectl get pods -o wide` |
| Create a pod | `kubectl run <name> --image=<image>` |
| Generate pod YAML without creating it | `kubectl run <name> --image=<image> --dry-run=client -o yaml > file.yaml` |
| Create / update from YAML | `kubectl create -f file.yaml` / `kubectl apply -f file.yaml` |
| Inspect anything | `kubectl describe <type> <name>` |
| Edit a live object | `kubectl edit <type> <name>` |
| Logs of a crashed container | `kubectl logs <pod> -c <container> --previous` |
| Field reference for a kind | `kubectl explain <type>` |
| apiVersion of a kind | `kubectl api-resources \| grep <kind>` |
| ReplicaSets | `kubectl get rs` |
| Scale | `kubectl scale rs <name> --replicas=5` |
| Deployments | `kubectl get deployment` |
| Namespaces | `kubectl get namespaces`, `kubectl create namespace <name>` |
| Work inside a namespace | `kubectl config set-context --current --namespace=<name>` |
| Search all namespaces | `kubectl get pods -A \| grep <name>` |
| Services | `kubectl get services`, `kubectl describe service <name>` |
| Expose a pod | `kubectl expose pod <pod> --port=<port> --name <service>` |
| Storage | `kubectl get pv`, `kubectl get pvc`, `kubectl get storageclass` |
| Events | `kubectl get events` |

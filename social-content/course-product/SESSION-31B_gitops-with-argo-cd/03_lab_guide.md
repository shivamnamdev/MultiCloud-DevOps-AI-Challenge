# Session 31B lab guide: GitOps with Argo CD (optional bonus)

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal. Commands and outputs below come from a real run on a local cluster (Argo CD 3.6.1, Kubernetes 1.37 on kind 0.34, `argocd` CLI 3.6.1, kubectl 1.36). Your IDs, hashes and timings will differ.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 35 min, Part C 40 min, Part D 30 min |
| **Cost** | Free. Everything runs on your laptop in Docker. No cloud account and no GitHub account needed. |
| **Skill check** | You finished Sessions 23 to 25 (kind, Deployments, Services, namespaces) and Session 16B (Git push, `git revert`). |

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  gitserver.yaml                  a tiny Git server inside the cluster (practice only)
  config_repo/part_b/rooms/       the config vault for Part B: deployment.yaml, service.yaml
  config_repo/part_c/             the same, split into base/ and overlays/dev, overlays/prod
  apps/                           the Argo CD objects: Application (manual, dev, prod), AppProject,
                                  ApplicationSet, and one Application that should be refused
```

## Where does the config vault live?

GitOps needs a Git repository that holds the Kubernetes manifests, the "config vault". You have two choices:

- **Option 1: the in-cluster Git server (tested, free, recommended).** `lab_files/gitserver.yaml` runs a small Git server inside your kind cluster, at `http://gitserver.default.svc/config.git`. No login. Practice only. It forgets everything if its pod restarts.
- **Option 2: a GitHub repository `atithi-config`** as in the script. We did not test this path. Replace every `repoURL` and `sourceRepos` value in `lab_files/apps/` with your own repo URL, and make the repo public for now (private repos need credentials, which this lab does not cover).

The commands below use Option 1.

---

## Part A: a cluster, Argo CD and a login (Episode 1)

**Goal:** install Argo CD on a fresh kind cluster, log in, and remove the one risky leftover.

```bash
kind create cluster --name argo
kubectl get nodes
```

Expected: one node `argo-control-plane` with status `Ready`.

### The Git server

```bash
kubectl apply -f lab_files/gitserver.yaml
kubectl rollout status deploy/gitserver
```

Expected: `deployment "gitserver" successfully rolled out` (the first start takes a short while, because it installs `git` and `fcgiwrap` inside the pod, so it needs internet).

### Install Argo CD

```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.6.1/manifests/install.yaml
```

### Deliberate break: the plain apply

Expected:

```
The CustomResourceDefinition "applicationsets.argoproj.io" is invalid: metadata.annotations: Too long: may not be more than 262144 bytes
```

One of Argo CD's definitions is too big for a normal `kubectl apply`, which stores a copy of the whole object in an annotation. The fix is a **server-side apply**:

```bash
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.6.1/manifests/install.yaml
kubectl -n argocd get pods
```

Expected (about a minute): seven pods, all `Running`: `argocd-application-controller-0`, `argocd-applicationset-controller`, `argocd-dex-server`, `argocd-notifications-controller`, `argocd-redis`, `argocd-repo-server`, `argocd-server`. The repo-server and server may show `0/1` for the first 20 to 40 seconds.

### Log in

```bash
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d; echo
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

(or `argocd admin initial-password -n argocd` for the password). The password is 16 characters. Leave the port-forward running and open a second terminal. In a browser go to `https://localhost:8080`: the certificate warning is normal for a local test. Log in as `admin`.

Install the `argocd` CLI from the official docs, then:

```bash
argocd login localhost:8080 --username admin --password 'PASTE-THE-PASSWORD' --insecure
```

Expected: `'admin:login' logged in successfully`. Now close the open door: change the password and remove the initial secret.

```bash
argocd account update-password --current-password 'PASTE-THE-PASSWORD' --new-password 'a-new-practice-password'
kubectl -n argocd delete secret argocd-initial-admin-secret
```

Expected: a short confirmation from the first command, and `secret "argocd-initial-admin-secret" deleted`. Log in again with the new password to prove it works.

### Check yourself

- [ ] You saw the "Too long" error and know why server-side apply fixes it.
- [ ] Seven Argo CD pods are `Running`.
- [ ] You logged in, changed the password and deleted the initial secret.

---

## Part B: the first Application, drift and self-heal (Episode 2)

**Goal:** make Git the source of truth, then see Argo CD put things back when someone changes the cluster by hand.

### B1. Put the vault in Git

Open a second port-forward for the Git server (keep the Argo CD one running):

```bash
kubectl port-forward svc/gitserver 8081:80
```

In a third terminal:

```bash
mkdir atithi-config && cd atithi-config
cp -R /path/to/lab_files/config_repo/part_b/rooms .
git init -b main
git add . && git commit -m "rooms: first standing order"
git remote add origin http://localhost:8081/config.git
git push origin main
git ls-remote origin
```

Expected: `ls-remote` lists `HEAD` and `refs/heads/main`. The `rooms/` folder holds a Deployment with 2 replicas (nginx, with CPU and memory requests) and a Service.

If the push says `rejected ... fetch first`, the Git server still holds an earlier commit. Reset it with `kubectl rollout restart deploy/gitserver`, restart the port-forward and push again.

### B2. The Application

Look at `lab_files/apps/application-rooms.yaml`: one object answering three questions (which repo, revision and path; which cluster and wing; which project). There is no `automated` section yet, so syncing is manual.

```bash
kubectl apply -f lab_files/apps/application-rooms.yaml
argocd app get rooms
```

Expected: `Sync Status: OutOfSync from main (...)` and `Health Status: Missing`. Nothing exists in the cluster yet. If you see `Unknown` and `app path does not exist`, your push did not arrive; check B1.

```bash
argocd app sync rooms
argocd app get rooms
kubectl -n atithi get pods
```

Expected: `Phase: Succeeded`, then `Synced to main (...)` and `Healthy`, and two `rooms` pods `Running` in the `atithi` wing. `CreateNamespace=true` made the wing for you. Argo CD also labelled the objects: `kubectl -n atithi get deploy rooms -o jsonpath='{.metadata.annotations}'` contains `argocd.argoproj.io/tracking-id`.

### B3. Change Git, then watch

In your clone, change `replicas: 2` to `replicas: 3` in `rooms/deployment.yaml`, then:

```bash
git commit -am "rooms: three replicas" && git push origin main
argocd app get rooms           # still Synced: Argo CD has not looked yet
argocd app get rooms --refresh # now OutOfSync from main (new hash)
```

Expected: after `--refresh`, `OutOfSync`, but the Deployment still says `2/2`: out of sync does not change anything by itself with manual sync. Apply it:

```bash
argocd app sync rooms
kubectl -n atithi get deploy rooms
```

Expected: `3/3`.

**How fast does Argo CD notice on its own?** By default it polls Git every few minutes. In our test, auto-sync picked up one new commit in **282 seconds** (about 4 minutes 40). "About three minutes, sometimes longer" is the honest answer. `--refresh` or `--hard-refresh` and webhooks are the fast paths.

### B4. Auto-sync, and the drift you did not allow

Turn on automated sync with pruning, but **not** self-heal yet:

```bash
kubectl -n argocd patch application rooms --type merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true}}}}'
```

Make a change by hand, as if someone did it at 3 a.m.:

```bash
kubectl -n atithi scale deploy rooms --replicas=5
sleep 20
kubectl -n atithi get deploy rooms
argocd app get rooms
```

Expected: `5/5` stays, and `Sync Status: OutOfSync`. Argo CD **tells** you about the drift, but without `selfHeal` it does not undo it.

Now turn self-heal on:

```bash
kubectl -n argocd patch application rooms --type merge -p '{"spec":{"syncPolicy":{"automated":{"prune":true,"selfHeal":true}}}}'
kubectl -n atithi get deploy rooms
```

Expected: back to `3/3` within a few seconds, and `Synced`. In our run the number was already back at the first check.

Finally, delete something by hand:

```bash
kubectl -n atithi delete svc rooms
sleep 4
kubectl -n atithi get svc rooms
```

Expected: the Service exists again, with an `AGE` of a couple of seconds.

### Check yourself

- [ ] The Application started `OutOfSync` / `Missing`, then became `Synced` / `Healthy`.
- [ ] You saw `5/5` stay without self-heal, and snap back to `3/3` with it.
- [ ] A deleted Service came back by itself.

### Cleanup for Part B

```bash
argocd app delete rooms --cascade -y
```

Note: the `atithi` wing (namespace) is **not** deleted, because Argo CD only created it. Remove it yourself with `kubectl delete namespace atithi`.

---

## Part C: dev and prod from one design, a bad release, a revert (Episode 3)

**Goal:** use Kustomize overlays for two environments, promote a change from dev to prod, break prod on purpose, and recover with `git revert`.

In your `atithi-config` clone, replace `rooms/` with the Part C layout:

```bash
git rm -r -q rooms
cp -R /path/to/lab_files/config_repo/part_c/base .
cp -R /path/to/lab_files/config_repo/part_c/overlays .
git add -A && git commit -m "restructure into base and overlays" && git push origin main
```

You now have `base/` (Deployment, Service, `kustomization.yaml`), `overlays/dev` (1 replica, wing `atithi-dev`) and `overlays/prod` (3 replicas, wing `atithi-prod`). The images are `nginx`, so the overlay changes the image tag with `images: - name: nginx newTag: ...`. (In the script the image is named `rooms`; the idea is the same.)

```bash
kubectl apply -f lab_files/apps/application-dev.yaml -f lab_files/apps/application-prod.yaml
sleep 25
argocd app list
kubectl -n atithi-dev get pods
kubectl -n atithi-prod get pods
```

Expected: `rooms-dev` and `rooms-prod` both `Healthy` with `Auto-Prune`, one pod in `atithi-dev` and three in `atithi-prod`.

### Promote: dev first

Edit `overlays/dev/kustomization.yaml`, change `newTag` to `"1.28-alpine"`, commit and push, then:

```bash
argocd app get rooms-dev --hard-refresh
kubectl -n atithi-dev get deploy rooms -o jsonpath='{.spec.template.spec.containers[0].image}'; echo
kubectl -n atithi-prod get deploy rooms -o jsonpath='{.spec.template.spec.containers[0].image}'; echo
```

Expected: dev shows `nginx:1.28-alpine`, prod still `nginx:1.27-alpine`. One commit changed one environment.

### Look before you promote

Change the prod `newTag` to `"1.28-alpine"` too and push, and **before** it syncs, ask Argo CD what would change:

```bash
argocd app diff rooms-prod --refresh
```

Expected:

```
===== apps/Deployment atithi-prod/rooms ======
<       - image: nginx:1.27-alpine
>       - image: nginx:1.28-alpine
```

Exactly one line. Prod then follows Git and moves to `1.28-alpine`. (If you are slow, auto-sync may already have applied the change and the diff will be empty: that is fine, it only means Argo CD got there first.)

### Deliberate break: a tag that does not exist

In `overlays/prod/kustomization.yaml` set `newTag: "9.9.9-nope"`, commit and push.

```bash
argocd app get rooms-prod --hard-refresh
sleep 25
argocd app get rooms-prod
kubectl -n atithi-prod get pods
```

Expected:

```
Sync Status:   Synced to main (...)
Health Status: Progressing

rooms-56b6468bcc-vsbss   0/1   ImagePullBackOff
rooms-8695dc749b-...     1/1   Running      (three of these)
```

Read this twice. Argo CD says **Synced**, because the cluster matches Git. The problem is that Git says something broken. The new pod cannot start, but the three old pods keep serving, so guests feel nothing. Synced is not Healthy.

Try the obvious fix:

```bash
argocd app rollback rooms-prod 1
```

Expected: `rollback cannot be initiated when auto-sync is enabled`. With GitOps the cluster follows Git, so you roll back **in Git**.

### Fix: `git revert`

```bash
git revert --no-edit HEAD && git push origin main
argocd app get rooms-prod --hard-refresh
argocd app get rooms-prod
```

Expected: `Healthy` again within a few seconds of the refresh, and three `1/1 Running` pods. `argocd app history rooms-prod` lists each sync. The mistake and the fix are both in the Git history.

### Check yourself

- [ ] Dev changed and prod did not, from one commit.
- [ ] `argocd app diff` showed a single image line.
- [ ] You saw `Synced` together with `Progressing` and `ImagePullBackOff`.
- [ ] You recovered with `git revert`, not with a rollback command.

---

## Part D: guard rails and many Applications from one file (Episode 4)

**Goal:** stop an Application from deploying where it should not, then generate dev and prod Applications from a single template.

### D1. A project with limits

Look at `lab_files/apps/appproject.yaml`: allowed repo, allowed wings `atithi-*`, and an empty `clusterResourceWhitelist` (no cluster-wide objects).

```bash
kubectl apply -f lab_files/apps/appproject.yaml
kubectl apply -f lab_files/apps/application-sneaky.yaml
sleep 8
kubectl -n argocd get application sneaky -o jsonpath='{.status.conditions[0].type}: {.status.conditions[0].message}{"\n"}'
```

`application-sneaky.yaml` belongs to the new project but tries to deploy into `kube-system`. Expected:

```
InvalidSpecError: application destination server 'https://kubernetes.default.svc' and namespace 'kube-system' do not match any of the allowed destinations in project 'atithi'
```

The default project allows everything, so for real work always create your own.

### D2. An ApplicationSet

Remove the hand-made Applications first, then apply the set:

```bash
argocd app delete rooms-dev rooms-prod --cascade -y
argocd app delete sneaky -y
kubectl apply -f lab_files/apps/applicationset.yaml
sleep 30
argocd app list
```

Expected: `rooms-dev` and `rooms-prod` appear on their own, both `Synced`, `Healthy`, `Auto-Prune`. One template and a list of two environments made two Applications. The same pattern scales to ten services and three environments.

### Deliberate break: the 3 a.m. hand edit in prod

The script asks what happens when you edit prod by hand with self-heal on. Try it:

```bash
kubectl -n atithi-prod scale deploy rooms --replicas=1
sleep 4
kubectl -n atithi-prod get deploy rooms
```

Expected: `3/3`. Argo CD undid your emergency edit within seconds.

You may think: "I will pause auto-sync on that Application first."

```bash
argocd app set rooms-prod --sync-policy none
kubectl -n argocd get application rooms-prod -o jsonpath='{.spec.syncPolicy}{"\n"}'
```

Expected: the command exits successfully, but the policy still shows `automated` with `selfHeal`. The ApplicationSet **owns** the Application and writes your change back. To pause you have to edit the ApplicationSet itself (for example `kubectl -n argocd patch applicationset rooms --type merge -p '{"spec":{"template":{"spec":{"syncPolicy":{"automated":null}}}}}'`), which affects every Application it generates. After that, your hand scale to `1/1` stays and the Application shows `OutOfSync`. Put it back with `kubectl apply -f lab_files/apps/applicationset.yaml` and within seconds prod is `3/3` again.

The emergency path in GitOps is therefore a **Git commit**: it is fast, reviewed, and leaves a record.

### Cleanup (do not skip)

```bash
pkill -f 'port-forward svc/argocd-server'; pkill -f 'port-forward svc/gitserver'
kind delete cluster --name argo
kind get clusters          # expect: No kind clusters found.
```

Deleting the cluster removes Argo CD, your applications and the Git server. Delete your local `atithi-config` folder if you do not need it.

### Check yourself

- [ ] `sneaky` was refused with `InvalidSpecError`.
- [ ] The ApplicationSet created two Applications.
- [ ] You know why `argocd app set --sync-policy none` did not pause an ApplicationSet-owned app.
- [ ] The cluster and port-forwards are gone.

---

## Final checklist for Session 31B

- [ ] Part A: Argo CD installed with server-side apply; password changed, initial secret deleted
- [ ] Part B: manual sync, then auto-sync; hand edit stayed without `selfHeal`, snapped back with it
- [ ] Part C: dev and prod from one base; a bad tag was `Synced` but `Progressing`; recovered by `git revert`
- [ ] Part D: a project refused `kube-system`; an ApplicationSet created two Applications
- [ ] `kind delete cluster --name argo` done

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `Too long: may not be more than 262144 bytes` | Plain `kubectl apply` of Argo CD | Use `--server-side --force-conflicts` |
| `app path does not exist` | Nothing (or the wrong folder) was pushed | `git ls-remote origin`, then check the `path` in the Application |
| `rejected ... fetch first` on push | Git server holds an older commit | `kubectl rollout restart deploy/gitserver`, redo the port-forward and push |
| Application stays `Unknown` | Argo CD cannot reach the repo URL | Check `repoURL`; for Option 1 it must be `http://gitserver.default.svc/config.git` |
| Change in Git not applied | Argo CD polls every few minutes | `argocd app get NAME --hard-refresh` |
| `rollback cannot be initiated when auto-sync is enabled` | Expected | `git revert` and push |
| Hand edit keeps vanishing | `selfHeal: true` | Change Git, or edit the ApplicationSet (see Part D) |
| Port 8080 or 8081 already in use | Another port-forward is running | `pkill -f 'port-forward'` and start again |

## What we did not test

Everything above ran on a local kind cluster with an in-cluster Git server (Option 1). We did not run: a GitHub-hosted config repo (Option 2), `prune` removing a manifest deleted from Git (documented Argo CD behaviour, stated in the script), webhooks, SSO, private-repo credentials or deploy keys, the secrets tools (Sealed Secrets, External Secrets, SOPS), a cloud cluster, Argo Rollouts, Flux, or the capstone's Jenkins stage that updates the vault (only its `sed`, commit and push lines were run).

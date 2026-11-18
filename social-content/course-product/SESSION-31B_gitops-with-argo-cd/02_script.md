# ✍️ 02: SCRIPT — SESSION-31B: GitOps with Argo CD (optional)
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S31B`
- **Focus:** GitOps (declarative, versioned, pulled, continuously reconciled), push vs pull deploys, two repos (app and config), Argo CD parts, install (and the `--server-side` fix), first login, `Application` (source, destination, project), Sync Status vs Health Status, manual and automated sync, `prune` and `selfHeal`, polling time and webhooks, drift repair, Kustomize base and overlays, promotion by pull request, `argocd app diff`, a bad release and rollback by `git revert`, secrets in Git (never plain), `AppProject`, `ApplicationSet`, repo credentials, how it replaces the deploy step of the capstone, limits
- **Builds on:** Session 16B (pull request, review), Session 20 (secrets, least privilege), Session 22 (truck design, edition label), Session 23 to 25 (Kubernetes, Deployment, Service, wings), Session 26 (control room), Session 27 (drift), Session 31 (capstone pipeline and its `deploy.sh`)
- **Story position:** Zoom level 3, head office and operations command. Ab foreman har nayi truck ko khud pahunchane nahi jaata. Campus mein ek site supervisor rehta hai, jo config vault mein rakhe standing orders ko asli campus se milata hai, aur farq mile to theek kar deta hai.
- **Story words used:** site supervisor (Argo CD), config vault (the config repo), vault (Git), standing order (Deployment), truck, edition label (tag), operations command (Kubernetes), wing (namespace), drift, chief architect (review), foreman (Jenkins), conveyor (pipeline), key cabinet (credentials), duty badge (role), control room, guest (end user), staff (admin)
- **Lab project:** Atithi's `rooms-service` on a local `kind` cluster, deployed only from a config repo: manual sync, auto-sync with self-heal, dev and prod overlays, a deliberate bad release rolled back by `git revert`, and a project that refuses a wrong wing.
- **Cost rule:** everything runs on a local `kind` cluster, so nothing is billed. Delete the cluster at the end. If you use a real cloud cluster, delete it the same day.
- **Tested with:** Argo CD 3.6.1 on Kubernetes 1.37 (`kind`), November 2026. Version numbers change quickly, so check the release page before you record or teach.
- **Episodes:**
  - Episode 1: Vault hi Sach Hai: GitOps aur Argo CD ka Install
  - Episode 2: Application: Sync, Health, Auto-sync aur Self-heal
  - Episode 3: Naya Version: Overlays, Promotion aur Rollback
  - Episode 4: Guard Rails: Project, ApplicationSet aur Capstone ke Saath

---

# 📺 EPISODE 1: Vault hi Sach Hai

### [00:00 – 02:00] Scene 1: Raat ke Teen Baje, Ek `kubectl edit`
**[VISUAL: A production wing at 3 a.m. An engineer runs `kubectl edit deployment rooms` and changes the replica count. The vault still says 3. A diff icon between the vault page and the live wing glows red, but nobody is looking at it.]**

**(Voiceover):**
Raat ke teen baje, rooms-service par load badha. Ek engineer ne jaldi mein `kubectl edit` kiya aur replicas badha diye. Kaam ho gaya. Par vault mein ab bhi purana number hai. Agle hafte pipeline chali, number wapas ghat gaya, aur kisi ko samajh nahi aaya ki guests ki line kyun lambi ho gayi. Ye wahi drift hai jo Session 27 mein Terraform ke saath dekha tha, ab Kubernetes ke andar. Sawaal seedha hai: agar vault hi sach hai, to campus apne aap vault jaisa kyun nahi rehta? Is session ka jawab GitOps hai.

### [02:00 – 04:20] Scene 2: GitOps ke Chaar Niyam
**[VISUAL: Four cards in a row: "described in files" (declarative), "kept in Git" (versioned), "pulled automatically", "continuously compared and repaired". Under them a loop: vault page → site supervisor → campus → compare → fix.]**

**(Voiceover):**
GitOps ke chaar niyam. Ek: jo campus mein hona chahiye, wo files mein likha ho, yaani manifests, jaise Session 24 ke Deployment aur Service. Do: wo files vault mein rahein, to har badlaav ka naam, tareekh aur review ho. Teen: koi agent unhe khud khinchkar lagaye. Chaar: wo agent baar baar milaye ki asli campus vault jaisa hai ya nahi, aur farq ho to theek kare. Chaar niyam milkar ek simple baat banate hain: vault mein change karo, campus apne aap badal jaata hai, aur campus mein haath se change karo to wo wapas ho jaata hai. Story mein is agent ka naam hai site supervisor.

### [04:20 – 07:45] Scene 3: Foreman Dhakelta Hai, Supervisor Kheenchta Hai
**[VISUAL: Left, "push": Jenkins foreman outside the campus with a ring of cluster keys, pushing a truck in. Right, "pull": a supervisor already inside the campus reading a config vault, with a thin one-way arrow from the vault. A red label on the left: "cluster keys live in the CI". A green label on the right: "keys stay inside".]**

**(Voiceover):**
Session 31 mein foreman ne `deploy.sh` ke saath truck ko building tak dhakela. Isse push kehte hain, aur uske liye foreman ke paas campus ki chaabi chahiye, yaani CI ke key cabinet mein cluster ke credentials. Agar CI par koi daaka dale, to campus ki chaabi bhi gayi. Pull ulta hai: supervisor campus ke andar rehta hai, aur bahar vault ko padhta hai. Chaabi andar hi rehti hai, aur CI ko sirf vault mein likhne ka haq chahiye. Isliye do vault rakhte hain. Ek app vault, jisme code hai, jis par foreman test aur truck design banata hai. Aur ek config vault, jisme sirf manifests hain, jo supervisor padhta hai. Foreman ka kaam banta hai: nayi truck design depot mein rakho, aur config vault mein edition label badlo. Ek aur fayda: "prod mein ye kisne badla?" ka jawab `git log` mein hota hai, kisi ke terminal history mein nahi. Har badlaav ka naam, tareekh aur review.

### [07:45 – 10:35] Scene 4: Argo CD Ke Hisse aur Install
**[VISUAL: The `argocd` wing with seven small boxes: application controller (compares), repo server (reads the vault and builds manifests), API server and UI, Redis (cache), Dex (login), notifications, ApplicationSet controller. Then the terminal: `kubectl create namespace argocd`, and the `kubectl apply --server-side` command. A red error for the plain `kubectl apply`.]**

**(Voiceover):**
Argo CD site supervisor ka asli naam hai, aur wo campus ke andar apne ek wing `argocd` mein chalta hai. Uske hisse: application controller, jo vault aur campus ko milata hai. Repo server, jo vault padhkar manifests banata hai. API server aur UI. Redis cache ke liye, Dex login ke liye, aur notifications aur ApplicationSet ke controller. Install ek manifest se hota hai, par ek jaal hai. Seedha `kubectl apply` karo to ApplicationSet ki CRD par error aata hai: `Too long: may not be more than 262144 bytes`, kyunki client-side apply ek bada annotation likhta hai. Hal: `kubectl apply --server-side --force-conflicts`. Aur URL mein `stable` ki jagah ek pakka version likho, taaki aaj aur kal ka install ek jaisa ho. Hamare test mein sab pods ek minute mein Running ho gaye.

### [10:35 – 13:30] Scene 5: Lab: kind par Argo CD
**[VISUAL: `kind create cluster --name argo`, then the namespace and the server-side apply with a pinned version, then `kubectl -n argocd get pods`. The initial password command, `kubectl port-forward svc/argocd-server -n argocd 8080:443`, the browser on `https://localhost:8080` with a certificate warning, the login page.]**

**(Voiceover):**
Lab. Session 23 ka `kind` cluster banao: `kind create cluster --name argo`. Phir:
```bash
kubectl create namespace argocd
kubectl apply -n argocd --server-side --force-conflicts \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/v3.6.1/manifests/install.yaml
kubectl -n argocd get pods
```
Jab sab Running ho, pehla password nikalo: `kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' | base64 -d`, ya `argocd admin initial-password -n argocd`. Phir `kubectl port-forward svc/argocd-server -n argocd 8080:443` aur browser mein `https://localhost:8080`. Certificate ki chetavani local test mein normal hai. User `admin`, wahi password. Terminal ke liye `argocd` CLI bhi lagao aur `argocd login localhost:8080 --username admin --insecure` se login karo. Pehli cheez: password badlo, aur initial secret hata do, kyunki wo ek khula taala hai. Ek GitHub repo `atithi-config` banao, aur usme `rooms/deployment.yaml` aur `rooms/service.yaml` rakho, jaise Session 24 mein likhe the, jisme CPU request ho.

### [13:30 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "vault = truth · pull, not push · app vault + config vault · Argo CD = site supervisor · install server-side · pin the version". Then an empty application tile labelled "rooms" appears in the Argo CD UI.]**

**(Voiceover):**
Recap: GitOps ka matlab hai vault hi sach. Supervisor khinchta hai, chaabi andar rehti hai, aur do vault. Install server-side, aur version pakka. Ab supervisor ko pehla kaam do: ek Application.

---

# 📺 EPISODE 2: Application

### [00:00 – 02:25] Scene 1: Ek Application, Teen Sawaal
**[VISUAL: An `Application` card with three questions: "where is the order?" (repo, revision, path), "where should it run?" (cluster, wing), "who may do this?" (project). Beside it the YAML.]**

**(Voiceover):**
Supervisor ko teen sawaal ka jawab chahiye. Standing order kahan rakha hai: repo, branch aur folder. Kahan lagana hai: kaun sa cluster aur kaun sa wing. Aur kis ijaazat ke saath: project. Ye teen jawab ek `Application` object mein likhte hain:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: rooms
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/YOUR_ORG/atithi-config.git
    targetRevision: main
    path: rooms
  destination:
    server: https://kubernetes.default.svc
    namespace: atithi
  syncPolicy:
    syncOptions:
      - CreateNamespace=true
```
`https://kubernetes.default.svc` ka matlab wahi cluster jisme Argo CD khud chal raha hai. `CreateNamespace=true` se wing khud ban jaata hai.

### [02:25 – 04:55] Scene 2: Do Alag Sawaal: Synced Hai Ya Healthy?
**[VISUAL: The Application tile with two badges. Sync Status: Synced, OutOfSync, Unknown. Health Status: Healthy, Progressing, Degraded, Missing. A 2 by 2 grid showing four combinations with one-line meanings.]**

**(Voiceover):**
Application par do alag badge dikhte hain, aur inhe mila dena sabse aam galti hai. Sync Status poochta hai: campus vault se milta hai ya nahi, yaani Synced ya OutOfSync. Health Status poochta hai: jo chal raha hai wo theek chal raha hai ya nahi: Healthy, Progressing, Degraded ya Missing. Pehle sync se pehle Application OutOfSync aur Missing dikhta hai, kyunki vault mein order hai par campus mein kuch nahi. Sync ke baad Synced aur Progressing, aur pods ready hote hi Healthy. Aage dekhenge: ek kharab release Synced bhi ho sakta hai aur Healthy nahi.

### [04:55 – 07:30] Scene 3: Sync: Haath Se, Phir Apne Aap
**[VISUAL: `argocd app sync rooms` and the UI Sync button. A diff panel before sync. Then the `syncPolicy.automated` block with `prune` and `selfHeal`, each with a one-line description. A tracking annotation `argocd.argoproj.io/tracking-id` on the Deployment.]**

**(Voiceover):**
Sync ka matlab hai vault ke order ko campus par lagana. Haath se: UI ka Sync button, ya `argocd app sync rooms`. Argo CD har object par ek annotation `argocd.argoproj.io/tracking-id` lagata hai, taaki jaane ki kaun si cheez uski hai. Automatic ke liye `syncPolicy` mein `automated` likhte hain. Do switch ka dhyaan: `prune: true` ka matlab hai ki jo cheez vault se hat gayi, wo campus se bhi hat jaaye. `selfHeal: true` ka matlab hai ki campus mein haath se kuch badla to wapas vault jaisa ho. Dono default mein band hain, yaani sirf `automated` likhna kaafi nahi.

### [07:30 – 10:40] Scene 4: Kitni Jaldi Pata Chalta Hai, aur Drift ka Ilaaj
**[VISUAL: A timeline. A commit in the vault at 0:00. Argo CD's poll arrives later; a bar labelled "about 3 minutes, sometimes more" and a bolt labelled "webhook: seconds". Then `kubectl scale deployment rooms --replicas=5`: OutOfSync with self-heal off, and the number snapping back in seconds with self-heal on.]**

**(Voiceover):**
Vault mein badlaav karo to Argo CD ko kitni der mein pata chalta hai? Default mein wo har teen minute ke aas paas vault ko dekhta hai, jitter ke saath. Hamare test mein ek commit ko campus tak pahunchne mein lagbhag paanch minute lage. Usse pehle chahiye to UI mein refresh dabao, ya vault mein webhook lagao, jo seconds mein bata deta hai. Ab drift. `selfHeal` band ho aur aap `kubectl scale` se replicas paanch kar do, to Application OutOfSync dikhata hai, par campus ko wahin chhod deta hai. `selfHeal` chalu karo, to kuch seconds mein replicas wapas vault wale number par aa jaate hain. Hamare test mein haath se hataya hua Service bhi kuch seconds mein wapas aa gaya.

### [10:40 – 13:20] Scene 5: Lab: Pehla Sync aur Drift
**[VISUAL: Apply the `Application`. The tile turns OutOfSync and Missing. Click Sync, it turns Synced and Healthy. Change `replicas` in Git, wait or refresh. Then `kubectl scale` by hand, then `selfHeal: true` added and the number snapping back.]**

**(Voiceover):**
Lab. Upar wala Application apne repo ke URL ke saath `kubectl apply -f` karo. Tile OutOfSync aur Missing dikhegi. Sync dabao: Synced, phir Healthy, aur `kubectl -n atithi get pods` mein do pods. Ab vault mein `replicas` ko teen karo, commit karo, aur refresh dabao ya intezaar karo. Phir `syncPolicy` mein `automated: {prune: true}` jodo. `kubectl -n atithi scale deploy rooms --replicas=5` karo: OutOfSync, par number wahin atka rehta hai. Ab `selfHeal: true` jodo, aur dekho ki number kuch seconds mein teen par wapas. Aakhir mein `kubectl -n atithi delete svc rooms` karo aur dekho ki Service wapas aa jaati hai.

### [13:20 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "Application = where, what, who · Sync vs Health · automated needs prune and selfHeal switches · poll ≈ 3 min, webhook = seconds · drift heals". Then two new folders, `dev` and `prod`, appear in the config vault.]**

**(Voiceover):**
Recap: Application, do alag badge, auto-sync ke do switch, aur drift ka ilaaj. Ab ek asli sawaal: naya version dev se prod tak kaise jaaye, aur kuch kharab ho to wapas kaise aayein.

---

# 📺 EPISODE 3: Naya Version

### [00:00 – 02:10] Scene 1: Naya Edition Label Kahan Se Aata Hai
**[VISUAL: A conveyor from the app vault: test, truck design, scan, depot. A last station "update config vault" opens a pull request that changes one edition label in the config vault. The supervisor then rolls it out. The conveyor has no arrow into the cluster.]**

**(Voiceover):**
GitOps mein naya version aise chalta hai. App vault mein badlaav, foreman ki conveyor test karti hai, truck design banati hai, scan karti hai, aur depot mein edition label ke saath rakhti hai, bilkul Session 31 jaisa. Aakhri station alag hai: wo config vault mein sirf ek line badalta hai, naya edition label, aur ek pull request kholta hai. Chief architect use review karta hai, jaise Session 16B mein. Merge hote hi site supervisor naya label campus par lagata hai. Conveyor ko cluster ki chaabi kabhi nahi chahiye.

### [02:10 – 04:30] Scene 2: Base aur Overlay: Dev aur Prod
**[VISUAL: A folder tree. `base/` with `deployment.yaml`, `service.yaml`, `kustomization.yaml`. `overlays/dev/kustomization.yaml` (replicas 1, wing `atithi-dev`) and `overlays/prod/kustomization.yaml` (replicas 3, wing `atithi-prod`). Two Applications pointing at the two overlay folders.]**

**(Voiceover):**
Dev aur prod mein zyada tar cheezein ek jaisi hoti hain, bas replicas, wing aur edition label alag. Isliye Kustomize: ek `base` folder mein common manifests, aur har environment ka ek chhota overlay. Argo CD Kustomize aur Helm dono ko seedha samajhta hai, kuch extra install nahi karna.
```yaml
# overlays/prod/kustomization.yaml
resources:
  - ../../base
namespace: atithi-prod
replicas:
  - name: rooms
    count: 3
images:
  - name: rooms
    newTag: "1.0.0"
```
`overlays/dev` mein wahi, par `count: 1` aur `namespace: atithi-dev`. Phir do Application, ek `overlays/dev` par aur ek `overlays/prod` par. Edition label sirf `images` mein badalta hai.

### [04:30 – 06:40] Scene 3: Promotion: Pehle Dev, Phir Prod, Diff ke Saath
**[VISUAL: A pull request that changes `newTag` in `overlays/dev`. Dev turns green. A second pull request changes the same line in `overlays/prod`. Before merging, `argocd app diff rooms-prod --refresh` prints the one-line image change.]**

**(Voiceover):**
Promotion ka matlab hai wahi edition label pehle dev mein, aur jab dev theek ho, prod mein. Har step ek pull request: dev ki file badlo, supervisor dev par lagata hai, tum dekhte ho. Phir prod ki file mein wahi ek line, review ke saath. Merge se pehle `argocd app diff rooms-prod --refresh` chalao: wo bilkul batata hai ki campus mein kya badlega, hamare test mein sirf `image: rooms:s22` se `rooms:s31`. Yaani prod mein kya jaa raha hai, ye deploy se pehle review mein dikh jaata hai.

### [06:40 – 09:45] Scene 4: Kharab Release aur Rollback: Git Revert
**[VISUAL: A commit with an edition label that does not exist. The tile says Synced but Progressing, and one new pod is `ImagePullBackOff` while the two old pods still serve guests. `argocd app rollback` refused. Then `git revert` and the tile healing in seconds.]**

**(Voiceover):**
Ab jaan-boojh kar kharab release: edition label jo depot mein hai hi nahi. Application dikhata hai Synced, kyunki campus vault jaisa hi hai, par Health Progressing, kyunki naya pod `ImagePullBackOff` mein hai. Rolling update ki wajah se purane pods abhi guests ko serve kar rahe hain. Synced ka matlab sahi nahi hota, vault jaisa hota hai. Rollback ka natural tareeka vault mein hai: `git revert` aur push. Hamare test mein revert ke kuch seconds baad Application wapas Healthy tha. Ek jaal: `argocd app rollback rooms 1` auto-sync ke saath mana hai, error aata hai ki rollback cannot be initiated when auto-sync is enabled, kyunki supervisor use turant undo kar deta. Isliye rollback hamesha vault ka badlaav hai. `argocd app history rooms` purane syncs ki list dikhata hai.

### [09:45 – 12:10] Scene 5: Secrets Vault Mein Nahi
**[VISUAL: A Kubernetes Secret manifest with a base64 value, crossed out in red in the config vault. Next to it three sealed options: an encrypted secret that only the cluster can open, a reference to a cloud secret manager, and an encrypted file with a team key.]**

**(Voiceover):**
Ek sawaal turant uthta hai: secrets ka kya? Secret ka manifest vault mein plain mat daalo, base64 sirf encoding hai, Session 25 aur Session 20 ki wahi baat. Teen raaste hain, aur teeno alag tool hain jo Argo CD ke saath chalte hain. Encrypted Secret jise sirf cluster khol sake, cloud ke secret manager se padhne wala tool, ya ek encrypted file jo team ki chaabi se khulti hai. Tool ka naam apni team ke saath chuno, aur uska doc padho. Sabka niyam ek hai: config vault mein jo bhi hai, wo public hone par bhi nuksaan na kare.

### [12:10 – 14:25] Scene 6: Lab: Overlay, Promotion aur Revert
**[VISUAL: Restructure the repo into `base` and `overlays`. Two Applications. A commit changing the dev tag. A bad tag in prod, Progressing. `git revert`, Healthy again. `argocd app diff` before a change.]**

**(Voiceover):**
Lab. Config vault ko `base` aur `overlays/dev`, `overlays/prod` mein baanto, jaise upar. Do Application banao. Dono Synced aur Healthy: dev mein ek pod, prod mein teen. Dev ki `newTag` badlo aur dekho ki sirf dev badalta hai. Phir prod ke liye pehle `argocd app diff rooms-prod --refresh`, phir badlao. Ab jaan-boojh kar prod mein `newTag` mein aisa label likho jo depot mein nahi hai. Dekho Synced aur Progressing, `kubectl -n atithi-prod get pods` mein `ImagePullBackOff`. `argocd app rollback` try karke error padho. Phir `git revert HEAD` aur push, aur Healthy wapas aate dekho.

### [14:25 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "conveyor writes the label, never the cluster · base + overlays · promote by pull request · diff before merge · Synced ≠ Healthy · rollback = git revert · no plain secrets". Then a gate with a sign "project" appears at the campus entrance.]**

**(Voiceover):**
Recap: conveyor sirf label likhti hai. Base aur overlay, promotion pull request se, diff pehle, rollback git revert se, aur secrets vault mein plain nahi. Ab supervisor ko kuch limit chahiye: wo kis vault se, kis wing mein, kya laga sakta hai.

---

# 📺 EPISODE 4: Guard Rails

### [00:00 – 02:20] Scene 1: AppProject: Supervisor ki Hadd
**[VISUAL: An `AppProject` card: allowed source repos, allowed destination wings `atithi-*`, allowed object kinds. An Application trying to deploy into `kube-system` is stopped at the gate with the error text.]**

**(Voiceover):**
Supervisor bahut taaqatwar hai, wo campus mein kuch bhi laga sakta hai. Isliye har Application ek project ke andar chalta hai, aur project batata hai: kaun se vault, kaun se wing, aur kaun se object allowed hain. Ye Session 9 ka least privilege hai, Argo CD ke andar.
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AppProject
metadata:
  name: atithi
  namespace: argocd
spec:
  sourceRepos:
    - https://github.com/YOUR_ORG/atithi-config.git
  destinations:
    - server: https://kubernetes.default.svc
      namespace: "atithi-*"
  clusterResourceWhitelist: []
```
Is project mein koi Application `kube-system` mein lagana chahe, to Argo CD mana karta hai: `application destination ... do not match any of the allowed destinations in project 'atithi'`. Default project sab kuch allow karta hai, isliye asli kaam ke liye apna project banao.

### [02:20 – 04:30] Scene 2: ApplicationSet: Ek Template, Kai Application
**[VISUAL: An `ApplicationSet` with a list generator of two elements, `dev` and `prod`, feeding one template. Two Applications appear in the UI. A note: "other generators: Git folders, clusters".]**

**(Voiceover):**
Dev aur prod ke liye do alag Application likhna theek hai. Par das services aur teen environments ho jaayein, to tees file. ApplicationSet ek template aur ek list se Applications khud banata hai:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: rooms
  namespace: argocd
spec:
  generators:
    - list:
        elements:
          - env: dev
          - env: prod
  template:
    metadata:
      name: "rooms-{{env}}"
    spec:
      project: atithi
      source:
        repoURL: https://github.com/YOUR_ORG/atithi-config.git
        targetRevision: main
        path: "overlays/{{env}}"
      destination:
        server: https://kubernetes.default.svc
        namespace: "atithi-{{env}}"
      syncPolicy:
        automated: {prune: true, selfHeal: true}
        syncOptions: [CreateNamespace=true]
```
Hamare test mein `rooms-dev` aur `rooms-prod` is ek file se khud ban gaye. List ke alawa folders ya clusters par bhi generator hota hai.

### [04:30 – 07:10] Scene 3: Kaun Andar Aa Sakta Hai, aur Private Vault
**[VISUAL: The Argo CD login page with SSO through Dex. A read-only deploy key added to the config vault, and the private half in the `argocd` wing as a repository credential. A webhook from the vault to the Argo CD API. A padlock on the API server, not exposed to the internet.]**

**(Voiceover):**
Argo CD ka apna darwaza bhi surakshit rakho. `admin` account sirf shuruat ke liye hai: SSO se login, role ke hisaab se access, aur `admin` ko band karo. UI aur API ko seedha internet par mat kholo; ingress aur HTTPS ke peeche, jaise Session 25 ke concierge mein. Agar config vault private hai, to supervisor ko ek read-only deploy key do, wahi Session 17 ka sabak: sirf padhne ki chaabi, aur wo Argo CD ke repository credential mein. Instant sync chahiye to vault ka webhook Argo CD ke API ko bhejo. Exact steps apne version ke docs mein dekho, kyunki settings badalti rehti hain. Aur Argo CD ki apni settings aur Applications bhi config vault mein rakho, taaki supervisor par bhi wahi review lage jo trucks par lagta hai.

### [07:10 – 09:10] Scene 4: Capstone Mein Kahan Baithta Hai
**[VISUAL: The Session 31 conveyor. The old last station, `deploy.sh` over SSH to an app building, is replaced by "update config vault", then the supervisor syncs and the Health badge confirms. The inspector (Prometheus) and the control room remain unchanged.]**

**(Voiceover):**
Session 31 mein aakhir ka station `deploy.sh` tha: SSH se building par jaao, truck badlo, health check karo. Kubernetes par wahi station config vault ka update ban jaata hai. Conveyor config vault ko clone karta hai, `overlays/dev/kustomization.yaml` mein `newTag` ko naye edition label se badalta hai, commit aur push karta hai. Baaki kaam supervisor ka: naya label lagana, aur health batana. Health check aur rollback ab Argo CD ke Health aur `git revert` mein hain. Control room, yaani Prometheus aur Grafana, jaise the waise rehte hain. Pehle dev par aazmao, aur prod ke liye pull request zaroori rakho.

### [09:10 – 11:25] Scene 5: Kab Nahi, aur Kya Alag Hai
**[VISUAL: A two-column board. Left "Argo CD is good at": Kubernetes manifests, many environments, audit by Git. Right "it is not": building trucks, infrastructure like Terraform's campus, instant deploys without a webhook. Small tags: Flux (another GitOps tool), Argo Rollouts (canary and blue-green).]**

**(Voiceover):**
Argo CD sab kaam ka tool nahi hai. Wo Kubernetes ke manifests lagane mein achha hai, kai environments ke saath, aur har badlaav Git mein record hota hai. Wo truck banata nahi, wo foreman ka kaam hai. Wo campus ki infrastructure, yaani Terraform ka kaam, nahi karta. Aur pull ka matlab hai thodi der: webhook ke bina kuch minute. Do naam jo aap sunoge: Flux, ek aur GitOps tool jo isi vichar par chalta hai, aur Argo Rollouts, jo dheere dheere ya canary rollout deta hai, jaise Session 11 ke weighted target groups, par Kubernetes ke andar. Pehle Argo CD ke yeh basics seekho, phir aage ke tools dekhna.

### [11:25 – 13:55] Scene 6: Lab: Project aur ApplicationSet
**[VISUAL: Apply the `AppProject`. An Application aimed at `kube-system` shows `InvalidSpecError`. Delete the two hand-made Applications and apply the `ApplicationSet`. Two Applications appear, both Synced and Healthy. `kind delete cluster --name argo`.]**

**(Voiceover):**
Lab. Upar wala `AppProject` apply karo. Ek Application banao jo `kube-system` mein lagana chahe, aur dekho ki wo `InvalidSpecError` ke saath ruk jaata hai. Phir do haath se banaye Application hata do, `ApplicationSet` apply karo, aur dekho ki `rooms-dev` aur `rooms-prod` khud ban gaye, dono Synced aur Healthy. Ek aakhri sawaal: prod mein `selfHeal` ke saath aap emergency mein `kubectl edit` karo to kya hoga? Aazma kar dekho, kyunki asli raat ke teen baje yahi sawaal aayega. Hamare test mein hath ka badlaav do second mein wapas ho gaya, aur ApplicationSet wale Application par `argocd app set --sync-policy none` bhi kaam nahi karta, kyunki set use wapas likh deta hai. Emergency ka rasta Git commit hai. Safai: `kind delete cluster --name argo`.

### [13:55 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "vault = truth · supervisor pulls · Sync ≠ Health · rollback = git revert · project limits the supervisor · ApplicationSet = template · no plain secrets". Then a well-read assistant appears beside a designer at head office.]**

**(Voiceover):**
Recap: vault hi sach hai. Supervisor khinchta hai, Sync aur Health alag hain, rollback git revert hai, project supervisor ki hadd tay karta hai, aur ApplicationSet ek template se kai Application banata hai. Ab Atithi ke head office mein ek naya sadasya aata hai: ek bahut padha-likha assistant. Pehle wo ek bahari expert ki tarah phone par jawab dega. Phir ek trained brain ki tarah, jo kisi bhi truck ki tarah chalta hai. Agla session: AI apps aur MLOps.

---

# 📎 Student handout: Session 31B cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| GitOps | Declarative, Git mein, khinchkar lagao, baar baar milao |
| Push vs pull | Push: CI ke paas cluster ki chaabi. Pull: supervisor andar, CI sirf config vault mein likhta hai |
| Do vault | App vault (code) aur config vault (manifests) |
| Install | `kubectl apply -n argocd --server-side --force-conflicts -f .../v3.6.1/manifests/install.yaml`; seedha `apply` par "Too long" |
| Pehla login | `kubectl -n argocd get secret argocd-initial-admin-secret ...`; password badlo, secret hatao |
| UI | `kubectl port-forward svc/argocd-server -n argocd 8080:443` |
| Application | `source` (repo, revision, path), `destination` (cluster, wing), `project` |
| Do badge | Sync Status (Synced, OutOfSync) aur Health (Healthy, Progressing, Degraded, Missing) |
| Auto-sync | `automated`; `prune` aur `selfHeal` alag switch, default band |
| Kitni jaldi | Poll lagbhag teen minute (test mein paanch ke aas paas); webhook seconds |
| Drift | `selfHeal` ke saath haath ka badlaav seconds mein wapas |
| Overlay | `base` + `overlays/dev`, `overlays/prod`; `images: newTag` |
| Promotion | Dev ka pull request, phir prod ka; `argocd app diff NAME --refresh` |
| Rollback | `git revert` aur push; `argocd app rollback` auto-sync ke saath mana |
| Secrets | Vault mein plain nahi; sealed, secret manager ya encrypted file |
| AppProject | Allowed repos, wings aur kinds; galat wing par `InvalidSpecError` |
| ApplicationSet | Ek template + generator se kai Application |
| Safai | `kind delete cluster --name argo`; real cluster ho to usi din hatao |

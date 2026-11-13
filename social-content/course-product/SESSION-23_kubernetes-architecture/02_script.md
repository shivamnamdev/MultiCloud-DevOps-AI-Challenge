# ✍️ 02: SCRIPT — SESSION-23: Kubernetes Architecture
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S23`
- **Focus:** Why orchestration, control plane vs nodes, desired-state reconciliation, kubectl & YAML, local cluster
- **Episodes:**
  - Episode 1: Orchestration kyun: Sau Containers ka Sawaal
  - Episode 2: Cluster Architecture: Control Plane aur Nodes
  - Episode 3: Desired State aur Reconciliation Loop
  - Episode 4: kubectl, YAML aur Apna Local Cluster

---

# 📺 EPISODE 1: Orchestration kyun?

### [00:00 – 01:15] Scene 1: Sau Containers, Ek Insaan
**[VISUAL: An admin at a desk with a wall of 100 containers on 10 servers. Some crash, some are overloaded, one needs an update. Phone buzzing. A "manual" counter overflows.]**

**(Voiceover):**
Ek container chalana aasaan hai. Sau containers, das servers par, aur har ek ko monitor karna? Koi mara to restart, kisi server par load zyada to shift, naya version aaya to bina downtime ke update. Insaan ye sab haath se nahi kar sakta. Container orchestration ka kaam yahi hai, aur duniya ka sabse popular orchestrator Kubernetes hai, jise log K8s bhi kehte hain.

### [01:15 – 05:00] Scene 2: Kubernetes kya Dete Hain
**[VISUAL: Six cards: Scheduling, Self-healing, Scaling, Rolling updates/rollbacks, Service discovery/load balancing, Config & secrets.]**

**(Voiceover):**
Kubernetes chhe cheezein sambhalta hai. Scheduling: kaun sa container kaun se server par chalega. Self-healing: container mara to naya bana do. Scaling: load ke hisaab se kam ya zyada copies. Rolling updates: naya version dheere dheere, aur galat nikla to rollback. Service discovery aur load balancing: containers ek doosre ko dhoondh sakein aur traffic baante. Aur configuration aur secrets ka prabandh. Kubernetes Google ke Borg system se prerit hai aur ab CNCF ke under open source hai.

### [05:00 – 08:30] Scene 3: Kubernetes vs Docker vs Docker Compose
**[VISUAL: A three-row comparison: Docker = build/run one container. Docker Compose = define multi-container app on one machine. Kubernetes = run and manage containers across many machines.]**

**(Voiceover):**
Docker ek container banata aur chalata hai. Docker Compose ek machine par kai containers ki app define karne ke liye achha hai, development ke liye mast. Kubernetes kai machines ke cluster par containers ko chalata aur sambhalta hai. Ye competitors nahi, alag level ke tool hain. Chhote project ke liye Kubernetes overkill ho sakta hai, aur ye sach hai. Seekhne ka maksad ye jaanna hai ki jahan scale aur reliability chahiye, wahan ye kaise kaam karta hai.

### [08:30 – 11:30] Scene 4: Lab: Problem Mehsoos Karo
**[VISUAL: Run 5 containers with Docker. Kill one with `docker kill`. It stays dead. Text: "Nobody restarts it for you unless you tell it to."]**

**(Voiceover):**
Lab: `for i in 1 2 3 4 5; do docker run -d --name w$i nginx:alpine; done`. Ab `docker kill w3` karo aur `docker ps` mein dekho: wo gayab hai, koi use wapas nahi laayega, jab tak aap `--restart` na lagao. Aur ab socho: agar ye sau machines par hota, aur kisi server ke band hone par poori machine ke containers gayab ho jaate? Is dard ko mehsoos karke agle episode mein Kubernetes ka solution dekhenge. Safai: `docker rm -f w1 w2 w3 w4 w5`.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "scale + self-heal + roll out + discover + config · cluster of machines".]**

**(Voiceover):**
Recap: orchestration ka matlab. Ab Kubernetes ke andar jhaankte hain: cluster ke hisse.

---

# 📺 EPISODE 2: Cluster Architecture

### [00:00 – 01:15] Scene 1: Airport ka Control Tower
**[VISUAL: An airport: control tower (control plane) giving instructions to runways and planes (nodes and pods). A flight plan board (desired state).]**

**(Voiceover):**
Kubernetes cluster ko ek airport ki tarah socho. Control tower tay karta hai ki kaun sa jahaz kahan utrega aur kahan jayega. Runways aur gate asli kaam karte hain. Control tower control plane hai, aur runways worker nodes. Dono ko samajhna Kubernetes ki neev hai.

### [01:15 – 05:00] Scene 2: Control Plane ke Hisse
**[VISUAL: A control plane box with four components: kube-apiserver (front door), etcd (database of truth), kube-scheduler (placement), kube-controller-manager (reconcile loops). Optional: cloud-controller-manager.]**

**(Voiceover):**
Control plane mein chaar mukhya hisse. kube-apiserver, jo cluster ka darwaza hai: kubectl, aur sab components isi se baat karte hain. etcd, ek database jisme cluster ki poori state rehti hai, to uska backup bahut zaroori hai. kube-scheduler, jo naye pods ke liye sahi node chunta hai. Aur kube-controller-manager, jo kai controllers chalata hai, jo state ko sahi banaye rakhte hain. Cloud par ek cloud-controller-manager bhi hota hai jo cloud ke load balancers aur disks se baat karta hai.

### [05:00 – 08:30] Scene 3: Worker Node ke Hisse aur Pod
**[VISUAL: A worker node with kubelet (node agent), container runtime (containerd), kube-proxy (networking rules), and several pods. A pod shown as a small box containing one or two containers sharing network and storage.]**

**(Voiceover):**
Worker node par kubelet hota hai, jo control plane ka agent hai aur batata hai ki pods theek chal rahe hain ya nahi. Container runtime, jaise containerd, jo containers chalata hai. Aur kube-proxy, jo Services ke network rules sambhalta hai. Kubernetes seedha container nahi chalata, pod chalata hai: pod ek ya kai containers ka ek chhota group hai jo ek IP aur storage share karte hain. Pod Kubernetes ka sabse chhota deployable unit hai, aur ye naa-sthayi hota hai, yaani mar sakta hai aur naya ban sakta hai.

### [08:30 – 11:30] Scene 4: Lab: Architecture Apne Cluster Mein Dekho
**[VISUAL: `kubectl get nodes -o wide`, `kubectl get pods -n kube-system`, highlighting apiserver, etcd, scheduler, coredns, kube-proxy pods. `kubectl describe node`.]**

**(Voiceover):**
Lab (agla episode ke cluster ke baad bhi kar sakte ho): `kubectl get nodes -o wide` se nodes. `kubectl get pods -n kube-system` mein control plane aur system ke pods dikhte hain: `kube-apiserver`, `etcd`, `kube-scheduler`, `coredns`, `kube-proxy`. `kubectl describe node NODE_NAME` mein dekho node ka capacity, kitne pods chal rahe hain, aur conditions. Managed services jaise GKE mein control plane Google sambhalta hai, isliye kuch pods aapko dikhenge hi nahi.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "apiserver · etcd · scheduler · controllers | kubelet · runtime · kube-proxy | pod = smallest unit".]**

**(Voiceover):**
Recap: control plane aur nodes. Ab Kubernetes ka sabse bada vichar: aap batao kya chahiye, Kubernetes khud karega.

---

# 📺 EPISODE 3: Desired State aur Reconciliation Loop

### [00:00 – 01:15] Scene 1: Thermostat ki Tarah
**[VISUAL: A thermostat set to 24°C. The room warms to 28°C; the AC turns on until it returns to 24°C. Label: "Desired vs Actual".]**

**(Voiceover):**
Thermostat ko aap bolte ho 24 degree. Wo ye nahi poochta ki kaise, bas room ko 24 par rakhta hai: garmi ho to AC chalata hai, thand ho to band. Kubernetes bhi wahi karta hai. Aap batate ho ki aap kya chahte ho, jaise teen copies, aur Kubernetes lagataar use sach banaye rakhta hai.

### [01:15 – 05:00] Scene 2: Declarative vs Imperative
**[VISUAL: Left: imperative steps "start container, start another, if one dies start again". Right: declarative YAML "replicas: 3". A reconciliation loop: observe → compare → act → observe.]**

**(Voiceover):**
Imperative mein aap steps batate ho: ye karo, phir ye karo. Declarative mein aap end result batate ho: "mujhe nginx ke teen pods chahiye." Kubernetes controllers ek loop chalate hain: dekho abhi kya hai, tulna karo ki kya hona chahiye, aur agar farq hai to sudharo. Yahi reconciliation loop hai. Isiliye agar ek pod mar jaye, to controller dekhta hai ki do hain aur teen chahiye, aur ek naya bana deta hai.

### [05:00 – 08:30] Scene 3: Objects, Labels aur Selectors
**[VISUAL: A YAML with `apiVersion`, `kind`, `metadata` (name, labels), `spec`. Pods with labels `app=web`. A Service with selector `app=web` selecting them.]**

**(Voiceover):**
Kubernetes mein har cheez ek object hai, aur har object ke YAML mein chaar hisse: `apiVersion`, `kind`, `metadata` aur `spec`. Labels chhote key-value tag hote hain, jaise `app: web`, jo objects ko pehchaan dete hain. Selectors un labels ke zariye objects ko chunte hain. Isi tarah Service ya Deployment apne pods ko dhoondhte hain, naam se nahi, label se. Ye design kaafi flexible hai, kyunki pods badalte rehte hain, par label wahi rehta hai.

### [08:30 – 11:30] Scene 4: Lab: Pod Mara, Naya Aaya
**[VISUAL: `kubectl create deployment web --image=nginx:alpine --replicas=3`, `kubectl get pods -w`. In another terminal `kubectl delete pod <one>`; a new pod appears within seconds.]**

**(Voiceover):**
Lab: `kubectl create deployment web --image=nginx:alpine --replicas=3`. `kubectl get pods -w` chalaye rakho. Doosre terminal mein ek pod ka naam lekar `kubectl delete pod POD_NAME`. Dekho ki ek pod Terminating ho raha hai aur ek naya Pending se Running ho gaya, aur total teen hi bane. Ye self-healing hai. Ab `kubectl scale deployment web --replicas=5` aur dekho ki do pods aur aaye. Safai: `kubectl delete deployment web`.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "declarative · observe-compare-act · labels + selectors · pods are disposable".]**

**(Voiceover):**
Recap: desired state aur reconciliation. Ab apna cluster banate hain aur kubectl aur YAML se kaam karna seekhte hain.

---

# 📺 EPISODE 4: kubectl, YAML aur Apna Local Cluster

### [00:00 – 01:15] Scene 1: Cluster Ka Remote Control
**[VISUAL: A remote control labelled `kubectl` pointing at a cluster. A config file `~/.kube/config` with contexts. Switching between "minikube", "gke-prod".]**

**(Voiceover):**
`kubectl` Kubernetes ka remote control hai. Ye apiserver se baat karta hai, aur kis cluster se baat karni hai ye `~/.kube/config` mein hota hai, jisme kai contexts ho sakte hain. Production aur test context mein galti se ulta command chalana ek aam disaster hai, isliye hamesha context dekho: `kubectl config current-context`.

### [01:15 – 05:00] Scene 2: Local Cluster ke Options aur Zaroori Commands
**[VISUAL: Local options: minikube, kind, Docker Desktop K8s, k3d. A commands list: `get`, `describe`, `logs`, `exec`, `apply -f`, `delete`, `explain`, `-o yaml`, `-n namespace`.]**

**(Voiceover):**
Seekhne ke liye local cluster banate hain: minikube, kind ya Docker Desktop mein Kubernetes. Commands ka pattern simple hai: `kubectl get` list dikhata hai, `describe` detail aur events, `logs` container ke logs, `exec -it` andar jaane ke liye, `apply -f file.yaml` YAML se banane ya update karne ke liye, aur `delete`. `-n` namespace ke liye, jaise alag alag teams ke alag alag kamre. `kubectl explain pod.spec` se YAML ke fields ke arth built-in milte hain.

### [05:00 – 08:30] Scene 3: Pehla Manifest
**[VISUAL: A `pod.yaml` and a `deployment.yaml` with annotations. `kubectl apply -f deployment.yaml`, `kubectl diff`, and `kubectl get deploy,pods`.]**

**(Voiceover):**
Ek simple Deployment ka YAML:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata: { name: web }
spec:
  replicas: 2
  selector: { matchLabels: { app: web } }
  template:
    metadata: { labels: { app: web } }
    spec:
      containers:
        - name: web
          image: nginx:1.27-alpine
          ports: [{ containerPort: 80 }]
```
`kubectl apply -f deployment.yaml` banata ya update karta hai. YAML ko Git mein rakho, aur `kubectl diff -f` se badlav pehle dekho. Imperative commands seekhne ke liye theek hain, par asli kaam YAML se hota hai.

### [08:30 – 11:30] Scene 4: Lab: Cluster Banao aur Deploy Karo
**[VISUAL: `minikube start` or `kind create cluster`, `kubectl get nodes`, apply the manifest, `kubectl port-forward deploy/web 8080:80`, curl works, `kubectl logs`, `kubectl delete -f`.]**

**(Voiceover):**
Lab: `minikube start` ya `kind create cluster` chalao. `kubectl get nodes` mein Ready dekho. Upar wala manifest `deployment.yaml` mein save karke `kubectl apply -f deployment.yaml`. `kubectl get deploy,pods`. Service ke bina bhi test: `kubectl port-forward deploy/web 8080:80` aur dusre terminal mein `curl localhost:8080`. `kubectl logs deploy/web` se logs. Aakhir mein `kubectl delete -f deployment.yaml`. Ab aapke paas ek asli Kubernetes cluster hai jisme aap bina darr ke prayog kar sakte ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "context check · get/describe/logs/exec/apply · YAML in Git · port-forward for tests".]**

**(Voiceover):**
Recap: kubectl aur YAML. Ab asli workloads: Deployments, Services, scaling, config, aur cloud par GKE. Agle session mein.

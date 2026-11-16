# ✍️ 02: SCRIPT — SESSION-23: Kubernetes Architecture
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`. Author's class notes: `K8s-Handwritten-Notes.md` (applied as in `NOTES_INTEGRATION_MAP_LINUX_K8S.md` section 2).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S23`
- **Focus:** Why orchestration, what Kubernetes gives you, Docker vs Compose vs Kubernetes, managed Kubernetes (GKE, EKS, AKS), control plane (API server, etcd, scheduler, controllers), node (kubelet, container runtime, kube-proxy), what happens when you create a Deployment, desired state and the reconciliation loop, objects (`apiVersion`, `kind`, `metadata`, `spec`, `status`), labels and selectors, `kubectl` and contexts, a local cluster, pods (create, inspect, YAML, dry-run, apply, edit), the READY column, the questions `describe` answers
- **Builds on:** Session 05 (processes, `systemctl`), Session 11 (marshal, health check), Session 14 (private wing), Session 21 and 22 (trucks, truck designs, depot, the `rooms-service` design)
- **Story position:** Zoom level 3, head office. Sau trucks, das buildings: haath se sambhalna mumkin nahi. Chain ka operations command aata hai: aap likhte ho "hamesha paanch rooms-service trucks chalti rehni chahiye", aur command asliyat ko us likhe hue ke barabar rakhta hai.
- **Story words used:** operations command (Kubernetes), reception (API server), master ledger (etcd), allocation officer (scheduler), supervisors (controllers), resident manager (kubelet), parking bay (pod), courtyard (the node's space for bays), truck (container), truck design (image), depot (registry), standing order (Deployment, preview), guest (end user), staff (admin)
- **Lab project:** Atithi's `rooms-service` truck (from Session 22) first as a plain pod in a local cluster, then as the object the operations command keeps alive.
- **Cost rule:** a local cluster (kind, minikube, Docker Desktop) costs nothing but laptop memory. Stop or delete it after the lab. A cloud cluster is billed from the first minute, so cloud labs start in Session 24.
- **Episodes:**
  - Episode 1: Sau Trucks, Ek Insaan: Operations Command kyun
  - Episode 2: Operations Command ke Hisse: Control Plane aur Nodes
  - Episode 3: Likha Hua Sach: Desired State aur Reconciliation Loop
  - Episode 4: Remote Control: kubectl, Local Cluster aur Pehla Pod

---

# 📺 EPISODE 1: Sau Trucks, Ek Insaan

### [00:00 – 02:50] Scene 1: Sau Trucks, Das Buildings
**[VISUAL: An admin at a desk with a wall of one hundred truck icons spread over ten buildings. Some trucks crash, one building is overloaded, one truck needs the new design. A phone buzzes and a "manual" counter overflows.]**

**(Voiceover):**
Pichhle do sessions mein humne rooms-service ki truck design likhi, usse chhota aur surakshit banaya, aur depot mein rakha. Ek truck chalana aasaan hai. Ab Atithi ke paas dus services hain, har ek ki kai trucks, aur das buildings. Koi truck mari to dobara chalao. Kisi building par zyada bojh ho to trucks doosri building mein bhejo. Naya design aaya to bina guests ko roke ek ek karke badlo. Raat ke teen baje koi building gir jaaye, to uski saari trucks ka kya hoga? Insaan ye sab haath se nahi kar sakta. Is kaam ke liye head office ka operations command hai: Kubernetes.

### [02:50 – 06:05] Scene 2: Operations Command Kya Sambhalta Hai
**[VISUAL: Six cards around a command room: Scheduling, Self-healing, Scaling, Rolling updates and rollbacks, Discovery and load balancing, Config and secrets. A small note: "from Google's Borg, now open source under the CNCF".]**

**(Voiceover):**
Operations command chhe kaam sambhalta hai. Placement: kaun si truck kis building ke courtyard mein khadi hogi. Self-healing: truck mari to nayi. Scaling: bheed ke hisaab se kam ya zyada trucks. Rolling updates: naya design ek ek karke, aur galat nikla to rollback. Discovery aur load balancing: trucks ek doosre ko dhoondh sakein aur traffic baante. Aur config aur secrets ka prabandh. Ye sab Session 11 ke marshal, Session 10 ke Auto Scaling aur Session 15 ke alarms ke vichar hain, jo ab trucks ke liye ek hi jagah mil gaye. Kubernetes ka vichar Google ke andar ke Borg system se aaya, aur ab ye CNCF ke under open source hai. Log ise chhote mein K8s bhi kehte hain.

### [06:05 – 09:40] Scene 3: Docker, Compose aur Kubernetes
**[VISUAL: A three-row comparison. Docker: build and run one truck. Compose: describe a small park of trucks in one building. Kubernetes: run and keep alive trucks across many buildings. An honest tag: "small project? Kubernetes can be too much".]**

**(Voiceover):**
Docker ek truck banata aur chalata hai. Compose ek building mein kai trucks ka chhota park define karta hai, development ke liye mast. Kubernetes kai buildings ke cluster par trucks ko chalata, badhata aur zinda rakhta hai. Ye competitors nahi, alag star ke tool hain. Aur sach ye bhi hai ki ek chhoti team ke ek service ke liye Kubernetes bahut bhari cheez ho sakti hai: ek ya do buildings, ek Auto Scaling Group aur ek marshal kaafi ho sakte hain. Hum Kubernetes isliye seekh rahe hain ki jahan scale aur bharose ki zaroorat hai, wahan ye kaise kaam karta hai. Aur ek aur baat: control plane khud chalana mushkil hai, isliye zyadatar log GKE, EKS ya AKS jaisi managed service lete hain, jahan landlord command ka dimaag chalata hai.

### [09:40 – 12:25] Scene 4: Lab: Dard Mehsoos Karo
**[VISUAL: Terminal. Start five containers with a loop, `docker kill w3`, `docker ps` shows only four, and no one brings w3 back. A second take: `docker run --restart unless-stopped` brings it back on the same building, but not after the building is down.]**

**(Voiceover):**
Lab. Pehle problem mehsoos karo. `for i in 1 2 3 4 5; do docker run -d --name w$i nginx:alpine; done`. Phir `docker kill w3` aur `docker ps`: chaar hi bachi, aur koi use wapas nahi laayega. `--restart unless-stopped` ke saath ye ek hi building par ho jaata hai. Ab socho ki poori building band ho jaaye, ya trucks sau hon aur buildings das. Docker ke paas us building ke bahar ki koi khabar hi nahi. Isi khali jagah ko operations command bharta hai. Safai: `docker rm -f w1 w2 w3 w4 w5`. Agle episode mein hum command ke andar jhaankenge.

### [12:25 – 13:05] Scene 5: Recap aur Bridge
**[VISUAL: A card: "place · self-heal · scale · roll out · discover · config · across many buildings · managed control plane in the cloud".]**

**(Voiceover):**
Recap: orchestration ka matlab, aur Kubernetes ke chhe kaam. Ab command ke andar ka daftar dekhte hain: reception, ledger, allocation officer aur supervisors.

---

# 📺 EPISODE 2: Operations Command ke Hisse

### [00:00 – 01:55] Scene 1: Airport ka Control Tower
**[VISUAL: An airport. A control tower (control plane) sending instructions to gates and runways (nodes) where planes (trucks) wait. A flight-plan board labelled "desired state".]**

**(Voiceover):**
Cluster ko ek airport ki tarah socho. Control tower tay karta hai ki kaun sa jahaz kahan utrega aur kahan jayega. Runway aur gate asli kaam karte hain. Control tower control plane hai, aur runway worker nodes. Hamari story mein control plane operations command ka daftar hai, aur node ek building, jiske courtyard mein parking bays hain. Dono ko alag alag samajhna Kubernetes ki neev hai, kyunki jab kuch toote, sabse pehla sawaal yahi hota hai: gadbad daftar mein hai ya building mein?

### [01:55 – 04:35] Scene 2: Control Plane ke Chaar Mukhya Hisse
**[VISUAL: A control-plane box with four parts: kube-apiserver (reception), etcd (master ledger), kube-scheduler (allocation officer), kube-controller-manager (supervisors). An optional fifth: cloud-controller-manager. Arrows show everyone talking only to the API server.]**

**(Voiceover):**
Daftar mein chaar mukhya hisse. kube-apiserver, jo reception hai: kubectl se lekar saare components isi se baat karte hain, aur koi bhi seedha ledger tak nahi jaata. etcd, master ledger: ek database jisme cluster ki poori sachchai rehti hai, kaun si trucks chahiye, kaun si chal rahi hain. Ledger gaya to command andha ho gaya, isliye uska backup sabse zaroori hai, jaise Session 19 mein foreman ke records ka. kube-scheduler, allocation officer: naye bay ke liye sahi building chunta hai. Aur kube-controller-manager, supervisors: kai controllers ek saath chalte hain, jo ledger ko asliyat se milate rehte hain. Cloud par ek cloud-controller-manager bhi hota hai, jo cloud ke load balancers aur disks se baat karta hai.

### [04:35 – 07:05] Scene 3: Node ke Hisse aur Pod
**[VISUAL: A worker node with kubelet (resident manager), a container runtime (containerd), kube-proxy (network rules), and several pods. A pod drawn as a small parking bay with one or two trucks sharing one address and one locker.]**

**(Voiceover):**
Har building, yaani worker node, mein teen cheezein. kubelet, resident manager: wo daftar ka agent hai, jo bay ki list leta hai, trucks chalwata hai aur daftar ko haalat batata hai. Container runtime, jaise containerd, jo asli mein truck chalata hai. Aur kube-proxy, jo Services ke network rules sambhalta hai. Kubernetes seedha truck nahi chalata, wo parking bay chalata hai, jise pod kehte hain. Ek pod mein ek ya kuch tight truck hote hain, jo ek address aur storage share karte hain. Pod sabse chhota deployable unit hai, aur asthayi hai: wo mar sakta hai aur naya ban sakta hai. Isliye kabhi pod ke IP par bharosa mat karo.

### [07:05 – 10:00] Scene 4: Ek Order ka Safar
**[VISUAL: A flow diagram. `kubectl create deployment` → API server (authenticate, validate) → master ledger records the order → the Deployment controller creates a ReplicaSet → ReplicaSet controller creates pod objects → scheduler picks a node for each → kubelet on that node tells the runtime to start the truck → kubelet reports status back. Each step numbered.]**

**(Voiceover):**
Ek order ka poora safar dekho. Aap `kubectl create deployment` likhte ho. Ek: reception aapko pehchanta hai, jaanchta hai, aur order master ledger mein likh deta hai. Do: supervisors ledger padhte hain, aur Deployment ke liye ek ReplicaSet banate hain, phir ReplicaSet ke liye pod objects. Teen: allocation officer har naye bay ke liye ek building chunta hai, resources dekhkar. Chaar: us building ka resident manager dekhta hai ki mere naam ka ek naya bay hai, aur runtime se truck chalwata hai. Paanch: wo ledger mein status wapas likhta hai. Ek baat dhyaan dene wali: koi bhi ek doosre ko seedha order nahi deta. Sab reception ke raaste ledger se baat karte hain. Isi liye debugging mein "kis step par atka?" ka jawab events se milta hai.

### [10:00 – 12:55] Scene 5: Jab Daftar Girta Hai
**[VISUAL: A split picture. Left: the control plane goes down; existing trucks keep running but nothing new is placed and a dead truck is not replaced. Right: a node goes down; the supervisors notice its resident manager has gone quiet and recreate its pods on other nodes.]**

**(Voiceover):**
Do alag haadse alag asar rakhte hain. Agar control plane gir jaaye, to jo trucks chal rahi hain wo chalti rehti hain, kyunki resident manager apna kaam jaanta hai. Par nayi truck ke liye bay nahi ban sakta, scaling ruk jaati hai, aur mari hui truck wapas nahi aati. Isliye production mein control plane ke kai copies chalte hain, aksar teen, aur managed service mein landlord ye sambhalta hai. Agar ek building gir jaaye, to supervisors dekhte hain ki uske resident manager ki awaaz aani band ho gayi, kuch der intezaar karte hain, aur phir us building ke bays ko doosri buildings mein dobara banate hain. Ye tabhi chalega jab doosri buildings mein jagah ho, jo Session 11 ke "tower" ki soch hai: do towers mein phailao.

### [12:55 – 15:00] Scene 6: Lab: Apne Cluster mein Command ko Dekho
**[VISUAL: Terminal on a running cluster: `kubectl get nodes -o wide`, `kubectl get pods -n kube-system`, highlighting kube-apiserver, etcd, kube-scheduler, kube-controller-manager, coredns, kube-proxy. `kubectl describe node NODE` showing capacity, allocatable, conditions, and non-terminated pods.]**

**(Voiceover):**
Lab. Ye episode agle episode ke cluster ke baad bhi kar sakte ho. `kubectl get nodes -o wide` mein nodes, unka IP aur version. `kubectl get pods -n kube-system` mein control plane aur system ke pods: `kube-apiserver`, `etcd`, `kube-scheduler`, `kube-controller-manager`, `coredns`, `kube-proxy`. `kubectl describe node NODE_NAME` mein capacity, allocatable, conditions, aur node par chalte pods dekho. Allocatable aur capacity ka farq: kuch hissa system ke liye rakha jaata hai. GKE jaise managed cluster mein control plane ke pods aapko dikhenge hi nahi, kyunki wo landlord ke daftar mein hain.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "reception (apiserver) · master ledger (etcd) · allocation officer (scheduler) · supervisors (controllers) | resident manager (kubelet) · runtime · kube-proxy | pod = parking bay · everyone talks through the reception".]**

**(Voiceover):**
Recap: control plane, node, pod, aur ek order ka safar. Ab Kubernetes ka sabse bada vichar: aap likho kya chahiye, command khud karega.

---

# 📺 EPISODE 3: Likha Hua Sach

### [00:00 – 01:50] Scene 1: Thermostat ki Tarah
**[VISUAL: A thermostat set to 24 degrees. The room warms to 28 and the AC turns on until it is back to 24. Two labels: "desired" and "actual". A second picture: a standing board "5 rooms-service trucks always".]**

**(Voiceover):**
Thermostat ko aap bolte ho 24 degree. Wo ye nahi poochta ki kaise. Garmi ho to AC chalata hai, thand ho to band. Kubernetes bhi yahi karta hai. Aap batate ho ki aap kya chahte ho, jaise paanch rooms-service trucks, aur command lagataar use sach banaye rakhta hai. Isi ko desired state kehte hain, aur jo asli mein chal raha hai use actual state. Command ka poora kaam in dono ka farq mitana hai.

### [01:50 – 04:30] Scene 2: Declarative vs Imperative aur Loop
**[VISUAL: Left: imperative steps "start a truck, start another, if one dies start again". Right: declarative file "replicas: 3". A loop in the centre: observe → compare → act → observe.]**

**(Voiceover):**
Imperative mein aap steps batate ho: ye karo, phir ye karo, aur agar wo mare to phir ye karo. Declarative mein aap end result likhte ho: "mujhe rooms-service ki teen trucks chahiye." Controllers ek loop chalate hain: dekho abhi kya hai, tulna karo ki kya hona chahiye, farq ho to sudharo. Isi ko reconciliation loop kehte hain. Isi liye ek pod mara to controller dekhta hai ki do hain aur teen chahiye, aur ek naya bana deta hai, bina kisi ke kahe. Ye wahi aadat hai jo Session 7 ke boto3 mein aur aage Terraform mein dikhegi: pehle batao ki kya chahiye, phir tool ko farq nikaalne do.

### [04:30 – 07:00] Scene 3: Object ke Chaar Hisse
**[VISUAL: A YAML on screen with four coloured parts: `apiVersion`, `kind`, `metadata` (name, labels, namespace), `spec`. A fifth part, `status`, shown in grey, "written by the command, not by you". Tools: `kubectl explain pod.spec.containers` and `kubectl api-resources | grep replicaset`.]**

**(Voiceover):**
Kubernetes mein har cheez ek object hai, aur har object ke YAML mein chaar hisse. `apiVersion`: kaun si API ka hissa, jaise pod ke liye `v1` aur Deployment ke liye `apps/v1`. `kind`: object ka type. `metadata`: naam, labels, namespace. `spec`: aap kya chahte ho. Ek paanchva hissa `status` hai, jo command khud likhta hai: actual kya hai. Ise aap nahi likhte. Agar kisi kind ka `apiVersion` yaad na ho, to `kubectl api-resources | grep replicaset` batata hai `apps/v1`. Aur har field ka matlab `kubectl explain pod.spec.containers` se built-in milta hai, bina Google kiye. Ye do commands YAML likhte waqt sabse bade dost hain.

### [07:00 – 09:30] Scene 4: Labels aur Selectors
**[VISUAL: Pods with labels `app=rooms` and `tier=web`. A Service and a ReplicaSet each with a selector `app=rooms` pulling in only matching pods. A pod with a mismatched label left out.]**

**(Voiceover):**
Labels chhote key-value tag hain, jaise `app: rooms`. Selector un labels ke zariye objects ko chunta hai. Isi tarah ReplicaSet apne pods ko pehchanta hai, aur Service apne pods ko, naam se nahi, label se. Ye design bahut flexible hai: pods badalte rehte hain, par label wahi rehta hai. Ek chhota jaal bhi hai. Agar selector aur pod ke label mein ek akshar ka bhi farq ho, to Service ya ReplicaSet use dekh hi nahi paata, aur koi error bhi nahi aata. Wo sirf chupchap khaali rehta hai. Isliye "kuch nahi ho raha" wale haalat mein pehle labels mila kar dekho.

### [09:30 – 12:25] Scene 5: create, apply, replace
**[VISUAL: A table. `create -f`: fails if the object exists. `apply -f`: creates or updates, remembers your intent. `replace -f`: swaps the object for the file, fails if it does not exist. `delete -f`: removes what the file describes. A "diff" preview: `kubectl diff -f`.]**

**(Voiceover):**
YAML ko cluster tak pahunchane ke teen tareeke. `kubectl create -f` naya object banata hai, aur wo pehle se ho to error deta hai. `kubectl apply -f` banata bhi hai aur update bhi karta hai, aur ye aapke likhe hue ko yaad rakhta hai, isliye roz ke kaam ke liye wahi sahi hai. `kubectl replace -f` purane object ko file se badal deta hai, aur object na ho to fail hota hai. Hatane ke liye `kubectl delete -f file.yaml`, jo wahi object hatata hai jo file mein likha hai. Aur kuch badalne se pehle `kubectl diff -f file.yaml` dikha deta hai ki kya badlega. File vault mein hogi, aur badlaav pull request se, jaise Session 17 ki Jenkinsfile.

### [12:25 – 15:05] Scene 6: Lab: Pod Mara, Naya Aaya
**[VISUAL: `kubectl create deployment rooms --image=nginx:alpine --replicas=3`; `kubectl get pods -w` in one terminal; `kubectl delete pod POD` in another; a new pod appears within seconds. Then `kubectl scale deployment rooms --replicas=5` and `kubectl get deployment rooms`.]**

**(Voiceover):**
Lab. `kubectl create deployment rooms --image=nginx:alpine --replicas=3`. Ek terminal mein `kubectl get pods -w` chalaye rakho. Doosre mein ek pod ka naam lekar `kubectl delete pod POD_NAME`. Dekho: ek pod Terminating hota hai, ek naya Pending se Running hota hai, aur total teen hi rehte hain. Ye self-healing hai, aur ye wahi loop hai jo abhi samjha. Ab `kubectl scale deployment rooms --replicas=5` aur dekho ki do aur aaye. Phir pod ke labels dekhne ke liye `kubectl get pods --show-labels`, aur ek pod ka label `kubectl label pod POD app=other --overwrite` se badalo: Deployment use apna maanna chhod dega, aur ek naya bana dega. Safai: `kubectl delete deployment rooms`.

### [15:05 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "desired vs actual · observe, compare, act · apiVersion / kind / metadata / spec (+ status) · labels and selectors · apply for daily use · diff before apply".]**

**(Voiceover):**
Recap: desired state, objects, labels, aur create, apply, replace. Ab apna cluster banate hain, aur kubectl se pehla pod chalate hain.

---

# 📺 EPISODE 4: Remote Control

### [00:00 – 02:00] Scene 1: Cluster ka Remote
**[VISUAL: A remote control labelled `kubectl` pointing at a cluster. A file `~/.kube/config` with three contexts: `kind-lab`, `gke-staging`, `eks-prod`. A red label on the wrong context.]**

**(Voiceover):**
`kubectl` command ka remote control hai. Wo reception, yaani API server, se baat karta hai, aur kis cluster se baat karni hai, ye `~/.kube/config` mein likha hota hai, jisme kai contexts ho sakte hain: ek lab ka, ek staging ka, ek production ka. Sabse aam disaster: production ke context par lab wali delete command chal jaana. Isliye command chalane se pehle context dekho: `kubectl config current-context`. Aur ek achhi aadat: production context ke naam ko lal rang ke prompt mein dikhao, aur `kubectl config use-context` se jaan boojh kar badlo.

### [02:00 – 04:10] Scene 2: Local Cluster aur Command ka Pattern
**[VISUAL: Local cluster options in a row: kind, minikube, Docker Desktop Kubernetes, k3d. A commands list: `get`, `describe`, `logs`, `exec -it`, `apply -f`, `delete`, `explain`, `-o wide`, `-o yaml`, `-n`.]**

**(Voiceover):**
Seekhne ke liye local cluster banate hain: kind, minikube, ya Docker Desktop ka Kubernetes. Commands ka pattern aasan hai. `kubectl get` list dikhata hai. `describe` ek object ki poori detail aur sabse neeche Events. `logs` truck ke logs. `exec -it` andar jaane ke liye. `apply -f` YAML se banane ya badalne ke liye, aur `delete`. `-o wide` extra columns, `-o yaml` poora object, aur `-n` namespace ke liye. Ye pattern har resource par ek jaisa chalta hai: `kubectl get pods`, `get deployments`, `get services`. Aur `kubectl get all` ek namespace ki badi cheezein ek saath dikhata hai.

### [04:10 – 06:25] Scene 3: Pehla Pod: Teen Tareeke
**[VISUAL: Three ways side by side. 1: `kubectl run rooms --image=nginx:alpine`. 2: `kubectl run rooms --image=nginx:alpine --dry-run=client -o yaml > rooms-pod.yaml`. 3: the YAML opened, edited, then `kubectl apply -f rooms-pod.yaml`. A note: "dry-run=client builds the object but does not create it".]**

**(Voiceover):**
Pod banane ke teen tareeke. Seedha: `kubectl run rooms --image=nginx:alpine`, jahan `rooms` pod ka naam aur `--image` truck design. Doosra: YAML haath se likhne ki jagah kubectl se banwao: `kubectl run rooms --image=nginx:alpine --dry-run=client -o yaml > rooms-pod.yaml`. `--dry-run=client` object banata hai par cluster mein rakhta nahi, aur `-o yaml` use YAML mein likhta hai. Teesra: us file ko kholo, jo badalna ho badlo, aur `kubectl apply -f rooms-pod.yaml`. YAML file ko manifest bhi kehte hain. Ye dry-run wali trick roz kaam aati hai, kyunki khaali page se YAML likhne se behtar hai ki kubectl ka likha hua dhancha badlo.

### [06:25 – 09:15] Scene 4: Pod ko Padhna: describe aur READY
**[VISUAL: `kubectl get pods -o wide` with columns NAME, READY, STATUS, RESTARTS, AGE, IP, NODE. A pod with READY `1/2`. A table: "Which node?" → NODE column; "How many containers?" → `Containers:`; "Which images?" → `Image:`; "State of container X?" → `State:`; "Why in error?" → Events at the bottom.]**

**(Voiceover):**
`kubectl get pods -o wide` ke columns: NAME, READY, STATUS, RESTARTS, AGE, IP aur NODE. NODE column bataata hai ki pod kis building mein hai, aur sabse tez tareeka wahi hai. READY mein `x/y` hota hai: y pod ke andar kitne trucks hain, aur x mein se kitne chal rahe hain. Matlab `1/2` ka arth hai ki pod mein do trucks hain aur ek hi chal rahi hai. READY pods ki ginti nahi hai. Ab `kubectl describe pod rooms`: usme image, state, mounts, conditions, aur sabse neeche Events ki table: Type, Reason, Age, From, Message. Kuch galat ho to pehle wahi dekho. Kaun si building, kitne trucks, kaun si images, kis truck ki kya state, aur kyun error: pichhle paanch sawaalon ke jawab describe mein hain.

### [09:15 – 11:40] Scene 5: Pod Badalna aur Hatana
**[VISUAL: A diff of the YAML changing `image: nginx:alpine` to `image: nginx:1.27-alpine`, then `kubectl apply -f rooms-pod.yaml`. A second panel: `kubectl edit pod rooms` opens an editor and prints `pod/rooms edited`. A note: "only a few pod fields can change in place, such as the image".]**

**(Voiceover):**
Pod ka image badalne ke do tareeke. Ek: YAML mein image ka naam badlo aur `kubectl apply -f rooms-pod.yaml`. Do: chalte object ko seedha badlo, `kubectl edit pod rooms`, jo pod ka YAML kholta hai, aur save karne par `pod/rooms edited` likhta hai. Dhyaan: ek chalte pod mein sirf kuch hi fields badal sakte hain, jaise image. Baaki ke liye pod ko hatana aur dobara banana padta hai. Isiliye asli kaam mein hum pod ko seedha nahi, Deployment ke zariye chalate hain, jo agle session mein aayega: wo image badalne par khud naya pod banata hai aur purana hatata hai. Hatane ke liye `kubectl delete pod rooms`.

### [11:40 – 14:40] Scene 6: Lab: Cluster Banao aur Pehla Pod Chalao
**[VISUAL: `kind create cluster --name lab`, `kubectl config current-context`, `kubectl get nodes`, `docker build -t rooms:slim .`, `kind load docker-image rooms:slim --name lab`, a pod YAML with `imagePullPolicy: IfNotPresent`, `kubectl apply`, `kubectl port-forward pod/rooms 8080:5000`, `curl localhost:8080/health`.]**

**(Voiceover):**
Lab. `kind create cluster --name lab`, ya `minikube start`, ya Docker Desktop mein Kubernetes on karo. `kubectl config current-context` se pakka karo ki aap lab cluster par ho. `kubectl get nodes` mein Ready dekho. Ab Session 22 ka `rooms:slim` design lo. Local cluster ko usse dene ke liye `kind load docker-image rooms:slim --name lab`, ya minikube mein `minikube image load rooms:slim`. Pod YAML `kubectl run rooms --image=rooms:slim --dry-run=client -o yaml` se banao, usme `imagePullPolicy: IfNotPresent` jodo, aur `kubectl apply -f`. Ek jaal: tag `latest` ho to Kubernetes har baar depot se khichna chahta hai, aur local design milta nahi. Phir `kubectl port-forward pod/rooms 8080:5000` aur dusre terminal mein `curl localhost:8080/health`. `describe` ke Events mein pod ki poori kahani padho. Safai: `kubectl delete pod rooms`, aur cluster band: `kind delete cluster --name lab`.

### [14:40 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "check the context · kind / minikube / Docker Desktop · run, dry-run → YAML, apply · READY = running trucks / total trucks · describe → Events at the bottom · image is one of few editable fields".]**

**(Voiceover):**
Recap: kubectl, local cluster, pehla pod, aur describe ke sawaal. Par pod akela asthayi hai. Agle session mein asli workloads: pod ki sehat aur exit code, standing orders, extension numbers, wings, aur cloud par GKE.

---

# 📎 Student handout: Session 23 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Kubernetes ke kaam | Placement, self-healing, scaling, rolling update, discovery, config |
| Docker / Compose / K8s | Ek truck / ek building ka park / kai buildings ka cluster |
| Control plane | apiserver (reception), etcd (ledger), scheduler, controller-manager |
| Node | kubelet, container runtime, kube-proxy |
| Pod | Sabse chhota unit; ek ya kuch tight trucks; asthayi; IP par bharosa nahi |
| Control plane gir jaye | Chalti trucks chalti hain; naya kuch nahi, mari wapas nahi |
| Desired vs actual | Likho kya chahiye; loop farq mitata hai |
| Object | `apiVersion`, `kind`, `metadata`, `spec` (+ `status`) |
| YAML ki madad | `kubectl explain`, `kubectl api-resources \| grep <kind>` |
| Labels | Selector se chuno; ek akshar ka farq = chupchap khaali |
| create / apply / replace | Naya / banao ya badlo (roz) / file se badlo |
| Pehle dekho | `kubectl diff -f`; `current-context` |
| Pod banana | `kubectl run <naam> --image=<design>`; `--dry-run=client -o yaml > file` |
| READY | Chalti trucks / kul trucks pod mein, pods ki ginti nahi |
| `describe` | Image, state, conditions; neeche Events |
| Pod badalna | `apply` ya `kubectl edit pod`; kuch hi fields badalte hain |
| Local image | `kind load docker-image` / `minikube image load`; `imagePullPolicy` |
| Safai | `kubectl delete`, `kind delete cluster` |

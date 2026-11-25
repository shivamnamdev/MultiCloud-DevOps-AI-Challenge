# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-23_kubernetes-architecture

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,598 · **Episodes:** 4

---

# EPISODE 1: Sau Trucks, Ek Insaan

## Sau Trucks, Das Buildings

Pichhle do sessions mein humne rooms-service ki truck design likhi, usse chhota aur surakshit banaya, aur depot mein rakha. Ek truck chalana aasaan hai. Ab Atithi ke paas dus services hain, har ek ki kai trucks, aur das buildings. Koi truck mari to dobara chalao. Kisi building par zyada bojh ho to trucks doosri building mein bhejo. Naya design aaya to bina guests ko roke ek ek karke badlo. Raat ke teen baje koi building gir jaaye, to uski saari trucks ka kya hoga? Insaan ye sab haath se nahi kar sakta. Is kaam ke liye head office ka operations command hai: Kubernetes.

## Operations Command Kya Sambhalta Hai

Operations command chhe kaam sambhalta hai. Placement: kaun si truck kis building ke courtyard mein khadi hogi. Self-healing: truck mari to nayi. Scaling: shaadi ke season mein zyada trucks, baad mein kam. Rolling updates: naya design ek ek karke, jaise hotel khula rakh kar floor by floor renovation, aur galat nikla to rollback. Discovery aur load balancing: trucks ek doosre ko dhoondh sakein aur traffic baante. Aur config aur secrets ka prabandh. Ye sab Session 11 ke marshal, Session 10 ke Auto Scaling aur Session 15 ke alarms ke vichar hain, jo ab trucks ke liye ek hi jagah mil gaye. Kubernetes ka vichar Google ke andar ke Borg system se aaya, aur ab ye CNCF ke under open source hai.

## Docker, Compose aur Kubernetes

Docker ek truck banata aur chalata hai. Compose ek building mein kai trucks ka chhota park define karta hai, development ke liye mast. Kubernetes kai buildings ke cluster par trucks ko chalata, badhata aur zinda rakhta hai. Ye competitors nahi, alag star ke tool hain. Aur sach ye bhi hai ki ek chhoti team ke ek service ke liye Kubernetes bahut bhari cheez ho sakti hai: ek ya do buildings, ek Auto Scaling Group aur ek marshal kaafi ho sakte hain. Hum Kubernetes isliye seekh rahe hain ki jahan scale aur bharose ki zaroorat hai, wahan ye kaise kaam karta hai. Aur ek aur baat: control plane khud chalana mushkil hai, isliye zyadatar log GKE, EKS ya AKS jaisi managed service lete hain, jahan landlord command ka dimaag chalata hai.

## Lab: Dard Mehsoos Karo

Lab. Pehle problem mehsoos karo. for i in 1 2 3 4 5; do docker run -d --name w$i nginx:alpine; done. Phir docker kill w3 aur docker ps: chaar hi bachi, aur koi use wapas nahi laayega. --restart unless-stopped crash par truck wapas laata hai: humne sh -c 'sleep 3; exit 1' wali truck ko do baar wapas aate dekha. Par docker kill se roki hui truck wapas nahi aati, aur ye sab sirf usi ek building par hota hai. Ab socho ki poori building band ho jaaye, ya trucks sau hon aur buildings das. Docker ke paas us building ke bahar ki koi khabar hi nahi. Isi khali jagah ko operations command bharta hai. Safai: docker rm -f w1 w2 w3 w4 w5. Agle episode mein hum command ke andar jhaankenge.

## Recap aur Bridge

Recap: orchestration ka matlab, aur Kubernetes ke chhe kaam. Ab command ke andar ka daftar dekhte hain: reception, ledger, allocation officer aur supervisors.

---

# EPISODE 2: Operations Command ke Hisse

## Airport ka Control Tower

Cluster ko ek airport ki tarah socho. Control tower tay karta hai ki kaun sa jahaz kahan utrega aur kahan jayega. Runway aur gate asli kaam karte hain. Control tower control plane hai, aur runway worker nodes. Hamari story mein control plane operations command ka daftar hai, aur node ek building, jiske courtyard mein parking bays hain. Dono ko alag alag samajhna Kubernetes ki neev hai, kyunki jab kuch toote, sabse pehla sawaal yahi hota hai: gadbad daftar mein hai ya building mein?

## Control Plane ke Chaar Mukhya Hisse

Daftar mein chaar mukhya hisse. kube-apiserver, jo reception hai: kubectl se lekar saare components isi se baat karte hain, aur koi bhi seedha ledger tak nahi jaata. etcd, master ledger: ek database jisme cluster ki poori sachchai rehti hai, kaun si trucks chahiye, kaun si chal rahi hain. Ledger gaya to command andha ho gaya, isliye uska backup sabse zaroori hai, jaise Session 19 mein foreman ke records ka. kube-scheduler, allocation officer: naye bay ke liye sahi building chunta hai. Aur kube-controller-manager, supervisors: kai controllers ek saath chalte hain, jo ledger ko asliyat se milate rehte hain. Cloud par ek cloud-controller-manager bhi hota hai, jo cloud ke load balancers aur disks se baat karta hai.

## Node ke Hisse aur Pod

Har building, yaani worker node, mein teen cheezein. kubelet, resident manager: wo daftar ka agent hai, jo bay ki list leta hai, trucks chalwata hai aur daftar ko haalat batata hai. Container runtime, jaise containerd, jo asli mein truck chalata hai. Aur kube-proxy, jo Services ke network rules sambhalta hai. Kubernetes seedha truck nahi chalata, wo parking bay chalata hai, jise pod kehte hain. Ek pod mein ek ya kuch tight truck hote hain, jo ek address aur storage share karte hain. Pod sabse chhota deployable unit hai, aur asthayi hai: wo mar sakta hai aur naya ban sakta hai. Isliye kabhi pod ke IP par bharosa mat karo.

## Ek Order ka Safar

Ek order ka poora safar dekho. Aap kubectl create deployment likhte ho. Ek: reception aapko pehchanta hai, jaanchta hai, aur order master ledger mein likh deta hai. Do: supervisors ledger padhte hain, aur Deployment ke liye ek ReplicaSet banate hain, phir ReplicaSet ke liye pod objects. Teen: allocation officer har naye bay ke liye ek building chunta hai, resources dekhkar. Chaar: us building ka resident manager dekhta hai ki mere naam ka ek naya bay hai, aur runtime se truck chalwata hai. Paanch: wo ledger mein status wapas likhta hai. Ek baat dhyaan dene wali: koi bhi ek doosre ko seedha order nahi deta. Sab reception ke raaste ledger se baat karte hain. Isi liye debugging mein "kis step par atka?" ka jawab events se milta hai.

## Jab Daftar Girta Hai

Do alag haadse alag asar rakhte hain. Agar control plane gir jaaye, to jo trucks chal rahi hain wo chalti rehti hain, kyunki resident manager apna kaam jaanta hai. Par nayi truck ke liye bay nahi ban sakta, scaling ruk jaati hai, aur mari hui truck wapas nahi aati. Isliye production mein control plane ke kai copies chalte hain, aksar teen, aur managed service mein landlord ye sambhalta hai. Agar ek building gir jaaye, to supervisors dekhte hain ki uske resident manager ki awaaz aani band ho gayi, kuch der intezaar karte hain, aur phir us building ke bays ko doosri buildings mein dobara banate hain. Humne lab mein building band ki: lagbhag pachaas second baad node NotReady dikhi, aur naye pods lagbhag chhe minute baad doosri building par aaye. Tab tak purane pods Running hi dikhte rahe. Ye tabhi chalega jab doosri buildings mein jagah ho, jo Session 11 ke "tower" ki soch hai: do towers mein phailao.

## Lab: Apne Cluster mein Command ko Dekho

Lab. Ye episode agle episode ke cluster ke baad bhi kar sakte ho. kubectl get nodes -o wide mein nodes, unka IP aur version. kubectl get pods -n kube-system mein control plane aur system ke pods: kube-apiserver, etcd, kube-scheduler, kube-controller-manager, coredns, kube-proxy. kubectl describe node NODE_NAME mein capacity, allocatable, conditions, aur node par chalte pods dekho. Allocatable aur capacity ka farq: kuch hissa system ke liye rakha jaata hai, par kind mein dono barabar dikhte hain. Aur kind mein kindnet ka bhi ek pod har node par hai, jo network ka plugin hai. GKE jaise managed cluster mein control plane ke pods aapko dikhenge hi nahi, kyunki wo landlord ke daftar mein hain.

## Recap aur Bridge

Recap: control plane, node, pod, aur ek order ka safar. Ab Kubernetes ka sabse bada vichar: aap likho kya chahiye, command khud karega.

---

# EPISODE 3: Likha Hua Sach

## Thermostat ki Tarah

Thermostat ko aap bolte ho 24 degree. Wo ye nahi poochta ki kaise. Garmi ho to AC chalata hai, thand ho to band. Kubernetes bhi yahi karta hai. Aap batate ho ki aap kya chahte ho, jaise paanch rooms-service trucks, aur command lagataar use sach banaye rakhta hai. Isi ko desired state kehte hain, aur jo asli mein chal raha hai use actual state. Command ka poora kaam in dono ka farq mitana hai.

## Declarative vs Imperative aur Loop

Imperative mein aap steps batate ho: ye karo, phir ye karo, aur agar wo mare to phir ye karo. Declarative mein aap end result likhte ho: "mujhe rooms-service ki teen trucks chahiye." Controllers ek loop chalate hain: dekho abhi kya hai, tulna karo ki kya hona chahiye, farq ho to sudharo. Isi ko reconciliation loop kehte hain. Isi liye ek pod mara to controller dekhta hai ki do hain aur teen chahiye, aur ek naya bana deta hai, bina kisi ke kahe. Ye wahi aadat hai jo Session 7 ke boto3 mein aur aage Terraform mein dikhegi: pehle batao ki kya chahiye, phir tool ko farq nikaalne do.

## Object ke Chaar Hisse

Kubernetes mein har cheez ek object hai, aur har object ke YAML mein chaar hisse. apiVersion: kaun si API ka hissa, jaise pod ke liye v1 aur Deployment ke liye apps/v1. kind: object ka type. metadata: naam, labels, namespace. spec: aap kya chahte ho. Ek paanchva hissa status hai, jo command khud likhta hai: actual kya hai. Ise aap nahi likhte. Agar kisi kind ka apiVersion yaad na ho, to kubectl api-resources | grep replicaset batata hai apps/v1. Aur har field ka matlab kubectl explain pod.spec.containers se built-in milta hai, bina Google kiye. Ye do commands YAML likhte waqt sabse bade dost hain.

## Labels aur Selectors

Labels chhote key-value tag hain, jaise app: rooms. Selector un labels ke zariye objects ko chunta hai. Isi tarah ReplicaSet apne pods ko pehchanta hai, aur Service apne pods ko, naam se nahi, label se. Ye design bahut flexible hai: pods badalte rehte hain, par label wahi rehta hai. Ek chhota jaal bhi hai. Agar selector aur pod ke label mein ek akshar ka bhi farq ho, to Service ya ReplicaSet use dekh hi nahi paata, aur koi error bhi nahi aata. Wo sirf chupchap khaali rehta hai. Isliye "kuch nahi ho raha" wale haalat mein pehle labels mila kar dekho.

## create, apply, replace

YAML ko cluster tak pahunchane ke teen tareeke. kubectl create -f naya object banata hai, aur wo pehle se ho to error deta hai. kubectl apply -f banata bhi hai aur update bhi karta hai, aur ye aapke likhe hue ko yaad rakhta hai, isliye roz ke kaam ke liye wahi sahi hai. kubectl replace -f purane object ko file se badal deta hai, aur object na ho to fail hota hai. Hatane ke liye kubectl delete -f file.yaml, jo wahi object hatata hai jo file mein likha hai. Aur kuch badalne se pehle kubectl diff -f file.yaml dikha deta hai ki kya badlega. File vault mein hogi, aur badlaav pull request se, jaise Session 17 ki Jenkinsfile. Field ka matlab bhool jao to kubectl explain pod.spec.containers cluster se seedha batata hai, aur kubectl api-resources har object ka naam aur short form, jaise po, deploy, svc. Ye dono commands lab aur interview, dono mein kaam aate hain.

## Lab: Pod Mara, Naya Aaya

Lab. kubectl create deployment rooms --image=nginx:alpine --replicas=3. Ek terminal mein kubectl get pods -w chalaye rakho. Doosre mein ek pod ka naam lekar kubectl delete pod POD_NAME. Dekho: ek pod Terminating hota hai, ek naya Pending se Running hota hai, aur total teen hi rehte hain. Ye self-healing hai, aur ye wahi loop hai jo abhi samjha. Ab kubectl scale deployment rooms --replicas=5 aur dekho ki do aur aaye. Phir pod ke labels dekhne ke liye kubectl get pods --show-labels, aur ek pod ka label kubectl label pod POD app=other --overwrite se badalo: Deployment use apna maanna chhod dega, aur ek naya bana dega. Safai: kubectl delete deployment rooms.

## Recap aur Bridge

Recap: desired state, objects, labels, aur create, apply, replace. Ab apna cluster banate hain, aur kubectl se pehla pod chalate hain.

---

# EPISODE 4: Remote Control

## Cluster ka Remote

kubectl command ka remote control hai. Wo reception, yaani API server, se baat karta hai, aur kis cluster se baat karni hai, ye ~/.kube/config mein likha hota hai, jisme kai contexts ho sakte hain: ek lab ka, ek staging ka, ek production ka. Sabse aam disaster: production ke context par lab wali delete command chal jaana. Isliye command chalane se pehle context dekho: kubectl config current-context. Aur ek achhi aadat: production context ke naam ko lal rang ke prompt mein dikhao, aur kubectl config use-context se jaan boojh kar badlo.

## Local Cluster aur Command ka Pattern

Seekhne ke liye local cluster banate hain: kind, minikube, ya Docker Desktop ka Kubernetes. Commands ka pattern aasan hai. kubectl get list dikhata hai. describe ek object ki poori detail aur sabse neeche Events. logs truck ke logs. exec -it andar jaane ke liye. apply -f YAML se banane ya badalne ke liye, aur delete. -o wide extra columns, -o yaml poora object, aur -n namespace ke liye. Ye pattern har resource par ek jaisa chalta hai: kubectl get pods, get deployments, get services. Aur kubectl get all ek namespace ki badi cheezein ek saath dikhata hai.

## Pehla Pod: Teen Tareeke

Pod banane ke teen tareeke. Seedha: kubectl run rooms --image=nginx:alpine, jahan rooms pod ka naam aur --image truck design. Doosra: YAML haath se likhne ki jagah kubectl se banwao: kubectl run rooms --image=nginx:alpine --dry-run=client -o yaml > rooms-pod.yaml. --dry-run=client object banata hai par cluster mein rakhta nahi, aur -o yaml use YAML mein likhta hai. Teesra: us file ko kholo, jo badalna ho badlo, aur kubectl apply -f rooms-pod.yaml. YAML file ko manifest bhi kehte hain. Ye dry-run wali trick roz kaam aati hai, kyunki khaali page se YAML likhne se behtar hai ki kubectl ka likha hua dhancha badlo.

## Pod ko Padhna: describe aur READY

kubectl get pods -o wide ke columns: NAME, READY, STATUS, RESTARTS, AGE, IP aur NODE. NODE column bataata hai ki pod kis building mein hai, aur sabse tez tareeka wahi hai. READY mein x/y hota hai: y pod ke andar kitne trucks hain, aur x mein se kitne chal rahe hain. Matlab 1/2 ka arth hai ki pod mein do trucks hain aur ek hi chal rahi hai. READY pods ki ginti nahi hai. Ab kubectl describe pod rooms: usme image, state, mounts, conditions, aur sabse neeche Events ki table: Type, Reason, Age, From, Message. Kuch galat ho to pehle wahi dekho. Kaun si building, kitne trucks, kaun si images, kis truck ki kya state, aur kyun error: pichhle paanch sawaalon ke jawab describe mein hain.

## Pod Badalna aur Hatana

Pod ka image badalne ke do tareeke. Ek: YAML mein image ka naam badlo aur kubectl apply -f rooms-pod.yaml. Do: chalte object ko seedha badlo, kubectl edit pod rooms, jo pod ka YAML kholta hai, aur save karne par pod/rooms edited likhta hai. Dhyaan: ek chalte pod mein sirf kuch hi fields badal sakte hain, jaise image. Baaki ke liye pod ko hatana aur dobara banana padta hai. Isiliye asli kaam mein hum pod ko seedha nahi, Deployment ke zariye chalate hain, jo agle session mein aayega: wo image badalne par khud naya pod banata hai aur purana hatata hai. Hatane ke liye kubectl delete pod rooms.

## Lab: Cluster Banao aur Pehla Pod Chalao

Lab. kind create cluster --name lab, ya minikube start, ya Docker Desktop mein Kubernetes on karo. kubectl config current-context se pakka karo ki aap lab cluster par ho. kubectl get nodes mein Ready dekho. Ab Session 22 ka rooms:slim design lo. Local cluster ko usse dene ke liye kind load docker-image rooms:slim --name lab, ya minikube mein minikube image load rooms:slim. Pod YAML kubectl run rooms --image=rooms:slim --dry-run=client -o yaml se banao, usme imagePullPolicy: IfNotPresent jodo, aur kubectl apply -f. Ek jaal: tag latest ho to Kubernetes har baar depot se khichna chahta hai, aur local design milta nahi. Phir kubectl port-forward pod/rooms 8080:5000 aur dusre terminal mein curl localhost:8080/health. describe ke Events mein pod ki poori kahani padho. Safai: kubectl delete pod rooms, aur cluster band: kind delete cluster --name lab.

## Recap aur Bridge

Recap: kubectl, local cluster, pehla pod, aur describe ke sawaal. Par pod akela asthayi hai. Agle session mein asli workloads: pod ki sehat aur exit code, standing orders, extension numbers, wings, aur cloud par GKE.

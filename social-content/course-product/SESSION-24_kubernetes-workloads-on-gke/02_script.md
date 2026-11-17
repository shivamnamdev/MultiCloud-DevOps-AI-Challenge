# ✍️ 02: SCRIPT — SESSION-24: Kubernetes Workloads on GKE
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`. Author's class notes: `K8s-Handwritten-Notes.md` (applied as in `NOTES_INTEGRATION_MAP_LINUX_K8S.md` section 2). This is the heaviest Kubernetes session.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S24`
- **Focus:** Pod states and statuses, container exit codes, `describe` events, `logs --previous`, ReplicaSets (desired, current, ready), Deployments (rolling update, rollout history, rollback), READY for a pod vs a deployment, namespaces (why, YAML, switching, cross-namespace DNS, scope), Services (ClusterIP, NodePort, LoadBalancer, endpoints, `expose`), horizontal and vertical scaling, HPA and its needs, GKE (Autopilot vs Standard), image access from Artifact Registry, deploy and clean up on GKE
- **Builds on:** Session 05 (signals, troubleshooting method), Session 10 (Auto Scaling, vertical vs horizontal), Session 11 (marshal, health checks), Session 13 (instance class vs read replica), Session 14 (CIDR, private wings), Session 21 and 22 (exit codes, depot, `rooms-service` design), Session 23 (operations command, objects, `kubectl`)
- **Story position:** Zoom level 3, head office. Ab Atithi standing orders deta hai, parking bays mein trucks khadi karta hai, har service ko ek permanent extension number deta hai, dev, staging aur production ke alag wings banata hai, aur jab guests ki line badhti hai to aur trucks kholta hai. Landlord GCP command ka dimaag chalata hai.
- **Story words used:** operations command (Kubernetes), parking bay (pod), standing order (ReplicaSet, Deployment), extension number (Service), wing (namespace), truck (container), truck design (image), depot (registry), marshal (load balancer), more trucks vs a bigger truck (horizontal vs vertical), guest (end user), staff (admin)
- **Lab project:** Atithi's `rooms-service` truck in a cluster: five sick pods diagnosed, a standing order with a failed and rolled-back release, dev and staging wings with a permanent extension number, and finally the same service on a managed GKE cluster behind a Google load balancer.
- **Cost rule (GCP):** a GKE cluster, its load balancer, disks and registry images are billed while they exist. New-account credits and Autopilot pricing change, so read the live pricing page first. Every cloud lab ends with deleting the cluster, the load balancer, the images and the repository.
- **Episodes:**
  - Episode 1: Parking Bay ki Sehat: Pod States aur Exit Codes
  - Episode 2: Standing Order: ReplicaSet, Deployment, Rollout aur Rollback
  - Episode 3: Wings aur Extension Number: Namespaces aur Services
  - Episode 4: Zyada Trucks ya Bada Truck: Scaling aur GKE par Deploy

---

# 📺 EPISODE 1: Parking Bay ki Sehat

### [00:00 – 02:00] Scene 1: Pod Chal Nahi Raha, Ab Kya?
**[VISUAL: A `kubectl get pods` list with five pods showing five different statuses: Pending, ImagePullBackOff, CrashLoopBackOff, Error, Running with READY 1/2. A manager points at it and asks "which one first?".]**

**(Voiceover):**
Session 23 mein humne pod chalaya aur woh Running tha. Asli kaam mein pods aise nahi hote. Subah kisi ne bataya ki rooms-service sust hai. `kubectl get pods` ki list mein paanch pods paanch alag status dikhate hain. Kaun sa pehle dekhein? Is episode mein ek hi seedhi aadat banegi: status padho, exit code padho, describe ke Events padho. Session 5 ka troubleshooting method wahi hai, bas ab bays aur trucks ke naam se. Asli seekh tab hoti hai jab cheezein tootein, isliye lab mein hum jaan boojh kar pods ko todenge.

### [02:00 – 04:45] Scene 2: Pod ke States
**[VISUAL: A table. Pending: not started, no room or storage. Running: scheduled and at least one truck running. Succeeded: all trucks finished fine. Failed: a truck stopped with a non-zero code. Unknown: the node cannot be reached. Below, another list of statuses seen in the STATUS column: CrashLoopBackOff, Terminating, ImagePullBackOff, ContainerCreating.]**

**(Voiceover):**
Pod ke paanch asli phases hain. Pending: pod ban gaya par abhi chalu nahi hua, aksar kyunki kisi building mein itna CPU ya memory nahi, ya jis storage ki zaroorat hai wo nahi mila. Running: pod ek building par laga hai aur kam se kam ek truck chal rahi hai, doosri abhi start ho rahi ho sakti hai. Succeeded: saari trucks ne kaam poora karke theek tareeke se band hui, jobs ke liye normal. Failed: ek ya zyada truck non-zero exit code ke saath band hui. Unknown: building tak pahunch nahi paa rahe. Ek zaroori sudhaar: `CrashLoopBackOff` aur `Terminating` phases nahi hain. Ye woh status hain jo `kubectl get pods` ke STATUS column mein dikhte hain, jaise `ImagePullBackOff` aur `ContainerCreating`. Roz dikhte yahi hain, isliye inhe jaanna zaroori hai.

### [04:45 – 07:20] Scene 3: Exit Code: Truck Ne Kya Kaha
**[VISUAL: A table of exit codes. 0 success. 1 general error, for example a config missing. 126 permission denied (not executable). 127 command not found. 137 killed, often out of memory. 143 stopped by SIGTERM. A line: "137 = 128 + 9; 143 = 128 + 15".]**

**(Voiceover):**
Truck ka exit code uski aakhri baat hai. Zero: theek se khatam. Ek: aam error, jaise web server config na milne se start nahi hua. 126: permission denied, yaani file executable nahi, chmod ki dikkat, jo Session 4 ka sabak hai. 127: command mili hi nahi, jaise truck ne aisi command chalayi jo design mein hai hi nahi. 137: kill kar di gayi, aur sabse aam wajah memory ki hadd paar karna, yaani OOMKilled. Ye 128 plus 9 hai, yaani signal 9, SIGKILL. 143 ek aur: 128 plus 15, SIGTERM, jo tab aata hai jab command ne use band hone ko kaha. Ye Session 5 aur 21 ke signals hain. Exit code ka matlab jaan liya to aadha debugging ho gaya.

### [07:20 – 10:00] Scene 4: describe, Events aur logs --previous
**[VISUAL: `kubectl describe pod rooms-bad`. The Events table at the bottom: Scheduled, Pulling, Failed, BackOff. The "Last State: Terminated, Reason: OOMKilled, Exit Code: 137" block. Then `kubectl logs rooms-bad -c rooms --previous`.]**

**(Voiceover):**
Pod ki kahani `kubectl describe pod` ke sabse neeche Events table mein hai: kab schedule hua, kab image khichi, kab fail hua, aur kyun. Upar Containers section mein har truck ki State aur Last State hai: usme Reason aur Exit Code hota hai, jaise OOMKilled aur 137. Ab ek sawaal jo har engineer ko milta hai: "raat ke barah baje pod restart hua, par ab naya truck chal raha hai, to purane ke logs kahan?" `kubectl logs POD -c TRUCK --previous` pichhli truck ke logs deta hai, wahi jo crash hui thi. Jab pod mein ek se zyada trucks hon, to `-c` se naam batao. Aur agar pod mein ek hi truck hai, to bhi `--previous` crash ke baad sabse pehla command hai.

### [10:00 – 12:30] Scene 5: Pending aur CrashLoopBackOff
**[VISUAL: Left: a pod stuck in Pending with the event "0/3 nodes are available: insufficient cpu". Right: a restart counter climbing and the wait between restarts doubling (10s, 20s, 40s ... up to 5 min). Causes written under each.]**

**(Voiceover):**
Do status sabse zyada rulate hain. Pending: describe ke Events mein likha aata hai jaise "teen mein se koi building nahi jisme itna CPU ho." Wajah: pod ne zyada resources maange, ya jis disk ki zaroorat hai wo nahi mili, ya node ka koi niyam match nahi hua. Hal: request kam karo ya building jodo. CrashLoopBackOff: truck start hoti hai, mar jaati hai, command use phir chalata hai, aur har baar ruk ruk ke, kuch second se badhte badhte kuch minute tak. Wajah aksar app ki apni galti: database tak abhi pahunch nahi paayi, koi environment variable, ConfigMap ya Secret nahi mila, ya galat command. Hal: `logs --previous`, phir exit code. Pehle logs, phir change.

### [12:30 – 15:05] Scene 6: Lab: Paanch Beemar Pods
**[VISUAL: A single file with five pod manifests. (a) image `nginx:doesnotexist`. (b) `command: ["sh","-c","exit 1"]`. (c) memory limit 32Mi with `tail /dev/zero`. (d) CPU request 100. (e) `command: ["sh","-c","nosuchcmd"]`. A terminal listing statuses, then `describe` for each.]**

**(Voiceover):**
Lab. Paanch beemar pods banao, ek ek `kubectl run` ya YAML se. Ek: image `nginx:doesnotexist`. Do: `--command -- sh -c 'exit 1'`. Teen: ek truck jo `tail /dev/zero` chalaye aur uski memory limit 32Mi ho. Chaar: ek pod jiski CPU request sau ho. Paanch: `sh -c nosuchcmd`. Ab har ek ke liye `kubectl get pods`, phir `kubectl describe pod`, aur likho: status, exit code, event ka sabse zaroori shabd. Ek hafta aap yahi order dohrao: status se shuru, describe ke Events, `logs --previous` agar crash ho, aur exit code se wajah. Dhyaan: ek pod mein dusra truck jodkar READY ko `1/2` dikha kar dekho, aur samjho ki ye truck ginti hai, pod ginti nahi. Safai: `kubectl delete pod --all`.

### [15:05 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "5 phases + extra statuses · exit codes 0, 1, 126, 127, 137, 143 · describe Events · logs --previous · Pending = no room · CrashLoopBackOff = the app's own fault".]**

**(Voiceover):**
Recap: pod ke states, exit code, describe aur `--previous`. Par ab bhi ek pod mara to koi wapas nahi laata. Agle episode mein standing order.

---

# 📺 EPISODE 2: Standing Order

### [00:00 – 01:50] Scene 1: Pod Mara, Koi Wapas Nahi Laya
**[VISUAL: A lone pod deleted with `kubectl delete pod rooms`; it stays gone. A standing order board "always 3 rooms trucks" and the same delete leading to an immediate replacement.]**

**(Voiceover):**
Bare pod ko `kubectl delete pod` karo, to wo gaya, aur koi use wapas nahi laata, kyunki kisi ne "hamesha teen" kaha hi nahi. Isliye pods ko hum seedha nahi chalate. Standing order dete hain. Pehla level hai ReplicaSet: ek order jo kehta hai "is label ke teen pods hamesha rahein." Doosra level Deployment hai, jo ReplicaSet ko sambhalta hai aur release ka kaam bhi. Dono ko samajhna zaroori hai, kyunki jab kuch galat ho to dono ka status dekhna padta hai.

### [01:50 – 04:25] Scene 2: ReplicaSet ka YAML aur Columns
**[VISUAL: A ReplicaSet YAML: `apiVersion: apps/v1`, `kind: ReplicaSet`, `spec.replicas: 3`, `selector.matchLabels: app: rooms`, `template` with labels and a container. `kubectl get rs` columns: NAME, DESIRED, CURRENT, READY, AGE.]**

**(Voiceover):**
ReplicaSet ka YAML: `apiVersion: apps/v1`, `kind: ReplicaSet`. `spec` mein `replicas`, ek `selector` jo bataata hai kaun se pods apne hain, aur `template`, jisme pod ka nuskha hai. Template ke labels selector se match hone chahiye, nahi to ReplicaSet banta hi nahi. `kubectl get rs` ke columns: DESIRED, CURRENT aur READY. DESIRED matlab kitne pods hone chahiye. CURRENT jitne bane hain. READY jitne taiyaar hain. `kubectl describe rs NAME` mein Containers ke neeche image dikhta hai, aur pods ready kyun nahi, ye kisi pod ka describe dekhne se pata chalta hai. Pehle ye commands yaad karo: `kubectl get rs`, aur resource ka type hamesha likho, kyunki `kubectl get new-replica-set` nahi, `kubectl get rs new-replica-set` chalta hai.

### [04:25 – 07:15] Scene 3: Scale, Replace aur Delete
**[VISUAL: Commands. `kubectl create -f rs.yaml`, `kubectl scale rs rooms-rs --replicas=5`, `kubectl edit rs rooms-rs`, `kubectl replace -f rs.yaml`, `kubectl delete rs rooms-rs`. A pod with a matching label added by hand is adopted by the ReplicaSet and then deleted when the count is reached.]**

**(Voiceover):**
ReplicaSet banane ke liye `kubectl create -f`, update ke baad `kubectl apply -f`, ya `kubectl replace -f`. Paanch pods tak le jaane ke do tareeke. `kubectl scale rs rooms-rs --replicas=5`. Ya `kubectl edit rs rooms-rs`, jahan spec mein replicas badal kar save karo. Hatane ke liye `kubectl delete rs rooms-rs`, ya `kubectl delete -f rs.yaml`. Ek naya sawaal: ek pod hata diya, phir bhi chaar hi kyun dikhte hain? Kyunki ReplicaSet dekhta hai ki desired paanch aur current chaar hai, aur turant ek naya bana deta hai. Ek hairan karne wali baat: agar aapne haath se ek pod banaya jiska label ReplicaSet ke selector se milta hai, to ReplicaSet use apna maan leta hai, aur ginti poori hone par use hata bhi sakta hai. Isliye labels sochkar rakho.

### [07:15 – 09:55] Scene 4: Deployment: Release ka Maalik
**[VISUAL: A hierarchy. Deployment → ReplicaSet v1 (3 pods) and, on update, a new ReplicaSet v2 growing while v1 shrinks. Parameters shown: `maxSurge`, `maxUnavailable`. A line: "ReplicaSet counts pods; Deployment manages ReplicaSets".]**

**(Voiceover):**
Deployment ReplicaSet ke upar ka standing order hai. Aap Deployment likhte ho, wo ek ReplicaSet banata hai, aur ReplicaSet pods. Image badalne par Deployment ek naya ReplicaSet banata hai, aur purane ko dheere dheere kam karta hai. Isi ko rolling update kehte hain. `maxSurge` batata hai ki ek saath kitne extra pods ban sakte hain, aur `maxUnavailable` ki kitne kam ho sakte hain. Dono ka default pachchees percent hai. Purana ReplicaSet kuch samay bacha rehta hai, aur isi se rollback ho paata hai. Deployment ka READY column `3/3` hota hai, yaani teen mein se teen taiyaar. Dhyaan: pod ke READY mein trucks gine jaate hain, Deployment ke READY mein pods. `0/4` ka matlab chaar pods chahiye aur ek bhi taiyaar nahi.

### [09:55 – 12:35] Scene 5: Release, Galat Release aur Rollback
**[VISUAL: Commands. `kubectl set image deploy/rooms rooms=ghcr.io/atithi/rooms-service:1.0.1`, `kubectl rollout status deploy/rooms`, `kubectl rollout history deploy/rooms`, `kubectl rollout undo deploy/rooms`, `--to-revision=2`. A bad release stuck at 1 of 3 new pods with ImagePullBackOff while old pods still serve.]**

**(Voiceover):**
Naya design chalane ke liye YAML mein tag badal kar `kubectl apply`, ya `kubectl set image deploy/rooms rooms=ghcr.io/atithi/rooms-service:1.0.1`. `kubectl rollout status deploy/rooms` progress dikhata hai. `rollout history` purane revisions, aur `rollout undo` pichhle par wapas, ya `--to-revision` se kisi tay par. Agar naya design galat ho, jaise tag ka naam galat, to naye pods ImagePullBackOff mein atak jaate hain, par purane pods chalte rehte hain, kyunki Deployment tab tak purane nahi hatata jab tak naye taiyaar na hon. Isliye guests tak asar nahi. Ye tab hi sachhi suraksha hai jab pod mein readiness check bhi ho, jise hum agle session mein dekhenge. Aur ek aadat: har release par change-cause ka ek note rakho, taaki history mein "kya badla" dikhe.

### [12:35 – 14:45] Scene 6: Lab: Order, Galat Release, Wapas
**[VISUAL: A Deployment YAML for rooms with three replicas. Apply, then set a bad image tag; `kubectl get pods` shows old pods Running and new ones failing; `rollout status` hangs; `kubectl rollout undo`; everything Running. Then a good tag, watching pods swap one by one.]**

**(Voiceover):**
Lab. Deployment ka YAML `kubectl create deployment rooms --image=nginx:1.26-alpine --replicas=3 --dry-run=client -o yaml > rooms.yaml` se banao, aur `kubectl apply -f rooms.yaml`. Phir `kubectl delete pod` karke dekho ki replacement turant aata hai. Ab `kubectl set image deploy/rooms nginx=nginx:doesnotexist`, kyunki `create deployment` ne truck ka naam `nginx` rakha hai. `kubectl get pods` mein naye pod ImagePullBackOff mein hain par purane Running. `kubectl rollout status` atka rahega. Phir `kubectl rollout undo deploy/rooms`. Ab sahi tag, `nginx:1.27-alpine`, set karo aur dekho ki pods ek ek karke badalte hain, aur `kubectl rollout history` mein revisions. Safai: `kubectl delete deploy rooms`.

### [14:45 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "ReplicaSet: DESIRED / CURRENT / READY · Deployment owns ReplicaSets · rolling update, maxSurge, maxUnavailable · set image, status, history, undo · pod READY counts trucks, Deployment READY counts pods".]**

**(Voiceover):**
Recap: ReplicaSet, Deployment, rollout aur rollback. Ab sawaal: pods badalte rehte hain, to guests ko kaun sa address milega? Aur ek hi cluster mein dev, staging aur production ko kaise alag rakhein?

---

# 📺 EPISODE 3: Wings aur Extension Number

### [00:00 – 02:10] Scene 1: Ek Cluster, Teen Team
**[VISUAL: A cluster drawn as a building with wings labelled dev, staging, prod. Each wing has its own pods and services. The dev wing and the staging wing both contain a service named `backend`, with no clash.]**

**(Voiceover):**
Ek cluster mein dev, staging aur production, aur kai teams. Agar sab ek hi jagah ho, to naam takrate hain: dono jagah `frontend` aur `backend` hain. Ek ki galti doosre ko tod sakti hai. Namespace cluster ke andar ek alag wing hai: alag naam, alag access, alag resource ki hadd. Dev wing mein `backend` aur staging wing mein bhi `backend` aaram se chalte hain, aur ek doosre se takrate nahi. Notes ki ek achhi misaal: cluster ek library hai aur namespace alag alag bookshelf. Do shelf par ek hi naam ki kitaab ho sakti hai, aur koi confusion nahi.

### [02:10 – 04:45] Scene 2: Namespace ke Commands
**[VISUAL: A Namespace YAML with `name: dev-wing` and `labels: environment: development`, with a red cross over `dev_wing`. Commands: `kubectl create namespace dev`, `kubectl get ns`, `kubectl describe ns dev`, `kubectl get pods -n dev`, `kubectl run redis --image=redis -n dev`, `kubectl create -f x.yaml -n dev`, `kubectl delete ns dev`.]**

**(Voiceover):**
Namespace ka YAML: `apiVersion: v1`, `kind: Namespace`, aur `metadata` mein `name` aur `labels`. Naam mein underscore nahi chalta, isliye `dev-wing`, `dev_wing` nahi. Bina YAML ke `kubectl create namespace dev`. `kubectl get namespaces` list, `describe` detail. Kisi wing mein kaam ke liye `-n dev`: `kubectl get pods -n dev`, `kubectl run redis --image=redis -n dev`, `kubectl create -f x.yaml -n dev`. Ek pod kis wing mein hai ye bhoolo to `kubectl get pods -A | grep blue`. Flag `-A` ya `--all-namespaces` hai. Ek khatra: `kubectl delete namespace dev` us wing ki saari cheezein hata deta hai. Aur kuch cheezein wing ki hoti hi nahi, jaise nodes aur persistent volumes. Cluster ke default wing: `default`, `kube-system`, `kube-public` aur `kube-node-lease`.

### [04:45 – 07:00] Scene 3: Wing Badalna aur Wing Paar Baat
**[VISUAL: `kubectl config set-context --current --namespace=dev` followed by `kubectl get pods` with no flag. A call from a pod in the staging wing to `backend.dev.svc.cluster.local`. A diagram: `<service>.<namespace>.svc.cluster.local`.]**

**(Voiceover):**
Har command ke saath `-n dev` thakane wala hai. Isliye `kubectl config set-context --current --namespace=dev`: ab bina `-n` ke har command dev wing mein chalega. Isme bhi khatra: bhool jao ki ab dev mein ho. Isliye prompt mein namespace dikhao. Kya ek wing ka pod doosre wing ke pod se baat kar sakta hai? Haan, service ke poore naam se: `<service>.<namespace>.svc.cluster.local`, jaise `backend.dev.svc.cluster.local`. Apni wing mein sirf `backend` kaafi hai. Ye dhyaan rakho ki wing akeli suraksha ki deewar nahi: bina network policy ke koi bhi pod kisi bhi wing se baat kar sakta hai. Network policy hum Session 25 mein dekhenge.

### [07:00 – 09:20] Scene 4: Service: Permanent Extension Number
**[VISUAL: A client calls pod IP `10.1.0.5`. The pod is replaced and the new IP is `10.1.0.9`; the client breaks. A Service with a stable IP and DNS name `rooms` fixes it. The Service finds its pods by a label selector and lists their IPs as endpoints.]**

**(Voiceover):**
Pod ka IP naya pod banne par badal jaata hai. Jo client usi IP se baat karta rahe, wo tootega. Service ek permanent extension number hai: ek tay IP aur DNS naam, jo peeche ke pods ko label ke zariye dhoondhti hai aur traffic baantti hai. Cluster mein ek Service pehle se hoti hai: `kubernetes`. `kubectl get services` mein uska TYPE dikhta hai, aur `kubectl describe service kubernetes` mein TargetPort, Labels aur Endpoints. Endpoints wahi pods hain jinhe Service abhi traffic bhej rahi hai. Aur sirf Ready pods hi endpoints mein aate hain. Ye Session 11 ke marshal ka health check hai, bas cluster ke andar.

### [09:20 – 12:00] Scene 5: Service ke Types aur YAML
**[VISUAL: Three layered boxes. ClusterIP (inside only), NodePort (a port 30000 to 32767 opened on every node), LoadBalancer (a cloud load balancer with an external IP). A Service YAML with `selector`, `port`, `targetPort`. A command `kubectl expose pod redis --port=6379 --name redis-service`.]**

**(Voiceover):**
Service ke teen mukhya types. ClusterIP default hai: sirf cluster ke andar. NodePort har building par 30000 se 32767 ke beech ek port kholta hai. LoadBalancer cloud ka load balancer banata hai aur ek external IP deta hai, jo Session 11 ke marshal ka Kubernetes roop hai. YAML mein `selector` batata hai kaun se pods, `port` Service ka darwaza, aur `targetPort` truck ka port. Ek chhoti command: `kubectl expose pod redis --port=6379 --name redis-service`, jo ek chalte pod ke liye ek Service bana deti hai, jo cluster ke andar redis ko 6379 par dikhaye. Aur ek hi pehchaan wali galti: Service ka selector aur pod ka label mile nahi, to `kubectl get endpoints rooms` khaali aayega. Wahi Session 23 ka label jaal.

### [12:00 – 15:00] Scene 6: Lab: Dev Wing, Staging Wing, Ek Naam
**[VISUAL: Namespaces `dev` and `staging`. A Deployment `rooms` and Service `rooms` in each. `kubectl get pods -A | grep rooms`. A test pod in staging calls `rooms.dev.svc.cluster.local`. Break the selector and watch `kubectl get endpoints` go empty.]**

**(Voiceover):**
Lab. `kubectl create namespace dev` aur `kubectl create namespace staging`. Dono mein `kubectl create deployment rooms --image=nginx:alpine --replicas=2 -n dev` aur wahi staging mein, aur `kubectl expose deployment rooms --port=80 -n dev`, staging mein bhi. `kubectl get pods -A | grep rooms` se dono wing ke pods dekho. Ab staging mein ek test pod: `kubectl run tmp -n staging --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- rooms.dev.svc.cluster.local`. Nginx ka page aayega. Phir `kubectl get endpoints rooms -n dev` mein do IP. Naye Kubernetes mein ye command deprecated ka warning deti hai, kyunki ab EndpointSlice use hota hai, to `kubectl get endpointslices -n dev` bhi aazma lo. Ab `kubectl edit svc rooms -n dev` se selector galat kar do aur `get endpoints` dobara: khaali. Aakhir mein `kubectl delete namespace dev staging` aur dekho ki sab saath hat gaya.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "namespace = wing · hyphens, not underscores · -n, -A, set-context · name.ns.svc.cluster.local · a wing is not a security wall · Service = IP + DNS + selector · endpoints empty = label mismatch".]**

**(Voiceover):**
Recap: wings aur extension numbers. Ab sawaal: guests ki line badhe to kya karein? Aur ye sab cloud par kaise chalayein?

---

# 📺 EPISODE 4: Zyada Trucks ya Bada Truck

### [00:00 – 01:20] Scene 1: Shaadi ka Season
**[VISUAL: A graph of guests per minute. A wedding-season spike. Left: more identical trucks open and share the line. Right: one truck replaced by a bigger truck with more power and more stock. Labels: "out and in" for the left, "up and down" for the right.]**

**(Voiceover):**
Shaadi ke season mein Atithi ki booking site par line badh jaati hai. Do hi raaste hain. Ya zyada trucks kholo, ya ek truck ko bada karo. Pehle ko horizontal scaling kehte hain, out aur in. Doosre ko vertical scaling, up aur down. Session 10 mein humne Auto Scaling mein buildings badhai thi, aur Session 13 mein records office ka size badhaya tha. Wahi do vichar yahan trucks par hain.

### [01:20 – 03:15] Scene 2: Kab Kaun Sa
**[VISUAL: A two-column table. Horizontal: more pods, spread the load, fits web servers and microservices. Vertical: more CPU and memory for the existing pod, fits a database or heavy processing. Below, a mapping: web → horizontal, rooms database → vertical, reads → replicas (Session 13).]**

**(Voiceover):**
Horizontal tab, jab app ke independent copies ban sakte hon: web server, microservices. Badi sale mein zyada log aate hain, aur har pod thoda traffic sambhalta hai. Vertical tab, jab ek hi strong instance chahiye. Maan lo Atithi ke database mein peak ghanton mein complex queries chalte hain. Copies banane se data sync ki dikkat aati hai, to ek ko zyada CPU aur memory do. Session 13 ka wahi sabak: instance class badalna vertical hai, aur read replica horizontal. Seedha rule: web ko phailao, database ko mazboot karo, aur database ko phailana ho to uska poora alag tareeka hai.

### [03:15 – 05:05] Scene 3: HPA: Apne Aap Zyada Trucks
**[VISUAL: A Horizontal Pod Autoscaler watching average CPU against a target of 50 percent of the requested CPU. Pods grow from 2 to 5 under load, then shrink slowly after a cool-down. Requirements listed: metrics server and a CPU request on the container.]**

**(Voiceover):**
HPA, Horizontal Pod Autoscaler, ek supervisor hai jo pods ka average CPU dekhta hai aur replicas badhata ya ghatata hai. `kubectl autoscale deployment rooms --cpu=50% --min=2 --max=5`. Iske do shart hain. Metrics ka source chahiye, yaani metrics-server, jo GKE mein pehle se hota hai aur local cluster mein alag lagana padta hai. Aur pod ke container mein CPU `request` likha hona chahiye, kyunki percent usi request ka hota hai. Scale up tez hota hai, par scale down jaan boojh kar dheere: kuch minute ka intezaar, taaki line ek second ke liye ghat jaaye to trucks hat na jaayein.

### [05:05 – 06:35] Scene 4: Vertical, aur Buildings ka Sawaal
**[VISUAL: A vertical autoscaler suggesting new requests for a pod. A warning on changing resources of a running pod. A picture: more trucks need more room, so an extra building opens (cluster autoscaler or Autopilot).]**

**(Voiceover):**
Vertical ke liye Kubernetes mein Vertical Pod Autoscaler jaisa ek alag tool hai, jo dekhta hai ki pod ko asli mein kitna chahiye, aur request badalne ki salah deta hai. Aur ek aur baat: HPA ne pods badha diye, par buildings mein jagah nahi hui to naye pods Pending ho jaayenge. Wahan building ka scaling aata hai: node autoscaler. Autopilot jaise mode mein landlord ye khud karta hai. Ek HPA aur VPA ek hi resource par saath mat chalao.

### [06:35 – 09:30] Scene 5: GKE: Landlord Command Chalaye
**[VISUAL: Two modes. Autopilot: Google manages nodes and billing is by pod resource requests. Standard: you manage node pools with a machine type and autoscaling. A command `gcloud container clusters get-credentials`. Beside it, equivalents: EKS (AWS) and AKS (Azure).]**

**(Voiceover):**
Control plane khud chalana mehnat ka kaam hai: upgrades, etcd ka backup, security patches. GKE, Google Kubernetes Engine, ye kaam landlord ko de deta hai. Iske do mode. Autopilot mein buildings bhi Google sambhalta hai, aur bill pods ke maange hue resources par aata hai, isliye resource requests likhna zaroori ho jaata hai. Request na likho to Autopilot khud default laga deta hai, aadha vCPU aur do GiB, aur bahut chhoti request ko minimum tak badha deta hai, jaise CPU ke liye 250 milli. Standard mein aap node pools khud chalate ho: machine type, autoscaling, aur zyada control. AWS par wahi kaam EKS karta hai, aur Azure par AKS. Cluster se judne ke liye `gcloud container clusters get-credentials`, jo kubeconfig mein ek naya context jod deta hai. `kubectl` ko GKE se baat karne ke liye `gke-gcloud-auth-plugin` chahiye: `gcloud components install gke-gcloud-auth-plugin`. Docs mein ab `--region` ki jagah `--location` likha hota hai, dono chalte hain.

### [09:30 – 12:05] Scene 6: Depot se Image aur Bahar ka Darwaza
**[VISUAL: A design `rooms-service:1.0.0` pushed from the laptop to Artifact Registry. A cluster pulls it using the nodes' identity. A Service with `type: LoadBalancer` gets an external IP. A bill icon next to the load balancer.]**

**(Voiceover):**
Pehle depot banao: `gcloud artifacts repositories create REPO --repository-format=docker --location=REGION`, aur `gcloud auth configure-docker REGION-docker.pkg.dev` se Docker ko login sikhao. Phir apni design ko Artifact Registry mein push karo: `docker tag`, `docker push REGION-docker.pkg.dev/PROJECT/REPO/rooms-service:1.0.0`. Cluster ko use khichne ki ijaazat chahiye: nodes ki service account ko registry padhne ka role. Naye project mein ye service account ke paas koi role hota hi nahi, to pehli baar pods `ImagePullBackOff` mein aate hain, aur `kubectl get events` mein `403 Forbidden` dikhta hai. Hal: `gcloud artifacts repositories add-iam-policy-binding REPO --location=REGION --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com --role=roles/artifactregistry.reader`. Session 9 ka wahi sabak: kaun kya kar sakta hai. Service ko `type: LoadBalancer` karo, to GKE ek Google load balancer banata hai aur kuch der mein EXTERNAL-IP dikhata hai. Load balancer aur uski IP bhi paisa leti hain, isliye lab ke baad sab hatao.

### [12:05 – 15:40] Scene 7: Lab: GKE par Poora Deploy
**[VISUAL: `gcloud container clusters create-auto atithi-lab --region=REGION`, `gcloud container clusters get-credentials atithi-lab --region=REGION`, `kubectl config current-context`, `kubectl apply -f deploy.yaml -f svc.yaml`, `kubectl get svc -w`, a browser at the external IP, `kubectl autoscale`, `gcloud container clusters delete`.]**

**(Voiceover):**
Lab. GCP project mein billing on karo, aur `gcloud services enable container.googleapis.com artifactregistry.googleapis.com` se Kubernetes Engine aur Artifact Registry API chalu karo. `gcloud container clusters create-auto atithi-lab --region=YOUR_REGION`, jisme saat-aath minute lagte hain, aur cluster shuru mein bina kisi node ke hota hai. Phir `gcloud container clusters get-credentials atithi-lab --region=YOUR_REGION` aur `kubectl config current-context` se pakka karo ki aap sahi cluster par ho. Deployment aur `type: LoadBalancer` Service ke YAML `kubectl apply -f` karo, jisme container ki CPU request zaroor ho. `kubectl get svc -w` mein EXTERNAL-IP aaye to browser mein kholo. Pehli baar pods kareeb teen minute Pending rehte hain, kyunki Autopilot pehle building kholta hai. Ek rolling update karo aur rollback bhi. Phir `kubectl autoscale deployment rooms --cpu=50% --min=2 --max=5`, ek chhote load generator se line badhao, aur `kubectl get hpa -w` dekho. Hamare test mein replicas do se paanch kareeb ek minute mein ho gaye, aur wapas do hone mein das se pandrah minute lage. Scale down jaan boojh kar dheere hai. Sabse aakhir mein `gcloud container clusters delete atithi-lab --region=YOUR_REGION`, aur console mein dekho ki koi load balancer, forwarding rule, disk ya image nahi bacha.

### [15:40 – 16:40] Scene 8: Recap aur Bridge
**[VISUAL: A card: "horizontal for web, vertical for the database · HPA needs metrics + CPU request · scale-down is slow on purpose · pods need buildings · managed control plane: GKE, EKS, AKS · registry access · load balancer costs money · delete after the lab". Then a truck park fades in.]**

**(Voiceover):**
Recap: Kubernetes ke asli workloads: pod ki sehat, standing order, wings, extension numbers, scaling, aur GKE. Ab Atithi ka poora truck park: kai chhoti services, jo ek doosre ko extension se bulati hain, ek concierge jo guests ko sahi truck tak le jaaye, aur ek locker room jisme records bachein. Agle session mein microservices.

---

# 📎 Student handout: Session 24 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Pod phases | Pending, Running, Succeeded, Failed, Unknown |
| STATUS column | `CrashLoopBackOff`, `Terminating`, `ImagePullBackOff`, `ContainerCreating` phase nahi hain |
| Exit codes | 0 theek, 1 error, 126 permission, 127 command nahi, 137 kill (aksar memory), 143 SIGTERM |
| Pending | Jagah ya storage nahi; Events padho |
| CrashLoopBackOff | App ki apni galti; `logs --previous` |
| READY | Pod: chalti trucks / kul trucks. Deployment: taiyaar pods / chahiye pods |
| ReplicaSet | DESIRED, CURRENT, READY; `kubectl get rs`; `delete rs <naam>` |
| Scale | `kubectl scale rs <naam> --replicas=5`; `kubectl edit rs <naam>` |
| Deployment | Naya ReplicaSet banata hai; `maxSurge`, `maxUnavailable` (default 25%) |
| Release | `set image`, `rollout status`, `rollout history`, `rollout undo` |
| Namespace | Naam mein hyphen; `-n`, `-A`, `set-context --current --namespace=` |
| Wing paar | `<service>.<ns>.svc.cluster.local`; wing akeli suraksha nahi |
| `delete namespace` | Andar ki sab cheezein hatati hai |
| Service | Stable IP + DNS + selector; `get endpoints` khaali = label mismatch |
| Types | ClusterIP (andar), NodePort (30000 se 32767), LoadBalancer (bahar) |
| `expose` | `kubectl expose pod redis --port=6379 --name redis-service` |
| Scaling | Web: horizontal. Database: vertical. HPA ko metrics + CPU request chahiye |
| GKE | Autopilot vs Standard; `get-credentials`; registry role; LoadBalancer = paisa |
| Safai | Cluster, load balancer, images, repository |

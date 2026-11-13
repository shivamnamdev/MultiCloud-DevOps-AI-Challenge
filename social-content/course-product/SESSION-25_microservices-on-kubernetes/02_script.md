# ✍️ 02: SCRIPT — SESSION-25: Microservices on Kubernetes
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S25`
- **Focus:** Microservices architecture, namespaces & manifests per service, Ingress routing, persistent storage (PVC/StatefulSet), service-to-service communication, network policy, Helm intro
- **Episodes:**
  - Episode 1: Monolith se Microservices: Architecture aur Trade-offs
  - Episode 2: Namespaces, Manifests aur Service-to-Service Calls
  - Episode 3: Ingress aur Persistent Storage
  - Episode 4: Production Touches: Network Policy, Helm aur Troubleshooting

---

# 📺 EPISODE 1: Monolith se Microservices

### [00:00 – 01:15] Scene 1: Ek Bug, Poori Dukaan Band
**[VISUAL: An e-commerce monolith: catalogue, cart, payments, orders in one block. The payment code has a memory leak; the entire site crashes. Next: separate small boxes, only payments red, rest green.]**

**(Voiceover):**
Ek e-commerce site ek hi bade program mein bani hai. Payment ke code mein ek bug aaya aur poori site gir gayi, catalogue bhi, cart bhi. Microservices ka idea hai ki ise chhote chhote independent services mein todo: catalogue, cart, payments, orders. Ek girti hai to baaki chalti hain.

### [01:15 – 05:00] Scene 2: Microservices ke Fayde aur Keemat
**[VISUAL: A balanced scale. Plus: independent deploys, scale per service, tech freedom, fault isolation. Minus: network calls, distributed debugging, data consistency, operational overhead.]**

**(Voiceover):**
Fayde: har service alag deploy ho sakti hai, jo zyada load le use alag scale kar sakte ho, aur ek team ek service ki malik ho sakti hai. Keemat: ab function calls network calls ban gaye, jo fail ho sakte hain aur dheere hote hain. Debugging kai services mein faili hoti hai, data alag alag databases mein hota hai, aur operations ka kaam badh jata hai. Isliye chhoti team ke liye pehle monolith bhi theek hai. Microservices tab lo jab team aur scale ki zaroorat ho, "kyunki sab karte hain" isliye nahi.

### [05:00 – 08:30] Scene 3: Hamara Project: Mini Shop
**[VISUAL: An architecture diagram: Browser → Ingress → `frontend` (web UI), `catalog` (API), `cart` (API with Redis), `orders` (API + Postgres). Arrows between services. Each in its own Deployment + Service.]**

**(Voiceover):**
Is session ka project: Mini Shop. Frontend jo UI dikhata hai, catalog service jo products deti hai, cart service jo Redis mein cart rakhti hai, aur orders service jo Postgres mein orders likhti hai. Har service ek alag Deployment aur Service hai, aur sab ek namespace mein. Hum kam se kam teen services aur ek database use karenge, taaki real life ka pattern dikhe: kuch stateless hain, kuch stateful.

### [08:30 – 11:30] Scene 4: Lab: Services ko Pehchano
**[VISUAL: A table where the learner fills columns: Service, Port, Depends on, Stateful? A checklist of 12-factor ideas: config via env, logs to stdout, stateless processes.]**

**(Voiceover):**
Lab (design exercise): Mini Shop ke chaar services ke liye ek table banao: naam, port, kiski zaroorat hai, stateful hai ya nahi. Jaise cart ko Redis chahiye, orders ko Postgres. Phir 12-factor app ke teen niyam har service par check karo: config environment variables se, logs stdout par, aur process stateless. Ye niyam Kubernetes par microservices ko aasaan banate hain. Is table ko hum agle episodes mein YAML mein badlenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "split by business capability · cost = distributed complexity · 12-factor basics".]**

**(Voiceover):**
Recap: microservices ka idea aur uski keemat. Ab asli kaam: namespace, manifests aur services ka aapas mein baat karna.

---

# 📺 EPISODE 2: Namespaces, Manifests aur Service-to-Service Calls

### [00:00 – 01:15] Scene 1: Ek Cluster, Kai Team
**[VISUAL: A cluster as an office building with floors labelled `dev`, `staging`, `shop`. Each floor has its own rooms, keys and budget.]**

**(Voiceover):**
Ek cluster mein kai teams aur kai environments chalte hain. Agar sab ek hi jagah ho, to naam takrate hain aur ek ki galti doosre ko tod deti hai. Namespace cluster ke andar ek virtual kamra hai: alag naam, alag access, alag resource limits.

### [01:15 – 05:00] Scene 2: Namespace, Quotas aur Labels ka Standard
**[VISUAL: `kubectl create namespace shop`, `-n shop`. A ResourceQuota (pods/cpu/memory) and a LimitRange. A labels convention: `app.kubernetes.io/name`, `app.kubernetes.io/part-of: shop`.]**

**(Voiceover):**
`kubectl create namespace shop`, aur har object `-n shop` ke saath ya YAML mein `namespace: shop`. ResourceQuota se namespace ke total CPU, memory aur pods ki seema tay hoti hai, aur LimitRange se har container ke default resources. Labels ka ek standard rakho, jaise `app.kubernetes.io/name` aur `part-of: shop`, taaki aage dashboards, policies aur debugging mein kaam aaye. Namespace se alag alag teams ke liye RBAC bhi laga sakte ho. Dhyaan: namespace security ki poori deewar nahi, network policy alag se lagani padti hai.

### [05:00 – 08:30] Scene 3: Service-to-Service Communication
**[VISUAL: `orders` calling `http://catalog.shop.svc.cluster.local:8080/products/1`. Environment variable `CATALOG_URL=http://catalog:8080`. A diagram with timeouts and retries between services.]**

**(Voiceover):**
Service ek doosre ko DNS naam se bulati hai: same namespace mein `http://catalog:8080`, alag namespace mein `catalog.shop.svc.cluster.local`. Ye URL code mein hardcode nahi, ConfigMap ya environment variable se do. Ab network par bharosa nahi kiya ja sakta, isliye har call par timeout lagao, thoda retry karo, aur fail hone par graceful jawab do. Bina timeout ke ek dheemi service poori chain ko latka sakti hai. Isse cascading failure kehte hain.

### [08:30 – 11:30] Scene 4: Lab: Teen Services Deploy Karo
**[VISUAL: A namespace `shop`; Deployments and ClusterIP Services for `catalog` and `frontend` using simple public images or tiny custom ones; `kubectl run` test pod calls catalog by DNS name.]**

**(Voiceover):**
Lab: `kubectl create namespace shop`. Ek simple `catalog` Deployment aur Service banao, jisme koi chhota HTTP server ho, jaise `hashicorp/http-echo` ya aapki apni image, port 8080. Ek `frontend` bhi. Fir test pod `kubectl run tmp -n shop --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- http://catalog:8080`. Phir namespace ke bahar se `catalog.shop.svc.cluster.local` se call karo. Ek ResourceQuota lagao aur dekho ki limit cross karne par naya pod Pending ho jata hai, event mein wajah ke saath.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "namespace = kamra · quotas · DNS names · timeouts + retries".]**

**(Voiceover):**
Recap: namespace, DNS aur calls. Ab bahar ki duniya ko andar laana: Ingress. Aur data ko bachana: persistent storage.

---

# 📺 EPISODE 3: Ingress aur Persistent Storage

### [00:00 – 01:15] Scene 1: Har Service ka Alag Load Balancer?
**[VISUAL: Four services each with their own cloud load balancer and a bill meter rising. Replaced by one Ingress with path rules.]**

**(Voiceover):**
Agar har service ke liye alag LoadBalancer banao, to har ek ka alag IP aur alag bill. Ingress ek hi entry point deta hai aur HTTP rules se tay karta hai ki kaun si request kaun si service ko jayegi. Ek darwaza, kai kamre.

### [01:15 – 05:00] Scene 2: Ingress aur Ingress Controller
**[VISUAL: A diagram: Internet → Load Balancer → Ingress Controller (nginx or GKE's) → rules: `/` → frontend, `/api/catalog` → catalog, `/api/orders` → orders. TLS certificate on the Ingress.]**

**(Voiceover):**
Ingress ek rule ka object hai: host aur path ke hisaab se Service. Lekin rules akele kaam nahi karte, unhe lagu karne ke liye ek Ingress controller chahiye, jaise nginx ingress ya cloud ka apna. GKE mein built-in controller ek Google load balancer banata hai. Ingress par TLS certificate bhi lag sakta hai. Naye clusters mein Gateway API bhi aa raha hai, jo Ingress ka zyada flexible roop hai, par concept ek hi hai.

### [05:00 – 08:30] Scene 3: Persistent Storage: PV, PVC, StatefulSet
**[VISUAL: A pod writes to a disk. Pod deleted; data persists on the PersistentVolume. PVC as a request, StorageClass provisioning a disk dynamically. StatefulSet with stable names `pg-0`, `pg-1`.]**

**(Voiceover):**
Pod mara to uska disk bhi gaya, jab tak data persistent volume par na ho. PersistentVolumeClaim, PVC, ek request hai: "mujhe 5 GB disk chahiye." StorageClass cloud par automatically ek disk bana deta hai aur use pod se jod deta hai. Database jaise stateful apps ke liye StatefulSet use hota hai: pods ke naam stable, jaise `pg-0`, aur har pod ka apna volume. Dhyaan: production mein database ko Kubernetes mein khud chalana mushkil hai, managed database aksar behtar hota hai.

### [08:30 – 11:30] Scene 4: Lab: Ingress aur PVC
**[VISUAL: An Ingress YAML routing `/` and `/api`. After applying, the external IP serves both. A PVC with a Redis or Postgres pod writes data; the pod is deleted and recreated; data remains.]**

**(Voiceover):**
Lab: ek Ingress YAML likho jisme `/` frontend ko aur `/api/catalog` catalog ko jaaye. Minikube mein `minikube addons enable ingress`, aur GKE mein built-in. Apply karo aur external IP ya `minikube tunnel` se test karo. Phir ek PVC banao, `accessModes: [ReadWriteOnce]`, `storage: 1Gi`, aur use ek pod mein `/data` par mount karo. `kubectl exec` se `echo hi > /data/a`, pod delete karo, naya pod aane par `cat /data/a` aur dekho ki data bacha hai. Safai mein PVC bhi delete karo, kyunki disk ka paisa lagta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Ingress rules + controller · TLS · PVC via StorageClass · StatefulSet for stateful".]**

**(Voiceover):**
Recap: Ingress aur storage. Ab production ke chhote lekin zaroori kaam: network policy, Helm, aur troubleshooting.

---

# 📺 EPISODE 4: Production Touches

### [00:00 – 01:15] Scene 1: Sab Pods Sab Se Baat Kar Sakte Hain
**[VISUAL: A network graph of all pods fully connected. A hacked frontend pod connects straight to the database. A red alarm. Then policies cut lines so only `orders → postgres` remains.]**

**(Voiceover):**
By default Kubernetes mein koi bhi pod kisi bhi pod se baat kar sakta hai. Agar frontend hack ho gaya, to attacker seedha database tak pahunch sakta hai. Network policy ye allow-list banati hai: kaun kisse baat kar sakta hai. Isse blast radius, yaani nuksaan ka daayra, chhota hota hai.

### [01:15 – 05:00] Scene 2: NetworkPolicy aur RBAC
**[VISUAL: A NetworkPolicy YAML: `podSelector: app=postgres`, ingress from `podSelector: app=orders` on port 5432. A note: requires a CNI that supports it. RBAC: Role, RoleBinding, ServiceAccount shown briefly.]**

**(Voiceover):**
NetworkPolicy mein aap batate ho ki postgres ke pods sirf orders ke pods se port 5432 par traffic le sakte hain. Policy tabhi kaam karti hai jab cluster ka network plugin use support kare. RBAC alag hai: wo batata hai ki kaun kya kar sakta hai Kubernetes API par. Har service ko apni ServiceAccount do, jisme sirf zaroori permissions hon. Aur pod security ke liye containers ko non-root aur read-only filesystem ke saath chalao.

### [05:00 – 08:30] Scene 3: Helm ka Parichay
**[VISUAL: A chart folder: `Chart.yaml`, `values.yaml`, `templates/`. A command `helm install shop ./shop -f values-prod.yaml`. A diagram: templates + values = rendered YAML.]**

**(Voiceover):**
Teen services ke liye teen YAML theek hain. Par dus environments aur dus services ke liye copy paste ka jungle ban jaata hai. Helm Kubernetes ka package manager hai: ek chart mein templates aur `values.yaml` hota hai, aur alag environments ke liye alag values file. `helm install shop ./shop -f values-prod.yaml` poori app lagata hai, `helm upgrade` update karta hai, aur `helm rollback` wapas. Aur Helm ka istemaal hum monitoring stack lagane mein bhi karenge.

### [08:30 – 11:30] Scene 4: Lab: Policy lagao aur Troubleshoot Karo
**[VISUAL: Apply a default-deny policy; the frontend can no longer reach postgres; an allow policy for `orders` restores it. A troubleshooting table: Pending, CrashLoopBackOff, ImagePullBackOff, empty endpoints, 502 from ingress.]**

**(Voiceover):**
Lab: namespace `shop` mein ek default-deny NetworkPolicy lagao, aur dekho ki pods ek doosre se baat nahi kar paate; phir sirf zaroori allow policies jodo. Ab troubleshooting yaad rakho. Pod Pending: resources ya scheduling, `kubectl describe pod` ke events dekho. CrashLoopBackOff: app khud crash, `kubectl logs --previous`. ImagePullBackOff: image ka naam ya registry access. Service ka endpoint khaali: label mismatch. Ingress 502: backend pod ready nahi ya port galat. Ye table apne paas rakho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "default-deny · least-privilege RBAC · Helm for repeatable deploys · describe → logs → events".]**

**(Voiceover):**
Recap: microservices ek poore cluster par, surakshit aur repeatable. Ab sawaal: kaise pata chalega ki ye sab theek chal raha hai? Agla session: Prometheus aur Grafana.

# ✍️ 02: SCRIPT — SESSION-24: Kubernetes Workloads on GKE
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S24`
- **Focus:** Deployments (rolling update/rollback), Services (ClusterIP/NodePort/LoadBalancer), ConfigMaps/Secrets, probes/resources/HPA, GKE cluster + deploy
- **Episodes:**
  - Episode 1: Deployments: Rolling Update aur Rollback
  - Episode 2: Services: Pods ko Pata aur Traffic
  - Episode 3: Config, Secrets, Probes aur Autoscaling
  - Episode 4: GKE par Poora Deploy

---

# 📺 EPISODE 1: Deployments — Rolling Update aur Rollback

### [00:00 – 01:15] Scene 1: Release ke Waqt Site Band
**[VISUAL: A release at midnight: the old version stops, the new starts, 2 minutes of "503 Service Unavailable". Next: pods gradually swap one by one with the site always up.]**

**(Voiceover):**
Purane tareeke mein release ka matlab hota tha: purana version band karo, naya chalao, aur beech ke kuch minute website band. Kubernetes ka Deployment ek-ek pod badalta hai, isliye site chalti rehti hai. Aur naya version kharab nikla to ek command se wapas.

### [01:15 – 05:00] Scene 2: Deployment, ReplicaSet aur Pod
**[VISUAL: A hierarchy: Deployment → ReplicaSet (v1) → Pods; on update, a new ReplicaSet (v2) scales up while the old scales down. Rolling update params: `maxSurge`, `maxUnavailable`.]**

**(Voiceover):**
Deployment aapki desired state ka manager hai. Wo ek ReplicaSet banata hai jo tay karta hai ki kitne pods chahiye. Image badalne par Deployment ek naya ReplicaSet banata hai aur purane ko dheere dheere kam karta hai, jisse rolling update kehte hain. `maxSurge` batata hai ki ek saath kitne extra pods ban sakte hain, aur `maxUnavailable` ki kitne kam ho sakte hain. Purana ReplicaSet kuch time tak bacha rehta hai, isi se rollback ho paata hai.

### [05:00 – 08:30] Scene 3: Update aur Rollback Commands
**[VISUAL: Terminal: `kubectl set image deploy/web web=nginx:1.27-alpine`, `kubectl rollout status deploy/web`, `kubectl rollout history deploy/web`, `kubectl rollout undo deploy/web`. A failed rollout stuck with ImagePullBackOff.]**

**(Voiceover):**
Image badalne ke liye YAML mein version badal kar `kubectl apply`, ya `kubectl set image deploy/web web=nginx:1.27-alpine`. `kubectl rollout status deploy/web` progress dikhata hai. `rollout history` purane revisions, aur `rollout undo` pichhle version par wapas. Agar naya image galat naam ka ho, to pods `ImagePullBackOff` mein atak jaate hain, lekin purane pods chalte rehte hain, isliye site gir nahi jaati. Ye hi rolling update ki khoobi hai.

### [08:30 – 11:30] Scene 4: Lab: Galat Release aur Rollback
**[VISUAL: A deployment of 3 replicas. Update to `nginx:doesnotexist`. `kubectl get pods` shows ErrImagePull while old pods still serve. `kubectl rollout undo`. All Running again.]**

**(Voiceover):**
Lab: Deployment banao `kubectl create deployment web --image=nginx:1.26-alpine --replicas=3`. Phir `kubectl set image deploy/web nginx=nginx:doesnotexist`; container ka naam `nginx` hota hai jab `create deployment` se banao. `kubectl get pods` mein `ErrImagePull` dikhega, par purane pods abhi Running hain. `kubectl rollout status` atka rahega. Phir `kubectl rollout undo deploy/web`. Sab theek. Ab sahi image se update karke dekho ki pods ek ek karke badalte hain. Safai: `kubectl delete deploy web`.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Deployment → ReplicaSet → Pods · rolling update · rollout status/undo".]**

**(Voiceover):**
Recap: Deployments, rolling update, rollback. Ab sawaal: pods badalte rehte hain, to unka IP bhi badalta hai. Traffic kaun sambhalega? Services.

---

# 📺 EPISODE 2: Services

### [00:00 – 01:15] Scene 1: Pod ka IP Roz Badalta Hai
**[VISUAL: A client calls pod IP 10.1.0.5. The pod is replaced; the IP is now 10.1.0.9. The client breaks. A Service with a stable virtual IP and DNS name fixes it.]**

**(Voiceover):**
Pod ka IP naya pod banne par badal jaata hai. Agar client usi IP se baat karta rahe, to tootega. Service ek stable address hai: ek fixed IP aur ek DNS naam, jo peeche chalte pods ko label ke zariye dhoondhti hai aur traffic baantti hai.

### [01:15 – 05:00] Scene 2: Service ke Types
**[VISUAL: Four layered boxes: ClusterIP (internal only), NodePort (opens a port on every node 30000-32767), LoadBalancer (cloud LB with external IP), and Ingress (HTTP routing, covered later). ExternalName shown as a DNS alias.]**

**(Voiceover):**
ClusterIP default hai: sirf cluster ke andar se access. NodePort har node par ek port kholta hai, 30000 se 32767 ke beech. LoadBalancer cloud ka load balancer banata hai aur ek external IP deta hai, GKE par ye Google ka load balancer hota hai. ExternalName ek DNS alias hai. Aur HTTP routing ke liye Ingress, jo hum project session mein dekhenge. Internal services ko ClusterIP, aur bahar ke liye LoadBalancer ya Ingress.

### [05:00 – 08:30] Scene 3: Service YAML aur DNS
**[VISUAL: A Service YAML with `selector: app: web`, `port: 80`, `targetPort: 80`. DNS names: `web`, `web.default`, `web.default.svc.cluster.local`. `kubectl get endpoints web`.]**

**(Voiceover):**
Service YAML mein `selector` batata hai ki kaun se pods, `port` Service ka port, aur `targetPort` container ka port. Cluster ke andar DNS se Service ko bula sakte ho: `web` ya `web.default.svc.cluster.local`, jisme `default` namespace hai. Agar Service ke peeche traffic nahi aa raha, to `kubectl get endpoints web` dekho: agar khaali hai, to selector aur pod ke labels mein mismatch hai. Ye Kubernetes ki sabse aam debugging cheez hai.

### [08:30 – 11:30] Scene 4: Lab: Service aur Endpoints
**[VISUAL: Create a deployment and expose it: `kubectl expose deploy web --port 80`. A test pod: `kubectl run tmp --rm -it --image=busybox -- wget -qO- web`. Break the selector to see empty endpoints.]**

**(Voiceover):**
Lab: `kubectl create deployment web --image=nginx:alpine --replicas=2`, phir `kubectl expose deployment web --port=80`. Ek test pod se andar se call: `kubectl run tmp --rm -it --image=busybox:1.36 --restart=Never -- wget -qO- web`. Nginx ka page aayega. Ab `kubectl get endpoints web` mein do IP dikhenge. Service ka selector `kubectl edit svc web` se galat kar do aur `get endpoints` dobara dekho: khaali. Ye wahi symptom hai jo asli incident mein dikhta hai. Safai karna na bhoolo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Service = stable IP + DNS · selector → endpoints · ClusterIP/NodePort/LB".]**

**(Voiceover):**
Recap: Services aur endpoints. Ab application ko config, secrets, health checks aur autoscaling dena.

---

# 📺 EPISODE 3: Config, Secrets, Probes aur Autoscaling

### [00:00 – 01:15] Scene 1: Image Badle Bina Config Badalna
**[VISUAL: An app image with hardcoded DB URL. A developer rebuilds the image for each environment. Next: one image with config injected from outside.]**

**(Voiceover):**
Agar dev, staging aur prod ke liye alag image banani pade, to wo galat design hai. Ek hi image, aur config bahar se. Kubernetes mein iske liye ConfigMap aur Secret hain. Aur app ko zinda rakhne ke liye health probes, aur load ke liye autoscaling.

### [01:15 – 05:00] Scene 2: ConfigMap aur Secret
**[VISUAL: A ConfigMap with `APP_MODE: production`. A Secret with `DB_PASSWORD` (base64). A pod using `envFrom`/`env.valueFrom` and a mounted volume. A warning: "base64 is encoding, not encryption".]**

**(Voiceover):**
ConfigMap mein normal config rehti hai, jaise `APP_MODE`. Secret mein sensitive cheezein, jaise password. Pod ko ye environment variables ya mounted files ke roop mein milti hain. Bahut zaroori: Secret mein value base64 mein hoti hai, jo sirf encoding hai, encryption nahi. Koi bhi use decode kar sakta hai. Isliye RBAC se access seemit karo, etcd encryption on rakho, aur bade systems mein cloud secret managers jaise Secret Manager ya Vault ko integrate karo. Aur secret ko Git mein plain YAML mein kabhi commit mat karo.

### [05:00 – 08:30] Scene 3: Probes aur Resources
**[VISUAL: A container spec with `resources: requests/limits`, `readinessProbe`, `livenessProbe`, `startupProbe`. A timeline: Pod starts → startup probe → readiness passes → traffic starts. Liveness fails → restart.]**

**(Voiceover):**
Resources mein `requests` batata hai kitna kam se kam chahiye, scheduler isi ke hisaab se node chunta hai, aur `limits` upar ki seema. CPU limit par throttle hota hai, aur memory limit se zyada hua to container kill ho jaata hai, OOMKilled. Probes: readiness batata hai ki pod traffic lene ke liye taiyaar hai ya nahi, liveness batata hai ki pod atak gaya hai aur restart chahiye, aur startup dheere start hone wali apps ke liye. Galat liveness probe pods ko baar baar maar sakta hai, isliye usse dhyaan se likho.

### [08:30 – 11:30] Scene 4: Lab: Config, Probe aur HPA
**[VISUAL: A Deployment YAML with env from ConfigMap, readiness probe on `/`, requests cpu 100m, limits 200m. `kubectl autoscale deployment web --cpu-percent=50 --min=2 --max=5`. A load generator increases replicas.]**

**(Voiceover):**
Lab: ConfigMap banao `kubectl create configmap app-config --from-literal=APP_MODE=demo`. Deployment ke container mein `envFrom: [{configMapRef: {name: app-config}}]`, `readinessProbe: {httpGet: {path: /, port: 80}}`, aur `resources: {requests: {cpu: 100m}, limits: {cpu: 200m}}`. Phir `kubectl autoscale deployment web --cpu-percent=50 --min=2 --max=5`. HPA ko metrics chahiye: GKE mein built-in hai, minikube mein `minikube addons enable metrics-server`. Load dene ke liye ek busybox pod mein `while true; do wget -q -O- http://web; done` chalao aur `kubectl get hpa -w` dekho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "ConfigMap/Secret (base64 ≠ secure) · requests/limits · readiness/liveness · HPA needs metrics".]**

**(Voiceover):**
Recap: config, probes, resources, HPA. Ab ye sab cloud par: GKE.

---

# 📺 EPISODE 4: GKE par Poora Deploy

### [00:00 – 01:15] Scene 1: Control Plane Khud Kyun Chalao?
**[VISUAL: A self-managed cluster with a person patching etcd at 3 AM. Next, a managed GKE badge: Google runs the control plane.]**

**(Voiceover):**
Control plane khud chalana, upgrades, etcd ka backup, security patches, bahut mehnat ka kaam hai. GKE, Google Kubernetes Engine, ye kaam Google ko de deta hai. Aap bas apni apps par dhyaan dete ho.

### [01:15 – 05:00] Scene 2: GKE: Autopilot vs Standard
**[VISUAL: Two modes. Autopilot: Google manages nodes, you pay per pod resources. Standard: you manage node pools, more control. A node pool with machine type and autoscaling.]**

**(Voiceover):**
GKE ke do mode. Autopilot mein nodes bhi Google sambhalta hai aur aap pods ke resources ke hisaab se paisa dete ho, to ye shuruaat ke liye aasan hai. Standard mein aap node pools khud chalate ho, machine type, autoscaling, aur zyada control ke saath. Dono mein cluster ko ek region ya zone mein bana sakte ho, aur regional cluster zyada available hota hai. Cluster se connect hone ke liye `gcloud container clusters get-credentials`, jo kubeconfig mein context jod deta hai.

### [05:00 – 08:30] Scene 3: Cloud par Image aur Access
**[VISUAL: Push an image to Artifact Registry. A GKE cluster pulls it. A diagram of IAM: nodes' service account has `roles/artifactregistry.reader`. A Service type LoadBalancer gets an external IP.]**

**(Voiceover):**
Apni image Artifact Registry mein push karo. GKE ko use pull karne ke liye permission chahiye: nodes ki service account ko registry reader role. Service ko `type: LoadBalancer` banao, to GKE khud ek load balancer banata hai aur kuch der mein `EXTERNAL-IP` dikhata hai. Dhyaan: jo cheezein aap banate ho, jaise load balancer, wo paisa leti hain, to lab ke baad cluster aur uske load balancer hata do, warna bill chalta rehta hai.

### [08:30 – 11:30] Scene 4: Lab: GKE par Deploy
**[VISUAL: `gcloud container clusters create-auto demo --region=REGION`, `gcloud container clusters get-credentials demo --region=REGION`, `kubectl apply -f deploy.yaml -f svc.yaml`, `kubectl get svc -w` until EXTERNAL-IP, browser works, then `gcloud container clusters delete demo`.]**

**(Voiceover):**
Lab: GCP project mein billing aur Kubernetes Engine API on karo. `gcloud container clusters create-auto demo --region=YOUR_REGION`, kuch minute lagte hain. `gcloud container clusters get-credentials demo --region=YOUR_REGION`. Phir apne Deployment aur `type: LoadBalancer` Service ke YAML `kubectl apply -f` karo. `kubectl get svc -w` mein EXTERNAL-IP aane par browser mein kholo. Rolling update karo aur rollback bhi. Sabse aakhir mein `gcloud container clusters delete demo --region=YOUR_REGION`, aur console mein dekho ki koi load balancer ya disk nahi bacha.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "managed control plane · Autopilot vs Standard · registry access · LB = cost · delete after lab".]**

**(Voiceover):**
Recap: Kubernetes ke asli workloads, aur GKE par deploy. Ab ek poora multi-service microservices project, Ingress, storage aur namespaces ke saath.

# ✍️ 02: SCRIPT — SESSION-11: AWS Load Balancing
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S11`
- **Focus:** Why load balancers, ALB vs NLB, target groups & health checks, TLS termination, ALB + ASG, troubleshooting
- **Episodes:**
  - Episode 1: Load Balancer kyun? Ek Darwaza, Kai Server
  - Episode 2: ALB vs NLB: Kaun Kab
  - Episode 3: Target Groups, Health Checks aur TLS
  - Episode 4: ALB + ASG: Poora Setup aur Debugging

---

# 📺 EPISODE 1: Load Balancer kyun?

### [00:00 – 01:15] Scene 1: Ek Counter par Sab Log
**[VISUAL: A bank with one counter and a long queue. Next frame: a reception desk directing people to five open counters.]**

**(Voiceover):**
Ek bank mein ek hi counter khula ho aur sau log line mein hon. Ab ek receptionist bula lo jo sabko khaali counter par bhej de. Load balancer ye receptionist hai. Wo users ki requests ko kai servers mein baant deta hai, aur jo server kharab ho use bhoolkar sirf achhon ko traffic bhejta hai.

### [01:15 – 05:00] Scene 2: Load Balancer ke Teen Fayde
**[VISUAL: Three icons: Distribute (arrows to multiple servers), Health (a red server skipped), Single entry point (one DNS name).]**

**(Voiceover):**
Teen fayde. Ek, load baantna, taaki koi ek server na jale. Do, health check, yani kharab server ko traffic na bhejna. Teen, ek hi address: users ek DNS naam par aate hain, aur peeche servers badalte rehte hain, scale hote rehte hain. Isiliye load balancer aur Auto Scaling hamesha saath chalte hain. AWS ka service Elastic Load Balancing, ELB, kehlata hai.

### [05:00 – 08:30] Scene 3: Load Balancing Algorithms aur Stickiness
**[VISUAL: Round robin arrows cycling A→B→C. Then a user's session arrow glued to server B with label "sticky session".]**

**(Voiceover):**
Traffic baantne ke tareeke, jaise round robin, yani baari baari se, ya kam busy server ko. Kabhi kabhi ek user ko ek hi server par chipkana padta hai, ise sticky session kehte hain. Lekin sticky sessions scaling ko mushkil banate hain. Behtar design: server par session na rakho, use database ya cache mein rakho, taaki koi bhi server kisi bhi request ko sambhal sake.

### [08:30 – 11:30] Scene 4: Lab: Do Servers, Alag Pages
**[VISUAL: Two instances with user data that prints their hostnames. In a browser, refreshing shows hostnames alternating in later episodes. For now, each instance is checked individually.]**

**(Voiceover):**
Lab ki taiyaari: do EC2 instances launch karo, alag AZ mein, user data se nginx install karo aur page mein hostname dikhao:
```bash
#!/bin/bash
apt-get update -y && apt-get install -y nginx
echo "Hello from $(hostname)" > /var/www/html/index.html
```
Security group mein port 80 kholo. Dono ke public IP kholkar dekho ki alag hostname dikh raha hai. Agle episodes mein inhi ke aage load balancer lagayenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "distribute · health · one DNS · stateless servers".]**

**(Voiceover):**
Recap: load balancer kya karta hai aur kyun. Ab AWS ke options: ALB, NLB, aur kab kaun.

---

# 📺 EPISODE 2: ALB vs NLB

### [00:00 – 01:15] Scene 1: Dak Ghar vs Courier
**[VISUAL: Two delivery services. One reads the address on each letter and routes by the contents (smart). Another just forwards sealed parcels extremely fast (speedy).]**

**(Voiceover):**
Do tarah ke courier socho. Ek letter ko khol kar padhta hai aur andar likhe ke hisaab se sahi vibhag mein bhejta hai. Doosra sirf sealed parcel ko bahut tez forward karta hai. AWS ke load balancers mein bhi yahi farq hai.

### [01:15 – 05:00] Scene 2: Application Load Balancer
**[VISUAL: ALB diagram, layer 7. Rules: `/api/*` → API target group, `/images/*` → image servers, host header `admin.example.com` → admin servers.]**

**(Voiceover):**
Application Load Balancer, ALB, OSI ki layer 7 par kaam karta hai, yaani wo HTTP aur HTTPS samajhta hai. Wo request ka path, host naam ya headers dekhkar routing kar sakta hai. Jaise `/api/*` ko ek group mein, `/images/*` ko doosre mein. Microservices aur containers ke liye ALB ek natural choice hai, kyunki ek hi load balancer ke peeche kai services chal sakti hain.

### [05:00 – 08:30] Scene 3: Network Load Balancer aur Baaki
**[VISUAL: NLB diagram, layer 4: TCP/UDP. Features: static IP, extreme performance. Gateway Load Balancer and Classic LB shown greyed as niche/legacy.]**

**(Voiceover):**
Network Load Balancer, NLB, layer 4 par TCP aur UDP traffic ko bahut tez aur kam latency ke saath forward karta hai. Isme har AZ ke liye static IP mil sakta hai, jo tab kaam aata hai jab client ko fixed IP chahiye. Gateway Load Balancer security appliances jaise firewalls ke liye hai, aur Classic Load Balancer purana hai jise naye kaam ke liye nahi chunte. Seedha rule: web aur HTTP ke liye ALB, bahut tez ya non-HTTP ke liye NLB.

### [08:30 – 11:30] Scene 4: Lab: Faisla Karo
**[VISUAL: A quiz card with 5 scenarios. The user drags each to ALB or NLB: "Path-based routing", "Gaming UDP", "Static IP needed", "WebSocket HTTP app", "TLS pass-through at scale".]**

**(Voiceover):**
Lab (paper exercise): paanch situations ke liye tay karo ALB ya NLB. Path ke hisaab se routing: ALB. UDP par game server: NLB. Client ko fixed IP chahiye: NLB. Normal website ke liye HTTP routing: ALB. Aur jahan bahut high throughput hai aur seedha TCP chahiye: NLB. Har jawab ke saath ek line likho ki kyun. Ye "kyun" hi interview mein poochha jaata hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "ALB L7 HTTP routing · NLB L4 fast, static IP".]**

**(Voiceover):**
Recap: ALB aur NLB. Ab andar ke hisse: target groups, health checks aur HTTPS.

---

# 📺 EPISODE 3: Target Groups, Health Checks aur TLS

### [00:00 – 01:15] Scene 1: Load Balancer ko Kaise Pata Server Zinda Hai?
**[VISUAL: A load balancer sending small "pings" to three servers. Two answer with a thumbs-up; one stays silent and is greyed out.]**

**(Voiceover):**
Load balancer har server ko ek chhota sawaal poochta rehta hai: "kya tum theek ho?" Jo jawab nahi deta use rota se hata deta hai. Aur jab wo thik hota hai, wapas jod leta hai. Ye sab target group aur health check se hota hai.

### [01:15 – 05:00] Scene 2: Target Group aur Health Check Settings
**[VISUAL: A target group card with targets (instances/IPs/Lambda), port 80, health check path `/health`, interval 30s, healthy threshold 3, unhealthy threshold 2, success code 200.]**

**(Voiceover):**
Target group servers ka ek set hai jise load balancer traffic bhejta hai. Targets instances, IP addresses ya Lambda ho sakte hain. Health check mein aap path dete ho, jaise `/health`, interval, aur kitni baar pass ya fail hone par target healthy ya unhealthy maana jaye. Ek achha health endpoint sirf "200 OK" nahi, balki app ke zaroori hisse, jaise database connection, bhi check karta hai. Lekin ise itna bhaari mat banao ki health check khud load bana de.

### [05:00 – 08:30] Scene 3: HTTPS aur TLS Termination
**[VISUAL: A browser with a lock → ALB with a certificate (ACM) → plain HTTP to private servers. Listener rules: 80 redirects to 443.]**

**(Voiceover):**
HTTPS ke liye certificate chahiye. AWS Certificate Manager, ACM, mein aap certificate le sakte ho, aur ALB ke listener par HTTPS 443 par lagate ho. Isse TLS termination kehte hain: user se baat load balancer encrypt karke karta hai, aur peeche servers se HTTP ya naye setup mein HTTPS. Port 80 par listener ko 443 par redirect karne ka rule lagao, taaki koi unencrypted na jaye. Certificate ko domain se jodna padta hai, jiske liye DNS validation hoti hai.

### [08:30 – 11:30] Scene 4: Lab: ALB Banao
**[VISUAL: Console: Create target group "web-tg" with health check `/`. Register the two instances. Create ALB, listener on 80 forwarding to web-tg. Copy ALB DNS name; refresh the browser to see alternating hostnames.]**

**(Voiceover):**
Lab: pehle target group `web-tg` banao, protocol HTTP port 80, health check path `/`, aur do instances register karo. Phir Application Load Balancer banao, internet-facing, do AZ ke subnets, aur uske security group mein port 80 kholo. Listener 80 ko `web-tg` par forward karo. ALB ka DNS naam browser mein kholo aur baar baar refresh karo: hostname badalta dikhega. Ek instance par nginx stop karo, kuch der baad wo unhealthy dikhega aur traffic sirf doosre par jayega.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "target group · health check path · ACM cert · redirect 80→443".]**

**(Voiceover):**
Recap: target group, health check, TLS. Ab sab ko jodte hain: ALB ke peeche Auto Scaling Group.

---

# 📺 EPISODE 4: ALB + ASG — Poora Setup aur Debugging

### [00:00 – 01:15] Scene 1: Self-Healing, Self-Scaling Web App
**[VISUAL: An architecture picture: Users → ALB (2 AZ) → ASG (instances in both AZ). A server is terminated; a new one appears automatically.]**

**(Voiceover):**
Ab hum woh architecture banate hain jo asli companies chalati hain: ek ALB, uske peeche Auto Scaling Group, do AZ mein. Server mare to naya khud aata hai, traffic badhe to servers badhte hain, aur user ko pata bhi nahi chalta.

### [01:15 – 05:00] Scene 2: Security Groups ki Chain
**[VISUAL: A layered diagram: Internet → ALB SG (allow 80/443 from anywhere) → Instance SG (allow 80 only from ALB SG).]**

**(Voiceover):**
Security ka ek acha pattern: ALB ke security group mein 80 aur 443 duniya ke liye kholo. Instances ke security group mein port 80 sirf ALB ke security group se allow karo, IP range se nahi, balki security group ko source bana kar. Isse instances seedha internet se access nahi hote, sirf load balancer ke through. Ye defence in depth ka seedha udaharan hai.

### [05:00 – 08:30] Scene 3: Attach ASG aur Health Check Type
**[VISUAL: ASG settings: attach to target group; health check type "ELB" selected; grace period 300s. A diagram showing an unhealthy instance being replaced.]**

**(Voiceover):**
ASG ko target group se attach karo. Aur health check type ko EC2 se ELB badlo, taaki agar load balancer kisi instance ko unhealthy dekhe, to ASG use replace kare, sirf tab nahi jab machine khud mar jaye. Health check grace period do, taaki naya instance boot hone ke samay turant unhealthy na maana jaye. Aur load balancer ka cross-zone behavior ALB mein by default on hota hai, jisse traffic AZ ke beech sahi tarah baantta hai.

### [08:30 – 11:30] Scene 4: Lab: Todo aur Dekho
**[VISUAL: Terminate one instance manually. ASG activity: "Launching a new instance". The ALB target list shows healthy count returning to 2. A troubleshooting flow for 502/503/504.]**

**(Voiceover):**
Lab: ASG ko ALB ke target group se jodo, min 2 aur max 4. Ek instance ko manually terminate karo aur dekho ki ASG ek naya bana deta hai, aur ALB mein healthy count wapas 2 ho jata hai. Ab debugging yaad rakho: 502 matlab backend ne galat jawab diya, 503 matlab koi healthy target nahi, 504 matlab backend ne samay par jawab nahi diya. Pehle target group mein health status dekho, phir security group, phir app ke logs.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "ALB → ASG · SG chain · ELB health type · 502/503/504".]**

**(Voiceover):**
Recap: ek highly available web architecture. Agla session storage ka naya roop: S3, jahan files bahar internet-scale par rakhi jaati hain. Aur cleanup: ALB aur ASG delete karna na bhoolna.

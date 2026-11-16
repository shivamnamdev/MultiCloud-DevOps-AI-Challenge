# ✍️ 02: SCRIPT — SESSION-11: AWS Load Balancing
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S11`
- **Focus:** Why load balancers, ALB vs NLB, listeners and rules, target groups and health checks, TLS termination and ACM, client IP (`X-Forwarded-For`), ALB with Auto Scaling, security group chain, troubleshooting 502, 503 and 504
- **Builds on:** Session 08 (user data, security groups), Session 10 (AMI, launch template, Auto Scaling Group)
- **Story position:** Zoom level 2, the rented campus. Campus ke main gate par ek marshal khada hota hai, jo guests ko sirf unhi buildings ki taraf bhejta hai jo "we are open" kehti hain.
- **Story words used:** marshal (load balancer), guest (end user), sealed envelope (TLS), building (EC2 instance), door guard (security group), tower (Availability Zone), wedding season (scaling)
- **Lab project:** the Atithi booking page served by two buildings behind one gate, then by an Auto Scaling Group behind the same gate.
- **Cost rule:** an Application Load Balancer is billed by the hour while it exists. Every lab ends with deleting the load balancer, target group, ASG and instances.
- **Episodes:**
  - Episode 1: Campus ka Marshal: Load Balancer kyun
  - Episode 2: Do Tarah ke Marshal: ALB vs NLB
  - Episode 3: "Kya Aap Khule Ho?": Target Groups, Health Checks aur TLS
  - Episode 4: Marshal ke Peeche Shaadi ka Season: ALB + ASG aur Debugging

---

# 📺 EPISODE 1: Campus ka Marshal

### [00:00 – 02:20] Scene 1: Ek Counter, Sau Log
**[VISUAL: Atithi's lobby with one open check-in counter and a hundred guests in a queue. Next frame: a marshal at the main gate with a clipboard, pointing guests toward five open counters; the queue vanishes.]**

**(Voiceover):**
Pichhle session mein Atithi ne shaadi ke season ke liye buildings ko photocopy karna seekha. Ab maan lo bees buildings khuli hain. Guest kis building mein jaye? Ek bank mein ek hi counter khula ho aur sau log line mein hon. Ab ek marshal bula lo jo sabko khaali counter par bhej de. Load balancer wahi marshal hai. Wo guests ki requests ko kai buildings mein baant deta hai, aur jo building kharab ho use chhod kar sirf theek buildings ki taraf bhejta hai.

### [02:20 – 04:55] Scene 2: Marshal ke Teen Kaam
**[VISUAL: Three icons around the marshal. 1: arrows spreading evenly to several buildings. 2: a building with a red "closed" sign skipped. 3: one signboard at the gate with the hotel's name, while buildings change behind it.]**

**(Voiceover):**
Marshal ke teen kaam hain. Ek, load baantna, taaki koi ek building na jale. Do, health check: wo har building se poochta rehta hai "kya aap khule ho?", aur jo jawab nahi deti use guest nahi bhejta. Teen, ek hi address: guests ek hi naam par aate hain, aur peeche buildings badalti, badhti aur ghat-ti rehti hain. Isliye marshal aur Auto Scaling hamesha saath chalte hain, ek buildings ki ginti sambhalta hai aur doosra unka raasta. AWS mein is service ka naam Elastic Load Balancing, ELB, hai, aur wo kai tower mein ek saath phailti hai.

### [04:55 – 07:40] Scene 3: Baantne ke Tareeke aur Chipakna
**[VISUAL: Round-robin arrows cycling A → B → C. A second pattern: send to the building with the fewest guests. Then a guest's arrow glued to building B with a cookie icon: "sticky session". A warning beside it: "makes scaling harder".]**

**(Voiceover):**
Marshal guests ko kai tareekon se baant sakta hai. Baari baari se, yaani round robin. Ya us building ko jisme sabse kam guests hain. Kabhi kabhi ek guest ko ek hi building par chipkana padta hai, jaise jab uski kahani us building mein rakhi ho. Ise sticky session kehte hain, aur ye ek cookie se hota hai. Par sticky sessions scaling ko mushkil banate hain: wo building gayi to guest ki kahani gayi. Behtar design: building mein kahani mat rakho. Session ko database ya cache mein rakho, taaki koi bhi building kisi bhi guest ko sambhal sake. Session 10 mein humne ise stateless kaha tha.

### [07:40 – 10:45] Scene 4: Marshal Guest ka Pata Kaise Batata Hai
**[VISUAL: A guest's request arriving at the marshal with their address `203.0.113.7`; the marshal forwards it to a building, and on the request a new header appears: `X-Forwarded-For: 203.0.113.7`. A building's access log line that shows the marshal's address instead of the guest's. An arrow from the header into the log format.]**

**(Voiceover):**
Ek chhoti par aham baat. Jab marshal guest ko building tak bhejta hai, to building ko request marshal se aati dikhti hai, guest se nahi. Isliye building ke logbook mein har guest ka address marshal ka hi hota hai. Guest ka asli address marshal ek chhote header mein likh kar bhejta hai, jiska naam `X-Forwarded-For` hai. Nginx ya app ko wo header padhna aur logbook mein likhna sikhana padta hai. Ye security aur debugging dono ke liye zaroori hai, kyunki warna "koi bahut requests bhej raha hai" ka pata hi nahi chalta ki wo kaun hai. Ek aur dhyaan: ye header koi bhi guest khud bhi bhej sakta hai, isliye usse bharosemand sirf wahi hissa maano jo aapke apne marshal ne likha.

### [10:45 – 13:05] Scene 5: Lab: Do Buildings, Do Pages
**[VISUAL: Two buildings in two different towers launched with user data that writes the hostname into the page. Security group with port 80 open. Two browser tabs show two different hostnames.]**

**(Voiceover):**
Lab ki taiyaari. Do buildings launch karo, alag alag towers mein, yaani alag AZ mein. User data wahi jo Session 8 mein tha, par page mein building ka naam:
```bash
#!/bin/bash
apt-get update -y
apt-get install -y nginx
echo "<h1>Atithi Hotels: Book Now</h1><p>Served by $(hostname)</p>" > /var/www/html/index.html
```
Security group mein 80 kholo. Dono ke public address do alag tabs mein kholo: do alag naam dikhne chahiye. Agle episodes mein inhi ke aage marshal khada karenge. Abhi in dono ko chalta rehne do.

### [13:05 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "distribute · health check · one address · stateless buildings · X-Forwarded-For".]**

**(Voiceover):**
Recap: marshal kya karta hai, kyun, aur guest ka asli address kahan milta hai. Ab AWS ke options: ALB aur NLB, aur kab kaun.

---

# 📺 EPISODE 2: Do Tarah ke Marshal

### [00:00 – 01:25] Scene 1: Dak Ghar vs Courier
**[VISUAL: Two delivery services. One opens each letter, reads who it is for and the subject, and sends it to the right department. The other never opens parcels, only forwards sealed ones extremely fast.]**

**(Voiceover):**
Do tarah ke courier socho. Ek letter ko khol kar padhta hai aur andar likhe ke hisaab se sahi vibhag mein bhejta hai. Doosra sirf sealed parcel ko bahut tez forward karta hai, bina khole. AWS ke marshals mein bhi yahi farq hai.

### [01:25 – 03:55] Scene 2: Application Load Balancer
**[VISUAL: An ALB diagram labelled layer 7. Rules on a board: path `/api/*` → API buildings, path `/photos/*` → photo buildings, host `admin.atithi.example` → admin buildings. Under it: HTTP, HTTPS, WebSocket, gRPC icons.]**

**(Voiceover):**
Application Load Balancer, ALB, wo marshal hai jo letter khol kar padhta hai. Wo OSI ki layer 7 par kaam karta hai, yaani HTTP aur HTTPS samajhta hai. Wo request ka path, host naam, header ya query dekhkar routing karta hai. Jaise `/api/*` booking ki API wali buildings ko, `/photos/*` photo wali buildings ko, aur `admin.atithi.example` admin wali buildings ko. Ek hi marshal ke peeche kai alag services chal sakti hain, isliye microservices aur containers ke liye ALB natural choice hai. Wo WebSocket aur HTTP/2 jaise naye tareeke bhi sambhalta hai. Aur wo apne aap kai towers mein cross-zone baantta hai.

### [03:55 – 06:40] Scene 3: Network Load Balancer aur Baaki
**[VISUAL: An NLB diagram labelled layer 4: TCP, UDP, TLS passing at very high speed, with a fixed address plate per tower. Two greyed cards at the side: Gateway Load Balancer (for inspection appliances) and Classic Load Balancer (legacy).]**

**(Voiceover):**
Network Load Balancer, NLB, wo marshal hai jo parcel nahi kholta. Wo layer 4 par TCP aur UDP ko bahut tez, bahut kam deri ke saath forward karta hai. Har tower ke liye ek pakka address mil sakta hai, jo tab kaam aata hai jab client ko firewall mein ek fixed address likhna ho. Aur wo guest ka asli address building tak le jaata hai. Gateway Load Balancer ek aur marshal hai, jo security appliances, jaise inspection wale firewalls, ke liye hai. Classic Load Balancer purana hai aur naye kaam ke liye nahi chuna jaata. Seedha niyam: web aur HTTP ke liye ALB. Bahut tez ya non-HTTP traffic ke liye, ya fixed address ke liye, NLB.

### [06:40 – 09:10] Scene 4: Marshal ki Suchi: Listener aur Rules
**[VISUAL: A gate with a numbered list. "Listener: port 443 (HTTPS)". Under it, rules in order: 1 if path is `/api/*` forward to api-tg; 2 if host is `admin...` forward to admin-tg; default: forward to web-tg. A card: "first matching rule wins, the default catches the rest".]**

**(Voiceover):**
Marshal ke paas ek suchi hoti hai. Listener batata hai kaun se darwaze, yaani port, par wo sunega, jaise 80 ya 443. Listener ke andar rules: pehla rule, agar path `/api/` se shuru ho to API wali buildings ko. Doosra rule, agar host admin ka ho to admin ko. Aur ek default rule, jo baaki sabko sambhalta hai. Rules ko ek tay kram mein dekha jaata hai, pehla jo milta hai wahi chalta hai, isliye kram ka dhyaan rakho. Ye wahi `case` ka tareeka hai jo Session 6 mein dekha tha: ek lambi `if` ki chain ki jagah saaf suchi.

### [09:10 – 11:50] Scene 5: Marshal ka Kharch aur Ek Marshal ya Kai?
**[VISUAL: A bill with two lines: an hourly charge for the gate and a charge for how much traffic it handled. Left: five marshals for five small services, five hourly charges. Right: one marshal with five rules, one hourly charge. A note: "path rules save money, but one rule mistake affects every service".]**

**(Voiceover):**
Marshal ka bhi kiraya lagta hai: ek hissa ghante ka, jab tak wo khada hai, aur ek hissa is par ki kitni baat-cheet usne sambhali. Isliye agar Atithi ki paanch chhoti services hain, aur aap har ek ke liye alag marshal khada kar do, to paanch ghante ke kiraye lagte hain. Ek marshal ke paanch rules sasta padta hai. Par iske apne sauda hain: ek rule ki galti paanchon services ko hila sakti hai. Isliye bade ya alag teams ke liye kabhi kabhi alag marshal hi theek hota hai. Ek aur jaankari: jis marshal ka koi target nahi bacha, wo bhi bill banata hai. Isliye lab ke baad hamesha use hatao.

### [11:50 – 14:25] Scene 6: Lab: Faisla Karo (Kagaz par)
**[VISUAL: A quiz card with six scenarios. Each is dragged to ALB or NLB with a one-line reason: "path-based routing", "game server over UDP", "client allow-lists a fixed address", "regular website with HTTP routing", "huge TCP throughput, no HTTP inspection needed", "WebSocket chat app".]**

**(Voiceover):**
Lab (kagaz par). Chhe situations ke liye tay karo ALB ya NLB. Path ke hisaab se routing: ALB. UDP par game server: NLB. Client ko ek fixed address chahiye: NLB. Normal website ke liye HTTP routing: ALB. Bahut zyada TCP traffic, HTTP samajhne ki zaroorat nahi: NLB. WebSocket wala chat app: ALB. Har jawab ke saath ek line likho ki kyun. Ye "kyun" hi interview mein poochha jaata hai, aur asli design meeting mein bhi. Ek ulta sawaal bhi socho: ALB ke saath fixed address chahiye to? Uske aage NLB ya Global Accelerator naam ki service lagti hai. Abhi bas ye yaad rakho ki jawab maujood hai.

### [14:25 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "ALB: layer 7 · NLB: layer 4 · listener + rules · default rule · first match wins".]**

**(Voiceover):**
Recap: ALB aur NLB, listener aur rules. Ab andar ke hisse: target group, health check, aur sealed envelope, yaani HTTPS.

---

# 📺 EPISODE 3: "Kya Aap Khule Ho?"

### [00:00 – 01:30] Scene 1: Marshal ko Kaise Pata Building Khuli Hai?
**[VISUAL: The marshal sends a small runner to each building with a card: "Are you open?". Two buildings answer "yes" with a stamp; one stays silent and is greyed out on the marshal's board.]**

**(Voiceover):**
Marshal har building ke paas ek chhota messenger bhejta rehta hai: "kya aap khule ho?" Jo jawab nahi deti, use list se hata deta hai. Jab wo wapas theek ho jaye, use phir list mein jod leta hai. Ye sab target group aur health check se hota hai.

### [01:30 – 04:45] Scene 2: Target Group aur Health Check
**[VISUAL: A target group card. Targets: instances, IP addresses, or a Lambda. Port 80. Health check: path `/health`, interval, timeout, healthy and unhealthy thresholds, success code 200. A traffic-light timeline showing a target going from healthy to unhealthy after consecutive failures.]**

**(Voiceover):**
Target group buildings ka wo set hai jise marshal guests bhejta hai. Targets buildings, IP address, ya Lambda ho sakte hain. Health check mein aap path dete ho, jaise `/health`, interval, aur kitni baar lagataar fail ya pass hone par building unhealthy ya healthy maani jaye. Console mein iske default dikhte hain, unhe dekh kar hi tay karo. Achha health endpoint sirf "200 OK" nahi deta. Wo ye bhi dekhta hai ki building ke zaroori hisse, jaise database ka connection, kaam kar rahe hain. Par ise bhaari mat banao: agar har health check ek lamba kaam kare, to khud health check load ban jaata hai. Aur ek aur baat: agar saari buildings ek saath unhealthy dikhein, to marshal sabko dobara guests bhejne lagta hai, kyunki sab band hone se behtar hai ki kuch to kaam kare.

### [04:45 – 07:50] Scene 3: Sealed Envelope: TLS aur Certificate
**[VISUAL: A browser with a padlock sends a sealed envelope to the marshal's gate. The marshal holds a certificate from ACM and opens the envelope at the gate. Inside the campus the letter travels in a plain envelope to the buildings. A listener card: port 80 → redirect to 443.]**

**(Voiceover):**
HTTPS ke liye certificate chahiye. Guest aur marshal ke beech baat sealed envelope mein hoti hai: ye TLS hai. AWS Certificate Manager, ACM, mein aap certificate le sakte ho, aur ALB ke 443 wale listener par laga sakte ho. Isse TLS termination kehte hain: envelope marshal ke gate par khulta hai, aur peeche buildings ko ya to seedha HTTP ya naye setup mein phir HTTPS mein bheja jaata hai. Port 80 par ek listener rakho jo guest ko 443 par redirect kare, taaki koi bina envelope ke na jaaye. Certificate ek domain ke naam par hota hai, aur ACM ye pakka karne ke liye DNS validation maangta hai, yaani aapko dikhana padta hai ki wo domain aapka hai. Isliye is hisse ko tabhi chalao jab aapke paas apna domain ho.

### [07:50 – 10:20] Scene 4: Health Check Fail Hone par Kya Hota Hai
**[VISUAL: A target in the target group's Targets tab with a status and a reason column: `Target.FailedHealthChecks`, `Target.Timeout`, `Request timed out`. A short decision board: "timeout → security group or port", "wrong code → app or path", "connection refused → service not listening".]**

**(Voiceover):**
Health check fail ho to console mein target ke saamne ek wajah likhi hoti hai. Usse seedha sahi jagah jao. Timeout aaye, to marshal tak building pahunchi hi nahi: security group ne marshal ko roka, ya port galat hai. Galat status code aaye, jaise 404 jab 200 chahiye tha, to ya to path galat hai ya app ne jawab galat diya. Connection refused aaye, to building mil gayi par us port par koi service sun hi nahi rahi. Ye wahi layer-by-layer soch hai jo Session 5 aur Session 8 mein thi: kaun si parat tak pahunche aur kahan ruke.

### [10:20 – 13:05] Scene 5: Lab: Marshal Khada Karo
**[VISUAL: Console: create target group `web-tg` (HTTP 80, health path `/`), register the two buildings. Create an internet-facing ALB in two towers with a security group that allows 80 from anywhere. Listener 80 forwards to `web-tg`. The ALB's DNS name opens in the browser; refreshing alternates the two hostnames. Then `sudo systemctl stop nginx` on one building; its target turns unhealthy.]**

**(Voiceover):**
Lab. Pehle target group `web-tg`: protocol HTTP, port 80, health check path `/`, aur Episode 1 ki do buildings register karo. Phir ek Application Load Balancer banao: internet-facing, do alag towers ke subnets, aur uska apna naya security group jisme 80 duniya ke liye khula ho. Listener 80 ko `web-tg` par forward karo. Provisioning ke baad ALB ka DNS naam browser mein kholo, aur baar baar refresh karo: building ka naam badalta dikhega. Ab ek building par `sudo systemctl stop nginx` chalao. Kuch der mein uska target unhealthy dikhega, aur saare guests sirf doosri building ko jaayenge. Phir nginx wapas chalu karo aur dekho ki target phir healthy ho jaata hai.

### [13:05 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "target group · health check path · reasons column · ACM certificate · redirect 80 → 443".]**

**(Voiceover):**
Recap: target group, health check, aur HTTPS ka sealed envelope. Ab sab ko jodte hain: marshal ke peeche Auto Scaling Group, aur jab sab toote to kya dekhein.

---

# 📺 EPISODE 4: Marshal ke Peeche Shaadi ka Season

### [00:00 – 01:15] Scene 1: Khud Theek, Khud Badhne Wali Site
**[VISUAL: An architecture picture: guests → ALB at the gate (two towers) → ASG with buildings in both towers. One building is terminated; a replacement appears on its own; the marshal's list updates without a guest noticing.]**

**(Voiceover):**
Ab Atithi wo architecture banata hai jo asli companies chalati hain: ek marshal, uske peeche Auto Scaling Group, do towers mein. Building mare to nayi khud aati hai. Shaadi ke season mein buildings badh jaati hain. Aur guest ko ye sab dikhta bhi nahi.

### [01:15 – 03:25] Scene 2: Door Guards ki Zanjeer
**[VISUAL: A chain of door guards. Internet → marshal's guard (allow 80 and 443 from anywhere) → building's guard (allow 80 only from the marshal's guard). A direct internet arrow to a building bounces off.]**

**(Voiceover):**
Ek achha pattern: marshal ke door guard ki list mein 80 aur 443 poori duniya ke liye kholo. Buildings ke door guard ki list mein port 80 sirf marshal ke guard se allow karo. Yahan source mein IP range nahi, balki marshal ka security group likho. Isse buildings seedha internet se nahi, sirf marshal ke raaste se hi milti hain. Ye defence in depth ka seedha udaharan hai, aur isse buildings ke public address ki zaroorat bhi kam ho jaati hai. Aage VPC ke sessions mein hum buildings ko private wing mein rakhne tak ye soch le jayenge.

### [03:25 – 05:45] Scene 3: ASG ko Marshal se Jodna
**[VISUAL: ASG settings: attach to target group `web-tg`; health check type changed from EC2 to ELB; grace period 300 seconds. A diagram: the marshal flags a building unhealthy → ASG terminates and replaces it. Another card: "deregistration delay: the marshal finishes the guests in flight before a building leaves".]**

**(Voiceover):**
ASG ko target group se attach karo. Ab ek zaroori setting: health check type ko EC2 se ELB karo. EC2 type tabhi building badalta hai jab building khud mar jaye. ELB type tab bhi badalta hai jab marshal use unhealthy dekhe, chahe building chal rahi ho par site na chal rahi ho. Saath mein ek grace period do, taaki nayi building ko boot hone ka samay mile, aur wo turant unhealthy na maani jaye. Aur jab building hatayi jaati hai, to marshal pehle chal rahe guests ko khatam hone deta hai. Isko deregistration delay kehte hain, jo by default kuch minute hota hai. Isse guest beech mein nahi kat-ta.

### [05:45 – 08:30] Scene 4: Gadbad ho to: 502, 503, 504
**[VISUAL: Three error stamps. 502 Bad Gateway: a building replied with something the marshal could not use, or hung up. 503 Service Unavailable: there is nobody registered to send the guest to. 504 Gateway Timeout: a building did not answer in time. Under each, the first place to look.]**

**(Voiceover):**
Marshal ke error numbers samjho, kyunki wahi raasta dikhate hain. 502: marshal ko building se aisa jawab mila jo wo samajh nahi paya, ya building ne beech mein baat kaat di. App ke logs dekho, aur ye ki app crash to nahi hui. 503: marshal ke paas bhejne ke liye koi registered building hi nahi hai. Target group khaali to nahi, ya ASG ne kuch register kiya hi nahi? 504: building ne samay par jawab nahi diya. App dheema hai, ya security group beech mein hai, ya marshal ka idle timeout app ke kaam se chhota hai. Pehle target group mein health dekho, phir security groups, phir app ke logs. Aur marshal ka apna access log, jo ek bucket mein likha ja sakta hai, har request ka nateeja aur wajah dikhata hai.

### [08:30 – 10:55] Scene 5: Naya Version Dheere Dheere: Weighted Target Groups
**[VISUAL: A marshal with two target groups: `web-v1` getting 90 percent of guests and `web-v2` 10 percent. A dial moves the split to 50/50, then 0/100. A red "rollback" arrow turns it back in one step. A graph of error rate for the 10 percent group.]**

**(Voiceover):**
Marshal ek aur kaam kar sakta hai: ek rule ke andar do target groups ko alag alag hissa de sakta hai. Maan lo booking page ka naya version `web-v2` taiyaar hai. Pehle sirf dus percent guests use do, nabbe purane ko. Agar naye ke errors nahi badhe, to pachaas, phir sau. Aur agar kuch bigde, to ek hi badlaav mein sab wapas purane par. Isko canary release kehte hain: ek chhoti tukdi pehle. Aage Jenkins aur Kubernetes ke sessions mein hum yahi sochenge, par yahan ye ALB ki taakat dikhne ka sabse saaf udaharan hai. Aur isse yaad aata hai ki ALB ka kaam sirf baantna nahi, deploy ko surakshit banana bhi hai.

### [10:55 – 13:45] Scene 6: Lab: Building Todo aur Dekho
**[VISUAL: Create a launch template from `atithi-web-v1`, an ASG with min 2, max 4, attached to `web-tg`, health check type ELB. One building is terminated manually. The Activity tab shows "Launching a new EC2 instance". The marshal's target list returns from 1 to 2 healthy. Then cleanup: delete the ASG, the ALB, the target group, the AMI and its snapshot.]**

**(Voiceover):**
Lab. Session 10 ke AMI se ek launch template aur ek ASG banao: minimum 2, maximum 4, `web-tg` se attached, health check type ELB. Episode 1 ki do haath se banayi buildings ko ab target group se hata do aur terminate kar do. Ab ASG ki nayi buildings dikhengi, aur ALB ka DNS naam kholne par page chalega. Ek building ko haath se terminate karo, aur dekho ki ASG nayi bana deta hai, aur marshal ki list mein healthy count wapas do ho jaata hai. Phir ek building par nginx band karke dekho ki marshal use unhealthy maan kar ASG ko batata hai, aur ASG use badal deta hai. Aakhir mein safai ka kram: ASG, phir ALB, phir target group, phir AMI aur uska snapshot. ALB ghante ke hisaab se chalta hai, isliye ise sabse pehle mat bhoolna.

### [13:45 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "ALB → ASG · SG chain · health check type ELB · grace period · 502 / 503 / 504". Then the warehouse from Session 0's map comes into view: rows of labelled boxes stretching to the horizon.]**

**(Voiceover):**
Recap: ek highly available web architecture: marshal, Auto Scaling, door guards ki zanjeer, aur error numbers. Ab Atithi ki site ke paas apna gate, apni buildings aur apna storage hai. Par booking site ki photos aur brochures ke liye building ka storeroom bahut mehnga aur bahut chhota hai. Agla session ek anant gaudam, S3, ka hai: jahan files internet ke paimane par rakhi jaati hain, building mein nahi. Aur cleanup: ALB aur ASG delete karna na bhoolna.

---

# 📎 Student handout: Session 11 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Marshal ke kaam | Baantna, health check, ek address |
| ALB | Layer 7, HTTP aur HTTPS, path, host, header ke hisaab se rules |
| NLB | Layer 4, TCP, UDP, TLS; tez; har tower ke liye pakka address |
| Listener | Port aur protocol; rules ek kram mein, pehla match jeetta hai, default sabse neeche |
| Target group | Buildings, IP ya Lambda; health check path, interval, thresholds |
| Health fail wajah | Timeout (SG ya port), galat code (app ya path), refused (service nahi sun rahi) |
| TLS | ACM certificate ALB par; 80 se 443 par redirect; DNS validation ke liye domain |
| Guest ka address | `X-Forwarded-For` header |
| SG zanjeer | Marshal: 80/443 sabko. Buildings: 80 sirf marshal ke SG se |
| ASG + ALB | Target group se attach, health check type ELB, grace period |
| 502 | Building ka jawab samajh nahi aaya, ya baat kaati |
| 503 | Koi registered building nahi |
| 504 | Building ne samay par jawab nahi diya |
| Safai | ASG, ALB, target group, AMI + snapshot, volumes |

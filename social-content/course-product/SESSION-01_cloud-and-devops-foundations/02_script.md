# ✍️ 02: SCRIPT — SESSION-01: Cloud & DevOps Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording, no source text reused).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S01`
- **Focus:** Servers before cloud, virtualization, IaaS/PaaS/SaaS, what DevOps really is, the CI/CD loop
- **Episodes:**
  - Episode 1: Cloud se pehle ki duniya: servers, data center aur virtualization
  - Episode 2: Cloud kya hai: IaaS, PaaS, SaaS aur Shared Responsibility
  - Episode 3: DevOps kya hai: Dev aur Ops ke beech ki deewar
  - Episode 4: The Delivery Loop: CI/CD, tools ka map aur aapka roadmap

---

# 📺 EPISODE 1: Cloud se pehle ki duniya

### [00:00 – 01:30] Scene 1: Ek Startup, Ek Server Room
**[VISUAL: Dark office, a small server rack humming in a cupboard. A calendar flips to "Sale Day". A red graph spikes, the server LED turns red, a phone rings. Text slams: "SALE START. SERVER DOWN."]**

**(Voiceover):**
Maan lijiye aapne ek online kapde ki dukaan kholi. Ek server kharida, office ki almari mein rakha, aur kaam chal gaya. Phir sale ka din aaya. Achanak hazaar ki jagah pachas hazaar log website par aa gaye. Server ki CPU sau percent, website slow, phir band. Ab aap naya server order karte ho, aur wo aata hai teen hafte baad. Tab tak sale khatam. Yahi hai cloud se pehle ki duniya. Is module ka sawaal simple hai: jab computing power ko bijli ki tarah on-demand mil sakti hai, to hum purane tareeke se kyun fase the? Chaliye, shuru se samajhte hain.

### [01:30 – 04:00] Scene 2: Physical Server aur Data Center ki Problems
**[VISUAL: A server rack diagram builds up: power, cooling, network cable, UPS, guard. Each item gets a price tag that fills a "Capex" bucket.]**

**(Voiceover):**
Ek physical server sirf ek machine nahi hota. Uske saath jagah chahiye, bijli, backup power, thanda rakhne ke liye cooling, network, security aur ek admin jo raat ko bhi alert sun sake. Ye sab upfront kharch hai, isse capital expenditure kehte hain. Aur sabse bada dard: aapko peak load ke hisaab se server kharidna padta tha, jabki saal ke zyadatar din machine aadhi khaali rehti thi. Ise kehte hain over-provisioning. Ulta, kam server liya to peak par fail. Dono taraf nuksaan.

### [04:00 – 07:30] Scene 3: Virtualization aur Hypervisor
**[VISUAL: One big physical box splits into three transparent rooms labelled VM1, VM2, VM3. A thin layer on top of hardware is labelled "Hypervisor". Each VM has its own OS and app.]**

**(Voiceover):**
Pehli badi chaal thi virtualization. Socho ek bada flat hai. Pehle usme ek hi parivaar rehta tha aur baaki kamre khaali. Virtualization ne flat ko kamron mein baant diya, har kamre ka apna darwaza aur apna kirayedaar. Technically, ek hardware ke upar hypervisor naam ka software baithta hai. Wo CPU, RAM aur disk ko baant kar kai virtual machines banata hai. Har VM ko lagta hai ki wo akeli poori machine hai, apna operating system, apne apps. Isolation milta hai: ek VM crash ho to doosre chalte rehte hain. Aur hardware ka use badhta hai, kyunki ek server par kai kaam chalte hain.

### [07:30 – 11:00] Scene 4: Type-1 vs Type-2 aur Lab: Pehli VM
**[VISUAL: Two stacks side by side. Left: Hardware → Hypervisor → VMs (Type 1). Right: Hardware → Host OS → Hypervisor app → VMs (Type 2). Then a screen recording of VirtualBox creating a VM.]**

**(Voiceover):**
Hypervisor do tarah ke hote hain. Type-1 seedha hardware par chalta hai, jaise KVM ya VMware ESXi, aur data center mein yahi use hota hai. Type-2 aapke laptop ke OS ke upar app ki tarah chalta hai, jaise VirtualBox. Seekhne ke liye Type-2 kaafi hai. Aaj ka lab: VirtualBox install karo, ek naya VM banao, 2 GB RAM aur 20 GB disk do, aur dekho ki aapke laptop ke andar ek alag computer boot ho raha hai. Cloud mein jab aap ek server launch karte ho, peeche ye hi idea bade scale par chal raha hota hai.

### [11:00 – 12:30] Scene 5: Recap aur Bridge
**[VISUAL: Three-line recap card: "Problem: slow, costly servers → Fix: virtualization → Next: rent them over the internet".]**

**(Voiceover):**
Recap: physical server mehenge aur dheere the, virtualization ne ek machine ko kai machines mein badla. Lekin ab bhi machine aapki thi, aapke data center mein. Agar koi ye machines kiraye par de de, aur wo bhi minutes mein? Wo hai cloud. Agle episode mein dekhenge ki cloud assal mein hai kya, aur ye IaaS, PaaS, SaaS ke teen shabd kya bolte hain.

---

# 📺 EPISODE 2: Cloud kya hai?

### [00:00 – 01:15] Scene 1: Bijli ka Bill ya Generator?
**[VISUAL: Split screen. Left: a household with its own noisy diesel generator. Right: a plug in the wall with a meter. Text: "Own it" vs "Rent it, pay per use".]**

**(Voiceover):**
Ghar mein bijli ke do tareeke hain. Ya to apna generator rakho, tel bharo, repair karao. Ya board se connection lo, jitni chalaao utna bill do. Cloud computing bilkul doosra tareeka hai: servers, storage, database, networking, sab internet par kiraye par, jitna use karo utna paisa. Na intezaar, na upfront kharch. Aur aaj ka sabse bada fayda: aap ek button se ek sau server bhi launch kar sakte ho aur kaam khatam hone par band bhi.

### [01:15 – 04:30] Scene 2: Cloud ke Paanch Gun
**[VISUAL: Five icons appear one by one: Self-service, Network access, Resource pool, Elasticity, Metered billing.]**

**(Voiceover):**
Cloud ki pehchaan paanch baaton se hoti hai. Self-service: aap khud console ya API se resource maangte ho. Broad network access: internet se kahin se bhi. Resource pooling: provider ke bade pool se aapko hissa milta hai. Elasticity: load badhe to resource badhao, ghate to ghatao. Aur measured service: jitna use, utna bill. Dhyaan rakhna, sirf "kisi aur ka server" ko cloud nahi kehte. Agar aap ticket daal kar teen din baad machine paate ho, to wo hosting hai, cloud nahi.

### [04:30 – 08:30] Scene 3: IaaS, PaaS, SaaS: Pizza Analogy
**[VISUAL: Four columns: "Home-made", "Take and bake", "Pizza delivered", "Dine-in". Layers listed on the left (Networking, Storage, Servers, OS, Runtime, App, Data) with colours showing who manages what.]**

**(Voiceover):**
Isko pizza se samjho. Ghar par poora pizza banao: aate se lekar oven tak sab aapka. Ye on-premises hai. IaaS mein kiraye ka kitchen mila, ingredients aur sab aap laate ho: jaise AWS EC2 ya Google Compute Engine, machine milti hai, OS aur app aap sambhalo. PaaS mein tayaar dough aur oven, aap sirf topping lagao: jaise Google App Engine, aap sirf code do. SaaS mein pizza seedha table par: Gmail, Google Docs, aap sirf use karte ho. Jaise jaise upar jaate ho, control kam, aur dimaagi bojh bhi kam.

### [08:30 – 11:30] Scene 4: Public, Private, Hybrid aur Shared Responsibility
**[VISUAL: Three cloud shapes: public (shared building), private (own house), hybrid (house with a flat in the building). Then a split bar: "Security OF the cloud" (provider) vs "Security IN the cloud" (you).]**

**(Voiceover):**
Deployment ke teen model: public cloud, jaise AWS, Azure, GCP; private cloud, sirf ek company ke liye; hybrid, dono ka mix. Ab ek zaroori baat: shared responsibility model. Provider zimmedar hai data center, hardware aur hypervisor ki security ka. Lekin aapka data, aapki permissions, aapka firewall, aapka password, wo aapki zimmedari hai. Duniya ke zyadatar cloud leaks provider ki galti se nahi, galat configuration se hote hain. Isliye is course mein har cloud session ke saath security ki aadat banayenge.

### [11:30 – 13:00] Scene 5: Lab aur Bridge
**[VISUAL: Screen recording: opening the free-tier page of a cloud provider, then a checklist: "Billing alert ON", "MFA ON", "No root usage".]**

**(Voiceover):**
Homework lab: ek cloud account ke liye ready ho jao. Abhi account banana zaroori nahi, par sab providers ke free-tier rules padho aur ek baat note karo: billing alert pehle din lagana hai. Cloud mein "bhool gaya band karna" sabse mehnga sabak hota hai. Ab aapko pata hai ki cloud kya hai. Agla sawaal: jab ye sab itna aasaan hai, to dev aur ops ke beech jhagde kyun hote the? Episode 3 mein DevOps ki wo deewar girate hain.

---

# 📺 EPISODE 3: DevOps kya hai?

### [00:00 – 01:30] Scene 1: "Mere Laptop Par To Chal Raha Tha"
**[VISUAL: A developer shrugs with a laptop showing a green app. Next frame: an ops engineer at a server with a red error. Between them a literal brick wall labelled "Throw it over the wall".]**

**(Voiceover):**
Ek purani kahaani. Developer ne feature banaya, apne laptop par chalaya, sab theek. Code ops team ko diya gaya. Production par wo chala hi nahi. Developer bola, mere laptop par to chal raha tha. Ops bola, hum to bas deploy karte hain, code galat hai. Dono sahi the, aur dono phase the. Kyunki dono ke goal alag the: developer ko naye features chahiye, ops ko stability. Naya release matlab risk, isliye ops release rokta tha. Deewar yahin se bani.

### [01:30 – 05:00] Scene 2: DevOps ki Definition aur Culture
**[VISUAL: The wall cracks and dissolves. Two circles (Dev, Ops) merge into one loop labelled "You build it, you run it".]**

**(Voiceover):**
DevOps koi tool ya job title bhar nahi, ye kaam karne ka tareeka hai. Seedhi baat: dev aur ops ek hi team ki tarah poore lifecycle ki zimmedari lete hain, plan se lekar production monitoring tak. Isme culture pehle aata hai, tools baad mein. Chhote chhote releases baar baar, kyunki chhota change fail ho to dhoondhna aasaan. Automation, kyunki insaan thakta hai, script nahi. Measurement, kyunki bina naape sudhar nahi hota. Aur sharing, kyunki jo ek ko pata hai, poori team ko pata hona chahiye.

### [05:00 – 08:30] Scene 3: DevOps Lifecycle ka Infinity Loop
**[VISUAL: An infinity symbol. Left loop: Plan → Code → Build → Test. Right loop: Release → Deploy → Operate → Monitor. Arrow from Monitor back to Plan.]**

**(Voiceover):**
DevOps ko ek infinity loop ki tarah dekho. Plan, code, build, test: ye hissa banane ka hai. Release, deploy, operate, monitor: ye hissa chalane ka hai. Aur monitor se jo seekh mili, wo wapas plan mein jaati hai. Ye loop kabhi khatam nahi hota. Hamare course ka naam isi se juda hai: Build, Ship, Fix. Build matlab code se artifact, Ship matlab usse safely production tak pahunchana, Fix matlab jab wo toote to jaldi pakadna aur theek karna.

### [08:30 – 12:00] Scene 4: Waterfall vs Agile vs DevOps
**[VISUAL: Three timelines: a long waterfall staircase, small agile sprints, and tiny rapid DevOps releases looping continuously.]**

**(Voiceover):**
Pehle software waterfall mein banta tha: requirement, design, code, test, release, har step ke baad agla, aur feedback saal bhar baad. Agile ne development ko chhote sprints mein baant diya, lekin release ab bhi ops ke paas atka rehta tha. DevOps ne wo aakhri deewar bhi hatayi: code likhte hi test, package aur release automatic. Result: din mein kai baar deploy, aur wo bhi kam darr ke saath. Dhyaan rahe: speed ka matlab laaparwahi nahi, automation ke bharose tez chalna hai.

### [12:00 – 13:30] Scene 5: Lab aur Bridge
**[VISUAL: A notebook page titled "My last release" with three prompts: Who deployed? How long? What broke?]**

**(Voiceover):**
Lab: kisi bhi chhote project ko dimaag mein rakho, apna ya office ka. Teen sawaal likho: deploy kaun karta hai, kitna time lagta hai, aur pichli baar kya toota. Jo steps haath se hote hain, unke aage star lagao. Ye star hi aapki automation ki list hain. Agle episode mein hum us list ko CI/CD ke saath jodenge aur poore course ka map dekhenge.

---

# 📺 EPISODE 4: The Delivery Loop aur Aapka Roadmap

### [00:00 – 01:30] Scene 1: Haath se Deploy ka Dard
**[VISUAL: A person typing 12 commands on a server, copy-pasting from a text file, and one typo turns the screen red. Counter: "Manual steps: 12".]**

**(Voiceover):**
Soch ke dekho: har release ke liye barah commands, ek text file se copy karke. Ek jagah typo, aur raat ki neend gayi. Isi dard ko door karne ke liye CI/CD aaya. CI, Continuous Integration, matlab sabka code baar baar ek shared jagah milaya jaye aur har baar automatic build aur test chale. CD, Continuous Delivery ya Deployment, matlab jo pass ho gaya wo ready-to-release ho, ya seedha production tak chala jaye.

### [01:30 – 05:00] Scene 2: Ek Pipeline ki Shakal
**[VISUAL: A conveyor belt of stages: Commit → Build → Unit tests → Package (artifact) → Deploy to staging → Smoke test → Deploy to prod → Monitor. Green ticks run across; one stage turns red and the belt stops.]**

**(Voiceover):**
Ek pipeline ek conveyor belt hai. Developer code commit karta hai, ye belt chalu ho jati hai: build, tests, package, staging par deploy, smoke test, aur phir production. Jahan bhi koi stage fail, belt ruk jati hai aur team ko turant pata chalta hai. Pipeline ke do fayde: speed, aur repeatability. Jo kaam aaj haath se aap karte ho, kal ek button se ya bina button ke, har baar ek jaisa hoga.

### [05:00 – 08:30] Scene 3: DevOps Tools ka Map
**[VISUAL: A circular map: Linux/Bash/Python (base) → Git → CI (Jenkins, GitHub Actions) → Docker → Kubernetes → Terraform/Ansible → Prometheus/Grafana → Cloud (AWS/Azure/GCP).]**

**(Voiceover):**
Ab course ka map. Neeche base: Linux, Bash, Python. Phir version control, Git. Uske upar CI/CD, Jenkins aur GitHub Actions. Phir containers, Docker, aur unhe chalane ke liye Kubernetes. Infrastructure ko code mein likhne ke liye Terraform aur Ansible. Dekhne ke liye Prometheus aur Grafana. Aur sab kuch cloud par, AWS, Azure aur GCP. Ek baat yaad rakho: tool badlte rehte hain, concept nahi. Isliye hum pehle sawaal poochhenge: ye tool kis dard ko door karta hai.

### [08:30 – 11:30] Scene 4: AI ki Jagah aur DevOps Engineer ka Kaam
**[VISUAL: A DevOps engineer's day: reading an alert, checking logs, reviewing a pipeline diff, asking an AI assistant for a draft, verifying it with a stamp "Reviewed by human".]**

**(Voiceover):**
DevOps engineer ka din kya hota hai? Pipelines banana aur sudharna, infrastructure ko code mein sambhalna, alerts dekhna, incident aane par logs padhna aur fix nikalna, aur security aur cost par nazar. AI is kaam mein tez draft de sakta hai, par wo aapke production ka context nahi jaanta. Isliye ye course aapko AI ke saath chalna sikhayega: draft AI ka, jaanch aapki. Pilot aap, autopilot AI.

### [11:30 – 13:00] Scene 5: Lab aur Next Session Bridge
**[VISUAL: A checklist: "Create GitHub account", "Install VS Code", "Install Git", "Pick a cloud (AWS free tier)", each ticking.]**

**(Voiceover):**
Aaj ka lab, setup. GitHub account banao, VS Code aur Git install karo, aur ek cloud free-tier ke liye taiyaar raho. Pehla assignment: apne last release ki list se ek haath wala step chuno jise aap automate karna chahte ho. Hum is course mein usse sach mein automate karenge. Agla session AI ka hai: ek co-programmer ki tarah AI ko kaise use karna hai, bina uspar aandhi bharosa kiye.

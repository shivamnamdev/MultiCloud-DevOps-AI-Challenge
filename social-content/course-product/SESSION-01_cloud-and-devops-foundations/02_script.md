# ✍️ 02: SCRIPT — SESSION-01: Cloud & DevOps Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording, no source text reused). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S01`
- **Focus:** Servers before cloud, virtualization, IaaS/PaaS/SaaS, what DevOps really is, the CI/CD loop
- **Story position:** All three zoom levels. Ye session kahaani shuru karta hai: aap Atithi Hotels naam ki hotel company khol rahe ho.
- **Story words introduced:** guest (end user), staff (server aur cloud ke users), building (server ya VM), tower aur building engineer (physical machine aur hypervisor), landlord (cloud provider), khaali building / serviced banquet hall / booked room (IaaS / PaaS / SaaS), head office, conveyor (pipeline), assistant (AI), teen zoom levels
- **Episodes:**
  - Episode 1: Cloud se pehle ki duniya: servers, data center aur virtualization
  - Episode 2: Cloud kya hai: IaaS, PaaS, SaaS aur Shared Responsibility
  - Episode 3: DevOps kya hai: Dev aur Ops ke beech ki deewar
  - Episode 4: The Delivery Loop: CI/CD, tools ka map aur aapka roadmap

---

# 📺 EPISODE 1: Cloud se pehle ki duniya

### [00:00 – 03:50] Scene 1: Ek Hotel Company, Ek Server Room
**[VISUAL: Title card "Atithi Hotels". An empty plot of land, months of construction on a calendar, no guests yet. Cut to a dark office, a small server rack humming in a corner. A calendar flips to "Sale Day". A red graph spikes, the server LED turns red, a phone rings. Text slams: "SALE START. SERVER DOWN."]**

**(Voiceover):**
Is poore course mein ek hi kahaani chalegi. Aap ek hotel company shuru kar rahe ho: Atithi Hotels. Atithi Devo Bhava, yaani guest sabse pehle. Hamare liye guest hai website ka end user. Ab purana tareeka socho: zameen kharido, building banao, generator lagao, guard rakho. Mahino lag gaye aur lakhon kharch ho gaye, tab jaakar pehla guest aaya. Software ki duniya mein bhi yahi hota tha. Maan lijiye aapne ek online kapde ki dukaan kholi. Ek server kharida, office ke ek kone mein rakha, aur kaam chal gaya. Phir sale ka din aaya. Achanak hazaar ki jagah pachas hazaar log website par aa gaye. Server ki CPU sau percent, website slow, phir band. Ab aap naya server order karte ho, aur wo aata hai teen hafte baad. Tab tak sale khatam. Yahi hai cloud se pehle ki duniya. Is session ka sawaal simple hai: jab tayaar building minutes mein kiraye par mil sakti hai, to hum purane tareeke se kyun fase the? Chaliye, shuru se samajhte hain.

### [03:50 – 06:00] Scene 2: Physical Server aur Data Center ki Problems
**[VISUAL: A server rack diagram builds up: power, cooling, network cable, UPS, guard. Beside it, a hotel building with its own generator, AC plant and guard. Each item gets a price tag that fills a "Capex" bucket.]**

**(Voiceover):**
Ek physical server sirf ek machine nahi hota. Jaise apni building ke saath zameen, generator, AC aur guard aate hain, waise hi server ke saath jagah chahiye, bijli, backup power, thanda rakhne ke liye cooling, network, security aur ek admin jo raat ko bhi alert sun sake. Ye sab upfront kharch hai, isse capital expenditure kehte hain. Aur sabse bada dard: aapko peak load ke hisaab se server kharidna padta tha, jabki saal ke zyadatar din machine aadhi khaali rehti thi. Ise kehte hain over-provisioning. Ulta, kam server liya to peak par fail. Dono taraf nuksaan.

### [06:00 – 09:05] Scene 3: Virtualization aur Hypervisor
**[VISUAL: One huge tower with a single hotel on the ground floor and empty floors above. A building engineer divides it into three independent buildings labelled VM1, VM2, VM3, each with its own entrance. A thin layer on top of the hardware is labelled "Hypervisor". Each VM has its own OS and app.]**

**(Voiceover):**
Pehli badi chaal thi virtualization. Socho ek bada tower hai jisme ek hi hotel chal raha hai, aur zyadatar floors khaali pade hain. Ek building engineer us tower ko kai alag, independent buildings mein baant deta hai. Har building ka apna darwaza, apna staff aur apna management. Technically, ek hardware ke upar hypervisor naam ka software baithta hai, wahi hamara building engineer hai. Wo CPU, RAM aur disk ko baant kar kai virtual machines banata hai. Har VM ko lagta hai ki wo akeli poori machine hai, apna operating system, apne apps. Isolation milta hai: ek VM crash ho to doosre chalte rehte hain. Aur hardware ka use badhta hai, kyunki ek server par kai kaam chalte hain. Is course mein jab bhi hum "building" bolenge, uska matlab hoga ek server ya ek VM.

### [09:05 – 11:20] Scene 4: Type-1 vs Type-2 aur Lab: Pehli VM
**[VISUAL: Two stacks side by side. Left: Hardware → Hypervisor → VMs (Type 1). Right: Hardware → Host OS → Hypervisor app → VMs (Type 2). Then a screen recording of VirtualBox creating a VM.]**

**(Voiceover):**
Hypervisor do tarah ke hote hain. Type-1 seedha hardware par chalta hai, jaise KVM ya VMware ESXi, aur data center mein yahi use hota hai. Type-2 aapke laptop ke OS ke upar app ki tarah chalta hai, jaise VirtualBox. Seekhne ke liye Type-2 kaafi hai. Aaj ka lab: VirtualBox install karo, ek naya VM banao, 2 GB RAM aur 20 GB disk do, aur dekho ki aapke laptop ke andar ek alag computer boot ho raha hai. Cloud mein jab aap ek server launch karte ho, peeche ye hi idea bade scale par chal raha hota hai.

### [11:20 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: Three-line recap card: "Problem: slow, costly servers → Fix: virtualization → Next: rent them over the internet".]**

**(Voiceover):**
Recap: physical server mehenge aur dheere the, virtualization ne ek machine ko kai machines mein badla, jaise ek tower ko kai buildings mein. Lekin ab bhi tower aapka tha, aapke data center mein. Agar koi landlord bani banayi buildings kiraye par de de, aur wo bhi minutes mein? Wo hai cloud. Agle episode mein dekhenge ki cloud assal mein hai kya, aur ye IaaS, PaaS, SaaS ke teen shabd kya bolte hain.

---

# 📺 EPISODE 2: Cloud kya hai?

### [00:00 – 02:35] Scene 1: Zameen Kharido ya Building Kiraye par Lo?
**[VISUAL: Split screen. Left: the Atithi founder at a construction site beside a noisy diesel generator. Right: a skyline of ready towers with a "Rent by the hour" meter and three signboards: AWS, Azure, GCP. Text: "Own it" vs "Rent it, pay per use".]**

**(Voiceover):**
Atithi Hotels ke saamne do raaste hain. Ya to apni zameen kharido, building banao, generator mein tel bharo, repair karao. Ya ek landlord se bani banayi building kiraye par lo, ghante ke hisaab se, aur kaam khatam ho to wapas kar do. Cloud computing doosra raasta hai. Teen bade landlord hain, AWS, Azure aur GCP, jinhone duniya ke bade shehron mein tayaar towers bana rakhe hain. Servers, storage, database, networking, sab internet par kiraye par, jitna use karo utna paisa. Zameen, bijli aur maintenance landlord ki. Na intezaar, na upfront kharch. Aur aaj ka sabse bada fayda: aap ek button se ek sau server bhi launch kar sakte ho aur kaam khatam hone par band bhi.

### [02:35 – 05:35] Scene 2: Cloud ke Paanch Gun
**[VISUAL: Five icons appear one by one: Self-service, Network access, Resource pool, Elasticity, Metered billing. At "Elasticity", one furnished building is photocopied into five, then four fade away.]**

**(Voiceover):**
Cloud ki pehchaan paanch baaton se hoti hai. Self-service: aap khud console ya API se resource maangte ho. Broad network access: internet se kahin se bhi. Resource pooling: provider ke bade pool se aapko hissa milta hai. Elasticity: load badhe to resource badhao, ghate to ghatao. Aur measured service: jitna use, utna bill. Hamari kahaani ka ek jaadui rule yahin se aata hai: is duniya mein saji sajayi building ki minutes mein photocopy ho sakti hai, aur use bina kharch giraya bhi ja sakta hai. Asli imaarat ke saath ye nahi hota, software ke saath hota hai, aur cloud ki poori taakat isi mein hai. Dhyaan rakhna, sirf "kisi aur ka server" ko cloud nahi kehte. Agar aap ticket daal kar teen din baad machine paate ho, to wo hosting hai, cloud nahi.

### [05:35 – 08:15] Scene 3: IaaS, PaaS, SaaS: Khaali Building, Banquet Hall, Booked Room
**[VISUAL: Four columns: "Apni zameen (On-premises)", "Khaali building kiraye par (IaaS)", "Serviced banquet hall (PaaS)", "Booked room (SaaS)". Layers listed on the left (Networking, Storage, Servers, OS, Runtime, App, Data) with colours showing who manages what.]**

**(Voiceover):**
Ise Atithi ke saamne khule raaston se samjho. Apni zameen par apni building: neev se lekar bedsheet tak sab aapka. Ye on-premises hai. IaaS mein landlord se ek khaali building kiraye par mili: deewarein, bijli aur paani landlord ke, par andar ka poora intezaam aapka. Jaise AWS EC2 ya Google Compute Engine: machine milti hai, OS aur app aap sambhalo. PaaS ek serviced banquet hall hai: hall, staff aur kitchen sab tayaar, aap sirf apna event lekar aao. Jaise Google App Engine, aap sirf code do. SaaS mein aap bas ek kamra book karte ho aur rehte ho: Gmail, Google Docs, aap sirf use karte ho. Jaise jaise upar jaate ho, control kam, aur dimaagi bojh bhi kam.

### [08:15 – 11:00] Scene 4: Public, Private, Hybrid aur Shared Responsibility
**[VISUAL: Three pictures: public (the landlord's towers shared by many companies), private (a campus built for one company only), hybrid (your own old hotel plus rented buildings, joined by a road). Then a split bar: "Security OF the cloud" (provider) vs "Security IN the cloud" (you).]**

**(Voiceover):**
Deployment ke teen model. Public cloud, jaise AWS, Azure, GCP, jahan landlord ke towers kai companies share karti hain. Private cloud, sirf ek company ke liye bana campus. Aur hybrid, yaani apna purana hotel aur kiraye ki buildings, dono ka mix. Ab ek zaroori baat: shared responsibility model. Landlord zimmedar hai zameen, imaarat aur bijli ka, yaani data center, hardware aur hypervisor ki security ka. Lekin building ke andar ke taale, kiske paas kaun si chaabi hai, aur darwaze ka guard, ye sab aapki zimmedari hai. Yaani aapka data, aapki permissions, aapka firewall, aapka password. Duniya ke zyadatar cloud leaks provider ki galti se nahi, galat configuration se hote hain. Isliye is course mein har cloud session ke saath security ki aadat banayenge.

### [11:00 – 13:05] Scene 5: Lab aur Bridge
**[VISUAL: Screen recording: opening the free-tier page of a cloud provider, then a checklist: "Billing alert ON", "MFA ON", "No root usage".]**

**(Voiceover):**
Homework lab: ek cloud account ke liye ready ho jao. Abhi account banana zaroori nahi, par sab providers ke free-tier rules padho aur ek baat note karo: billing alert pehle din lagana hai. Cloud mein "bhool gaya band karna" sabse mehnga sabak hota hai, kyunki kiraye ki building khaali padi ho tab bhi meter chalta rehta hai. Ab aapko pata hai ki cloud kya hai. Agla sawaal: jab building itni aasaani se milti hai, to dev aur ops ke beech jhagde kyun hote the? Episode 3 mein DevOps ki wo deewar girate hain.

---

# 📺 EPISODE 3: DevOps kya hai?

### [00:00 – 03:25] Scene 1: "Mere Laptop Par To Chal Raha Tha"
**[VISUAL: Atithi head office: a designer throws a rolled-up service design over a brick wall to a hotel operator, who looks at a queue of unhappy guests. The scene morphs: a developer shrugs with a laptop showing a green app; an ops engineer at a server with a red error. The wall is labelled "Throw it over the wall".]**

**(Voiceover):**
Atithi Hotels mein do tarah ke log hain. Head office ke designers, jo naye services design karte hain. Aur hotel chalane wale operators, jinhe guest ke saamne sab kuch theek rakhna hai. Designer ne naya design deewar ke us paar phenk diya, aur hotel mein wo chala hi nahi. Software mein bilkul yahi purani kahaani hai. Developer ne feature banaya, apne laptop par chalaya, sab theek. Code ops team ko diya gaya. Production par wo chala hi nahi. Developer bola, mere laptop par to chal raha tha. Ops bola, hum to bas deploy karte hain, code galat hai. Dono sahi the, aur dono phase the. Kyunki dono ke goal alag the: developer ko naye features chahiye, ops ko stability. Naya release matlab risk, isliye ops release rokta tha. Deewar yahin se bani.

### [03:25 – 06:40] Scene 2: DevOps ki Definition aur Culture
**[VISUAL: The wall cracks and dissolves. In its place a conveyor runs from head office to the hotels, and a feedback arrow runs back from the guests. Two circles (Dev, Ops) merge into one loop labelled "You build it, you run it".]**

**(Voiceover):**
DevOps koi tool ya job title bhar nahi, ye kaam karne ka tareeka hai. Seedhi baat: dev aur ops ek hi team ki tarah poore lifecycle ki zimmedari lete hain, plan se lekar production monitoring tak. Atithi mein iska matlab hai: designers aur operators ek hi team, aur dono ke beech deewar ki jagah ek conveyor. Naya kaam us conveyor se seedha hotel tak pahunchta hai, aur guest ka feedback wapas head office aata hai. Isme culture pehle aata hai, tools baad mein. Chhote chhote releases baar baar, kyunki chhota change fail ho to dhoondhna aasaan. Automation, kyunki insaan thakta hai, script nahi. Measurement, kyunki bina naape sudhar nahi hota. Aur sharing, kyunki jo ek ko pata hai, poori team ko pata hona chahiye.

### [06:40 – 08:45] Scene 3: DevOps Lifecycle ka Infinity Loop
**[VISUAL: An infinity symbol. Left loop: Plan → Code → Build → Test. Right loop: Release → Deploy → Operate → Monitor. Arrow from Monitor back to Plan, labelled "guest feedback".]**

**(Voiceover):**
DevOps ko ek infinity loop ki tarah dekho. Plan, code, build, test: ye hissa banane ka hai. Release, deploy, operate, monitor: ye hissa chalane ka hai. Aur monitor se jo seekh mili, yaani guest ka feedback, wo wapas plan mein jaati hai. Ye loop kabhi khatam nahi hota. Hamare course ka naam isi se juda hai: Build, Ship, Fix. Build matlab code se artifact, Ship matlab usse safely production tak pahunchana, Fix matlab jab wo toote to jaldi pakadna aur theek karna.

### [08:45 – 11:20] Scene 4: Waterfall vs Agile vs DevOps
**[VISUAL: Three timelines: a long waterfall staircase, small agile sprints, and tiny rapid DevOps releases looping continuously.]**

**(Voiceover):**
Pehle software waterfall mein banta tha: requirement, design, code, test, release, har step ke baad agla, aur feedback saal bhar baad. Ye saal mein ek baar poore hotel ka renovation karne jaisa hai. Agile ne development ko chhote sprints mein baant diya, lekin release ab bhi ops ke paas atka rehta tha. DevOps ne wo aakhri deewar bhi hatayi: code likhte hi test, package aur release automatic. Result: din mein kai baar deploy, aur wo bhi kam darr ke saath, jaise hotel mein roz ek chhota sudhaar. Dhyaan rahe: speed ka matlab laaparwahi nahi, automation ke bharose tez chalna hai.

### [11:20 – 13:00] Scene 5: Lab aur Bridge
**[VISUAL: A notebook page titled "My last release" with three prompts: Who deployed? How long? What broke?]**

**(Voiceover):**
Lab: kisi bhi chhote project ko dimaag mein rakho, apna ya office ka. Teen sawaal likho: deploy kaun karta hai, kitna time lagta hai, aur pichli baar kya toota. Jo steps haath se hote hain, unke aage star lagao. Ye star hi aapki automation ki list hain. Agle episode mein hum us list ko CI/CD ke saath jodenge aur poore course ka map dekhenge.

---

# 📺 EPISODE 4: The Delivery Loop aur Aapka Roadmap

### [00:00 – 01:50] Scene 1: Haath se Deploy ka Dard
**[VISUAL: A person typing 12 commands on a server, copy-pasting from a text file, and one typo turns the screen red. Counter: "Manual steps: 12".]**

**(Voiceover):**
Soch ke dekho: har release ke liye barah commands, ek text file se copy karke. Ek jagah typo, aur raat ki neend gayi. Isi dard ko door karne ke liye CI/CD aaya. CI, Continuous Integration, matlab sabka code baar baar ek shared jagah milaya jaye aur har baar automatic build aur test chale. CD, Continuous Delivery ya Deployment, matlab jo pass ho gaya wo ready-to-release ho, ya seedha production tak chala jaye.

### [01:50 – 03:55] Scene 2: Ek Pipeline ki Shakal
**[VISUAL: The conveyor from head office to the hotels, now with stations: Commit → Build → Unit tests → Package (artifact) → Deploy to staging → Smoke test → Deploy to prod → Monitor. Green ticks run across; one station turns red and the conveyor stops.]**

**(Voiceover):**
Ek pipeline wahi conveyor hai jo Atithi ke head office ko hotels se jodta hai. Developer code commit karta hai, ye conveyor chalu ho jata hai: build, tests, package, staging par deploy, smoke test, aur phir production. Jahan bhi koi stage fail, conveyor ruk jata hai aur team ko turant pata chalta hai. Pipeline ke do fayde: speed, aur repeatability. Jo kaam aaj haath se aap karte ho, kal ek button se ya bina button ke, har baar ek jaisa hoga.

### [03:55 – 09:05] Scene 3: DevOps Tools ka Map
**[VISUAL: A map of Atithi Hotels at three zoom levels, joined by roads labelled "Internet". Level 1, inside one building: Linux, Bash, Python. Level 2, the rented campus: AWS/Azure/GCP, Terraform, Ansible. Level 3, head office: Git, Jenkins/GitHub Actions, Docker, Kubernetes, Prometheus/Grafana.]**

**(Voiceover):**
Ab course ka map, Atithi Hotels ke teen zoom levels mein. Pehla level: ek building ke andar. Staff, kamre, taale aur logbooks. Ye Linux hai, aur uske saath Bash aur Python. Doosra level: landlord se kiraye par liya poora campus. Kai buildings, gate, warehouse aur records office. Ye cloud hai, AWS, Azure aur GCP, aur is campus ko document se banane ke liye Terraform aur Ansible. Teesra level: head office. Yahan services ke design rakhe jaate hain, yaani Git. Ek automated workshop unhe tayaar karke bhejti hai, yaani CI/CD, Jenkins aur GitHub Actions. Har service ek sealed truck mein pack hoti hai jo kisi bhi building par ek jaisi chalti hai, yaani Docker containers, aur un trucks ko sambhalne ke liye Kubernetes. Aur ek control room sab par nazar rakhta hai, Prometheus aur Grafana. Teeno levels ko sadkein jodti hain, yaani internet. Ek rule yaad rakhna: is kahaani mein staff aur guest alag hain. Staff yaani server aur cloud ke users, jaise aap. Guest yaani website ka end user. Aur ek baat: tool badlte rehte hain, concept nahi. Isliye har session mein hum pehle do sawaal poochhenge: hum kis zoom level par hain, aur ye tool kis dard ko door karta hai.

### [09:05 – 11:10] Scene 4: AI ki Jagah aur DevOps Engineer ka Kaam
**[VISUAL: A DevOps engineer's day: reading an alert, checking logs, reviewing a pipeline diff, asking an AI assistant for a draft, verifying it with a stamp "Reviewed by human".]**

**(Voiceover):**
DevOps engineer ka din kya hota hai? Pipelines banana aur sudharna, infrastructure ko code mein sambhalna, alerts dekhna, incident aane par logs padhna aur fix nikalna, aur security aur cost par nazar. Atithi ki har team ke saath ek padha-likha assistant bhi baithta hai: AI. Wo tez draft de sakta hai, par wo aapke production ka context nahi jaanta. Isliye ye course aapko AI ke saath chalna sikhayega: draft assistant ka, jaanch aapki. Guest tak wahi pahunchta hai jo aapne khud jaancha ho.

### [11:10 – 12:55] Scene 5: Lab aur Next Session Bridge
**[VISUAL: A checklist: "Create GitHub account", "Install VS Code", "Install Git", "Pick a cloud (AWS free tier)", each ticking.]**

**(Voiceover):**
Aaj ka lab, setup. GitHub account banao, VS Code aur Git install karo, aur ek cloud free-tier ke liye taiyaar raho. Pehla assignment: apne last release ki list se ek haath wala step chuno jise aap automate karna chahte ho. Hum is course mein usse sach mein automate karenge. Agla session isi assistant ka hai: AI ko ek co-programmer ki tarah kaise use karna hai, bina uspar aandhi bharosa kiye.

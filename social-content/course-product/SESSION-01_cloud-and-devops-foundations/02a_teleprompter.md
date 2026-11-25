# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-01_cloud-and-devops-foundations

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,523 · **Episodes:** 4

---

# EPISODE 1: Cloud se pehle ki duniya

## Ek Hotel Company, Ek Server Room

Is poore course mein ek hi kahaani chalegi. Aap ek hotel company shuru kar rahe ho: Atithi Hotels. Atithi Devo Bhava, yaani guest sabse pehle. Hamare liye guest hai website ka end user. Ab purana tareeka socho: zameen kharido, building banao, generator lagao, guard rakho. Mahino lag gaye aur lakhon kharch ho gaye, tab jaakar pehla guest aaya. Software ki duniya mein bhi yahi hota tha. Maan lijiye aapne ek online kapde ki dukaan kholi. Ek server kharida, office ke ek kone mein rakha, aur kaam chal gaya. Phir sale ka din aaya. Achanak hazaar ki jagah pachas hazaar log website par aa gaye. Server ki CPU sau percent, website slow, phir band. Ab aap naya server order karte ho, aur wo aata hai teen hafte baad. Tab tak sale khatam. Yahi hai cloud se pehle ki duniya. Is session ka sawaal simple hai: jab tayaar building minutes mein kiraye par mil sakti hai, to hum purane tareeke se kyun fase the? Chaliye, shuru se samajhte hain.

## Physical Server aur Data Center ki Problems

Ek physical server sirf ek machine nahi hota. Jaise apni building ke saath zameen, generator, AC aur guard aate hain, waise hi server ke saath jagah chahiye, bijli, backup power, thanda rakhne ke liye cooling, network, security aur ek admin jo raat ko bhi alert sun sake. Ye sab upfront kharch hai, isse capital expenditure kehte hain. Aur sabse bada dard: aapko peak load ke hisaab se server kharidna padta tha, jabki saal ke zyadatar din machine aadhi khaali rehti thi. Ise kehte hain over-provisioning. Ulta, kam server liya to peak par fail. Dono taraf nuksaan.

## Virtualization aur Hypervisor

Pehli badi chaal thi virtualization. Socho ek bada tower hai jisme ek hi hotel chal raha hai, aur zyadatar floors khaali pade hain. Ek building engineer us tower ko kai alag, independent buildings mein baant deta hai. Har building ka apna darwaza, apna staff aur apna management. Technically, ek hardware ke upar hypervisor naam ka software baithta hai, wahi hamara building engineer hai. Wo CPU, RAM aur disk ko baant kar kai virtual machines banata hai. Har VM ko lagta hai ki wo akeli poori machine hai, apna operating system, apne apps. Isolation milta hai: ek VM crash ho to doosre chalte rehte hain. Aur hardware ka use badhta hai, kyunki ek server par kai kaam chalte hain. Is course mein jab bhi hum "building" bolenge, uska matlab hoga ek server ya ek VM.

## Ek Halka Raasta: Container ki Jhalak

Virtualization ke baad ek aur idea: container. VM ek poori alag building hai, apne management office ke saath, isliye bhaari hai aur shuru hone mein der lagti hai. Container ek truck hai, jo building ke management office ko hi saajha karti hai, isliye halki hai aur jaldi chalti hai. VM zyada alag-thalag, container zyada tez aur chhota. Aaj kal cloud mein dono saath chalte hain: building ke andar trucks. Poora kaam Session 21 mein hoga. Abhi ek line yaad rakho: VM building hai, container truck.

## Type-1 vs Type-2 aur Lab: Pehli VM

Hypervisor do tarah ke hote hain. Type-1 seedha hardware par chalta hai, jaise KVM ya VMware ESXi, aur data center mein yahi use hota hai. Type-2 aapke laptop ke OS ke upar app ki tarah chalta hai, jaise VirtualBox. Seekhne ke liye Type-2 kaafi hai. Aaj ka lab: VirtualBox install karo, ek naya VM banao, 2 GB RAM aur 20 GB disk do (Apple chip wale Mac par VirtualBox sirf ARM Linux chalata hai, to ARM wali ISO lo), aur dekho ki aapke laptop ke andar ek alag computer boot ho raha hai. Cloud mein jab aap ek server launch karte ho, peeche ye hi idea bade scale par chal raha hota hai.

## Recap aur Bridge

Recap: physical server mehenge aur dheere the, virtualization ne ek machine ko kai machines mein badla, jaise ek tower ko kai buildings mein. Lekin ab bhi tower aapka tha, aapke data center mein. Agar koi landlord bani banayi buildings kiraye par de de, aur wo bhi minutes mein? Wo hai cloud. Agle episode mein dekhenge ki cloud assal mein hai kya, aur ye IaaS, PaaS, SaaS ke teen shabd kya bolte hain. Ab tak ke teen shabd saath yaad rakhna: hypervisor, container aur region.

---

# EPISODE 2: Cloud kya hai?

## Zameen Kharido ya Building Kiraye par Lo?

Atithi Hotels ke saamne do raaste hain. Ya to apni zameen kharido, building banao, generator mein tel bharo, repair karao. Ya ek landlord se bani banayi building kiraye par lo, ghante ke hisaab se, aur kaam khatam ho to wapas kar do. Cloud computing doosra raasta hai. Teen bade landlord hain, AWS, Azure aur GCP, jinhone duniya ke bade shehron mein tayaar towers bana rakhe hain. Servers, storage, database, networking, sab internet par kiraye par, jitna use karo utna paisa. Zameen, bijli aur maintenance landlord ki. Na intezaar, na upfront kharch. Aur aaj ka sabse bada fayda: aap ek button se ek sau server bhi launch kar sakte ho aur kaam khatam hone par band bhi.

## Cloud ke Paanch Gun

Cloud ki pehchaan paanch baaton se hoti hai. Self-service: aap khud console ya API se resource maangte ho. Broad network access: internet se kahin se bhi. Resource pooling: provider ke bade pool se aapko hissa milta hai. Elasticity: load badhe to resource badhao, ghate to ghatao. Aur measured service: jitna use, utna bill. Hamari kahaani ka ek jaadui rule yahin se aata hai: is duniya mein saji sajayi building ki minutes mein photocopy ho sakti hai, aur use bina kharch giraya bhi ja sakta hai. Asli imaarat ke saath ye nahi hota, software ke saath hota hai, aur cloud ki poori taakat isi mein hai. Dhyaan rakhna, sirf "kisi aur ka server" ko cloud nahi kehte. Agar aap ticket daal kar teen din baad machine paate ho, to wo hosting hai, cloud nahi.

## IaaS, PaaS, SaaS: Khaali Building, Banquet Hall, Booked Room

Ise Atithi ke saamne khule raaston se samjho. Apni zameen par apni building: neev se lekar bedsheet tak sab aapka. Ye on-premises hai. IaaS mein landlord se ek khaali building kiraye par mili: deewarein, bijli aur paani landlord ke, par andar ka poora intezaam aapka. Jaise AWS EC2 ya Google Compute Engine: machine milti hai, OS aur app aap sambhalo. PaaS ek serviced banquet hall hai: hall, staff aur kitchen sab tayaar, aap sirf apna event lekar aao. Jaise Google App Engine, aap sirf code do. SaaS mein aap bas ek kamra book karte ho aur rehte ho: Gmail, Google Docs, aap sirf use karte ho. Jaise jaise upar jaate ho, control kam, aur dimaagi bojh bhi kam.

## Public, Private, Hybrid aur Shared Responsibility

Deployment ke teen model. Public cloud, jaise AWS, Azure, GCP, jahan landlord ke towers kai companies share karti hain. Private cloud, sirf ek company ke liye bana campus. Aur hybrid, yaani apna purana hotel aur kiraye ki buildings, dono ka mix. Ab ek zaroori baat: shared responsibility model. Landlord zimmedar hai zameen, imaarat aur bijli ka, yaani data center, hardware aur hypervisor ki security ka. Lekin building ke andar ke taale, kiske paas kaun si chaabi hai, aur darwaze ka guard, ye sab aapki zimmedari hai. Yaani aapka data, aapki permissions, aapka firewall, aapka password. Duniya ke zyadatar cloud leaks provider ki galti se nahi, galat configuration se hote hain. Isliye is course mein har cloud session ke saath security ki aadat banayenge.

## Landlord Kahan Hai: Region aur Availability Zone

Landlord ki buildings har jagah nahi hoti. Ek shehar ko region kehte hain, jaise Mumbai. Us shehar mein alag alag towers hoti hain, jinki bijli aur network alag hote hain: inhe Availability Zone kehte hain. Ek tower band ho jaaye, to doosri chalti rehti hain, isliye gambhir system kai towers mein chalta hai. Region chunne ke teen karan: guest kitna paas hai, kanoon aur data kahan rakhna allowed hai, aur kharch. Poora detail Session 8 mein.

## Lab aur Bridge

Homework lab: apne sabse paas ka region dhoondho, jaise AWS ki region list mein, aur likho ki us shehar mein kitni Availability Zones hain. Phir ek cloud account ke liye ready ho jao. Abhi account banana zaroori nahi, par sab providers ke free-tier rules padho aur ek baat note karo: billing alert pehle din lagana hai. Cloud mein "bhool gaya band karna" sabse mehnga sabak hota hai, kyunki kiraye ki building khaali padi ho tab bhi meter chalta rehta hai. Ab aapko pata hai ki cloud kya hai. Agla sawaal: jab building itni aasaani se milti hai, to dev aur ops ke beech jhagde kyun hote the? Episode 3 mein DevOps ki wo deewar girate hain.

---

# EPISODE 3: DevOps kya hai?

## "Mere Laptop Par To Chal Raha Tha"

Atithi Hotels mein do tarah ke log hain. Head office ke designers, jo naye services design karte hain. Aur hotel chalane wale operators, jinhe guest ke saamne sab kuch theek rakhna hai. Designer ne naya design deewar ke us paar phenk diya, aur hotel mein wo chala hi nahi. Software mein bilkul yahi purani kahaani hai. Developer ne feature banaya, apne laptop par chalaya, sab theek. Code ops team ko diya gaya. Production par wo chala hi nahi. Developer bola, mere laptop par to chal raha tha. Ops bola, hum to bas deploy karte hain, code galat hai. Dono sahi the, aur dono phase the. Kyunki dono ke goal alag the: developer ko naye features chahiye, ops ko stability. Naya release matlab risk, isliye ops release rokta tha. Deewar yahin se bani.

## DevOps ki Definition aur Culture

DevOps koi tool ya job title bhar nahi, ye kaam karne ka tareeka hai. Seedhi baat: dev aur ops ek hi team ki tarah poore lifecycle ki zimmedari lete hain, plan se lekar production monitoring tak. Atithi mein iska matlab hai: designers aur operators ek hi team, aur dono ke beech deewar ki jagah ek conveyor. Naya kaam us conveyor se seedha hotel tak pahunchta hai, aur guest ka feedback wapas head office aata hai. Isme culture pehle aata hai, tools baad mein. Chhote chhote releases baar baar, kyunki chhota change fail ho to dhoondhna aasaan. Automation, kyunki insaan thakta hai, script nahi. Measurement, kyunki bina naape sudhar nahi hota. Aur sharing, kyunki jo ek ko pata hai, poori team ko pata hona chahiye.

## DevOps Lifecycle ka Infinity Loop

DevOps ko ek infinity loop ki tarah dekho. Plan, code, build, test: ye hissa banane ka hai. Release, deploy, operate, monitor: ye hissa chalane ka hai. Aur monitor se jo seekh mili, yaani guest ka feedback, wo wapas plan mein jaati hai. Ye loop kabhi khatam nahi hota. Hamare course ka naam isi se juda hai: Build, Ship, Fix. Build matlab code se artifact, Ship matlab usse safely production tak pahunchana, Fix matlab jab wo toote to jaldi pakadna aur theek karna.

## DevOps Achha Chal Raha Hai? Paanch Number

DevOps achha chal raha hai ya nahi, ye andaze se nahi, kuch numbers se pata chalta hai. DORA ki research paanch number batati hai. Hum kitni baar release karte hain. Ek badlaav code se guest tak kitne samay mein pahunchta hai. Kitne release mein gadbad hoti hai. Gadbad ho to kitni jaldi theek hoti hai. Aur kitne release sirf production ki kisi problem ki wajah se bina plan ke karne pade, yaani rework. Pehle teen speed ke hain, aakhri do stability ke. Ek zaroori baat: speed aur stability dushman nahi, achhi teams dono mein achhi hoti hain. Aur ye number kisi insaan ko number dene ke liye nahi, system ki kamzori dhoondhne ke liye hain.

## Waterfall vs Agile vs DevOps

Pehle software waterfall mein banta tha: requirement, design, code, test, release, har step ke baad agla, aur feedback saal bhar baad. Ye saal mein ek baar poore hotel ka renovation karne jaisa hai. Agile ne development ko chhote sprints mein baant diya, lekin release ab bhi ops ke paas atka rehta tha. DevOps ne wo aakhri deewar bhi hatayi: code likhte hi test, package aur release automatic. Result: din mein kai baar deploy, aur wo bhi kam darr ke saath, jaise hotel mein roz ek chhota sudhaar. Dhyaan rahe: speed ka matlab laaparwahi nahi, automation ke bharose tez chalna hai.

## Lab aur Bridge

Lab: kisi bhi chhote project ko dimaag mein rakho, apna ya office ka. Teen sawaal likho: deploy kaun karta hai, kitna time lagta hai, aur pichli baar kya toota. Ek andaza bhi likho: kitni baar release hota hai, aur kitne release mein gadbad hui. Wahi aapke DORA ke pehle do number hain. Jo steps haath se hote hain, unke aage star lagao. Ye star hi aapki automation ki list hain. Agle episode mein hum us list ko CI/CD ke saath jodenge aur poore course ka map dekhenge.

---

# EPISODE 4: The Delivery Loop aur Aapka Roadmap

## Haath se Deploy ka Dard

Soch ke dekho: har release ke liye barah commands, ek text file se copy karke. Ek jagah typo, aur raat ki neend gayi. Isi dard ko door karne ke liye CI/CD aaya. CI, Continuous Integration, matlab sabka code baar baar ek shared jagah milaya jaye aur har baar automatic build aur test chale. CD, Continuous Delivery ya Deployment, matlab jo pass ho gaya wo ready-to-release ho, ya seedha production tak chala jaye.

## Ek Pipeline ki Shakal

Ek pipeline wahi conveyor hai jo Atithi ke head office ko hotels se jodta hai. Developer code commit karta hai, ye conveyor chalu ho jata hai: build, tests, package, staging par deploy, smoke test, aur phir production. Jahan bhi koi stage fail, conveyor ruk jata hai aur team ko turant pata chalta hai. Pipeline ke do fayde: speed, aur repeatability. Jo kaam aaj haath se aap karte ho, kal ek button se ya bina button ke, har baar ek jaisa hoga.

## DevOps Tools ka Map

Ab course ka map, Atithi Hotels ke teen zoom levels mein. Pehla level: ek building ke andar. Staff, kamre, taale aur logbooks. Ye Linux hai, aur uske saath Bash aur Python. Doosra level: landlord se kiraye par liya poora campus. Kai buildings, gate, warehouse aur records office. Ye cloud hai, AWS, Azure aur GCP, aur is campus ko document se banane ke liye Terraform aur Ansible. Teesra level: head office. Yahan services ke design rakhe jaate hain, yaani Git. Ek automated workshop unhe tayaar karke bhejti hai, yaani CI/CD, Jenkins aur GitHub Actions. Har service ek sealed truck mein pack hoti hai jo kisi bhi building par ek jaisi chalti hai, yaani Docker containers, aur un trucks ko sambhalne ke liye Kubernetes. Aur ek control room sab par nazar rakhta hai, Prometheus aur Grafana. Teeno levels ko sadkein jodti hain, yaani internet. Ek rule yaad rakhna: is kahaani mein staff aur guest alag hain. Staff yaani server aur cloud ke users, jaise aap. Guest yaani website ka end user. Aur ek baat: tool badlte rehte hain, concept nahi. Isliye har session mein hum pehle do sawaal poochhenge: hum kis zoom level par hain, aur ye tool kis dard ko door karta hai.

## AI ki Jagah aur DevOps Engineer ka Kaam

DevOps engineer ka din kya hota hai? Pipelines banana aur sudharna, infrastructure ko code mein sambhalna, alerts dekhna, incident aane par logs padhna aur fix nikalna, aur security aur cost par nazar. Atithi ki har team ke saath ek padha-likha assistant bhi baithta hai: AI. Wo tez draft de sakta hai, par wo aapke production ka context nahi jaanta. Isliye ye course aapko AI ke saath chalna sikhayega: draft assistant ka, jaanch aapki. Guest tak wahi pahunchta hai jo aapne khud jaancha ho.

## Lab aur Next Session Bridge

Aaj ka lab, setup. GitHub account banao, VS Code aur Git install karo, aur ek cloud free-tier ke liye taiyaar raho. Pehla assignment: apne last release ki list se ek haath wala step chuno jise aap automate karna chahte ho. Hum is course mein usse sach mein automate karenge. Agla session isi assistant ka hai: AI ko ek co-programmer ki tarah kaise use karna hai, bina uspar aandhi bharosa kiye. Ab tak ka safar yaad rakho: server, VM, cloud, DevOps, aur uske paanch number.

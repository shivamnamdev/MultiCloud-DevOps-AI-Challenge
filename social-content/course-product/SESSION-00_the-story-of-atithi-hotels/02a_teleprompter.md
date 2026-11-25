# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-00_the-story-of-atithi-hotels

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,857 · **Episodes:** 4

---

# EPISODE 1: Tutorial Trap aur Ek Guest ki Yatra

## Tutorials Dekhe, Phir Bhi Blank

Aapne mahino se DevOps ke tutorials dekhe hain. EC2 banana aata hai, Docker ka command yaad hai. Phir interview mein ek sawaal aata hai: "Production mein traffic sau guna badh gaya aur website slow hai. Aap sabse pehle kahan dekhoge?" Aur dimaag khaali. Problem aap mein nahi hai. Problem seekhne ke tareeke mein hai: aapne tools alag alag seekhe, par kisi ne ye nahi dikhaya ki wo sab ek saath kaise chalte hain. Ye session wahi poori tasveer dikhata hai, aur batata hai ki agle 33 sessions mein hum kahan se kahan jaayenge.

## Bees Tools ya Ek Kahaani?

DevOps seekhne mein sabse badi dikkat ye hai ki sab kuch alag alag tools ka dher lagta hai. Linux alag, AWS alag, Docker alag, Kubernetes alag. Yaad to ho jaate hain, par judte nahi. Isliye is course mein ek hi kahaani chalegi. Aap ek hotel company chala rahe ho: Atithi Hotels. Atithi Devo Bhava, yaani guest sabse pehle. Is kahaani mein do tarah ke log hain, aur inka fark hamesha yaad rakhna. Guest, yaani website ya app ka end user, jo bas aata hai, service leta hai aur chala jaata hai. Aur staff, yaani aap aur aapki team, jo servers aur cloud par kaam karte ho. Guest ko kabhi staff ka ID card nahi milta. Har tool is company ka ek hissa hai, aur har hissa ek dard ko door karta hai.

Aur is kahaani mein ek client bhi hai: Mrs. Mehta, Atithi Hotels ki owner. Wo techie nahi hain. Unka message aaya hai: "Hamari booking website ek purane computer par chalti hai. Sale wale din site baith jaati hai aur guests phone kaat dete hain. Mujhe bas ye chahiye. Sale wale din bhi site chalni chahiye. Koi booking kabhi gum na ho. Bill mere haath se bahar na jaye. Sirf meri team andar aaye, aur guest ka data safe rahe. Naya feature jaldi aaye, par site tootay nahi. Aur guest ko problem dikhne se pehle mujhe pata chal jaye." Ye chhe maangein, aur poora course inhi chhe ko poora karne ki yatra hai. Aap woh engineer ho jise Mrs. Mehta ne hire kiya hai.

## Yatra ke Aath Padaav

Ek guest phone par "Book Now" dabata hai, aur do second mein "Booking Confirmed" aa jaata hai. Wahi do second, dheere dheere. Ek: guest directory mein "Atithi Hotels" dhoondhta hai aur use pata milta hai. Ye DNS hai. Do: wo public sadkon aur chauraahon se guzarta hai. Ye internet hai, aur chauraahe routers hain. Teen: wo hamare campus ke main gate par pahunchta hai, yaani internet gateway. Chaar: gate par khada marshal use us building ki taraf bhejta hai jo khuli hai aur khaali hai. Ye load balancer hai. Paanch: building ke darwaze ka guard apni list dekhta hai aur use darwaza number 443 se andar aane deta hai. Guard security group hai, aur darwaze ka number port. Chhah: andar ek service truck use serve karta hai. Ye hamari application hai, ek container ke andar. Saat: truck private wing ke records office se uski booking nikalta hai, yaani database, aur warehouse se photos laata hai, yaani object storage. Aath: control room mein baithi team ye poori visit apni screens par dekhti hai. Ye monitoring hai. Ab wahi interview ka sawaal dobara suno: traffic sau guna, website slow, kahan dekhoge? Is naksha ke saath jawab aasaan hai: control room ki screens se shuru karo, phir marshal, phir buildings, phir trucks, phir records office. Aapko pata hai guest kahan kahan se guzarta hai, to aapko pata hai kahan dhoondhna hai.

## Vaada aur Shart

Ab saaf baat, pehle hi din. Is course ka vaada: 35 sessions aur ek optional bonus, GitOps, har session mein chaar episodes, aur har episode mein ek lab jo aap apne haath se karoge. Linux se shuru karke cloud, CI/CD, containers, Kubernetes, infrastructure as code aur AI tak. Aur ant mein ek capstone, jahan aap ye poori yatra khud banate ho. Aur aapki shart: sirf dekhna nahi. Hotel chalana kitaab padh kar nahi aata, hotel chala kar aata hai. Har lab karo, jo toote use theek karo, aur apna kaam GitHub par rakho, taaki aapke paas dikhane ke liye saboot ho, sirf certificate nahi. Main kisi package ya naukri ka vaada nahi karunga. Vaada sirf itna hai: jo ye sab karega, wo us interview ke sawaal par blank nahi hoga.

## Activity, Recap aur Bridge

Pehli activity: ek kaagaz lo aur aath dabbe banao, ek line mein. Har dabbe mein story word likho: directory, sadkein, main gate, marshal, guard, truck, records office aur warehouse, control room. Neeche jagah khaali chhodo. Jaise jaise course aage badhega, aap wahan asli tool ka naam, uska session number aur ek command likhoge. Course ke ant mein ye ek kaagaz aapka poora DevOps ka naksha hoga. Recap: ek guest, aath padaav, aur aap wo insaan jo har padaav banata hai. Ab ye sab kis kram mein seekhenge? Hum Atithi Hotels ko teen zoom levels par dekhenge. Pehla: ek building ke andar. Doosra: kiraye ka poora campus. Teesra: head office. Agle episode mein pehle do levels, yaani Linux aur cloud.

---

# EPISODE 2: Ek Building aur Kiraye ka Campus

## Zameen Kharidein ya Kiraye par Lein?

Atithi Hotels ko pehle ek building chahiye. Purana tareeka: zameen kharido, building banao, generator lagao, guard rakho, aur mahino baad pehla guest aaye. Ise on-premises kehte hain. Naya tareeka: teen bade landlord, AWS, Azure aur GCP, ne duniya ke bade shehron mein tayaar towers bana rakhe hain. Aap ghante ke hisaab se building kiraye par lete ho aur kaam khatam hone par wapas kar dete ho. Ye cloud hai. Aur is kahaani ka ek jaadui rule: yahan saji sajayi building ki minutes mein photocopy ho sakti hai. Asli imaarat ke saath ye nahi hota, software ke saath hota hai. Session 1 isi faisle par hai.

## Zoom Level 1: Ek Building ke Andar

Kiraye ki building khaali milti hai. Use chalane ke liye andar ek management system chahiye, aur wo Linux hai. Sessions 3 se 5, aur 5B jahan storage aur web server aate hain, isi building ke andar hain. Yahan ek instruction desk hai jahan aap apni baat kehte ho, yaani shell, aur ek management office jo bijli, paani aur lift sambhalta hai, yaani kernel. Building ka ek naksha hai jo main lobby se shuru hota hai, yaani filesystem. Phir aap staff rakhte ho: har ek ka ID card, ek general manager jiske paas master key hai, yaani root, aur har kamre par teen-ring taala, yaani permissions. Staff ek alag staff entrance se andar aata hai, yaani SSH. Aur phir manager ka roz ka round: kaun sa department chal raha hai, storeroom kitna bhara hai, logbooks mein kya likha hai. Jis din kuch toot-ta hai, usi round se aap wajah dhoondhte ho.

## Parchi aur Operations Officer

Roz wahi paanch instructions desk par bolna thakane wala hai. Session 6 mein aap unhe ek parchi par likh dete ho, shart aur dohraav ke saath, aur use timetable par laga dete ho. Ye Bash scripting aur cron hai. Par parchi ki bhi ek had hai. Session 7 mein ek trained operations officer aata hai, jo kai buildings par ek saath kaam kar sakta hai aur seedha landlord ke office ko phone laga sakta hai. Ye Python hai, aur wo phone line AWS ki library hai.

## Zoom Level 2: Kiraye ka Campus

Ab camera peeche hatao. Ek building se kaam nahi chalega, hamein poora campus chahiye. Sessions 8 se 15 landlord AWS ke saath hain. Pehle shehar aur tower chunte ho, yaani region aur availability zone, aur ek building kiraye par lete ho, yaani EC2. Phir landlord ke office mein tay hota hai ki aapki company mein kaun building kiraye par le sakta hai aur kaun gira sakta hai. Ye IAM hai, aur ye building ke andar ke staff se alag hai. Phir storerooms judte hain, ek model hotel ki photocopy banti hai, aur shaadi ke season mein extra buildings apne aap khulti aur band hoti hain. Main gate par marshal guests ko baant-ta hai. Ek kabhi na bharne wala warehouse hai, yaani S3. Ek records office hai jise landlord ke log chalate hain, yaani RDS. Aur phir poora campus design hota hai: sadak ki taraf wala wing, peeche ka private wing, main gate, aur do tarah ke guard. Ye VPC hai. Ant mein landlord ke meter, alarm, aur ek freelancer jo ghanti bajne par aata hai, kaam karta hai aur chala jaata hai.

## Activity aur Bridge

Activity: apni yatra sheet nikalo. Jo padaav campus ke hain unke upar "level 2" likho: main gate, marshal, guard, records office aur warehouse. Dekho, aath mein se chaar padaav sirf campus ke hain. Par ek sawaal baaki hai. Guest building dekhne nahi aata. Wo service lene aata hai: booking, khana, payment. Wo services kaun banata hai, aur wo har building tak kaise pahunchti hain? Iska jawab head office mein hai. Agle episode mein.

---

# EPISODE 3: Head Office: Design se Guest tak

## Gyarah Baje Badla, Gyarah Das par Har Hotel Mein

Subah gyarah baje head office mein ek designer ne ek service ka design badla. Gyarah bajkar das minute par wo badlaav har hotel mein chal raha tha. Kisi ne kuch uthaya nahi, kisi ne raat bhar jaag kar deploy nahi kiya. Ye kaise hua? Head office mein chaar cheezein hain jo ye karti hain, aur course ka sabse bada hissa, sessions 16 se 26, yahin hai.

## Vault aur Workshop

Pehli cheez: design. Hamari services ke design code hain. Har badlaav ek register mein tareekh aur dastakhat ke saath likha jaata hai, yaani Git. Naya idea ek alag draft par banta hai, yaani branch, aur chief architect ke review ke baad hi master mein judta hai, yaani pull request. Saare designs ek central vault mein rehte hain, yaani GitHub. Doosri cheez: workshop. Jaise hi vault mein naya revision aata hai, ek ghanti bajti hai aur workshop ka foreman ek conveyor chalu karta hai: banao, jaancho, pack karo, pahunchao. Foreman Jenkins hai, aur conveyor pipeline. Jaanch conveyor ke andar hi hoti hai: ek inspector design ko dekhta hai aur ek X-ray tayaar maal ko, taaki kharab cheez workshop se bahar hi na jaaye. Ye DevSecOps hai. Aur GitHub Actions wahi conveyor hai, bas seedha vault ke andar bana hua.

## Service Truck

Teesri cheez sabse mazedaar hai. Hamari har service ek sealed truck mein pack hoti hai. Ek food truck socho: uske andar uska apna saaman, apna stock, apni setting. Wo kisi bhi building ke aangan mein khada hota hai, building ki bijli aur paani se judta hai, aur har jagah bilkul ek jaisa chalta hai. Ye container hai. Dhyaan do: hamare truck mein apna generator aur apni paani ki tanki nahi hoti, isiliye wo halka hai aur seconds mein chalu ho jaata hai. Truck ka master design image hai, use banane ki fit-out sheet Dockerfile hai, aur jahan saare designs rakhe hain wo depot registry hai. "Mere laptop par to chal raha tha" wali purani ladai yahin khatam hoti hai, kyunki laptop par bhi wahi truck tha aur hotel mein bhi wahi.

## Operations Command aur Control Room

Jab trucks sau se zyada ho jaate hain, to unhe haath se sambhalna namumkin hai. Chauthi cheez: operations command, yaani Kubernetes. Aap use ye nahi bolte ki "building saat mein ek truck lagao". Aap ek standing order dete ho: "coffee ke paanch trucks hamesha chalte rehne chahiye". Command khud dekhta hai ki kis building ke aangan mein parking bay khaali hai. Ek truck kharab hua, to use theek nahi kiya jaata, depot se naya truck aa jaata hai. Queue badhi, to aur trucks khul jaate hain. Bahut saare chhote trucks, har ek ka ek hi kaam, milkar ek truck park banate hain: ye microservices hain. Aur in sab par nazar rakhne ke liye control room: ek inspector jo har meter padhta hai, ek alarm desk jo sahi duty manager ko phone karta hai, aur live screens ki ek deewar. Ye Prometheus aur Grafana hain.

## Activity aur Bridge

Activity: yatra sheet par padaav chhah aur aath ke upar "level 3" likho. Phir koi bhi app socho jo aap roz use karte ho, aur andaaza lagao ki uske peeche kaun se teen trucks ho sakte hain, jaise search, cart aur payment. Bas naam likho, sahi galat ki chinta mat karo. Ab ek aakhri sawaal: ye poora campus, itni buildings, gate, wings, kya hum har baar haath se kiraye par lenge? Nahi. Agle episode mein campus ek document se banta hai.

---

# EPISODE 4: Document se Campus, Naye Landlord, aur Aapka Day 0

## Naya Sheher, Das Minute

Atithi Hotels ek naye sheher mein khulna chahta hai. Purane tareeke se: console mein ek ek cheez par click, ghanton ka kaam, aur har baar thoda alag. Naye tareeke se: poore campus ka master plan ek document mein likha hai. Ye Terraform hai. Pehle aap poochhte ho "kya kya badlega, dikhao", phir contractor wahi banata hai jo likha hai, aur ek register mein darj hota hai ki asal mein kya bana. Das minute mein poora campus khada, har baar bilkul ek jaisa. Par Terraform sirf khaali buildings deta hai. Unhe andar se tayaar karne ke liye ek setup crew aata hai, checklist lekar. Wo staff entrance se andar jaata hai, har building ko ek jaisa set karta hai, aur chala jaata hai. Ye Ansible hai. Ab paanchon ko ek line mein yaad rakho: Terraform campus banata hai, Ansible buildings tayaar karta hai, Jenkins naye trucks pahunchata hai, Kubernetes unhe chalta rakhta hai, aur Prometheus sab par nazar rakhta hai.

## Doosra Landlord, Assistant aur Grand Opening

Is course ki do khaas baatein. Pehli: ek se zyada landlord. Session 30 mein Atithi ek doosre landlord ke saath bhi kaam shuru karta hai, Azure, aur labs mein Google Cloud bhi aata hai. Buildings wahi hain, bas naam alag, aur ek translation table se kaam chal jaata hai. Isiliye ise multi-cloud kehte hain: aap kisi ek landlord ko nahi, hotel chalana seekhte ho. Doosri: poore course mein aapke saath ek assistant baitha hai, AI. Wo bahut padha-likha aur bahut tez hai, par uska har kaam aap jaanchte ho. Session 2 mein aap use saaf brief dena seekhte ho. Session 32 mein ek truck har guest ke sawaal par ek baahar ke expert ko phone karta hai. Session 33 mein assistant control room mein raat ki duty leta hai, aur aap deewar mein ek service hatch lagate ho jisse wo hotel ke auzaar safely use kar sake. Wo hatch MCP server hai. Aur session 31 grand opening hai: ek designer design badalta hai, vault ki ghanti bajti hai, foreman banata aur jaanchta hai, ek naya truck depot se nikal kar bay mein lagta hai, aur ek guest serve hota hai. Uske baad ek optional bonus, 31B, jahan ek supervisor campus par rehkar sab theek rakhta hai: GitOps. Wahi aath padaav, par is baar sab kuch aapne banaya hai.

## Ye Course Kaise Chalega

Course ka tareeka seedha hai. Har session mein chaar episodes, aur har episode mein ek lab, kyunki DevOps dekh kar nahi, kar ke aata hai. Har session do sawaalon se shuru hoga: hum kis zoom level par hain, aur ye tool kis dard ko door karta hai. Aur ek imaandar baat: kahaani sirf ye batati hai ki tool kyun hai aur kahan baithta hai. Commands, YAML aur numbers hum seedhe asli roop mein seekhenge. Ek notebook rakho, pehle page par do column banao, "story word" aur "asli naam", aur aaj ke shabd likh daalo: guest, staff, building, landlord, campus, truck, conveyor, control room. Ye page har session ke saath badhega.

Aur ek cheez jo asli engineer ki tarah kaam karwayegi. Mrs. Mehta ki chhe maangein aapke saamne tickets ban kar aayengi. Har ticket mein pehle client ki maang, phir shartein, phir aapko kya deliver karna hai, aur ant mein "Done when": kuch checks, jo commands se pass hone chahiye. Aur har ticket ke baad ek handover note: aapne kya banaya, kaise pahunchenge, kitna kharcha, kaise undo karenge, aur abhi kya kami hai. Ye note hi aapko tutorial dekhne wale se kaam deliver karne wala engineer banata hai. Ek zaroori baat: ticket aur handover note mein story ke shabd nahi hote. Wahan seedhi technical bhasha hoti hai, kyunki client ko wahi chahiye.

## Task-002: Day 0 ka Setup

Session 1 se pehle aapka saaman tayaar hona chahiye. Ye Task-002 hai. Pehle landlords ke saath account kholo: Google Cloud ka free trial, jo naye account ko 90 din ke liye 300 dollar ka credit deta hai, aur AWS ka free tier. Free offers ke rules badalte rehte hain, isliye account banate waqt official page zaroor padh lo. Aur pehle hi din billing alert lagao, kyunki kiraye ki building khaali padi ho tab bhi meter chalta rehta hai. Phir vault aur depot ke account: GitHub, jahan aapka code rahega, aur Docker Hub, jahan aapke truck designs rahenge. Aur apne laptop par: VS Code, Git, ek SSH client, yaani Windows par MobaXterm ya built-in terminal, aur VS Code mein ek AI assistant. Abhi kuch launch nahi karna hai. Sirf account aur tools tayaar rakhne hain.

## Task-001, Recap aur Bridge

Aur ab Task-001: apna faisla public karo. LinkedIn par apne shabdon mein likho ki aap ye course aaj shuru kar rahe ho, kya kya seekhoge, aur kab tak khatam karoge. Jab aap sabke saamne bol dete ho, to beech mein chhodna mushkil ho jaata hai, aur aapka har lab us post ka agla saboot banta hai. Recap, poori kahaani ek saans mein. Ek guest, aath padaav. Teen zoom levels: ek building ke andar Linux, kiraye ka campus cloud, aur head office jahan design, conveyor, trucks, operations command aur control room hain. Campus document se banta hai, landlord badal sakte hain, aur ek assistant hamesha saath hai. Course ka naam yaad rakho: Build, Ship, Fix. Banao, pahunchao, aur toote to theek karo. Dono tasks poore karo, aur phir Atithi Hotels ka pehla faisla: zameen kharidein ya building kiraye par lein? Session 1 mein milte hain.

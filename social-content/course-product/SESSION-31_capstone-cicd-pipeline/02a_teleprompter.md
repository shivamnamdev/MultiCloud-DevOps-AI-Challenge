# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-31_capstone-cicd-pipeline

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,745 · **Episodes:** 4

---

# EPISODE 1: Grand Opening ka Plan

## Ab Tak Ke Tukde, Ab Poori Kahani

Ab tak Atithi Hotels ne alag alag cheezein seekhi: building ke andar Linux, campus mein AWS, head office mein vault, foreman aur trucks, aur control room. Aaj sab ek saath. Ek designer room ki ek line badalta hai, aur kuch minute baad wo badlaav ek asli building mein, ek asli truck mein, ek asli guest ko dikh raha hota hai. Beech mein koi haath se kuch nahi karta, aur agar kuch toota to guest tak pahunchne se pehle ruk jaata hai. Ye Build, Ship, Fix ki poori kahani hai. Is session ka ek naya niyam: naya kuch seekhna nahi, jo seekha hai wahi jodna hai.

## Guest ki Journey: Aathon Kadam

Story ke shuru mein humne guest ki journey ke aath kadam kaha tha. Guest directory mein hotel ka address dhoondhta hai, yaani DNS. Raaste aur junction par chalta hai. Campus ke main gate par pahunchta hai. Marshal use khuli building mein bhejta hai. Door guard list dekh kar door 443 se andar jaane deta hai. Ek truck use serve karti hai. Truck records office aur warehouse se baat karti hai. Aur control room ye poori visit apni screens par dekhta hai. Aaj hum ek truck banate hain, usse pahunchate hain, aur dekhte hain ki wo kadam chaar se aath tak sach mein kaam karti hai. Pehle teen kadam ke liye campus Session 14 ka hi rahega.

## Pehle Team ka Niyam, Phir Ghanti

Sabse pehli galti jo hum capstone mein rokte hain: seedha master par push. Session 16B ka master lock yaad hai. Isliye grand opening ka pehla kadam kod nahi, team ka niyam hai. Har badlaav ek draft branch par, jaise feature/room-count. Vault mein push, aur ek pull request. Chief architect, yaani reviewer, dekhta hai. Foreman ka required check, yaani test aur scan, sabz hona chahiye. Tabhi master mein merge. Aur sirf merge hone par ghanti bajegi, yaani webhook, aur truck baahar jayegi. Branch protection mein ye teen niyam rakho: review zaroori, check zaroori, seedha push band. Ek CODEOWNERS file mein likho ki Jenkinsfile aur deploy/ ka maalik kaun hai, taaki conveyor ke niyam bina us maalik ke review ke na badlein. Isse conveyor ki apni suraksha banti hai.

## Design ke Faisle aur Definition of Done

Ab faisle likh lo, kyunki jo likha nahi, wo beech mein badalta hai. Depot: GHCR ya ECR. Deploy target: ek app building, jahan Docker chal raha hai, kyunki hum simple rakhte hain. Edition label: Git SHA ke pehle saat akshar, taaki har truck se vault ka ek revision milaya ja sake. Secrets: key cabinet mein, kisi file mein nahi. Rollback: pichhla edition label. Aur Definition of Done: master mein merge se production tak sab automatic, test fail ho to truck design banta hi nahi, scan fail ho to depot mein nahi jaata, health check fail ho to purani truck wapas, aur har deploy ka record. Ye likhe hone se project ke beech mein bhatakna nahi padta, aur interview mein isse accha jawab nahi: "mera success criteria ye tha, aur ye maine kaise saabit kiya".

## Infra: Master Plan aur Setup Crew se

Infra ke do raaste hain. Seedha raasta: do chhote Ubuntu buildings, jenkins aur app, haath se. Bonus raasta: Session 27 aur 28 ka master plan buildings aur door guards banaye, aur Session 29 ki setup crew dono mein Docker lagaye, aur ek mein Java aur Jenkins. Jo bhi raasta lo, niyam wahi. Jenkins ka port 8080 sirf aapke IP se. App building par staff entrance, yaani port 22, sirf Jenkins building ke security group se. Aur guest ka door, jaise 8081, aapke IP se aaj ke test ke liye. Jenkins building se app building par bina password ke SSH key chalaao, aur wo private key Jenkins ke key cabinet mein SSH credential ke type se rakho, kisi file mein nahi. Session 17 ka jenkins user aur Session 4 ka key permission 600 yaad rakho.

## Lab: Repo, Rules aur Pehla Check

Is capstone ka ticket, ATITHI-031. Mrs. Mehta kehti hain: "Naya feature jaldi aaye, par site tootay nahi." Done when: review aur check ke bina kuch main mein merge na ho, merge hote hi tests chalein aur naya version app tak pahunche, aur ek jaan-boojh kar toota hua release apne aap wapas ho jaye. Lab: GitHub par atithi-rooms repo banao. Branch protection on karo: pull request zaroori, ek review, status checks zaroori, aur force push band. .gitignore mein __pycache__/, .venv/ aur .env. CODEOWNERS mein Jenkinsfile aur deploy/ ka maalik likho. Phir ek chhota test: ek branch banao, README mein ek line jodo, push karo, pull request kholo, aur dekho ki merge button tab tak band hai jab tak review aur check na ho. Abhi check koi nahi hai, to ye agle episodes mein aayega. Bas dekh lo ki master par seedha push sach mein rukta hai. Agar kisi ek account ko bypass milta hai, to uski wajah likho aur band karo.

## Recap aur Bridge

Recap: guest ki journey, team ka niyam, faisle aur infra. Ab service aur uska truck.

---

# EPISODE 2: Service aur Truck

## Pipeline ka Kaam, Service ka Nahi

Capstone mein service chhoti rakhenge, kyunki seekhne ki cheez pipeline hai. Hum Session 22 ki rooms-service lete hain: Flask ki ek app, jo room ki list deti hai, /health par zinda hone ka jawab deti hai, aur Session 26 ke baad /metrics bhi deti hai. Aap apni Node ya Java app se bhi yahi kar sakte ho: concept wahi.

## Service, Tests aur Health

Ek chhoti app:

Aur ek test:

Ek chhoti pytest.ini bhi rakho, [pytest] aur pythonpath = ., warna tests folder se from app import app nahi milta. pytest -q chalao. Conveyor ki sabse pehli suraksha yahi tests hain. /health halka rakho, aur database tak na jaao, taaki marshal aur deploy ka check database ki dikkat par poori fleet ko bimaar na dikhaye. /metrics Session 26 se aata hai, to wahi code yahan jod do, aur label mein route rakho, room ya guest ki ID nahi.

## Truck Design: Fit-out Sheet

Fit-out sheet wahi jo Session 22 mein banayi thi:

Ek hi baat ka dhyaan: requirements.txt pehle copy hota hai, taaki naya code aane par bhi libraries ki layer cache se aaye. Non-root user, gunicorn, 0.0.0.0, health check: sab Session 22 se. .dockerignore mein .git, .env aur .venv zaroor, warna secret truck design mein ghus sakta hai. Production ke liye base image ko version par pin karo.

## Pehle Local, Phir Pipeline

Ek purana niyam: jo laptop par nahi chalta, use conveyor par mat chalao. Pehle pytest. Phir docker build -t rooms:local ., docker run -d -p 8081:5000 rooms:local, aur curl localhost:8081/health, /rooms, /metrics. Jab teeno sahi, tab pull request. Aur ek aadat: pipeline mein jo bhi command hai, wo pehle haath se chal chuki ho. Isse jab conveyor laal hoti hai, to aap jaante ho ki galti conveyor mein hai, app mein nahi.

## Lab: Pehla Pull Request

Lab: ek branch banao, jaise feature/first-service. Upar ki saari files rakho. pytest -q, docker build, docker run, aur teen curl. Phir commit, push, aur pull request. Kisi doosre se, ya khud ek doosre account se, review karwao: kam se kam ek comment Dockerfile par, jaise "base image pin karo". Review ke baad merge. Ek aur laptop par, ya nayi folder mein, git clone karke docker build chalao, aur dekho ki bina aapke laptop ki kisi cheez ke wahi truck banta hai. Agar nahi banta, to koi file vault mein jaana bhool gayi, aur abhi pakadna sasta hai.

## Recap aur Bridge

Recap: service, tests, truck design aur pehla pull request. Ab foreman ki conveyor, jo ye sab khud chalaye.

---

# EPISODE 3: Foreman ki Conveyor

## Merge Karo, Baaki Machine Karegi

Ab wo kaam jo aap haath se karte ho, test, truck design banana, jaanchna, depot mein bhejna, foreman ko do. Hum ek Jenkinsfile likhenge jo test se depot tak jaaye. Pull request par sirf test aur scan chalega, kyunki unse merge ka faisla hota hai. Master par merge ke baad truck design bhi depot mein jaayegi. Deploy agle episode mein.

## Jenkinsfile

Jenkinsfile:

Edition label Git SHA ke pehle saat akshar: depot mein jo truck dikhe, vault mein uska exact revision mile. when { branch 'main' } sirf multibranch project mein chalta hai, jo Session 19 mein dekha. Aur Push station ke andar hi credentials khulte hain, poori conveyor mein nahi.

## Gate: Jo Kharab Hai Wo Aage Nahi Jaata

Conveyor ka asli kaam rokna hai. Test fail hua to aage ke station skip, truck design banegi hi nahi. Trivy ne HIGH ya CRITICAL kamzori dekhi to scan laal, aur truck design depot tak nahi pahunchti. Kamzori aksar aapke code mein nahi, kisi aur ke base image ya library mein hoti hai. Hamare test mein python:3.12-slim par pehli hi baar mein 48 HIGH ya CRITICAL mile, jinme se sirf ek ka fix aaya tha. Isliye scan mein --ignore-unfixed lagta hai, jo wo kamzori chhodta hai jiska abhi koi fix nahi, aur Dockerfile ki apt-get upgrade wali line wo fix le leti hai jo aa chuka hai. Pehli baar Trivy apna database utarta hai, jisme ek-do minute lagte hain. Phir kya karna hai: base image update, ya library upgrade, ya jaanboojh kar ek chhoti ignore list, jiske saath likha ho ki kyun. Pull request par jo check dikhte hain, wahi master lock ke required checks hain. Ek sabz nishan ka matlab hai ki foreman ne jaancha, aur tabhi chief architect merge ka button dabaata hai. Aur agar scan ya build mein bahut samay lagta hai, to Docker layer cache aur pip cache workbench par rakho.

## Key Cabinet aur Ghanti

Do cheezein key cabinet mein: ghcr ka username aur token, jise sirf packages likhne ki ijaazat ho, aur app-server-key, wahi SSH key. Dono aise scope mein ki sirf is project ki conveyor unhe dekh sake. Multibranch project mein GitHub ko source banao. Repo mein webhook lagao, jo Jenkins ke /github-webhook/ par jaata hai. GitHub ki delivery page par ek hara nishan dekho: yehi ghanti hai. Agar ghanti nahi baj rahi, to usually teen kaaran: Jenkins tak raasta nahi (security group ya URL), webhook mein galat URL, ya Jenkins mein GitHub plugin ka setting. Ek periodic scan bhi rakho, taaki koi chhooti hui ghanti pakdi jaye. Fork wale pull request ke liye trust setting wahi: Everyone nahi.

## Teen Jaan-boojh ke Hadse

Ab teen jaan-boojh ke hadse, kyunki conveyor ka bharosa tab banta hai jab aapne use todkar dekha ho. Pehla: ek test tod do, to Test laal. Doosra: Dockerfile mein ek purana base image rakho jisme kamzori ho, to Scan laal. Teesra: depot ka token galat kar do, to Push laal. Har laal station ke log mein dhoondho ki kaaran kahan likha hai. Ye wahi debugging hai jo asli team har hafte karti hai. Ek aur: pull request par Push station chalta hi nahi, kyunki wo sirf master ke liye hai. Ye bhi jaanch lo.

## Lab: Conveyor Chalao

Lab: Jenkinsfile ko ek pull request mein jodo. Multibranch project banao, webhook lagao, ghcr credential rakho. Pull request par Test aur Scan chalte dekho, aur Push ko skip hote. Branch protection mein Jenkins ke check ko required banao. Phir merge karo, aur master par Push chalte dekho. GHCR ke packages ke page par SHA wala edition label dikhega. Teen hadse dobara karo, ek ek karke, aur har baar wapas theek karo. Agar workbench par Docker ya Trivy nahi hai, to Session 18 aur 22 ka install wapis dekho. Trivy ka install official guide se, version apna dekh lo. Pehli baar do branch ek saath scan karein to Trivy ka database ek hi jagah utarta hai aur ek scan crash ho sakta hai: bas dobara chalao.

## Recap aur Bridge

Recap: CI poora ho gaya. Ab CD: truck ko building mein pahunchao, jaancho, aur zaroorat ho to wapas lo.

---

# EPISODE 4: Pahunchao, Jaancho, Wapas Lo

## Deploy Mein Sabse Zyada Galti

Deploy wo kadam hai jahan sabse zyada galtiyan hoti hain. Nayi truck chalu ki, kisi ne check nahi kiya, aur bees minute tak guests ko error dikha. Isliye deploy ke baad health check zaroori hai, jaise naya menu pehle test kitchen mein chakha jaata hai, aur dono, check aur rollback, automatic hone chahiye. Insaan raat ko teen baje se behtar script hai, jo har baar wahi kare.

## Deploy Script

App building par ek chhoti script, deploy/deploy.sh:

Pehle purani truck ka label yaad rakhta hai. Naya design pull karta hai. Truck chalata hai. Bees baar, har teen second par, health check. Pass to log mein ek line, fail to purani truck wapas aur script exit 1, jisse Jenkins ka station laal ho. Humne ise ek local registry aur ek toote hue release ke saath aazmaya: pehli deploy, upgrade aur rollback teeno sahi chale, aur log mein teeno line aayi. App building par ek baar depot ka docker login karo, warna pull par no basic auth credentials aayega. Ek chhoti baat: rollback ke turant baad purani truck ko khud health check mein aane mein kuch second lagte hain, isliye rollback ke baad bhi ek baar health dekho. Ek sachchai: isme kuch second ke liye service ruk jaati hai. Kai buildings ke saath rolling ya blue-green se ye bacha jaata hai, jo Kubernetes ka kaam hai. Ek building ke liye ye saaf aur seekhne layak hai.

## Pehle Staging, Phir Manjoori, Phir Production

Asli setup mein pehle staging par deploy, phir ek chhota smoke test, jaise /rooms ka jawab. Uske baad manjoori ka station, input, jisme "Production par bhejna hai?" poocha jaata hai. Session 19 ki baat: input ke samay workbench rok kar mat rakho, yaani agent none aur ek timeout. Manjoori sirf duty manager ke group se, aur har manjoori ka naam record mein. Deploy stage mein SSH sshagent(['app-server-key']) se, aur script ko ssh ubuntu@APP_IP 'bash -s' -- "IMAGE:TAG" < deploy/deploy.sh ki tarah chalao, taaki script alag se copy na karni pade. Agar staging aur production alag buildings hain, to bas IP ka farq hai. Wahi checklist, wahi script.

## Deploy ke Baad Control Room

Deploy khatam hone ka matlab kaam khatam nahi. Control room dekho. Session 26 ka inspector app building ke /metrics ko padhta hai. Wall of screens par request rate, errors aur latency. Deploy ke samay ek line lagao, jis par edition label likha ho, taaki graph par dikhe ki kab version badla. Agar errors us line ke baad badhe, to pehla shak naye release par. Ek alarm bhi rakho: errors ek percent se zyada paanch minute tak. Ye script ke health check se alag hai: health check batata hai ki truck zinda hai, aur control room batata hai ki guests ko theek serve ho rahi hai. Dono chahiye.

## Jab Rollback bhi Kam Pad Jaye

Rollback ke teen star hain. Pehla: jaise purana menu wapas, script khud purani truck wapas laati hai, kuch second mein. Doosra: koi release baad mein kharab nikla, to Jenkins se ek purane edition label ko dobara deploy karo. Teesra: kharab badlaav ko vault se bhi hatao, git revert se naya pull request, taaki register imaandar rahe, jaisa Session 16B mein dekha. Ek chetavani: truck wapas laana aasaan hai, par agar naye release ne database mein kuch badal diya, to purani truck us database ke saath nahi chal sakti. Isliye database ke badlaav chhote aur peeche ki taraf mel khate hon, pehle database, phir truck, aur kabhi ek saath bada badlaav nahi.

## Lab: Poora Safar aur Toota Hua Release

Lab: Jenkinsfile mein Deploy station jodo, jisme sshagent(['app-server-key']) ho. Pehle ek chhota badlaav: /rooms mein ek naya room type jodo, pull request, review, merge. Kuch minute mein curl http://APP_IP:8081/rooms mein naya data. Ab ek toota hua release: app ke shuru mein jaan-boojh kar ek exception daalo, jisse wo start par crash ho. Pull request par test shayad pass ho jaaye, aur isiliye pehle ye bhi dekho ki kaun sa check is hadse ko nahi pakadta: ek test jodo jo app ko import karke dekhe. Phir bhi, agar release chhoot gaya, to Deploy station health check par laal hoga, script purani truck wapas laayegi, site chalti rahegi, aur /var/log/atithi-deploys.log mein FAILED aur rollback ka record rahega. Wahi Fix wala hissa.

## Safai aur Post-Incident Review

Pehle handover note likho: kya banaya, kaise chalta hai, status kahan dikhta hai, kitna kharcha, undo kaise karte hain, aur known gaps. Yahan gaps ye hain: practice depot ki jagah asli registry ka push alag se jaanchna hai, aur deploy ek hi app server par hota hai. Safai ka checklist: dono buildings band ya delete, depot token revoke, SSH key key cabinet se hatao, test images delete, aur console mein dekho ki koi volume, public IP ya security group baaki to nahi. Aur ek chhota post-incident review likho, bina kisi par ilzaam ke: kya hua, kis check ne pakda, kis ne nahi pakda, aur ek badlaav jo agli baar rokega. Ye likhna asli teams ki aadat hai, aur interview mein bhi kaam aati hai. Aur ab pichhe mudo: master lock, bell, foreman, truck, depot, health check, rollback, control room. Atithi ka pehla grand opening poora.

## Recap aur Bridge

Recap: aapne code se production tak ek poori, surakshit conveyor banayi, aur use jaan-boojh kar todkar dekha. Ab Atithi ke head office mein ek naya sadasya aata hai: ek bahut padha-likha assistant. Pehle wo ek bahari expert ki tarah phone par jawab dega, jo har guest ke sawaal par kaam aaye. Phir ek trained brain ki tarah, jo apni truck mein chalta hai, aur kisi bhi truck ki tarah naya version pahunchaya jaata hai. Agla session: AI apps aur model serving.

# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-22_dockerfile-and-registries

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,685 · **Episodes:** 4

---

# EPISODE 1: Fit-out Sheet

## Dusron ki Truck Nahi, Apni

Pichhle session mein humne dusron ke truck designs chalaye: nginx, postgres. Ab Atithi ki apni rooms-service ko truck mein pack karna hai. Uske liye ek fit-out sheet chahiye, yaani Dockerfile: ek text file jisme likha hota hai ki design kaise banega, kis base se shuru, kya kya andar jaayega, aur truck chalu hote hi kya chalega. Ye wahi nuskha hai jo kisi bhi machine par, kisi bhi building ke courtyard mein, ek jaisi truck deta hai. Aur wo bhi blueprint ka hissa hai: vault mein, pull request ke saath.

## Zaroori Instructions

FROM batata hai kis base design se shuru karna hai, jaise python:3.12-slim. WORKDIR andar ka kaam ka folder. COPY building ki files design mein. RUN build ke waqt command chalata hai, jaise pip install. ENV environment variable jo truck mein bhi rehta hai, aur ARG sirf build ke waqt. EXPOSE sirf dastavez hai ki app kaun sa port sunti hai, wo port khud nahi kholta. USER batata hai kaun chalayega. HEALTHCHECK ek chhoti jaanch hai jo Docker baar baar chalata hai. CMD truck chalu hote hi default command. ENTRYPOINT ek tay command, jisme CMD uske arguments ban sakte hain. Dono ko hamesha exec form mein likho, ["python","app.py"], taaki signal sahi pahunche.

## Pehli Dockerfile

Ek chhoti Flask service ki Dockerfile:

docker build -t rooms:1.0 . design banata hai, aur docker run -d -p 5000:5000 rooms:1.0 truck chalata hai. Ek dhyaan ki baat: app ko host="0.0.0.0" par sunna hoga. Agar wo 127.0.0.1 par sunegi, to sirf truck ke andar se dikhegi, aur serving window kaam nahi karega. Ye Session 14 ke private aur public wing wali baat ka chhota roop hai: kisi cheez ko kahan sunna hai, wo uske address par nirbhar hai.

## CMD vs ENTRYPOINT aur Dev Server

CMD aur ENTRYPOINT ka farq ek misaal se. CMD ["python","app.py"] default hai: docker run rooms:1.0 sh likhoge to ye replace ho jaayega. ENTRYPOINT ["python"] aur CMD ["app.py"] likhoge to docker run rooms:1.0 other.py sirf argument badlega. Ek aur zaroori sudhaar: python app.py Flask ka development server chalata hai, aur Flask khud likhta hai ki production ke liye nahi. Asli service ke liye gunicorn jaisa server: CMD ["gunicorn","-b","0.0.0.0:5000","-w","2","app:app"], aur requirements.txt mein gunicorn. Wahi Session 5B ke Apache wali baat: web server ek alag, taiyaar cheez hai, jo guests ki bheed sambhalta hai, designer ka test server nahi.

## Health Check

Truck chal rahi hai, par kya wo jawab de rahi hai? Process zinda ho aur app atki ho, ye ho sakta hai. Isliye HEALTHCHECK: ek chhoti command jo Docker har kuch second par chalata hai. App par ek /health route rakho jo sirf 200 de, aur Dockerfile mein HEALTHCHECK --interval=30s --timeout=3s CMD python -c "..." || exit 1. docker ps mein status healthy ya unhealthy dikhta hai. Ye Session 11 ke marshal ke health check ka truck ke andar ka roop hai, jaise housekeeping ka "room ready" status. Yahi baat aage Kubernetes mein probes ban jaati hai. Dhyaan: health check halka ho, database tak na jaaye, nahi to database ki dikkat par saari trucks unhealthy dikhengi.

## Lab: Apni Service ko Truck Karo

Is session ka ticket, ATITHI-022. Mrs. Mehta kehti hain: "Naya feature jaldi aaye, par site tootay nahi." Done when: rooms service ek container image ban jaye jo /health par jawab de, non-root user se chale, chhota ho, aur version ke tag ke saath registry mein jaye. Lab. app.py:

requirements.txt mein flask aur gunicorn. Dockerfile mein CMD gunicorn wala rakho, aur build karo. docker run -d -p 5000:5000 --name rooms rooms:1.0, phir curl localhost:5000/health. Mac par port 5000 aksar AirPlay ke paas hota hai, to -p 5050:5000 aur curl localhost:5050/health chalao. Ab gunicorn ka bind 127.0.0.1:5000 kar do, dobara build karo, aur dekho ki bahar se jawab nahi aata. docker ps mein health status dekho: wo phir bhi healthy dikhega, kyunki jaanch truck ke andar se hoti hai, bahar ke raaste ko nahi dekhti. Ye bahut aam galti hai, aur ise samajhna networking ka ek zaroori sabak hai.

## Recap aur Bridge

Recap: Dockerfile ke instructions, CMD aur ENTRYPOINT, aur production server. Ab ek sawaal: har baar build karne par itna samay kyun lagta hai?

---

# EPISODE 2: Build ki Speed

## Ek Line Badli, Poora Build Dobara

Designer ne sirf ek line code badli, aur Docker ne phir se saare packages install kar diye. Teen minute. Din mein bees baar. Ye fit-out sheet ke order ki galti hai. Layers ka cache samajh gaye, to build second mein ho sakta hai. Aur wahi samay Session 20 ki conveyor ke minutes bhi bachata hai, kyunki conveyor har push par ye build chalati hai. Seedha hisaab: tees push, har ek teen minute, yaani roz dedh ghanta.

## Cache ka Niyam

Niyam: har instruction ek layer banata hai, aur agar instruction aur uski input files nahi badli, to Docker cache se uthata hai. Par ek layer badli to uske baad ki saari layers dobara banti hain. Isliye jo cheez kam badalti hai, jaise dependencies, use pehle rakho, aur jo roz badalti hai, jaise aapka code, baad mein. Pehle sirf requirements.txt copy karo aur pip install, aur phir COPY . .. Ab code badalne par install wali layer CACHED rahegi. Isi tarah RUN apt-get update && apt-get install -y ... ek hi RUN mein likho, aur baad mein rm -rf /var/lib/apt/lists/*, taaki purani package list cache mein na atke.

## Build Context aur .dockerignore

docker build . ka dot build context hai, yaani wo folder jo Docker ko bheja jaata hai. Agar usme .git, bade datasets ya node_modules ho, to wo sab daemon ko jaata hai aur build dheema hota hai. .dockerignore mein inhe likho: .git, __pycache__, .env, *.md, tests/ agar zaroorat nahi. Aur ek bahut zaroori baat: .env aur chaabi ki files kabhi design mein na jaayein. Layer mein ek baar gaya hua secret baad mein delete karne par bhi design ki history mein reh sakta hai, aur depot se koi bhi pull karke padh sakta hai. Isliye .dockerignore mein .env, aur build ke time par secret chahiye to BuildKit ka --mount=type=secret.

## Secret Build ke Time

Kabhi build mein hi ek secret chahiye hota hai, jaise private package index ka token. ARG TOKEN ya ENV TOKEN kabhi nahi, kyunki wo docker history mein dikh jaata hai. Sahi tareeka BuildKit ka secret mount: Dockerfile mein RUN --mount=type=secret,id=pipcred pip install -r requirements.txt, aur build karte waqt docker build --secret id=pipcred,src=pip.conf .. Secret sirf us ek step ke liye ek file ki tarah dikhta hai, aur kisi layer mein nahi jaata. Conveyor mein wahi secret key cabinet ya Actions ke secrets se aata hai, Session 19 aur 20 ke niyamon ke saath. Aur final check: docker history rooms:1.0 aur Trivy ke secret scan se dekho ki kuch leak to nahi.

## Lab: Build Time Naapo

Lab. Sahi order wali Dockerfile ko time docker build -t rooms:cache . se build karo. Phir app.py mein ek line badlo aur dobara build karo: install step par CACHED likha aayega aur build second mein khatam. Ab Dockerfile mein COPY . . ko install se pehle rakh do, aur wahi karo: install dobara chalega. Dono ka samay note karo. Sirf flask aur gunicorn ke saath farq chhota hai, humne teen second aur aadha second naape. numpy aur pandas jod do, to barah second aur aadhe second se bhi kam. Phir .dockerignore banao, usme .git, __pycache__ aur .env likho, aur build ke context size ka farq dekho. Aakhir mein docker history rooms:cache padho aur dekho ki koi secret ya password to nahi dikh raha. Agle episode mein hum design ka size ghataenge.

## Recap aur Bridge

Recap: cache, ignore aur secrets ka dhyaan. Ab design ko chhota aur surakshit banate hain.

---

# EPISODE 3: Chhota aur Surakshit Design

## Hello World, 1.6 GB

Ek chhoti si service ka design, aur size 1.6 GB? Humne python:3.12 ka poora design naapa to itna nikla, jabki slim sirf lagbhag 200 MB ka tha. Ye dheema download, zyada disk, aur zyada packages, yaani hamle ke zyada raaste hain. Har extra package ek aur jagah hai jahan se koi kamzori aa sakti hai, aur Session 20 ka X-ray, Trivy, utna hi zyada finding dikhata hai. Chhota design tez, sasta aur surakshit hota hai. Teen tareeke: chhota base, multi-stage build, aur non-root user. Aur ek chauthi cheez: design mein sirf wahi jaaye jo truck chalane ke liye chahiye, workshop ka saaman nahi.

## Multi-stage: Workshop Peeche, Sirf Truck Aage

Multi-stage build mein pehle stage workshop hai: saare build tools, compilers aur dependencies. Doosre stage mein sirf truck: wo cheezein jo chalane ke liye chahiye. COPY --from=build se sirf built files, jaise Python wheels ya ek compiled binary, saath aati hain. Compiler aur tools final design mein jaate hi nahi. Isse design chhota aur attack surface kam. Ek sachchai: agar aapki Python service ko compiler ki zaroorat nahi, jaise sirf Flask aur gunicorn, to slim base par multi-stage se size lagbhag wahi rehta hai, humne naapa to dono design 227 aur 228 MB ke the. Multi-stage ka asli fayda tab dikhta hai jab build ko gcc ya headers chahiye, ya Java aur Go mein, jahan akeli binary ya jar aati hai. Java ke liye bhi wahi: pehle stage mein Maven aur JDK, doosre mein sirf JRE aur .jar, jo Session 17 ke finished unit ko seedha truck mein daalta hai. Go jaisi languages mein ek akeli binary se aur bhi chhota design milta hai.

## Non-root aur Base ka Chunav

Truck ko by default root se chalana khatarnak hai. RUN useradd -m -u 10001 app aur USER app se non-root par chalao, taaki agar service hack ho, to nuksaan kam ho. Session 4 ke service user ka wahi sabak: ek kaam, kam ijaazat. Base ka chunav: slim aksar sahi balance hai. Alpine bahut chhota hai, par musl ki wajah se kabhi kabhi Python packages mein dikkat. Distroless mein shell tak nahi, jo security ke liye achha par debugging ke liye mushkil. Base ko ek tay version par pin karo, jaise python:3.12.7-slim, ya digest se, aur use niyam se update karo, Dependabot ya Renovate se, taaki naye security patches milte rahein.

## Mac par Banao, Server par Chalao: Architecture

Ek jaal jo Mac ya ARM laptop wale ko zaroor milta hai. Design usi CPU ke liye banta hai jis par build hua. M-series Mac par build kiya to arm64 design. Use Intel ya AMD wali EC2 building par chalao, to "exec format error". Hal: --platform linux/amd64 ke saath build karo, par Mac par ye Docker Desktop ke emulation par tika hai. Humare lab mein wo band tha aur build khud "exec format error" par gira, to emulation chalu karo ya amd64 runner par build karo. Ya docker buildx build --platform linux/amd64,linux/arm64, jo ek hi naam mein dono ke design rakhta hai. Isse Session 10 ke t4g jaise Graviton, yaani ARM, buildings par bhi wahi design chal sakta hai, jo aksar sasti hoti hain. Aur CI mein jo runner hai, wahi architecture banata hai, to wahan ke build par bharosa zyada hota hai.

## Truck ko Aur Kasna: Read-only aur Kam Ijaazat

Design ko non-root banane ke baad ek aur parat chalte waqt lagti hai. --read-only truck ki file system ko read-only kar deta hai, aur jahan likhna zaroori ho, jaise /tmp, wahan --tmpfs /tmp. Isse koi hamlavar andar aakar kuch likh nahi paata. --cap-drop ALL Linux ki khaas ijaazatein, yaani capabilities, saari hata deta hai, aur jo chahiye wahi --cap-add se wapas. --security-opt no-new-privileges ye rokta hai ki koi process aur zyada ijaazat le le. --memory aur --pids-limit se ek bigdi truck poori building ko nahi khaa sakti. Ek jaal: naye gunicorn mein aisa bhi hota hai ki read-only file system par wo apne home folder mein ek control file likhne ki koshish karta hai, aur log mein Read-only file system ka error dikhta hai, jabki service chalti rehti hai. Isko ya to is feature ko band karke, ya ek aur --tmpfs lagakar sambhalte hain, aur apne gunicorn version ke docs dekh lo. Ye Session 4 ke least privilege ka truck wala roop hai, aur Kubernetes mein wahi baatein security context ban jaati hain.

## Lab: Multi-stage aur Non-root

Lab:

Build karo, docker images mein size dekho, aur docker run --rm rooms:slim id se check karo ki user root nahi hai. Agar Trivy install hai, to trivy image rooms:slim chalao aur pehle wale design se findings ki ginti milao. Ek aur test: truck ke andar touch /etc/x karo aur dekho ki permission denied aata hai. Aur ek baat: rm -rf /wheels se size nahi ghatta, kyunki wheels COPY ki layer mein pehle hi ja chuki hain.

## Recap aur Bridge

Recap: multi-stage, non-root, base ka chunav aur architecture ka jaal. Ab design ko label lagana aur depot mein rakhna.

---

# EPISODE 4: Edition Label, Depot aur CI se Push

## Production Mein Kaun Sa Edition?

Production mein rooms:latest chal raha hai, aur ek bug aaya. Ab kaun sa code chal raha hai? Koi nahi jaanta, kyunki latest badalta rehta hai. Rollback bhi mushkil: pichhla edition kaun sa tha? Achhi labelling se aap kisi bhi truck ko ek commit tak wapas jod sakte ho, aur rollback ek command ka kaam ban jaata hai. Ye wahi Session 16B ki release ki mohar, yaani Git tag, ki kahani hai, bas ab usse truck design ka label banana hai.

## Edition Label ki Strategy

Teen label saath chalte hain. Semantic version, jaise 1.4.2, jo logon ke liye. Git commit ka SHA, jaise sha-a1b2c3d, jo exact code se jodta hai. Aur digest, sha256:..., jo content ki asli pehchaan hai. Rule: Git tag v1.4.2 lagate hi conveyor wahi design 1.4.2 aur sha-a1b2c3d ke naam se depot mein rakhe. Isse vault ki release ki mohar aur depot ka edition label ek hi kahani kehte hain. Deploy hamesha version, SHA ya digest se, latest se kabhi nahi. Naam ka format hai registry/namespace/name:tag, jaise ghcr.io/atithi/rooms-service:1.4.2.

## Depot aur Login

Depot designs ka ghar hai. Docker Hub public aur private dono, GHCR vault ke saath, ECR AWS ke liye, Artifact Registry GCP ke liye, ACR Azure ke liye. Flow: docker login, docker tag rooms:1.0 REGISTRY/rooms:1.0, docker push REGISTRY/rooms:1.0. Login ke liye password nahi, token ya cloud ka role. ECR mein: aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com, aur wo token building ke duty badge se aata hai, jaise Session 9 mein. Private depot mein extras bhi hote hain: push par scan, tags ko immutable banana, aur purane designs ke liye lifecycle rule, jaise Session 12 ke godown mein.

## Purane Designs ka Kachra

Har push ek naya edition rakhta hai, aur depot mein purane designs ka dher lag jaata hai. Chaar sau editions, har ek saath MB ka, aur har mahine storage ka bill. ECR mein lifecycle policy likho: "pichhle bees tagged editions rakho, aur untagged ko saat din baad hatao." Dhyaan: jo edition production mein chal raha hai, ya jis par rollback ho sakta hai, wo kabhi na hate. Isliye release ke labels, jaise 1.4.2, ko alag niyam do. Aur depot mein scanning on rakho, taaki purana design bhi tab pakda jaaye jab uski nayi kamzori mile, Session 20 ke raat wale scan ki tarah.

## Design par Mohar aur Saaman ki Soochi

Depot mein design jaane se pehle teen cheezein sochne ki hain. Ek, X-ray: Trivy ki report, aur gate ki wahi niyam jo Session 20 mein tay hue, yaani fixable HIGH aur CRITICAL par fail. Do, SBOM: design ke andar ke har package ki ek soochi, yaani parts list. Kal koi nayi kamzori aaye, to aap seedhe dekh sakte ho ki kaun si trucks mein wo package hai. Teen, mohar: signing tool, jaise cosign, se design par ek digital hastakshar, taaki deploy karne wala check kar sake ki ye design sach mein hamari conveyor se aaya hai, kisi aur ne depot mein chupke se badla nahi. Ye teeno aaj ek lab nahi, par ek achhi aadat ki disha hain, aur bade teams mein ye zaroori hote hain.

## Lab: Actions se Build aur Push

Lab. Vault mein Actions ki ek workflow:

Push karo, aur Packages mein image dikhegi. Ek Git tag v1.0.0 lagao aur dekho ki wahi design 1.0.0 aur sha- wale label ke saath aata hai. Dhyaan: bina tags ke metadata action v1.0.0 aur latest deta hai, isliye humne tags aur flavor khud likhe. Action versions ke liye docs dekh lena, aur Session 20 ki tarah unhe pin karo. Aakhir mein koi bhi doosri building docker pull karke wahi truck chala sakti hai. Ab handover note likho: kaunsa image aur kaunsa tag, kahan se pull hoga, size kitna hai aur kaunsa user chalata hai, undo kaise karte hain, aur known gaps. Yahan gaps ye hain: image signed nahi hai, aur koi gate nahi jo bina scan ke release ko roke.

## Recap aur Bridge

Recap: Docker ka poora safar: design likhna, chhota aur surakshit banana, label lagana aur depot mein bhejna. Aur ek sawaal jo ab bada ho gaya hai: sau trucks, das buildings. Koi gir jaaye to kaun use dobara chalayega? Naya edition kaun ek ek karke badlega, bina guests ko roke? Isi kaam ke liye head office ka operations command aata hai: Kubernetes. Agle session se.

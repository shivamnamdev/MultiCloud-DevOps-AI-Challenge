# ✍️ 02: SCRIPT — SESSION-22: Dockerfile and Registries
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S22`
- **Focus:** Dockerfile instructions, `CMD` vs `ENTRYPOINT`, exec form, binding to `0.0.0.0`, a production server instead of the Flask dev server, `HEALTHCHECK`, build context and `.dockerignore`, layer order and the cache, secrets that must not enter layers, multi-stage builds, non-root user, base image choices and pinning, CPU architecture (arm64 vs amd64), tags, digests and Git tags, registries (GHCR, ECR), pushing from CI, scanning, lifecycle of old images
- **Builds on:** Session 06 and 07 (scripts, Python), Session 09 (roles for ECR), Session 12 (lifecycle rules), Session 16B (tags as release stamps), Session 17 to 20 (conveyor, Actions, Trivy), Session 21 (images, layers, run, volumes)
- **Story position:** Zoom level 3, head office. Ab Atithi apni rooms-service ka truck design khud likhta hai: ek fit-out sheet, jis order mein cheezein lagti hain wahi design ki speed tay karta hai, sirf finished truck bhejte hain, workshop nahi, aur har edition par ek label lagta hai.
- **Story words used:** truck (container), truck design (image), fit-out sheet (Dockerfile), edition label (tag), depot (registry), workshop (build tools), release stamp (Git tag), X-ray (Trivy), conveyor (CI), duty badge (role), serving window (port), guest (end user)
- **Lab project:** Atithi's `rooms-service` (Flask): first design, a fast cached design, a small non-root multi-stage design, and the conveyor pushing it to a depot with a label tied to the Git release stamp.
- **Cost rule (AWS):** a private registry (ECR) charges for storage and data transfer, and CI runners have limits. Delete lab repositories and old images at the end. Do not leave images with secrets in any registry.
- **Episodes:**
  - Episode 1: Fit-out Sheet: Dockerfile ka Nuskha
  - Episode 2: Build ki Speed: Layer Order, Cache aur .dockerignore
  - Episode 3: Chhota aur Surakshit Design: Multi-stage, Non-root
  - Episode 4: Edition Label, Depot aur CI se Push

---

# 📺 EPISODE 1: Fit-out Sheet

### [00:00 – 02:15] Scene 1: Dusron ki Truck Nahi, Apni
**[VISUAL: A small Flask app folder on a desk, a speech bubble "how do I run this anywhere?". A fit-out sheet slides in, and a truck rolls out of it with the rooms-service painted on its side.]**

**(Voiceover):**
Pichhle session mein humne dusron ke truck designs chalaye: nginx, postgres. Ab Atithi ki apni rooms-service ko truck mein pack karna hai. Uske liye ek fit-out sheet chahiye, yaani Dockerfile: ek text file jisme likha hota hai ki design kaise banega, kis base se shuru, kya kya andar jaayega, aur truck chalu hote hi kya chalega. Ye wahi nuskha hai jo kisi bhi machine par, kisi bhi building ke courtyard mein, ek jaisi truck deta hai. Aur wo bhi blueprint ka hissa hai: vault mein, pull request ke saath.

### [02:15 – 05:00] Scene 2: Zaroori Instructions
**[VISUAL: A Dockerfile with each instruction highlighted: FROM, WORKDIR, COPY, RUN, ENV, ARG, EXPOSE, USER, HEALTHCHECK, CMD, ENTRYPOINT. Side labels: "when building" for FROM, COPY, RUN, ARG; "when running" for CMD, ENTRYPOINT, ENV.]**

**(Voiceover):**
`FROM` batata hai kis base design se shuru karna hai, jaise `python:3.12-slim`. `WORKDIR` andar ka kaam ka folder. `COPY` building ki files design mein. `RUN` build ke waqt command chalata hai, jaise `pip install`. `ENV` environment variable jo truck mein bhi rehta hai, aur `ARG` sirf build ke waqt. `EXPOSE` sirf dastavez hai ki app kaun sa port sunti hai, wo port khud nahi kholta. `USER` batata hai kaun chalayega. `HEALTHCHECK` ek chhoti jaanch hai jo Docker baar baar chalata hai. `CMD` truck chalu hote hi default command. `ENTRYPOINT` ek tay command, jisme CMD uske arguments ban sakte hain. Dono ko hamesha exec form mein likho, `["python","app.py"]`, taaki signal sahi pahunche.

### [05:00 – 07:30] Scene 3: Pehli Dockerfile
**[VISUAL: The Dockerfile on screen and a build log. `docker build -t rooms:1.0 .` then `docker run -d -p 5000:5000 rooms:1.0`. A highlighted line: `app.run(host="0.0.0.0")`.]**

**(Voiceover):**
Ek chhoti Flask service ki Dockerfile:
```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```
`docker build -t rooms:1.0 .` design banata hai, aur `docker run -d -p 5000:5000 rooms:1.0` truck chalata hai. Ek dhyaan ki baat: app ko `host="0.0.0.0"` par sunna hoga. Agar wo `127.0.0.1` par sunegi, to sirf truck ke andar se dikhegi, aur serving window kaam nahi karega. Ye Session 14 ke private aur public wing wali baat ka chhota roop hai: kisi cheez ko kahan sunna hai, wo uske address par nirbhar hai.

### [07:30 – 09:55] Scene 4: CMD vs ENTRYPOINT aur Dev Server
**[VISUAL: Left: `CMD ["python","app.py"]` with the Flask development server warning. Right: `CMD ["gunicorn","-b","0.0.0.0:5000","-w","2","app:app"]`. A table: CMD is replaced by arguments to `docker run`; ENTRYPOINT stays and CMD becomes its arguments.]**

**(Voiceover):**
CMD aur ENTRYPOINT ka farq ek misaal se. `CMD ["python","app.py"]` default hai: `docker run rooms:1.0 sh` likhoge to ye replace ho jaayega. `ENTRYPOINT ["python"]` aur `CMD ["app.py"]` likhoge to `docker run rooms:1.0 other.py` sirf argument badlega. Ek aur zaroori sudhaar: `python app.py` Flask ka development server chalata hai, aur Flask khud likhta hai ki production ke liye nahi. Asli service ke liye gunicorn jaisa server: `CMD ["gunicorn","-b","0.0.0.0:5000","-w","2","app:app"]`, aur `requirements.txt` mein `gunicorn`. Wahi Session 5B ke Apache wali baat: web server ek alag, taiyaar cheez hai, jo guests ki bheed sambhalta hai, designer ka test server nahi.

### [09:55 – 12:40] Scene 5: Health Check
**[VISUAL: A Dockerfile line `HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1`. `docker ps` shows `(healthy)` and later `(unhealthy)`. A mention of the marshal's health check.]**

**(Voiceover):**
Truck chal rahi hai, par kya wo jawab de rahi hai? Process zinda ho aur app atki ho, ye ho sakta hai. Isliye `HEALTHCHECK`: ek chhoti command jo Docker har kuch second par chalata hai. App par ek `/health` route rakho jo sirf 200 de, aur Dockerfile mein `HEALTHCHECK --interval=30s --timeout=3s CMD python -c "..." || exit 1`. `docker ps` mein status healthy ya unhealthy dikhta hai. Ye Session 11 ke marshal ke health check ka truck ke andar ka roop hai. Yahi baat aage Kubernetes mein probes ban jaati hai. Dhyaan: health check halka ho, database tak na jaaye, nahi to database ki dikkat par saari trucks unhealthy dikhengi.

### [12:40 – 14:55] Scene 6: Lab: Apni Service ko Truck Karo
**[VISUAL: `app.py` with `/` and `/health` routes. `requirements.txt` with `flask` and `gunicorn`. Build, run, `curl localhost:5000/health`. Then the same with `127.0.0.1` binding failing from outside.]**

**(Voiceover):**
Lab. `app.py`:
```python
from flask import Flask
app = Flask(__name__)

@app.get("/")
def home():
    return "Atithi rooms-service"

@app.get("/health")
def health():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```
`requirements.txt` mein `flask` aur `gunicorn`. Dockerfile mein CMD gunicorn wala rakho, aur build karo. `docker run -d -p 5000:5000 --name rooms rooms:1.0`, phir `curl localhost:5000/health`. Ab gunicorn ka bind `127.0.0.1:5000` kar do, dobara build karo, aur dekho ki bahar se jawab nahi aata. `docker ps` mein health status dekho. Ye bahut aam galti hai, aur ise samajhna networking ka ek zaroori sabak hai.

### [14:55 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "FROM · WORKDIR · COPY · RUN · ENV/ARG · USER · HEALTHCHECK · CMD / ENTRYPOINT in exec form · bind 0.0.0.0 · gunicorn, not the dev server".]**

**(Voiceover):**
Recap: Dockerfile ke instructions, CMD aur ENTRYPOINT, aur production server. Ab ek sawaal: har baar build karne par itna samay kyun lagta hai?

---

# 📺 EPISODE 2: Build ki Speed

### [00:00 – 02:05] Scene 1: Ek Line Badli, Poora Build Dobara
**[VISUAL: A designer changes one line of code. The build log shows `pip install` running again for three minutes. A clock and a sigh.]**

**(Voiceover):**
Designer ne sirf ek line code badli, aur Docker ne phir se saare packages install kar diye. Teen minute. Din mein bees baar. Ye fit-out sheet ke order ki galti hai. Layers ka cache samajh gaye, to build second mein ho sakta hai. Aur wahi samay Session 20 ki conveyor ke minutes bhi bachata hai, kyunki conveyor har push par ye build chalati hai. Seedha hisaab: tees push, har ek teen minute, yaani roz dedh ghanta.

### [02:05 – 05:00] Scene 2: Cache ka Niyam
**[VISUAL: Two fit-out sheets. Bad: `COPY . .` then `RUN pip install`, every step re-run after a code change. Good: `COPY requirements.txt .`, `RUN pip install`, then `COPY . .`, with `CACHED` on the install step. An arrow: "once a layer changes, every layer after it rebuilds".]**

**(Voiceover):**
Niyam: har instruction ek layer banata hai, aur agar instruction aur uski input files nahi badli, to Docker cache se uthata hai. Par ek layer badli to uske baad ki saari layers dobara banti hain. Isliye jo cheez kam badalti hai, jaise dependencies, use pehle rakho, aur jo roz badalti hai, jaise aapka code, baad mein. Pehle sirf `requirements.txt` copy karo aur `pip install`, aur phir `COPY . .`. Ab code badalne par install wali layer CACHED rahegi. Isi tarah `RUN apt-get update && apt-get install -y ...` ek hi `RUN` mein likho, aur baad mein `rm -rf /var/lib/apt/lists/*`, taaki purani package list cache mein na atke.

### [05:00 – 08:00] Scene 3: Build Context aur .dockerignore
**[VISUAL: A project folder with `.git`, `node_modules`, `.env`, `__pycache__`, `data/`. A `.dockerignore` listing them. A build log line: "transferring context: 1.2GB" shrinking to "12KB".]**

**(Voiceover):**
`docker build .` ka dot build context hai, yaani wo folder jo Docker ko bheja jaata hai. Agar usme `.git`, bade datasets ya `node_modules` ho, to wo sab daemon ko jaata hai aur build dheema hota hai. `.dockerignore` mein inhe likho: `.git`, `__pycache__`, `.env`, `*.md`, `tests/` agar zaroorat nahi. Aur ek bahut zaroori baat: `.env` aur chaabi ki files kabhi design mein na jaayein. Layer mein ek baar gaya hua secret baad mein delete karne par bhi design ki history mein reh sakta hai, aur depot se koi bhi pull karke padh sakta hai. Isliye `.dockerignore` mein `.env`, aur build ke time par secret chahiye to BuildKit ka `--mount=type=secret`.

### [08:00 – 11:05] Scene 4: Secret Build ke Time
**[VISUAL: A Dockerfile line `RUN --mount=type=secret,id=pipcred pip install ...` with `docker build --secret id=pipcred,src=pip.conf .`. Next to it, a red `ARG TOKEN` line with `docker history` revealing the value.]**

**(Voiceover):**
Kabhi build mein hi ek secret chahiye hota hai, jaise private package index ka token. `ARG TOKEN` ya `ENV TOKEN` kabhi nahi, kyunki wo `docker history` mein dikh jaata hai. Sahi tareeka BuildKit ka secret mount: Dockerfile mein `RUN --mount=type=secret,id=pipcred pip install -r requirements.txt`, aur build karte waqt `docker build --secret id=pipcred,src=pip.conf .`. Secret sirf us ek step ke liye ek file ki tarah dikhta hai, aur kisi layer mein nahi jaata. Conveyor mein wahi secret key cabinet ya Actions ke secrets se aata hai, Session 19 aur 20 ke niyamon ke saath. Aur final check: `docker history rooms:1.0` aur Trivy ke secret scan se dekho ki kuch leak to nahi.

### [11:05 – 13:50] Scene 5: Lab: Build Time Naapo
**[VISUAL: `time docker build -t rooms:cache .` cold, then a one-line change to `app.py` and a second build with CACHED lines, and then the reordered bad Dockerfile rebuilding the install. A `.dockerignore` and the context size before and after.]**

**(Voiceover):**
Lab. Sahi order wali Dockerfile ko `time docker build -t rooms:cache .` se build karo. Phir `app.py` mein ek line badlo aur dobara build karo: install step par CACHED likha aayega aur build second mein khatam. Ab Dockerfile mein `COPY . .` ko install se pehle rakh do, aur wahi karo: install dobara chalega. Dono ka samay note karo. Phir `.dockerignore` banao, usme `.git`, `__pycache__` aur `.env` likho, aur build ke context size ka farq dekho. Aakhir mein `docker history rooms:cache` padho aur dekho ki koi secret ya password to nahi dikh raha. Agle episode mein hum design ka size ghataenge.

### [13:50 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "deps first, code last · one RUN for apt · .dockerignore · no secrets in layers · BuildKit secret mount · docker history is public".]**

**(Voiceover):**
Recap: cache, ignore aur secrets ka dhyaan. Ab design ko chhota aur surakshit banate hain.

---

# 📺 EPISODE 3: Chhota aur Surakshit Design

### [00:00 – 02:05] Scene 1: Hello World, 1.6 GB
**[VISUAL: A bar chart of image sizes: `python:3.12` about 1.6 GB, `slim` about 200 MB, a Python service with the compiler left behind a little smaller or the same, and a Go or Java binary-only design under 100 MB. Next to it, a count of known vulnerabilities shrinking from hundreds to a handful.]**

**(Voiceover):**
Ek chhoti si service ka design, aur size 1.6 GB? Humne `python:3.12` ka poora design naapa to itna nikla, jabki `slim` sirf lagbhag 200 MB ka tha. Ye dheema download, zyada disk, aur zyada packages, yaani hamle ke zyada raaste hain. Har extra package ek aur jagah hai jahan se koi kamzori aa sakti hai, aur Session 20 ka X-ray, Trivy, utna hi zyada finding dikhata hai. Chhota design tez, sasta aur surakshit hota hai. Teen tareeke: chhota base, multi-stage build, aur non-root user. Aur ek chauthi cheez: design mein sirf wahi jaaye jo truck chalane ke liye chahiye, workshop ka saaman nahi.

### [02:05 – 04:30] Scene 2: Multi-stage: Workshop Peeche, Sirf Truck Aage
**[VISUAL: A fit-out sheet with two stages. Stage 1 "workshop": compilers and build tools build wheels or a binary. Stage 2 "truck": a slim base, `COPY --from=build`. A size bar: with a compiler needed, large before and smaller after; for pure Python, nearly unchanged. The workshop stage is discarded.]**

**(Voiceover):**
Multi-stage build mein pehle stage workshop hai: saare build tools, compilers aur dependencies. Doosre stage mein sirf truck: wo cheezein jo chalane ke liye chahiye. `COPY --from=build` se sirf built files, jaise Python wheels ya ek compiled binary, saath aati hain. Compiler aur tools final design mein jaate hi nahi. Isse design chhota aur attack surface kam. Ek sachchai: agar aapki Python service ko compiler ki zaroorat nahi, jaise sirf Flask aur gunicorn, to `slim` base par multi-stage se size lagbhag wahi rehta hai, humne naapa to 205 MB ke aaspaas. Multi-stage ka asli fayda tab dikhta hai jab build ko gcc ya headers chahiye, ya Java aur Go mein, jahan akeli binary ya jar aati hai. Java ke liye bhi wahi: pehle stage mein Maven aur JDK, doosre mein sirf JRE aur `.jar`, jo Session 17 ke finished unit ko seedha truck mein daalta hai. Go jaisi languages mein ek akeli binary se aur bhi chhota design milta hai.

### [04:30 – 07:10] Scene 3: Non-root aur Base ka Chunav
**[VISUAL: `RUN useradd -m -u 10001 app` and `USER app`. A comparison table of bases: full, slim, alpine, distroless. Notes: "alpine uses musl, some Python wheels fail", "distroless has no shell, debugging is harder", "pin the version or digest".]**

**(Voiceover):**
Truck ko by default root se chalana khatarnak hai. `RUN useradd -m -u 10001 app` aur `USER app` se non-root par chalao, taaki agar service hack ho, to nuksaan kam ho. Session 4 ke service user ka wahi sabak: ek kaam, kam ijaazat. Base ka chunav: slim aksar sahi balance hai. Alpine bahut chhota hai, par musl ki wajah se kabhi kabhi Python packages mein dikkat. Distroless mein shell tak nahi, jo security ke liye achha par debugging ke liye mushkil. Base ko ek tay version par pin karo, jaise `python:3.12.7-slim`, ya digest se, aur use niyam se update karo, Dependabot ya Renovate se, taaki naye security patches milte rahein.

### [07:10 – 09:45] Scene 4: Mac par Banao, Server par Chalao: Architecture
**[VISUAL: A laptop with an M-series chip building `rooms:1.0` and a cloud building running Intel or AMD. A message on the server: "exec format error". A fix: `docker build --platform linux/amd64 .` and `docker buildx build --platform linux/amd64,linux/arm64 ...`.]**

**(Voiceover):**
Ek jaal jo Mac ya ARM laptop wale ko zaroor milta hai. Design usi CPU ke liye banta hai jis par build hua. M-series Mac par build kiya to arm64 design. Use Intel ya AMD wali EC2 building par chalao, to "exec format error". Hal: `--platform linux/amd64` ke saath build karo, ya `docker buildx build --platform linux/amd64,linux/arm64`, jo ek hi naam mein dono ke design rakhta hai. Isse Session 10 ke `t4g` jaise Graviton, yaani ARM, buildings par bhi wahi design chal sakta hai, jo aksar sasti hoti hain. Aur CI mein jo runner hai, wahi architecture banata hai, to wahan ke build par bharosa zyada hota hai.

### [09:45 – 12:20] Scene 5: Truck ko Aur Kasna: Read-only aur Kam Ijaazat
**[VISUAL: A command `docker run -d --read-only --tmpfs /tmp --cap-drop ALL --security-opt no-new-privileges --memory 256m --pids-limit 100 rooms:slim`. A truck with most doors locked and one labelled `/tmp`. A list of what each flag blocks.]**

**(Voiceover):**
Design ko non-root banane ke baad ek aur parat chalte waqt lagti hai. `--read-only` truck ki file system ko read-only kar deta hai, aur jahan likhna zaroori ho, jaise `/tmp`, wahan `--tmpfs /tmp`. Isse koi hamlavar andar aakar kuch likh nahi paata. `--cap-drop ALL` Linux ki khaas ijaazatein, yaani capabilities, saari hata deta hai, aur jo chahiye wahi `--cap-add` se wapas. `--security-opt no-new-privileges` ye rokta hai ki koi process aur zyada ijaazat le le. `--memory` aur `--pids-limit` se ek bigdi truck poori building ko nahi khaa sakti. Ek jaal: naye gunicorn mein aisa bhi hota hai ki read-only file system par wo apne home folder mein ek control file likhne ki koshish karta hai, aur log mein `Read-only file system` ka error dikhta hai, jabki service chalti rehti hai. Isko ya to is feature ko band karke, ya ek aur `--tmpfs` lagakar sambhalte hain, aur apne gunicorn version ke docs dekh lo. Ye Session 4 ke least privilege ka truck wala roop hai, aur Kubernetes mein wahi baatein security context ban jaati hain.

### [12:20 – 15:05] Scene 6: Lab: Multi-stage aur Non-root
**[VISUAL: The multi-stage Dockerfile on screen. `docker images` showing two sizes. `docker run --rm rooms:slim id` printing `uid=10001(app)`. `trivy image rooms:slim` count compared with the single-stage design.]**

**(Voiceover):**
Lab:
```dockerfile
FROM python:3.12-slim AS build
WORKDIR /w
COPY requirements.txt .
RUN pip wheel --no-cache-dir -w /wheels -r requirements.txt

FROM python:3.12-slim
RUN useradd -m -u 10001 app
WORKDIR /app
COPY --from=build /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/* && rm -rf /wheels
COPY --chown=app:app . .
USER app
EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app:app"]
```
Build karo, `docker images` mein size dekho, aur `docker run --rm rooms:slim id` se check karo ki user root nahi hai. Agar Trivy install hai, to `trivy image rooms:slim` chalao aur pehle wale design se findings ki ginti milao. Ek aur test: truck ke andar `touch /etc/x` karo aur dekho ki permission denied aata hai.

### [15:05 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "multi-stage: workshop stays behind · non-root user · slim base, pinned · Graviton and Intel need the right platform · scan with the X-ray".]**

**(Voiceover):**
Recap: multi-stage, non-root, base ka chunav aur architecture ka jaal. Ab design ko label lagana aur depot mein rakhna.

---

# 📺 EPISODE 4: Edition Label, Depot aur CI se Push

### [00:00 – 01:50] Scene 1: Production Mein Kaun Sa Edition?
**[VISUAL: A production building runs `rooms:latest`. A bug appears and nobody knows which commit it came from. Next frame: `rooms:1.4.2-a1b2c3d`, traceable to a commit and a release stamp.]**

**(Voiceover):**
Production mein `rooms:latest` chal raha hai, aur ek bug aaya. Ab kaun sa code chal raha hai? Koi nahi jaanta, kyunki `latest` badalta rehta hai. Rollback bhi mushkil: pichhla edition kaun sa tha? Achhi labelling se aap kisi bhi truck ko ek commit tak wapas jod sakte ho, aur rollback ek command ka kaam ban jaata hai. Ye wahi Session 16B ki release ki mohar, yaani Git tag, ki kahani hai, bas ab usse truck design ka label banana hai.

### [01:50 – 03:45] Scene 2: Edition Label ki Strategy
**[VISUAL: Tag examples on one design: `1.4.2` (semantic version), `a1b2c3d` (commit SHA), `main` (branch), and an immutable digest `sha256:...`. A flow: Git tag `v1.4.2` in the vault → conveyor → image tags `1.4.2` and `1.4.2-a1b2c3d`.]**

**(Voiceover):**
Teen label saath chalte hain. Semantic version, jaise `1.4.2`, jo logon ke liye. Git commit ka SHA, jaise `a1b2c3d`, jo exact code se jodta hai. Aur digest, `sha256:...`, jo content ki asli pehchaan hai. Rule: Git tag `v1.4.2` lagate hi conveyor wahi design `1.4.2` aur `1.4.2-a1b2c3d` ke naam se depot mein rakhe. Isse vault ki release ki mohar aur depot ka edition label ek hi kahani kehte hain. Deploy hamesha version, SHA ya digest se, `latest` se kabhi nahi. Naam ka format hai `registry/namespace/name:tag`, jaise `ghcr.io/atithi/rooms-service:1.4.2`.

### [03:45 – 06:00] Scene 3: Depot aur Login
**[VISUAL: Registries: Docker Hub, GHCR, AWS ECR, Google Artifact Registry, Azure ACR. A flow: `docker login`, `docker tag rooms:1.0 REGISTRY/rooms:1.0`, `docker push`, `docker pull`. For ECR: `aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com`.]**

**(Voiceover):**
Depot designs ka ghar hai. Docker Hub public aur private dono, GHCR vault ke saath, ECR AWS ke liye, Artifact Registry GCP ke liye, ACR Azure ke liye. Flow: `docker login`, `docker tag rooms:1.0 REGISTRY/rooms:1.0`, `docker push REGISTRY/rooms:1.0`. Login ke liye password nahi, token ya cloud ka role. ECR mein: `aws ecr get-login-password | docker login --username AWS --password-stdin ACCOUNT.dkr.ecr.REGION.amazonaws.com`, aur wo token building ke duty badge se aata hai, jaise Session 9 mein. Private depot mein extras bhi hote hain: push par scan, tags ko immutable banana, aur purane designs ke liye lifecycle rule, jaise Session 12 ke godown mein.

### [06:00 – 08:20] Scene 4: Purane Designs ka Kachra
**[VISUAL: A depot shelf with 400 old editions, each 60 MB, and a storage bill. A lifecycle rule: "keep the last 20 tagged editions, delete untagged after 7 days". An "untagged" list of orphaned layers.]**

**(Voiceover):**
Har push ek naya edition rakhta hai, aur depot mein purane designs ka dher lag jaata hai. Chaar sau editions, har ek saath MB ka, aur har mahine storage ka bill. ECR mein lifecycle policy likho: "pichhle bees tagged editions rakho, aur untagged ko saat din baad hatao." Dhyaan: jo edition production mein chal raha hai, ya jis par rollback ho sakta hai, wo kabhi na hate. Isliye release ke labels, jaise `1.4.2`, ko alag niyam do. Aur depot mein scanning on rakho, taaki purana design bhi tab pakda jaaye jab uski nayi kamzori mile, Session 20 ke raat wale scan ki tarah.

### [08:20 – 11:10] Scene 5: Design par Mohar aur Saaman ki Soochi
**[VISUAL: A built design with three attachments: a Trivy report ("X-ray"), an SBOM listing every package inside (a parts list), and a signature from a signing tool. A deploy gate that checks the signature before running.]**

**(Voiceover):**
Depot mein design jaane se pehle teen cheezein sochne ki hain. Ek, X-ray: Trivy ki report, aur gate ki wahi niyam jo Session 20 mein tay hue, yaani fixable HIGH aur CRITICAL par fail. Do, SBOM: design ke andar ke har package ki ek soochi, yaani parts list. Kal koi nayi kamzori aaye, to aap seedhe dekh sakte ho ki kaun si trucks mein wo package hai. Teen, mohar: signing tool, jaise cosign, se design par ek digital hastakshar, taaki deploy karne wala check kar sake ki ye design sach mein hamari conveyor se aaya hai, kisi aur ne depot mein chupke se badla nahi. Ye teeno aaj ek lab nahi, par ek achhi aadat ki disha hain, aur bade teams mein ye zaroori hote hain.

### [11:10 – 14:05] Scene 6: Lab: Actions se Build aur Push
**[VISUAL: A workflow using `docker/login-action`, `docker/metadata-action`, `docker/build-push-action` that pushes to GHCR on a Git tag `v*` and on `main`. The repository's Packages tab shows the image with its tags. A Trivy step runs before push.]**

**(Voiceover):**
Lab. Vault mein Actions ki ek workflow:
```yaml
name: image
on:
  push:
    branches: [main]
    tags: ['v*']
permissions: { contents: read, packages: write }
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: docker/metadata-action@v5
        id: meta
        with: { images: "ghcr.io/${{ github.repository }}" }
      - uses: docker/login-action@v3
        with: { registry: ghcr.io, username: "${{ github.actor }}", password: "${{ secrets.GITHUB_TOKEN }}" }
      - uses: docker/build-push-action@v6
        with: { push: true, tags: "${{ steps.meta.outputs.tags }}", labels: "${{ steps.meta.outputs.labels }}" }
```
Push karo, aur Packages mein image dikhegi. Ek Git tag `v1.0.0` lagao aur dekho ki wahi design `1.0.0` label ke saath aata hai. Action versions ke liye docs dekh lena, aur Session 20 ki tarah unhe pin karo. Aakhir mein koi bhi doosri building `docker pull` karke wahi truck chala sakti hai.

### [14:05 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "version + SHA labels · Git tag → image tag · digest · depot with scan + lifecycle · push from CI with a role or token · never deploy latest". Then a courtyard full of trucks and a thick operations book fade in.]**

**(Voiceover):**
Recap: Docker ka poora safar: design likhna, chhota aur surakshit banana, label lagana aur depot mein bhejna. Aur ek sawaal jo ab bada ho gaya hai: sau trucks, das buildings. Koi gir jaaye to kaun use dobara chalayega? Naya edition kaun ek ek karke badlega, bina guests ko roke? Isi kaam ke liye head office ka operations command aata hai: Kubernetes. Agle session se.

---

# 📎 Student handout: Session 22 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Dockerfile | `FROM`, `WORKDIR`, `COPY`, `RUN`, `ENV` / `ARG`, `USER`, `HEALTHCHECK`, `CMD` / `ENTRYPOINT` |
| Exec form | `["python","app.py"]`; signal sahi pahunche |
| Bind | `0.0.0.0`, `127.0.0.1` nahi |
| Server | Flask dev server nahi; gunicorn jaisa asli server |
| Health check | Halka, `/health`; database tak nahi |
| Cache | Dependencies pehle, code baad mein; ek `RUN` mein apt |
| `.dockerignore` | `.git`, `.env`, `__pycache__`, bade folders |
| Secrets | Design mein nahi; `ARG` / `ENV` nahi; `--mount=type=secret`; `docker history` dekho |
| Multi-stage | Workshop peeche, sirf truck aage; `COPY --from=build` |
| Non-root | `USER app`; base pin karo; update niyam se |
| Architecture | Mac par amd64 ke liye `--platform linux/amd64` ya buildx |
| Labels | Version + SHA + digest; `latest` par deploy nahi |
| Git tag → image tag | `v1.4.2` tag se `1.4.2` aur `1.4.2-SHA` |
| Depot | GHCR, ECR, Artifact Registry, ACR; role ya token, password nahi |
| Depot ki safai | Lifecycle rule, scan on push; chalte edition ko mat hatao |
| CI push | login, metadata, build-push; Trivy pehle; actions pin |

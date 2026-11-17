# ✍️ 02: SCRIPT — SESSION-31: Capstone — CI/CD Pipeline, Code to Production
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`. Teaching order for the team flow: the author's own Git cohort, day 16 (`GIT_NOTES_INTEGRATION_MAP.md`, section 6).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S31`
- **Focus:** One end-to-end journey: a change made on a branch, a pull request with review and a required check, merge, the vault bell, the foreman's conveyor (test, truck design, scan, depot), a deploy to a building, a health check, an automatic rollback, and the control room watching. Definition of Done, design decisions, branch rules and `CODEOWNERS`, Terraform and Ansible for the infrastructure (optional), `rooms-service` with tests, `/health` and `/metrics`, Dockerfile recap, Jenkinsfile with multibranch and credentials, image tags from the Git SHA, a deploy script with health check and rollback, approval for production, a deploy marker, failure drills, cleanup, post-incident review
- **Builds on:** every earlier block: Session 04 (users, ownership), Session 05 (ports, `ufw`), Session 06 (Bash, exit codes), Session 09 (roles, key cabinet), Session 10 and 14 (buildings, security groups, wings), Session 16 and 16B (branch, pull request, master lock, tags), Session 17 to 19 (foreman, Jenkinsfile, webhook, workbench), Session 20 (scan stations), Session 21 and 22 (truck, truck design, depot), Session 26 (inspector, `/metrics`), Session 27 to 29 (Terraform, Ansible)
- **Story position:** All three zoom levels. Pehla grand opening: ek revision vault mein aata hai, ghanti bajti hai, foreman jaanchta hai aur truck design banata hai, ek truck building mein jaake khadi hoti hai, aur ek guest serve hota hai. Guest ki journey ke aathon kadam ek baar poore chalte hain.
- **Story words used:** every word from earlier sessions: vault, register, draft, master lock, chief architect (review), bell (webhook), foreman (Jenkins), conveyor (pipeline), station (stage), workbench (agent), key cabinet (credentials), truck, truck design, fit-out sheet (Dockerfile), edition label (tag), depot (registry), serving window (port), marshal (load balancer), inspector (Prometheus), wall of screens (Grafana), alarm desk (Alertmanager), setup crew (Ansible), master plan (Terraform), campus, wing, building, door guard (security group), gatehouse, duty badge, guest (end user), staff (admin)
- **Lab project:** Atithi's `rooms-service`, from first commit to a running truck on an app building, with a deliberate broken release that is caught and rolled back.
- **Cost rule:** two small instances for a few hours (or two local VMs). Stop or destroy them after the lab, revoke the tokens, delete the depot images you no longer need, and check the console for leftovers.
- **Episodes:**
  - Episode 1: Grand Opening ka Plan: Journey, Faisle aur Team ke Niyam
  - Episode 2: Service aur Truck: Tests, Health, Metrics aur Truck Design
  - Episode 3: Foreman ki Conveyor: Test, Truck Design, Scan, Depot
  - Episode 4: Pahunchao, Jaancho, Wapas Lo: Deploy, Rollback aur Control Room

---

# 📺 EPISODE 1: Grand Opening ka Plan

### [00:00 – 02:10] Scene 1: Ab Tak Ke Tukde, Ab Poori Kahani
**[VISUAL: A montage of earlier sessions as puzzle pieces: Linux staff, Git vault, Jenkins foreman, Docker truck, campus, control room. They snap together into one flow from a designer's laptop to a guest's phone.]**

**(Voiceover):**
Ab tak Atithi Hotels ne alag alag cheezein seekhi: building ke andar Linux, campus mein AWS, head office mein vault, foreman aur trucks, aur control room. Aaj sab ek saath. Ek designer room ki ek line badalta hai, aur kuch minute baad wo badlaav ek asli building mein, ek asli truck mein, ek asli guest ko dikh raha hota hai. Beech mein koi haath se kuch nahi karta, aur agar kuch toota to guest tak pahunchne se pehle ruk jaata hai. Ye Build, Ship, Fix ki poori kahani hai. Is session ka ek naya niyam: naya kuch seekhna nahi, jo seekha hai wahi jodna hai.

### [02:10 – 04:35] Scene 2: Guest ki Journey: Aathon Kadam
**[VISUAL: The eight steps of the guest's journey lit one at a time on a map: directory lookup (DNS), roads (internet), campus main gate, marshal, door guard and door 443, truck serves, records office and warehouse, control room. Beside each, the session number where it was taught.]**

**(Voiceover):**
Story ke shuru mein humne guest ki journey ke aath kadam kaha tha. Guest directory mein hotel ka address dhoondhta hai, yaani DNS. Raaste aur junction par chalta hai. Campus ke main gate par pahunchta hai. Marshal use khuli building mein bhejta hai. Door guard list dekh kar door 443 se andar jaane deta hai. Ek truck use serve karti hai. Truck records office aur warehouse se baat karti hai. Aur control room ye poori visit apni screens par dekhta hai. Aaj hum ek truck banate hain, usse pahunchate hain, aur dekhte hain ki wo kadam chaar se aath tak sach mein kaam karti hai. Pehle teen kadam ke liye campus Session 14 ka hi rahega.

### [04:35 – 07:15] Scene 3: Pehle Team ka Niyam, Phir Ghanti
**[VISUAL: A flow: draft branch `feature/room-count` → commits → push → pull request → chief architect's review → required check from the foreman → merge to master → the vault's bell rings. A crossed-out arrow: "push straight to master". A `CODEOWNERS` file naming the pipeline folder owner.]**

**(Voiceover):**
Sabse pehli galti jo hum capstone mein rokte hain: seedha master par push. Session 16B ka master lock yaad hai. Isliye grand opening ka pehla kadam kod nahi, team ka niyam hai. Har badlaav ek draft branch par, jaise `feature/room-count`. Vault mein push, aur ek pull request. Chief architect, yaani reviewer, dekhta hai. Foreman ka required check, yaani test aur scan, sabz hona chahiye. Tabhi master mein merge. Aur sirf merge hone par ghanti bajegi, yaani webhook, aur truck baahar jayegi. Branch protection mein ye teen niyam rakho: review zaroori, check zaroori, seedha push band. Ek `CODEOWNERS` file mein likho ki `Jenkinsfile` aur `deploy/` ka maalik kaun hai, taaki conveyor ke niyam bina us maalik ke review ke na badlein. Isse conveyor ki apni suraksha banti hai.

### [07:15 – 10:05] Scene 4: Design ke Faisle aur Definition of Done
**[VISUAL: A decision table. Registry: GHCR or ECR. Deploy target: one app building with Docker. Image tag: first seven letters of the Git SHA. Secrets: key cabinet. Rollback: previous edition label. Approval: only before production. A "Definition of Done" checklist.]**

**(Voiceover):**
Ab faisle likh lo, kyunki jo likha nahi, wo beech mein badalta hai. Depot: GHCR ya ECR. Deploy target: ek app building, jahan Docker chal raha hai, kyunki hum simple rakhte hain. Edition label: Git SHA ke pehle saat akshar, taaki har truck se vault ka ek revision milaya ja sake. Secrets: key cabinet mein, kisi file mein nahi. Rollback: pichhla edition label. Aur Definition of Done: master mein merge se production tak sab automatic, test fail ho to truck design banta hi nahi, scan fail ho to depot mein nahi jaata, health check fail ho to purani truck wapas, aur har deploy ka record. Ye likhe hone se project ke beech mein bhatakna nahi padta, aur interview mein isse accha jawab nahi: "mera success criteria ye tha, aur ye maine kaise saabit kiya".

### [10:05 – 12:55] Scene 5: Infra: Master Plan aur Setup Crew se
**[VISUAL: Two paths. Path A (quick): two Ubuntu VMs, `jenkins` and `app`, with a security-group checklist. Path B (bonus): a Terraform plan creating the two buildings and the security groups, then an Ansible checklist installing Docker on both and Java plus Jenkins on one. Diagram: `jenkins-sg` allows 8080 only from the author's IP; `app-sg` allows 22 only from `jenkins-sg` and 8081 from the author's IP.]**

**(Voiceover):**
Infra ke do raaste hain. Seedha raasta: do chhote Ubuntu buildings, `jenkins` aur `app`, haath se. Bonus raasta: Session 27 aur 28 ka master plan buildings aur door guards banaye, aur Session 29 ki setup crew dono mein Docker lagaye, aur ek mein Java aur Jenkins. Jo bhi raasta lo, niyam wahi. Jenkins ka port 8080 sirf aapke IP se. App building par staff entrance, yaani port 22, sirf Jenkins building ke security group se. Aur guest ka door, jaise 8081, aapke IP se aaj ke test ke liye. Jenkins building se app building par bina password ke SSH key chalaao, aur wo private key Jenkins ke key cabinet mein SSH credential ke type se rakho, kisi file mein nahi. Session 17 ka `jenkins` user aur Session 4 ka key permission `600` yaad rakho.

### [12:55 – 15:10] Scene 6: Lab: Repo, Rules aur Pehla Check
**[VISUAL: A new repo `atithi-rooms`. Branch protection on `main`: require pull request, require one review, require status checks, block force push. A `.gitignore` for Python. A `CODEOWNERS` file. A first pull request that only adds a README.]**

**(Voiceover):**
Lab: GitHub par `atithi-rooms` repo banao. Branch protection on karo: pull request zaroori, ek review, status checks zaroori, aur force push band. `.gitignore` mein `__pycache__/`, `.venv/` aur `.env`. `CODEOWNERS` mein `Jenkinsfile` aur `deploy/` ka maalik likho. Phir ek chhota test: ek branch banao, README mein ek line jodo, push karo, pull request kholo, aur dekho ki merge button tab tak band hai jab tak review aur check na ho. Abhi check koi nahi hai, to ye agle episodes mein aayega. Bas dekh lo ki master par seedha push sach mein rukta hai. Agar kisi ek account ko bypass milta hai, to uski wajah likho aur band karo.

### [15:10 – 15:40] Scene 7: Recap aur Bridge
**[VISUAL: A card: "journey in eight steps · team flow first: branch, PR, review, required check, merge, then the bell · decisions written · Definition of Done · infra by hand or by Terraform + Ansible".]**

**(Voiceover):**
Recap: guest ki journey, team ka niyam, faisle aur infra. Ab service aur uska truck.

---

# 📺 EPISODE 2: Service aur Truck

### [00:00 – 01:40] Scene 1: Pipeline ka Kaam, Service ka Nahi
**[VISUAL: A small `rooms-service` with `/rooms`, `/health` and `/metrics`. A large pipeline arrow pointing at it. Text: "The service can be small; the pipeline is the lesson".]**

**(Voiceover):**
Capstone mein service chhoti rakhenge, kyunki seekhne ki cheez pipeline hai. Hum Session 22 ki `rooms-service` lete hain: Flask ki ek app, jo room ki list deti hai, `/health` par zinda hone ka jawab deti hai, aur Session 26 ke baad `/metrics` bhi deti hai. Aap apni Node ya Java app se bhi yahi kar sakte ho: concept wahi.

### [01:40 – 05:15] Scene 2: Service, Tests aur Health
**[VISUAL: `app.py` with `/rooms`, `/health`, `/metrics`. `tests/test_app.py` using Flask's test client. `requirements.txt` with `flask`, `gunicorn`, `prometheus-client`, `pytest`. A terminal run of `pytest -q`.]**

**(Voiceover):**
Ek chhoti app:
```python
from flask import Flask, jsonify

app = Flask(__name__)
ROOMS = [{"id": 1, "type": "deluxe", "free": 4}, {"id": 2, "type": "suite", "free": 1}]

@app.get("/rooms")
def rooms():
    return jsonify(ROOMS)

@app.get("/health")
def health():
    return "ok", 200
```
Aur ek test:
```python
from app import app

def test_rooms_returns_list():
    r = app.test_client().get("/rooms")
    assert r.status_code == 200
    assert len(r.get_json()) >= 1

def test_health():
    assert app.test_client().get("/health").status_code == 200
```
`pytest -q` chalao. Conveyor ki sabse pehli suraksha yahi tests hain. `/health` halka rakho, aur database tak na jaao, taaki marshal aur deploy ka check database ki dikkat par poori fleet ko bimaar na dikhaye. `/metrics` Session 26 se aata hai, to wahi code yahan jod do, aur label mein route rakho, room ya guest ki ID nahi.

### [05:15 – 08:50] Scene 3: Truck Design: Fit-out Sheet
**[VISUAL: The multi-stage Dockerfile from Session 22: `python:3.12-slim`, a build stage with dependencies, a final stage copying them, `USER app`, `EXPOSE 5000`, `HEALTHCHECK`, gunicorn `CMD`. A `.dockerignore` with `.git`, `.venv`, `__pycache__`, `.env`, `tests`.]**

**(Voiceover):**
Fit-out sheet wahi jo Session 22 mein banayi thi:
```dockerfile
FROM python:3.12-slim AS build
WORKDIR /w
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
RUN useradd -m -u 10001 app
WORKDIR /app
COPY --from=build /install /usr/local
COPY app.py .
USER app
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5000/health')" || exit 1
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "2", "app:app"]
```
Ek hi baat ka dhyaan: `requirements.txt` pehle copy hota hai, taaki naya code aane par bhi libraries ki layer cache se aaye. Non-root user, gunicorn, `0.0.0.0`, health check: sab Session 22 se. `.dockerignore` mein `.git`, `.env` aur `.venv` zaroor, warna secret truck design mein ghus sakta hai. Production ke liye base image ko version par pin karo.

### [08:50 – 10:55] Scene 4: Pehle Local, Phir Pipeline
**[VISUAL: A "works on my laptop first" ladder: `pytest`, `docker build`, `docker run`, `curl /health`, `curl /rooms`, `curl /metrics`. A rule card: "never debug the pipeline with an app that has never run".]**

**(Voiceover):**
Ek purana niyam: jo laptop par nahi chalta, use conveyor par mat chalao. Pehle `pytest`. Phir `docker build -t rooms:local .`, `docker run -d -p 8081:5000 rooms:local`, aur `curl localhost:8081/health`, `/rooms`, `/metrics`. Jab teeno sahi, tab pull request. Aur ek aadat: pipeline mein jo bhi command hai, wo pehle haath se chal chuki ho. Isse jab conveyor laal hoti hai, to aap jaante ho ki galti conveyor mein hai, app mein nahi.

### [10:55 – 13:45] Scene 5: Lab: Pehla Pull Request
**[VISUAL: A branch `feature/first-service` with `app.py`, `tests/`, `Dockerfile`, `.dockerignore`, `requirements.txt`. The pull request page with a reviewer comment on the Dockerfile. After approval, the merge button turns green. A second laptop runs `git clone` and `docker build`.]**

**(Voiceover):**
Lab: ek branch banao, jaise `feature/first-service`. Upar ki saari files rakho. `pytest -q`, `docker build`, `docker run`, aur teen `curl`. Phir commit, push, aur pull request. Kisi doosre se, ya khud ek doosre account se, review karwao: kam se kam ek comment Dockerfile par, jaise "base image pin karo". Review ke baad merge. Ek aur laptop par, ya nayi folder mein, `git clone` karke `docker build` chalao, aur dekho ki bina aapke laptop ki kisi cheez ke wahi truck banta hai. Agar nahi banta, to koi file vault mein jaana bhool gayi, aur abhi pakadna sasta hai.

### [13:45 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "tests · /health light · /metrics by route · fit-out sheet from Session 22 · local first · PR with review".]**

**(Voiceover):**
Recap: service, tests, truck design aur pehla pull request. Ab foreman ki conveyor, jo ye sab khud chalaye.

---

# 📺 EPISODE 3: Foreman ki Conveyor

### [00:00 – 01:20] Scene 1: Merge Karo, Baaki Machine Karegi
**[VISUAL: A merge to `main`. The vault bell rings (webhook). The foreman's stage view lights up station by station. A Slack message says "Build #42 passed, rooms-service:3f9a2c1".]**

**(Voiceover):**
Ab wo kaam jo aap haath se karte ho, test, truck design banana, jaanchna, depot mein bhejna, foreman ko do. Hum ek `Jenkinsfile` likhenge jo test se depot tak jaaye. Pull request par sirf test aur scan chalega, kyunki unse merge ka faisla hota hai. Master par merge ke baad truck design bhi depot mein jaayegi. Deploy agle episode mein.

### [01:20 – 05:10] Scene 2: Jenkinsfile
**[VISUAL: A Jenkinsfile. `options` with a timeout. `environment` with REGISTRY, IMAGE and TAG from the Git SHA. Stages: Test, Build image, Scan, Push (with `when { branch 'main' }`), and `post` notifications. Callouts: "credentials only where needed", "the push station runs only on main".]**

**(Voiceover):**
Jenkinsfile:
```groovy
pipeline {
  agent any
  options { timeout(time: 20, unit: 'MINUTES') }
  environment {
    REGISTRY = 'ghcr.io/YOUR_ORG'
    IMAGE    = "${REGISTRY}/rooms-service"
    TAG      = "${env.GIT_COMMIT.take(7)}"
  }
  stages {
    stage('Test') {
      steps {
        sh 'python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt && pytest -q'
      }
    }
    stage('Build image') { steps { sh 'docker build -t $IMAGE:$TAG .' } }
    stage('Scan') {
      steps { sh 'trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE:$TAG' }
    }
    stage('Push') {
      when { branch 'main' }
      steps {
        withCredentials([usernamePassword(credentialsId: 'ghcr', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo "$P" | docker login ghcr.io -u "$U" --password-stdin'
          sh 'docker push $IMAGE:$TAG'
        }
      }
    }
  }
  post { failure { echo "FAILED: ${env.BUILD_URL}" } }
}
```
Edition label Git SHA ke pehle saat akshar: depot mein jo truck dikhe, vault mein uska exact revision mile. `when { branch 'main' }` sirf multibranch project mein chalta hai, jo Session 19 mein dekha. Aur Push station ke andar hi credentials khulte hain, poori conveyor mein nahi.

### [05:10 – 08:10] Scene 3: Gate: Jo Kharab Hai Wo Aage Nahi Jaata
**[VISUAL: A failing Test station turns red and the later stations grey. A Trivy report shows a HIGH vulnerability in an old base image, failing the Scan. The depot page on GHCR shows the pushed truck design with its short-SHA label. The pull request page shows two green checks.]**

**(Voiceover):**
Conveyor ka asli kaam rokna hai. Test fail hua to aage ke station skip, truck design banegi hi nahi. Trivy ne HIGH ya CRITICAL kamzori dekhi to scan laal, aur truck design depot tak nahi pahunchti. Kamzori aksar aapke code mein nahi, kisi aur ke base image ya library mein hoti hai. Phir kya karna hai: base image update, ya library upgrade, ya jaanboojh kar ek chhoti ignore list, jiske saath likha ho ki kyun. Pull request par jo check dikhte hain, wahi master lock ke required checks hain. Ek sabz nishan ka matlab hai ki foreman ne jaancha, aur tabhi chief architect merge ka button dabaata hai. Aur agar scan ya build mein bahut samay lagta hai, to Docker layer cache aur pip cache workbench par rakho.

### [08:10 – 10:45] Scene 4: Key Cabinet aur Ghanti
**[VISUAL: Jenkins credentials page: `ghcr` (username and token), `app-server-key` (SSH key). A multibranch project with the GitHub source. A webhook in the GitHub repo pointing at `/github-webhook/` with a green delivery tick.]**

**(Voiceover):**
Do cheezein key cabinet mein: `ghcr` ka username aur token, jise sirf packages likhne ki ijaazat ho, aur `app-server-key`, wahi SSH key. Dono aise scope mein ki sirf is project ki conveyor unhe dekh sake. Multibranch project mein GitHub ko source banao. Repo mein webhook lagao, jo Jenkins ke `/github-webhook/` par jaata hai. GitHub ki delivery page par ek hara nishan dekho: yehi ghanti hai. Agar ghanti nahi baj rahi, to usually teen kaaran: Jenkins tak raasta nahi (security group ya URL), webhook mein galat URL, ya Jenkins mein GitHub plugin ka setting. Ek periodic scan bhi rakho, taaki koi chhooti hui ghanti pakdi jaye. Fork wale pull request ke liye trust setting wahi: Everyone nahi.

### [10:45 – 12:50] Scene 5: Teen Jaan-boojh ke Hadse
**[VISUAL: Three drills. 1: break a test, Test goes red. 2: pin an old base image with a known vulnerability, Scan goes red. 3: revoke the depot token, Push goes red. For each: where to look in the log.]**

**(Voiceover):**
Ab teen jaan-boojh ke hadse, kyunki conveyor ka bharosa tab banta hai jab aapne use todkar dekha ho. Pehla: ek test tod do, to Test laal. Doosra: Dockerfile mein ek purana base image rakho jisme kamzori ho, to Scan laal. Teesra: depot ka token galat kar do, to Push laal. Har laal station ke log mein dhoondho ki kaaran kahan likha hai. Ye wahi debugging hai jo asli team har hafte karti hai. Ek aur: pull request par Push station chalta hi nahi, kyunki wo sirf master ke liye hai. Ye bhi jaanch lo.

### [12:50 – 15:00] Scene 6: Lab: Conveyor Chalao
**[VISUAL: A multibranch project scanning the repo. A pull request starts a build with Test and Scan. After merge, `main` builds and pushes. The depot shows `rooms-service:3f9a2c1`. Branch protection updated to require the Jenkins check.]**

**(Voiceover):**
Lab: Jenkinsfile ko ek pull request mein jodo. Multibranch project banao, webhook lagao, `ghcr` credential rakho. Pull request par Test aur Scan chalte dekho, aur Push ko skip hote. Branch protection mein Jenkins ke check ko required banao. Phir merge karo, aur master par Push chalte dekho. GHCR ke packages ke page par SHA wala edition label dikhega. Teen hadse dobara karo, ek ek karke, aur har baar wapas theek karo. Agar workbench par Docker ya Trivy nahi hai, to Session 18 aur 22 ka install wapis dekho. Trivy ka install official guide se, version apna dekh lo.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "PR: test + scan required · main: build + push · SHA edition label · key cabinet scopes · bell that rings · break it on purpose".]**

**(Voiceover):**
Recap: CI poora ho gaya. Ab CD: truck ko building mein pahunchao, jaancho, aur zaroorat ho to wapas lo.

---

# 📺 EPISODE 4: Pahunchao, Jaancho, Wapas Lo

### [00:00 – 01:05] Scene 1: Deploy Mein Sabse Zyada Galti
**[VISUAL: A new truck is started. Nobody checks. The truck crashes at startup. For twenty minutes guests see errors. Next: the same release with a health check and an automatic rollback, and guests never notice.]**

**(Voiceover):**
Deploy wo kadam hai jahan sabse zyada galtiyan hoti hain. Nayi truck chalu ki, kisi ne check nahi kiya, aur bees minute tak guests ko error dikha. Isliye deploy ke baad health check zaroori hai, aur dono, check aur rollback, automatic hone chahiye. Insaan raat ko teen baje se behtar script hai, jo har baar wahi kare.

### [01:05 – 04:50] Scene 2: Deploy Script
**[VISUAL: `deploy.sh` run over SSH. Steps: pull the new truck design, remember the current edition label, start the new truck on a spare port, check `/health`, switch, stop the old, or remove the new and keep the old. A deploy log line appended: time, who, label, result.]**

**(Voiceover):**
App building par ek chhoti script, `deploy/deploy.sh`:
```bash
#!/usr/bin/env bash
set -euo pipefail
IMAGE="$1"; NAME=rooms
PREV=$(docker inspect -f '{{.Config.Image}}' "$NAME" 2>/dev/null || true)
docker pull "$IMAGE"
docker rm -f "$NAME" 2>/dev/null || true
docker run -d --name "$NAME" --restart unless-stopped -p 8081:5000 "$IMAGE"
for i in $(seq 1 20); do
  if curl -fsS http://localhost:8081/health >/dev/null; then
    echo "$(date -Is) deployed $IMAGE (was ${PREV:-none})" | sudo tee -a /var/log/atithi-deploys.log
    exit 0
  fi
  sleep 3
done
echo "$(date -Is) FAILED $IMAGE, rolling back to ${PREV:-none}" | sudo tee -a /var/log/atithi-deploys.log
docker rm -f "$NAME"
[ -n "$PREV" ] && docker run -d --name "$NAME" --restart unless-stopped -p 8081:5000 "$PREV"
exit 1
```
Pehle purani truck ka label yaad rakhta hai. Naya design pull karta hai. Truck chalata hai. Bees baar, har teen second par, health check. Pass to log mein ek line, fail to purani truck wapas aur script `exit 1`, jisse Jenkins ka station laal ho. Humne ise ek local registry aur ek toote hue release ke saath aazmaya: pehli deploy, upgrade aur rollback teeno sahi chale, aur log mein teeno line aayi. Ek chhoti baat: rollback ke turant baad purani truck ko khud health check mein aane mein kuch second lagte hain, isliye rollback ke baad bhi ek baar health dekho. Ek sachchai: isme kuch second ke liye service ruk jaati hai. Kai buildings ke saath rolling ya blue-green se ye bacha jaata hai, jo Kubernetes ka kaam hai. Ek building ke liye ye saaf aur seekhne layak hai.

### [04:50 – 06:55] Scene 3: Pehle Staging, Phir Manjoori, Phir Production
**[VISUAL: Jenkins stages: Deploy staging, Smoke test, an `input` step "Deploy to production?" with a timeout (with `agent none` so no workbench is held), then Deploy production. A box: "approval only by the duty manager".]**

**(Voiceover):**
Asli setup mein pehle staging par deploy, phir ek chhota smoke test, jaise `/rooms` ka jawab. Uske baad manjoori ka station, `input`, jisme "Production par bhejna hai?" poocha jaata hai. Session 19 ki baat: `input` ke samay workbench rok kar mat rakho, yaani `agent none` aur ek timeout. Manjoori sirf duty manager ke group se, aur har manjoori ka naam record mein. Deploy stage mein SSH `sshagent(['app-server-key'])` se, aur script ko `ssh ubuntu@APP_IP 'bash -s' -- "$IMAGE:$TAG" < deploy/deploy.sh` ki tarah chalao, taaki script alag se copy na karni pade. Agar staging aur production alag buildings hain, to bas IP ka farq hai. Wahi checklist, wahi script.

### [06:55 – 09:00] Scene 4: Deploy ke Baad Control Room
**[VISUAL: Prometheus scraping `/metrics` of the app building. A Grafana panel with request rate, error rate and p95 latency. A vertical line marks the deploy time with the edition label. An alert rule: error rate above one percent for five minutes.]**

**(Voiceover):**
Deploy khatam hone ka matlab kaam khatam nahi. Control room dekho. Session 26 ka inspector app building ke `/metrics` ko padhta hai. Wall of screens par request rate, errors aur latency. Deploy ke samay ek line lagao, jis par edition label likha ho, taaki graph par dikhe ki kab version badla. Agar errors us line ke baad badhe, to pehla shak naye release par. Ek alarm bhi rakho: errors ek percent se zyada paanch minute tak. Ye script ke health check se alag hai: health check batata hai ki truck zinda hai, aur control room batata hai ki guests ko theek serve ho rahi hai. Dono chahiye.

### [09:00 – 11:05] Scene 5: Jab Rollback bhi Kam Pad Jaye
**[VISUAL: A comparison of three rollback layers. 1: the script's automatic rollback to the previous label (seconds). 2: a manual rerun of the deploy with an older label (minutes). 3: a `git revert` through a new pull request (the history stays honest). A note: "database changes cannot be rolled back by changing the truck".]**

**(Voiceover):**
Rollback ke teen star hain. Pehla: script khud purani truck wapas laati hai, kuch second mein. Doosra: koi release baad mein kharab nikla, to Jenkins se ek purane edition label ko dobara deploy karo. Teesra: kharab badlaav ko vault se bhi hatao, `git revert` se naya pull request, taaki register imaandar rahe, jaisa Session 16B mein dekha. Ek chetavani: truck wapas laana aasaan hai, par agar naye release ne database mein kuch badal diya, to purani truck us database ke saath nahi chal sakti. Isliye database ke badlaav chhote aur peeche ki taraf mel khate hon, pehle database, phir truck, aur kabhi ek saath bada badlaav nahi.

### [11:05 – 13:25] Scene 6: Lab: Poora Safar aur Toota Hua Release
**[VISUAL: Add a Deploy stage with `sshagent` to the Jenkinsfile. A change to the `/rooms` response goes through pull request, merge, and the new data appears on the app building. Then a deliberately broken release crashes at startup: the health loop fails, the old truck is back, the stage is red, the deploy log shows FAILED and the rollback.]**

**(Voiceover):**
Lab: Jenkinsfile mein Deploy station jodo, jisme `sshagent(['app-server-key'])` ho. Pehle ek chhota badlaav: `/rooms` mein ek naya room type jodo, pull request, review, merge. Kuch minute mein `curl http://APP_IP:8081/rooms` mein naya data. Ab ek toota hua release: app ke shuru mein jaan-boojh kar ek exception daalo, jisse wo start par crash ho. Pull request par test shayad pass ho jaaye, aur isiliye pehle ye bhi dekho ki kaun sa check is hadse ko nahi pakadta: ek test jodo jo app ko import karke dekhe. Phir bhi, agar release chhoot gaya, to Deploy station health check par laal hoga, script purani truck wapas laayegi, site chalti rahegi, aur `/var/log/atithi-deploys.log` mein FAILED aur rollback ka record rahega. Wahi Fix wala hissa.

### [13:25 – 15:20] Scene 7: Safai aur Post-Incident Review
**[VISUAL: A cleanup checklist: stop or destroy the two buildings, revoke the depot token, remove the SSH key from the key cabinet, delete test images, check for leftover volumes, public IPs and security groups, budget alert on. Beside it: a short blameless review template: what happened, what the check caught, what it missed, one change.]**

**(Voiceover):**
Safai ka checklist: dono buildings band ya delete, depot token revoke, SSH key key cabinet se hatao, test images delete, aur console mein dekho ki koi volume, public IP ya security group baaki to nahi. Aur ek chhota post-incident review likho, bina kisi par ilzaam ke: kya hua, kis check ne pakda, kis ne nahi pakda, aur ek badlaav jo agli baar rokega. Ye likhna asli teams ki aadat hai, aur interview mein bhi kaam aati hai. Aur ab pichhe mudo: master lock, bell, foreman, truck, depot, health check, rollback, control room. Atithi ka pehla grand opening poora.

### [15:20 – 16:55] Scene 8: Recap aur Bridge
**[VISUAL: A card: "branch → PR → review → required check → merge → bell → test → truck design → scan → depot → deploy → health → rollback → control room". Then a new figure appears at the head office: a well-read assistant sitting beside a designer.]**

**(Voiceover):**
Recap: aapne code se production tak ek poori, surakshit conveyor banayi, aur use jaan-boojh kar todkar dekha. Ab Atithi ke head office mein ek naya sadasya aata hai: ek bahut padha-likha assistant. Pehle wo ek bahari expert ki tarah phone par jawab dega, jo har guest ke sawaal par kaam aaye. Phir ek trained brain ki tarah, jo apni truck mein chalta hai, aur kisi bhi truck ki tarah naya version pahunchaya jaata hai. Agla session: AI apps aur model serving.

---

# 📎 Student handout: Session 31 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Journey | DNS → roads → main gate → marshal → door guard → truck → records office and warehouse → control room |
| Team flow | Draft branch → push → PR → review → required check → merge → bell |
| Branch protection | Review, required checks, no force push, no direct push to `main` |
| `CODEOWNERS` | `Jenkinsfile` aur `deploy/` ka maalik review mein |
| Definition of Done | Merge se production tak automatic; fail par rukna; ek rollback; deploy ka record |
| Edition label | Git SHA ke pehle 7 akshar |
| Test | `pytest -q` pehle, haath se, phir conveyor mein |
| `/health` | Halka, database tak nahi |
| Truck design | Multi-stage, non-root, gunicorn, `0.0.0.0`, `HEALTHCHECK`, `.dockerignore` |
| Jenkinsfile | Test → Build → Scan → Push (`when { branch 'main' }`) |
| Scan | Trivy, `--exit-code 1` on HIGH, CRITICAL |
| Key cabinet | `ghcr` token (sirf packages), `app-server-key`; scope chhota |
| Bell | Webhook `/github-webhook/` + periodic scan; fork trust: Everyone nahi |
| Deploy | Pull, run, 20 health checks, success log ya rollback, `exit 1` |
| Approval | `input` with `agent none` aur timeout; duty manager group |
| Observe | `/metrics`, deploy marker, error alert |
| Rollback | Script (seconds) → older label (minutes) → `git revert` PR |
| Database | Truck wapas ho sakti hai, database badlaav nahi; chhote, peeche-compatible badlaav |
| Safai | Buildings, tokens, keys, images, volumes, IPs; budget alert; post-incident review |

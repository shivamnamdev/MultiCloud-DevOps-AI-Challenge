# ✍️ 02: SCRIPT — SESSION-18: Jenkins Pipelines & Plugins
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S18`
- **Focus:** Pipeline depth (parameters, env, when, parallel), Groovy basics, webhooks, key plugins (Git, Docker, Slack, SonarQube), shared libraries
- **Episodes:**
  - Episode 1: Pipeline ko Smart Banao: parameters, when, parallel
  - Episode 2: Webhook: Commit Hote Hi Build
  - Episode 3: Plugins: Slack, Docker aur Quality Gate
  - Episode 4: Shared Library: Code Dohrao Nahi

---

# 📺 EPISODE 1: Pipeline ko Smart Banao

### [00:00 – 01:15] Scene 1: Ek Pipeline, Kai Kaam
**[VISUAL: A single linear pipeline that is slow (20 min). Next, the same pipeline with parallel branches finishing in 8 min.]**

**(Voiceover):**
Ek pipeline jo har stage ek ke baad ek chalaye, bees minute leti hai. Wahi pipeline agar tests ko parallel chalaye, aur sirf zaroorat padne par deploy kare, to aath minute mein ho jaati hai. Aaj hum pipeline ko smart banate hain.

### [01:15 – 05:00] Scene 2: parameters, environment aur when
**[VISUAL: Jenkinsfile snippet: `parameters { choice(name:'ENV', choices:['dev','staging'], description:'Target') }`, `environment { APP_NAME = 'shop' }`, `when { branch 'main' }`, `when { expression { params.ENV == 'staging' } }`.]**

**(Voiceover):**
`parameters` block se user chunta hai ki kahan deploy karna hai, jaise dev ya staging. `environment` mein pure pipeline ke variables. `when` condition stage ko tabhi chalata hai jab shart sahi ho, jaise sirf `main` branch par deploy. Ye teen cheezein ek pipeline ko flexible banati hain, bina copy paste ke. Aur yaad rakho: production deploy ke liye manual approval ka stage rakhna `input` step se kaafi surakshit hai.

### [05:00 – 08:30] Scene 3: Parallel Stages aur Groovy Basics
**[VISUAL: A `parallel` block with `Unit tests` and `Lint` side by side. A tiny Groovy snippet: a variable, a `def` function, a `script { }` block, string interpolation `"Build ${env.BUILD_NUMBER}"`.]**

**(Voiceover):**
Parallel stages mein do independent kaam ek saath chalte hain, jaise unit tests aur lint, aur jo dheere hota hai wahi total time tay karta hai. Declarative pipeline ke andar kabhi kabhi Groovy code chahiye hota hai, jiske liye `script { }` block hota hai. Groovy mein `def x = 5`, string interpolation `"Build ${env.BUILD_NUMBER}"`, aur functions. Rule: pipeline mein jitna kam Groovy, utna behtar. Complex logic ko scripts ya shared library mein daalo.

### [08:30 – 11:30] Scene 4: Lab: Smart Pipeline
**[VISUAL: A Jenkinsfile with a `parameters` choice, a parallel test/lint stage, a `when { branch 'main' }` deploy stage, and an `input` approval. The Stage View shows parallel boxes.]**

**(Voiceover):**
Lab: apni Jenkinsfile mein ye badlav karo: ek `ENV` choice parameter, `Test` aur `Lint` ko `parallel` mein, aur ek `Deploy` stage jo `when { branch 'main' }` ke saath chale aur uske pehle `input { message 'Deploy to ' + params.ENV + '?' }`. Chalao aur Stage View mein parallel branches dekho. Deploy abhi sirf `echo` kare, asli deploy hum capstone mein karenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "parameters · environment · when · parallel · input · minimal Groovy".]**

**(Voiceover):**
Recap: smart pipeline. Ab Jenkins ko commit hote hi build karwana, bina button dabaye.

---

# 📺 EPISODE 2: Webhook — Commit Hote Hi Build

### [00:00 – 01:15] Scene 1: Build Now ab Nahi
**[VISUAL: A developer pushes code, then walks to the Jenkins dashboard and clicks "Build Now". A sign: "CI is not a button".]**

**(Voiceover):**
Agar CI sirf tab chale jab koi "Build Now" dabaye, to wo CI nahi, ek manual process hai. Asli CI mein push hote hi build shuru hota hai. Do tareeke hain: poll, jisme Jenkins har kuch minute pooche, aur webhook, jisme GitHub khud Jenkins ko bata de.

### [01:15 – 05:00] Scene 2: Poll SCM vs Webhook
**[VISUAL: Left: Jenkins repeatedly asking GitHub "any change?" every 5 min (wasteful). Right: GitHub sending an HTTP POST to Jenkins on push (instant).]**

**(Voiceover):**
Poll SCM mein Jenkins baar baar GitHub se poochta hai ki kuch badla? Bekaar traffic aur deri. Webhook mein GitHub ek HTTP request Jenkins ke URL par bhejta hai jab bhi push ya PR hota hai. Ye tez aur sasta hai. Isme ek shart: Jenkins ka URL GitHub ko dikhna chahiye. Local ya private network mein ho to tunnel ya reverse proxy chahiye, aur webhook ko secret ke saath surakshit karna chahiye.

### [05:00 – 08:30] Scene 3: Webhook Set Karna aur Surakshit Rakhna
**[VISUAL: GitHub repo → Settings → Webhooks → Payload URL `http://JENKINS/github-webhook/`, content type JSON, push events. Jenkins job: "GitHub hook trigger for GITScm polling". A shield: reverse proxy + HTTPS.]**

**(Voiceover):**
GitHub repo ke Settings mein Webhooks, Payload URL `http://JENKINS_HOST:8080/github-webhook/`, content type JSON, aur events mein push. Jenkins job mein "GitHub hook trigger for GITScm polling" on karo. Production mein Jenkins ko seedha internet par kholne ki jagah reverse proxy aur HTTPS ke peeche rakho. Aur GitHub Actions ya Multibranch scanning jaise options bhi hain, par webhook samajhna har CI system mein kaam aata hai.

### [08:30 – 11:30] Scene 4: Lab: Push par Auto Build
**[VISUAL: A commit pushed. GitHub shows a green delivery tick on the webhook. Jenkins starts a build within seconds. The build log says "Started by GitHub push".]**

**(Voiceover):**
Lab: apne repo mein webhook lagao. Jenkins job par hook trigger on karo. Ab ek chhota change commit karo aur push karo. Kuch second mein Jenkins mein naya build shuru hoga, aur log mein "Started by GitHub push" dikhega. GitHub ke webhook page par Recent Deliveries mein response code dekho: 200 matlab sahi. Agar na chale, to firewall port 8080, ya URL, ya content type galat ho sakta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "webhook > polling · /github-webhook/ · secure Jenkins · check Recent Deliveries".]**

**(Voiceover):**
Recap: webhook se instant CI. Ab Jenkins ko doosre tools se jodne wale plugins.

---

# 📺 EPISODE 3: Plugins — Slack, Docker aur Quality Gate

### [00:00 – 01:15] Scene 1: Jenkins ki Asli Taakat
**[VISUAL: Jenkins as a hub with spokes to dozens of tool logos (Git, Docker, Slack, SonarQube, AWS). A caution tag on the hub: "every plugin = more to maintain".]**

**(Voiceover):**
Jenkins ke paas hazaaron plugins hain, aur wahi uski taakat hai. Lekin har plugin ek aur cheez hai jise update aur surakshit rakhna padta hai. Isliye rule: sirf wahi plugins lagao jinki zaroorat ho, aur unhe update rakho.

### [01:15 – 05:00] Scene 2: Zaroori Plugins ka Parichay
**[VISUAL: Plugin cards: Git, Pipeline, Credentials Binding, Docker Pipeline, Slack Notification, SonarQube Scanner, Email Extension, Blue Ocean (optional). One line each on what they do.]**

**(Voiceover):**
Git plugin repo se code laata hai. Pipeline plugin Jenkinsfile ka poora support deta hai. Credentials Binding secrets ko surakshit tareeke se pipeline mein deta hai. Docker Pipeline Docker se build aur push mein madad karta hai. Slack aur Email plugin notifications bhejte hain. SonarQube Scanner code quality ki jaanch karta hai. Plugin Manager mein updates aur security advisories regularly dekhte rehna chahiye, aur naye plugin pehle test jenkins par try karo.

### [05:00 – 08:30] Scene 3: Notification aur Quality Gate
**[VISUAL: A pipeline's `post { failure { slackSend ... } }`. A SonarQube dashboard with a "Quality Gate: Passed/Failed". The pipeline waits for the gate with `waitForQualityGate abortPipeline: true`.]**

**(Voiceover):**
Build fail hone par team ko turant pata chalna chahiye: `post { failure { slackSend(channel:'#ci', message:"FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}") } }`. Slack token ko Jenkins credentials mein rakho. Quality gate ka matlab: SonarQube code ko bugs, vulnerabilities aur coverage ke rules par check karta hai, aur agar gate fail ho to pipeline rok do, `waitForQualityGate abortPipeline: true` se. Isse kharab code production tak jaata hi nahi.

### [08:30 – 11:30] Scene 4: Lab: Slack/Email Alert aur Docker Stage
**[VISUAL: A Jenkinsfile with a `post { failure { mail ... } }` block (email) and a Docker build stage `sh 'docker build -t shop:${BUILD_NUMBER} .'`. A failed build sends an email.]**

**(Voiceover):**
Lab: pipeline mein `post { failure { mail to: 'you@example.com', subject: "FAILED ${env.JOB_NAME}", body: "${env.BUILD_URL}" } }` jodo, aur ek build fail karao. Email ya Slack message check karo. Agar aapki repo mein Dockerfile hai, to ek `Docker` stage jodo jo `docker build -t shop:${BUILD_NUMBER} .` chalaye; Jenkins ke user ko docker group mein hona chahiye, ye Docker session mein detail se dekhenge. Aur alert mein build URL zaroor rakho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "few plugins · credentials binding · notify on failure · quality gate stops bad code".]**

**(Voiceover):**
Recap: plugins, alerts, quality gates. Ab ek aur baat: jab dus pipelines mein wahi code dohrana pade, to? Shared library.

---

# 📺 EPISODE 4: Shared Library

### [00:00 – 01:15] Scene 1: Dus Pipelines, Ek Hi Code
**[VISUAL: Ten Jenkinsfiles each containing the same 30 lines for notifications. A change request: "update message format" needs ten edits.]**

**(Voiceover):**
Aapki company mein dus services hain aur har ek ki Jenkinsfile mein notification wala wahi tees line ka code. Format badalna ho to dus jagah edit. Software mein jab code dohrane lagta hai, to ek jagah banate hain aur sabko use karne dete hain. Jenkins mein iska naam shared library hai.

### [01:15 – 05:00] Scene 2: Shared Library ka Dhancha
**[VISUAL: A repo with `vars/notifyBuild.groovy` and optionally `src/`. A Jenkins config: Manage Jenkins → System → Global Pipeline Libraries (name `ci-lib`, default version `main`, Git repo URL).]**

**(Voiceover):**
Shared library ek alag Git repo hota hai. Uske `vars/` folder mein aapki global functions, jaise `vars/notifyBuild.groovy`. Jenkins mein Global Pipeline Libraries mein library ka naam, default version aur repo URL do. Fir Jenkinsfile mein `@Library('ci-lib') _` likhkar `notifyBuild(status: 'FAILED')` bula sakte ho. Library ko version dena mat bhoolna, taaki ek badlav sab pipelines ko ek saath na tode.

### [05:00 – 08:30] Scene 3: Ek Acchi Library ke Niyam
**[VISUAL: A checklist: small focused steps, documented parameters, tests for the library, version tags (v1.0), avoid hidden secrets, review via PR.]**

**(Voiceover):**
Library mein chhote, ek kaam karne wale steps rakho. Har step ke parameters likho. Library ko bhi code ki tarah test aur review karo, PR ke saath. Version tags jaise `v1.0` use karo, aur pipelines ko explicit version se jodo. Secrets library mein mat likho, wo Jenkins credentials se aayein. Library jitni saaf hogi, naye service ke liye pipeline utni hi chhoti ho jayegi, jaise sirf paanch line ka Jenkinsfile.

### [08:30 – 11:30] Scene 4: Lab: notifyBuild Library
**[VISUAL: A new repo `ci-lib` with `vars/notifyBuild.groovy`. The Jenkins global library config. A Jenkinsfile calling `notifyBuild(...)` in `post`.]**

**(Voiceover):**
Lab: ek naya repo `ci-lib` banao, aur `vars/notifyBuild.groovy` mein:
```groovy
def call(Map cfg = [:]) {
  def status = cfg.status ?: 'UNKNOWN'
  echo "[${status}] ${env.JOB_NAME} #${env.BUILD_NUMBER} -> ${env.BUILD_URL}"
}
```
Jenkins mein library jodo, naam `ci-lib`. Apni Jenkinsfile ke top par `@Library('ci-lib') _` aur `post { always { notifyBuild(status: currentBuild.currentResult) } }`. Build chalao aur log mein message dekho. Ab ek hi jagah badal kar sab pipelines ka message badal sakte ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "vars/ functions · @Library · version tags · tests + PR review".]**

**(Voiceover):**
Recap: shared library se pipeline saaf aur reusable. Ab bade scale ki baatein: multibranch, credentials, backups, aur distributed builds ke saath agents. Agle session mein.

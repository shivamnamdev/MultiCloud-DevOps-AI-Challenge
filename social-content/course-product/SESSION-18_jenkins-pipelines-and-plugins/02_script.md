# ✍️ 02: SCRIPT — SESSION-18: Jenkins Pipelines and Plugins
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S18`
- **Focus:** Pipeline depth (parameters, environment, `options`, `when`, parallel stages, `input`, `post` conditions, `retry` and `timeout`), minimal Groovy, GitHub webhook and how to expose Jenkins safely, plugins (what to install, how to keep them safe), notifications, quality gate, a Docker stage and its risk, shared libraries
- **Builds on:** Session 04 (groups), Session 11 (ALB with HTTPS in front of a service), Session 14 (security group rules, source ranges), Session 15 (SNS topic `ops-alerts`, role), Session 16 and 16B (hooks, vault, review), Session 17 (Jenkinsfile, `post`, secrets and quotes)
- **Story position:** Zoom level 3, head office. Conveyor ab smart banti hai: kuch stations saath chalte hain, kuch sirf master par, vault khud ghanti bajata hai, foreman ke paas attachments aate hain, aur ek shared instruction binder sab conveyors ko ek jaisa rakhta hai.
- **Story words used:** foreman (Jenkins), conveyor (pipeline), station (stage), bell (webhook), vault (GitHub), attachment (plugin), instruction binder (shared library), finished unit (artifact), inspect (test), blueprint inspector (SonarQube), workbench (agent), staff (admin), guest (end user)
- **Lab project:** Atithi's `booking-service` conveyor with a parameter, parallel inspection, an approval gate, a vault bell, a notification on failure, and a shared binder.
- **Cost rule (AWS):** the lab Jenkins server is billed while it runs. Stop it after each lab day. A tunnel or load balancer used for the webhook is billed too; delete it after the lab.
- **Episodes:**
  - Episode 1: Conveyor ko Smart Banao: Parameter, Parallel aur Approval
  - Episode 2: Vault ki Ghanti: Webhook aur Surakshit Raasta
  - Episode 3: Attachments: Plugins, Alert aur Quality Gate
  - Episode 4: Shared Instruction Binder: Shared Library

---

# 📺 EPISODE 1: Conveyor ko Smart Banao

### [00:00 – 01:45] Scene 1: Ek Hi Raasta, Bees Minute
**[VISUAL: A single straight conveyor with five stations, one after another, total 20 minutes. Next frame: the same conveyor where the two inspection stations run side by side and a deploy station appears only for the master blueprint. Total 9 minutes.]**

**(Voiceover):**
Session 17 ki conveyor har station ek ke baad ek chalati hai. Atithi ki booking-service par ye bees minute leti hai. Aur har revision par, chahe wo kisi designer ka adhoora experiment ho, deploy wala station bhi chal jaata hai. Ye dono galat hain. Jo inspections ek doosre par nirbhar nahi, unhe saath chalna chahiye. Aur jo kaam sirf master blueprint ke liye hai, use sirf master par chalna chahiye. Aaj hum conveyor ko smart banate hain: kam samay, kam shor, aur koi bhi dangerous kaam bina haan ke nahi.

### [01:45 – 04:00] Scene 2: Parameter, Environment aur Options
**[VISUAL: Jenkinsfile blocks: `parameters { choice(name: 'ENV', choices: ['dev','staging'], description: 'Target') }`, `environment { APP_NAME = 'booking-service' }`, `options { timeout(time: 20, unit: 'MINUTES'); timestamps(); disableConcurrentBuilds(); buildDiscarder(logRotator(numToKeepStr: '10')) }`.]**

**(Voiceover):**
Teen blocks ek conveyor ko flexible banate hain. `parameters` mein user chunta hai kahan deploy karna hai, jaise `ENV`, dev ya staging, aur wo `params.ENV` mein aata hai. `environment` mein poori conveyor ke variables, jaise `APP_NAME`. Aur `options` mein conveyor ke niyam: `timeout` taaki atki hui build raat bhar na chale, `timestamps` taaki log mein samay dikhe, `disableConcurrentBuilds` taaki do build ek saath ek hi jagah na likhein, aur `buildDiscarder` taaki purani builds ka kachra disk na bhare. Disk bharna ek sachchi pareshani hai, jo Session 5 se jaante ho. Aur ek aur step: `retry(3)` ek aise station ke aas paas, jo kabhi kabhi network ki wajah se tootta hai, jaise dependency download.

### [04:00 – 06:10] Scene 3: when: Kaun sa Station Kab
**[VISUAL: Three `when` blocks. `when { branch 'main' }` with a note "only in a multibranch pipeline". `when { expression { env.GIT_BRANCH == 'origin/main' } }` for a single pipeline. `when { expression { params.ENV == 'staging' } }`. A small matrix showing which branch makes the deploy station light up.]**

**(Voiceover):**
`when` condition tay karti hai ki station chalega ya nahi. Ek jaal yahan pakda jaata hai. `when { branch 'main' }` sirf Multibranch Pipeline mein kaam karta hai, jo hum Session 19 mein banayenge, kyunki sirf wahan Jenkins ko branch ka naam pata hota hai. Aam pipeline job mein usi cheez ke liye `when { expression { env.GIT_BRANCH == 'origin/main' } }` likhte hain, ya parameter se: `when { expression { params.ENV == 'staging' } }`. Aur ek teesra tareeka: `when { changeRequest() }` sirf pull request ke build ke liye. Idea ek hi hai: chhote inspections har revision par, aur deploy sirf master par aur sirf jab koi haan kahe.

### [06:10 – 08:30] Scene 4: Parallel Stations aur Thoda Groovy
**[VISUAL: A `parallel` block inside a stage called `Checks`: `Unit tests` and `Lint` side by side, with `failFast true`. A Gantt chart shows total time equal to the slower one. A tiny Groovy panel: `def x = 5`, `"Build ${env.BUILD_NUMBER}"`, a `script { }` block.]**

**(Voiceover):**
Parallel stations mein do independent inspections saath chalte hain, jaise unit tests aur lint. Total samay unmein se jo dheema ho utna hota hai. `failFast true` laga do to ek fail hote hi doosra rok diya jaata hai. Parallel ke liye wahi workbench ya do workbenches chahiye, aur yaad rakho, executors jitne hain utne hi saath chalenge. Declarative pipeline ke andar kabhi kabhi Groovy chahiye hota hai, jiske liye `script { }` block hai. Groovy mein `def x = 5`, string ke andar `"Build ${env.BUILD_NUMBER}"`, aur chhote functions. Rule: pipeline mein jitna kam Groovy, utna behtar. Zyada logic ho to use ek bash parchi mein daalo, jo Session 6 mein humne test karna seekha tha, ya shared binder mein.

### [08:30 – 11:20] Scene 5: Approval Gate aur post ke Naye Shart
**[VISUAL: A deploy station guarded by an `input` step: `input message: "Deploy to staging?", ok: "Deploy", submitter: "lead-developer"` inside `agent none`, wrapped in `timeout(time: 1, unit: 'HOURS')`. A `post` block with `always`, `success`, `failure`, `unstable`, `fixed`, `changed`.]**

**(Voiceover):**
Production jaise kaam ke pehle insaan ki haan chahiye. Iske liye `input` step hai: `input message: "Deploy to staging?", ok: "Deploy"`. Aur `submitter` se tay karo ki kaun haan kah sakta hai, jaise sirf lead developer. Ek galti: `input` ko kisi workbench par chalte hue mat rakho, kyunki wo workbench ghanton rukegi. Jenkinsfile ke sabse upar `agent none` rakho, kyunki upar `agent any` ho to `input` par bhi ek workbench ruki rehti hai. `input` karo, phir jis stage ko workbench chahiye wahan `agent any` likho. Ek niyam aur: jis stage mein `parallel` ho, us par `agent` nahi chalta, har branch par likho. Aur har `input` ko ek `timeout` mein lapeto. `post` ke bhi naye shart hain: `unstable` aur `fixed`, jisme pichhli build laal thi aur ab hari hui. Alert ke liye `fixed` bahut kaam ka hai: "Atithi ki build wapas hari ho gayi."

### [11:20 – 13:55] Scene 6: Jenkinsfile mein Galti Pehle Pakdo
**[VISUAL: A terminal: `curl -s -X POST -u USER:API_TOKEN -F "jenkinsfile=<Jenkinsfile" "$JENKINS_URL/pipeline-model-converter/validate"` printing "Jenkinsfile successfully validated." and, after a typo, an error with a line number. Beside it, a workspace cleanup step `cleanWs()` in `post`.]**

**(Voiceover):**
Jenkinsfile mein ek bracket chhoot jaaye, to tabhi pata chalta hai jab build chalti hai, aur wo pehle hi second mein tootti hai. Isse bachne ke do aasan tareeke hain. Ek, Jenkins ka apna linter: `curl -X POST -F "jenkinsfile=<Jenkinsfile" $JENKINS_URL/pipeline-model-converter/validate`, jo bina build chalaye batata hai ki structure theek hai ya nahi aur kis line par galti hai. Is call ke liye Jenkins ka API token lagta hai, jo aapka personal token hai aur kabhi Jenkinsfile mein nahi likhte. Do, Replay se chhote badlaav pehle try karo. Aur ek aur ghar ki safai: build ke baad `cleanWs()` ya `post { cleanup { cleanWs() } }` workspace saaf kar deta hai, taaki agle build mein purane build ki files na bachi rahein. Session 5 ke disk bharne ka darr yahin kam hota hai.

### [13:55 – 16:30] Scene 7: Lab: Smart Conveyor
**[VISUAL: A Jenkinsfile with a choice parameter, a `Checks` stage with parallel `Unit` and `Lint`, an approval `input`, and a `Deploy` stage guarded by `when`. Stage View shows two parallel boxes and a paused "Approval" stage waiting for a button.]**

**(Voiceover):**
Lab. Apni `Jenkinsfile` mein ye jodo. Ek `ENV` choice parameter. Dhyaan: Jenkins ko parameters pehli run ke baad hi pata chalte hain, to pehli build bina parameter ke chalegi, aur uske baad `Build with Parameters` dikhega. Ek `Checks` station jisme `Unit` aur `Lint` `parallel` mein hon, `Lint` ke liye abhi `sh 'echo lint ok'` bhi chalega. Phir ek `Approval` station: `agent none` ke saath `input` aur ek ghante ka timeout. Aur ek `Deploy` station jo `when { expression { params.ENV == 'staging' } }` ke saath chale, aur abhi sirf `echo "deploying ${env.APP_NAME} to ${params.ENV}"` kare. Asli deploy hum capstone mein karenge. `Build with Parameters` se chalao, aur Stage View mein dekho ki parallel boxes saath chalte hain aur approval par conveyor ruk jaati hai. Dev chuno aur dekho ki Deploy skip hota hai.

### [16:30 – 17:00] Scene 8: Recap aur Bridge
**[VISUAL: A card: "parameters · environment · options (timeout, discard) · when (branch only in multibranch) · parallel · input outside an agent · post fixed".]**

**(Voiceover):**
Recap: smart conveyor. Ab ghanti: koi insaan Build Now na dabaye, vault khud bataye.

---

# 📺 EPISODE 2: Vault ki Ghanti

### [00:00 – 02:05] Scene 1: Build Now Dabane Wala Insaan
**[VISUAL: A designer pushes to the vault, walks across the office to the foreman's screen and clicks "Build Now". A sign hangs above: "CI is not a button".]**

**(Voiceover):**
Agar koi insaan har push ke baad jaakar Build Now dabaye, to wo CI nahi, ek rasm hai. Ek din wo bhool jaayega, aur koi bhi buggy revision chupchap master mein baitha rahega. Asli CI mein push hote hi vault ghanti bajata hai. Do tareeke hain. Poll: foreman har kuch minute mein vault se poochta hai, "kuch badla?" Aur webhook: vault khud foreman ko HTTP request bhej deta hai jab push ya pull request hota hai.

### [02:05 – 04:45] Scene 2: Poll vs Webhook
**[VISUAL: Left: the foreman calls the vault every five minutes, answered "no change" nineteen times and "yes" once. Right: the vault sends one HTTP POST at the moment of a push. A delivery tick on the vault side.]**

**(Voiceover):**
Poll mein foreman baar baar poochta hai, aur zyadatar jawab hota hai "kuch nahi badla". Bekaar traffic, aur kabhi kabhi paanch minute ki deri. Webhook mein vault ek HTTP POST bhejta hai, usi pal jab push hota hai. Tez, sasta, aur sirf zaroorat par. Ye Session 16 ke hook ka bada bhai hai: hook ek laptop ki ghanti thi, webhook poore head office ki. Ek shart hai: vault ko foreman ka URL dikhna chahiye. Agar Jenkins ek private network ya laptop par hai, to wo vault tak nahi pahunch sakta, aur tab ek tunnel ya reverse proxy chahiye.

### [04:45 – 07:35] Scene 3: Webhook Lagana
**[VISUAL: GitHub repo → Settings → Webhooks → Payload URL `https://JENKINS_HOST/github-webhook/` (with the trailing slash), content type `application/json`, event: push (and pull request). Jenkins job: "GitHub hook trigger for GITScm polling". Recent Deliveries shows a 200.]**

**(Voiceover):**
Vault ke repo Settings mein Webhooks: Payload URL `https://JENKINS_HOST/github-webhook/`, aur aakhri slash zaroori hai. Content type JSON, aur events mein push, aur pull request chahiye ho to wo bhi. Jenkins mein job par "GitHub hook trigger for GITScm polling" on karo. Pipeline job ke liye Jenkinsfile mein `triggers { githubPush() }` bhi likh sakte ho, par wo pehli build ke baad register hota hai. GitHub plugin install hona chahiye. Aur deliveries ko GitHub ka webhook page "Recent Deliveries" mein dikhata hai: 200 matlab ghanti Jenkins tak pahunchi. Wahin se "Redeliver" bhi dabaya ja sakta hai, jo debugging mein bahut kaam aata hai.

### [07:35 – 10:50] Scene 4: Ghanti ka Darwaza Surakshit Rakho
**[VISUAL: Three options drawn as doors. Door 1, port 8080 open to the world (red cross). Door 2, security group allows 443 only from the vault's published webhook ranges, with a reverse proxy and a certificate in front. Door 3, an ALB with an ACM certificate, plus a path rule `/github-webhook/` only. The request pipeline shown with the Jenkins login page hidden from the world.]**

**(Voiceover):**
Ghanti ka darwaza internet par kholne ka matlab hai ki puri duniya foreman ka login page dekh sakti hai. Saaf tareeke teen hain. Ek, Jenkins ke aage ek reverse proxy aur HTTPS, jaise Session 5B ka web server, aur security group mein sirf vault ke webhook IP ranges allow, jo GitHub apne `meta` page par chhapta hai. Do, Session 11 ka marshal: ek ALB, ACM certificate ke saath, jo sirf `/github-webhook/` ka raasta bahar deta hai, aur baaki sab band. Teen, agar Jenkins private wing mein hai, to ek chhota alag receiver ya tunnel. Ranges badal sakti hain, isliye unhe live page se dekhna. Aur webhook ke saath ek shared secret aur HTTPS lagao, jitna plugin support kare.

### [10:50 – 13:55] Scene 5: Lab: Push par Auto Build
**[VISUAL: A small change to `README.md` is committed and pushed. GitHub shows a green tick on the webhook. Jenkins starts a build within seconds. The log starts with "Started by GitHub push by ...".]**

**(Voiceover):**
Lab. Apne repo mein webhook lagao, aur Jenkins job par hook trigger on karo. Security group mein vault ke published ranges allow karo, ya agar Jenkins private hai to ek tunnel use karo. Apna IP daalne se vault ki ghanti andar nahi aayegi. Phir ek chhota change commit karo aur push karo. Kuch second mein Jenkins mein naya build shuru hoga, aur log mein "Started by GitHub push" dikhega. Agar na chale, to Session 14 ke kram se dekho: vault ke Recent Deliveries mein response code, phir security group, phir URL ka aakhri slash, phir Jenkins ka plugin. Kaam ke baad webhook delete karo aur security group ka rule hata do.

### [13:55 – 14:25] Scene 6: Recap aur Bridge
**[VISUAL: A card: "webhook > poll · /github-webhook/ with slash · expose only that path · HTTPS · check Recent Deliveries and Redeliver".]**

**(Voiceover):**
Recap: vault ki ghanti, aur uska surakshit raasta. Ab foreman ki attachments: plugins.

---

# 📺 EPISODE 3: Attachments

### [00:00 – 02:10] Scene 1: Foreman ki Taakat aur Bojh
**[VISUAL: Jenkins as a hub with spokes to many tool logos (Git, Docker, Slack, SonarQube, AWS). A caution tag on the hub: "every plugin = one more thing to update". A Plugin Manager screen showing "security warning" next to one plugin.]**

**(Voiceover):**
Jenkins ke paas hazaaron attachments, yaani plugins hain, aur wahi uski taakat hai. Par har plugin ek aur cheez hai jise update aur surakshit rakhna padta hai, aur Jenkins ke zyadatar security advisories plugins ke hote hain, core ke nahi. Isliye teen niyam. Sirf wahi plugin jo sach mein chahiye. Jo plugin ab koi nahi use karta, use hatao. Aur updates ko aadat banao: Plugin Manager mein "Updates" aur security warnings dekho. Naye plugin ya bade update ko pehle test Jenkins par try karo, aur uske liye backup chahiye, jo hum Session 19 mein banayenge.

### [02:10 – 04:50] Scene 2: Zaroori Attachments
**[VISUAL: Plugin cards with one line each: Git and GitHub, Pipeline and Stage View, Credentials Binding, Docker Pipeline, Slack Notification, Email Extension, SonarQube Scanner, Timestamper, Configuration as Code, Role-based Authorization Strategy.]**

**(Voiceover):**
Pehchaan ek ek ki. Git aur GitHub plugin vault se code laate hain aur webhook sunte hain. Pipeline plugin Jenkinsfile ka poora support deta hai, aur Stage View stations ka dashboard. Credentials Binding chaabiyan surakshit tareeke se conveyor tak pahunchata hai. Docker Pipeline Docker se build aur push mein madad karta hai. Slack aur Email plugin notifications bhejte hain. SonarQube Scanner blueprint inspector se baat karta hai. Timestamper log mein samay lagata hai. Configuration as Code aur Role-based Authorization Session 19 mein aayenge. Aur ek sabse sasta alert tareeka bina kisi plugin ke hai: Session 15 ka SNS topic. Jenkins ki workbench par ek duty badge ho jisme `sns:Publish` ki ijaazat ho, aur step mein `aws sns publish`.

### [04:50 – 07:20] Scene 3: Alert: Build Toote to Pata Chale
**[VISUAL: A pipeline's `post { failure { sh 'aws sns publish --topic-arn $TOPIC --message "FAILED: booking-service #$BUILD_NUMBER $BUILD_URL"' } fixed { ... } }`. Beside it, a phone showing the same text from the `ops-alerts` topic. A second option: `slackSend(...)`.]**

**(Voiceover):**
Build tootne par team ko turant pata chalna chahiye, aur alert mein build ka URL zaroor ho. Pehla tareeka: `post { failure { sh 'aws sns publish --topic-arn "$TOPIC" --message "FAILED: booking-service #$BUILD_NUMBER $BUILD_URL"' } }`. Yahan single quotes aur shell variables dekho, Session 17 ke jaal ke hisaab se. Message wahi `ops-alerts` topic par jaata hai jo Session 15 mein banaya tha, aur phone par aa jaata hai. Doosra tareeka Slack: `slackSend(channel: '#ci', message: "FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}")`, jisme Slack token Jenkins ki credentials mein rehta hai, aur double quotes yahan theek hain kyunki isme koi secret nahi. Aur `fixed` par ek alag, khushi wala message bhi bhejo.

### [07:20 – 09:45] Scene 4: Blueprint Inspector aur Quality Gate
**[VISUAL: A SonarQube dashboard with a Quality Gate: Passed or Failed, with bugs, vulnerabilities, coverage. A pipeline fragment: `withSonarQubeEnv('sonar') { sh 'mvn -B sonar:sonar' }`, then `timeout(time: 10, unit: 'MINUTES') { waitForQualityGate abortPipeline: true }`. A note: "SonarQube calls Jenkins back through a webhook".]**

**(Voiceover):**
Quality gate ka matlab: ek blueprint inspector, SonarQube, code ko padhta hai, bugs, vulnerabilities aur test coverage ke niyamon par check karta hai, aur ek faisla deta hai: gate pass ya fail. Conveyor mein: `withSonarQubeEnv('sonar') { sh 'mvn -B sonar:sonar' }` inspector ko code bhejta hai. Phir `waitForQualityGate abortPipeline: true`, ek timeout ke andar, conveyor ko rok deta hai jab tak faisla na aaye, aur fail hone par poori conveyor band. Dhyaan: gate ka jawab SonarQube ek webhook se Jenkins ko wapas deta hai, to wo webhook bhi lagani padti hai. Isse kharab code production tak pahunchta hi nahi. Hum DevSecOps mein inspections ko aur gehra dekhenge.

### [09:45 – 12:20] Scene 5: Docker Station aur uska Khatra
**[VISUAL: A `Docker` stage: `sh 'docker build -t booking-service:${BUILD_NUMBER} .'`. A terminal showing `sudo usermod -aG docker jenkins` and then `id jenkins` with the group `docker`. A red tag on the group: "docker group = root on this machine".]**

**(Voiceover):**
Aapki repo mein Dockerfile ho, to ek station `docker build -t booking-service:${BUILD_NUMBER} .` chala sakta hai. Iske liye `jenkins` user ko Docker chalane ki ijaazat chahiye, aur aam tareeka `sudo usermod -aG docker jenkins` hai. Yahan Session 4 ka groups wala sabak chetavni ban jaata hai. `docker` group mein hona, us machine par practically root hone ke barabar hai, kyunki Docker ke zariye koi bhi host ki files mount kar sakta hai. Isliye Jenkins ki us workbench par sirf wahi conveyors chalao jinhe aap par bharosa hai, aur secrets us par na rakho. Docker ka poora kaam hum Session 21 aur 22 mein dekhenge, to abhi sirf station ki jagah samajh lo.

### [12:20 – 14:55] Scene 6: Lab: Alert aur Gate
**[VISUAL: A Jenkinsfile with a `post { failure; fixed }` calling SNS, and an optional SonarQube stage. A test is broken, the build fails, the phone gets a message with the build link. The test is fixed, a second message arrives: "fixed".]**

**(Voiceover):**
Lab. Jenkins ki workbench ko ek duty badge do jisme sirf `sns:Publish` ho, `ops-alerts` topic par. `post { failure { ... } fixed { ... } }` mein `aws sns publish` jodo, jisme `$BUILD_URL` ho. Ek test jaan boojh kar tod do. Build fail hoga, aur phone par message aayega. Test theek karo, aur `fixed` ka message aayega. Agar aapke paas SonarQube nahi hai, to ye optional hai: ek chhota SonarQube container chalao aur `withSonarQubeEnv` jodo. Aur ek Plugin Manager ki aadat: Installed plugins mein dekho ki kitne updates baki hain, aur kaun si plugin ab kaam mein nahi. Safai: topic ya badge agar kisi aur kaam ke nahi, to hata do.

### [14:55 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "few plugins, updated · alert with build URL · fixed message · quality gate stops bad code · docker group = root · SNS needs no plugin". Then ten Jenkinsfiles with the same thirty lines fade in.]**

**(Voiceover):**
Recap: attachments, alerts, quality gate aur Docker ka khatra. Ab ek aur pareshani: dus conveyors mein wahi tees line dohrana. Iska hal ek shared instruction binder.

---

# 📺 EPISODE 4: Shared Instruction Binder

### [00:00 – 02:05] Scene 1: Dus Services, Ek Hi Code
**[VISUAL: Ten Jenkinsfiles, each with the same 30 lines for sending alerts. A request: "change the message format". Ten pull requests appear.]**

**(Voiceover):**
Atithi mein ab dus services hain: booking, payments, rooms, photos, aur baaki. Har ek ki Jenkinsfile mein alert bhejne wale wahi tees line. Message ka format badalna ho to dus jagah edit, dus pull request, aur ek jagah bhool gaye to alag alag message. Software mein jab code dohrane lagta hai, to hum use ek jagah banate hain aur sab use bulate hain. Jenkins mein iska naam shared library hai: ek instruction binder, jise saari conveyors padhti hain.

### [02:05 – 04:30] Scene 2: Binder ka Dhancha
**[VISUAL: A repo `ci-lib` with `vars/notifyBuild.groovy`, `vars/notifyBuild.txt`, `src/`, `resources/`. A Jenkins config page: Manage Jenkins → System → Global Trusted Pipeline Libraries (name `ci-lib`, default version `main`, Git source). A Jenkinsfile starting with `@Library('ci-lib@v1.0') _`.]**

**(Voiceover):**
Shared library ek alag Git repo hai, jisme `vars/` folder mein aapke global steps hote hain, jaise `vars/notifyBuild.groovy`, aur uske saath ek `.txt` mein uska dastavez. `src/` mein classes aur `resources/` mein files bhi aa sakti hain. Jenkins mein Global Trusted Pipeline Libraries mein library ka naam, default version aur repo URL do. Phir Jenkinsfile mein `@Library('ci-lib@v1.0') _` likho, aur `notifyBuild(status: 'FAILED')` ek step ki tarah bula lo. `@v1.0` ka matlab ek tay version. Binder ko version dena zaroori hai, nahi to ek badlaav ek saath saari conveyors tod sakta hai.

### [04:30 – 07:25] Scene 3: Achhe Binder ke Niyam
**[VISUAL: A checklist: small focused steps, documented parameters, defaults, tests for the library, version tags `v1.0`, pull request review, no secrets in the library, "trusted = runs outside the sandbox".]**

**(Voiceover):**
Ek achhe binder ke niyam. Chhote, ek kaam karne wale steps. Har step ke parameters aur default dastavez mein. Binder ko bhi code ki tarah test karo, kisi library test framework se, aur pull request se review karo, jaise Session 16 ka chief architect. Version tags jaise `v1.0`, aur conveyors ko tay version se jodo. Secrets library mein kabhi nahi, wo Jenkins credentials se aayein. Ek aur zaroori baat: trusted global library ka code Jenkins ke sandbox ke bahar chalta hai, matlab usme jo likha, wo foreman ki poori taakat se chalta hai. Isliye binder mein badlaav karne ki ijaazat kam logon ko aur review ke saath hi.

### [07:25 – 10:05] Scene 4: Ek Naya Service, Paanch Line ki Jenkinsfile
**[VISUAL: A new service `rooms-service` whose entire Jenkinsfile is five lines: `@Library('ci-lib@v1.0') _`, then `standardJavaPipeline(app: 'rooms-service')`. The binder does the stations, the alerts, the archive.]**

**(Voiceover):**
Binder ka asli fayda tab dikhta hai jab ek naya service aaye. Agar binder mein ek `standardJavaPipeline` step hai, jo build, test, package, archive aur alert, sab kar deta hai, to `rooms-service` ki poori Jenkinsfile paanch line ki ho sakti hai: library ka naam aur `standardJavaPipeline(app: 'rooms-service')`. Nayi service aati hai, to koi alag se conveyor nahi banata. Aur jab standard badalna ho, jaise ek naya lint station, to binder mein ek badlaav aur ek naya version. Ye wahi soch hai jo Session 6 ke functions mein aur Session 7 ke modules mein thi: ek baar likho, kai baar bulao.

### [10:05 – 13:20] Scene 5: Lab: notifyBuild Binder
**[VISUAL: A new repo `ci-lib` with `vars/notifyBuild.groovy`. The Jenkins global library config with name `ci-lib`. A Jenkinsfile calling `notifyBuild(status: currentBuild.currentResult)` in `post { always { ... } }`. The build log shows the message.]**

**(Voiceover):**
Lab. Ek naya repo `ci-lib` banao, aur `vars/notifyBuild.groovy` mein:
```groovy
def call(Map cfg = [:]) {
  def status = cfg.status ?: 'UNKNOWN'
  def line = "[${status}] ${env.JOB_NAME} #${env.BUILD_NUMBER} ${env.BUILD_URL}"
  echo line
  if (cfg.topic) {
    sh "aws sns publish --topic-arn '${cfg.topic}' --message '${line}'"
  }
}
```
Jenkins mein library jodo, naam `ci-lib`, version `main`. Tag `v1.0` lagao. Apni Jenkinsfile ke upar `@Library('ci-lib@v1.0') _` likho, aur `post { always { notifyBuild(status: currentBuild.currentResult) } }`. Build chalao aur log mein message dekho. Phir `topic` ka argument do aur phone par message dekho. Ab ek hi jagah badal kar saari conveyors ka message badal sakte ho. Is `sh` mein double quotes isliye theek hain ki isme koi secret nahi, sirf topic ka ARN aur build ki jaankari.

### [13:20 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "vars/ steps · @Library('ci-lib@v1.0') · version tags · tests + PR review · trusted = powerful · new service = five lines". Then a locked key cabinet and a stack of workbenches appear.]**

**(Voiceover):**
Recap: ek binder, saari conveyors. Ab bade head office ki baatein: har branch ki apni conveyor, chaabiyon ki locked almari, foreman ke records ka backup, aur workbenches jo bhaari kaam uthayein. Agle session mein.

---

# 📎 Student handout: Session 18 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| `parameters` | User ka chunav; `params.NAME` |
| `options` | `timeout`, `timestamps`, `disableConcurrentBuilds`, `buildDiscarder` |
| `retry`, `timeout` | Kabhi kabhi tootne wale station par; atki build ko rokne ke liye |
| `when` | `branch` sirf multibranch mein; baaki jagah `expression { env.GIT_BRANCH == 'origin/main' }` |
| `parallel` | Jo dheema, utna total samay; `failFast true` |
| Groovy | Kam se kam; `script { }`; double quotes mein Jenkins ka substitution |
| `input` | `agent none` ke saath, `timeout` ke andar, `submitter` se haan kaun |
| `post` | `always`, `success`, `failure`, `unstable`, `fixed`, `changed` |
| Webhook | `/github-webhook/` (slash), JSON, push; Recent Deliveries, Redeliver |
| Ghanti ka darwaza | HTTPS, sirf vault ke ranges ya ALB ka ek path; login page duniya ko nahi |
| Plugins | Kam se kam, update rakho, security warnings dekho, test Jenkins par pehle |
| Alert | `aws sns publish` (badge se) ya Slack; build URL zaroor |
| Quality gate | `waitForQualityGate abortPipeline: true`; SonarQube ka webhook bhi |
| Docker station | `docker` group = us machine par root jaisa |
| Shared library | `vars/`, `@Library('ci-lib@v1.0') _`, version tags, review, trusted = powerful |

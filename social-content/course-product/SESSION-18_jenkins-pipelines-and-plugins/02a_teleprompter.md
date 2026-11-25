# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-18_jenkins-pipelines-and-plugins

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,551 · **Episodes:** 4

---

# EPISODE 1: Conveyor ko Smart Banao

## Ek Hi Raasta, Bees Minute

Session 17 ki conveyor har station ek ke baad ek chalati hai. Atithi ki booking-service par ye bees minute leti hai. Aur har revision par, chahe wo kisi designer ka adhoora experiment ho, deploy wala station bhi chal jaata hai. Ye dono galat hain. Jo inspections ek doosre par nirbhar nahi, unhe saath chalna chahiye. Aur jo kaam sirf master blueprint ke liye hai, use sirf master par chalna chahiye. Aaj hum conveyor ko smart banate hain: kam samay, kam shor, aur koi bhi dangerous kaam bina haan ke nahi.

## Parameter, Environment aur Options

Teen blocks ek conveyor ko flexible banate hain. parameters mein user chunta hai kahan deploy karna hai, jaise ENV, dev ya staging, aur wo params.ENV mein aata hai. environment mein poori conveyor ke variables, jaise APP_NAME. Aur options mein conveyor ke niyam: timeout taaki atki hui build raat bhar na chale, timestamps taaki log mein samay dikhe, disableConcurrentBuilds taaki do build ek saath ek hi jagah na likhein, aur buildDiscarder taaki purani builds ka kachra disk na bhare. Disk bharna ek sachchi pareshani hai, jo Session 5 se jaante ho. Aur ek aur step: retry(3) ek aise station ke aas paas, jo kabhi kabhi network ki wajah se tootta hai, jaise dependency download.

## when: Kaun sa Station Kab

when condition tay karti hai ki station chalega ya nahi. Ek jaal yahan pakda jaata hai. when { branch 'main' } sirf Multibranch Pipeline mein kaam karta hai, jo hum Session 19 mein banayenge, kyunki sirf wahan Jenkins ko branch ka naam pata hota hai. Aam pipeline job mein usi cheez ke liye when { expression { env.GIT_BRANCH == 'origin/main' } } likhte hain, ya parameter se: when { expression { params.ENV == 'staging' } }. Aur ek teesra tareeka: when { changeRequest() } sirf pull request ke build ke liye. Idea ek hi hai: chhote inspections har revision par, aur deploy sirf master par aur sirf jab koi haan kahe.

## Parallel Stations aur Thoda Groovy

Parallel stations mein do independent inspections saath chalte hain, jaise unit tests aur lint. Total samay unmein se jo dheema ho utna hota hai. failFast true laga do to ek fail hote hi doosra rok diya jaata hai. Parallel ke liye wahi workbench ya do workbenches chahiye, aur yaad rakho, executors jitne hain utne hi saath chalenge. Declarative pipeline ke andar kabhi kabhi Groovy chahiye hota hai, jiske liye script { } block hai. Groovy mein def x = 5, string ke andar "Build ${env.BUILD_NUMBER}", aur chhote functions. Rule: pipeline mein jitna kam Groovy, utna behtar. Zyada logic ho to use ek bash parchi mein daalo, jo Session 6 mein humne test karna seekha tha, ya shared binder mein.

## Approval Gate aur post ke Naye Shart

Production jaise kaam ke pehle insaan ki haan chahiye. Iske liye input step hai: input message: "Deploy to staging?", ok: "Deploy". Aur submitter se tay karo ki kaun haan kah sakta hai, jaise sirf lead developer. Ek galti: input ko kisi workbench par chalte hue mat rakho, kyunki wo workbench ghanton rukegi. Jenkinsfile ke sabse upar agent none rakho, kyunki upar agent any ho to input par bhi ek workbench ruki rehti hai. input karo, phir jis stage ko workbench chahiye wahan agent any likho. Ek niyam aur: jis stage mein parallel ho, us par agent nahi chalta, har branch par likho. Aur har input ko ek timeout mein lapeto. post ke bhi naye shart hain: unstable aur fixed, jisme pichhli build laal thi aur ab hari hui. Alert ke liye fixed bahut kaam ka hai: "Atithi ki build wapas hari ho gayi."

## Jenkinsfile mein Galti Pehle Pakdo

Jenkinsfile mein ek bracket chhoot jaaye, to tabhi pata chalta hai jab build chalti hai, aur wo pehle hi second mein tootti hai. Isse bachne ke do aasan tareeke hain. Ek, Jenkins ka apna linter: curl -X POST -F "jenkinsfile=<Jenkinsfile" $JENKINS_URL/pipeline-model-converter/validate, jo bina build chalaye batata hai ki structure theek hai ya nahi aur kis line par galti hai. Is call ke liye Jenkins ka API token lagta hai, jo aapka personal token hai aur kabhi Jenkinsfile mein nahi likhte. Do, Replay se chhote badlaav pehle try karo. Aur ek aur ghar ki safai: build ke baad cleanWs() ya post { cleanup { cleanWs() } } workspace saaf kar deta hai, taaki agle build mein purane build ki files na bachi rahein. Session 5 ke disk bharne ka darr yahin kam hota hai.

## Lab: Smart Conveyor

Lab. Apni Jenkinsfile mein ye jodo. Ek ENV choice parameter. Dhyaan: Jenkins ko parameters pehli run ke baad hi pata chalte hain, to pehli build bina parameter ke chalegi, aur uske baad Build with Parameters dikhega. Ek Checks station jisme Unit aur Lint parallel mein hon, Lint ke liye abhi sh 'echo lint ok' bhi chalega. Phir ek Approval station: agent none ke saath input aur ek ghante ka timeout. Aur ek Deploy station jo when { expression { params.ENV == 'staging' } } ke saath chale, aur abhi sirf echo "deploying {env.APP_NAME} to {params.ENV}" kare. Asli deploy hum capstone mein karenge. Build with Parameters se chalao, aur Stage View mein dekho ki parallel boxes saath chalte hain aur approval par conveyor ruk jaati hai. Dev chuno aur dekho ki Deploy skip hota hai.

## Recap aur Bridge

Recap: smart conveyor. Ab ghanti: koi insaan Build Now na dabaye, vault khud bataye.

---

# EPISODE 2: Vault ki Ghanti

## Build Now Dabane Wala Insaan

Agar koi insaan har push ke baad jaakar Build Now dabaye, to wo CI nahi, ek rasm hai. Ek din wo bhool jaayega, aur koi bhi buggy revision chupchap master mein baitha rahega. Asli CI mein push hote hi vault ghanti bajata hai. Do tareeke hain. Poll: foreman har kuch minute mein vault se poochta hai, "kuch badla?" Aur webhook: vault khud foreman ko HTTP request bhej deta hai jab push ya pull request hota hai.

## Poll vs Webhook

Poll mein foreman baar baar poochta hai, aur zyadatar jawab hota hai "kuch nahi badla". Bekaar traffic, aur kabhi kabhi paanch minute ki deri. Webhook mein vault ek HTTP POST bhejta hai, usi pal jab push hota hai. Tez, sasta, aur sirf zaroorat par. Ye Session 16 ke hook ka bada bhai hai: hook ek laptop ki ghanti thi, webhook poore head office ki. Ek shart hai: vault ko foreman ka URL dikhna chahiye. Agar Jenkins ek private network ya laptop par hai, to wo vault tak nahi pahunch sakta, aur tab ek tunnel ya reverse proxy chahiye.

## Webhook Lagana

Vault ke repo Settings mein Webhooks: Payload URL https://JENKINS_HOST/github-webhook/, aur aakhri slash zaroori hai. Content type JSON, aur events mein push, aur pull request chahiye ho to wo bhi. Jenkins mein job par "GitHub hook trigger for GITScm polling" on karo. Pipeline job ke liye Jenkinsfile mein triggers { githubPush() } bhi likh sakte ho, par wo pehli build ke baad register hota hai. GitHub plugin install hona chahiye. Aur deliveries ko GitHub ka webhook page "Recent Deliveries" mein dikhata hai: 200 matlab ghanti Jenkins tak pahunchi. Wahin se "Redeliver" bhi dabaya ja sakta hai, jo debugging mein bahut kaam aata hai.

## Ghanti ka Darwaza Surakshit Rakho

Ghanti ka darwaza internet par kholne ka matlab hai ki puri duniya foreman ka login page dekh sakti hai. Saaf tareeke teen hain. Ek, Jenkins ke aage ek reverse proxy aur HTTPS, jaise Session 5B ka web server, aur security group mein sirf vault ke webhook IP ranges allow, jo GitHub apne meta page par chhapta hai. Do, Session 11 ka marshal: ek ALB, ACM certificate ke saath, jo sirf /github-webhook/ ka raasta bahar deta hai, aur baaki sab band. Teen, agar Jenkins private wing mein hai, to ek chhota alag receiver ya tunnel. Ranges badal sakti hain, isliye unhe live page se dekhna. Aur webhook ke saath ek shared secret aur HTTPS lagao, jitna plugin support kare.

## Lab: Push par Auto Build

Lab. Apne repo mein webhook lagao, aur Jenkins job par hook trigger on karo. Security group mein vault ke published ranges allow karo, ya agar Jenkins private hai to ek tunnel use karo. Apna IP daalne se vault ki ghanti andar nahi aayegi. Phir ek chhota change commit karo aur push karo. Kuch second mein Jenkins mein naya build shuru hoga, aur log mein "Started by GitHub push" dikhega. Agar na chale, to Session 14 ke kram se dekho: vault ke Recent Deliveries mein response code, phir security group, phir URL ka aakhri slash, phir Jenkins ka plugin. Kaam ke baad webhook delete karo aur security group ka rule hata do.

## Recap aur Bridge

Recap: vault ki ghanti, aur uska surakshit raasta. Ab foreman ki attachments: plugins.

---

# EPISODE 3: Attachments

## Foreman ki Taakat aur Bojh

Jenkins ke paas hazaaron attachments, yaani plugins hain, aur wahi uski taakat hai. Par har plugin ek aur cheez hai jise update aur surakshit rakhna padta hai, aur Jenkins ke zyadatar security advisories plugins ke hote hain, core ke nahi. Isliye teen niyam. Sirf wahi plugin jo sach mein chahiye. Jo plugin ab koi nahi use karta, use hatao. Aur updates ko aadat banao: Plugin Manager mein "Updates" aur security warnings dekho. Naye plugin ya bade update ko pehle test Jenkins par try karo, aur uske liye backup chahiye, jo hum Session 19 mein banayenge.

## Zaroori Attachments

Pehchaan ek ek ki. Git aur GitHub plugin vault se code laate hain aur webhook sunte hain. Pipeline plugin Jenkinsfile ka poora support deta hai, aur Stage View stations ka dashboard. Credentials Binding chaabiyan surakshit tareeke se conveyor tak pahunchata hai. Docker Pipeline Docker se build aur push mein madad karta hai. Slack aur Email plugin notifications bhejte hain. SonarQube Scanner blueprint inspector se baat karta hai. Timestamper log mein samay lagata hai. Configuration as Code aur Role-based Authorization Session 19 mein aayenge. Aur ek sabse sasta alert tareeka bina kisi plugin ke hai: Session 15 ka SNS topic. Jenkins ki workbench par ek duty badge ho jisme sns:Publish ki ijaazat ho, aur step mein aws sns publish.

## Alert: Build Toote to Pata Chale

Build tootne par team ko turant pata chalna chahiye, aur alert mein build ka URL zaroor ho. Pehla tareeka: post { failure { sh 'aws sns publish --topic-arn "TOPIC" --message "FAILED: booking-service #BUILD_NUMBER BUILD_URL"' } }. Yahan single quotes aur shell variables dekho, Session 17 ke jaal ke hisaab se. Message wahi ops-alerts topic par jaata hai jo Session 15 mein banaya tha, aur phone par aa jaata hai. Doosra tareeka Slack: slackSend(channel: '#ci', message: "FAILED: {env.JOB_NAME} #${env.BUILD_NUMBER}"), jisme Slack token Jenkins ki credentials mein rehta hai, aur double quotes yahan theek hain kyunki isme koi secret nahi. Aur fixed par ek alag, khushi wala message bhi bhejo.

## Blueprint Inspector aur Quality Gate

Quality gate ka matlab: ek blueprint inspector, SonarQube, code ko padhta hai, bugs, vulnerabilities aur test coverage ke niyamon par check karta hai, aur ek faisla deta hai: gate pass ya fail. Conveyor mein: withSonarQubeEnv('sonar') { sh 'mvn -B sonar:sonar' } inspector ko code bhejta hai. Phir waitForQualityGate abortPipeline: true, ek timeout ke andar, conveyor ko rok deta hai jab tak faisla na aaye, aur fail hone par poori conveyor band. Dhyaan: gate ka jawab SonarQube ek webhook se Jenkins ko wapas deta hai, to wo webhook bhi lagani padti hai. Isse kharab code production tak pahunchta hi nahi. Hum DevSecOps mein inspections ko aur gehra dekhenge.

## Docker Station aur uska Khatra

Aapki repo mein Dockerfile ho, to ek station docker build -t booking-service:${BUILD_NUMBER} . chala sakta hai. Iske liye jenkins user ko Docker chalane ki ijaazat chahiye, aur aam tareeka sudo usermod -aG docker jenkins hai. Yahan Session 4 ka groups wala sabak chetavni ban jaata hai. docker group mein hona, us machine par practically root hone ke barabar hai, kyunki Docker ke zariye koi bhi host ki files mount kar sakta hai. Isliye Jenkins ki us workbench par sirf wahi conveyors chalao jinhe aap par bharosa hai, aur secrets us par na rakho. Docker ka poora kaam hum Session 21 aur 22 mein dekhenge, to abhi sirf station ki jagah samajh lo.

## Lab: Alert aur Gate

Lab. Jenkins ki workbench ko ek duty badge do jisme sirf sns:Publish ho, ops-alerts topic par. post { failure { ... } fixed { ... } } mein aws sns publish jodo, jisme $BUILD_URL ho. Ek test jaan boojh kar tod do. Build fail hoga, aur phone par message aayega. Test theek karo, aur fixed ka message aayega. Agar aapke paas SonarQube nahi hai, to ye optional hai: ek chhota SonarQube container chalao aur withSonarQubeEnv jodo. Aur ek Plugin Manager ki aadat: Installed plugins mein dekho ki kitne updates baki hain, aur kaun si plugin ab kaam mein nahi. Safai: topic ya badge agar kisi aur kaam ke nahi, to hata do.

## Recap aur Bridge

Recap: attachments, alerts, quality gate aur Docker ka khatra. Ab ek aur pareshani: dus conveyors mein wahi tees line dohrana. Iska hal ek shared instruction binder.

---

# EPISODE 4: Shared Instruction Binder

## Dus Services, Ek Hi Code

Atithi mein ab dus services hain: booking, payments, rooms, photos, aur baaki. Har ek ki Jenkinsfile mein alert bhejne wale wahi tees line. Message ka format badalna ho to dus jagah edit, dus pull request, aur ek jagah bhool gaye to alag alag message. Software mein jab code dohrane lagta hai, to hum use ek jagah banate hain aur sab use bulate hain. Jenkins mein iska naam shared library hai: ek instruction binder, jise saari conveyors padhti hain.

## Binder ka Dhancha

Shared library ek alag Git repo hai, jisme vars/ folder mein aapke global steps hote hain, jaise vars/notifyBuild.groovy, aur uske saath ek .txt mein uska dastavez. src/ mein classes aur resources/ mein files bhi aa sakti hain. Jenkins mein Global Trusted Pipeline Libraries mein library ka naam, default version aur repo URL do. Phir Jenkinsfile mein @Library('ci-lib@v1.0') _ likho, aur notifyBuild(status: 'FAILED') ek step ki tarah bula lo. @v1.0 ka matlab ek tay version. Binder ko version dena zaroori hai, nahi to ek badlaav ek saath saari conveyors tod sakta hai.

## Achhe Binder ke Niyam

Ek achhe binder ke niyam. Chhote, ek kaam karne wale steps. Har step ke parameters aur default dastavez mein. Binder ko bhi code ki tarah test karo, kisi library test framework se, aur pull request se review karo, jaise Session 16 ka chief architect. Version tags jaise v1.0, aur conveyors ko tay version se jodo. Secrets library mein kabhi nahi, wo Jenkins credentials se aayein. Ek aur zaroori baat: trusted global library ka code Jenkins ke sandbox ke bahar chalta hai, matlab usme jo likha, wo foreman ki poori taakat se chalta hai. Isliye binder mein badlaav karne ki ijaazat kam logon ko aur review ke saath hi.

## Ek Naya Service, Paanch Line ki Jenkinsfile

Binder ka asli fayda tab dikhta hai jab ek naya service aaye. Agar binder mein ek standardJavaPipeline step hai, jo build, test, package, archive aur alert, sab kar deta hai, to rooms-service ki poori Jenkinsfile paanch line ki ho sakti hai: library ka naam aur standardJavaPipeline(app: 'rooms-service'). Nayi service aati hai, to koi alag se conveyor nahi banata. Aur jab standard badalna ho, jaise ek naya lint station, to binder mein ek badlaav aur ek naya version. Ye wahi soch hai jo Session 6 ke functions mein aur Session 7 ke modules mein thi: ek baar likho, kai baar bulao.

## Lab: notifyBuild Binder

Lab. Ek naya repo ci-lib banao, aur vars/notifyBuild.groovy mein:

Jenkins mein library jodo, naam ci-lib, version main. Tag v1.0 lagao. Apni Jenkinsfile ke upar @Library('ci-lib@v1.0') _ likho, aur post { always { notifyBuild(status: currentBuild.currentResult) } }. Build chalao aur log mein message dekho. Phir topic ka argument do aur phone par message dekho. Ab ek hi jagah badal kar saari conveyors ka message badal sakte ho. Is sh mein double quotes isliye theek hain ki isme koi secret nahi, sirf topic ka ARN aur build ki jaankari.

## Recap aur Bridge

Recap: ek binder, saari conveyors. Ab bade head office ki baatein: har branch ki apni conveyor, chaabiyon ki locked almari, foreman ke records ka backup, aur workbenches jo bhaari kaam uthayein. Agle session mein.

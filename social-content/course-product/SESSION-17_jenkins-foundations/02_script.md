# ✍️ 02: SCRIPT — SESSION-17: Jenkins Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S17`
- **Focus:** Continuous Integration as a habit, Jenkins controller and agents, installing Jenkins on a Linux server (service user, `JENKINS_HOME`, port, first unlock), freestyle job, exit codes, parameters, Git source, Maven build lifecycle, test reports, archiving the finished unit, the first Jenkinsfile (declarative pipeline), `post`, "Pipeline script from SCM"
- **Builds on:** Session 04 (service users, ownership, SSH key), Session 05 (`systemctl`, `journalctl`, `ss`), Session 06 (exit codes), Session 08 (EC2, security group, stop vs terminate), Session 14 (do not open admin ports to the world), Session 16 and 16B (Git, hooks, the vault, pull request review)
- **Story position:** Zoom level 3, head office. Designers aur vault ke baad ab workshop aati hai. Ek foreman hire hota hai, jo har nayi revision ko fabricate karta hai, inspect karta hai, aur finished unit shelf par rakhta hai.
- **Story words used:** foreman (Jenkins), conveyor (pipeline), station (stage), fabricate (build), inspect (test), finished unit (artifact), blueprint (code), vault (GitHub), workbench (agent), bell (webhook, preview), guest (end user), staff (admin)
- **Lab project:** Atithi's `booking-service`, a small Java service built with Maven: first with a freestyle job, then with a `Jenkinsfile` kept in the vault beside the blueprint.
- **Cost rule (AWS):** the Jenkins server is a running building and is billed while it runs. Stop (do not terminate) it at the end of each lab day, and terminate it when the course is done. Do not open port 8080 to the world.
- **Episodes:**
  - Episode 1: Foreman kyun: Continuous Integration ka Matlab
  - Episode 2: Foreman ko Hire Karo: Install aur Pehla Job
  - Episode 3: Blueprint se Finished Unit: Git aur Maven
  - Episode 4: Conveyor ke Nirdesh: Pehla Jenkinsfile

---

# 📺 EPISODE 1: Foreman kyun

### [00:00 – 02:40] Scene 1: Friday Shaam ki Integration
**[VISUAL: Five designers each work for two weeks on their own copy of the booking blueprint. On release Friday, the copies are merged. A giant red cloud of conflicts, a broken room-booking screen, and a clock at 6 PM.]**

**(Voiceover):**
Atithi ke paanch designers do hafte tak apni apni copy par booking site ka kaam karte hain. Release ki Friday ko sab ki copies milaai jaati hain. Ek ka naya rate table, doosre ka naya payment button, teesre ka naya form. Kuch bhi saath nahi chalta, aur Friday ki shaam ek bhi booking test nahi ho pati. Session 16 mein humne register aur branches seekhe, jo is mushkil ko sambhalte hain. Par ek aur aadat chahiye: kaam ko roz, balki din mein kai baar, milao, aur har baar check karo ki sab saath chalta hai. Is aadat ka naam Continuous Integration hai.

### [02:40 – 05:35] Scene 2: CI ka Matlab: Roz Milao, Roz Jaancho
**[VISUAL: A loop: designer commits → vault → bell → workshop fetches the new revision → fabricates the unit → inspector tests → result on the team's screen. A badge: "minutes, not days".]**

**(Voiceover):**
CI ka matlab hai: designer apni revision vault mein bhejta hai, aur workshop turant use uthati hai, finished unit banati hai, inspection karti hai, aur team ko batati hai ki sab theek hai ya kuch toota. Teen faayde. Galtiyan jaldi pakdi jaati hain, jab unka kaaran chhota aur taaza hota hai, kyunki ek hi change ki jaanch hai, paanch hafton ki nahi. Fabrication har baar ek jaise saaf mahaul mein hoti hai, "mere laptop par to chal raha tha" wali baat nahi. Aur team ko release se darr nahi lagta. CI ek tool ka naam nahi, ek aadat ka naam hai. Jenkins uske liye ek bahut purana aur bharosemand tool hai.

### [05:35 – 08:15] Scene 3: Kaun Kya Kaam Karta Hai
**[VISUAL: A workshop floor plan. A foreman's office (controller) with a schedule board and a plugin shelf. Workbenches (agents) with a "Java" sign. A row of jobs waiting on a board. A caption: "controller plans, workbenches build".]**

**(Voiceover):**
Jenkins ek open source automation server hai, Java mein bana hua. Uska controller foreman ka daftar hai: wo UI dikhata hai, jobs ko schedule karta hai, aur plugins sambhalta hai. Asli fabrication workbenches par hoti hai, jinhe agents kehte hain. Chhote setup mein foreman khud bhi kaam kar leta hai, par asli workshop mein foreman sirf plan banata hai aur workbenches kaam karti hain. Isse hum Session 19 mein dekhenge. Jenkins ki taakat uske hazaaron plugins hain, yaani foreman ki attachments. Par har attachment ek aur cheez hai jise update aur surakshit rakhna padta hai. Isiliye jo zaroori ho wahi lagao.

### [08:15 – 10:50] Scene 4: Local Hook se Bell tak
**[VISUAL: Left: the pre-push hook from Session 16 running tests on one designer's laptop. Right: the vault ringing a bell, and the workshop starting a build for everyone. A line between them: "the same idea, shared".]**

**(Voiceover):**
Session 16 ke hooks yaad hain? Designer apni laptop par ek `pre-push` hook se tests chala sakta tha. Wo ek local jaancha hai: sirf us designer ke liye, aur wo use band bhi kar sakta hai. CI uska shared roop hai. Vault mein revision aate hi vault workshop ki ghanti bajata hai, aur foreman sab ke liye ek hi tarah ki jaancha chalata hai, jise koi chhod nahi sakta. Is ghanti ko webhook kehte hain, aur wo hum Session 18 mein jodenge. Aaj ke liye bas itna: pehle haath se foreman ko kaam dena seekhenge, phir use ghanti se jodenge.

### [10:50 – 13:35] Scene 5: Lab: Foreman ka Daftar Taiyaar Karo
**[VISUAL: A checklist: Ubuntu server (an EC2 building or a local VM), at least 2 GB RAM, Java installed, `java -version`, Git, a security group with 8080 open only to "my IP", and a Name tag `jenkins-lab`.]**

**(Voiceover):**
Lab ki taiyaari. Ek Ubuntu building lo, EC2 ya apni VM, kam se kam do GB RAM, jaise `t3.small`. Naam ka tag `jenkins-lab` lagao, Session 8 ki tarah. `sudo apt update && sudo apt install -y openjdk-17-jre git maven` chalao, aur `java -version` aur `mvn -v` se check karo. Jenkins ke supported Java versions release ke saath badalte hain, isliye install se pehle official documentation dekh lo. Jenkins ka default port 8080 hai. Security group mein 8080 sirf apne IP se kholo, poori duniya ke liye nahi. Session 14 ka niyam yahan bhi: jo darwaza staff ke liye hai, use sabke liye mat kholo.

### [13:35 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "CI = merge often + auto fabricate + inspect · hook = local, CI = shared · controller plans, workbenches build · plugins = attachments".]**

**(Voiceover):**
Recap: CI ek aadat hai, Jenkins uska ek tool. Foreman ka daftar aur workbenches. Ab foreman ko hire karte hain: install, pehla unlock aur pehla job.

---

# 📺 EPISODE 2: Foreman ko Hire Karo

### [00:00 – 02:00] Scene 1: Pandrah Minute mein Workshop
**[VISUAL: A timer from 15:00 counting down while a Jenkins login screen appears. A key icon labelled "initial admin password". A small note: "this server can reach your code and your keys".]**

**(Voiceover):**
Ek CI server banane mein kitna samay lagta hai? Aaj ke tools ke saath, paandrah minute. Hum Jenkins ko Ubuntu par install karenge, uska pehla login karenge, aur ek simple job chalayenge. Lekin pehle ek chetavni. Jenkins aisa server hai jo aapka code, cloud ki chaabiyan aur production tak ka raasta chhoo sakta hai. Agar foreman ke daftar ka darwaza kamzor raha, to poora head office khule mein hai. Isliye install ke saath hi security ki soch shuru hoti hai, baad mein nahi.

### [02:00 – 04:25] Scene 2: Install: Official Raaste se
**[VISUAL: Terminal. Add the Jenkins package repository and its signing key as shown in the official docs, `sudo apt install jenkins`, `sudo systemctl enable --now jenkins`, `systemctl status jenkins`, `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`. Browser: Unlock Jenkins at `http://SERVER_IP:8080`.]**

**(Voiceover):**
Install ke liye Jenkins ki official documentation ke commands use karo, kyunki repository aur signing key ke details badalte rehte hain. Install ke baad `sudo systemctl enable --now jenkins`, aur `systemctl status jenkins` se dekho ki chal raha hai. Pehla password `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` mein hota hai. Browser mein `http://SERVER_IP:8080` kholo, password daalo, "Install suggested plugins" chuno, aur apna admin user banao. Uske baad wo pehla password dobara kaam nahi aata, apna user istemaal karo. Aur agar page nahi khulta, to Session 5 ka kram: `ss -tlnp | grep 8080` se service sun rahi hai ya nahi, phir security group.

### [04:25 – 07:20] Scene 3: Jenkins ek Service Hai, aur ek User
**[VISUAL: `ps -o user,pid,cmd -C java` showing user `jenkins`. `ls -ld /var/lib/jenkins` showing owner `jenkins`. `journalctl -u jenkins -n 20`. A tree of `JENKINS_HOME` with `jobs/`, `plugins/`, `secrets/`, `workspace/`.]**

**(Voiceover):**
Ab dekho ki Jenkins asli mein hai kya. Wo ek systemd service hai, bilkul Session 5 ki `apache` ya `nginx` ki tarah. Aur wo `jenkins` naam ke ek system user ke naam par chalta hai, jo Session 4 ka uniformed service staff hai: ek hi kaam, koi login nahi. Uska ghar `/var/lib/jenkins` hai, jise `JENKINS_HOME` kehte hain, aur uski ownership `jenkins` ke paas hai. Saare jobs, plugins, users aur chaabiyan wahin rehti hain. Iska ek seedha matlab: jab Jenkins koi command chalata hai, wo `jenkins` user ki tarah chalti hai. Agar kisi tool ka PATH ya permission `jenkins` ke liye theek nahi, to haath se `sudo -u jenkins mvn -v` chalakar dekho. Aur Jenkins ke logs `journalctl -u jenkins` mein hain.

### [07:20 – 09:50] Scene 4: Job aur Freestyle Job
**[VISUAL: Jenkins "New Item" → Freestyle project `hello-job`. An "Execute shell" build step with `echo "Hello from Jenkins"` and `date`. Build Now, a blue ball, Console Output, a build history list with build numbers.]**

**(Voiceover):**
Job foreman ko diya hua ek kaam ka vivaran hai. Freestyle job sabse saral hai: ek form mein aap batate ho ki code kahan se aayega aur kaun si commands chalani hain. "Execute shell" step mein `echo "Hello from Jenkins"` aur `date`. "Build Now" dabao, aur Console Output mein dekho. Har run ko ek build number milta hai, aur Jenkins uska log aur result yaad rakhta hai. Nila ball matlab pass, laal ball matlab fail. Har build ka apna workspace folder hota hai, `JENKINS_HOME/workspace/hello-job`, jahan code utarta hai. Freestyle seekhne ke liye achha hai, par ek kamzori jaldi dikhegi, jo Episode 4 mein hal hogi.

### [09:50 – 12:40] Scene 5: Exit Code aur Parameter
**[VISUAL: A job with a string parameter `NAME`. Shell step `echo "Hello, $NAME"`. "Build with Parameters" asks for a value. A second build with `exit 1` turns the ball red. A card: "exit 0 = pass, anything else = fail".]**

**(Voiceover):**
Ek job ko ek hi kaam mein bandh kar rakhna zaroori nahi. "This project is parameterised" mein ek String parameter `NAME` jodo, aur shell step mein `echo "Hello, $NAME"` likho. "Build with Parameters" se chalao, aur har baar alag naam do. Ab ek build jaan boojh kar fail karo, `exit 1` likhkar, aur dekho ki ball laal ho gaya. Session 6 ka sabak yahan seedhe kaam aata hai: Jenkins shell step ke exit code ko dekhta hai. Zero matlab pass, koi bhi aur number matlab fail. Isliye hamari bash parchiyan jo galti par non-zero exit karti hain, wahi Jenkins ko batati hain ki kuch toota. Aur `set -e` ya `set -euo pipefail` ki aadat yahan kaam aati hai.

### [12:40 – 15:00] Scene 6: Lab: Pehla Job aur Parameter
**[VISUAL: Terminal on the Jenkins server and the browser side by side. Jenkins job `hello-job` with parameter `NAME`, shell step `echo "Hello, $NAME"; hostname; whoami`. The log shows the hostname of the server and the user `jenkins`. Then a failing step turns red.]**

**(Voiceover):**
Lab. Ek freestyle job `hello-job` banao, parameter `NAME`, aur shell step mein `echo "Hello, $NAME"; hostname; whoami`. "Build with Parameters" se chalao. Log mein server ka hostname dikhega, aur `whoami` ka jawab `jenkins` hoga, jo Scene 3 ki baat pakki karta hai. Ab step mein `ls /root` jodo aur dekho ki kyun fail hota hai: `jenkins` user ko wahan ki ijaazat nahi, aur wahi least privilege hai. Aakhir mein ek build `exit 1` se fail karo aur Console Output padhna seekho: sabse neeche se, ek line upar. Aur kaam ke baad building ko stop kar do, terminate nahi.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "install from official docs · unlock once · jenkins user + JENKINS_HOME · freestyle job · exit 0 = pass · stop the building after the lab".]**

**(Voiceover):**
Recap: Jenkins install, jenkins user, freestyle job aur exit code. Ab asli kaam: vault se blueprint uthakar uski finished unit banana.

---

# 📺 EPISODE 3: Blueprint se Finished Unit

### [00:00 – 02:20] Scene 1: Java Service Banti Kaise Hai
**[VISUAL: Java source files → compile → test → package into `booking-service.jar`. A gear labelled "Maven" drives each step. Beside it, a small card for Python: "pip install, pytest" with a note "same conveyor, different tools".]**

**(Voiceover):**
Atithi ki `booking-service` Java mein hai. Java service ko chalne layak banana ek chhota kaam nahi: code compile karo, tests chalao, dependencies jodo, aur ek `.jar` file banao. Maven ye sab ek standard tareeke se karta hai, aur ek hi file se, `pom.xml`. Jenkins aur Maven ki jodi Java projects mein bahut aam hai. Agar aapka project Python mein hai, to wahi conveyor chalegi: `pip install -r requirements.txt`, phir `pytest`, jo humne Session 7 mein seekha tha. Tool alag, conveyor wahi. Isliye is session ki jo baatein Maven ke naam par hain, unhe apne tool par laagu karna aasaan hai.

### [02:20 – 04:45] Scene 2: pom.xml aur Lifecycle
**[VISUAL: A trimmed `pom.xml` with groupId, artifactId, version, one dependency and a JUnit test dependency. A lifecycle ribbon: validate → compile → test → package → verify. Command `mvn -B clean package`. A `target/` folder with `booking-service-1.0.jar` and `surefire-reports/`.]**

**(Voiceover):**
`pom.xml` mein project ka naam, version aur dependencies likhi hoti hain. Maven dependencies khud download karta hai. Build ka ek tay kram hai, jise lifecycle kehte hain: compile, test, package aur aage. `mvn clean package` purane build ko saaf karta hai, aur phir naya `.jar` banata hai, aur agar koi test fail ho to wahin ruk jaata hai. Output `target/` folder mein milta hai: `.jar` aur `surefire-reports/`, jisme har test ka result hota hai. `-B` ka matlab batch mode, jisme progress ke bar nahi aate aur log saaf rehta hai. `-DskipTests` ek option hai, par CI mein tests chhod dena aam taur par buri aadat hai.

### [04:45 – 08:05] Scene 3: Git se Code, Credentials se Chaabi
**[VISUAL: Job config: Source Code Management → Git, repository URL, credentials dropdown, branch `*/main`. A private repo with a read-only deploy key whose public half sits on the vault and the private half in Jenkins Credentials. A red cross over a token typed into the URL.]**

**(Voiceover):**
Job mein Source Code Management mein Git chuno aur vault ka URL aur branch do. Agar repository private hai, to Jenkins ko ek pass chahiye. Do saaf tareeke hain. Ek, personal access token, jise Credentials mein rakho. Do, ek deploy key: ek SSH key ka joda, jisme public hissa vault par read-only lagta hai, aur private hissa Jenkins ke Credentials mein. Ye Session 4 ka SSH key ka hi dusra roop hai. Dono mein ek rule: chaabi ya token URL mein ya Jenkinsfile mein kabhi nahi likhte. Aur ek chhoti baat: Jenkins ko ye bhi tay karna padta hai ki kab check kare. Abhi ke liye "Poll SCM" mein `H/5 * * * *`, jiska matlab hai har paanch minute mein, par `H` ek hash hai jo saari jobs ko ek hi second par ek saath tootne se rokta hai. Asli ghanti, webhook, Session 18 mein.

### [08:05 – 10:40] Scene 4: Inspection ki Report aur Finished Unit
**[VISUAL: A Jenkins build page with a "Test Result" trend chart: green bars, one yellow bar. Post-build actions: "Publish JUnit test result report" with `target/surefire-reports/*.xml` and "Archive the artifacts" with `target/*.jar`. A fingerprint icon next to the jar.]**

**(Voiceover):**
Build ka mat sirf "pass ya fail" nahi hota. Jenkins ek JUnit report utha sakta hai: `target/surefire-reports/*.xml`. Isse build page par test result ka graph aata hai, aur kaun sa test kab tootna shuru hua, ye dikhta hai. Ek nuance: agar report publish ho par kuch tests fail hon, aur build ko `-Dmaven.test.failure.ignore` ke saath chalayein, to Jenkins use peela maanta hai, yaani unstable. Seedhe Maven fail ho jaaye, to laal. Aur finished unit ko shelf par rakhne ke liye "Archive the artifacts" mein `target/*.jar`. Fingerprint on rakho, taaki baad mein pata chale ki ye jar kis build se bani thi. Workspace to kabhi bhi saaf ho sakta hai, finished unit nahi.

### [10:40 – 13:20] Scene 5: Lab: booking-service ki Pehli Fabrication
**[VISUAL: A sample Maven repo with two unit tests. Job `booking-build`: Git source, shell step `mvn -B clean package`, JUnit report, archive `target/*.jar`. The first build is blue. A test is changed to `assertEquals(3, nights)`, the build turns red, the log shows the failing test name and line.]**

**(Voiceover):**
Lab. Vault par ek chhota Maven repo lo, jisme kuch unit tests hon, jaise ek function jo check-in aur check-out se raaton ki ginti nikaale. Agar aapke paas apna nahi hai, to ek sample repo fork karo, jaise Session 16B mein fork karna seekha tha. Freestyle job `booking-build` banao, Git source, aur shell step `mvn -B clean package`. Post-build mein JUnit report aur `target/*.jar` archive karo. Pehli build chalao, jar dekho. Phir ek test jaan boojh kar tod do: `assertEquals(3, nights)` ko galat value de do, push karo, aur build dobara chalao. Build laal hoga, aur Console Output mein test ka naam aur line likhi hogi. Isi tarah CI aapki galti commit ke turant baad pakadta hai.

### [13:20 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "pom.xml + lifecycle · target/ (jar, reports) · Git source + deploy key · JUnit trend · archive + fingerprint · red build tells you the line".]**

**(Voiceover):**
Recap: Git se blueprint, Maven se finished unit, aur inspection ki report. Par ek kamzori bachi hai: ye saari settings foreman ke daftar ke form mein chhupi hain. Agle episode mein hum conveyor ko blueprint ke saath hi rakhna seekhenge.

---

# 📺 EPISODE 4: Conveyor ke Nirdesh

### [00:00 – 02:10] Scene 1: Kisi ne Ek Checkbox Badal Diya
**[VISUAL: A freestyle job with twenty settings. Someone un-ticks one box; the next build breaks. Another person asks "who changed it, and when?" and the history screen is empty.]**

**(Voiceover):**
Ek subah build toot gaya. Kal tak theek tha. Pata chala ki kisi ne freestyle job ka ek checkbox badal diya. Kisne, kab aur kyun, kuch nahi pata, kyunki wo form mein chhupa tha. Aur agar foreman ka server kharab ho jaaye, to ye saari settings bhi gayi. Hal: conveyor ke nirdesh blueprint ke saath hi rakho. Ek file, `Jenkinsfile`, jo vault mein rehti hai. Uska poora register hota hai, uski chief architect review kar sakta hai, aur galti hone par ek purani revision par wapas jaa sakte ho. Session 16 ki saari aadatein ab conveyor par bhi laagu hoti hain.

### [02:10 – 04:30] Scene 2: Declarative Pipeline ka Dhancha
**[VISUAL: A Jenkinsfile on screen. `pipeline { agent any; options {...}; stages { stage('Build') { steps { sh '...' } } ... }; post { always {...}; failure {...} } }`. Each block is highlighted in turn with a one-word label.]**

**(Voiceover):**
Declarative pipeline ka dhancha seekho. Sabse bahar `pipeline`. Uske andar `agent`, jo batata hai kaun si workbench par chalega. `options` mein timeout jaise settings. `stages` mein kai `stage`, yaani stations, aur har station ke andar `steps`, jo asli commands hain, jaise `sh 'mvn -B test'`. Aur aakhir mein `post`, jo build ke ant mein chalta hai: `always`, `success`, `failure`. Ek aur blocks hain: `environment` variables ke liye, aur `parameters`, jaise freestyle ka parameter. Ek aadat: har stage ka naam aisa rakho ki sirf naam padhkar pata chale ki kahan atka. Isse "Build" ya "Test" laal hota hai, to aapko sidha pata hai ki fabrication mein dikkat hai ya inspection mein.

### [04:30 – 06:40] Scene 3: Pipeline Job, aur Jenkinsfile Vault Se
**[VISUAL: Jenkins "New Item → Pipeline", Definition "Pipeline script from SCM", SCM Git, repo URL, branch, Script Path `Jenkinsfile`. Beside it, the `Jenkinsfile` sitting in the repo root next to `pom.xml`. A "Replay" button and the Pipeline Syntax snippet generator are pointed to.]**

**(Voiceover):**
Ab pipeline job banao, aur Definition mein "Pipeline script from SCM" chuno. Vault ka URL, branch, aur Script Path `Jenkinsfile` do. Is tarah Jenkinsfile Jenkins ke form mein nahi, repo ke andar rehti hai, `pom.xml` ke bagal mein. Jenkins har build se pehle use vault se uthata hai. Do madadgar cheezein. Pipeline Syntax ka snippet generator: aap form mein kuch chuno, aur wo ek step ka sahi code bana deta hai. Aur Replay: purane build ko thoda badal kar dobara chalane ka tareeka, bina commit kiye. Replay sirf try karne ke liye hai. Jo kaam kare, use Jenkinsfile mein commit karo.

### [06:40 – 09:05] Scene 4: Secrets aur Quotes ka Jaal
**[VISUAL: Two snippets. 1: `sh 'echo $TOKEN'` (single quotes, the shell expands it). 2: `sh "echo $TOKEN"` (double quotes, Jenkins interpolates and the secret leaks into the log, with a warning). A line with `withCredentials` is shown instead.]**

**(Voiceover):**
Pipeline mein ek chhota jaal hai, jise sab seekhte waqt pakadte hain. Jenkinsfile Groovy mein hai, aur Groovy mein double quote wali string ke andar `$` ka matlab Jenkins ka apna substitution hota hai. Isliye `sh "echo $TOKEN"` mein Jenkins khud secret ko command mein likh deta hai, aur wo log mein aa sakta hai. Single quote mein, `sh 'echo $TOKEN'`, Jenkins kuch nahi badalta aur shell variable ko sambhalta hai. Isliye secrets hamesha single quotes ke saath, aur `credentials()` ya `withCredentials` se lo, plain text mein kabhi nahi. Ye hum Session 19 mein Jenkins ki security ke saath poori tarah dekhenge. Aaj bas yaad rakho: secret ek, quote ek, aur kabhi print nahi.

### [09:05 – 12:10] Scene 5: Lab: Build, Test, Package aur Archive
**[VISUAL: The `Jenkinsfile` in the repo root. Stage View: Build, Test, Package all green, with timing. A failing test turns the Test stage red; Package is skipped (grey). Archived jar visible on the build page.]**

**(Voiceover):**
Lab. Apne `booking-service` repo ke root mein ye `Jenkinsfile` rakho:
```groovy
pipeline {
  agent any
  options { timeout(time: 15, unit: 'MINUTES') }
  stages {
    stage('Build')   { steps { sh 'mvn -B -DskipTests clean compile' } }
    stage('Test')    { steps { sh 'mvn -B test' } }
    stage('Package') { steps { sh 'mvn -B -DskipTests package' } }
  }
  post {
    always  { junit allowEmptyResults: true, testResults: 'target/surefire-reports/*.xml' }
    success { archiveArtifacts artifacts: 'target/*.jar', fingerprint: true }
    failure { echo 'Build failed. Look at the red stage first.' }
  }
}
```
Commit karke vault mein push karo. Pipeline job banao, "Pipeline script from SCM" ke saath, aur chalao. Stage View mein har station dekho. Phir ek test tod kar dekho: Test laal hoga, Package grey, aur `post failure` ka message chalega. Ek test ko theek karke push karo aur dekho ki naya build hara hota hai.

### [12:10 – 14:15] Scene 6: Pull Request ke Saath Jenkinsfile
**[VISUAL: A pull request that changes `Jenkinsfile` to add a lint stage. The chief architect reviews it in the vault like any other file. A merged commit and a build using the new conveyor. A history list of `Jenkinsfile` changes with authors and dates.]**

**(Voiceover):**
Ab Jenkinsfile bhi blueprint ka hissa hai, to wahi niyam. Ek nayi station jodni ho, jaise lint, to ek branch banao, `Jenkinsfile` badlo, aur pull request kholo. Chief architect use review karta hai, jaise kisi bhi file ko. Merge hone ke baad agla build nayi conveyor se chalega. Aur agar nayi station ne sab toda, to Session 16 ki aadat: `git revert` se purani halat wapas. Har badlaav ka register hai: kisne, kab, kyun. Ye wahi cheez hai jo freestyle ke form mein nahi thi. Isi ko pipeline as code kehte hain, aur ye agle sessions ki neev hai.

### [14:15 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "Jenkinsfile lives in the vault · pipeline / agent / stages / post · Script from SCM · single quotes for secrets · change it by pull request". Then a vault building with a bell on its roof fades in.]**

**(Voiceover):**
Recap: Jenkinsfile, declarative pipeline, stages aur post. Conveyor ab blueprint ke saath rehti hai, aur uske badlaav bhi review hote hain. Par abhi bhi koi insaan Build Now dabata hai ya Jenkins har paanch minute mein poochta hai. Agle session mein vault khud ghanti bajayega, aur conveyor mein parallel stations, plugins aur ek shared binder aayenge.

---

# 📎 Student handout: Session 17 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| CI | Roz milao, har baar automatic build aur test, turant jawab |
| Hook vs CI | Hook = local, chhod sakte ho. CI = shared, sab par laagu |
| Controller / agent | Foreman plan karta hai; workbench kaam karti hai |
| Install | Official docs ke commands; `systemctl status jenkins`; `initialAdminPassword` |
| Jenkins ka user | `jenkins` system user; `JENKINS_HOME` = `/var/lib/jenkins`; logs `journalctl -u jenkins` |
| Port | 8080, sirf apne IP se; `ss -tlnp | grep 8080` |
| Freestyle job | Form mein setting; build number; workspace; neela = pass, laal = fail |
| Exit code | 0 = pass, baaki sab fail; `set -e` |
| Poll SCM | `H/5 * * * *`; asli ghanti webhook, Session 18 |
| Maven | `pom.xml`; `mvn -B clean package`; `target/*.jar`; `surefire-reports/` |
| JUnit report | Trend graph; test fail + ignore = unstable (peela) |
| Finished unit | `archiveArtifacts` + `fingerprint` |
| Jenkinsfile | `pipeline` / `agent` / `stages` / `steps` / `post` |
| Script from SCM | Jenkinsfile repo mein, `pom.xml` ke bagal mein |
| Secrets | Single quotes; `credentials()` ya `withCredentials`; kabhi print nahi |
| Badlaav | Branch, pull request, review, revert; Replay sirf try karne ke liye |
| Safai | Building stop (terminate nahi); kaam ke baad poori terminate |

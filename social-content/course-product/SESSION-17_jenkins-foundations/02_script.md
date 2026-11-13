# ✍️ 02: SCRIPT — SESSION-17: Jenkins Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S17`
- **Focus:** CI concept, Jenkins architecture & install, freestyle job, Maven build, first Jenkinsfile
- **Episodes:**
  - Episode 1: Continuous Integration kya hai aur Jenkins kyun
  - Episode 2: Jenkins Install aur Pehla Freestyle Job
  - Episode 3: Maven aur GitHub: Asli Build
  - Episode 4: Pehla Jenkinsfile: Pipeline as Code

---

# 📺 EPISODE 1: CI kya hai aur Jenkins kyun?

### [00:00 – 01:15] Scene 1: Integration Hell
**[VISUAL: Five developers each work for two weeks on their own copies. On merge day, a giant red cloud of conflicts and failures. A clock shows "Friday 6 PM".]**

**(Voiceover):**
Paanch developers do hafte tak alag alag kaam karte hain, aur release ke din sab ka code milate hain. Sab kuch tootta hai, aur Friday ki shaam gayi. Isko integration hell kehte hain. Continuous Integration is problem ka seedha hal hai: roz, balki din mein kai baar, sab ka code milao, aur har baar automatic build aur test chalao.

### [01:15 – 05:00] Scene 2: CI ka Matlab aur Fayde
**[VISUAL: A loop: Developer commits → CI server pulls → builds → runs tests → reports pass/fail (email/Slack). Fast feedback badge: "minutes, not days".]**

**(Voiceover):**
CI mein developer apna code shared repo mein push karta hai. CI server usse uthata hai, build karta hai, tests chalata hai, aur turant batata hai ki sab theek hai ya kuch toota. Fayde: galtiyan jaldi pakdi jaati hain jab unka kaaran chhota aur taaza hota hai, build har baar ek jaise environment mein hota hai, aur team ko release se darr nahi lagta. CI ka naam ek tool ka nahi, ek aadat ka hai, aur Jenkins uske liye ek bahut purana aur lokpriya tool hai.

### [05:00 – 08:30] Scene 3: Jenkins Architecture
**[VISUAL: A diagram: Jenkins controller (UI, scheduling, plugins) with multiple agents (build executors). Jobs/pipelines run on agents. Plugins around the controller.]**

**(Voiceover):**
Jenkins ek open source automation server hai, Java mein bana hua. Uska controller wo dimaag hai jo UI dikhata hai, jobs ko schedule karta hai, aur plugins sambhalta hai. Asli kaam agents par hota hai, jinhe pehle slaves kehte the. Chhote setup mein controller khud kaam kar leta hai, par production mein build agents par chalne chahiye. Jenkins ki taakat uske hazaaron plugins hain, aur uski kamzori bhi: plugins sambhalna aur upgrade karna ek zimmedari hai.

### [08:30 – 11:30] Scene 4: Lab: Tools Taiyaar Karo
**[VISUAL: A checklist: Linux VM (Ubuntu), Java 17/21 installed `java -version`, Git installed, port 8080 allowed in the security group, a plan "Jenkins on EC2 t3.small or local VM".]**

**(Voiceover):**
Lab ki taiyaari: ek Ubuntu VM lo, EC2 ya local, kam se kam 2 GB RAM. `sudo apt update && sudo apt install -y openjdk-17-jre git` chalao, aur `java -version` se check karo. Jenkins ka default port 8080 hai, to security group mein sirf apne IP ke liye 8080 kholo, poori duniya ke liye nahi. Ab jab hum agle episode mein Jenkins install karenge, ye sab ready hoga. Dhyaan: Jenkins ke supported Java versions release ke saath badalte hain, isliye install se pehle official docs mein check karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "CI = merge often + auto build/test · Jenkins controller + agents · plugins".]**

**(Voiceover):**
Recap: CI aur Jenkins ka architecture. Ab install karte hain aur apna pehla job banate hain.

---

# 📺 EPISODE 2: Jenkins Install aur Pehla Freestyle Job

### [00:00 – 01:15] Scene 1: 15 Minute mein CI Server
**[VISUAL: A timer from 15:00 counting down while a Jenkins login screen appears. A key icon: "initial admin password".]**

**(Voiceover):**
Ek CI server banane mein kitna time lagta hai? Aaj ke tools ke saath, 15 minute. Hum Jenkins ko ek Ubuntu server par install karenge, uska pehla login karenge, aur ek simple job chalayenge. Lekin pehle ek baat: Jenkins ek powerful tool hai jo aapke code aur secrets chhoo sakta hai, to uski security shuru se sochni padegi.

### [01:15 – 05:00] Scene 2: Install aur Pehla Setup
**[VISUAL: Terminal: add Jenkins apt repo and key per the official docs, `sudo apt install jenkins`, `sudo systemctl enable --now jenkins`, `sudo cat /var/lib/jenkins/secrets/initialAdminPassword`. Browser shows the Unlock screen.]**

**(Voiceover):**
Install ke liye Jenkins ki official documentation ke commands use karo, kyunki repository aur signing key ke details badalte rehte hain. Install ke baad `sudo systemctl enable --now jenkins`, aur `sudo cat /var/lib/jenkins/secrets/initialAdminPassword` se pehla password. Browser mein `http://SERVER_IP:8080` kholo, password daalo, "Install suggested plugins" chuno, aur ek admin user banao. Ye pehla admin password ek baar use hota hai; uske baad apna user istemaal karo.

### [05:00 – 08:30] Scene 3: Freestyle Job
**[VISUAL: Jenkins "New Item" → Freestyle project. Build step: Execute shell. Build Now button. Console Output page with green blue ball. A "Build history" list.]**

**(Voiceover):**
Job Jenkins ka ek kaam ka description hai. Freestyle job sabse saral: aap form mein batate ho ki source code kahan se aayega aur kaun si commands chalani hain. "Execute shell" step mein `echo "Hello from Jenkins"` aur `date`. "Build Now" dabao, aur Console Output mein dekho. Har run ko ek build number milta hai, aur Jenkins uska log aur result rakhta hai. Freestyle seekhne ke liye achha hai, par bade kaam ke liye hum jaldi hi pipeline as code par jayenge.

### [08:30 – 11:30] Scene 4: Lab: Pehla Job aur Parameter
**[VISUAL: A job with a string parameter `NAME`. The shell step: `echo "Hello, $NAME"`. "Build with Parameters" prompts for a value. Output shows the greeting. A second build intentionally fails with `exit 1` and turns red.]**

**(Voiceover):**
Lab: ek freestyle job `hello-job` banao. "This project is parameterised" mein ek String parameter `NAME` jodo. Execute shell mein `echo "Hello, $NAME"` likho. "Build with Parameters" se chalao. Ab ek build jaan-boojh kar fail karao, `exit 1` likhkar, aur dekho ki ball laal ho gaya. Jenkins har non-zero exit code ko failure maanta hai, isliye hamari Bash scripts ke exit codes yahan kaam aate hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "install from official docs · unlock · freestyle job · parameters · non-zero = fail".]**

**(Voiceover):**
Recap: Jenkins install, freestyle job, parameters. Ab ek asli project: Git se code, aur Maven se build.

---

# 📺 EPISODE 3: Maven aur GitHub

### [00:00 – 01:15] Scene 1: Java App kaise Banta Hai
**[VISUAL: Java source files → compile → test → package into `app.jar`. A gear labelled "Maven" drives each step.]**

**(Voiceover):**
Java application ko chalane layak banana ek chhota kaam nahi: code compile karo, tests chalao, dependencies jodo, aur ek `.jar` file banao. Maven ye sab ek standard tareeke se karta hai, aur ek hi file se: `pom.xml`. Jenkins aur Maven ki jodi Java projects ke liye kaafi aam hai.

### [01:15 – 05:00] Scene 2: pom.xml aur Build Lifecycle
**[VISUAL: A trimmed `pom.xml` with groupId, artifactId, version, dependencies. A lifecycle ribbon: validate → compile → test → package → verify → install. Commands: `mvn clean package`.]**

**(Voiceover):**
`pom.xml` mein project ka naam, version aur dependencies likhi hoti hain. Maven dependencies khud download karta hai. Build lifecycle ke steps: compile, test, package aur aage. `mvn clean package` purane build ko saaf karke naya `.jar` banata hai, aur tests fail hon to rok deta hai. Output `target/` folder mein milta hai. Tests ke bina package karna `-DskipTests` se hota hai, par CI mein tests skip karna aam taur par ek buri aadat hai.

### [05:00 – 08:30] Scene 3: Jenkins mein Git aur Maven
**[VISUAL: Jenkins "Manage Jenkins → Tools": add JDK and Maven. A job: Source Code Management → Git (repo URL). Build step: Invoke top-level Maven targets `clean package`. Post-build: archive `target/*.jar`.]**

**(Voiceover):**
Jenkins mein Manage Jenkins, Tools mein JDK aur Maven configure karo. Job mein Source Code Management mein Git ka repo URL daalo. Agar repo private hai, to Credentials mein ek token ya SSH key jodo, aur code mein kabhi nahi. Build step mein Maven ka `clean package`. Post-build mein artifacts archive karo, taaki `.jar` Jenkins se download ho sake. Trigger ke liye "Poll SCM" ya webhook, jo hum aage dekhenge.

### [08:30 – 11:30] Scene 4: Lab: Sample Java App Build
**[VISUAL: A public Spring Boot or simple Maven sample repo. The job pulls it, runs `mvn -B clean package`, tests pass, `app.jar` archived. A failing test turns the build red.]**

**(Voiceover):**
Lab: GitHub par ek chhota Maven sample repo lo, ya apna banao. Jenkins job mein uska URL daalo, Maven ka `-B clean package` chalao. Build ke baad artifacts mein `.jar` file dikhegi. Ab repo mein ek test jaan-boojh kar tod do aur dobara build chalao: build laal hoga aur Console Output mein batayega kaun sa test fail hua. Isi tarah CI aapki code ki galtiyan commit ke turant baad pakadta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "pom.xml · mvn clean package · Git + credentials · archive artifacts".]**

**(Voiceover):**
Recap: Git se code, Maven se build, Jenkins se automation. Lekin freestyle jobs form mein chhupe hote hain, unhe version control nahi kar sakte. Isliye ab pipeline as code.

---

# 📺 EPISODE 4: Pehla Jenkinsfile

### [00:00 – 01:15] Scene 1: Job ki Setting Gayab, Koi Nahi Jaanta Kyun
**[VISUAL: A Jenkins freestyle job with 20 settings. Someone changes one checkbox; the build breaks. No history of what changed.]**

**(Voiceover):**
Freestyle job ki setting kisi ne badal di, aur ab build toot raha hai. Kisne badla, kab badla, kuch pata nahi, kyunki wo form mein chhupa tha. Iska hal: pipeline ko code ki tarah repo mein rakho. Ek file, `Jenkinsfile`, jo version control mein rehti hai, review hoti hai, aur uska history hota hai.

### [01:15 – 05:00] Scene 2: Declarative Pipeline ka Dhancha
**[VISUAL: A Jenkinsfile with `pipeline { agent any; stages { stage('Build') { steps { sh 'mvn -B clean package' } } stage('Test') ... } post { always { ... } failure { ... } } }`. Each block highlighted.]**

**(Voiceover):**
Declarative pipeline ka dhancha: `pipeline` ke andar `agent`, jo batata hai kahan chalega. `stages` mein kai `stage`, har ek ke andar `steps`. Aur `post`, jo build ke ant mein chalta hai: `always`, `success`, `failure`. `environment` block mein variables, aur `options` mein timeouts jaise settings. Ek sabse zaroori aadat: pipeline mein secrets ko `credentials()` se lo, plain text mein nahi.

### [05:00 – 08:30] Scene 3: Pipeline Job aur Multibranch ka Idea
**[VISUAL: Jenkins "New Item → Pipeline", Definition: "Pipeline script from SCM", repo URL, script path `Jenkinsfile`. Next, a note: "Multibranch Pipeline = one job per branch automatically".]**

**(Voiceover):**
Pipeline job banao, aur Definition mein "Pipeline script from SCM" chuno, jahan repo aur Jenkinsfile ka path do. Isse Jenkinsfile repo se hi uthti hai. Aage jaake Multibranch Pipeline ek aur level deti hai: har branch ke liye apne aap ek pipeline. Is se feature branch par automatic build aur PR check aasan ho jaata hai. Pipeline sirf shell commands nahi, wo stages ki ek kahani hai: har stage ka naam batata hai ki kahan fail hua.

### [08:30 – 11:30] Scene 4: Lab: Build + Test + Archive Pipeline
**[VISUAL: A Jenkinsfile in the repo root. Stage view shows Build, Test, Package all green. A failing test turns the Test stage red; later stages skipped.]**

**(Voiceover):**
Lab: apne Maven repo ke root mein ye `Jenkinsfile` rakho:
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
    success { archiveArtifacts artifacts: 'target/*.jar', fingerprint: true }
    failure { echo 'Build failed. Check the failing stage.' }
  }
}
```
Pipeline job se chalao, Stage View mein har stage dekho. Ek test tod kar dekho ki Test stage laal hota hai aur Package skip ho jata hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Jenkinsfile in repo · stages · post · timeout · secrets via credentials()".]**

**(Voiceover):**
Recap: Jenkinsfile, declarative pipeline, stages. Ab aage: parallel stages, shared libraries, aur plugins jinse Jenkins kai tools se judta hai.

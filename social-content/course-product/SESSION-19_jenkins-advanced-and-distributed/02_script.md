# ✍️ 02: SCRIPT — SESSION-19: Jenkins Advanced & Distributed Builds
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S19`
- **Focus:** Multibranch pipelines, credentials management, security & access control, backup/restore, agents (SSH/inbound), build labels
- **Episodes:**
  - Episode 1: Multibranch Pipeline: Har Branch ki Apni Pipeline
  - Episode 2: Credentials aur Jenkins ki Security
  - Episode 3: Backup, Restore aur Upgrade ki Aadat
  - Episode 4: Agents: Distributed Builds aur Labels

---

# 📺 EPISODE 1: Multibranch Pipeline

### [00:00 – 01:15] Scene 1: Har Branch ke liye Naya Job?
**[VISUAL: A developer creating a new Jenkins job for every feature branch, then forgetting to delete 40 old ones. Replace with one multibranch folder that auto-creates and removes branch jobs.]**

**(Voiceover):**
Har feature branch ke liye haath se naya Jenkins job banana, aur branch merge hone par use hatana bhoolna: ye ek sare dard ka naam hai. Multibranch Pipeline is kaam ko khud karta hai: repo scan karta hai, har branch aur PR ke liye pipeline banata hai, aur branch hatne par job bhi hata deta hai.

### [01:15 – 05:00] Scene 2: Kaise Kaam Karta Hai
**[VISUAL: A Multibranch project config: Branch Sources (GitHub), credentials, behaviours (discover branches, PRs from origin), Build Configuration "by Jenkinsfile", scan triggers. Result: folder of branch jobs: main, feature/login, PR-12.]**

**(Voiceover):**
Multibranch project mein aap batate ho ki repo kahan hai aur kaun si branches discover karni hain. Jenkins har branch mein `Jenkinsfile` dhoondhta hai, aur jahan mile, wahan ek job banata hai. Isse har PR par automatic checks chalte hain, aur review karne wale ko build ka result PR mein hi dikhta hai. Branch ke hisaab se alag behaviour ke liye `when { branch 'main' }` jaisi conditions use hoti hain: jaise PR par sirf build aur test, aur main par deploy.

### [05:00 – 08:30] Scene 3: PR Checks aur Branch Policies
**[VISUAL: A GitHub PR page showing "continuous-integration/jenkins: Build passed". Branch protection requiring that status check before merge.]**

**(Voiceover):**
Jenkins ka status GitHub ke PR par check ke roop mein dikhta hai. Agar aap branch protection mein is check ko required kar do, to code tab tak merge nahi ho sakta jab tak build pass na ho. Ye CI ka asli fayda hai: kharab code main tak pahunchta hi nahi. Scan ko webhook se trigger karo, aur "Orphaned item strategy" se purane branches ke jobs ko automatic saaf karo.

### [08:30 – 11:30] Scene 4: Lab: Multibranch Setup
**[VISUAL: Jenkins New Item → Multibranch Pipeline. Add GitHub source, scan. Jenkins discovers `main` and `feature/demo`. Open a PR; a PR job appears and reports status back.]**

**(Voiceover):**
Lab: ek naya Multibranch Pipeline banao, source GitHub repo, credentials ke saath. "Scan now" dabao aur dekho ki `main` ke saath jo bhi branches hain unke jobs ban gaye. Ek nayi branch `feature/demo` banao, usme chhota change karo aur PR kholo. Jenkins ka build PR par dikhega. Ab ek test tod kar PR ka status laal hota hua dekho, aur sahi karke hara.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "branch discovery · PR builds · required checks · auto cleanup".]**

**(Voiceover):**
Recap: multibranch, PR checks. Ab ek bahut zaroori topic: Jenkins mein secrets aur security.

---

# 📺 EPISODE 2: Credentials aur Jenkins ki Security

### [00:00 – 01:15] Scene 1: Token Log mein Print Ho Gaya
**[VISUAL: A Jenkins console log with `echo $DOCKER_PASSWORD` printing a real password in plain text. A red alert. Next, the same line masked as `****`.]**

**(Voiceover):**
Ek developer ne debug ke liye `echo $DOCKER_PASSWORD` likh diya, aur password build log mein, sabko dikhta hua. Jenkins ek aisa server hai jo aapke code, cloud keys aur production tak ki chaabiyan chhoota hai. Agar wo kamzor hua, to poora system khatre mein. Isliye credentials aur security uska sabse zaroori hissa hai.

### [01:15 – 05:00] Scene 2: Credentials ka Sahi Upyog
**[VISUAL: Jenkins "Manage Credentials": types: Username with password, Secret text, SSH key, Secret file. A pipeline using `withCredentials([string(credentialsId:'api-token', variable:'TOKEN')]) { sh 'curl -H "Authorization: Bearer $TOKEN" ...' }` with the value masked in logs.]**

**(Voiceover):**
Jenkins ke Credentials store mein secrets alag alag type mein rakhte hain: username-password, secret text, SSH key, secret file. Pipeline mein `withCredentials` se unhe milta hai, aur Jenkins unko log mein mask kar deta hai. Phir bhi ek dhyaan: masking pakki suraksha nahi, agar aap secret ko modify karke print karoge to wo dikh sakta hai. Isliye secrets ko print mat karo, aur double quotes ki jagah single quotes se shell mein variable ko Jenkins ke interpolation se bachao.

### [05:00 – 08:30] Scene 3: Access Control aur Hardening
**[VISUAL: A security checklist: Login required; matrix-based authorisation; no anonymous access; Controller built-in node has 0 executors; HTTPS via reverse proxy; CSRF protection on; plugins updated; audit.]**

**(Voiceover):**
Jenkins ko surakshit rakhne ki checklist. Login zaroori, anonymous access band. Authorization mein role ya matrix ke through, har insaan ko sirf utna access jitna kaam ke liye chahiye. Controller par builds mat chalao: built-in node par executors zero rakho, aur builds agents par. HTTPS reverse proxy ke peeche. Plugins aur Jenkins ko regular update karo. Aur Jenkins ke URL ko seedha internet par khula mat chodo.

### [08:30 – 11:30] Scene 4: Lab: Secret Safe Pipeline
**[VISUAL: Add a "Secret text" credential. A pipeline step uses it via `withCredentials`. The console shows `****`. Then the built-in node executors set to 0 in Manage Nodes.]**

**(Voiceover):**
Lab: ek Secret text credential banao, id `demo-token`. Pipeline mein:
```groovy
stage('Use secret') {
  steps {
    withCredentials([string(credentialsId: 'demo-token', variable: 'TOKEN')]) {
      sh 'echo "Token length: ${#TOKEN}"'
    }
  }
}
```
Log mein sirf length dikhegi, aur agar `echo $TOKEN` karoge to `****`. Phir Manage Jenkins, Nodes mein built-in node ke executors ko 0 karo aur dekho ki ab builds ke liye agent chahiye; agle episodes mein hum agent banayenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "withCredentials · never print secrets · least privilege · 0 executors on controller".]**

**(Voiceover):**
Recap: credentials aur Jenkins ki hardening. Ab ek aur zaroori cheez: Jenkins ka backup.

---

# 📺 EPISODE 3: Backup, Restore aur Upgrade

### [00:00 – 01:15] Scene 1: Jenkins Server Mar Gaya, Saare Jobs Gaye
**[VISUAL: A Jenkins EC2 instance terminated. A team stares at an empty new Jenkins login page. A "years of jobs: gone" label.]**

**(Voiceover):**
Jenkins ka server kharab hua, disk gayi, aur saath mein saare jobs, credentials aur history. Agar backup nahi tha, to maheenon ka kaam gaya. Jenkins ka sab kuch ek folder mein rehta hai, aur use samajhna aapke backup aur restore ki neev hai.

### [01:15 – 05:00] Scene 2: JENKINS_HOME mein Kya Hai
**[VISUAL: A directory tree of `/var/lib/jenkins` highlighting: `config.xml`, `jobs/`, `credentials.xml`, `secrets/`, `plugins/`, `users/`, `nodes/`. A warning on `secrets/` (needed to decrypt credentials).]**

**(Voiceover):**
`JENKINS_HOME`, aam taur par `/var/lib/jenkins`, mein sab kuch hai: global config, jobs, plugins, users, aur credentials. `secrets/` folder bahut sensitive hai kyunki uske bina credentials decrypt nahi ho sakte, aur uske saath backup ko encrypted rakhna zaroori hai. Pipeline-as-code ka ek bada fayda: Jenkinsfile aur job config Git mein hai, to server gaya to bhi pipelines bache. Is liye Jenkins configuration ko bhi code mein rakhne ke raaste, jaise Configuration as Code, kaafi achhe hain.

### [05:00 – 08:30] Scene 3: Backup Strategy
**[VISUAL: A plan: nightly `tar` of JENKINS_HOME (excluding workspace/caches), copy to S3 (encrypted), keep 14 days, test restore monthly. Alternative: EBS snapshot of the disk.]**

**(Voiceover):**
Ek simple strategy. Roz raat JENKINS_HOME ka archive banao, build workspace aur cache ko exclude karke, aur use S3 ya kisi surakshit jagah encrypt karke rakho. Ya EC2 par disk ka EBS snapshot lo. Retention tay karo, jaise 14 din. Sabse zaroori: restore ka test. Mahine mein ek baar naye server par restore karke dekho ki Jenkins sahi uthta hai ya nahi. Aur upgrade se pehle hamesha backup, aur Jenkins ke naye version ko pehle test instance par chalao.

### [08:30 – 11:30] Scene 4: Lab: Backup aur Restore Test
**[VISUAL: A script `jenkins-backup.sh` using `tar --exclude` and `aws s3 cp`. Then a restore on a second VM: stop jenkins, extract, fix ownership, start, and see the jobs.]**

**(Voiceover):**
Lab:
```bash
#!/usr/bin/env bash
set -euo pipefail
ts=$(date +%F)
sudo tar --exclude='workspace' --exclude='caches' -czf "/tmp/jenkins-$ts.tgz" -C /var/lib jenkins
# aws s3 cp "/tmp/jenkins-$ts.tgz" s3://YOUR-BACKUP-BUCKET/jenkins/
echo "backup: /tmp/jenkins-$ts.tgz"
```
Isko cron se chalao. Restore test: doosri VM par Jenkins install karo, `sudo systemctl stop jenkins`, archive extract karo, `sudo chown -R jenkins:jenkins /var/lib/jenkins`, aur `sudo systemctl start jenkins`. Check karo ki jobs aur users wapas aa gaye. Test ke baad extra VM hata do.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "JENKINS_HOME · encrypt backups · test restore · config as code".]**

**(Voiceover):**
Recap: backup aur restore ki aadat. Ab scale: ek Jenkins par sab build chalana kab tak?

---

# 📺 EPISODE 4: Agents — Distributed Builds

### [00:00 – 01:15] Scene 1: Ek Kitchen, Bees Order
**[VISUAL: A kitchen with one chef and a mountain of orders. Next frame: a head chef (controller) assigning orders to several kitchens (agents).]**

**(Voiceover):**
Ek akela Jenkins server jab sabke builds chalata hai, to jaldi hi queue lag jaati hai, aur ek bhaari build baaki sab ko rok deti hai. Distributed builds mein controller sirf tay karta hai ki kaun sa job kahan chalega, aur asli kaam alag machines, yaani agents, par hota hai.

### [01:15 – 05:00] Scene 2: Agent ke Tareeke aur Labels
**[VISUAL: Controller with three agents: Linux-maven, Linux-docker, Windows. Labels: `linux`, `docker`, `windows`. A pipeline: `agent { label 'docker' }`. Connection types: SSH (controller → agent), inbound/JNLP (agent → controller), cloud/dynamic agents.]**

**(Voiceover):**
Agent ek machine hai jisme Java ho aur jo controller se jud sake. Do aam tareeke: SSH, jisme controller agent par login karta hai, aur inbound, jisme agent khud controller se connect hota hai, jo firewall ke peeche wali machines ke liye kaam aata hai. Aur dynamic agents, jaise Kubernetes ya cloud par automatic bani hui, jo build khatam hote hi gayab ho jaati hain. Labels se aap tay karte ho ki job kahan chale: `agent { label 'docker' }`.

### [05:00 – 08:30] Scene 3: Agent ki Design Best Practices
**[VISUAL: A checklist: Agents are disposable; same tools via AMI/Docker; no secrets stored on agents; builds in clean workspace; small executors count; controller has none.]**

**(Voiceover):**
Agents ko disposable maano: unko aap AMI ya container se ek jaise bana sako, aur kabhi kabhi baar baar naya bana do. Unpar secrets store mat karo, wo Jenkins credentials se aayein. Executors utne hi rakho jitni CPU aur RAM sambhaal sake. Workspace saaf rakho, taaki purane build ka kuch asar na pade. Aur controller par koi build nahi. Agar agent par tools alag alag versions ke hon to "mere agent par to chal raha tha" wali purani bimari wapas aa jaati hai.

### [08:30 – 11:30] Scene 4: Lab: SSH Agent Joro
**[VISUAL: A second EC2 instance with Java installed. Jenkins: Manage Nodes → New Node, remote root dir, label `linux-agent`, launch method SSH with credentials. The node goes online. A pipeline with `agent { label 'linux-agent' }` runs there; `hostname` shows the agent.]**

**(Voiceover):**
Lab: ek doosra Linux instance banao, `sudo apt install -y openjdk-17-jre git`. Jenkins mein Manage Nodes mein New Node: naam, remote root directory `/home/ubuntu/jenkins`, label `linux-agent`, launch method SSH, aur credentials mein private key. Node online ho jaye to pipeline mein `agent { label 'linux-agent' }` likho aur ek `sh 'hostname'` stage jodo. Log mein agent ka hostname dikhega, controller ka nahi. Ab aapka Jenkins distributed hai. Lab ke baad extra instance hata dena.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "controller schedules · agents build · labels · disposable agents · no secrets on agents".]**

**(Voiceover):**
Recap: Jenkins ka poora toolkit: pipelines, plugins, security, backup aur agents. Ab ek aur popular tool: GitHub Actions, jahan CI seedha aapke repo ke andar rehta hai, aur saath mein DevSecOps: pipeline mein security.

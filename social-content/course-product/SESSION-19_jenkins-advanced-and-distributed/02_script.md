# ✍️ 02: SCRIPT — SESSION-19: Jenkins Advanced and Distributed
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S19`
- **Focus:** Multibranch pipelines (branch discovery, pull request builds, fork trust, required status checks, tag builds), credentials (types, scope, masking, long-lived keys vs instance roles), Jenkins security hardening (realm, authorization, zero executors on the controller, admin = all secrets), `JENKINS_HOME`, backup and restore (tar and EBS snapshot), upgrade habits, Configuration as Code, agents (SSH and inbound, labels, ephemeral agents, private-wing agents), executors
- **Builds on:** Session 04 (ownership), Session 06 (backup script, cron), Session 09 (roles, access keys), Session 10 (EBS, snapshot, AMI, launch template), Session 12 (S3 lifecycle), Session 14 (private wing, security group chain, NAT), Session 16B (branch protection, pull request review, tags), Session 17 and 18 (Jenkinsfile, webhook, plugins)
- **Story position:** Zoom level 3, head office. Har draft ki apni conveyor, foreman ki locked key cabinet, foreman ke records ki nightly copy, aur workbenches jo bhaari kaam uthati hain. Ye wo sab hai jo ek chhoti workshop ko ek bharosemand workshop banata hai.
- **Story words used:** foreman (Jenkins), conveyor (pipeline), key cabinet (credentials), workbench (agent), blueprint (code), vault (GitHub), master par taala (branch protection), release ki mohar (tag), photograph (snapshot), duty badge (role), private wing (private subnet), door guard (security group), dispatch desk (NAT), staff (admin)
- **Lab project:** Atithi's `booking-service`: each branch and pull request gets its own conveyor, secrets stay in the key cabinet, the foreman's records are backed up and restored on a second building, and a workbench in the private wing does the building.
- **Cost rule (AWS):** every extra building (agent, restore test) is billed while it runs. Every lab ends with stopping or terminating the extra buildings, and with deleting test snapshots and old backups.
- **Episodes:**
  - Episode 1: Har Branch ki Apni Conveyor: Multibranch Pipeline
  - Episode 2: Key Cabinet aur Foreman ki Suraksha
  - Episode 3: Foreman ke Records ka Backup, Restore aur Upgrade
  - Episode 4: Workbenches: Distributed Builds

---

# 📺 EPISODE 1: Har Branch ki Apni Conveyor

### [00:00 – 02:10] Scene 1: Har Draft ke liye Naya Job?
**[VISUAL: A team lead creating a new Jenkins job by hand for every feature branch and forgetting to delete forty old ones. The picture changes to one Multibranch folder that grows and shrinks on its own as branches appear and disappear.]**

**(Voiceover):**
Session 16B mein Atithi ke designers har kaam ke liye alag draft, yaani branch, banate hain. Agar har draft ke liye foreman ke daftar mein haath se naya job banana pade, aur merge hone ke baad use hatana bhi yaad rakhna pade, to chalta nahi: ek mahine mein chaalis purane jobs ka kachra. Multibranch Pipeline is kaam ko khud sambhalta hai. Wo vault ko scan karta hai, har branch aur har pull request ke liye ek alag conveyor banata hai, aur branch hatne par us conveyor ko bhi hata deta hai.

### [02:10 – 05:05] Scene 2: Multibranch Kaise Kaam Karta Hai
**[VISUAL: A Multibranch project config: Branch Sources → GitHub, credentials, repository. Behaviours: discover branches, discover pull requests from origin, discover pull requests from forks (trust setting). Build Configuration: "by Jenkinsfile". Scan triggers: periodic and webhook. Result: a folder with `main`, `feature/login`, `PR-12`, `release-1.0`.]**

**(Voiceover):**
Multibranch project mein aap vault ka repo aur credentials batate ho, aur kaun si cheezein dhoondhni hain: branches, origin ke pull requests, aur forks ke pull requests. Jenkins har branch mein `Jenkinsfile` dhoondhta hai, aur jahan mile wahan ek conveyor banata hai. Isme Jenkins ko branch ka naam pata hota hai, `BRANCH_NAME`, aur pull request ka number, `CHANGE_ID`. Isiliye ab `when { branch 'main' }` aur `when { changeRequest() }` chalte hain, jo Session 18 mein aam job mein kaam nahi karte the. Scan ko webhook se trigger karo, aur ek periodic scan bhi rakho, jo kisi chhooti hui ghanti ko pakad le. Aur "Orphaned item strategy" se purane branches ki conveyors ek tay samay baad apne aap saaf ho jaati hain.

### [05:05 – 07:30] Scene 3: Pull Request par Check aur Master par Taala
**[VISUAL: A pull request page on the vault: the check `continuous-integration/jenkins/pr-merge` shown in red, then green. Branch protection settings with "Require status checks to pass before merging" and the Jenkins check selected. The merge button greyed out until the check is green.]**

**(Voiceover):**
Jenkins ka natija vault ke pull request par ek check ki tarah dikhta hai. Ab Session 16B ke master par taale ko is check se jodo. Branch protection mein "Require status checks to pass before merging" on karo, aur Jenkins ka check chuno. Check ke naam console mein dikhte hain, jaise `continuous-integration/jenkins/pr-merge`. Phir jab tak conveyor hari na ho, merge ka button grey rahega. Yahi CI ka asli faayda hai: kharab revision master tak pahunchta hi nahi, aur chief architect ko review mein ye pata hota hai ki inspection pass ho chuka hai. Isse reviewer ka samay kaam ki cheezon mein jaata hai.

### [07:30 – 09:50] Scene 4: Fork ka Khatra
**[VISUAL: An outside contractor's fork opens a pull request that also edits the `Jenkinsfile` to print the secrets. A red arrow shows the conveyor reading the changed Jenkinsfile and the key cabinet. Below, a trust setting: "Nobody / Contributors / Collaborators / Everyone".]**

**(Voiceover):**
Ek khaas khatra yaad rakho. Pull request ke saath uski Jenkinsfile bhi aati hai, aur Jenkins use chalata hai. Agar baahar ka koi contractor, yaani fork wala, apni pull request mein Jenkinsfile badal de, aur usme key cabinet ki chaabiyan print karne wali line daal de, to Jenkins use chala sakta hai. Isliye forks ke liye trust setting ka dhyaan: sirf "Contributors" ya "Nobody" rakho, "Everyone" nahi. Aur pull request ki conveyor ko credentials mat do, jab tak wo vishwaaspaatr na ho. Ek aur surakshit tareeka: Jenkinsfile hamesha target branch, yaani trusted revision, se lo, pull request se nahi.

### [09:50 – 12:25] Scene 5: Branch ke Hisaab se Behaviour
**[VISUAL: A Jenkinsfile with three stations. `Build` and `Test` for every branch and PR. `Package` only for `main` and tags. `Deploy to staging` only for `main`. A tag `v1.2.0` in the vault starts a station `Release`. A table showing which branch runs which station.]**

**(Voiceover):**
Multibranch ka ek aur faayda: ek hi Jenkinsfile alag alag branches par alag alag kaam kar sakti hai. Har branch aur pull request par sirf Build aur Test. Master par Package aur staging ka Deploy. Aur Session 16B ki release ki mohar, yaani tag, jaise `v1.2.0`, `when { tag 'v*' }` se ek Release station chala sakti hai. Isse jo kaam khatarnak hai, wo sirf bharose ki jagah par hota hai. Aur ek aadat: har station ka log sirf ek hi branch ka dikhe, taaki ek branch ka kharab build doosre ki halat na bigaade. Ye tag, aage Docker mein, image ke tag banenge, jo hum Session 22 mein dekhenge.

### [12:25 – 15:00] Scene 6: Lab: Multibranch Setup
**[VISUAL: Jenkins New Item → Multibranch Pipeline → GitHub source. Scan Repository Now. `main` and `feature/demo` appear. A pull request opens; a PR conveyor appears and the check shows on the vault page. A broken test turns the check red; the fix turns it green. Branch protection added.]**

**(Voiceover):**
Lab. Ek naya Multibranch Pipeline banao, source vault ka repo, credentials ke saath. "Scan Repository Now" dabao, aur dekho ki `main` ke saath jitni branches hain, utni conveyors ban gayi. Ab ek branch `feature/demo` banao, chhota change karo aur pull request kholo. Jenkins ka check pull request par dikhega. Ek test jaan boojh kar tod do, aur check laal hote dekho. Phir use theek karo aur check hara hote dekho. Ab branch protection mein ye check required karo, aur dekho ki laal check par merge nahi hota. Aakhir mein `feature/demo` ko merge karke hatao, aur dekho ki agli scan par Jenkins ki folder se uski conveyor ghaib ho jaati hai.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "branch + PR discovery · check on the pull request · required check on master · fork trust: Contributors · tag builds · orphan cleanup".]**

**(Voiceover):**
Recap: multibranch, pull request ke checks, aur fork ka khatra. Ab key cabinet: Jenkins mein secrets aur uski suraksha.

---

# 📺 EPISODE 2: Key Cabinet aur Foreman ki Suraksha

### [00:00 – 01:35] Scene 1: Password Log mein Print Ho Gaya
**[VISUAL: A build log with `echo $DOCKER_PASSWORD` printing a real password in plain text to everyone. A red alert. In the next frame, the same line shows `****`.]**

**(Voiceover):**
Ek developer ne debug karne ke liye `echo $DOCKER_PASSWORD` likh diya, aur password build log mein, sabko dikhta hua. Jenkins ek aisa server hai jo aapke code, cloud ki chaabiyan, aur production tak ke raaste chhoota hai. Agar foreman ka daftar kamzor hua, to poora head office khatre mein. Isliye key cabinet aur Jenkins ki suraksha uska sabse zaroori hissa hai. Session 17 mein humne quotes ka jaal dekha tha. Aaj poori tasveer.

### [01:35 – 03:50] Scene 2: Key Cabinet ka Sahi Upyog
**[VISUAL: Manage Jenkins → Credentials with types: Username with password, Secret text, SSH Username with private key, Secret file, Certificate. A scope label "Global" vs "System" vs a folder. A pipeline fragment with `withCredentials([string(credentialsId: 'api-token', variable: 'TOKEN')]) { sh 'curl -sH "Authorization: Bearer $TOKEN" https://api.example.com' }`.]**

**(Voiceover):**
Jenkins ki key cabinet mein secrets alag alag type ke hote hain: username aur password, secret text, SSH private key, secret file, certificate. Har ek ka ek ID hota hai, aur ek scope. System scope ki chaabi sirf Jenkins ke apne kaam ke liye, global sab conveyors ke liye, aur folder scope sirf ek folder ki conveyors ke liye. Jitna chhota scope, utna achha. Conveyor mein `withCredentials` se chaabi ek variable ban jaati hai, aur Jenkins use log mein `****` kar deta hai. Ek hi shart: single quotes. `sh 'curl ... $TOKEN'`, jisse shell variable padhe, Jenkins nahi, jaisa Session 17 mein dekha.

### [03:50 – 06:40] Scene 3: Masking Pakki Suraksha Nahi
**[VISUAL: A log where the secret is masked as `****`, but a reversed, spaced-out or hex copy of the same secret printed by a script appears in full. Beside it, a Script Console window listing every credential decrypted in clear text for an admin.]**

**(Voiceover):**
Masking ek parda hai, taala nahi. Jenkins log mein secret ka seedha text dhundh kar `****` kar deta hai. Naye Jenkins base64 wali copy bhi chhupa dete hain, par agar koi parchi secret ko ulta, har akshar ke beech jagah daal kar, ya hex mein chhaap de, to wo poora dikh jaata hai, kyunki Jenkins ko wo secret nahi lagega. Aur ek badi baat: Jenkins ka admin Script Console se saari chaabiyan clear text mein padh sakta hai. Matlab, admin hona poore key cabinet ka maalik hona hai. Isliye admin kam logon ko, aur jo conveyor secret use karti hai uska Jenkinsfile bhi review se hi badle, jaisa Session 18 ke trusted library mein. Pehli suraksha secrets ko print na karna hai, doosri unhe kam se kam jagah rakhna.

### [06:40 – 09:25] Scene 4: Lambi Chaabi Nahi, Duty Badge
**[VISUAL: Two ways for a build to reach AWS. Way 1: an access key stored in the key cabinet, with a "rotate every 90 days" tag and a leak arrow. Way 2: the workbench building wearing a duty badge with only the permissions it needs, no key anywhere.]**

**(Voiceover):**
Sabse achhi chaabi wo hai jo hai hi nahi. Maan lo conveyor ko S3 mein finished unit rakhna hai, ya SNS par alert bhejna hai. Pehla tareeka: Session 9 ki access key banao aur key cabinet mein rakho. Wo lambi chaabi hai: jab tak koi use badle nahi, wo chalti rehti hai, aur leak ho sakti hai. Doosra tareeka: Jenkins ki workbench, yaani EC2 building, ko ek duty badge pehna do, jisme sirf zaroori ijaazat ho, jaise ek bucket ke ek prefix mein likhna. Phir koi chaabi key cabinet mein hai hi nahi, aur AWS CLI badge khud utha leta hai. Jo chaabiyan baahar ki service ke liye hoti hain, jaise Slack ya GitHub, unhe key cabinet mein rakho aur rotate karne ka plan banao.

### [09:25 – 12:05] Scene 5: Foreman ke Daftar ki Suraksha ka Checklist
**[VISUAL: A checklist screen of Manage Jenkins → Security: Security Realm (own database, LDAP or single sign-on), Authorization (matrix or role-based), "Allow anonymous read access" unticked, CSRF protection on, agent-to-controller access on. HTTPS via a reverse proxy or ALB. Built-In Node: number of executors 0.]**

**(Voiceover):**
Foreman ke daftar ka checklist. Ek, login zaroori, anonymous read band. Security Realm mein ya Jenkins ka apna database, ya LDAP ya single sign-on, jo company mein ho. Do, Authorization: matrix ya role-based, taaki har insaan ko sirf utna mile jitna kaam ke liye chahiye. Teen, builds controller par nahi: built-in node ke executors zero rakho, aur saare builds workbenches par. Jab chhote setup mein controller par chalte hain, to wahi machine jahan key cabinet rakhi hai, har kisi ke code ko chalti hai. Chaar, HTTPS, jaise Session 18 mein. Paanch, CSRF protection on, aur agent se controller ka access control on. Chhe, Jenkins aur plugins ko update rakho. Saat, Jenkins ka URL seedha internet par khula mat chhodo.

### [12:05 – 14:50] Scene 6: Lab: Secret Safe Conveyor
**[VISUAL: A Secret text credential with ID `demo-token`. A pipeline that prints only the length of the token, and then a line that prints the token and shows `****`. Manage Nodes → Built-In Node → executors set to 0, and a build stuck in the queue with "Waiting for next available executor".]**

**(Voiceover):**
Lab. Ek Secret text credential banao, ID `demo-token`. Conveyor mein:
```groovy
stage('Use secret') {
  steps {
    withCredentials([string(credentialsId: 'demo-token', variable: 'TOKEN')]) {
      sh 'echo "Token length: ${#TOKEN}"'
      sh 'echo "$TOKEN"'
    }
  }
}
```
Log mein length dikhegi, aur `echo "$TOKEN"` ki jagah `****`. Ab ek aur parchi likho jo `echo "$TOKEN" | rev` chalaye, aur dekho ki masking ka parda yahan kaise tootta hai. Base64 try karoge to wo bhi chhupa milega. Phir Manage Jenkins, Nodes mein built-in node ke executors ko zero karo, aur dekho ki build ab "Waiting for next available executor" mein atak jaati hai. Agle episodes mein hum workbench jodenge, tab chalegi. Aakhir mein apne account se kisi bhi ek credential ka scope check karo: global hai ya folder?

### [14:50 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "credentials by type and scope · single quotes · masking is a curtain · admin = all secrets · duty badge not a long key · 0 executors on the controller · HTTPS".]**

**(Voiceover):**
Recap: key cabinet, masking ki seema, aur foreman ke daftar ki suraksha. Ab ek sawaal jo kabhi na kabhi poochna padta hai: agar foreman ka server kal gir jaaye?

---

# 📺 EPISODE 3: Foreman ke Records ka Backup

### [00:00 – 02:05] Scene 1: Server Gaya, Saare Jobs Gaye
**[VISUAL: A Jenkins building terminated by mistake. A team looks at a fresh, empty login page. A label: "years of jobs, users and keys: gone".]**

**(Voiceover):**
Jenkins ka server kharab hua, ya kisi ne galti se terminate kar diya. Saath mein saare jobs, users, plugins aur chaabiyan. Agar backup nahi tha, to mahino ka kaam gaya. Lekin ek achhi baat hai: Session 17 ke baad aapki conveyor Jenkinsfile mein, yaani vault mein hai. Isliye kam se kam conveyors bach jaati hain. Jo nahi bachta wo hai Jenkins ki apni config, users, key cabinet aur build ka history. Is sab ka ghar ek hi folder hai, aur use samajhna backup aur restore ki neev hai.

### [02:05 – 05:05] Scene 2: JENKINS_HOME mein Kya Hai
**[VISUAL: A directory tree of `/var/lib/jenkins` with these entries highlighted: `config.xml`, `jobs/`, `credentials.xml`, `secrets/`, `plugins/`, `users/`, `nodes/`, `workspace/` and `caches/` (crossed out as "do not back up"). A warning next to `secrets/`: "needed to decrypt credentials".]**

**(Voiceover):**
`JENKINS_HOME`, aam taur par `/var/lib/jenkins`, mein sab kuch hai: global `config.xml`, `jobs/` jisme har job ka config aur build ka history, `plugins/`, `users/`, `nodes/`, aur key cabinet ka `credentials.xml`. `secrets/` folder sabse sensitive hai, kyunki uske bina `credentials.xml` ki chaabiyan khul hi nahi sakti. Isliye backup mein `secrets/` zaroor rakho, par backup khud encrypted ho aur bahut kam logon ki pahunch mein ho. `workspace/` aur `caches/` backup mein nahi chahiye, kyunki wo phir se ban jaate hain aur bahut bade hote hain. Aur ek aur jaankari: Jenkins ke andar ki config ko code mein rakhne ka tareeka Configuration as Code hai, jisme ek `jenkins.yaml` mein security realm, nodes aur plugins likhe jaate hain. Secrets us file mein nahi, environment ya secret store se aate hain.

### [05:05 – 07:50] Scene 3: Teen Tareeke aur Ek Niyam
**[VISUAL: Three options. 1: a nightly `tar` of `JENKINS_HOME` copied to an S3 bucket with a lifecycle rule. 2: `JENKINS_HOME` on a separate EBS volume mounted at `/var/lib/jenkins`, snapshotted nightly. 3: an AMI of the whole building after a big change. A rule below: "a backup you have never restored is a hope".]**

**(Voiceover):**
Tareeke teen hain. Ek, roz raat `JENKINS_HOME` ka tar archive, workspace aur cache hata kar, ek S3 bucket mein, jis par Session 12 ka lifecycle rule ho, jaise chaudah din baad purane hatao. Do, `JENKINS_HOME` ko ek alag EBS volume par rakho, `/var/lib/jenkins` par mount karo, jo Session 5B ke fstab mein Session 10 ke `nofail` ke saath ho, aur us volume ka roz ek snapshot lo. Snapshot se pehle Jenkins ko "Prepare for shutdown" ya quiet down kar do, taaki beech mein koi build file na likh raha ho. Teen, bade badlaav ke baad poori building ka AMI. Aur ek niyam: jis backup ko aapne kabhi restore nahi kiya, wo ek ummeed hai, backup nahi.

### [07:50 – 10:30] Scene 4: Upgrade ki Aadat
**[VISUAL: A timeline: backup → test copy built from the backup → upgrade the test copy → run the key conveyors → upgrade the real one. Two lanes, "LTS" and "weekly". A plugins list file `plugins.txt` with pinned versions.]**

**(Voiceover):**
Upgrade ki ek chhoti aadat. Pehle backup. Phir us backup se ek test copy banao, doosri building par. Upgrade pehle us par karo, aur kuch zaroori conveyors chalao. Sab theek ho tabhi asli foreman par. Jenkins ke do raaste hain: LTS, jo sthir hai aur jise production ke liye chuna jaata hai, aur weekly, jo har hafte naya hai. Atithi LTS par rahega. Plugins ke versions ko ek `plugins.txt` mein likh sakte ho, aur `jenkins-plugin-cli` se install, taaki test aur asli foreman ek hi plugins par chalen. Aur wahi Session 10 ka sabak: jo cheez haath se banti hai, use ek dusri building par dobara banane ka ek likha hua tareeka rakho.

### [10:30 – 13:35] Scene 5: Lab: Backup Parchi aur Restore Test
**[VISUAL: A script `jenkins-backup.sh` with `set -euo pipefail`, a timestamped file name, `tar --exclude`, an S3 upload with server-side encryption, and a lock. A second building: install Jenkins, stop it, extract, `chown -R jenkins:jenkins`, start it, and see the same jobs and users.]**

**(Voiceover):**
Lab. Ye Session 6 ki parchi ka naya rup hai:
```bash
#!/usr/bin/env bash
set -euo pipefail
ts=$(date +%Y%m%d-%H%M)
file="/tmp/jenkins-$ts.tgz"
sudo tar --exclude='workspace' --exclude='caches' -czf "$file" -C /var/lib jenkins
aws s3 cp "$file" "s3://YOUR-BACKUP-BUCKET/jenkins/" --sse AES256
rm -f "$file"
echo "backup done: $ts"
```
Building ko S3 mein likhne ka duty badge do, access key nahi. Isko cron se roz chalao, `flock` ke saath, jaise Session 6 mein. Ab restore test: ek doosri building par wahi Jenkins version install karo. `sudo systemctl stop jenkins`, backup ko `/var/lib` mein extract karo, `sudo chown -R jenkins:jenkins /var/lib/jenkins`, aur `sudo systemctl start jenkins`. Check karo ki jobs, users aur credentials wapas aa gaye. Test ke baad extra building hata do, aur purane backups ko lifecycle rule se chaudah din ke baad hatao.

### [13:35 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "JENKINS_HOME: jobs, config, credentials, secrets, plugins · skip workspace and caches · tar to S3 or EBS snapshot · restore drill · LTS · pin plugins · config as code".]**

**(Voiceover):**
Recap: foreman ke records ka ghar, uska backup, aur upgrade ki aadat. Ab ek aur sawaal: ek akela foreman ek akeli workbench par sab kuch kab tak banayega?

---

# 📺 EPISODE 4: Workbenches

### [00:00 – 01:55] Scene 1: Ek Workbench, Bees Order
**[VISUAL: A workshop with one workbench and twenty orders waiting. One heavy order blocks all the others. The next frame: the foreman at his desk assigning orders to several workbenches, each with its own sign.]**

**(Voiceover):**
Ab Atithi ke paas dus services hain, aur har revision par conveyor chalti hai. Ek workbench par saari builds ek ke peeche ek, aur ek bhaari build baaki sabko rok deti hai. Isi liye Session 17 mein hum ne controller aur workbench alag kiye the. Distributed build mein foreman sirf tay karta hai ki kaun sa kaam kis workbench par jaayega, aur asli fabrication workbenches, yaani agents, par hoti hai. Aur Episode 2 mein humne controller ke executors zero kiye the, to ye ab seedhi zaroorat hai.

### [01:55 – 04:30] Scene 2: Workbench Jodne ke Tareeke
**[VISUAL: The foreman with three connection types. 1: "SSH" arrow from controller to agent. 2: "Inbound" arrow from agent to controller, through a firewall. 3: "Ephemeral": a new agent appears from a template for each build and disappears after.]**

**(Voiceover):**
Workbench ek machine hai, jisme Java ho, aur jo foreman se jud sake. Teen tareeke. SSH: foreman workbench par login karta hai. Isme workbench par SSH ki chaabi aur uska security group chahiye. Inbound: workbench khud foreman se jud jaati hai, `agent.jar` aur ek secret ke saath, jo tab kaam aata hai jab workbench firewall ke peeche ho aur foreman use dekh na sake. Aur ephemeral agents: har build ke liye ek nayi workbench apne aap banti hai, EC2 ya container se, aur build ke baad gayab ho jaati hai. Aakhri tareeka sabse saaf hai, kyunki purani build ka kuch bacha hi nahi. Kubernetes par yehi kaam aage Session 23 aur 25 mein dikhega.

### [04:30 – 06:45] Scene 3: Labels aur Executors
**[VISUAL: Three workbenches with labels: `linux maven`, `linux docker`, `windows`. A Jenkinsfile using `agent { label 'docker' }` and another using `agent { docker { image 'maven:3-eclipse-temurin-17' } }`. A small gauge for executors: "about one per CPU core".]**

**(Voiceover):**
Labels se tay hota hai ki kaam kahan jaaye. Workbench par labels `linux`, `maven`, `docker` lagao, aur Jenkinsfile mein `agent { label 'docker' }`. Ya agar Docker Pipeline plugin ho to `agent { docker { image 'maven:3-eclipse-temurin-17' } }`, jisme har build ke liye ek saaf container milta hai, jisme Maven aur Java pehle se hain, aur workbench par kuch install nahi karna. Executors ka matlab hai ki ek workbench par kitne kaam ek saath chalen. Aam niyam: lagbhag CPU cores ke barabar. Isse zyada rakhoge to build dheemi hongi aur memory khatam hogi, jo Session 5 ki top ki kahani hai.

### [06:45 – 09:30] Scene 4: Private Wing mein Workbench
**[VISUAL: A campus map. The foreman in the public wing, workbenches in the private wing. Security group chain: `jenkins-sg` → port 22 → `agent-sg`. A dispatch desk lets the workbench reach the internet for dependencies. The workbench wears a duty badge. No public IP on the workbench.]**

**(Voiceover):**
Session 14 ka naksha yahan kaam aata hai. Workbenches ko private wing mein rakho, bina public IP ke. Unke door guard, `agent-sg`, ki list mein port 22 sirf `jenkins-sg` se, kisi IP list se nahi. Dependencies download karne ke liye private wing ki direction board dispatch desk, yaani NAT gateway, ki taraf ho. Aur har workbench par ek duty badge, jisme sirf wahi ijaazat jo build ko chahiye. Isse workbench ke paas koi chaabi bhi nahi aur koi bahar se aa bhi nahi sakta. Aur design ke niyam: workbench disposable ho, ek AMI ya launch template se bani, tools sab jagah ek jaise, aur us par secrets store nahi. "Mere workbench par to chal raha tha" wali bimari isi se jaati hai.

### [09:30 – 12:00] Scene 5: Jab Workbench Aati aur Jaati Hai
**[VISUAL: A build starts on workbench A, uploads a "stash" of the compiled classes, and a later station on workbench B retrieves it with `unstash`. A workbench goes offline mid-build, shown in red, with a retry policy.]**

**(Voiceover):**
Jab ek conveyor ke alag stations alag workbenches par chalte hain, to ek workbench ki files doosri par nahi hotin. Isliye `stash` aur `unstash`: ek station ke natije chhote paimane par rakho aur doosre station mein utha lo. Bade natije, jaise finished unit, `archiveArtifacts` ya S3 mein rakho, stash mein nahi. Aur ek workbench build ke beech mein offline ho sakti hai. Isliye conveyor mein `timeout` aur zaroorat par `retry` rakho, aur Jenkins ke Node monitors ko disk kam hone par workbench ko apne aap offline karne do. Kuch cheezein pehle se nahi dikhti, isliye workbench ke disk aur memory par bhi ek CloudWatch alarm laga do, jaise Session 15 mein.

### [12:00 – 14:35] Scene 6: Lab: SSH Workbench Jodo
**[VISUAL: A second building in the private wing. `sudo apt install -y openjdk-17-jre git`, a folder `/home/ubuntu/jenkins`. Jenkins: Manage Nodes → New Node with label `linux-agent`, launch method SSH, credentials, host key verification. The node turns online. A pipeline with `agent { label 'linux-agent' }` prints the hostname of the workbench.]**

**(Voiceover):**
Lab. Private wing mein ek doosri Ubuntu building banao, `agent-sg` ke saath. `sudo apt install -y openjdk-17-jre git maven`, aur ek folder `/home/ubuntu/jenkins`. Jenkins mein Manage Nodes, New Node: naam, remote root directory, label `linux-agent`, launch method SSH, credentials mein private key, aur host key verification strategy. Node online ho jaaye to Jenkinsfile mein `agent { label 'linux-agent' }` aur ek stage `sh 'hostname; whoami; mvn -v'`. Log mein workbench ka hostname dikhega, controller ka nahi. Ab built-in node ke executors zero hain, aur saari builds yahin chalti hain. Ek workbench ko jaan boojh kar offline karo, aur dekho ki build queue mein kaise atakti hai. Aakhir mein extra building stop ya terminate karo.

### [14:35 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "controller plans, workbenches build · SSH / inbound / ephemeral · labels · executors ≈ cores · private wing + badge · disposable · stash for small, archive for big". Then a platform with a logo of an automation tool built into the vault appears.]**

**(Voiceover):**
Recap: Jenkins ka poora toolkit: conveyor, attachments, key cabinet, backup aur workbenches. Ab ek aur tareeka: ek conveyor jo vault ke andar hi bani ho, bina alag foreman ke. Agle session mein GitHub Actions aur DevSecOps, jahan security conveyor ka hissa ban jaati hai.

---

# 📎 Student handout: Session 19 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Multibranch | Branch aur PR ki apni conveyor; `BRANCH_NAME`, `CHANGE_ID`; orphan cleanup |
| `when` | `branch`, `changeRequest()`, `tag` multibranch mein chalte hain |
| Required check | Branch protection mein Jenkins ka check; laal check par merge nahi |
| Fork ka khatra | Trust: Contributors ya Nobody; Jenkinsfile trusted revision se |
| Credentials | Type aur scope; chhota scope; `withCredentials`; single quotes |
| Masking | Parda hai, taala nahi; ulta ya hex chhapne se tootta hai |
| Admin | Script Console se saari chaabiyan padh sakta hai |
| AWS access | Duty badge, lambi access key nahi |
| Hardening | Login, anonymous band, role ya matrix, 0 executors, HTTPS, CSRF, updates |
| `JENKINS_HOME` | `config.xml`, `jobs/`, `credentials.xml`, `secrets/`, `plugins/`; skip `workspace/`, `caches/` |
| Backup | tar + S3 (lifecycle), ya alag EBS + snapshot (quiet down), ya AMI |
| Restore | Stop, extract, `chown -R jenkins:jenkins`, start; mahine mein ek drill |
| Upgrade | Backup, test copy, LTS, pinned `plugins.txt` |
| Config as Code | `jenkins.yaml`; secrets bahar se |
| Agent | SSH, inbound, ephemeral; Java chahiye; disposable AMI |
| Labels, executors | `agent { label }`; executors ≈ cores |
| Private wing | `agent-sg` port 22 sirf `jenkins-sg` se; NAT; duty badge |
| `stash` | Chhote natije; bade natije archive ya S3 |
| Safai | Extra buildings, test snapshots, purane backups |

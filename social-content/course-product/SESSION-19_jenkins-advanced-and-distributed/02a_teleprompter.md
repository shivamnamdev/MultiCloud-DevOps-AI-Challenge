# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-19_jenkins-advanced-and-distributed

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,588 · **Episodes:** 4

---

# EPISODE 1: Har Branch ki Apni Conveyor

## Har Draft ke liye Naya Job?

Session 16B mein Atithi ke designers har kaam ke liye alag draft, yaani branch, banate hain. Agar har draft ke liye foreman ke daftar mein haath se naya job banana pade, aur merge hone ke baad use hatana bhi yaad rakhna pade, to chalta nahi: ek mahine mein chaalis purane jobs ka kachra. Multibranch Pipeline is kaam ko khud sambhalta hai. Wo vault ko scan karta hai, har branch aur har pull request ke liye ek alag conveyor banata hai, aur branch hatne par us conveyor ko bhi hata deta hai.

## Multibranch Kaise Kaam Karta Hai

Multibranch project mein aap vault ka repo aur credentials batate ho, aur kaun si cheezein dhoondhni hain: branches, origin ke pull requests, aur forks ke pull requests. Jenkins har branch mein Jenkinsfile dhoondhta hai, aur jahan mile wahan ek conveyor banata hai. Isme Jenkins ko branch ka naam pata hota hai, BRANCH_NAME, aur pull request ka number, CHANGE_ID. Isiliye ab when { branch 'main' } aur when { changeRequest() } chalte hain, jo Session 18 mein aam job mein kaam nahi karte the. Scan ko webhook se trigger karo, aur ek periodic scan bhi rakho, jo kisi chhooti hui ghanti ko pakad le. Aur "Orphaned item strategy" se purane branches ki conveyors ek tay samay baad apne aap saaf ho jaati hain.

## Pull Request par Check aur Master par Taala

Jenkins ka natija vault ke pull request par ek check ki tarah dikhta hai. Ab Session 16B ke master par taale ko is check se jodo. Branch protection mein "Require status checks to pass before merging" on karo, aur Jenkins ka check chuno. Check ke naam console mein dikhte hain, jaise continuous-integration/jenkins/pr-merge. Phir jab tak conveyor hari na ho, merge ka button grey rahega. Yahi CI ka asli faayda hai: kharab revision master tak pahunchta hi nahi, aur chief architect ko review mein ye pata hota hai ki inspection pass ho chuka hai. Isse reviewer ka samay kaam ki cheezon mein jaata hai.

## Fork ka Khatra

Ek khaas khatra yaad rakho. Pull request ke saath uski Jenkinsfile bhi aati hai, aur Jenkins use chalata hai. Agar baahar ka koi contractor, yaani fork wala, apni pull request mein Jenkinsfile badal de, aur usme key cabinet ki chaabiyan print karne wali line daal de, to Jenkins use chala sakta hai. Isliye forks ke liye trust setting ka dhyaan: sirf "Contributors" ya "Nobody" rakho, "Everyone" nahi. Aur pull request ki conveyor ko credentials mat do, jab tak wo vishwaaspaatr na ho. Ek aur surakshit tareeka: Jenkinsfile hamesha target branch, yaani trusted revision, se lo, pull request se nahi.

## Branch ke Hisaab se Behaviour

Multibranch ka ek aur faayda: ek hi Jenkinsfile alag alag branches par alag alag kaam kar sakti hai. Har branch aur pull request par sirf Build aur Test. Master par Package aur staging ka Deploy. Aur Session 16B ki release ki mohar, yaani tag, jaise v1.2.0, when { tag 'v*' } se ek Release station chala sakti hai. Isse jo kaam khatarnak hai, wo sirf bharose ki jagah par hota hai. Aur ek aadat: har station ka log sirf ek hi branch ka dikhe, taaki ek branch ka kharab build doosre ki halat na bigaade. Ye tag, aage Docker mein, image ke tag banenge, jo hum Session 22 mein dekhenge.

## Lab: Multibranch Setup

Lab. Ek naya Multibranch Pipeline banao, source vault ka repo, credentials ke saath. "Scan Repository Now" dabao, aur dekho ki main ke saath jitni branches hain, utni conveyors ban gayi. Ab ek branch feature/demo banao, chhota change karo aur pull request kholo. Jenkins ka check pull request par dikhega. Ek test jaan boojh kar tod do, aur check laal hote dekho. Phir use theek karo aur check hara hote dekho. Ab branch protection mein ye check required karo, aur dekho ki laal check par merge nahi hota. Aakhir mein feature/demo ko merge karke hatao, aur dekho ki agli scan par Jenkins ki folder se uski conveyor ghaib ho jaati hai.

## Recap aur Bridge

Recap: multibranch, pull request ke checks, aur fork ka khatra. Ab key cabinet: Jenkins mein secrets aur uski suraksha.

---

# EPISODE 2: Key Cabinet aur Foreman ki Suraksha

## Password Log mein Print Ho Gaya

Ek developer ne debug karne ke liye echo $DOCKER_PASSWORD likh diya, aur password build log mein, sabko dikhta hua. Jenkins ek aisa server hai jo aapke code, cloud ki chaabiyan, aur production tak ke raaste chhoota hai. Agar foreman ka daftar kamzor hua, to poora head office khatre mein. Isliye key cabinet aur Jenkins ki suraksha uska sabse zaroori hissa hai. Session 17 mein humne quotes ka jaal dekha tha. Aaj poori tasveer.

## Key Cabinet ka Sahi Upyog

Jenkins ki key cabinet mein secrets alag alag type ke hote hain: username aur password, secret text, SSH private key, secret file, certificate. Har ek ka ek ID hota hai, aur ek scope. System scope ki chaabi sirf Jenkins ke apne kaam ke liye, global sab conveyors ke liye, aur folder scope sirf ek folder ki conveyors ke liye. Jitna chhota scope, utna achha. Conveyor mein withCredentials se chaabi ek variable ban jaati hai, aur Jenkins use log mein kar deta hai. Ek hi shart: single quotes. sh 'curl ... $TOKEN', jisse shell variable padhe, Jenkins nahi, jaisa Session 17 mein dekha.

## Masking Pakki Suraksha Nahi

Masking ek parda hai, taala nahi. Jenkins log mein secret ka seedha text dhundh kar kar deta hai. Naye Jenkins base64 wali copy bhi chhupa dete hain, par agar koi parchi secret ko ulta, har akshar ke beech jagah daal kar, ya hex mein chhaap de, to wo poora dikh jaata hai, kyunki Jenkins ko wo secret nahi lagega. Aur ek badi baat: Jenkins ka admin Script Console se saari chaabiyan clear text mein padh sakta hai. Matlab, admin hona poore key cabinet ka maalik hona hai. Isliye admin kam logon ko, aur jo conveyor secret use karti hai uska Jenkinsfile bhi review se hi badle, jaisa Session 18 ke trusted library mein. Pehli suraksha secrets ko print na karna hai, doosri unhe kam se kam jagah rakhna.

## Lambi Chaabi Nahi, Duty Badge

Sabse achhi chaabi wo hai jo hai hi nahi. Maan lo conveyor ko S3 mein finished unit rakhna hai, ya SNS par alert bhejna hai. Pehla tareeka: Session 9 ki access key banao aur key cabinet mein rakho. Wo lambi chaabi hai: jab tak koi use badle nahi, wo chalti rehti hai, aur leak ho sakti hai. Doosra tareeka: Jenkins ki workbench, yaani EC2 building, ko ek duty badge pehna do, jisme sirf zaroori ijaazat ho, jaise ek bucket ke ek prefix mein likhna. Phir koi chaabi key cabinet mein hai hi nahi, aur AWS CLI badge khud utha leta hai. Jo chaabiyan baahar ki service ke liye hoti hain, jaise Slack ya GitHub, unhe key cabinet mein rakho aur rotate karne ka plan banao.

## Foreman ke Daftar ki Suraksha ka Checklist

Foreman ke daftar ka checklist. Ek, login zaroori, anonymous read band. Security Realm mein ya Jenkins ka apna database, ya LDAP ya single sign-on, jo company mein ho. Do, Authorization: matrix ya role-based, taaki har insaan ko sirf utna mile jitna kaam ke liye chahiye. Teen, builds controller par nahi: built-in node ke executors zero rakho, aur saare builds workbenches par. Jab chhote setup mein controller par chalte hain, to wahi machine jahan key cabinet rakhi hai, har kisi ke code ko chalti hai. Chaar, HTTPS, jaise Session 18 mein. Paanch, CSRF protection on, aur agent se controller ka access control on. Chhe, Jenkins aur plugins ko update rakho. Saat, Jenkins ka URL seedha internet par khula mat chhodo.

## Lab: Secret Safe Conveyor

Lab. Ek Secret text credential banao, ID demo-token. Conveyor mein:

Log mein length dikhegi, aur echo "TOKEN" ki jagah . Ab ek aur parchi likho jo echo "TOKEN" | rev chalaye, aur dekho ki masking ka parda yahan kaise tootta hai. Base64 try karoge to wo bhi chhupa milega. Phir Manage Jenkins, Nodes mein built-in node ke executors ko zero karo, aur dekho ki build ab "Waiting for next available executor" mein atak jaati hai. Agle episodes mein hum workbench jodenge, tab chalegi. Aakhir mein apne account se kisi bhi ek credential ka scope check karo: global hai ya folder?

## Recap aur Bridge

Recap: key cabinet, masking ki seema, aur foreman ke daftar ki suraksha. Ab ek sawaal jo kabhi na kabhi poochna padta hai: agar foreman ka server kal gir jaaye?

---

# EPISODE 3: Foreman ke Records ka Backup

## Server Gaya, Saare Jobs Gaye

Jenkins ka server kharab hua, ya kisi ne galti se terminate kar diya. Saath mein saare jobs, users, plugins aur chaabiyan. Agar backup nahi tha, to mahino ka kaam gaya. Lekin ek achhi baat hai: Session 17 ke baad aapki conveyor Jenkinsfile mein, yaani vault mein hai. Isliye kam se kam conveyors bach jaati hain. Jo nahi bachta wo hai Jenkins ki apni config, users, key cabinet aur build ka history. Is sab ka ghar ek hi folder hai, aur use samajhna backup aur restore ki neev hai.

## JENKINS_HOME mein Kya Hai

JENKINS_HOME, aam taur par /var/lib/jenkins, mein sab kuch hai: global config.xml, jobs/ jisme har job ka config aur build ka history, plugins/, users/, nodes/, aur key cabinet ka credentials.xml. secrets/ folder sabse sensitive hai, kyunki uske bina credentials.xml ki chaabiyan khul hi nahi sakti. Isliye backup mein secrets/ zaroor rakho, par backup khud encrypted ho aur bahut kam logon ki pahunch mein ho. workspace/ aur caches/ backup mein nahi chahiye, kyunki wo phir se ban jaate hain aur bahut bade hote hain. Aur ek aur jaankari: Jenkins ke andar ki config ko code mein rakhne ka tareeka Configuration as Code hai, jisme ek jenkins.yaml mein security realm, nodes aur plugins likhe jaate hain. Secrets us file mein nahi, environment ya secret store se aate hain.

## Teen Tareeke aur Ek Niyam

Tareeke teen hain. Ek, roz raat JENKINS_HOME ka tar archive, workspace aur cache hata kar, ek S3 bucket mein, jis par Session 12 ka lifecycle rule ho, jaise chaudah din baad purane hatao. Do, JENKINS_HOME ko ek alag EBS volume par rakho, /var/lib/jenkins par mount karo, jo Session 5B ke fstab mein Session 10 ke nofail ke saath ho, aur us volume ka roz ek snapshot lo. Snapshot se pehle Jenkins ko "Prepare for shutdown" ya quiet down kar do, taaki beech mein koi build file na likh raha ho. Teen, bade badlaav ke baad poori building ka AMI. Aur ek niyam: jis backup ko aapne kabhi restore nahi kiya, wo ek ummeed hai, backup nahi.

## Upgrade ki Aadat

Upgrade ki ek chhoti aadat. Pehle backup. Phir us backup se ek test copy banao, doosri building par. Upgrade pehle us par karo, aur kuch zaroori conveyors chalao. Sab theek ho tabhi asli foreman par. Jenkins ke do raaste hain: LTS, jo sthir hai aur jise production ke liye chuna jaata hai, aur weekly, jo har hafte naya hai. Atithi LTS par rahega. Plugins ke versions ko ek plugins.txt mein likh sakte ho, aur jenkins-plugin-cli se install, taaki test aur asli foreman ek hi plugins par chalen. Aur wahi Session 10 ka sabak: jo cheez haath se banti hai, use ek dusri building par dobara banane ka ek likha hua tareeka rakho.

## Lab: Backup Parchi aur Restore Test

Lab. Ye Session 6 ki parchi ka naya rup hai:

Building ko S3 mein likhne ka duty badge do, access key nahi. Isko cron se roz chalao, flock ke saath, jaise Session 6 mein. Ab restore test: ek doosri building par wahi Jenkins version install karo. sudo systemctl stop jenkins, backup ko /var/lib mein extract karo, sudo chown -R jenkins:jenkins /var/lib/jenkins, aur sudo systemctl start jenkins. Check karo ki jobs, users aur credentials wapas aa gaye. Test ke baad extra building hata do, aur purane backups ko lifecycle rule se chaudah din ke baad hatao.

## Recap aur Bridge

Recap: foreman ke records ka ghar, uska backup, aur upgrade ki aadat. Ab ek aur sawaal: ek akela foreman ek akeli workbench par sab kuch kab tak banayega?

---

# EPISODE 4: Workbenches

## Ek Workbench, Bees Order

Ab Atithi ke paas dus services hain, aur har revision par conveyor chalti hai. Ek workbench par saari builds ek ke peeche ek, aur ek bhaari build baaki sabko rok deti hai. Isi liye Session 17 mein hum ne controller aur workbench alag kiye the. Distributed build mein foreman sirf tay karta hai ki kaun sa kaam kis workbench par jaayega, aur asli fabrication workbenches, yaani agents, par hoti hai. Aur Episode 2 mein humne controller ke executors zero kiye the, to ye ab seedhi zaroorat hai.

## Workbench Jodne ke Tareeke

Workbench ek machine hai, jisme Java ho, aur jo foreman se jud sake. Teen tareeke. SSH: foreman workbench par login karta hai. Isme workbench par SSH ki chaabi aur uska security group chahiye. Inbound: workbench khud foreman se jud jaati hai, agent.jar aur ek secret ke saath, jo tab kaam aata hai jab workbench firewall ke peeche ho aur foreman use dekh na sake. Aur ephemeral agents: har build ke liye ek nayi workbench apne aap banti hai, EC2 ya container se, aur build ke baad gayab ho jaati hai. Aakhri tareeka sabse saaf hai, kyunki purani build ka kuch bacha hi nahi. Kubernetes par yehi kaam aage Session 23 aur 25 mein dikhega.

## Labels aur Executors

Labels se tay hota hai ki kaam kahan jaaye. Workbench par labels linux, maven, docker lagao, aur Jenkinsfile mein agent { label 'docker' }. Ya agar Docker Pipeline plugin ho to agent { docker { image 'maven:3-eclipse-temurin-17' } }, jisme har build ke liye ek saaf container milta hai, jisme Maven aur Java pehle se hain, aur workbench par kuch install nahi karna. Executors ka matlab hai ki ek workbench par kitne kaam ek saath chalen. Aam niyam: lagbhag CPU cores ke barabar. Isse zyada rakhoge to build dheemi hongi aur memory khatam hogi, jo Session 5 ki top ki kahani hai.

## Private Wing mein Workbench

Session 14 ka naksha yahan kaam aata hai. Workbenches ko private wing mein rakho, bina public IP ke. Unke door guard, agent-sg, ki list mein port 22 sirf jenkins-sg se, kisi IP list se nahi. Dependencies download karne ke liye private wing ki direction board dispatch desk, yaani NAT gateway, ki taraf ho. Aur har workbench par ek duty badge, jisme sirf wahi ijaazat jo build ko chahiye. Isse workbench ke paas koi chaabi bhi nahi aur koi bahar se aa bhi nahi sakta. Aur design ke niyam: workbench disposable ho, ek AMI ya launch template se bani, tools sab jagah ek jaise, aur us par secrets store nahi. "Mere workbench par to chal raha tha" wali bimari isi se jaati hai.

## Jab Workbench Aati aur Jaati Hai

Jab ek conveyor ke alag stations alag workbenches par chalte hain, to ek workbench ki files doosri par nahi hotin. Isliye stash aur unstash: ek station ke natije chhote paimane par rakho aur doosre station mein utha lo. Bade natije, jaise finished unit, archiveArtifacts ya S3 mein rakho, stash mein nahi. Aur ek workbench build ke beech mein offline ho sakti hai. Isliye conveyor mein timeout aur zaroorat par retry rakho, aur Jenkins ke Node monitors ko disk kam hone par workbench ko apne aap offline karne do. Kuch cheezein pehle se nahi dikhti, isliye workbench ke disk aur memory par bhi ek CloudWatch alarm laga do, jaise Session 15 mein.

## Lab: SSH Workbench Jodo

Lab. Private wing mein ek doosri Ubuntu building banao, agent-sg ke saath. sudo apt install -y openjdk-17-jre git maven, aur ek folder /home/ubuntu/jenkins. Jenkins mein Manage Nodes, New Node: naam, remote root directory, label linux-agent, launch method SSH, credentials mein private key, aur host key verification strategy. Node online ho jaaye to Jenkinsfile mein agent { label 'linux-agent' } aur ek stage sh 'hostname; whoami; mvn -v'. Log mein workbench ka hostname dikhega, controller ka nahi. Ab built-in node ke executors zero hain, aur saari builds yahin chalti hain. Ek workbench ko jaan boojh kar offline karo, aur dekho ki build queue mein kaise atakti hai. Aakhir mein extra building stop ya terminate karo.

## Recap aur Bridge

Recap: Jenkins ka poora toolkit: conveyor, attachments, key cabinet, backup aur workbenches. Ab ek aur tareeka: ek conveyor jo vault ke andar hi bani ho, bina alag foreman ke. Agle session mein GitHub Actions aur DevSecOps, jahan security conveyor ka hissa ban jaati hai.

# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-17_jenkins-foundations

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,475 · **Episodes:** 4

---

# EPISODE 1: Foreman kyun

## Friday Shaam ki Integration

Atithi ke paanch designers do hafte tak apni apni copy par booking site ka kaam karte hain. Release ki Friday ko sab ki copies milaai jaati hain. Ek ka naya rate table, doosre ka naya payment button, teesre ka naya form. Kuch bhi saath nahi chalta, aur Friday ki shaam ek bhi booking test nahi ho pati. Session 16 mein humne register aur branches seekhe, jo is mushkil ko sambhalte hain. Par ek aur aadat chahiye: kaam ko roz, balki din mein kai baar, milao, aur har baar check karo ki sab saath chalta hai. Is aadat ka naam Continuous Integration hai.

## CI ka Matlab: Roz Milao, Roz Jaancho

CI ka matlab hai: designer apni revision vault mein bhejta hai, aur workshop turant use uthati hai, finished unit banati hai, inspection karti hai, aur team ko batati hai ki sab theek hai ya kuch toota. Teen faayde. Galtiyan jaldi pakdi jaati hain, jab unka kaaran chhota aur taaza hota hai, kyunki ek hi change ki jaanch hai, paanch hafton ki nahi. Fabrication har baar ek jaise saaf mahaul mein hoti hai, "mere laptop par to chal raha tha" wali baat nahi. Aur team ko release se darr nahi lagta. CI ek tool ka naam nahi, ek aadat ka naam hai. Jenkins uske liye ek bahut purana aur bharosemand tool hai.

## Kaun Kya Kaam Karta Hai

Jenkins ek open source automation server hai, Java mein bana hua. Uska controller foreman ka daftar hai: wo UI dikhata hai, jobs ko schedule karta hai, aur plugins sambhalta hai. Asli fabrication workbenches par hoti hai, jinhe agents kehte hain. Chhote setup mein foreman khud bhi kaam kar leta hai, par asli workshop mein foreman sirf plan banata hai aur workbenches kaam karti hain. Isse hum Session 19 mein dekhenge. Jenkins ki taakat uske hazaaron plugins hain, yaani foreman ki attachments. Par har attachment ek aur cheez hai jise update aur surakshit rakhna padta hai. Isiliye jo zaroori ho wahi lagao.

## Local Hook se Bell tak

Session 16 ke hooks yaad hain? Designer apni laptop par ek pre-push hook se tests chala sakta tha. Wo ek local jaancha hai: sirf us designer ke liye, aur wo use band bhi kar sakta hai. CI uska shared roop hai. Vault mein revision aate hi vault workshop ki ghanti bajata hai, aur foreman sab ke liye ek hi tarah ki jaancha chalata hai, jise koi chhod nahi sakta. Is ghanti ko webhook kehte hain, aur wo hum Session 18 mein jodenge. Aaj ke liye bas itna: pehle haath se foreman ko kaam dena seekhenge, phir use ghanti se jodenge.

## Lab: Foreman ka Daftar Taiyaar Karo

Lab ki taiyaari. Ek Ubuntu building lo, EC2 ya apni VM, kam se kam do GB RAM, jaise t3.small. Naam ka tag jenkins-lab lagao, Session 8 ki tarah. sudo apt update && sudo apt install -y openjdk-17-jre git maven chalao (Jenkins ke naye versions Java 17 ya 21 maangte hain, Java ka version Jenkins ke docs se milao), aur java -version aur mvn -v se check karo. Jenkins ke supported Java versions release ke saath badalte hain, isliye install se pehle official documentation dekh lo. Jenkins ka default port 8080 hai. Security group mein 8080 sirf apne IP se kholo, poori duniya ke liye nahi. Session 14 ka niyam yahan bhi: jo darwaza staff ke liye hai, use sabke liye mat kholo.

## Recap aur Bridge

Recap: CI ek aadat hai, Jenkins uska ek tool. Foreman ka daftar aur workbenches. Ab foreman ko hire karte hain: install, pehla unlock aur pehla job.

---

# EPISODE 2: Foreman ko Hire Karo

## Pandrah Minute mein Workshop

Ek CI server banane mein kitna samay lagta hai? Aaj ke tools ke saath, paandrah minute. Hum Jenkins ko Ubuntu par install karenge, uska pehla login karenge, aur ek simple job chalayenge. Lekin pehle ek chetavni. Jenkins aisa server hai jo aapka code, cloud ki chaabiyan aur production tak ka raasta chhoo sakta hai. Agar foreman ke daftar ka darwaza kamzor raha, to poora head office khule mein hai. Isliye install ke saath hi security ki soch shuru hoti hai, baad mein nahi.

## Install: Official Raaste se

Install ke liye Jenkins ki official documentation ke commands use karo, kyunki repository aur signing key ke details badalte rehte hain. Install ke baad sudo systemctl enable --now jenkins, aur systemctl status jenkins se dekho ki chal raha hai. Pehla password sudo cat /var/lib/jenkins/secrets/initialAdminPassword mein hota hai. Browser mein http://SERVER_IP:8080 kholo, password daalo, "Install suggested plugins" chuno, aur apna admin user banao. Uske baad wo pehla password dobara kaam nahi aata, apna user istemaal karo. Aur agar page nahi khulta, to Session 5 ka kram: ss -tlnp | grep 8080 se service sun rahi hai ya nahi, phir security group.

## Jenkins ek Service Hai, aur ek User

Ab dekho ki Jenkins asli mein hai kya. Wo ek systemd service hai, bilkul Session 5 ki apache ya nginx ki tarah. Aur wo jenkins naam ke ek system user ke naam par chalta hai, jo Session 4 ka uniformed service staff hai: ek hi kaam, koi login nahi. Uska ghar /var/lib/jenkins hai, jise JENKINS_HOME kehte hain, aur uski ownership jenkins ke paas hai. Saare jobs, plugins, users aur chaabiyan wahin rehti hain. Iska ek seedha matlab: jab Jenkins koi command chalata hai, wo jenkins user ki tarah chalti hai. Agar kisi tool ka PATH ya permission jenkins ke liye theek nahi, to haath se sudo -u jenkins mvn -v chalakar dekho. Aur Jenkins ke logs journalctl -u jenkins mein hain.

## Job aur Freestyle Job

Job foreman ko diya hua ek kaam ka vivaran hai. Freestyle job sabse saral hai: ek form mein aap batate ho ki code kahan se aayega aur kaun si commands chalani hain. "Execute shell" step mein echo "Hello from Jenkins" aur date. "Build Now" dabao, aur Console Output mein dekho. Har run ko ek build number milta hai, aur Jenkins uska log aur result yaad rakhta hai. Nila ball matlab pass, laal ball matlab fail. Har build ka apna workspace folder hota hai, JENKINS_HOME/workspace/hello-job, jahan code utarta hai. Freestyle seekhne ke liye achha hai, par ek kamzori jaldi dikhegi, jo Episode 4 mein hal hogi.

## Exit Code aur Parameter

Ek job ko ek hi kaam mein bandh kar rakhna zaroori nahi. "This project is parameterised" mein ek String parameter NAME jodo, aur shell step mein echo "Hello, $NAME" likho. "Build with Parameters" se chalao, aur har baar alag naam do. Ab ek build jaan boojh kar fail karo, exit 1 likhkar, aur dekho ki ball laal ho gaya. Session 6 ka sabak yahan seedhe kaam aata hai: Jenkins shell step ke exit code ko dekhta hai. Zero matlab pass, koi bhi aur number matlab fail. Isliye hamari bash parchiyan jo galti par non-zero exit karti hain, wahi Jenkins ko batati hain ki kuch toota. Aur set -e ya set -euo pipefail ki aadat yahan kaam aati hai.

## Lab: Pehla Job aur Parameter

Lab. Ek freestyle job hello-job banao, parameter NAME, aur shell step mein echo "Hello, $NAME"; hostname; whoami. "Build with Parameters" se chalao. Log mein server ka hostname dikhega, aur whoami ka jawab jenkins hoga, jo Scene 3 ki baat pakki karta hai. Ab step mein ls /root jodo aur dekho ki kyun fail hota hai: jenkins user ko wahan ki ijaazat nahi, aur wahi least privilege hai. Aakhir mein ek build exit 1 se fail karo aur Console Output padhna seekho: sabse neeche se, ek line upar. Aur kaam ke baad building ko stop kar do, terminate nahi.

## Recap aur Bridge

Recap: Jenkins install, jenkins user, freestyle job aur exit code. Ab asli kaam: vault se blueprint uthakar uski finished unit banana.

---

# EPISODE 3: Blueprint se Finished Unit

## Java Service Banti Kaise Hai

Atithi ki booking-service Java mein hai. Java service ko chalne layak banana ek chhota kaam nahi: code compile karo, tests chalao, dependencies jodo, aur ek .jar file banao. Maven ye sab ek standard tareeke se karta hai, aur ek hi file se, pom.xml. Jenkins aur Maven ki jodi Java projects mein bahut aam hai. Agar aapka project Python mein hai, to wahi conveyor chalegi: pip install -r requirements.txt, phir pytest, jo humne Session 7 mein seekha tha. Tool alag, conveyor wahi. Isliye is session ki jo baatein Maven ke naam par hain, unhe apne tool par laagu karna aasaan hai.

## pom.xml aur Lifecycle

pom.xml mein project ka naam, version aur dependencies likhi hoti hain. Maven dependencies khud download karta hai. Build ka ek tay kram hai, jise lifecycle kehte hain: compile, test, package aur aage. mvn clean package purane build ko saaf karta hai, aur phir naya .jar banata hai, aur agar koi test fail ho to wahin ruk jaata hai. Output target/ folder mein milta hai: .jar aur surefire-reports/, jisme har test ka result hota hai. -B ka matlab batch mode, jisme progress ke bar nahi aate aur log saaf rehta hai. -DskipTests ek option hai, par CI mein tests chhod dena aam taur par buri aadat hai.

## Git se Code, Credentials se Chaabi

Job mein Source Code Management mein Git chuno aur vault ka URL aur branch do. Agar repository private hai, to Jenkins ko ek pass chahiye. Do saaf tareeke hain. Ek, personal access token, jise Credentials mein rakho. Do, ek deploy key: ek SSH key ka joda, jisme public hissa vault par read-only lagta hai, aur private hissa Jenkins ke Credentials mein. Ye Session 4 ka SSH key ka hi dusra roop hai. Dono mein ek rule: chaabi ya token URL mein ya Jenkinsfile mein kabhi nahi likhte. Aur ek chhoti baat: Jenkins ko ye bhi tay karna padta hai ki kab check kare. Abhi ke liye "Poll SCM" mein H/5 * * * *, jiska matlab hai har paanch minute mein, par H ek hash hai jo saari jobs ko ek hi second par ek saath tootne se rokta hai. Asli ghanti, webhook, Session 18 mein.

## Inspection ki Report aur Finished Unit

Build ka mat sirf "pass ya fail" nahi hota. Jenkins ek JUnit report utha sakta hai: target/surefire-reports/.xml. Isse build page par test result ka graph aata hai, aur kaun sa test kab tootna shuru hua, ye dikhta hai. Ek nuance: agar report publish ho par kuch tests fail hon, aur build ko -Dmaven.test.failure.ignore ke saath chalayein, to Jenkins use peela maanta hai, yaani unstable. Seedhe Maven fail ho jaaye, to laal. Aur finished unit ko shelf par rakhne ke liye "Archive the artifacts" mein target/.jar. Fingerprint on rakho, taaki baad mein pata chale ki ye jar kis build se bani thi. Workspace to kabhi bhi saaf ho sakta hai, finished unit nahi.

## Lab: booking-service ki Pehli Fabrication

Lab. Vault par ek chhota Maven repo lo, jisme kuch unit tests hon, jaise ek function jo check-in aur check-out se raaton ki ginti nikaale. Agar aapke paas apna nahi hai, to ek sample repo fork karo, jaise Session 16B mein fork karna seekha tha. Freestyle job booking-build banao, Git source, aur shell step mvn -B clean package. Post-build mein JUnit report aur target/*.jar archive karo. Pehli build chalao, jar dekho. Phir ek test jaan boojh kar tod do: assertEquals(3, nights) ko galat value de do, push karo, aur build dobara chalao. Build laal hoga, aur Console Output mein test ka naam aur line likhi hogi. Isi tarah CI aapki galti commit ke turant baad pakadta hai.

## Recap aur Bridge

Recap: Git se blueprint, Maven se finished unit, aur inspection ki report. Par ek kamzori bachi hai: ye saari settings foreman ke daftar ke form mein chhupi hain. Agle episode mein hum conveyor ko blueprint ke saath hi rakhna seekhenge.

---

# EPISODE 4: Conveyor ke Nirdesh

## Kisi ne Ek Checkbox Badal Diya

Ek subah build toot gaya. Kal tak theek tha. Pata chala ki kisi ne freestyle job ka ek checkbox badal diya. Kisne, kab aur kyun, kuch nahi pata, kyunki wo form mein chhupa tha. Aur agar foreman ka server kharab ho jaaye, to ye saari settings bhi gayi. Hal: conveyor ke nirdesh blueprint ke saath hi rakho. Ek file, Jenkinsfile, jo vault mein rehti hai. Uska poora register hota hai, uski chief architect review kar sakta hai, aur galti hone par ek purani revision par wapas jaa sakte ho. Session 16 ki saari aadatein ab conveyor par bhi laagu hoti hain.

## Declarative Pipeline ka Dhancha

Declarative pipeline ka dhancha seekho. Sabse bahar pipeline. Uske andar agent, jo batata hai kaun si workbench par chalega. options mein timeout jaise settings. stages mein kai stage, yaani stations, aur har station ke andar steps, jo asli commands hain, jaise sh 'mvn -B test'. Aur aakhir mein post, jo build ke ant mein chalta hai: always, success, failure. Ek aur blocks hain: environment variables ke liye, aur parameters, jaise freestyle ka parameter. Ek aadat: har stage ka naam aisa rakho ki sirf naam padhkar pata chale ki kahan atka. Isse "Build" ya "Test" laal hota hai, to aapko sidha pata hai ki fabrication mein dikkat hai ya inspection mein.

## Pipeline Job, aur Jenkinsfile Vault Se

Ab pipeline job banao, aur Definition mein "Pipeline script from SCM" chuno. Vault ka URL, branch, aur Script Path Jenkinsfile do. Is tarah Jenkinsfile Jenkins ke form mein nahi, repo ke andar rehti hai, pom.xml ke bagal mein. Jenkins har build se pehle use vault se uthata hai. Do madadgar cheezein. Pipeline Syntax ka snippet generator: aap form mein kuch chuno, aur wo ek step ka sahi code bana deta hai. Aur Replay: purane build ko thoda badal kar dobara chalane ka tareeka, bina commit kiye. Replay sirf try karne ke liye hai. Jo kaam kare, use Jenkinsfile mein commit karo.

## Secrets aur Quotes ka Jaal

Pipeline mein ek chhota jaal hai, jise sab seekhte waqt pakadte hain. Jenkinsfile Groovy mein hai, aur Groovy mein double quote wali string ke andar ka matlab Jenkins ka apna substitution hota hai. Isliye sh "echo TOKEN" mein Jenkins khud secret ko command mein likh deta hai, aur wo log mein aa sakta hai. Single quote mein, sh 'echo $TOKEN', Jenkins kuch nahi badalta aur shell variable ko sambhalta hai. Isliye secrets hamesha single quotes ke saath, aur credentials() ya withCredentials se lo, plain text mein kabhi nahi. Ye hum Session 19 mein Jenkins ki security ke saath poori tarah dekhenge. Aaj bas yaad rakho: secret ek, quote ek, aur kabhi print nahi.

## Lab: Build, Test, Package aur Archive

Lab. Apne booking-service repo ke root mein ye Jenkinsfile rakho:

Commit karke vault mein push karo. Pipeline job banao, "Pipeline script from SCM" ke saath, aur chalao. Stage View mein har station dekho. Phir ek test tod kar dekho: Test laal hoga, Package skip hoga, aur post failure ka message chalega. Ek test ko theek karke push karo aur dekho ki naya build hara hota hai.

## Pull Request ke Saath Jenkinsfile

Ab Jenkinsfile bhi blueprint ka hissa hai, to wahi niyam. Ek nayi station jodni ho, jaise lint, to ek branch banao, Jenkinsfile badlo, aur pull request kholo. Chief architect use review karta hai, jaise kisi bhi file ko. Merge hone ke baad agla build nayi conveyor se chalega. Aur agar nayi station ne sab toda, to Session 16 ki aadat: git revert se purani halat wapas. Har badlaav ka register hai: kisne, kab, kyun. Ye wahi cheez hai jo freestyle ke form mein nahi thi. Isi ko pipeline as code kehte hain, aur ye agle sessions ki neev hai.

## Recap aur Bridge

Recap: Jenkinsfile, declarative pipeline, stages aur post. Conveyor ab blueprint ke saath rehti hai, aur uske badlaav bhi review hote hain. Par abhi bhi koi insaan Build Now dabata hai ya Jenkins har paanch minute mein poochta hai. Agle session mein vault khud ghanti bajayega, aur conveyor mein parallel stations, plugins aur ek shared binder aayenge.

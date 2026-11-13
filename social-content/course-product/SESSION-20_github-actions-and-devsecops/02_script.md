# ✍️ 02: SCRIPT — SESSION-20: GitHub Actions & DevSecOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S20`
- **Focus:** GitHub Actions workflows/events/jobs, matrix/cache/artifacts, secrets & OIDC, DevSecOps layers (SAST, SCA, secrets scan, image scan)
- **Episodes:**
  - Episode 1: GitHub Actions: Workflow, Event, Job, Step
  - Episode 2: Faster aur Smarter: matrix, cache, artifacts
  - Episode 3: Secrets aur Keyless Deploy: OIDC
  - Episode 4: DevSecOps: Pipeline mein Security Gate

---

# 📺 EPISODE 1: GitHub Actions

### [00:00 – 01:15] Scene 1: CI Jo Repo ke Andar Rehta Hai
**[VISUAL: A repo with a `.github/workflows/ci.yml` file. A push triggers a green check on a commit. No separate server visible.]**

**(Voiceover):**
Jenkins mein aapko server chalana padta tha. GitHub Actions mein CI seedha aapke repo ke andar hai: ek YAML file `.github/workflows/` mein, aur GitHub aapke liye machines chalata hai. Chhote aur medium projects ke liye ye bahut sahulat wala tareeka hai. Aur ek baar concept samajh gaye, to har CI tool aasaan lagta hai.

### [01:15 – 05:00] Scene 2: Workflow ke Hisse
**[VISUAL: A YAML file with sections coloured: `name`, `on` (events), `jobs` → `build` → `runs-on`, `steps` (`uses` actions and `run` commands). A diagram: Event → Workflow → Jobs (parallel) → Steps.]**

**(Voiceover):**
Workflow ek YAML file hai. `on` batata hai ki kaun si event se chalega, jaise `push` ya `pull_request`. `jobs` mein kaam, jo default mein parallel chalte hain, aur har job ke paas `runs-on`, jaise `ubuntu-latest`, ek fresh machine. Job ke andar `steps`: ya to `run` se shell command, ya `uses` se koi ready-made action, jaise code checkout karne ke liye `actions/checkout`. Dhyaan: action ko version ke saath use karo, aur sensitive workflows mein commit SHA se pin karna sabse surakshit hai.

### [05:00 – 08:30] Scene 3: Pehla Workflow
**[VISUAL: A `ci.yml` file for a Python project: checkout, setup-python, install deps, run tests. A "Actions" tab with a green run and logs per step.]**

**(Voiceover):**
Ek simple Python CI:
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
Push karte hi Actions tab mein run dikhta hai, har step ka log ke saath. Fail hone par PR par laal cross dikhta hai.

### [08:30 – 11:30] Scene 4: Lab: Apna CI Banao
**[VISUAL: A small Python repo with `test_app.py`. Add the workflow file, push, watch it run green. Break a test, see red.]**

**(Voiceover):**
Lab: ek chhota repo banao jisme `app.py` mein ek function, aur `test_app.py` mein ek `pytest` test. `.github/workflows/ci.yml` mein upar wala workflow rakho. Push karo aur Actions tab dekho. Ab test tod kar push karo aur PR mein laal check dekho. Branch protection mein is check ko required karo. Ab aapke repo ne khud ko test karna seekh liya.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "on · jobs · runs-on · steps · uses/run · pin actions".]**

**(Voiceover):**
Recap: workflow, jobs, steps. Ab ise tez aur smart banate hain.

---

# 📺 EPISODE 2: Faster aur Smarter — matrix, cache, artifacts

### [00:00 – 01:15] Scene 1: 12 Minute ka CI, Roz 40 Baar
**[VISUAL: A CI run bar showing "12 min" with a repeating "pip install" segment taking 4 min. A cache hit cuts it to 8 min.]**

**(Voiceover):**
Agar aapka CI 12 minute leta hai aur roz 40 baar chalta hai, to team ka bahut samay kaam hone ki jagah intezaar mein jaata hai. Teen tareeke se hum ise tez banayenge: cache, matrix aur sahi artifacts.

### [01:15 – 05:00] Scene 2: Matrix aur Cache
**[VISUAL: A `strategy.matrix` with `python: ['3.11','3.12']` and `os: [ubuntu-latest, windows-latest]` expanding into 4 parallel job boxes. A cache step keyed by hash of requirements file.]**

**(Voiceover):**
Matrix ek job ko kai combinations par chalata hai: do Python versions aur do operating systems, to chaar parallel jobs. Isse compatibility test hoti hai. Cache mein dependencies ko save karte hain, key requirements file ke hash se, taaki jab file nahi badli to download dobara na ho: `actions/setup-python` mein `cache: pip` jaise options isse aasaan bana dete hain. Aur `concurrency` se purane duplicate runs cancel kar sakte ho.

### [05:00 – 08:30] Scene 3: Artifacts aur Job Dependencies
**[VISUAL: Job `build` uploads `dist/` with `actions/upload-artifact`. Job `deploy` has `needs: build` and downloads the artifact. A conditional `if: github.ref == 'refs/heads/main'`.]**

**(Voiceover):**
Ek job ke output ko doosre job ko dena ho to artifacts. `upload-artifact` se build ka result save karo, aur doosre job mein `download-artifact`. `needs: build` batata hai ki deploy job tab chalega jab build pass ho. `if: github.ref == 'refs/heads/main'` se deploy sirf main par chalta hai. Jab main par hi release karna ho, to environment protection se manual approval bhi jod sakte ho.

### [08:30 – 11:30] Scene 4: Lab: Matrix + Cache
**[VISUAL: The previous workflow upgraded: matrix of Python versions, `cache: pip`, and an artifact upload of test results. The run page shows 2 parallel jobs and "Cache restored" in the logs.]**

**(Voiceover):**
Lab: pichle workflow ko badlo: `strategy: matrix: python: ['3.11','3.12']`, aur `python-version: ${{ matrix.python }}`. `setup-python` mein `cache: pip` jodo. Ek step mein pytest ka report `--junitxml=report.xml` se banao aur `upload-artifact` se save karo. Do baar push karo: doosri baar log mein "Cache restored" dikhega aur run tez hoga. Artifacts ko run page se download karke dekho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "matrix = many combos · cache keyed by lockfile · artifacts · needs + if".]**

**(Voiceover):**
Recap: matrix, cache, artifacts. Ab deploy ke liye secrets, aur unhe bina long-lived keys ke use karne ka tareeka.

---

# 📺 EPISODE 3: Secrets aur Keyless Deploy

### [00:00 – 01:15] Scene 1: AWS Keys GitHub Secrets Mein, Phir Bhi Khatra
**[VISUAL: A repo secret `AWS_SECRET_ACCESS_KEY` stored. A malicious PR from a fork tries to print secrets. A shield blocks it. A long-lived key icon shown as a liability.]**

**(Voiceover):**
AWS keys ko GitHub Secrets mein rakhna sahi shuruaat hai, par ye ek long-lived key hai, jo kabhi leak ho sakti hai aur rotate karni padti hai. Zyada surakshit tareeka hai OIDC: GitHub aur AWS ek doosre par bharosa karte hain, aur har run ke liye temporary credentials milte hain, bina kisi stored key ke.

### [01:15 – 05:00] Scene 2: Secrets aur Environments
**[VISUAL: Settings → Secrets and variables → Actions: Repository secrets, Environment secrets, Variables. Usage `${{ secrets.NAME }}`. An environment "production" with required reviewers.]**

**(Voiceover):**
Secrets ko repository ya environment level par save karte hain, aur workflow mein `${{ secrets.NAME }}` se use karte hain. GitHub unhe logs mein mask karta hai. Fork se aane wale PRs ko secrets nahi milte, jo ek achha safety feature hai. Environments mein, jaise `production`, aap required reviewers laga sakte ho. Aur workflow ki permissions ko `permissions:` block se kam rakho, jaise `contents: read`, taaki token ko zyada power na mile.

### [05:00 – 08:30] Scene 3: OIDC se AWS
**[VISUAL: A sequence: Workflow requests an OIDC token from GitHub → presents it to AWS STS → STS checks the IAM role's trust policy (repo and branch) → returns temporary credentials. A YAML snippet with `permissions: id-token: write` and `aws-actions/configure-aws-credentials` with `role-to-assume`.]**

**(Voiceover):**
OIDC mein workflow GitHub se ek token maangta hai, use AWS ke saamne rakhta hai, aur AWS dekhta hai ki IAM role ki trust policy ke hisaab se ye repo aur branch allowed hai ya nahi. Allowed ho to temporary credentials milte hain. Workflow mein `permissions: id-token: write` aur `aws-actions/configure-aws-credentials` action ke saath `role-to-assume`. Trust policy mein repo aur branch ki shart zaroor likho, warna koi bhi repo wo role le sakta hai.

### [08:30 – 11:30] Scene 4: Lab: Secret aur Environment Approval
**[VISUAL: Create a repo secret `DEMO_TOKEN`. A workflow step prints its length. Add an environment `production` with a required reviewer; a deploy job waits for approval.]**

**(Voiceover):**
Lab: repo mein Secret `DEMO_TOKEN` banao, workflow mein `run: echo "len=${#DEMO_TOKEN}"` aur `env: DEMO_TOKEN: ${{ secrets.DEMO_TOKEN }}`. Phir ek environment `production` banao aur khud ko required reviewer rakho. Ek `deploy` job mein `environment: production` likho. Run karo: job approval par rukega, aur approve karne ke baad hi chalega. Agar AWS account hai, to OIDC provider aur ek role banane ki official guide follow karke try karo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "secrets masked · least permissions · environments approval · OIDC > static keys".]**

**(Voiceover):**
Recap: secrets aur keyless deploy. Ab pipeline mein security ke gate lagate hain, yani DevSecOps.

---

# 📺 EPISODE 4: DevSecOps

### [00:00 – 01:15] Scene 1: Security Aakhir mein Kyun?
**[VISUAL: A software timeline: Code → Build → Test → Deploy → Production. A security team stands at the far end with a "stop" sign, delaying release by weeks. Next: small security gates placed at each stage, early.]**

**(Voiceover):**
Purane tareeke mein security team release ke aakhir mein aati thi, aur ek bada issue mile to hafton ki deri. DevSecOps ka matlab hai security ko shuru se pipeline mein daalna, jise "shift left" kehte hain. Chhote chhote automatic checks, har commit par, taaki problem sasti mein pakdi jaye.

### [01:15 – 05:00] Scene 2: Security ke Layers
**[VISUAL: Four layers on a pipeline: Secrets scanning (Gitleaks), SAST (static code analysis, CodeQL/SonarQube), SCA (dependency vulnerabilities, Dependabot/OWASP Dependency-Check/pip-audit), Container image scan (Trivy), plus IaC scan (tfsec/Checkov).]**

**(Voiceover):**
Teen-chaar layers yaad rakho. Secrets scanning: kya kisi ne key commit kar di? Tool, jaise Gitleaks. SAST: apne code mein bugs ya insecure patterns, jaise CodeQL ya SonarQube. SCA: dependencies mein known vulnerabilities, jaise Dependabot ya pip-audit. Container image scanning: Docker image mein vulnerable packages, jaise Trivy. Aur infrastructure code ka scan, jaise Terraform ke liye Checkov ya tfsec. Har ek alag cheez pakadta hai, koi ek tool sab kuch nahi karta.

### [05:00 – 08:30] Scene 3: Gates, False Positives aur Priority
**[VISUAL: A scan report with severities: CRITICAL, HIGH, MEDIUM, LOW. A policy: fail on CRITICAL/HIGH with a fix available. A triage board with "accept risk (documented)" and "fix".]**

**(Voiceover):**
Har finding ko rok-tok se rokne par pipeline roz toot jaati hai aur team usse ignore karna seekh leti hai. Isliye gate sochkar lagao: CRITICAL aur HIGH, jinka fix available hai, un par build fail. Baaki ko report karo aur plan karo. False positives hote hain, aur kabhi kabhi risk accept karna padta hai, par uska karan aur samay seema likhi honi chahiye. Aur dependencies ko automatic update PR se taaza rakho, jaise Dependabot.

### [08:30 – 11:30] Scene 4: Lab: Security Job
**[VISUAL: A workflow with a `security` job: Gitleaks, `pip-audit`, and Trivy scan of the filesystem or image. A deliberately vulnerable old dependency fails the job. After upgrade, it passes.]**

**(Voiceover):**
Lab: apne repo ke workflow mein ek `security` job jodo. Secrets scan ke liye Gitleaks ka official action, dependency check ke liye `pip install pip-audit && pip-audit -r requirements.txt`, aur Trivy ka filesystem scan, `trivy fs --severity HIGH,CRITICAL --exit-code 1 .`. `requirements.txt` mein jaan-boojh kar ek purana, vulnerable package version rakho, aur dekho ki job fail hoti hai. Version upgrade karke pass karo. Ye pehli baar DevSecOps ka asli chehra hai. Naye tool versions ke liye hamesha unki official docs dekho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "shift left · secrets/SAST/SCA/image/IaC · smart gates · triage".]**

**(Voiceover):**
Recap: CI/CD ka poora block: Git, Jenkins, GitHub Actions, aur security. Ab hum code ko packaging ki taraf le jaate hain. Container: wo cheez jisne "mere laptop par chal raha tha" ko khatam kar diya. Docker.

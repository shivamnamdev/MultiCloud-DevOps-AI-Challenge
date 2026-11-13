# ✍️ 02: SCRIPT — SESSION-28: Terraform on AWS
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S28`
- **Focus:** Remote state (S3 + locking), modules, environments (tfvars/workspaces), 3-tier AWS build, cost & security checks, CI for Terraform
- **Episodes:**
  - Episode 1: Remote State aur Locking: Team ke saath Terraform
  - Episode 2: Modules: Ek Baar Likho, Baar Baar Use Karo
  - Episode 3: Environments aur 3-Tier Architecture
  - Episode 4: Terraform Pipeline: Scan, Cost aur Safe Apply

---

# 📺 EPISODE 1: Remote State aur Locking

### [00:00 – 01:15] Scene 1: Do Engineers, Ek Apply
**[VISUAL: Two engineers run `terraform apply` at the same time from their laptops, each with a local state. Duplicate resources appear; one overwrites the other's state file. A red collision.]**

**(Voiceover):**
Aapne aur aapke teammate ne ek saath `terraform apply` chalaya, apne apne laptop ki state se. Dono ne alag alag cheezein banayi, ya ek ne doosre ki state overwrite kar di. Local state akele project mein theek hai, team mein nahi. Iska hal: remote state, aur locking.

### [01:15 – 05:00] Scene 2: S3 Backend aur State Locking
**[VISUAL: A backend block: `backend "s3" { bucket, key, region, encrypt = true, use_lockfile = true }`. A bucket with versioning and encryption. Older setups with a DynamoDB table for locks shown as legacy.]**

**(Voiceover):**
Remote backend mein state ek shared jagah rehti hai. AWS par aam tareeka S3 bucket hai: `backend "s3" { bucket = "...", key = "shop/terraform.tfstate", region = "...", encrypt = true }`. Bucket par versioning on karo, taaki state ki purani copy mil sake, aur public access band. Locking ka matlab hai ki ek samay par ek hi apply chale. Purane setups mein iske liye DynamoDB table use hoti thi, aur naye Terraform versions S3 ke apne lock file option ko support karte hain; aapke version ke docs dekhkar sahi option chuno.

### [05:00 – 08:30] Scene 3: Backend ko Bootstrap Karna
**[VISUAL: A chicken-and-egg diagram: "Backend bucket must exist before Terraform can use it". A small separate Terraform project (or CLI) creates the bucket; the main project then runs `terraform init -migrate-state`.]**

**(Voiceover):**
Ek sawaal: state ke liye bucket Terraform se banaye, to us bucket ki state kahan? Ye chicken-and-egg hai. Aam solution: bucket ko ek chhote alag bootstrap project se, ya AWS CLI se, ek baar banao. Phir asli project mein backend block likho aur `terraform init -migrate-state` chalao, jo local state ko bucket mein le jata hai. State bucket ko sambhaal kar rakho: usme kisi ko delete ya overwrite ka access na ho, aur uske access logs on rakho.

### [08:30 – 11:30] Scene 4: Lab: State ko S3 par Bhejo
**[VISUAL: Create a bucket with versioning and block public access via CLI. Add the backend block. `terraform init -migrate-state`. `aws s3 ls s3://BUCKET/shop/`. A second terminal attempting a concurrent apply is blocked by the lock.]**

**(Voiceover):**
Lab:
```bash
aws s3api create-bucket --bucket YOUR-UNIQUE-STATE-BUCKET --region YOUR_REGION \
  --create-bucket-configuration LocationConstraint=YOUR_REGION
aws s3api put-bucket-versioning --bucket YOUR-UNIQUE-STATE-BUCKET --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket YOUR-UNIQUE-STATE-BUCKET \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```
Phir backend block jodo aur `terraform init -migrate-state`. `aws s3 ls` se state file dekho. Do terminals mein ek saath apply try karo, aur dekho ki doosra "state locked" ka error deta hai. Dhyaan: us-east-1 mein `LocationConstraint` nahi dete.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "remote state · versioned · encrypted · locked · bootstrap once".]**

**(Voiceover):**
Recap: remote state aur locking. Ab code ko dohrane se bachate hain: modules.

---

# 📺 EPISODE 2: Modules

### [00:00 – 01:15] Scene 1: Copy-Paste ka Jungle
**[VISUAL: Three environment folders each containing the same 200-line VPC code with tiny differences. A change request means editing all three.]**

**(Voiceover):**
Dev, staging aur prod ke liye wahi VPC ka 200 line ka code teen baar copy paste kiya. Ab koi ek rule badalna ho to teen jagah edit, aur kahin ek jagah chhoot jata hai. Modules Terraform ka function hain: ek baar likho, alag alag inputs ke saath baar baar chalao.

### [01:15 – 05:00] Scene 2: Module ka Dhancha
**[VISUAL: A folder `modules/vpc/` with `main.tf`, `variables.tf`, `outputs.tf`. A root module calling it: `module "vpc" { source = "./modules/vpc"  cidr = "10.0.0.0/16" }` and reading `module.vpc.public_subnet_ids`.]**

**(Voiceover):**
Module ek folder hai jisme `.tf` files hoti hain: `variables.tf` input, `main.tf` resources, `outputs.tf` output. Root project use aise bulata hai: `module "vpc" { source = "./modules/vpc"  cidr = "10.0.0.0/16" }`. Module ke andar ke outputs ko `module.vpc.public_subnet_ids` se padhte hain. Ek achha module chhota hota hai, ek kaam karta hai, sahi defaults deta hai, aur variable ke type aur description likhe hote hain. Public Terraform Registry mein bane banaye modules milte hain, par unhe use karne se pehle padh lo, aur version pin karo.

### [05:00 – 08:30] Scene 3: Module Design ke Niyam
**[VISUAL: A checklist: inputs minimal, validation blocks, outputs for what callers need, no provider config inside, tags passed in, versioned (Git tag), README with example.]**

**(Voiceover):**
Module ke niyam. Inputs kam rakho aur zaroori ko hi expose karo. `validation` block se galat input pakdo, jaise CIDR ka format. Provider module ke andar configure mat karo, caller karta hai. Tags bahar se pass karo. Aur module ko Git tag se version do, jaise `?ref=v1.2.0`, taaki ek badlav sab environments ko ek saath na tode. Aur ek README ka example. Over-engineering se bachna: do baar dohraya hua pattern hi module banane layak hota hai.

### [08:30 – 11:30] Scene 4: Lab: VPC Module Banao
**[VISUAL: Refactor the previous lab's VPC code into `modules/vpc`. A root `main.tf` calls it twice with different CIDRs: `dev` and `staging`. `terraform plan` shows both sets of resources.]**

**(Voiceover):**
Lab: pichle session ke VPC code ko `modules/vpc` mein le jao: inputs `name`, `cidr`, `public_subnets`, `private_subnets`, outputs `vpc_id` aur subnet IDs. Root mein module ko do baar bulao, ek `dev` aur ek `staging` ke naam se, alag CIDR ke saath. `terraform init` (modules load karne ke liye) aur `plan`. Dekho ki ek hi code se do poore network ban rahe hain. Lab ke baad destroy karna, kyunki NAT Gateway jaisi cheezein paisa leti hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "module = folder with inputs/outputs · versioned · validate inputs · small and focused".]**

**(Voiceover):**
Recap: modules. Ab environments aur ek poora 3-tier architecture.

---

# 📺 EPISODE 3: Environments aur 3-Tier Architecture

### [00:00 – 01:15] Scene 1: Dev ka Dhakka Prod Par
**[VISUAL: An engineer runs `terraform destroy` thinking they are in dev, but the state in use is prod. A cascade of deletions. Safeguards appear: separate states, separate accounts.]**

**(Voiceover):**
Ek engineer ne socha wo dev mein hai, `terraform destroy` chalaya, aur wo prod tha. Aise hadse isliye hote hain ki environments ek dusre se alag nahi hote. Achhi setup mein har environment ki apni state, apne variables, aur aksar apna alag AWS account hota hai.

### [01:15 – 05:00] Scene 2: Environments ke Tareeke
**[VISUAL: Three options: separate folders/state per env (`envs/dev`, `envs/prod`), workspaces, separate accounts. A recommendation badge on separate directories + tfvars.]**

**(Voiceover):**
Teen tareeke. Alag folders, `envs/dev` aur `envs/prod`, har ek ka apna backend key aur `terraform.tfvars`, aur dono same modules bulate hain. Workspaces ek hi code se kai states dete hain, par galti se galat workspace mein kaam karna aasaan hota hai. Alag AWS accounts sabse surakshit hain, kyunki ek account ki galti doosre ko nahi chhoti. Shuruaat ke liye alag folders aur tfvars saaf aur seedha rasta hai.

### [05:00 – 08:30] Scene 3: 3-Tier Architecture
**[VISUAL: A diagram: Users → ALB (public subnets, 2 AZ) → ASG of web/app instances (private subnets) → RDS (private DB subnets). NAT Gateway for outbound. Security group chain. Modules labelled: network, alb, compute, database.]**

**(Voiceover):**
Ab AWS ke sessions ko jodte hain. 3-tier architecture: web tier mein ALB public subnets mein, app tier mein Auto Scaling Group private subnets mein, aur database tier mein RDS private DB subnets mein. Security groups ki chain: internet se ALB, ALB se app, app se database. Modules: `network`, `alb`, `compute`, `database`. Is design mein agar ek AZ gira to doosra sambhal leta hai, aur database kabhi seedha internet se nahi dikhta.

### [08:30 – 11:30] Scene 4: Lab: Dev Environment ka Plan
**[VISUAL: `envs/dev/main.tf` composing modules; `terraform.tfvars`; `terraform plan` summarizing "Plan: 38 to add". A cost reminder banner.]**

**(Voiceover):**
Lab: `envs/dev` mein modules ko jodo: network, alb, compute aur database, aur variables `terraform.tfvars` se do. Pehle sirf `terraform plan` chalao aur padho ki kitne resources banenge. Plan ko samajhna hi is lab ka asli maksad hai. Agar aap poora apply karna chahte ho, to chhote sizes lo, RDS ko single-AZ aur chhota instance rakho, aur kaam ke turant baad `terraform destroy`. NAT Gateway aur RDS dono ghante ke hisaab se paisa lete hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "state per env · tfvars · accounts for safety · 3-tier = ALB → ASG → RDS".]**

**(Voiceover):**
Recap: environments aur 3-tier. Ab Terraform ko pipeline mein lagate hain: scan, cost aur safe apply.

---

# 📺 EPISODE 4: Terraform Pipeline

### [00:00 – 01:15] Scene 1: Apply Apne Laptop Se?
**[VISUAL: An engineer applying to prod from a laptop with admin keys. A risk list pops up. Then a pipeline with a PR plan comment and an approval gate.]**

**(Voiceover):**
Production mein apply apne laptop se, admin keys ke saath? Ye risky aur trace karne mein mushkil hai. Behtar tareeka: pipeline. PR par plan chalta hai aur comment mein dikhta hai, review hota hai, aur merge ke baad approval ke saath apply hota hai.

### [01:15 – 05:00] Scene 2: Pipeline ke Stages
**[VISUAL: A flow: PR opened → `fmt -check` → `validate` → security scan (Checkov/tfsec/Trivy) → cost estimate (Infracost) → `plan` posted on PR → human review → merge → `apply` with environment approval.]**

**(Voiceover):**
PR par: `terraform fmt -check`, `validate`, security scan jaise Checkov ya Trivy jo kholi hui security groups ya unencrypted disks pakadte hain, cost estimate jaise Infracost, aur `terraform plan` jo PR mein dikhta hai. Merge ke baad `apply`, environment approval ke saath, aur wahi saved plan file `plan -out` se, taaki jo review hua wahi lagu ho. AWS keys ki jagah OIDC role, jo humne GitHub Actions session mein dekha. Aur apply ke liye pipeline ke role ke paas sirf zaroori permissions.

### [05:00 – 08:30] Scene 3: Drift Detection aur Guardrails
**[VISUAL: A scheduled pipeline running `terraform plan -detailed-exitcode` nightly. Exit code 2 sends a Slack alert "drift detected". Policy-as-code (OPA/Sentinel) mention.]**

**(Voiceover):**
Apply ke baad bhi kaam khatam nahi. Roz raat ek scheduled pipeline `terraform plan -detailed-exitcode` chalaye: exit code 0 matlab koi badlav nahi, 2 matlab drift, aur tab Slack alert. Policy as code, jaise OPA ya Sentinel, aise rules lagu karte hain: "koi bhi bucket public nahi", "tags zaroori". Aur prod ke state bucket aur apply role ko alag aur surakshit rakho. Ye sab milkar infrastructure ko code ki tarah safe banate hain.

### [08:30 – 11:30] Scene 4: Lab: GitHub Actions se Terraform CI
**[VISUAL: A workflow with steps: checkout, setup-terraform, `terraform fmt -check`, `terraform init -backend=false`, `terraform validate`, and a Trivy config scan `trivy config .`. A failing scan for an open `0.0.0.0/0` SSH rule.]**

**(Voiceover):**
Lab: GitHub Actions workflow jo PR par ye chalaye:
```yaml
- uses: hashicorp/setup-terraform@v3
- run: terraform fmt -check -recursive
- run: terraform init -backend=false
- run: terraform validate
- run: |
    curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
    trivy config --severity HIGH,CRITICAL --exit-code 1 .
```
Apne Terraform mein SSH ko `0.0.0.0/0` par khol kar push karo, aur dekho ki scan fail hoti hai. Rule theek karke pass karao. Action aur tool versions ko pin karna aur official install guide dekhna mat bhoolna.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "PR plan · scans · cost · approval · saved plan · OIDC · drift detection".]**

**(Voiceover):**
Recap: Terraform ka poora production workflow. Ab ek aur tool jo machine ke andar ki configuration sambhalta hai: Ansible.

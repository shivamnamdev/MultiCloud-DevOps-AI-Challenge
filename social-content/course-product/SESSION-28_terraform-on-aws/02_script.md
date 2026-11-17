# ✍️ 02: SCRIPT — SESSION-28: Terraform on AWS
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S28`
- **Focus:** Remote state on S3 (versioning, encryption, public access block, native locking or DynamoDB, bootstrap, `-backend-config`, protecting the state bucket), splitting state by layer, modules (structure, inputs, outputs, validation, versioned sources), environments (separate folders and state, tfvars, accounts, `default_tags`), the 3-tier campus (ALB, Auto Scaling, RDS with managed password), cost and blast radius, a Terraform pipeline (fmt, validate, scan, cost, plan on pull request, saved plan, approval, OIDC, separate plan and apply roles), drift detection, policy as code
- **Builds on:** Session 09 (roles, least privilege), Session 10 (launch template, Auto Scaling), Session 11 (ALB, security group chain), Session 12 (S3 versioning, public access block, lifecycle), Session 13 (RDS, managed password), Session 14 (campus, wings, NAT), Session 15 (budget alerts), Session 20 (OIDC, Trivy, required checks), Session 27 (the Terraform workflow, state, drift, lifecycle)
- **Story position:** Zoom level 2, the rented campus, run as a company. Poora Atithi campus Session 14 se ek hi master plan se banta hai, standard designs (modules) ke saath, aur ek shared as-built register jis par lock hai, taaki do contractor ek saath kabhi na banayein.
- **Story words used:** master plan (Terraform code), contractor (provider), as-built register (state), register lock (state locking), standard design (module), campus (VPC), wing (subnet), marshal (ALB), buildings (EC2 in an Auto Scaling Group), records office (RDS), dispatch desk (NAT gateway), door guard (security group), duty badge (role), drift, landlord (cloud provider), guest (end user), staff (admin)
- **Lab project:** Atithi's register moved to the warehouse (S3) with a lock; the Session 14 wing turned into a standard design called twice for dev and staging; the dev campus planned as ALB, Auto Scaling and RDS; and the conveyor for the plan.
- **Cost rule (AWS):** NAT gateways, load balancers and RDS instances are billed by the hour. Plan first, apply only a small copy, and `terraform destroy` the same day. Set a budget alert before the lab (Session 15). Check the console after destroy for leftovers.
- **Episodes:**
  - Episode 1: Shared Register aur Lock: Remote State
  - Episode 2: Standard Design: Modules
  - Episode 3: Alag Campus, Ek Master Plan: Environments aur 3-Tier
  - Episode 4: Master Plan ki Conveyor: Pipeline, Drift aur Guardrails

---

# 📺 EPISODE 1: Shared Register aur Lock

### [00:00 – 02:05] Scene 1: Do Contractor, Ek Hi Waqt
**[VISUAL: Two engineers run `terraform apply` from their laptops at the same time, each with its own local state. Duplicate buildings appear, and one overwrites the other's register. A red collision.]**

**(Voiceover):**
Atithi mein ab do engineers campus ka master plan sambhalte hain. Dono ne ek hi samay `terraform apply` chalaya, apne apne laptop ke register ke saath. Dono ne alag cheezein banayi, ya ek ne doosre ka register overwrite kar diya. Ab asli duniya aur kisi ke register mein mel nahi. Local state ek akele project ke liye theek hai, team ke liye nahi. Iska hal: register ko ek shared jagah rakho, jise sab padhein, aur jis par ek hi samay mein ek hi apply chale. Isko remote state aur locking kehte hain.

### [02:05 – 05:05] Scene 2: S3 Backend aur Lock
**[VISUAL: A backend block: `backend "s3" { bucket = "atithi-tfstate", key = "network/terraform.tfstate", region = "ap-south-1", encrypt = true, use_lockfile = true }`. A warehouse labelled versioning, encryption, public access block. Beside it, an older setup with a DynamoDB table for the lock, marked legacy.]**

**(Voiceover):**
AWS par aam tareeka warehouse hai, yaani S3 bucket. Backend block mein `bucket`, `key`, `region` aur `encrypt = true`. Bucket par versioning on, taaki register ki purani copy mil sake, Block Public Access on, aur default encryption, jo Session 12 ke saare niyam hain. Lock ka matlab hai ki ek hi samay ek apply chalega. Purane setups mein iske liye DynamoDB table lagti thi. Terraform 1.10 aur uske baad ke versions S3 ka apna lock file option, `use_lockfile = true`, dete hain, aur DynamoDB wala tareeka ab purana, yaani deprecated, maana jaata hai, jo abhi chalta hai par chetavani deta hai. Apne version ke docs dekh kar sahi option chuno. Ek chhoti jaal: backend block mein variables nahi chalte, isliye alag alag environments ke liye `-backend-config` file se values do.

### [05:05 – 07:35] Scene 3: Pehle Bucket, Phir Terraform
**[VISUAL: A chicken-and-egg diagram: "the register's warehouse must exist before Terraform can use it". A small bootstrap step creates the bucket once; the main project then runs `terraform init -migrate-state`.]**

**(Voiceover):**
Ek sawaal: register ke liye warehouse Terraform se banaye, to us warehouse ka register kahan? Ye chicken-and-egg hai. Aam hal: bucket ko ek baar, ek chhote bootstrap project se, ya AWS CLI se banao, aur uska apna chhota state ek surakshit jagah rakho. Phir asli project mein backend block likho aur `terraform init -migrate-state` chalao, jo local register ko bucket mein le jaata hai. Bucket ko sambhal kar rakho: usme sirf wahi role likh sake jo Terraform chalata hai, `aws:SecureTransport` ka Deny rule lagao, purane versions ka lifecycle rule rakho, aur access logs on. Register hi sabse keemti file hai, kyunki usme maujooda campus ki poori kahani hai.

### [07:35 – 09:50] Scene 4: Ek Bada Register Nahi: Layers mein Todo
**[VISUAL: One huge state for everything, a typo in the web code putting the database at risk. Next: three registers: `network`, `data`, `app`. Arrows show `app` reading outputs from `network` and `data`.]**

**(Voiceover):**
Ek hi register mein poora campus rakhoge, to har plan sab kuch dekhega, aur ek galat badlaav sab ko chhoo sakta hai. Isliye layers: network, data aur app ke alag register. Network kam badalta hai, data aur bhi kam, app roz. App wali layer network ke outputs padh sakti hai, jaise `terraform_remote_state` data source se, ya ek shared parameter store se. Isse ek galti ka daayra, yaani blast radius, chhota rehta hai. App ka apply database ko chhue hi nahi. Aur plan chhote aur tez rehte hain. Seedha rule: jo cheezein alag raftaar se badalti hain, unka register alag.

### [09:50 – 12:50] Scene 5: Register Bigad Gaya to
**[VISUAL: A bad apply corrupts the register. The warehouse's version history lists earlier copies. A command `terraform state pull > backup.json` taken before risky work. A restore by copying an earlier version back, then `terraform plan` to verify.]**

**(Voiceover):**
Kabhi register hi bigad jaata hai: koi apply beech mein toot gaya, ya kisi ne `state rm` galat chala diya. Warehouse mein versioning isi din ke liye hai. Pehle dekho ki bucket ki purani versions kaun si hain. Kisi bhi bade kaam, jaise `state mv` ya import, se pehle `terraform state pull > backup.json` se ek copy le lo. Bigad jaaye to pichhla theek version wapas rakho, aur turant `terraform plan` chalao: agar plan saaf aaye, ya sirf wahi badlaav dikhe jo aap jaante ho, to register theek hai. Agar plan mein achanak "sab kuch banana hai" dikhe, to rukna, kyunki Terraform ne apni buildings bhula di hain, aur apply karna sabko doguna bana dega. Lock atke to `force-unlock`, sirf tab jab pakka ho ki koi apply nahi chal raha.

### [12:50 – 15:10] Scene 6: Lab: Register ko Warehouse mein Bhejo
**[VISUAL: AWS CLI creating the bucket, enabling versioning, public access block, default encryption. A backend block added. `terraform init -migrate-state`. `aws s3 ls s3://BUCKET/network/`. Two terminals run `terraform apply` at once and the second is told the state is locked.]**

**(Voiceover):**
Lab:
```bash
aws s3api create-bucket --bucket YOUR-STATE-BUCKET --region YOUR_REGION \
  --create-bucket-configuration LocationConstraint=YOUR_REGION
aws s3api put-bucket-versioning --bucket YOUR-STATE-BUCKET --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket YOUR-STATE-BUCKET \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```
Dhyaan: us-east-1 mein `LocationConstraint` nahi dete. Phir backend block jodo aur `terraform init -migrate-state`. `aws s3 ls s3://YOUR-STATE-BUCKET/` se register dekho. Do terminals mein ek saath `terraform apply` try karo, aur dekho ki doosre ko "state locked" ka error milta hai. Lock atak jaaye to `terraform force-unlock` sirf tab, jab pakka ho ki koi apply chal nahi raha. Aakhir mein bucket ka version history kholkar dekho ki register ki purani copy kaise wapas milti hai.

### [15:10 – 15:40] Scene 7: Recap aur Bridge
**[VISUAL: A card: "remote state in S3 · versioned, encrypted, private · lock (native or DynamoDB) · bootstrap once · -backend-config · split state by layer · protect the register bucket".]**

**(Voiceover):**
Recap: shared register, lock, aur layers. Ab master plan ko dohrane se bachate hain: standard designs, yaani modules.

---

# 📺 EPISODE 2: Standard Design

### [00:00 – 01:45] Scene 1: Copy-Paste ka Jungle
**[VISUAL: Three folders (dev, staging, prod) each holding the same two hundred lines of campus code with tiny differences. A change request needs three edits and one is missed.]**

**(Voiceover):**
Dev, staging aur production, teen campus, aur teen jagah wahi 200 line ka network code, thode se farq ke saath. Ek rule badalna ho to teen jagah edit, aur ek jagah chhoot jaata hai, aur wahi jagah aage chalkar "staging production jaisa kyun nahi" ban jaati hai. Module Terraform ka function hai: ek baar standard design likho, aur alag alag inputs ke saath baar baar bulao.

### [01:45 – 04:30] Scene 2: Module ka Dhancha
**[VISUAL: A folder `modules/network/` with `main.tf`, `variables.tf`, `outputs.tf`, `README.md`. A caller: `module "network" { source = "../../modules/network"  name = "dev"  cidr = "10.10.0.0/16" }` and `module.network.public_subnet_ids` used elsewhere.]**

**(Voiceover):**
Module ek folder hai jisme `.tf` files hoti hain: `variables.tf` mein inputs, `main.tf` mein resources, `outputs.tf` mein jo bahar dena hai, aur ek README. Caller use aise bulata hai: `module "network" { source = "../../modules/network"  name = "dev"  cidr = "10.10.0.0/16" }`. Module ke outputs ko `module.network.public_subnet_ids` se padhte hain. Source teen jagah se aa sakta hai: local folder, Git repo `git::https://...?ref=v1.2.0`, ya Terraform Registry, jahan `version` likhte hain. Bane banaye registry modules kaam ke hote hain, par unhe use karne se pehle padh lo, aur version pin karo, kyunki ek hi `main` branch par bharosa Session 20 ke action pin wala khatra hai.

### [04:30 – 07:45] Scene 3: Achhe Module ke Niyam
**[VISUAL: A checklist: few inputs, types and descriptions, `validation` blocks, outputs for what callers need, no provider configuration inside, tags passed in, version tags in Git, a README with an example. A warning: "only make a module after the pattern repeats twice".]**

**(Voiceover):**
Module ke niyam. Inputs kam rakho, aur sirf wahi expose karo jo caller ko badalna hai. Har variable ka type aur description. `validation` block se galat input pakdo, jaise CIDR ka format, `can(cidrhost(var.cidr, 0))`. Module ke andar provider configure mat karo, caller karta hai. Tags bahar se pass karo. Module ko Git tag se version do, jaise `v1.2.0`, aur pull request ke saath badlo, taaki ek badlaav teen campus ko ek saath na tode. Ek module ek kaam kare: network, ya alb, ya database, sab ek mein nahi. Aur over-engineering se bacho: jo pattern do baar dohraya gaya wahi module banane layak hai. Pehle se banaye gaye bade, sab kuch karne wale module aksar utne hi ulajhe hote hain jitne unhe hatana mushkil.

### [07:45 – 10:50] Scene 4: Module ko Badalna, Safely
**[VISUAL: A module upgraded from `v1.2.0` to `v1.3.0` in dev first, plan reviewed, then staging, then prod. A plan showing `-/+` caused by a renamed resource inside the module, fixed by a `moved` block inside the module.]**

**(Voiceover):**
Module badalte waqt do khatre. Ek: module ke andar ka koi resource rename kar do, to har campus ka plan "hatao aur banao" dikhata hai. Iska hal wahi `moved` block jo Session 27 mein dekha, bas ab module ke andar. Do: ek naya version ek saath teen campus par gira, aur teeno tut gaye. Isliye upgrade ka kram: pehle dev, plan padho, apply karo, dekho. Phir staging. Phir prod. Har campus apna version pin karta hai, aur module ka naya version ek pull request ke saath aata hai jisme do line ka changelog ho: kya badla, aur kya `moved` ho sakta hai. Isse "standard design" ek aisi cheez ban jaati hai jise sab par bharosa hota hai.

### [10:50 – 13:40] Scene 5: Lab: Network ka Standard Design
**[VISUAL: The previous session's wing code moved into `modules/network`. A root `main.tf` calls it twice: `dev` with `10.10.0.0/16` and `staging` with `10.20.0.0/16`. `terraform init` loads modules; `plan` shows two sets of resources; outputs show subnet IDs.]**

**(Voiceover):**
Lab. Session 27 ke public wing ka code `modules/network` mein le jao. Inputs: `name`, `cidr`, `public_subnet_count`, aur outputs: `vpc_id`, `public_subnet_ids`. Subnet ke CIDR `cidrsubnet` se nikalo. Ek `validation` lagao jo galat CIDR par rok de. Root mein module ko do baar bulao: ek `dev` aur ek `staging`, alag CIDR ke saath, jo overlap nahi karte, Session 14 ka niyam. `terraform init` modules ko load karta hai, phir `plan`. Dekho ki ek hi code se do alag campus ban rahe hain. Phir `cidr` mein galat value do aur dekho ki validation ruk jaata hai. NAT gateway abhi mat jodo, kyunki wo hourly paisa leta hai. Aakhir mein `destroy`.

### [13:40 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "module = folder with inputs and outputs · small, one job · validate inputs · version with Git tags · upgrade dev → staging → prod · moved blocks inside modules".]**

**(Voiceover):**
Recap: modules. Ab ek bada sawaal: dev ka dhakka prod par kaise na pade, aur poora 3-tier campus ek plan se.

---

# 📺 EPISODE 3: Alag Campus, Ek Master Plan

### [00:00 – 01:35] Scene 1: Dev ka Dhakka Prod Par
**[VISUAL: An engineer runs `terraform destroy` believing they are in dev, but the working folder or the credentials point at prod. A cascade of deletions. Safeguards appear: separate state, separate account, a prompt that shows the environment.]**

**(Voiceover):**
Ek engineer ne socha wo dev mein hai, `terraform destroy` chalaya, aur wo production tha. Aise haadse isliye hote hain ki environments ek doosre se alag nahi hote. Achhi setup mein har environment ka apna register, apne variables, aur aksar apna alag AWS account hota hai. Aur terminal ka prompt environment ka naam dikhaye, jaise Session 23 mein kubectl ke context ke saath tay hua tha.

### [01:35 – 04:10] Scene 2: Environments ke Tareeke
**[VISUAL: Three options. 1: separate folders per environment (`envs/dev`, `envs/prod`) each with its own backend key and `terraform.tfvars`. 2: workspaces, one code and many states. 3: separate AWS accounts, each with its own role. A badge on option 1 as a good start and option 3 as the safest.]**

**(Voiceover):**
Teen tareeke. Ek: alag folders, `envs/dev` aur `envs/prod`, har ek ka apna backend key aur `terraform.tfvars`, aur sab wahi modules bulate hain. Do: workspaces, ek hi code se kai registers, par galat workspace mein kaam karna bahut aasaan hai, isliye bade campus ke liye mat chuno. Teen: alag AWS accounts, jahan har account ka apna role hota hai, aur provider `assume_role` se uske andar jaata hai. Account sabse surakshit hai, kyunki ek ki galti doosre ko chhoo nahi sakti, aur bill bhi alag. Shuruaat ke liye alag folders aur tfvars saaf raasta hai. Aur provider mein `default_tags` laga do, taaki har resource par Env aur Owner apne aap aaye.

### [04:10 – 06:35] Scene 3: Teen Parton ka Campus
**[VISUAL: Guests → ALB in public wings across two towers → Auto Scaling Group of app buildings in private wings → RDS in database wings. NAT gateway for outbound. The security group chain: internet to ALB, ALB to app, app to database. Four modules labelled `network`, `alb`, `compute`, `database`.]**

**(Voiceover):**
Ab AWS ke saare sessions ek jagah. 3-tier campus. Web tier: ALB, yaani marshal, public wings mein, do towers mein. App tier: Auto Scaling Group private wings mein, Session 10 ke launch template ke saath, aur bahar jaane ke liye dispatch desk. Database tier: RDS, Session 13 ka records office, private database wings mein. Door guard ki zanjeer, Session 11 ki tarah: internet se marshal, marshal se app, app se database, aur kisi par seedha nahi. Chaar modules: `network`, `alb`, `compute`, `database`. Is design mein ek tower gira to doosra sambhal leta hai, aur database kabhi seedha internet se nahi dikhta.

### [06:35 – 09:30] Scene 4: Database ke Password aur Kharcha
**[VISUAL: An `aws_db_instance` with `manage_master_user_password = true`, `multi_az = var.multi_az`, `deletion_protection = true`, `lifecycle { prevent_destroy = true }`. A cost bar: dev single-AZ and small, prod multi-AZ and larger. A NAT gateway per tower shown as a cost line.]**

**(Voiceover):**
Database module mein do cheezein dhyaan se. Password: `manage_master_user_password = true`, taaki password Secrets Manager mein ban jaaye aur Terraform ke state mein na aaye, jaise Session 13 aur Session 27 mein tay hua. Aur taale: `deletion_protection = true` aur `lifecycle { prevent_destroy = true }`, taaki ek galat plan records office ko na hata de. Kharcha: dev mein single-AZ aur chhota instance, production mein `multi_az = true` aur bada, aur ye difference ek variable se tay ho. NAT gateway ghante ka kharcha hai, aur har tower mein ek lagane se high availability milti hai par bill bhi doguna. Dev mein ek, production mein har tower mein ek. Ye faisle tfvars mein dikhne chahiye, taaki review mein sab dekh saken.

### [09:30 – 12:20] Scene 5: Cluster bhi Code, aur Doosre Landlord bhi
**[VISUAL: The same plan language with different contractors. A block `provider "aws"` building an EKS cluster module, a `provider "google"` building a GKE cluster, a `provider "azurerm"` building an AKS cluster, and a `provider "kubernetes"` or `helm` installing the monitoring stack on top.]**

**(Voiceover):**
Master plan sirf buildings ke liye nahi. Session 24 ka Kubernetes cluster bhi code ban sakta hai: AWS ka EKS, GCP ka GKE, Azure ka AKS, har ek ek module mein. Aur cluster ke upar ke kaam, jaise Session 26 ka monitoring stack, Helm provider se. Dhyaan: cluster banana aur cluster ke andar chizein lagana alag registers mein rakho, kyunki jab cluster hi gir jaaye, to uske andar ke resources ke plan bhi toot jaate hain. Aur landlord badalne par plan ki bhasha wahi rehti hai, par resources ke naam badal jaate hain: `aws_vpc` ki jagah `google_compute_network`. Isliye multi-cloud ka matlab "ek code sab jagah" nahi, "ek tareeka sab jagah" hai. Agle Azure ke session mein ye saaf dikhega.

### [12:20 – 15:05] Scene 6: Lab: Dev Campus ka Plan
**[VISUAL: `envs/dev/main.tf` composing four modules; `terraform.tfvars` setting sizes; `terraform plan` summarising how many resources would be added; a budget banner and a note "plan only today".]**

**(Voiceover):**
Lab. `envs/dev` folder mein chaar modules jodo: network, alb, compute aur database. Variables `terraform.tfvars` se do: chhote sizes, `multi_az = false`, ek NAT. Backend key `dev/terraform.tfstate`. Sabse pehle sirf `terraform plan` chalao, aur padho: kitne resources banenge, aur kaun se. Teen sawaal wahi Session 27 ke: kya kuch hatega, kuch anjaana badlega, ginti andaaze se milti hai? Aaj plan ko samajhna hi asli maksad hai. Agar poora apply karna chaho, to pehle Session 15 ka budget alert lagao, sabse chhote sizes lo, aur kaam ke turant baad `terraform destroy`, kyunki NAT gateway, ALB aur RDS teeno ghante ke hisaab se chalte hain. Destroy ke baad console mein check karo ki kuch bacha nahi.

### [15:05 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "one folder, one state, one tfvars per environment · accounts for safety · 3-tier = ALB → ASG → RDS · managed password · prevent_destroy · cost choices live in tfvars".]**

**(Voiceover):**
Recap: environments aur 3-tier campus. Ab master plan ko conveyor mein lagate hain: scan, cost aur safe apply.

---

# 📺 EPISODE 4: Master Plan ki Conveyor

### [00:00 – 01:35] Scene 1: Apply Apne Laptop Se?
**[VISUAL: An engineer applies to production from a laptop using admin keys. A risk list pops up: no review, no trace, keys on a laptop. Then a pipeline with a plan comment on the pull request and an approval gate.]**

**(Voiceover):**
Production mein apply apne laptop se, admin keys ke saath? Ye risky hai, aur baad mein trace karna mushkil. Behtar: master plan ki bhi apni conveyor. Pull request par plan chalta hai aur uska natija comment mein dikhta hai. Chief architect review karta hai. Merge ke baad, approval ke saath, apply. Session 17 se 20 ki conveyor ke saare vichar yahan wapas aate hain: review, required check, secret ka sahi upyog.

### [01:35 – 03:55] Scene 2: Pipeline ke Stations
**[VISUAL: A flow. Pull request → `fmt -check` → `validate` → lint → security scan (Checkov or Trivy config) → cost estimate (Infracost) → `plan -out` posted on the pull request → human review → merge → `apply` of the saved plan under an environment approval.]**

**(Voiceover):**
Pull request par ye stations. `terraform fmt -check`. `terraform validate`. Ek linter, jaise tflint. Security scan, jaise Checkov ya Trivy, jo khuli hui security group ya bina encryption wale disk pakadte hain. Cost estimate, jaise Infracost, jo plan ka mahine ka kharcha batata hai. Aur `terraform plan -out=tfplan`, jiska saransh pull request mein dikhta hai. Merge ke baad `apply tfplan`, ek environment approval ke saath, aur wahi saved plan, taaki jo review hua wahi lage. Aur ek chhoti baat: plan dikhane wala role register aur resources padh sake, par kuch badal na sake. Apply wala role alag, aur sirf wahi ijaazat jo master plan ko chahiye.

### [03:55 – 06:15] Scene 3: Pipeline ko Chaabi Nahi, Duty Badge
**[VISUAL: GitHub Actions asks for an identity token, AWS issues short credentials for a role `tf-plan` on pull requests and `tf-apply` only on the `main` branch under an environment. A trust policy with a `sub` condition on repo and branch.]**

**(Voiceover):**
Pipeline ko AWS keys kyun dein? Session 20 ka OIDC yahan seedha kaam aata hai: workflow vault se ek identity token maangta hai, AWS role ki trust policy dekhta hai, aur chhoti umar ke credentials deta hai. Do role rakho. `tf-plan`: pull request se, sirf padhne ki ijaazat. `tf-apply`: sirf `main` branch se, ek environment approval ke baad, aur trust policy ki `sub` shart mein repo aur branch likha ho. Is tarah ek khula hua pull request, chahe fork se ho, apply wala role kabhi nahi le sakta. Aur Terraform ka `provider "aws"` bas region aur `assume_role` jaisi cheezein jaanta hai, koi key nahi.

### [06:15 – 08:55] Scene 4: Drift aur Guardrails
**[VISUAL: A scheduled workflow running `terraform plan -detailed-exitcode` every night. Exit code 0 no changes, 1 error, 2 changes found, which posts "drift detected" to the alarm desk topic. A policy-as-code panel with two rules: "no public bucket", "every resource has Owner and Env".]**

**(Voiceover):**
Apply ke baad bhi kaam khatam nahi. Roz raat ek scheduled workflow `terraform plan -detailed-exitcode` chalaye. Exit code 0 matlab koi badlaav nahi. 1 matlab plan mein hi error. 2 matlab drift mila, aur tab Session 15 ke SNS ya chat mein alert, ki kisi ne console mein kuch badla. Phir tay karo: code mein likho ya mita do. Policy as code, jaise OPA ya Sentinel ya Checkov ke custom rules, aise niyam lagu karte hain: "koi bhi bucket public nahi", "har resource par Owner aur Env tag". Aur register ke bucket aur apply role ko sabse kam logon ke haath mein rakho. Ye sab milkar infrastructure ko wahi anushasan dete hain jo Session 17 se humne code ko diya.

### [08:55 – 11:35] Scene 5: Wapas Kaise Jaayein
**[VISUAL: A pull request reverted with `git revert`, the pipeline planning the previous state and applying it. Beside it, a list of things that cannot be rolled back by reverting: deleted databases, destroyed data, rotated secrets. A line: "snapshots first".]**

**(Voiceover):**
Application ka rollback aasaan tha: `kubectl rollout undo`. Master plan ka rollback kya hai? Pull request ko revert karo, aur conveyor purani halat ka plan banakar apply kar degi. Par ye har cheez ke liye nahi chalta. Jo cheez hat chuki ho, jaise ek database ya ek bucket ka data, wo revert se wapas nahi aati, kyunki Terraform sirf naya khaali bana dega. Isliye teen aadatein. Ek: critical resources par `prevent_destroy`. Do: unke liye backup aur snapshot, jaise Session 10 aur 13 mein, apply se pehle. Teen: bade badlaav chhote tukdon mein, kyunki ek chhota plan padhna aur wapas lena dono aasaan hain. Aur jab plan "replace" dikhaye, to ek aur baar poocho: kya is cheez ka data hai?

### [11:35 – 14:15] Scene 6: Lab: Master Plan ki CI
**[VISUAL: A workflow with steps: checkout, `hashicorp/setup-terraform`, `terraform fmt -check -recursive`, `terraform init -backend=false`, `terraform validate`, a Trivy config scan. A security group with SSH open to `0.0.0.0/0` makes the scan fail; the fix makes it pass.]**

**(Voiceover):**
Lab. Vault mein ek workflow jo pull request par ye chalaye:
```yaml
- uses: actions/checkout@v4
- uses: hashicorp/setup-terraform@v3
- run: terraform fmt -check -recursive
- run: terraform init -backend=false
- run: terraform validate
- uses: aquasecurity/trivy-action@PINNED-VERSION
  with: { scan-type: config, severity: 'HIGH,CRITICAL', exit-code: '1' }
```
Action versions ko pin karo: `@PINNED-VERSION` ki jagah tay version ya SHA likho, jaise Session 20 mein. Ab apne master plan mein SSH ko `0.0.0.0/0` par khol kar push karo, aur dekho ki scan fail hoti hai. Rule ko apne IP tak seemit karo aur pass karao. Is check ko required status check banao, jaise Session 19 ke branch protection mein. Agar AWS hai, to OIDC ke role ke saath ek `plan` step jodo.

### [14:15 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "plan on the pull request · scans and cost · saved plan, approved apply · OIDC with separate plan and apply roles · nightly drift check · policy as code". Then a crew of workers with checklists enters a building.]**

**(Voiceover):**
Recap: Terraform ka poora production workflow. Ab campus ban gaya, par har building ke andar abhi khaali kamre hain: users, packages, services, settings. Un sabko ek jaisa sajane ke liye ek crew chahiye, jo har building mein jaakar checklist ke hisaab se kaam kare, aur dobara chalane par kuch na bigaade. Agla session: Ansible.

---

# 📎 Student handout: Session 28 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Remote state | S3 bucket: versioning, encryption, Block Public Access |
| Lock | `use_lockfile = true` (naye versions) ya DynamoDB (purana); version ke docs dekho |
| Bootstrap | Bucket pehle ek baar alag banao; `terraform init -migrate-state` |
| Backend aur variables | Backend block mein variables nahi; `-backend-config` |
| State bucket ki suraksha | Kam access, TLS-only policy, lifecycle, logs |
| Layers | `network`, `data`, `app` ke alag register; blast radius chhota |
| Module | `variables.tf`, `main.tf`, `outputs.tf`, README; source local, Git `?ref=`, registry `version` |
| Module niyam | Kam inputs, `validation`, provider andar nahi, tags bahar se, ek kaam |
| Module upgrade | dev → staging → prod; `moved` block andar |
| Environments | Alag folders + tfvars + backend key; accounts sabse surakshit; workspaces se savdhan |
| `default_tags` | Provider mein; Env aur Owner har resource par |
| 3-tier | ALB (public) → ASG (private) → RDS (private DB wings); SG zanjeer |
| RDS password | `manage_master_user_password`; `deletion_protection`; `prevent_destroy` |
| Kharcha | NAT, ALB, RDS ghante ka; dev mein ek NAT; plan pehle |
| Pipeline | `fmt`, `validate`, lint, scan, cost, `plan -out`, approval, `apply tfplan` |
| OIDC | `tf-plan` (read) aur `tf-apply` (sirf `main`, approval); trust policy `sub` |
| Drift | Raat ko `plan -detailed-exitcode`: 0, 1, 2 |
| Policy as code | OPA, Sentinel, Checkov: public bucket nahi, tags zaroori |
| Safai | `terraform destroy`, console check, budget alert |

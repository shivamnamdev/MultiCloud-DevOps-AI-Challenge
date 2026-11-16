# ✍️ 02: SCRIPT — SESSION-27: Terraform Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S27`
- **Focus:** Infrastructure as Code (why, and where Terraform and OpenTofu sit), the workflow (`init`, `plan`, `apply`, `destroy`) and how to read a plan, HCL (blocks, providers and version constraints, resources, variables with types and validation, locals, outputs, `count` and `for_each`, functions such as `cidrsubnet`), credentials kept out of code, state (mapping, secrets, lock file, drift, `state` commands, `import`, `moved`), dependencies (implicit, `depends_on`), data sources, `lifecycle`, a safe working habit, the Session 14 public wing built from code
- **Builds on:** Session 01 (the "buildings can be photocopied" rule), Session 08 (EC2, security group), Session 09 (credentials, roles), Session 10 (AMI), Session 12 (S3), Session 14 (VPC, subnets, CIDR, route tables, internet gateway), Session 16 and 20 (review by pull request, state files and secrets must not enter Git)
- **Story position:** Zoom level 2, the rented campus, from the architect's table. Atithi ab haath se kiraye par lena band karta hai. Campus ka master plan ek document mein likhta hai, ek contractor se kehta hai "sirf badlaav dikhao", phir banwata hai, aur as-built register mein likhwata hai ki asli mein kya bana.
- **Story words used:** master plan (Terraform code), contractor (provider), as-built register (state), preview of changes (plan), standard design (module, preview), drift (someone changed a building by hand), campus (VPC), wing (subnet), main gate (internet gateway), direction boards (route table), door guard (security group), building (EC2), landlord (cloud provider), staff (admin), guest (end user)
- **Lab project:** a file the plan creates and destroys safely, then a building and door guard from code, then the Session 14 public wing (campus, wing, main gate, direction board, door guard, building) written once and rebuilt on demand.
- **Cost rule (AWS):** every lab that creates real resources ends with `terraform destroy`, and a check in the console that nothing is left. Do not leave an Elastic IP, NAT gateway or building behind. Never put credentials in the code or in Git.
- **Episodes:**
  - Episode 1: Console Clicking ka Ant: Master Plan aur Workflow
  - Episode 2: Master Plan ki Bhasha: HCL
  - Episode 3: As-built Register: State aur Drift
  - Episode 4: Pehle Kaun, Phir Kaun: Dependencies aur Safe Workflow

---

# 📺 EPISODE 1: Console Clicking ka Ant

### [00:00 – 02:20] Scene 1: "Staging Production Jaisa Kyun Nahi?"
**[VISUAL: Two campuses built months apart by two different engineers clicking in the console. A diff shows a missing door guard rule and a different building size. A bug appears only in production.]**

**(Voiceover):**
Atithi ka staging campus aur production campus haath se bane the, console mein click karke, alag alag engineers ne, alag alag mahine mein. Ek mein door guard ki list mein ek rule hai, doosre mein nahi. Ek mein building ka size chhota hai. Bug sirf production mein aata hai, aur koi nahi jaanta kyun. Session 1 mein humne kaha tha ki is duniya mein buildings ki photocopy ho sakti hai. Par jab tak har baar koi insaan click karke banata hai, har copy thodi alag banti hai. Hal: campus ka naksha ek document mein likho, ek tool use padhe, aur har baar wahi banaye.

### [02:20 – 05:05] Scene 2: Infrastructure as Code
**[VISUAL: A list of benefits: repeatable, reviewable by pull request, history in Git, fast, self-documenting, easy to destroy. A map of tools: Terraform and OpenTofu (create resources across clouds), CloudFormation (AWS only), Ansible (configure what is inside a building).]**

**(Voiceover):**
Infrastructure as Code, IaC, ka matlab hai ki campus ka naksha code mein hota hai. Faayde: repeatable, kyunki wahi code wahi campus banata hai. Reviewable, kyunki badlaav pull request mein dikhta hai. History, kyunki Git mein har badlaav ka register hai. Aur hatana bhi ek command ka kaam. Terraform HashiCorp ka tool hai jo AWS, Azure, GCP, Kubernetes aur hazaaron providers ke saath chalta hai. Uska ek open source fork OpenTofu bhi hai, jo lagbhag wahi kaam karta hai, aur license ki wajah se kuch teams use chunti hain. Terraform declarative hai: aap likhte ho kya chahiye, wo tay karta hai kaise. Buildings banane ke liye Terraform, aur building ke andar ki setup ke liye Ansible, jo agle session mein hai.

### [05:05 – 07:35] Scene 3: Chaar Commands ka Workflow
**[VISUAL: A cycle: write the plan → `terraform init` → `terraform plan` → `terraform apply` → `terraform destroy`. A preview showing `+ create`, `~ update in-place`, `- destroy`, and `-/+ destroy and then create replacement`.]**

**(Voiceover):**
Workflow chaar commands mein. `terraform init` contractors yaani providers ko download karta hai aur ek `.terraform` folder banata hai. `terraform plan` dikhata hai ki kya banega, badlega ya hatega, bina kuch kiye. `terraform apply` use asli mein lagu karta hai, aur ek baar "yes" poochta hai. `terraform destroy` sab hata deta hai. Plan sabse zaroori step hai. Usme `+` banega, `~` badlega, `-` hatega, aur `-/+` ka matlab hatao aur dobara banao, aur uske saath "forces replacement" likha hota hai. Agar aap `-/+` ya `-` par dhyaan na do, to production ka database bhi ja sakta hai. Isliye plan padhna ek kaushal hai, jise hum har lab mein abhyas karenge.

### [07:35 – 10:20] Scene 4: Plan Padhna: Teen Sawaal
**[VISUAL: A plan with highlighted lines. Three questions beside it. 1: "What is being destroyed or replaced?" 2: "Is anything changing that I did not touch?" 3: "Do the numbers at the bottom (add, change, destroy) match what I expected?" A red box on `Plan: 1 to add, 0 to change, 1 to destroy`.]**

**(Voiceover):**
Plan padhne ke liye teen sawaal. Ek: kya kuch hatega ya replace hoga? Do: kya koi aisi cheez badal rahi hai jise maine chhua hi nahi? Ye aksar drift ya kisi aur ke badlaav ka nishaan hota hai. Teen: neeche ka sarans, "Plan: x to add, y to change, z to destroy", kya mere andaaze se milta hai? Maan lo maine ek tag badla aur plan kehta hai "1 to add, 1 to destroy". To rukna, kyunki ek tag ki wajah se building replace nahi honi chahiye. Aur production mein plan ko pull request mein padha jaata hai, aur apply tabhi hota hai jab ek doosra insaan haan kahe, jaise Session 17 se humne conveyor ke badlaav ke saath kiya.

### [10:20 – 13:10] Scene 5: Terraform Kab Nahi, aur Dusre Raaste
**[VISUAL: A decision card. Small, one-off, learning → console is fine. AWS only and deep integration → CloudFormation. Many clouds, many teams, reviewable → Terraform or OpenTofu. A remote run service shown as an option.]**

**(Voiceover):**
Har kaam ke liye Terraform zaroori nahi. Ek din ka experiment ho, jise kal hatana hai, to console theek hai, jaise humne Session 8 mein kiya. Agar aap sirf AWS mein ho aur AWS ke saath gehra jodna chahte ho, to CloudFormation bhi ek raasta hai. Terraform tab chamakta hai jab kai clouds, kai teams, aur review ki zaroorat ho, jaise Atithi mein. Wahi plan ki bhasha AWS, Azure aur GCP par chalti hai, bas contractor badalta hai: ek provider se doosre. Aur ek aur option: terraform ko ek service par chalana, jo state, lock aur plan ke comment sambhalti hai. Hum pehle ye seekhenge ki ye sab haath se kaise chalta hai, kyunki tool badal jaate hain, par vichar wahi rehta hai.

### [13:10 – 15:15] Scene 6: Lab: Bina Cloud ke Practice
**[VISUAL: `terraform version`. A `main.tf` using the `local` provider that writes `hello.txt`. `init`, `plan`, `apply`, then a change of content and a second plan with `~ update` or `-/+`, then `destroy`.]**

**(Voiceover):**
Lab. Terraform ko official docs ke steps se install karo aur `terraform version` chalao. Bina cloud ke practice ke liye:
```hcl
resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello, Atithi"
}
```
`terraform init`, `terraform plan`, `terraform apply`. File ban gayi. Ab content badlo aur `plan` padho: kya `~` dikha ya `-/+`? Ek aur step: file ko haath se hata do aur `plan` dobara chalao. Terraform kehega ki ek aur banani hai. Aakhir mein `terraform destroy`. Ye bina kisi risk ke poora workflow hai, aur plan padhne ki pehli practice.

### [15:15 – 15:45] Scene 7: Recap aur Bridge
**[VISUAL: A card: "IaC = repeatable, reviewable, versioned · init / plan / apply / destroy · plan symbols + ~ - -/+ · three questions before every apply".]**

**(Voiceover):**
Recap: IaC, workflow aur plan padhna. Ab master plan ki bhasha: HCL.

---

# 📺 EPISODE 2: Master Plan ki Bhasha

### [00:00 – 01:50] Scene 1: Bees Line, Ek Building
**[VISUAL: A twenty-line Terraform file creating a door guard and a building. After `apply`, the AWS console shows both, tagged `Name: atithi-web`.]**

**(Voiceover):**
Bees line ki ek file, aur ek building aur ek door guard taiyaar. Session 8 mein humne wahi launch form ke das click kiye the. Ab wo likha hua hai. Terraform ki bhasha HCL hai, jo JSON se zyada padhne layak aur YAML se zyada saaf hai. Aaj hum uske chaar building blocks seekhte hain: provider, resource, variable aur output. Aur teen aur chhoti cheezein jo roz kaam aati hain: locals, count aur for_each.

### [01:50 – 04:30] Scene 2: Provider aur Resource
**[VISUAL: A `terraform` block with `required_version` and `required_providers` (aws, version constraint). A `provider "aws" { region = var.region }`. A `resource "aws_instance" "web"` with its parts labelled: block type, resource type, local name, arguments.]**

**(Voiceover):**
`terraform` block mein Terraform ka version aur required providers, aur unke version constraints, jaise `~> 5.0`, jiska matlab 5 ke andar ke naye versions, par agle major version nahi. Provider docs mein dekho ki aapke time par kaun sa major version chalta hai. `provider "aws"` mein region jaise settings. Credentials code mein nahi, kabhi nahi. Wo environment variables, ek profile, ya ek IAM role se aate hain, jaise Session 9 mein. `resource` block ka format: `resource "TYPE" "NAME" { ... }`, jaise `resource "aws_instance" "web"`. Type batata hai kya banana hai, name sirf Terraform ke andar ka label, aur andar arguments, jaise `instance_type`. Doosre resource ka reference aise: `aws_security_group.web.id`.

### [04:30 – 07:30] Scene 3: Variable, Local aur Output
**[VISUAL: `variable "instance_type" { type = string  default = "t3.micro"  description = "Building size" }`. A `validation` block rejecting a bad value. `locals { tags = { Owner = "atithi", Env = var.env } }`. `output "public_ip" { value = aws_instance.web.public_ip }`. A `sensitive = true` variable.]**

**(Voiceover):**
Variable plan ke inputs hain. Har variable ka `type`, `description` aur kabhi `default`. `validation` block galat input pakadta hai, jaise instance type ki list se bahar. `sensitive = true` log aur plan mein value chhupata hai, par ek dhyaan: wo state mein phir bhi hoti hai, jo hum agle episode mein dekhenge. Values `terraform.tfvars` file, `-var` flag, ya `TF_VAR_naam` environment variable se aati hain. Locals ek plan ke andar ke naam hain, jaise saari tags ek jagah. Output wo cheezein jo apply ke baad dikhani hain, jaise public IP, aur `terraform output` se baad mein bhi mil jaati hain. Aur Session 14 yaad rakho: `cidrsubnet("10.0.0.0/16", 8, 1)` ek function hai jo `10.0.1.0/24` nikaal deta hai, to subnet ka hisaab Terraform khud karta hai.

### [07:30 – 10:00] Scene 4: count aur for_each
**[VISUAL: Three door guard rules written by hand versus one block with `for_each = toset(var.ports)`. A subnet list built with `count = 2`. A warning: removing the middle item of a `count` list shifts everything after it, while `for_each` keeps the names.]**

**(Voiceover):**
Ek hi cheez kai baar chahiye ho to count ya for_each. `count = 2` do copy banata hai, aur `count.index` se har ek ka number. `for_each = toset(var.ports)` ek ek value ke liye ek copy banata hai, aur har ek ka naam us value se bandh jaata hai. Fark ye hai ki `count` mein list ke beech ki cheez hatao, to uske baad ki saari cheezein khiskengi aur Terraform unhe hatakar dobara banayega. `for_each` mein sirf wohi hatega jo aapne hataya. Isliye aksar for_each behtar hai. Aur ek aur function: `merge(local.tags, { Name = "web" })` do maps ko jod deta hai.

### [10:00 – 12:30] Scene 5: Expression aur Condition
**[VISUAL: A conditional `instance_type = var.env == "prod" ? "t3.medium" : "t3.micro"`. A `for` expression building a map of subnet names to IDs. `terraform console` evaluating `cidrsubnet("10.0.0.0/16", 8, 2)` and printing `10.0.2.0/24`.]**

**(Voiceover):**
Master plan mein thodi soch bhi likhi jaati hai. Condition: `var.env == "prod" ? "t3.medium" : "t3.micro"`, yaani production mein bada, baaki mein chhota. `for` expression: ek list se naya map banana, jaise subnet ke naam se unka ID. Aur functions: `cidrsubnet`, `merge`, `lookup`, `length`, `format`. In sab ko aazmane ke liye `terraform console`: ek chhoti shell jahan aap expression likhkar turant jawab dekhte ho, jaise `cidrsubnet("10.0.0.0/16", 8, 2)` ka jawab `10.0.2.0/24`. Seedha niyam: expression ko sasta rakho. Agar ek line samajhne mein ek minute lage, to use locals mein todo ya naam do, kyunki ye bhi code hai jise koi aur review karega.

### [12:30 – 15:00] Scene 6: Lab: Building aur Door Guard
**[VISUAL: A project with `main.tf`, `variables.tf`, `outputs.tf`, `terraform.tfvars`. A data source for the latest Ubuntu AMI, an `aws_security_group` allowing port 22 from my IP and port 80 from anywhere, and an `aws_instance`. `plan`, `apply`, the public IP in the output, `curl` or SSH, then `destroy`.]**

**(Voiceover):**
Lab. Teen file banao: `main.tf`, `variables.tf`, `outputs.tf`. Provider aur region ek variable se. Ek door guard `aws_security_group`: port 22 sirf aapke IP se, jo ek variable ho, aur port 80 sabse. Ek `aws_instance` jo us door guard se jude, chhota size, aur tags `merge` se. Ubuntu ka latest AMI ek data source se dhoondho. `terraform fmt`, `validate`, `plan`, aur plan ko Scene 4 ke teen sawaalon se padho. Phir `apply`, aur output mein public IP se SSH karo. Credentials ke liye `AWS_PROFILE` ya environment, code mein nahi. Aakhir mein `terraform destroy` aur console mein check karo ki building aur door guard dono gaye.

### [15:00 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "provider (contractor) · resource TYPE NAME · variable (type, validation, sensitive) · local · output · count vs for_each · credentials from env or role, never code".]**

**(Voiceover):**
Recap: HCL ke blocks. Ab ek chhupi hui cheez: Terraform ko kaise pata hai ki usne kya banaya hai? Isliye as-built register: state.

---

# 📺 EPISODE 3: As-built Register

### [00:00 – 01:45] Scene 1: Terraform ko Kaise Pata
**[VISUAL: The plan on the left, real buildings on the right, and a ledger file `terraform.tfstate` in the middle mapping each resource block to a real ID. A second `apply` shows "No changes".]**

**(Voiceover):**
Aapne ek building banayi. Dobara `terraform apply` karte ho, to wo doosri building kyun nahi banata? Kyunki contractor ek as-built register rakhta hai: state file. Usme likha hai ki master plan ka har resource asli duniya ki kaun si cheez hai: `aws_instance.web` ka matlab `i-0abc...`. Plan chalate waqt Terraform plan, register aur asli duniya teeno ko milata hai. Isliye state Terraform ki yaadashta hai, aur use samajhna sabse zaroori cheezon mein se ek hai.

### [01:45 – 04:25] Scene 2: State ke Khatre
**[VISUAL: Three jobs of state: mapping, dependency metadata, performance. Three dangers: secrets in plain text inside the file, a lost file means Terraform forgets its buildings, two people applying at the same time corrupt it.]**

**(Voiceover):**
State teen kaam karti hai: plan aur asli resources ka mapping, dependencies ki jaankari, aur performance. Par khatre bhi hain. Ek: state mein sensitive values, jaise database ka password, plain text mein ho sakti hain, chahe aapne `sensitive = true` likha ho. Isliye state ko Git mein kabhi commit mat karo, jaise Session 20 ka secrets wala sabak. Do: state kho jaye to Terraform bhool jaata hai ki kya banaya tha, aur dobara sab banane ki koshish karega. Teen: do log ek saath apply karein to state bigad sakti hai. Isliye team ke saath state ko remote backend mein, versioning aur locking ke saath rakhte hain, jo agle session mein hai.

### [04:25 – 06:55] Scene 3: Drift
**[VISUAL: An engineer changes a door guard rule in the console. `terraform plan` shows `~ update in-place` for the rule. A choice: bring the code back as truth with `apply`, or update the code to match the change.]**

**(Voiceover):**
Agar koi console mein jaakar resource badal de, to asli duniya aur register alag ho jaate hain. Isko drift kehte hain. `terraform plan` ise pakad leta hai: wo dikhata hai ki wapas code jaisa kar dega. Ab do raaste. Agar console wala badlaav galat tha, to `apply` use mita dega. Agar sahi tha, to code ko badlo, pull request se, aur phir apply. Seedha niyam: jo cheez Terraform se bani hai, use console se mat badlo. Kabhi emergency mein badalna pade, to turant code mein wahi badlaav likho. Nahi to agle apply par wo badlaav chupchap mit jaayega, aur kisi ko pata bhi nahi chalega kyun.

### [06:55 – 09:40] Scene 4: State ke Commands aur Import
**[VISUAL: Commands. `terraform state list`, `terraform state show aws_instance.web`, `terraform plan -refresh-only`, `terraform state mv`, `terraform state rm`. An `import { to = aws_s3_bucket.photos  id = "atithi-photos-123" }` block. A `moved { from = aws_instance.web  to = aws_instance.app }` block.]**

**(Voiceover):**
State ko dekhne ke liye `terraform state list` aur `terraform state show aws_instance.web`. `terraform plan -refresh-only` sirf register ko asli duniya ke hisaab se update dikhata hai, bina kuch badle. Ek purani cheez, jo haath se bani thi, ab master plan mein laani ho, to import: ek `import` block jisme `to` aur asli `id`, ya purani command `terraform import`. Import ke baad plan mein koi badlaav nahi dikhna chahiye, nahi to code asli cheez se milta nahi. Ek aur jaal: kisi resource ka naam badal do, to Terraform use hatakar naya banayega. Isse bachne ke liye `moved` block ya `terraform state mv`. State ko haath se edit mat karo, aur `state rm` jaisi commands bahut sochkar.

### [09:40 – 12:25] Scene 5: Secret ko State se Door Rakho
**[VISUAL: A database definition with a `password` argument in plain text that appears in the state file. Two safer paths: the cloud's managed password option that never passes through the plan, and a reference to a secret read at run time. A caution on `sensitive = true`: hides output, not the state.]**

**(Voiceover):**
State mein secret ka sabse aam raasta database ka password hai. Agar plan mein `password = "..."` likha, to wo state mein plain text mein jaayega, aur `sensitive = true` sirf screen par chhupata hai. Do behtar raaste. Ek: cloud ka managed password option, jaise RDS ka, jisme password Secrets Manager mein khud bante hain aur Terraform ke paas kabhi aate hi nahi. Do: password ko ek secret store mein rakho aur code mein sirf uska naam. Aur ek aur niyam: state ko wahi samjho jo ek key cabinet hota hai, yaani use ek remote backend mein, encryption aur kam logon ki pahunch ke saath rakho. Jo secret kabhi state mein gaya, usse badal do.

### [12:25 – 15:00] Scene 6: Lab: Register Dekho aur Drift Banao
**[VISUAL: After `apply`, `terraform state list`, `terraform state show`. A tag changed by hand in the console. `terraform plan` shows the drift. `.gitignore` with `*.tfstate`, `*.tfstate.*`, `.terraform/`. `.terraform.lock.hcl` committed.]**

**(Voiceover):**
Lab. Pichhle lab ki building dobara banao. `terraform state list`, aur `terraform state show aws_instance.web`. `terraform.tfstate` ko sirf padho, haath se edit mat karo, aur dekho ki usme kya kya likha hai: ID, AMI, IP, aur agar koi password variable ho to wo bhi. Ab console mein jaakar building ka ek tag badal do, aur `terraform plan` chalao: drift dikhega. `apply` se wapas code jaisa hoga. Phir resource ka local name badlo, `web` se `app`, aur plan padho: `-/+`. Ek `moved` block lagao aur plan phir dekho: ab koi replace nahi. Repo ke `.gitignore` mein `*.tfstate`, `*.tfstate.*` aur `.terraform/` daalo, aur `.terraform.lock.hcl` commit karo, taaki provider versions tay rahein.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "state = mapping + secrets · never in Git · drift: console change shows up in plan · import brings old buildings in · rename needs `moved` · lock file in Git".]**

**(Voiceover):**
Recap: state, drift, import aur moved. Ab dependencies, data sources, aur ek surakshit tareeke se kaam karna.

---

# 📺 EPISODE 4: Pehle Kaun, Phir Kaun

### [00:00 – 02:20] Scene 1: Dependency Graph
**[VISUAL: A graph: campus → wing → door guard → building. Terraform builds from left to right and destroys in reverse. Two independent branches built side by side.]**

**(Voiceover):**
Building banane se pehle wing chahiye, aur wing se pehle campus. Terraform ye order khud tay karta hai, kyunki jab aap ek resource ka reference doosre mein dete ho, wo ek dependency graph banata hai. Aapko "pehle ye, phir wo" likhna nahi padta. Jo cheezein ek doosre par nirbhar nahi, wo ek saath banti hain, to apply tez hota hai. Aur hatate waqt ulta kram chalta hai: pehle building, phir wing, phir campus. Ye Session 14 ka wahi kram hai jo cleanup mein hum haath se likhte the.

### [02:20 – 04:40] Scene 2: Implicit, Explicit aur Data Source
**[VISUAL: `subnet_id = aws_subnet.public.id` (implicit). `depends_on = [aws_iam_role_policy.app]` (explicit). A data source `data "aws_vpc" "default" { default = true }` reading an existing item, and a note "resource creates and owns; data only reads".]**

**(Voiceover):**
Reference dene se implicit dependency banti hai: `subnet_id = aws_subnet.public.id`. Kabhi dependency code mein dikhti nahi, jaise IAM policy attach hone ke baad hi building ka kaam shuru ho, to `depends_on` explicit likhte hain. Data source pehle se maujud cheez ki jaankari padhta hai, use banata nahi: `data "aws_vpc" "default"` default campus dhoondhta hai, aur `data "aws_ami"` Session 10 ka latest AMI. Resource banata aur sambhalta hai, data source sirf padhta hai. Ye dono mix mat karo, aur data source mein filter itna saaf rakho ki ek hi jawab aaye.

### [04:40 – 07:15] Scene 3: lifecycle ke Taale
**[VISUAL: A resource with `lifecycle { prevent_destroy = true }` and a plan that refuses. Other options: `create_before_destroy`, `ignore_changes = [tags]`, `replace_triggered_by`. A database icon marked "never by accident".]**

**(Voiceover):**
Kuch resources galti se bhi nahi hatne chahiye, jaise records office ka database. Unke `lifecycle` block mein `prevent_destroy = true`: ab `terraform destroy` ya replace wali koi bhi plan error degi. `create_before_destroy` naya pehle banata hai aur purana baad mein hatata hai, jo tab kaam aata hai jab downtime nahi chahiye. `ignore_changes` un fields ko chhod deta hai jinhe koi aur badalta hai, jaise Auto Scaling ki desired count. Ye taale bhi code hain, isliye pull request mein dikhte hain. Aur ek aur: terraform ko apply karne wale role ko bhi sirf zaroori ijaazat do, Session 9 ka least privilege.

### [07:15 – 10:05] Scene 4: Surakshit Workflow ki Aadatein
**[VISUAL: A checklist: `terraform fmt`, `terraform validate`, plan reviewed in a pull request, `plan -out` then `apply` of that exact plan, avoid `-target`, pin provider and Terraform versions, tags on everything, no secrets in code.]**

**(Voiceover):**
Surakshit workflow ki aadatein. `terraform fmt` code saaf karta hai, `terraform validate` galtiyan pakadta hai. Plan ko pull request mein review karo. Production mein `terraform plan -out=tfplan` aur phir `terraform apply tfplan`, taaki jo review hua wahi lage. `-target` se bacho, kyunki wo state ko adhoora bana sakta hai. `-auto-approve` sirf pipeline mein, jahan pehle se review ho chuka ho. Provider aur Terraform ke versions pin karo. Har resource par tags, jaise `Owner`, `Env` aur `Project`, taaki cost aur maalik pata chale. Aur secrets code mein nahi: database password ke liye, jaise Session 13 mein, Secrets Manager ka managed option, taaki password state mein bhi na ho.

### [10:05 – 13:20] Scene 5: Lab: Session 14 ka Public Wing, Code Mein
**[VISUAL: A project with a VPC, a public subnet from `cidrsubnet`, an internet gateway, a route table with `0.0.0.0/0 → igw` and an association, a door guard, and an EC2. `terraform graph | dot -Tpng` showing the dependency picture. `plan`, `apply`, SSH, then `destroy` removing things in reverse.]**

**(Voiceover):**
Lab. Session 14 ka public wing ab master plan mein likho. Campus `aws_vpc`, `10.0.0.0/16`. Ek public subnet, `cidrsubnet(aws_vpc.main.cidr_block, 8, 1)`. Internet gateway. Route table jisme `0.0.0.0/0` gateway ki taraf jaaye, aur use subnet se `aws_route_table_association` se jodo. Ek door guard, aur ek building jisme public IP ho. Sab kuch references se jodo, aur tags `merge` se. `terraform fmt`, `validate`, `plan`: chhe se aath resources dikhne chahiye. Ek hi `apply`. Agar `graphviz` hai to `terraform graph | dot -Tpng > graph.png` se dependency ki tasveer dekho. Phir SSH karo. Aakhir mein `terraform destroy`: dekho ki cheezein ulte kram mein hatti hain. Ye wahi campus hai jo Session 14 mein dus se zyada click mein bana tha. Ab ek command mein banta aur hatta hai.

### [13:20 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "references = dependencies · depends_on when hidden · data reads, resource owns · lifecycle prevent_destroy · plan -out then apply that plan · tags, pins, no secrets in code". Then a stack of standard blueprints and a locked register book appear.]**

**(Voiceover):**
Recap: Terraform ki neev. Ab master plan ko team ke liye taiyaar karte hain: standard designs yaani modules, ek shared register jis par lock ho, aur Atithi ka poora campus ek hi plan se. Agle session mein.

---

# 📎 Student handout: Session 27 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| IaC | Repeatable, reviewable, versioned, ek command mein banao aur hatao |
| Terraform / OpenTofu | Banane ke liye; andar ki setup ke liye Ansible |
| Workflow | `init`, `plan`, `apply`, `destroy` |
| Plan symbols | `+` banega, `~` badlega, `-` hatega, `-/+` replace |
| Plan ke teen sawaal | Kya hatega? Kuch anjaana badla? Ginti andaaze se milti hai? |
| Provider | `required_providers`, version constraint `~>`; credentials env, profile ya role |
| Resource | `resource "TYPE" "NAME"`; reference `type.name.attr` |
| Variable | `type`, `description`, `default`, `validation`, `sensitive`; tfvars, `-var`, `TF_VAR_` |
| Locals, outputs | Plan ke andar ke naam; apply ke baad ke jawab |
| count vs for_each | `count` mein beech ka hatana sab khiskata hai; `for_each` naam se bandha |
| State | Mapping + secrets; Git mein nahi; lost = bhool gaya |
| Drift | Console badlaav plan mein dikhta hai; code mein likho ya apply se mitao |
| State commands | `state list`, `state show`, `plan -refresh-only`, `state mv`, `import`, `moved` |
| Lock file | `.terraform.lock.hcl` commit karo |
| Dependencies | Reference = implicit; `depends_on` = explicit; data source sirf padhta hai |
| lifecycle | `prevent_destroy`, `create_before_destroy`, `ignore_changes` |
| Workflow aadatein | `fmt`, `validate`, `plan -out`, no `-target`, pins, tags, secrets bahar |
| Safai | `terraform destroy`, console mein check |

# ✍️ 02: SCRIPT — SESSION-27: Terraform Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S27`
- **Focus:** Infrastructure as Code idea, Terraform workflow, HCL (providers/resources/variables/outputs), state, data sources & dependencies
- **Episodes:**
  - Episode 1: Infrastructure as Code: Console Clicking ka Ant
  - Episode 2: HCL ki Basics: Provider, Resource, Variable, Output
  - Episode 3: State: Terraform ki Yaadashta
  - Episode 4: Dependencies, Data Sources aur Safe Workflow

---

# 📺 EPISODE 1: Infrastructure as Code

### [00:00 – 01:15] Scene 1: "Staging Production Jaisa Kyun Nahi?"
**[VISUAL: Two environments built by hand by two engineers months apart. A diff shows a missing security group rule and a different instance size. A bug appears only in production.]**

**(Voiceover):**
Staging aur production haath se, console mein click karke banaye gaye the, alag alag logon ne, alag alag samay par. Ek mein ek security group rule hai, doosre mein nahi. Bug sirf production mein aata hai, aur koi nahi jaanta kyun. Infrastructure as Code, IaC, is problem ko khatam karta hai: infrastructure ko code mein likho, Git mein rakho, aur har baar ek jaisa banao.

### [01:15 – 05:00] Scene 2: IaC ke Fayde aur Terraform
**[VISUAL: A list of benefits: repeatable, reviewable (PRs), versioned, faster, documented, easy to destroy. A map of tools: Terraform/OpenTofu (provisioning, multi-cloud), CloudFormation (AWS), Ansible (configuration).]**

**(Voiceover):**
IaC se infrastructure repeatable hota hai, PR mein review ho sakta hai, history rehti hai, aur ek command se bana aur hata sakte ho. Terraform HashiCorp ka tool hai jo AWS, Azure, GCP, Kubernetes aur hazaaron providers ke saath kaam karta hai. Ek aur compatible open source fork OpenTofu bhi hai. Terraform declarative hai: aap batate ho kya chahiye, wo tay karta hai kaise. Provisioning ke liye Terraform, aur machine ke andar ki configuration ke liye Ansible, jo hum agle sessions mein dekhenge.

### [05:00 – 08:30] Scene 3: Terraform Workflow
**[VISUAL: A cycle: write → `terraform init` → `terraform plan` (preview) → `terraform apply` → `terraform destroy`. A plan output with `+ create`, `~ update`, `- destroy` colours.]**

**(Voiceover):**
Workflow chaar commands mein. `terraform init` providers download karta hai. `terraform plan` dikhata hai ki kya banega, badlega ya hatega, bina kuch kiye. `terraform apply` use asli mein lagu karta hai. `terraform destroy` sab hata deta hai. Plan sabse zaroori step hai. Isse padhna seekho, kyunki "- destroy" dikhe aur aap dhyaan na do, to production database bhi ja sakta hai. Production mein plan PR mein review hota hai, aur apply pipeline se.

### [08:30 – 11:30] Scene 4: Lab: Terraform Install aur Local File
**[VISUAL: `terraform version`. A `main.tf` using the `local` provider creating `hello.txt`. `init`, `plan`, `apply`, then change the content and apply again.]**

**(Voiceover):**
Lab: Terraform install karo, official docs ke steps se, aur `terraform version` chalao. Bina cloud ke practice ke liye:
```hcl
resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello, Terraform"
}
```
`terraform init`, `terraform plan`, `terraform apply`. File ban gayi. Ab content badlo aur `plan` dekho: update dikhega. `terraform destroy` se file hat jayegi. Ye bina risk ke poora workflow hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "IaC = repeatable + reviewable · init/plan/apply/destroy · always read the plan".]**

**(Voiceover):**
Recap: IaC aur Terraform workflow. Ab HCL, yaani Terraform ki bhasha.

---

# 📺 EPISODE 2: HCL ki Basics

### [00:00 – 01:15] Scene 1: Ek File, Poora Server
**[VISUAL: A 20-line Terraform file creating a security group and an EC2 instance. The AWS console shows them appear after apply.]**

**(Voiceover):**
Bees line ki ek file aur ek EC2 instance aur security group taiyaar. Terraform ki bhasha HCL hoti hai, jo YAML ya JSON se zyada padhne layak hai. Aaj hum uske char building blocks seekhte hain: provider, resource, variable aur output.

### [01:15 – 05:00] Scene 2: Provider aur Resource
**[VISUAL: A `terraform` block with `required_providers` (aws ~> 5.0), a `provider "aws" { region = var.region }`, and a `resource "aws_instance" "web"` block. Labelled: type, name, arguments.]**

**(Voiceover):**
`terraform` block mein required providers aur unke version constraints. `provider "aws"` mein region jaise settings. Credentials code mein nahi, environment ya IAM role se. `resource` block ka format: `resource "TYPE" "NAME" { ... }`. Jaise `resource "aws_instance" "web"`. Type batata hai kya banana hai, name Terraform ke andar ka label, aur andar arguments jaise `ami` aur `instance_type`. Resource ko doosre resource se `aws_security_group.web.id` jaise reference se jodte hain.

### [05:00 – 08:30] Scene 3: Variables, Locals aur Outputs
**[VISUAL: `variable "instance_type" { type = string; default = "t3.micro" }`, `locals { tags = {...} }`, `output "public_ip" { value = aws_instance.web.public_ip }`. A `terraform.tfvars` file. `-var` flag.]**

**(Voiceover):**
Variable input hai: `variable "instance_type"` type aur default ke saath, aur `var.instance_type` se use. Values `terraform.tfvars` file ya `-var` flag se dete hain. Locals andar ke calculated values ke liye. Output wo cheez hai jo apply ke baad dikhani hai, jaise public IP. Sensitive output ko `sensitive = true` se chhupa sakte ho. Aur `count`, `for_each` se ek resource ke kai copies banate hain, aur functions jaise `join`, `lookup` kaam aate hain.

### [08:30 – 11:30] Scene 4: Lab: EC2 + Security Group
**[VISUAL: A project with `main.tf`, `variables.tf`, `outputs.tf`. A data source for the latest Amazon Linux AMI. `terraform apply` creates a SG and an instance; output prints the IP. Then `terraform destroy`.]**

**(Voiceover):**
Lab (AWS account ke saath, free-tier type): ek security group banao jisme port 80 inbound, aur ek `aws_instance` jo us group se jude. AMI ke liye data source `aws_ami` se naya Amazon Linux dhoondho, taaki ID hardcode na ho. `outputs.tf` mein `public_ip`. `terraform plan` se dekho ki kya kya banega, aur `apply` ke baad IP browser mein try karo. Kaam ke baad `terraform destroy`. Ye wahi cheez hai jo hum EC2 session mein click karke karte the, ab code mein.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "provider · resource TYPE NAME · variable/local/output · references · for_each".]**

**(Voiceover):**
Recap: HCL ke blocks. Ab ek chhupi hui cheez: Terraform ko kaise pata ki wo kya bana chuka hai? State.

---

# 📺 EPISODE 3: State — Terraform ki Yaadashta

### [00:00 – 01:15] Scene 1: Terraform ko Pata Hai Tumne Kya Banaya
**[VISUAL: Terraform code on the left, real cloud resources on the right, and in between a ledger file `terraform.tfstate` mapping each resource block to a real ID.]**

**(Voiceover):**
Aapne ek EC2 banaya. Dobara `terraform apply` karoge to wo dusra EC2 kyun nahi banata? Kyunki Terraform ek record rakhta hai: state file. Isme likha hota hai ki aapke code ka har resource asli duniya ki kaun si cheez hai. State Terraform ki yaadashta hai, aur ise samajhna sabse zaroori cheezon mein se ek hai.

### [01:15 – 05:00] Scene 2: State kya Karta Hai aur Khatre
**[VISUAL: Three roles: mapping, metadata/dependencies, performance. Dangers: state may contain secrets in plain text; if lost, Terraform forgets; if two people apply together, corruption.]**

**(Voiceover):**
State teen kaam karti hai: code aur asli resources ka mapping, dependencies ki jaankari, aur performance. Lekin khatre bhi hain. State mein sensitive values, jaise database password, plain text mein ho sakti hain, to ise Git mein kabhi commit mat karo. State kho jaye to Terraform bhool jata hai ki kya banaya tha. Aur do log ek saath apply karein to state corrupt ho sakti hai. Isliye team ke saath kaam karne ke liye state ko remote backend mein rakhte hain, locking ke saath.

### [05:00 – 08:30] Scene 3: Drift aur State Commands
**[VISUAL: Someone changes a security group in the console. `terraform plan` shows drift: "~ update in-place". Commands: `terraform state list`, `terraform state show`, `terraform import`, `terraform refresh`/`plan -refresh-only`.]**

**(Voiceover):**
Agar koi console mein jaakar resource badal de, to asli duniya aur state alag ho jaate hain, ise drift kehte hain. `terraform plan` ise pakad leta hai aur dikhata hai ki wapas code jaisa kar dega. `terraform state list` aur `state show` se aap dekh sakte ho ki Terraform kya jaanta hai. `terraform import` se pehle se bani cheez ko Terraform mein laate hain. Aur rule: Terraform se bani cheez ko console se mat badlo, warna drift aur confusion.

### [08:30 – 11:30] Scene 4: Lab: State ko Dekho aur Drift Banao
**[VISUAL: After apply, open `terraform.tfstate` (read only). `terraform state list`. Manually change an instance tag in the console; `terraform plan` shows the diff. `.gitignore` entries for state files.]**

**(Voiceover):**
Lab: apply ke baad `terraform state list` aur `terraform state show aws_instance.web` chalao. `terraform.tfstate` ko sirf padho, haath se edit mat karo. Ab AWS console mein us instance ka ek tag badal do aur `terraform plan` chalao: drift dikhega. `apply` se wapas code ke mutabiq ho jayega. Apne repo ke `.gitignore` mein `*.tfstate`, `*.tfstate.*` aur `.terraform/` zaroor daalo. Aur `.terraform.lock.hcl` ko commit karo, taaki provider versions fixed rahein.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "state = mapping · contains secrets · never in Git · drift · remote backend later".]**

**(Voiceover):**
Recap: state, drift, aur uske khatre. Ab dependencies, data sources, aur ek surakshit tareeke se kaam karna.

---

# 📺 EPISODE 4: Dependencies, Data Sources aur Safe Workflow

### [00:00 – 01:15] Scene 1: Pehle Kaun, Phir Kaun
**[VISUAL: A dependency graph: VPC → Subnet → Security Group → EC2. Terraform builds them in order, and destroys in reverse. A `terraform graph` visual.]**

**(Voiceover):**
EC2 banane se pehle subnet chahiye, aur subnet se pehle VPC. Terraform ye order khud tay karta hai, kyunki jab aap ek resource ka reference doosre mein dete ho, wo dependency graph banata hai. Aapko "pehle ye, phir wo" likhna nahi padta.

### [01:15 – 05:00] Scene 2: Implicit vs Explicit Dependency, Data Sources
**[VISUAL: `subnet_id = aws_subnet.public.id` (implicit). `depends_on = [aws_iam_role_policy.x]` (explicit). A `data "aws_vpc" "default" { default = true }` reading existing info.]**

**(Voiceover):**
Reference dene se implicit dependency banti hai: `subnet_id = aws_subnet.public.id`. Kabhi kabhi dependency code mein dikhti nahi, jaise IAM policy attach hone ke baad hi app ka kaam shuru ho, to `depends_on` explicit likhte hain. Data source pehle se maujud cheez ki jaankari padhta hai, bina use banaye: `data "aws_vpc" "default"` default VPC dhoondhta hai. Ye resource se alag hai: resource banata aur manage karta hai, data source sirf padhta hai.

### [05:00 – 08:30] Scene 3: Safe Workflow ke Niyam
**[VISUAL: A checklist: `terraform fmt`, `terraform validate`, plan reviewed in PR, `-target` avoided, `lifecycle { prevent_destroy = true }` on critical resources, version pinned, tags on everything.]**

**(Voiceover):**
Surakshit workflow. `terraform fmt` code ko saaf karta hai, `terraform validate` galtiyan pakadta hai. Plan ko PR mein review karo. `-target` se bachna, kyunki wo state ko adhoora bana sakta hai. Critical resources, jaise database, par `lifecycle { prevent_destroy = true }` lagao. Provider aur Terraform ka version pin karo. Aur har resource par tags, jaise `Owner` aur `Env`, taaki cost aur ownership pata chale. Ye aadatein baad mein bade nuksaan se bachati hain.

### [08:30 – 11:30] Scene 4: Lab: Network + Server Poora Code Mein
**[VISUAL: A Terraform project with a VPC, public subnet, internet gateway, route table, security group, and EC2. `terraform graph | dot -Tpng` picture. `terraform plan` shows 8 resources; `apply`; then `destroy` in reverse order.]**

**(Voiceover):**
Lab: Session 14 ka public VPC ab Terraform mein likho: VPC, public subnet, internet gateway, route table aur association, security group, aur ek EC2. Sab references se jodo. `terraform fmt` aur `terraform validate` chalao, phir `plan` aur `apply`. Agar `graphviz` installed hai, `terraform graph | dot -Tpng > graph.png` se dependency picture dekho. `terraform destroy` chalao aur dekho ki cheezein ulte kram mein hatti hain. Ye lab poora IaC ka asli maza hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "references = dependencies · data = read only · fmt/validate/plan review · prevent_destroy · pin versions".]**

**(Voiceover):**
Recap: Terraform ki foundation. Ab ise asli AWS projects par lagate hain: modules, remote state, aur ek poora 3-tier architecture. Agle session mein.

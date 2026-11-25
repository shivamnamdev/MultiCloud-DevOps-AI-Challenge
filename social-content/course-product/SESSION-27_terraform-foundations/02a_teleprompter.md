# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-27_terraform-foundations

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,557 · **Episodes:** 4

---

# EPISODE 1: Console Clicking ka Ant

## "Staging Production Jaisa Kyun Nahi?"

Atithi ka staging campus aur production campus haath se bane the, console mein click karke, alag alag engineers ne, alag alag mahine mein. Ek mein door guard ki list mein ek rule hai, doosre mein nahi. Ek mein building ka size chhota hai. Bug sirf production mein aata hai, aur koi nahi jaanta kyun. Session 1 mein humne kaha tha ki is duniya mein buildings ki photocopy ho sakti hai. Par jab tak har baar koi insaan click karke banata hai, har copy thodi alag banti hai. Hal: campus ka naksha ek document mein likho, ek tool use padhe, aur har baar wahi banaye.

## Infrastructure as Code

Infrastructure as Code, IaC, ka matlab hai ki campus ka naksha code mein hota hai. Faayde: repeatable, kyunki wahi code wahi campus banata hai. Reviewable, kyunki badlaav pull request mein dikhta hai. History, kyunki Git mein har badlaav ka register hai. Aur hatana bhi ek command ka kaam. Terraform HashiCorp ka tool hai jo AWS, Azure, GCP, Kubernetes aur hazaaron providers ke saath chalta hai. Uska ek open source fork OpenTofu bhi hai, jo lagbhag wahi kaam karta hai, aur license ki wajah se kuch teams use chunti hain. Terraform declarative hai: aap likhte ho kya chahiye, wo tay karta hai kaise. Buildings banane ke liye Terraform, aur building ke andar ki setup ke liye Ansible, jo agle session mein hai.

## Chaar Commands ka Workflow

Workflow chaar commands mein. terraform init contractors yaani providers ko download karta hai aur ek .terraform folder banata hai. terraform plan dikhata hai ki kya banega, badlega ya hatega, bina kuch kiye. terraform apply use asli mein lagu karta hai, aur ek baar "yes" poochta hai. terraform destroy sab hata deta hai. Plan sabse zaroori step hai. Usme + banega, ~ badlega, - hatega, aur -/+ ka matlab hatao aur dobara banao, aur uske saath "forces replacement" likha hota hai. Agar aap -/+ ya - par dhyaan na do, to production ka database bhi ja sakta hai. Isliye plan padhna ek kaushal hai, jise hum har lab mein abhyas karenge.

## Plan Padhna: Teen Sawaal

Plan padhne ke liye teen sawaal. Ek: kya kuch hatega ya replace hoga? Do: kya koi aisi cheez badal rahi hai jise maine chhua hi nahi? Ye aksar drift ya kisi aur ke badlaav ka nishaan hota hai. Teen: neeche ka sarans, "Plan: x to add, y to change, z to destroy", kya mere andaaze se milta hai? Maan lo maine ek tag badla aur plan kehta hai "1 to add, 1 to destroy". To rukna, kyunki ek tag ki wajah se building replace nahi honi chahiye. Aur production mein plan ko pull request mein padha jaata hai, aur apply tabhi hota hai jab ek doosra insaan haan kahe, jaise Session 17 se humne conveyor ke badlaav ke saath kiya.

## Terraform Kab Nahi, aur Dusre Raaste

Har kaam ke liye Terraform zaroori nahi. Ek din ka experiment ho, jise kal hatana hai, to console theek hai, jaise humne Session 8 mein kiya. Agar aap sirf AWS mein ho aur AWS ke saath gehra jodna chahte ho, to CloudFormation bhi ek raasta hai. Terraform tab chamakta hai jab kai clouds, kai teams, aur review ki zaroorat ho, jaise Atithi mein. Wahi plan ki bhasha AWS, Azure aur GCP par chalti hai, bas contractor badalta hai: ek provider se doosre. Aur ek aur option: terraform ko ek service par chalana, jo state, lock aur plan ke comment sambhalti hai. Hum pehle ye seekhenge ki ye sab haath se kaise chalta hai, kyunki tool badal jaate hain, par vichar wahi rehta hai.

## Lab: Bina Cloud ke Practice

Lab. Terraform ko official docs ke steps se install karo aur terraform version chalao. Bina cloud ke practice ke liye:

terraform init, terraform plan, terraform apply. File ban gayi. Ab content badlo aur plan padho: kya ~ dikha ya -/+? Ek aur step: file ko haath se hata do aur plan dobara chalao. Terraform kehega ki ek aur banani hai. Aakhir mein terraform destroy. Ye bina kisi risk ke poora workflow hai, aur plan padhne ki pehli practice.

## Recap aur Bridge

Recap: IaC, workflow aur plan padhna. Ab master plan ki bhasha: HCL.

---

# EPISODE 2: Master Plan ki Bhasha

## Bees Line, Ek Building

Bees line ki ek file, aur ek building aur ek door guard taiyaar. Session 8 mein humne wahi launch form ke das click kiye the. Ab wo likha hua hai. Terraform ki bhasha HCL hai, jo JSON se zyada padhne layak aur YAML se zyada saaf hai. Aaj hum uske chaar building blocks seekhte hain: provider, resource, variable aur output. Aur teen aur chhoti cheezein jo roz kaam aati hain: locals, count aur for_each.

## Provider aur Resource

terraform block mein Terraform ka version aur required providers, aur unke version constraints, jaise ~> 5.0, jiska matlab 5 ke andar ke naye versions, par agle major version nahi. Provider docs mein dekho ki aapke time par kaun sa major version chalta hai: AWS provider ab 6 par hai, aur ye lab 5 aur 6 dono par chala. provider "aws" mein region jaise settings. Credentials code mein nahi, kabhi nahi. Wo environment variables, ek profile, ya ek IAM role se aate hain, jaise Session 9 mein. resource block ka format: resource "TYPE" "NAME" { ... }, jaise resource "aws_instance" "web". Type batata hai kya banana hai, name sirf Terraform ke andar ka label, aur andar arguments, jaise instance_type. Doosre resource ka reference aise: aws_security_group.web.id.

## Variable, Local aur Output

Variable plan ke inputs hain. Har variable ka type, description aur kabhi default. validation block galat input pakadta hai, jaise instance type ki list se bahar. sensitive = true log aur plan mein value chhupata hai, par ek dhyaan: wo state mein phir bhi hoti hai, jo hum agle episode mein dekhenge. Values terraform.tfvars file, -var flag, ya TF_VAR_naam environment variable se aati hain. Locals ek plan ke andar ke naam hain, jaise saari tags ek jagah. Output wo cheezein jo apply ke baad dikhani hain, jaise public IP, aur terraform output se baad mein bhi mil jaati hain. Aur Session 14 yaad rakho: cidrsubnet("10.0.0.0/16", 8, 1) ek function hai jo 10.0.1.0/24 nikaal deta hai, to subnet ka hisaab Terraform khud karta hai.

## count aur for_each

Ek hi cheez kai baar chahiye ho to count ya for_each. count = 2 do copy banata hai, aur count.index se har ek ka number. for_each = toset(var.ports) ek ek value ke liye ek copy banata hai, aur har ek ka naam us value se bandh jaata hai. Fark ye hai ki count mein list ke beech ki cheez hatao, to uske baad ki saari cheezein ek number khisak jaati hain. Plan mein un par badlaav dikhta hai, aur jis field ko badalne se resource dobara banta hai, wo hatkar dobara bhi banta hai. for_each mein sirf wohi hatega jo aapne hataya. Isliye aksar for_each behtar hai. Aur ek aur function: merge(local.tags, { Name = "web" }) do maps ko jod deta hai.

## Expression aur Condition

Master plan mein thodi soch bhi likhi jaati hai. Condition: var.env == "prod" ? "t3.medium" : "t3.micro", yaani production mein bada, baaki mein chhota. for expression: ek list se naya map banana, jaise subnet ke naam se unka ID. Aur functions: cidrsubnet, merge, lookup, length, format. In sab ko aazmane ke liye terraform console: ek chhoti shell jahan aap expression likhkar turant jawab dekhte ho, jaise cidrsubnet("10.0.0.0/16", 8, 2) ka jawab 10.0.2.0/24. Seedha niyam: expression ko sasta rakho. Agar ek line samajhne mein ek minute lage, to use locals mein todo ya naam do, kyunki ye bhi code hai jise koi aur review karega.

## Lab: Building aur Door Guard

Lab. Teen file banao: main.tf, variables.tf, outputs.tf. Provider aur region ek variable se. Ek door guard aws_security_group: port 22 sirf aapke IP se, jo ek variable ho, aur port 80 sabse. Ek aws_instance jo us door guard se jude, chhota size, aur tags merge se. Ubuntu ka latest AMI ek data source se dhoondho. terraform fmt, validate, plan, aur plan ko Scene 4 ke teen sawaalon se padho. Phir apply, aur output mein public IP se SSH karo. Credentials ke liye AWS_PROFILE ya environment, code mein nahi. Aakhir mein terraform destroy aur console mein check karo ki building aur door guard dono gaye.

## Recap aur Bridge

Recap: HCL ke blocks. Ab ek chhupi hui cheez: Terraform ko kaise pata hai ki usne kya banaya hai? Isliye as-built register: state.

---

# EPISODE 3: As-built Register

## Terraform ko Kaise Pata

Aapne ek building banayi. Dobara terraform apply karte ho, to wo doosri building kyun nahi banata? Kyunki contractor ek as-built register rakhta hai: state file. Usme likha hai ki master plan ka har resource asli duniya ki kaun si cheez hai: aws_instance.web ka matlab i-0abc.... Plan chalate waqt Terraform plan, register aur asli duniya teeno ko milata hai. Isliye state Terraform ki yaadashta hai, aur use samajhna sabse zaroori cheezon mein se ek hai.

## State ke Khatre

State teen kaam karti hai: plan aur asli resources ka mapping, dependencies ki jaankari, aur performance. Par khatre bhi hain. Ek: state mein sensitive values, jaise database ka password, plain text mein ho sakti hain, chahe aapne sensitive = true likha ho. Isliye state ko Git mein kabhi commit mat karo, jaise Session 20 ka secrets wala sabak. Do: state kho jaye to Terraform bhool jaata hai ki kya banaya tha, aur dobara sab banane ki koshish karega. Teen: do log ek saath apply karein to state bigad sakti hai. Isliye team ke saath state ko remote backend mein, versioning aur locking ke saath rakhte hain, jo agle session mein hai.

## Drift

Agar koi console mein jaakar resource badal de, to asli duniya aur register alag ho jaate hain. Isko drift kehte hain. terraform plan ise pakad leta hai: wo dikhata hai ki wapas code jaisa kar dega. Ab do raaste. Agar console wala badlaav galat tha, to apply use mita dega. Agar sahi tha, to code ko badlo, pull request se, aur phir apply. Seedha niyam: jo cheez Terraform se bani hai, use console se mat badlo. Kabhi emergency mein badalna pade, to turant code mein wahi badlaav likho. Nahi to agle apply par wo badlaav chupchap mit jaayega, aur kisi ko pata bhi nahi chalega kyun.

## State ke Commands aur Import

State ko dekhne ke liye terraform state list aur terraform state show aws_instance.web. terraform plan -refresh-only sirf register ko asli duniya ke hisaab se update dikhata hai, bina kuch badle. Ek purani cheez, jo haath se bani thi, ab master plan mein laani ho, to import: ek import block jisme to aur asli id, ya purani command terraform import. Import ke baad plan mein koi badlaav nahi dikhna chahiye, nahi to code asli cheez se milta nahi. Ek aur jaal: kisi resource ka naam badal do, to Terraform use hatakar naya banayega. Isse bachne ke liye moved block ya terraform state mv. State ko haath se edit mat karo, aur state rm jaisi commands bahut sochkar.

## Secret ko State se Door Rakho

State mein secret ka sabse aam raasta database ka password hai. Agar plan mein password = "..." likha, to wo state mein plain text mein jaayega, aur sensitive = true sirf screen par chhupata hai. Do behtar raaste. Ek: cloud ka managed password option, jaise RDS ka, jisme password Secrets Manager mein khud bante hain aur Terraform ke paas kabhi aate hi nahi. Do: password ko ek secret store mein rakho aur code mein sirf uska naam. Aur ek aur niyam: state ko wahi samjho jo ek key cabinet hota hai, yaani use ek remote backend mein, encryption aur kam logon ki pahunch ke saath rakho. Jo secret kabhi state mein gaya, usse badal do.

## Lab: Register Dekho aur Drift Banao

Lab. Pichhle lab ki building dobara banao. terraform state list, aur terraform state show aws_instance.web. terraform.tfstate ko sirf padho, haath se edit mat karo, aur dekho ki usme kya kya likha hai: ID, AMI, IP, aur agar koi password variable ho to wo bhi. Ab console mein jaakar building ka ek tag badal do, aur terraform plan chalao: drift dikhega. apply se wapas code jaisa hoga. Phir resource ka local name badlo, web se app, aur plan padho: ek destroy aur ek create, 1 to add, 1 to destroy. Ek moved block lagao aur plan phir dekho: ab koi replace nahi. Repo ke .gitignore mein .tfstate, .tfstate.* aur .terraform/ daalo, aur .terraform.lock.hcl commit karo, taaki provider versions tay rahein.

## Recap aur Bridge

Recap: state, drift, import aur moved. Ab dependencies, data sources, aur ek surakshit tareeke se kaam karna.

---

# EPISODE 4: Pehle Kaun, Phir Kaun

## Dependency Graph

Building banane se pehle wing chahiye, aur wing se pehle campus. Terraform ye order khud tay karta hai, kyunki jab aap ek resource ka reference doosre mein dete ho, wo ek dependency graph banata hai. Aapko "pehle ye, phir wo" likhna nahi padta. Jo cheezein ek doosre par nirbhar nahi, wo ek saath banti hain, to apply tez hota hai. Aur hatate waqt ulta kram chalta hai: pehle building, phir wing, phir campus. Ye Session 14 ka wahi kram hai jo cleanup mein hum haath se likhte the.

## Implicit, Explicit aur Data Source

Reference dene se implicit dependency banti hai: subnet_id = aws_subnet.public.id. Kabhi dependency code mein dikhti nahi, jaise IAM policy attach hone ke baad hi building ka kaam shuru ho, to depends_on explicit likhte hain. Data source pehle se maujud cheez ki jaankari padhta hai, use banata nahi: data "aws_vpc" "default" default campus dhoondhta hai, aur data "aws_ami" Session 10 ka latest AMI. Resource banata aur sambhalta hai, data source sirf padhta hai. Ye dono mix mat karo, aur data source mein filter itna saaf rakho ki ek hi jawab aaye.

## lifecycle ke Taale

Kuch resources galti se bhi nahi hatne chahiye, jaise records office ka database. Unke lifecycle block mein prevent_destroy = true: ab terraform destroy ya replace wali koi bhi plan error degi. create_before_destroy naya pehle banata hai aur purana baad mein hatata hai, jo tab kaam aata hai jab downtime nahi chahiye. ignore_changes un fields ko chhod deta hai jinhe koi aur badalta hai, jaise Auto Scaling ki desired count. Ye taale bhi code hain, isliye pull request mein dikhte hain. Aur ek aur: terraform ko apply karne wale role ko bhi sirf zaroori ijaazat do, Session 9 ka least privilege.

## Surakshit Workflow ki Aadatein

Surakshit workflow ki aadatein. terraform fmt code saaf karta hai, terraform validate galtiyan pakadta hai. Plan ko pull request mein review karo. Production mein terraform plan -out=tfplan aur phir terraform apply tfplan, taaki jo review hua wahi lage. -target se bacho, kyunki wo state ko adhoora bana sakta hai. -auto-approve sirf pipeline mein, jahan pehle se review ho chuka ho. Provider aur Terraform ke versions pin karo. Har resource par tags, jaise Owner, Env aur Project, taaki cost aur maalik pata chale. Aur secrets code mein nahi: database password ke liye, jaise Session 13 mein, Secrets Manager ka managed option, taaki password state mein bhi na ho.

## Lab: Session 14 ka Public Wing, Code Mein

Lab. Session 14 ka public wing ab master plan mein likho. Campus aws_vpc, 10.0.0.0/16. Ek public subnet, cidrsubnet(aws_vpc.main.cidr_block, 8, 1). Internet gateway. Route table jisme 0.0.0.0/0 gateway ki taraf jaaye, aur use subnet se aws_route_table_association se jodo. Ek door guard, aur ek building jisme public IP ho. Sab kuch references se jodo, aur tags merge se. terraform fmt, validate, plan: saat se das resources dikhne chahiye, kyunki security group ke har rule ko alag resource banao to das. Ek hi apply. Agar graphviz hai to terraform graph | dot -Tpng > graph.png se dependency ki tasveer dekho. Phir SSH karo. Aakhir mein terraform destroy: dekho ki cheezein ulte kram mein hatti hain. Ye wahi campus hai jo Session 14 mein dus se zyada click mein bana tha. Ab ek command mein banta aur hatta hai.

## Recap aur Bridge

Recap: Terraform ki neev. Ab master plan ko team ke liye taiyaar karte hain: standard designs yaani modules, ek shared register jis par lock ho, aur Atithi ka poora campus ek hi plan se. Agle session mein.

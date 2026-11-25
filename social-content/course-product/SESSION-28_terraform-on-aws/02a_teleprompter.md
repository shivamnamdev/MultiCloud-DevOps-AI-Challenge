# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-28_terraform-on-aws

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,496 · **Episodes:** 4

---

# EPISODE 1: Shared Register aur Lock

## Do Contractor, Ek Hi Waqt

Atithi mein ab do engineers campus ka master plan sambhalte hain. Dono ne ek hi samay terraform apply chalaya, apne apne laptop ke register ke saath. Dono ne alag cheezein banayi, ya ek ne doosre ka register overwrite kar diya. Ab asli duniya aur kisi ke register mein mel nahi. Local state ek akele project ke liye theek hai, team ke liye nahi. Iska hal: register ko ek shared jagah rakho, jise sab padhein, aur jis par ek hi samay mein ek hi apply chale. Isko remote state aur locking kehte hain.

## S3 Backend aur Lock

AWS par aam tareeka warehouse hai, yaani S3 bucket. Backend block mein bucket, key, region aur encrypt = true. Bucket par versioning on, taaki register ki purani copy mil sake, Block Public Access on, aur default encryption, jo Session 12 ke saare niyam hain. Lock ka matlab hai ki ek hi samay ek apply chalega. Purane setups mein iske liye DynamoDB table lagti thi. Terraform 1.10 aur uske baad ke versions S3 ka apna lock file option, use_lockfile = true, dete hain, aur DynamoDB wala tareeka ab purana, yaani deprecated, maana jaata hai, jo abhi chalta hai par chetavani deta hai. Apne version ke docs dekh kar sahi option chuno. Ek chhoti jaal: backend block mein variables nahi chalte, isliye alag alag environments ke liye -backend-config file se values do.

## Pehle Bucket, Phir Terraform

Ek sawaal: register ke liye warehouse Terraform se banaye, to us warehouse ka register kahan? Ye chicken-and-egg hai. Aam hal: bucket ko ek baar, ek chhote bootstrap project se, ya AWS CLI se banao, aur uska apna chhota state ek surakshit jagah rakho. Phir asli project mein backend block likho aur terraform init -migrate-state chalao, jo local register ko bucket mein le jaata hai. Bucket ko sambhal kar rakho: usme sirf wahi role likh sake jo Terraform chalata hai, aws:SecureTransport ka Deny rule lagao, purane versions ka lifecycle rule rakho, aur access logs on. Register hi sabse keemti file hai, kyunki usme maujooda campus ki poori kahani hai.

## Ek Bada Register Nahi: Layers mein Todo

Ek hi register mein poora campus rakhoge, to har plan sab kuch dekhega, aur ek galat badlaav sab ko chhoo sakta hai. Isliye layers: network, data aur app ke alag register. Network kam badalta hai, data aur bhi kam, app roz. App wali layer network ke outputs padh sakti hai, jaise terraform_remote_state data source se, ya ek shared parameter store se. Isse ek galti ka daayra, yaani blast radius, chhota rehta hai. App ka apply database ko chhue hi nahi. Aur plan chhote aur tez rehte hain. Seedha rule: jo cheezein alag raftaar se badalti hain, unka register alag.

## Register Bigad Gaya to

Kabhi register hi bigad jaata hai: koi apply beech mein toot gaya, ya kisi ne state rm galat chala diya. Warehouse mein versioning isi din ke liye hai. Pehle dekho ki bucket ki purani versions kaun si hain. Kisi bhi bade kaam, jaise state mv ya import, se pehle terraform state pull > backup.json se ek copy le lo. Bigad jaaye to pichhla theek version wapas rakho, aur turant terraform plan chalao: agar plan saaf aaye, ya sirf wahi badlaav dikhe jo aap jaante ho, to register theek hai. Agar plan mein achanak "sab kuch banana hai" dikhe, to rukna, kyunki Terraform ne apni buildings bhula di hain, aur apply karna sabko doguna bana dega. Lock atke to force-unlock, sirf tab jab pakka ho ki koi apply nahi chal raha.

## Lab: Register ko Warehouse mein Bhejo

Lab:

Dhyaan: us-east-1 mein LocationConstraint nahi dete. Phir backend block jodo aur terraform init -migrate-state. aws s3 ls s3://YOUR-STATE-BUCKET/ se register dekho. Do terminals mein ek saath terraform apply try karo, aur dekho ki doosre ko "state locked" ka error milta hai. Lock atak jaaye to terraform force-unlock sirf tab, jab pakka ho ki koi apply chal nahi raha. Aakhir mein bucket ka version history kholkar dekho ki register ki purani copy kaise wapas milti hai.

## Recap aur Bridge

Recap: shared register, lock, aur layers. Ab master plan ko dohrane se bachate hain: standard designs, yaani modules.

---

# EPISODE 2: Standard Design

## Copy-Paste ka Jungle

Dev, staging aur production, teen campus, aur teen jagah wahi 200 line ka network code, thode se farq ke saath. Ek rule badalna ho to teen jagah edit, aur ek jagah chhoot jaata hai, aur wahi jagah aage chalkar "staging production jaisa kyun nahi" ban jaati hai. Module Terraform ka function hai: ek baar standard design likho, aur alag alag inputs ke saath baar baar bulao.

## Module ka Dhancha

Module ek folder hai jisme .tf files hoti hain: variables.tf mein inputs, main.tf mein resources, outputs.tf mein jo bahar dena hai, aur ek README. Caller use aise bulata hai: module "network" { source = "../../modules/network" name = "dev" cidr = "10.10.0.0/16" }. Module ke outputs ko module.network.public_subnet_ids se padhte hain. Source teen jagah se aa sakta hai: local folder, Git repo git::https://...?ref=v1.2.0, ya Terraform Registry, jahan version likhte hain. Bane banaye registry modules kaam ke hote hain, par unhe use karne se pehle padh lo, aur version pin karo, kyunki ek hi main branch par bharosa Session 20 ke action pin wala khatra hai.

## Achhe Module ke Niyam

Module ke niyam. Inputs kam rakho, aur sirf wahi expose karo jo caller ko badalna hai. Har variable ka type aur description. validation block se galat input pakdo, jaise CIDR ka format, can(cidrhost(var.cidr, 0)). Module ke andar provider configure mat karo, caller karta hai. Tags bahar se pass karo. Module ko Git tag se version do, jaise v1.2.0, aur pull request ke saath badlo, taaki ek badlaav teen campus ko ek saath na tode. Ek module ek kaam kare: network, ya alb, ya database, sab ek mein nahi. Aur over-engineering se bacho: jo pattern do baar dohraya gaya wahi module banane layak hai. Pehle se banaye gaye bade, sab kuch karne wale module aksar utne hi ulajhe hote hain jitne unhe hatana mushkil.

## Module ko Badalna, Safely

Module badalte waqt do khatre. Ek: module ke andar ka koi resource rename kar do, to har campus ka plan "hatao aur banao" dikhata hai. Iska hal wahi moved block jo Session 27 mein dekha, bas ab module ke andar. Do: ek naya version ek saath teen campus par gira, aur teeno tut gaye. Isliye upgrade ka kram: pehle dev, plan padho, apply karo, dekho. Phir staging. Phir prod. Har campus apna version pin karta hai, aur module ka naya version ek pull request ke saath aata hai jisme do line ka changelog ho: kya badla, aur kya moved ho sakta hai. Isse "standard design" ek aisi cheez ban jaati hai jise sab par bharosa hota hai.

## Lab: Network ka Standard Design

Lab. Session 27 ke public wing ka code modules/network mein le jao. Inputs: name, cidr, public_subnet_count, aur outputs: vpc_id, public_subnet_ids. Subnet ke CIDR cidrsubnet se nikalo. Ek validation lagao jo galat CIDR par rok de. Root mein module ko do baar bulao: ek dev aur ek staging, alag CIDR ke saath, jo overlap nahi karte, Session 14 ka niyam. terraform init modules ko load karta hai, phir plan. Dekho ki ek hi code se do alag campus ban rahe hain. Phir cidr mein galat value do aur dekho ki validation ruk jaata hai. NAT gateway abhi mat jodo, kyunki wo hourly paisa leta hai. Aakhir mein destroy.

## Recap aur Bridge

Recap: modules. Ab ek bada sawaal: dev ka dhakka prod par kaise na pade, aur poora 3-tier campus ek plan se.

---

# EPISODE 3: Alag Campus, Ek Master Plan

## Dev ka Dhakka Prod Par

Ek engineer ne socha wo dev mein hai, terraform destroy chalaya, aur wo production tha. Aise haadse isliye hote hain ki environments ek doosre se alag nahi hote. Achhi setup mein har environment ka apna register, apne variables, aur aksar apna alag AWS account hota hai. Aur terminal ka prompt environment ka naam dikhaye, jaise Session 23 mein kubectl ke context ke saath tay hua tha.

## Environments ke Tareeke

Teen tareeke. Ek: alag folders, envs/dev aur envs/prod, har ek ka apna backend key aur terraform.tfvars, aur sab wahi modules bulate hain. Do: workspaces, ek hi code se kai registers, par galat workspace mein kaam karna bahut aasaan hai, isliye bade campus ke liye mat chuno. Teen: alag AWS accounts, jahan har account ka apna role hota hai, aur provider assume_role se uske andar jaata hai. Account sabse surakshit hai, kyunki ek ki galti doosre ko chhoo nahi sakti, aur bill bhi alag. Shuruaat ke liye alag folders aur tfvars saaf raasta hai. Aur provider mein default_tags laga do, taaki har resource par Env aur Owner apne aap aaye.

## Teen Parton ka Campus

Ab AWS ke saare sessions ek jagah. 3-tier campus. Web tier: ALB, yaani marshal, public wings mein, do towers mein. App tier: Auto Scaling Group private wings mein, Session 10 ke launch template ke saath, aur bahar jaane ke liye dispatch desk. Database tier: RDS, Session 13 ka records office, private database wings mein. Door guard ki zanjeer, Session 11 ki tarah: internet se marshal, marshal se app, app se database, aur kisi par seedha nahi. Chaar modules: network, alb, compute, database. Is design mein ek tower gira to doosra sambhal leta hai, aur database kabhi seedha internet se nahi dikhta.

## Database ke Password aur Kharcha

Database module mein do cheezein dhyaan se. Password: manage_master_user_password = true, taaki password Secrets Manager mein ban jaaye aur Terraform ke state mein na aaye, jaise Session 13 aur Session 27 mein tay hua. Aur taale: deletion_protection = true aur lifecycle { prevent_destroy = true }, taaki ek galat plan records office ko na hata de. Kharcha: dev mein single-AZ aur chhota instance, production mein multi_az = true aur bada, aur ye difference ek variable se tay ho. NAT gateway ghante ka kharcha hai, aur har tower mein ek lagane se high availability milti hai par bill bhi doguna. Dev mein ek, production mein har tower mein ek. Ye faisle tfvars mein dikhne chahiye, taaki review mein sab dekh saken.

## Cluster bhi Code, aur Doosre Landlord bhi

Master plan sirf buildings ke liye nahi. Session 24 ka Kubernetes cluster bhi code ban sakta hai: AWS ka EKS, GCP ka GKE, Azure ka AKS, har ek ek module mein. Aur cluster ke upar ke kaam, jaise Session 26 ka monitoring stack, Helm provider se. Dhyaan: cluster banana aur cluster ke andar chizein lagana alag registers mein rakho, kyunki jab cluster hi gir jaaye, to uske andar ke resources ke plan bhi toot jaate hain. Aur landlord badalne par plan ki bhasha wahi rehti hai, par resources ke naam badal jaate hain: aws_vpc ki jagah google_compute_network. Isliye multi-cloud ka matlab "ek code sab jagah" nahi, "ek tareeka sab jagah" hai. Agle Azure ke session mein ye saaf dikhega.

## Lab: Dev Campus ka Plan

Lab. envs/dev folder mein chaar modules jodo: network, alb, compute aur database. Variables terraform.tfvars se do: chhote sizes, multi_az = false, ek NAT. Backend key dev/terraform.tfstate. Sabse pehle sirf terraform plan chalao, aur padho: kitne resources banenge, aur kaun se. Teen sawaal wahi Session 27 ke: kya kuch hatega, kuch anjaana badlega, ginti andaaze se milti hai? Aaj plan ko samajhna hi asli maksad hai. Agar poora apply karna chaho, to pehle Session 15 ka budget alert lagao, sabse chhote sizes lo, aur kaam ke turant baad terraform destroy, kyunki NAT gateway, ALB aur RDS teeno ghante ke hisaab se chalte hain. Destroy ke baad console mein check karo ki kuch bacha nahi.

## Recap aur Bridge

Recap: environments aur 3-tier campus. Ab master plan ko conveyor mein lagate hain: scan, cost aur safe apply.

---

# EPISODE 4: Master Plan ki Conveyor

## Apply Apne Laptop Se?

Production mein apply apne laptop se, admin keys ke saath? Ye risky hai, aur baad mein trace karna mushkil. Behtar: master plan ki bhi apni conveyor. Pull request par plan chalta hai aur uska natija comment mein dikhta hai. Chief architect review karta hai. Merge ke baad, approval ke saath, apply. Session 17 se 20 ki conveyor ke saare vichar yahan wapas aate hain: review, required check, secret ka sahi upyog.

## Pipeline ke Stations

Pull request par ye stations. terraform fmt -check. terraform validate. Ek linter, jaise tflint. Security scan, jaise Checkov ya Trivy, jo khuli hui security group ya bina encryption wale disk pakadte hain. Cost estimate, jaise Infracost, jo plan ka mahine ka kharcha batata hai. Aur terraform plan -out=tfplan, jiska saransh pull request mein dikhta hai. Merge ke baad apply tfplan, ek environment approval ke saath, aur wahi saved plan, taaki jo review hua wahi lage. Aur ek chhoti baat: plan dikhane wala role register aur resources padh sake, par kuch badal na sake. Apply wala role alag, aur sirf wahi ijaazat jo master plan ko chahiye.

## Pipeline ko Chaabi Nahi, Duty Badge

Pipeline ko AWS keys kyun dein? Session 20 ka OIDC yahan seedha kaam aata hai: workflow vault se ek identity token maangta hai, AWS role ki trust policy dekhta hai, aur chhoti umar ke credentials deta hai. Do role rakho. tf-plan: pull request se, sirf padhne ki ijaazat. tf-apply: sirf main branch se, ek environment approval ke baad, aur trust policy ki sub shart mein repo aur branch likha ho. Is tarah ek khula hua pull request, chahe fork se ho, apply wala role kabhi nahi le sakta. Aur Terraform ka provider "aws" bas region aur assume_role jaisi cheezein jaanta hai, koi key nahi.

## Drift aur Guardrails

Apply ke baad bhi kaam khatam nahi. Roz raat ek scheduled workflow terraform plan -detailed-exitcode chalaye. Exit code 0 matlab koi badlaav nahi. 1 matlab plan mein hi error. 2 matlab drift mila, aur tab Session 15 ke SNS ya chat mein alert, ki kisi ne console mein kuch badla. Phir tay karo: code mein likho ya mita do. Policy as code, jaise OPA ya Sentinel ya Checkov ke custom rules, aise niyam lagu karte hain: "koi bhi bucket public nahi", "har resource par Owner aur Env tag". Aur register ke bucket aur apply role ko sabse kam logon ke haath mein rakho. Ye sab milkar infrastructure ko wahi anushasan dete hain jo Session 17 se humne code ko diya.

## Wapas Kaise Jaayein

Application ka rollback aasaan tha: kubectl rollout undo. Master plan ka rollback kya hai? Pull request ko revert karo, aur conveyor purani halat ka plan banakar apply kar degi. Par ye har cheez ke liye nahi chalta. Jo cheez hat chuki ho, jaise ek database ya ek bucket ka data, wo revert se wapas nahi aati, kyunki Terraform sirf naya khaali bana dega. Isliye teen aadatein. Ek: critical resources par prevent_destroy. Do: unke liye backup aur snapshot, jaise Session 10 aur 13 mein, apply se pehle. Teen: bade badlaav chhote tukdon mein, kyunki ek chhota plan padhna aur wapas lena dono aasaan hain. Aur jab plan "replace" dikhaye, to ek aur baar poocho: kya is cheez ka data hai?

## Lab: Master Plan ki CI

Lab. Vault mein ek workflow jo pull request par ye chalaye:

Action versions ko pin karo: @PINNED-VERSION ki jagah tay version ya SHA likho, jaise Session 20 mein. Ab apne master plan mein SSH ko 0.0.0.0/0 par khol kar push karo, aur dekho ki scan fail hoti hai. Rule ko apne IP tak seemit karo aur pass karao. Is check ko required status check banao, jaise Session 19 ke branch protection mein. Agar AWS hai, to OIDC ke role ke saath ek plan step jodo.

## Recap aur Bridge

Recap: Terraform ka poora production workflow. Ab campus ban gaya, par har building ke andar abhi khaali kamre hain: users, packages, services, settings. Un sabko ek jaisa sajane ke liye ek crew chahiye, jo har building mein jaakar checklist ke hisaab se kaam kare, aur dobara chalane par kuch na bigaade. Agla session: Ansible.

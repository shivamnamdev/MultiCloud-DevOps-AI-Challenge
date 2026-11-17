# ✍️ 02: SCRIPT — SESSION-30: Azure and Azure DevOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S30`
- **Focus:** Multi-cloud mapping (AWS, Azure, GCP) and when multi-cloud is worth its cost; Azure hierarchy (tenant, management group, subscription, resource group, resource), regions and zones, naming and tags, budgets; Microsoft Entra ID, Azure RBAC (role, scope, principal), managed identity, service principal; core services (VM, VNet, NSG, Blob, App Service, Azure SQL and PostgreSQL, Key Vault, Azure Monitor); AKS and ACR; Terraform with the `azurerm` provider; Azure DevOps (Boards, Repos with branch policies, Pipelines with YAML stages and environments, Artifacts, service connections, variable groups)
- **Builds on:** Session 03 (cloud models), Session 09 (IAM, roles, least privilege), Session 10 to 14 (instance, load balancer, S3, RDS, campus), Session 15 (budget alerts), Session 17 to 20 (Jenkins, Actions), Session 22 (depot, truck design), Session 24 (GKE, `kubectl`), Session 27 and 28 (contractor, master plan, state)
- **Story position:** Zoom levels 2 and 3. Atithi ek doosre landlord, Azure, ke saath sign karta hai. Wahi buildings, wahi wings, wahi guards, bas naam alag. Is landlord ke paas ek ready-made head office bhi hai: planning wall, vault, conveyor aur parts store.
- **Story words used:** landlord (cloud provider), second landlord (Azure), campus (VPC or VNet), wing (subnet), door guard (security group or NSG), duty badge (role, managed identity), key cabinet (Key Vault, credentials), warehouse (Blob or S3), records office (managed database), depot (container registry), operations command (Kubernetes), planning wall (Boards), vault (Repos), conveyor (Pipelines), parts store (Artifacts), master plan (Terraform), contractor (provider), foreman (Jenkins), guest (end user), staff (admin)
- **Lab project:** Atithi's translation table filled from the real Azure portal, one resource group with a storage warehouse created and deleted from the CLI, `rooms-service` truck design from Session 22 pushed to ACR and run on a small AKS cluster, and a two-stage Azure Pipeline with an approval on the `prod` environment.
- **Cost rule (Azure):** AKS nodes, load balancers and public IPs are billed while they exist. Create everything in one resource group per lab, set a budget alert first, and finish with `az group delete`. Check the portal after deletion. Free account credits and free tiers change often; read the current offer before starting.
- **Episodes:**
  - Episode 1: Doosra Landlord: AWS, Azure, GCP ka Naksha
  - Episode 2: Azure ka Naksha: Subscription, Resource Group aur Duty Badge
  - Episode 3: Buildings aur Operations Command: Core Services, ACR aur AKS
  - Episode 4: Ready-made Head Office: Azure DevOps

---

# 📺 EPISODE 1: Doosra Landlord

### [00:00 – 01:50] Scene 1: Ek Landlord Seekha, Naukri Doosre Ke Saath Mili
**[VISUAL: A learner who knows AWS gets a job at a company on Azure. A translation card overlays AWS names with Azure names. A confident face replaces the worried one.]**

**(Voiceover):**
Maan lo Atithi Hotels ne ek bada hotel group khareeda, aur uski saari buildings Azure par hain. Aapne Session 10 se 14 mein AWS seekha. Kya aap bekaar ho gaye? Bilkul nahi. Landlord badla hai, par building, wing, door guard aur records office wahi. Naam aur console alag. Is episode mein hum ek translation table banate hain, jo har naye landlord par kaam aati hai.

### [01:50 – 05:05] Scene 2: Translation Table
**[VISUAL: A table with three columns: AWS, Azure, GCP. Rows: EC2, Azure Virtual Machines, Compute Engine. S3, Blob Storage, Cloud Storage. VPC, VNet, VPC. Security group, NSG, firewall rules. IAM role, managed identity, service account. RDS, Azure SQL or Azure Database for PostgreSQL, Cloud SQL. EKS, AKS, GKE. Lambda, Azure Functions, Cloud Functions. ECR, ACR, Artifact Registry. CloudWatch, Azure Monitor, Cloud Monitoring. Secrets Manager, Key Vault, Secret Manager. CloudFormation, ARM and Bicep, Deployment Manager.]**

**(Voiceover):**
Compute: AWS mein EC2, Azure mein Virtual Machines, GCP mein Compute Engine. Warehouse, yaani object storage: S3, Blob Storage, Cloud Storage. Campus: VPC, Azure mein VNet. Door guard: security group, Azure mein NSG, yaani Network Security Group. Records office: RDS, Azure mein Azure SQL aur Azure Database for PostgreSQL. Operations command: EKS, AKS, GKE. Freelancer: Lambda, Azure Functions. Depot: ECR, ACR. Key cabinet: Secrets Manager, Azure mein Key Vault. Meters aur CCTV: CloudWatch, Azure Monitor. Naam alag, idea ek. Par ek chetavani: mapping lagbhag hoti hai. Har service ke chhote farq hote hain, jaise limits, pricing, aur kaun si cheez default mein private hai. Isliye table ke saath ek column "farq" ka bhi rakho.

### [05:05 – 07:40] Scene 3: Teen Jagah Jahan Azure Alag Lagta Hai
**[VISUAL: Three callouts. 1. Azure groups resources in resource groups; AWS has none. 2. Azure identity lives in Microsoft Entra ID, separate from the subscription; AWS IAM is inside the account. 3. A VM in Azure comes with separate objects: NIC, disk, public IP, NSG; in AWS most of these hide behind one launch.]**

**(Voiceover):**
Teen jagah jahan AWS wale ko Azure alag lagega. Pehla: Azure mein resource group hota hai, jahan ek project ki saari cheezein ek dabbe mein. AWS mein aisa dabba nahi, tags se kaam chalta hai. Doosra: pehchaan, yaani staff aur unke badges, Azure mein Microsoft Entra ID mein rehti hai, jo company ki apni directory hai, aur subscription alag cheez hai. Teesra: Azure mein ek virtual machine ke saath network card, disk, public IP aur NSG alag objects ki tarah dikhte hain. In teen cheezon ko samajh liya to baaki aasaan.

### [07:40 – 11:00] Scene 4: Multi-Cloud kyun aur Kab
**[VISUAL: A balanced scale. Left: avoid lock-in, regulations, a special service, company acquisitions, resilience. Right: complexity, skills, egress fees, lowest common denominator, two bills and two security models. A note: "most companies are multi-cloud by accident".]**

**(Voiceover):**
Companies multi-cloud kyun chunti hain? Vendor lock-in se bachne ke liye, kisi niyam ki wajah se, kisi khaas service ke liye, ya kisi doosri company ko khareedne ki wajah se, jo doosre landlord par thi. Keemat bhi hai: complexity, do cloud ki skills, data bahar bhejne ka egress charge, aur har landlord ki sabse achhi cheezein chhodkar common cheezein use karna. Sach ye hai ki aksar companies multi-cloud chahkar nahi, halaat se ban jaati hain. Isi liye wo tools kaam aate hain jo har landlord par chalte hain: Terraform, Docker, Kubernetes, Ansible, Prometheus. Ye hum seekh chuke hain. Ek seedha rule: do cloud tab rakho jab uski wajah likhi ho, sirf "kya pata kabhi zaroorat pade" wajah nahi.

### [11:00 – 13:40] Scene 5: Lab: Apni Translation Table Banao
**[VISUAL: A spreadsheet with twelve rows for Atithi: website hosting, API, database, cache, queue, secrets, container registry, load balancer, DNS, monitoring, CI/CD, infrastructure as code. Columns: AWS, Azure, GCP, "farq".]**

**(Voiceover):**
Lab: ek table banao: Atithi ki website ke har hisse ke liye AWS, Azure aur GCP ke naam. Website hosting, API, database, cache, queue, secrets, container registry, load balancer, DNS, monitoring, CI/CD, aur infrastructure as code. Har row mein ek line "farq" likho. Jo naam aapko nahi pata, use docs mein dhoondho, aur guess mat likho. Ye table interview mein bhi kaam aati hai, kyunki "AWS mein ye kaise hota hai, Azure mein kaise?" ek pasandida sawaal hai. Aage ke episodes mein hum is table ko Azure ke asli portal se bharte jaayenge.

### [13:40 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "same ideas, new names · table with a farq column · resource group, Entra ID, separate objects · multi-cloud has real costs · portable tools".]**

**(Voiceover):**
Recap: translation table aur teen farq. Ab Azure ke andar ka naksha: tenant se resource group tak, aur duty badge kaise milte hain.

---

# 📺 EPISODE 2: Azure ka Naksha

### [00:00 – 01:50] Scene 1: Cheezein Kahan Rakhi Jaati Hain
**[VISUAL: A hierarchy: Tenant (Entra ID directory) → Management groups → Subscriptions → Resource groups → Resources. Cost and policy boundaries shown beside each level. The AWS account drawn as roughly one subscription.]**

**(Voiceover):**
Atithi ne Azure par kaam shuru kiya. Pehla sawaal: cheezein kahan rakhi jaayen? Sabse upar tenant hai, yaani company ki pehchaan wali directory. Uske neeche management groups, jinse kai subscriptions par ek saath niyam lagte hain. Subscription billing aur access ki sabse bada daayra hai, aur AWS ke account jaisa samjho. Subscription ke andar resource groups: ek project ki cheezein ek dabbe mein. Aur dabbe ke andar asli resources. Is naksha se hi pata chalta hai ki kharcha kahan dikhega aur kaun kya chhoo sakta hai.

### [01:50 – 04:20] Scene 2: Resource Group, Region, Naam aur Tags
**[VISUAL: A group `rg-atithi-dev-cin` containing a VNet, a VM, its disk, its NIC, a storage account. A tag list: `env=dev`, `owner=asha`, `cost-centre=web`. A budget alert at the subscription. A red delete button on the group.]**

**(Voiceover):**
Resource group ek dabba hai, jiske andar ek project ki saari cheezein. Group delete karo to andar ka sab delete, isliye lab ke baad safai aasaan: ek command. Har resource ek region mein hota hai, aur group ka bhi ek location hota hai, jahan uska metadata rehta hai. Naming convention banao, jaise `rg-atithi-dev-cin`, jisme project, environment aur region ho. Tags lagao: `env`, `owner`, `cost-centre`, taaki bill mein dikhe kaun kitna kharch kar raha hai. Aur lab shuru karne se pehle subscription par budget alert lagao, jaise Session 15 mein AWS par lagaya tha. Ek niyam aur: kuch resource ke naam poori duniya mein unique hote hain, jaise storage account, jisme sirf chhote akshar aur ank aate hain.

### [04:20 – 06:30] Scene 3: Pehchaan: Entra ID aur Azure RBAC
**[VISUAL: Left: Microsoft Entra ID with users, groups, service principals, managed identities. Right: Azure RBAC as three boxes: Role (Reader, Contributor, Owner) + Scope (subscription, resource group, resource) + Principal (user, group, identity) = Role assignment.]**

**(Voiceover):**
Staff kaun hai, ye Microsoft Entra ID tay karta hai, jo pehle Azure AD kehlata tha: users, groups, aur applications ke liye service principals. Kaun kya kar sakta hai, ye Azure RBAC tay karta hai. Ek role assignment mein teen cheezein hoti hain: role, jaise Reader, Contributor ya Owner; scope, jaise ek resource group; aur principal, yaani kisko. Jaise: asha ko `rg-atithi-dev-cin` par Contributor. Scope jitna chhota, utna surakshit. Contributor resource bana sakta hai par kisi ko role de nahi sakta, Owner de sakta hai, isliye Owner kam logon ko. Wahi least privilege jo Session 09 mein tha.

### [06:30 – 09:05] Scene 4: Managed Identity: Building ka Apna Duty Badge
**[VISUAL: A VM and an AKS node with a small badge. The badge asks Entra ID for a token; Key Vault and Blob Storage accept the token. A comparison: "service principal secret in a file" crossed out; "managed identity, no secret" ticked.]**

**(Voiceover):**
AWS mein building ko role milta tha, jise instance profile se pehnaya jaata tha. Azure mein iska naam managed identity hai. VM ya app ko ek identity milti hai, aur wo bina password ke Entra ID se token leti hai. Fir us identity ko Key Vault ya storage par ek role assignment mil jaata hai. Service principal ke saath secret ya certificate rakhna padta hai, aur wo kisi file mein ruk jaata hai. Managed identity mein koi secret hai hi nahi. Sabse achha rasta: jahan bhi ho sake, managed identity. Aur jahan pipeline ko Azure se baat karni ho, wahan workload identity federation, jo OIDC ka wahi idea hai jo humne Session 20 aur 28 mein dekha tha.

### [09:05 – 11:15] Scene 5: Azure par Terraform: Naya Contractor
**[VISUAL: A Terraform file with `provider "azurerm" { features {} }`, a `azurerm_resource_group`, an `azurerm_storage_account`. The register is stored in a Blob container with a lock. A side note: "the same plan, init, apply workflow".]**

**(Voiceover):**
Session 27 mein humne kaha tha ki har landlord ke liye alag contractor, yaani provider, hota hai. Azure ka contractor `azurerm` hai. Plan, apply, destroy, wahi sab. Naye resource ka naam alag: `azurerm_resource_group`, `azurerm_storage_account`. Register, yaani state, yahan Azure Blob Storage mein rakhte hain, aur wahan bhi lock milta hai. Provider block mein `features {}` chahiye. Azure ka apna tool Bicep bhi hai, jo sirf Azure ke liye hai. Par jo team do landlord ke saath kaam karti hai, wo aksar ek hi tool, Terraform, rakhti hai. Version aur authentication ke exact tareeke ke liye provider ke docs dekho.

### [11:15 – 13:50] Scene 6: Guardrails: Policy, Lock aur Cost
**[VISUAL: Three guard icons on a resource group. Azure Policy: "storage accounts must block public access; resources must have an `owner` tag". A delete lock: a padlock on the production group. Cost Management: a budget line with an alert at eighty percent.]**

**(Voiceover):**
Azure mein teen guardrails Atithi ke kaam ke hain. Pehla Azure Policy: ek niyam jo poore subscription par lagta hai, jaise "har resource par `owner` tag ho" ya "storage account public na ho". Niyam todne wala resource ban hi nahi paata, ya report mein laal dikhta hai. Ye wahi policy as code ka idea hai jo Session 28 mein tha. Doosra resource lock: production ke group par delete lock lagao, to galti se bhi group delete nahi hota, jab tak koi pehle lock na hataye. Teesra Cost Management: budget aur alert, aur dekho ki kharcha kis tag par ja raha hai. Ye teen ek baar lagao, aur phir naye logon ko Contributor dena bhi kam darawna lagta hai.

### [13:50 – 16:25] Scene 7: Lab: Azure CLI se Pehla Resource
**[VISUAL: `az login`, `az account show`, `az group create --name rg-demo --location centralindia`, `az storage account create ...`, `az group list -o table`, `az role assignment list --assignee ... -o table`, `az group delete --name rg-demo --yes --no-wait`.]**

**(Voiceover):**
Lab: Azure free account ya sandbox lo, aur Azure CLI install karo. Pehle `az login`, phir `az account show`, taaki dekho ki kaun sa subscription chal raha hai. Phir:
```bash
az group create --name rg-demo --location centralindia
az storage account create --name YOUR_UNIQUE_NAME --resource-group rg-demo \
  --sku Standard_LRS --kind StorageV2 --allow-blob-public-access false
az group list -o table
az role assignment list --assignee YOUR_EMAIL -o table
```
Storage account ka naam chhote akshar aur ank mein, poori duniya mein unique. `--allow-blob-public-access false` wahi Block Public Access ka idea hai jo Session 12 mein tha. Role assignments dekho. Aakhir mein `az group delete --name rg-demo --yes --no-wait`, aur portal mein confirm karo ki sab hat gaya. Ek group, ek delete.

### [16:25 – 16:55] Scene 8: Recap aur Bridge
**[VISUAL: A card: "tenant → subscription → resource group · naming + tags + budget · RBAC = role + scope + principal · managed identity, no secret · azurerm provider · delete the group".]**

**(Voiceover):**
Recap: Azure ka naksha, RBAC aur managed identity. Ab buildings aur operations command: core services, ACR aur AKS.

---

# 📺 EPISODE 3: Buildings aur Operations Command

### [00:00 – 01:00] Scene 1: Ek Website, Chaar Zaroorat
**[VISUAL: An Atithi web app on Azure: a VNet with a public wing and a private wing, App Service or VM in the public wing, a managed PostgreSQL in the private wing, Blob Storage for photos, Key Vault for secrets, Azure Monitor watching.]**

**(Voiceover):**
Atithi ki booking website ko Azure par chalane ke liye wahi chaar cheezein chahiye jo AWS par thi: building, campus, records office aur warehouse. Dekhte hain ki Azure inhe kaise deta hai, aur kab kaun sa raasta chunna chahiye.

### [01:00 – 04:35] Scene 2: Compute, Network, Storage aur Database
**[VISUAL: Four columns. Compute: VM, VM Scale Sets, App Service, Container Apps, AKS, Functions. Network: VNet, subnet, NSG, Load Balancer, Application Gateway, private endpoint. Storage: Blob, Files, Managed Disks. Database: Azure SQL, Azure Database for PostgreSQL or MySQL, Cosmos DB.]**

**(Voiceover):**
Compute mein seedhi building: Virtual Machine, aur uski Auto Scaling ka naam VM Scale Sets. App Service ek managed web hosting hai: bas code do, building landlord sambhalta hai. Container Apps aur AKS trucks ke liye. Functions freelancer ke liye. Campus mein VNet aur subnets, aur door guard NSG, jo subnet par ya building ke network card par lagta hai. Load Balancer layer 4 par kaam karta hai, Application Gateway layer 7 par, yaani marshal jo raasta dekh kar bhejta hai. Private endpoint se kisi managed service tak raasta campus ke andar se hi ata hai. Warehouse mein Blob, shared files ke liye Files, aur building ki disk ke liye Managed Disks. Records office mein Azure SQL, Azure Database for PostgreSQL, aur loose forms ke liye Cosmos DB. Seedha rule: jitna managed, utna kam kaam, aur utna kam control.

### [04:35 – 06:50] Scene 3: Key Vault aur Azure Monitor
**[VISUAL: A Key Vault with secrets and a role assignment for an app's managed identity. An Azure Monitor chart with a metric alert, a log query, and an action group that sends email and a phone message.]**

**(Voiceover):**
Key cabinet Azure mein Key Vault hai: secrets, keys aur certificates. App ki managed identity ko Key Vault par secrets padhne ka role do, aur password kisi file ya environment mein likhna nahi padega. Meters aur CCTV Azure Monitor mein: metrics, logs ke liye Log Analytics, aur alerts, jinhe action group se email ya phone par bheja jaata hai. Ye Session 15 ke CloudWatch aur SNS ka Azure roop hai, aur jo kuch Session 26 mein Prometheus aur Grafana se dekha, wo kisi bhi landlord par waise hi chalega.

### [06:50 – 10:15] Scene 4: ACR aur AKS
**[VISUAL: An AKS cluster. The control plane is labelled "Azure runs this". Node pools run on VM scale sets. ACR holds the `rooms-service` truck design. An arrow shows AKS pulling from ACR with permission from `az aks update --attach-acr`. `az aks get-credentials` adds a context; the same `kubectl` commands from Session 24.]**

**(Voiceover):**
AKS Azure ka managed operations command hai, GKE jaisa. Reception, ledger aur allocation officer, yaani control plane, Azure sambhalta hai. Aap node pools chalate ho, jo VM scale sets par chalte hain. Truck designs ACR, yaani Azure Container Registry, mein rakhte hain: wahi depot jo Session 22 mein tha. AKS ko ACR se pull karne ki permission `az aks update --attach-acr` se, ya cluster banate waqt `--attach-acr` flag se, mil jaati hai. `az aks get-credentials` kubeconfig mein naya context jod deta hai. Uske baad sab kuch wahi `kubectl get`, `apply`, `describe`, `logs` jo GKE par kiya tha. Yahi multi-cloud ka asli fayda hai: ek baar seekha, kai landlord par chala. Ek chetavani: control plane ka paisa tier par nirbhar hai, aur node, load balancer, public IP sab ghante ke hisaab se lagte hain.

### [10:15 – 13:50] Scene 5: Lab: ACR aur AKS par rooms-service
**[VISUAL: `az group create`, `az acr create`, `az acr build` or `docker push`, `az aks create --attach-acr`, `az aks get-credentials`, `kubectl apply`, `kubectl get svc -w`, `curl http://EXTERNAL_IP/health`, then `az group delete`.]**

**(Voiceover):**
Lab: pehle budget alert. Phir:
```bash
az group create --name rg-aks --location centralindia
az acr create --resource-group rg-aks --name YOUR_ACR_NAME --sku Basic
az acr build --registry YOUR_ACR_NAME --image rooms-service:1.0 .
az aks create --resource-group rg-aks --name aks-atithi --node-count 1 \
  --attach-acr YOUR_ACR_NAME --generate-ssh-keys
az aks get-credentials --resource-group rg-aks --name aks-atithi
```
Cluster banne mein kuch minute lagte hain. `kubectl get nodes` se dekho ki ek node Ready hai. Session 24 ka Deployment aur LoadBalancer Service YAML lo, image ka naam ACR ke address se badlo, `kubectl apply`, aur `kubectl get svc -w` se EXTERNAL-IP aane do. Browser ya `curl` se `/health`. Wahi YAML, naya landlord. Aakhir mein `az group delete --name rg-aks --yes --no-wait`, kyunki node aur load balancer paisa lete hain. Flags aur size ke naam badalte rehte hain, isliye `az aks create --help` se apna version dekh lo.

### [13:50 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "VM · Scale Sets · App Service · AKS · NSG · Blob · managed databases · Key Vault · Azure Monitor · ACR + AKS = same kubectl".]**

**(Voiceover):**
Recap: Azure ke core services, aur AKS par wahi Kubernetes. Ab Azure ka ready-made head office: Azure DevOps.

---

# 📺 EPISODE 4: Ready-made Head Office

### [00:00 – 01:40] Scene 1: Planning Wall se Parts Store Tak
**[VISUAL: Five tiles: Boards, Repos, Pipelines, Test Plans, Artifacts. A work item card travels: Board card → branch → pull request → pipeline → artifact → deployment. Beside it, the Atithi pieces from earlier sessions: vault, foreman, conveyor.]**

**(Voiceover):**
Head office mein hum pehle se vault (Git), foreman (Jenkins) aur conveyor (Actions) dekh chuke hain. Azure ek poora ready-made head office deta hai, jisme sab ek jagah: Boards, yaani planning wall, jahan kaam track hota hai. Repos, yaani vault, jahan Git ka code rehta hai. Pipelines, yaani conveyor. Test Plans, yaani inspection. Aur Artifacts, yaani parts store, jahan packages rakhe jaate hain. Ek kaam ka card shuru se deploy tak traceable rehta hai.

### [01:40 – 04:10] Scene 2: Boards, Repos aur Branch Policies
**[VISUAL: A Kanban board with columns To Do, Doing, Done. A work item with an id. A repo with a branch policy on `main`: one reviewer, a linked work item, and a successful build required. A commit message "Fix room count. Fixes AB#123".]**

**(Voiceover):**
Boards mein epics, user stories aur tasks, Kanban ya Scrum ke saath. Repos mein Git ka vault, aur branch policies, jo wahi master par taala hai jo Session 16B mein GitHub par tha: `main` par seedha push band, pull request mein kam se kam ek review, aur build successful hona zaroori. Commit ya PR mein `AB#123` likho to wo work item se judta hai. Ye traceability audit mein kaam aati hai: kaun sa feature, kis code se, kis deploy se. Aur agar aapka code GitHub par hai, to Azure Pipelines GitHub ke repo ke saath bhi chalta hai. Azure ka head office zaroori nahi ki vault bhi Azure mein ho.

### [04:10 – 06:25] Scene 3: YAML Pipeline: Stages, Jobs, Steps
**[VISUAL: An `azure-pipelines.yml` with `trigger`, `pool`, `stages`, `jobs`, `steps`. A mapping table to Jenkins and Actions: stage = stage, job = agent block, step = `sh`, agent pool = workbench, service connection = key cabinet entry.]**

**(Voiceover):**
Azure Pipelines mein conveyor YAML mein likhi jaati hai: `trigger` kab chalegi, `pool` kaun si machine, `stages`, har stage ke andar `jobs`, aur jobs ke andar `steps`. Jenkins se mila lo to: stage wahi, job ek workbench par chalne wala blok, step wahi `sh`. Azure se baat karne ke liye service connection, jise key cabinet ka ek entry samjho. Behtar hai ki wo workload identity federation se bane, yaani koi lambi umar wala secret nahi. Concept bilkul wahi jo Jenkins aur GitHub Actions mein tha. Sirf syntax alag hai, aur isliye ek baar seekha to teeno aate hain.

### [06:25 – 08:55] Scene 4: Environments, Approvals aur Secrets
**[VISUAL: A deployment job targeting an environment `prod`. The environment has an approval check from the duty manager and a branch control. A variable group linked to Key Vault. A flow: Build stage → Deploy dev → approval → Deploy prod.]**

**(Voiceover):**
Deploy ke liye environments. Environment par approvals aur checks lagte hain: `prod` ke liye ek duty manager ki manjoori, ya sirf `main` branch se deploy. Ye wahi `input` step hai jo Jenkins mein tha, par yahan ye platform ka hissa hai aur workbench ko rokta nahi. Secrets ke liye variable groups, jo Key Vault se jode ja sakte hain, to password pipeline ke YAML ya Git mein nahi aata. Aur pipeline logs mein secrets chhupe hote hain, par ye surakshit baad mein nahi, isliye unhe print mat karo. Artifacts mein build ka output ya package rakho, jise baad ke stages utha sakte hain, jaise Session 18 mein archive kiya tha.

### [08:55 – 12:25] Scene 5: Lab: Do Stage ki Conveyor
**[VISUAL: A free Azure DevOps organization with a project. A Python repo imported. `azure-pipelines.yml` with a Build stage (install, test, publish artifact) and a Deploy stage with `environment: dev`. The run shows two green stages. An approval check on `prod` makes the next stage wait.]**

**(Voiceover):**
Lab: free Azure DevOps organization aur ek project banao. Apna Python repo import karo, ya Atithi ka `rooms-service`. Phir `azure-pipelines.yml`:
```yaml
trigger: [ main ]
pool: { vmImage: ubuntu-latest }
stages:
  - stage: Build
    jobs:
      - job: build
        steps:
          - script: |
              pip install -r requirements.txt
              pytest -q
            displayName: Test
          - publish: $(System.DefaultWorkingDirectory)
            artifact: app
  - stage: DeployDev
    dependsOn: Build
    jobs:
      - deployment: dev
        environment: dev
        strategy:
          runOnce:
            deploy:
              steps:
                - script: echo "Deploying to dev"
```
Pipeline banao aur chalao. Phir ek `prod` environment banao, uspar approval check lagao, aur ek teesra stage jodo. Dekho ki wo manjoori ka intezaar karta hai. Free tier mein parallel jobs ki seema ho sakti hai, aur nayi organization ko shuru mein request bhejni pad sakti hai, isliye settings dekh lo. Aakhir mein pipeline ko ACR par image push karne wale step se jodne ki koshish karo, jo isi session ke Episode 3 se mil jaata hai.

### [12:25 – 14:10] Scene 6: Kab Azure DevOps, Kab Baaki
**[VISUAL: A decision table. Choose Azure DevOps: the company is on Microsoft tools, wants planning plus code plus pipelines in one place, or needs approvals and audit. Choose GitHub + Actions: open source, community, code already there. Choose Jenkins: special plugins, on-premise. A line: "same concepts".]**

**(Voiceover):**
Kab kaun sa head office? Agar company Microsoft ke tools par hai, aur planning, code aur pipeline ek hi jagah chahiye, to Azure DevOps theek hai. Agar code GitHub par hai aur community bada hai, to GitHub aur Actions. Agar bahut khaas plugins ya on-premise chahiye, to Jenkins. Teeno mein wahi concepts hain: vault, bell, conveyor, stage, approval, key cabinet. Isliye naya tool aane par ghabrao mat. Ye table interview ke liye bhi kaam aati hai.

### [14:10 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "Boards · Repos + branch policy · Pipelines YAML · environments + approvals · variable group + Key Vault · Artifacts · same concepts as Jenkins and Actions".]**

**(Voiceover):**
Recap: Azure ki translation, uska naksha, AKS, aur Azure DevOps. Atithi ke paas ab teen landlord ka gyaan hai, aur har tool ka ek ghar. Ab sab kuch ek saath jodte hain: pehla grand opening. Ek revision vault mein jaata hai, ghanti bajti hai, foreman fabricate karta hai, ek truck nikalta hai aur ek guest ko serve karta hai. Agla session: capstone.

---

# 📎 Student handout: Session 30 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Translation | EC2 = VM; S3 = Blob; VPC = VNet; SG = NSG; EKS = AKS; ECR = ACR; Secrets Manager = Key Vault; CloudWatch = Azure Monitor |
| Farq column | Mapping lagbhag hai: limits, pricing, defaults check karo |
| Hierarchy | Tenant → management group → subscription → resource group → resource |
| Resource group | Ek project ka dabba; delete karo to sab delete |
| Naam aur tags | `rg-atithi-dev-cin`; `env`, `owner`, `cost-centre`; storage account ka naam unique, chhote akshar |
| Budget | Lab se pehle alert lagao |
| Entra ID | Staff aur applications ki directory |
| RBAC | Role + scope + principal; scope chhota, role kam |
| Managed identity | Bina secret ke duty badge; service principal secret se bacho |
| Terraform | `azurerm` provider, `features {}`, state Blob mein |
| Compute | VM, Scale Sets, App Service, Container Apps, AKS, Functions |
| Network | VNet, NSG, Load Balancer (L4), Application Gateway (L7), private endpoint |
| Data | Blob, Files, Managed Disks; Azure SQL, PostgreSQL, Cosmos DB |
| Key Vault, Monitor | Secrets aur certificates; metrics, logs, alerts, action group |
| AKS | Control plane Azure ka; `az aks get-credentials`; `--attach-acr` |
| Azure DevOps | Boards, Repos, Pipelines, Test Plans, Artifacts |
| Branch policy | `main` par seedha push band; review aur build zaroori; `AB#123` |
| YAML pipeline | `trigger`, `pool`, `stages`, `jobs`, `steps`; environments par approval |
| Service connection | Workload identity federation; secret kam |
| Safai | `az group delete --yes --no-wait`; portal mein check |

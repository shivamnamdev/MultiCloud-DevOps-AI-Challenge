# ✍️ 02: SCRIPT — SESSION-30: Azure & Azure DevOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S30`
- **Focus:** Multi-cloud mapping (AWS/Azure/GCP), Azure core concepts (subscription/resource group/Entra ID), core services & AKS, Azure DevOps Boards/Repos/Pipelines/Artifacts, YAML multi-stage pipeline
- **Episodes:**
  - Episode 1: Multi-Cloud ki Soch: AWS, Azure, GCP ka Naksha
  - Episode 2: Azure ke Building Blocks: Subscription, Resource Group, Entra ID
  - Episode 3: Core Services aur AKS
  - Episode 4: Azure DevOps: Boards, Repos, Pipelines, Artifacts

---

# 📺 EPISODE 1: Multi-Cloud ki Soch

### [00:00 – 01:15] Scene 1: Ek Cloud Seekha, Naukri Mein Doosra Mila
**[VISUAL: A learner who knows only AWS gets a job where the company uses Azure. A translation map overlays AWS names onto Azure names.]**

**(Voiceover):**
Aapne AWS seekha, lekin company Azure par chalti hai. Kya aap bekaar ho? Bilkul nahi. Cloud ke concepts aapas mein bahut milte hain: compute, storage, network, identity, monitoring. Sirf naam aur console badalte hain. Is episode mein hum ek translation map banate hain.

### [01:15 – 05:00] Scene 2: Service Mapping
**[VISUAL: A table. Compute: EC2 / Azure VM / Compute Engine. Object storage: S3 / Blob Storage / Cloud Storage. Network: VPC / VNet / VPC. Identity: IAM / Microsoft Entra ID + RBAC / IAM. Kubernetes: EKS / AKS / GKE. Serverless: Lambda / Functions / Cloud Functions. Monitoring: CloudWatch / Azure Monitor / Cloud Monitoring. IaC: CloudFormation / Bicep+ARM / Deployment Manager.]**

**(Voiceover):**
Compute: AWS mein EC2, Azure mein Virtual Machines, GCP mein Compute Engine. Object storage: S3, Blob Storage, Cloud Storage. Network: VPC, Azure mein VNet. Kubernetes: EKS, AKS, GKE. Serverless: Lambda, Azure Functions, Cloud Functions. Monitoring: CloudWatch, Azure Monitor, Cloud Monitoring. Identity: AWS IAM, Azure mein Microsoft Entra ID aur RBAC. Naam alag, idea ek. Dhyaan: mapping lagbhag hai, har service ke chhote farq hote hain, jaise limits aur pricing.

### [05:00 – 08:30] Scene 3: Multi-Cloud kyun aur Kab
**[VISUAL: Reasons: avoid lock-in, regulatory, best-of-breed, acquisitions, resilience. Costs: complexity, skills, egress fees, lowest-common-denominator. A balanced scale.]**

**(Voiceover):**
Companies multi-cloud kyun chunti hain? Vendor lock-in se bachne ke liye, regulations, kisi khaas service ke liye, ya acquisitions ki wajah se. Keemat: complexity, skills ki zaroorat, data ke bahar bhejne ka egress charge, aur har cloud ke best features chhodkar common cheezein use karna. Aksar companies chahkar nahi, halaat se multi-cloud ho jaati hain. Isliye Terraform, Kubernetes aur Docker jaise portable tools kaam aate hain, jo hum pehle seekh chuke hain.

### [08:30 – 11:30] Scene 4: Lab: Apni Mapping Table Banao
**[VISUAL: A spreadsheet. The learner fills 12 rows with AWS/Azure/GCP names for services used in Mini Shop. Notes column: differences.]**

**(Voiceover):**
Lab: ek table banao: Mini Shop ke har hisse ke liye AWS, Azure aur GCP ke equivalent. Frontend hosting, API, database, cache, queue, secrets, container registry, load balancer, DNS, monitoring, CI/CD, IaC. Har row mein ek line likho ki farq kya hai. Ye table interview mein bhi kaam aati hai, kyunki "AWS mein ye kaise hota, Azure mein kaise?" ek pasandida sawaal hai. Agle episodes mein hum is table ko Azure ke asli console se bharenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "same concepts, different names · mapping table · multi-cloud has real costs".]**

**(Voiceover):**
Recap: multi-cloud mapping. Ab Azure ke andar: uski structure.

---

# 📺 EPISODE 2: Azure ke Building Blocks

### [00:00 – 01:15] Scene 1: Azure mein Cheezein Rakhne ka Tareeka
**[VISUAL: A hierarchy picture: Tenant → Management groups → Subscriptions → Resource groups → Resources. Cost and access boundaries drawn.]**

**(Voiceover):**
AWS mein account mein sab kuch rehta hai. Azure ka ek alag hierarchy hai. Sabse upar tenant, yaani aapka organisation ka identity boundary. Uske andar subscriptions, jo billing aur access ki boundary hain. Subscription ke andar resource groups, jo resources ke logical dabbe hain. Is structure ko samajhna Azure ki sabse pehli zaroorat hai.

### [01:15 – 05:00] Scene 2: Subscription, Resource Group, Region
**[VISUAL: A resource group "rg-shop-dev" containing a VM, a disk, a NIC, a VNet. Deleting the group deletes all. Tags `env=dev`, `owner=asha`.]**

**(Voiceover):**
Resource group ek container hai jisme aapki app ke saare resources: VM, disk, network. Group ko delete karo to andar ka sab delete, isliye lab ke baad safai aasaan: ek resource group delete. Har resource ek region mein hota hai, aur group ka bhi ek location hota hai metadata ke liye. Naming convention banao, jaise `rg-shop-dev`, aur tags lagao, jaise `env` aur `owner`, taaki cost aur ownership pata chale. Subscription par budgets aur alerts lagana mat bhoolna.

### [05:00 – 08:30] Scene 3: Identity aur Access: Entra ID aur RBAC
**[VISUAL: Microsoft Entra ID (users, groups, service principals, managed identities) on the left. Azure RBAC on the right: Role (Reader/Contributor/Owner) + Scope (subscription/resource group/resource) + Principal = Role assignment.]**

**(Voiceover):**
Pehchaan Microsoft Entra ID sambhalta hai, jo pehle Azure AD kehlata tha: users, groups, aur applications ke liye service principals. Kaun kya kar sakta hai ye Azure RBAC tay karta hai: ek role, jaise Reader, Contributor ya Owner, ek scope par, jaise resource group, kisi principal ko. Role assignment ka matlab yahi teen cheezein. AWS ke roles jaisa idea Azure mein managed identity hai: VM ya app ko bina password ke pehchaan milti hai. Aur least privilege wahi rule: Owner mat do jab Reader kaam kare.

### [08:30 – 11:30] Scene 4: Lab: Azure CLI se Pehla Resource
**[VISUAL: `az login`, `az group create -n rg-demo -l centralindia`, `az storage account create ...`, `az group list -o table`, `az role assignment list`, `az group delete -n rg-demo --yes --no-wait`.]**

**(Voiceover):**
Lab: Azure free account ya sandbox lo, aur Azure CLI install karo. `az login`. `az group create --name rg-demo --location centralindia`. Phir ek storage account: `az storage account create --name YOURUNIQUENAME --resource-group rg-demo --sku Standard_LRS`. `az group list -o table` se dekho. Apne user ke role assignments dekho: `az role assignment list --assignee YOUR_EMAIL -o table`. Sabse aakhir mein `az group delete --name rg-demo --yes --no-wait` aur confirm karo ki sab hat gaya.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "tenant → subscription → resource group · RBAC = role + scope + principal · delete the group to clean".]**

**(Voiceover):**
Recap: Azure ka structure aur identity. Ab services: VM, network, storage aur AKS.

---

# 📺 EPISODE 3: Core Services aur AKS

### [00:00 – 01:15] Scene 1: Ek App, Teen Services
**[VISUAL: A web app architecture on Azure: VNet with subnets, VMs or App Service, Azure SQL / PostgreSQL, Blob Storage, Application Gateway or Load Balancer.]**

**(Voiceover):**
Ek app ko Azure par chalane ke liye aapko compute, network, database aur storage chahiye. Dekhte hain ki kaun si service kya karti hai, aur kab kaun sa chunein.

### [01:15 – 05:00] Scene 2: Compute, Network, Storage, Database
**[VISUAL: Four columns with options. Compute: VM, VM Scale Sets, App Service, Container Apps, AKS, Functions. Network: VNet, subnet, NSG, Load Balancer, Application Gateway. Storage: Blob, Files, Managed Disks. Database: Azure SQL, Azure Database for PostgreSQL/MySQL, Cosmos DB.]**

**(Voiceover):**
Compute: VM sab kuch aap sambhalo. App Service ek managed web hosting hai, bas code do. Container Apps aur AKS containers ke liye. Functions serverless. Network: VNet aur subnets, NSG, jo Network Security Group hai, yaani security group ka Azure roop. Load Balancer layer 4, Application Gateway layer 7. Storage: Blob objects ke liye, Files shared file system, aur Managed Disks VM ke liye. Database: Azure SQL, Azure Database for PostgreSQL, aur Cosmos DB NoSQL ke liye. Seedha rule: jitna managed, utna kam kaam.

### [05:00 – 08:30] Scene 3: AKS
**[VISUAL: An AKS cluster with Azure-managed control plane and node pools (VM scale sets). ACR integrated for images. `az aks get-credentials`. kubectl contexts.]**

**(Voiceover):**
AKS Azure ka managed Kubernetes hai, GKE ke jaisa. Control plane Azure sambhalta hai, aap node pools chalate ho, jo VM scale sets par chalte hain. Images Azure Container Registry, ACR, mein rakhte hain, aur AKS ko ACR se pull ki permission `az aks update --attach-acr` jaise tareeke se milti hai. `az aks get-credentials` kubeconfig mein context jod deta hai, aur phir sab kuch wahi `kubectl` jo humne GKE par kiya. Ye aapka multi-cloud ka asli faayda hai: ek baar seekha, kai jagah chala.

### [08:30 – 11:30] Scene 4: Lab: AKS par Mini Shop Service
**[VISUAL: `az group create`, `az aks create -g rg-demo -n aks-demo --node-count 1 --generate-ssh-keys`, `az aks get-credentials`, `kubectl apply -f deploy.yaml -f svc.yaml`, `kubectl get svc -w`, then `az group delete`.]**

**(Voiceover):**
Lab: `az group create -n rg-aks -l centralindia`, phir `az aks create -g rg-aks -n aks-demo --node-count 1 --generate-ssh-keys`, jisme kuch minute lagte hain. `az aks get-credentials -g rg-aks -n aks-demo`. GKE wale Deployment aur LoadBalancer Service YAML wahi `kubectl apply`. `kubectl get svc -w` se EXTERNAL-IP aur browser mein test. Dekho ki YAML ek jaisa kaam kiya. Aakhir mein `az group delete -n rg-aks --yes --no-wait`, kyunki AKS ke nodes aur load balancer paisa lete hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "VM/AppService/AKS · NSG · Blob · managed DBs · AKS = same kubectl".]**

**(Voiceover):**
Recap: Azure ke core services aur AKS. Ab Azure ka DevOps platform: Boards, Repos, Pipelines aur Artifacts.

---

# 📺 EPISODE 4: Azure DevOps

### [00:00 – 01:15] Scene 1: Ek Hi Jagah, Poori Delivery
**[VISUAL: A single platform with five tiles: Boards, Repos, Pipelines, Test Plans, Artifacts. A work item flows: Board card → branch → PR → pipeline → artifact → deployment.]**

**(Voiceover):**
Azure DevOps ek poora platform hai jisme planning se deploy tak sab ek jagah. Boards kaam track karne ke liye, Repos Git ke liye, Pipelines CI/CD ke liye, Test Plans testing ke liye, aur Artifacts packages ke liye. Ek work item ek card se shuru hota hai, aur ek deploy tak traceable rehta hai.

### [01:15 – 05:00] Scene 2: Boards, Repos aur Branch Policies
**[VISUAL: A Kanban board (To Do, Doing, Done) with work items. Repos: Git repo with a PR requiring 1 reviewer and a successful build. Link: "Fixes AB#123" in a commit/PR.]**

**(Voiceover):**
Boards mein epics, user stories aur tasks hote hain, Kanban ya Scrum ke saath. Repos mein Git repo, aur branch policies: main par seedha push band, PR ke liye review aur successful build zaroori. Commit ya PR mein `AB#123` likhne se wo work item se judta hai. Ye traceability audits ke liye bahut kaam aati hai: kaun sa feature kis code se aur kis deploy se judta hai. Agar aap GitHub use karte ho, to Azure Pipelines GitHub repos ke saath bhi kaam karta hai.

### [05:00 – 08:30] Scene 3: YAML Pipelines: Stages, Jobs, Environments
**[VISUAL: `azure-pipelines.yml` with `trigger`, `pool: vmImage: ubuntu-latest`, `stages` → `jobs` → `steps`, `variables`, and a deployment job targeting an `environment` with approvals. Service connections shown for Azure.]**

**(Voiceover):**
Azure Pipelines mein pipeline YAML mein likhi jaati hai: `trigger` kab chalegi, `pool` kaun si machine, `stages`, har stage mein `jobs`, aur jobs mein `steps`. Azure se baat karne ke liye service connection, jo credentials ya workload identity se surakshit rehta hai. Deploy ke liye environments, jinpar approvals aur checks lagte hain, jaise prod ke liye manual approval. Secrets variable groups ya Key Vault se. Concept bilkul wahi jo Jenkins aur GitHub Actions mein tha, sirf syntax alag.

### [08:30 – 11:30] Scene 4: Lab: Multi-stage Pipeline
**[VISUAL: A repo with a simple app. `azure-pipelines.yml` with Build stage (test, publish artifact) and Deploy stage (environment `dev`). The run shows two stages; an approval gate for `prod`.]**

**(Voiceover):**
Lab: free Azure DevOps organization banao aur ek project. Apni Python ya Node app ka repo import karo. `azure-pipelines.yml`:
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
  - stage: Deploy
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
Pipeline banao aur chalao. Environment par approval jodo, aur dekho ki deploy stage rukti hai. Free tier mein parallel jobs ki seema ho sakti hai, to org ki settings dekh lena.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Boards/Repos/Pipelines/Artifacts · branch policies · YAML stages · environments + approvals".]**

**(Voiceover):**
Recap: Azure aur Azure DevOps, aur multi-cloud ki soch. Ab sab kuch jodte hain: ek capstone project jo Git se production tak ek poori pipeline chalata hai.

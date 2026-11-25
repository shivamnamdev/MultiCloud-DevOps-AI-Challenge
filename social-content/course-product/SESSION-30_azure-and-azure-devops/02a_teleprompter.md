# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-30_azure-and-azure-devops

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,573 · **Episodes:** 4

---

# EPISODE 1: Doosra Landlord

## Ek Landlord Seekha, Naukri Doosre Ke Saath Mili

Maan lo Atithi Hotels ne ek bada hotel group khareeda, aur uski saari buildings Azure par hain. Aapne Session 10 se 14 mein AWS seekha. Kya aap bekaar ho gaye? Bilkul nahi. Landlord badla hai, par building, wing, door guard aur records office wahi. Naam aur console alag. Is episode mein hum ek translation table banate hain, jo har naye landlord par kaam aati hai.

## Translation Table

Compute: AWS mein EC2, Azure mein Virtual Machines, GCP mein Compute Engine. Warehouse, yaani object storage: S3, Blob Storage, Cloud Storage. Campus: VPC, Azure mein VNet. Door guard: security group, Azure mein NSG, yaani Network Security Group. Records office: RDS, Azure mein Azure SQL aur Azure Database for PostgreSQL. Operations command: EKS, AKS, GKE. Freelancer: Lambda, Azure Functions. Depot: ECR, ACR. Key cabinet: Secrets Manager, Azure mein Key Vault. Meters aur CCTV: CloudWatch, Azure Monitor. Naam alag, idea ek. Par ek chetavani: mapping lagbhag hoti hai. Har service ke chhote farq hote hain, jaise limits, pricing, aur kaun si cheez default mein private hai. Isliye table ke saath ek column "farq" ka bhi rakho.

## Teen Jagah Jahan Azure Alag Lagta Hai

Teen jagah jahan AWS wale ko Azure alag lagega. Pehla: Azure mein resource group hota hai, jahan ek project ki saari cheezein ek dabbe mein. AWS mein aisa dabba nahi, tags se kaam chalta hai. Doosra: pehchaan, yaani staff aur unke badges, Azure mein Microsoft Entra ID mein rehti hai, jo company ki apni directory hai, aur subscription alag cheez hai. Teesra: Azure mein ek virtual machine ke saath network card, disk, public IP aur NSG alag objects ki tarah dikhte hain. In teen cheezon ko samajh liya to baaki aasaan.

## Multi-Cloud kyun aur Kab

Companies multi-cloud kyun chunti hain? Vendor lock-in se bachne ke liye, kisi niyam ki wajah se, kisi khaas service ke liye, ya kisi doosri company ko khareedne ki wajah se, jo doosre landlord par thi. Keemat bhi hai: complexity, do cloud ki skills, data bahar bhejne ka egress charge, aur har landlord ki sabse achhi cheezein chhodkar common cheezein use karna. Sach ye hai ki aksar companies multi-cloud chahkar nahi, halaat se ban jaati hain. Isi liye wo tools kaam aate hain jo har landlord par chalte hain: Terraform, Docker, Kubernetes, Ansible, Prometheus. Ye hum seekh chuke hain. Ek seedha rule: do cloud tab rakho jab uski wajah likhi ho, sirf "kya pata kabhi zaroorat pade" wajah nahi.

## Lab: Apni Translation Table Banao

Lab: ek table banao: Atithi ki website ke har hisse ke liye AWS, Azure aur GCP ke naam. Website hosting, API, database, cache, queue, secrets, container registry, load balancer, DNS, monitoring, CI/CD, aur infrastructure as code. Har row mein ek line "farq" likho. Jo naam aapko nahi pata, use docs mein dhoondho, aur guess mat likho. Ye table interview mein bhi kaam aati hai, kyunki "AWS mein ye kaise hota hai, Azure mein kaise?" ek pasandida sawaal hai. Aage ke episodes mein hum is table ko Azure ke asli portal se bharte jaayenge.

## Recap aur Bridge

Recap: translation table aur teen farq. Ab Azure ke andar ka naksha: tenant se resource group tak, aur duty badge kaise milte hain.

---

# EPISODE 2: Azure ka Naksha

## Cheezein Kahan Rakhi Jaati Hain

Atithi ne Azure par kaam shuru kiya. Pehla sawaal: cheezein kahan rakhi jaayen? Sabse upar tenant hai, yaani company ki pehchaan wali directory. Uske neeche management groups, jinse kai subscriptions par ek saath niyam lagte hain. Subscription billing aur access ki sabse bada daayra hai, aur AWS ke account jaisa samjho. Subscription ke andar resource groups: ek project ki cheezein ek dabbe mein. Aur dabbe ke andar asli resources. Is naksha se hi pata chalta hai ki kharcha kahan dikhega aur kaun kya chhoo sakta hai.

## Resource Group, Region, Naam aur Tags

Resource group ek dabba hai, jiske andar ek project ki saari cheezein. Group delete karo to andar ka sab delete, isliye lab ke baad safai aasaan: ek command. Har resource ek region mein hota hai, aur group ka bhi ek location hota hai, jahan uska metadata rehta hai. Naming convention banao, jaise rg-atithi-dev-cin, jisme project, environment aur region ho. Tags lagao: env, owner, cost-centre, taaki bill mein dikhe kaun kitna kharch kar raha hai. Aur lab shuru karne se pehle subscription par budget alert lagao, jaise Session 15 mein AWS par lagaya tha. Ek niyam aur: kuch resource ke naam poori duniya mein unique hote hain, jaise storage account, jisme sirf chhote akshar aur ank aate hain.

## Pehchaan: Entra ID aur Azure RBAC

Staff kaun hai, ye Microsoft Entra ID tay karta hai, jo pehle Azure AD kehlata tha: users, groups, aur applications ke liye service principals. Kaun kya kar sakta hai, ye Azure RBAC tay karta hai. Ek role assignment mein teen cheezein hoti hain: role, jaise Reader, Contributor ya Owner; scope, jaise ek resource group; aur principal, yaani kisko. Jaise: asha ko rg-atithi-dev-cin par Contributor. Scope jitna chhota, utna surakshit. Contributor resource bana sakta hai par kisi ko role de nahi sakta, Owner de sakta hai, isliye Owner kam logon ko. Wahi least privilege jo Session 09 mein tha.

## Managed Identity: Building ka Apna Duty Badge

AWS mein building ko role milta tha, jise instance profile se pehnaya jaata tha. Azure mein iska naam managed identity hai. VM ya app ko ek identity milti hai, aur wo bina password ke Entra ID se token leti hai. Fir us identity ko Key Vault ya storage par ek role assignment mil jaata hai. Service principal ke saath secret ya certificate rakhna padta hai, aur wo kisi file mein ruk jaata hai. Managed identity mein koi secret hai hi nahi. Sabse achha rasta: jahan bhi ho sake, managed identity. Aur jahan pipeline ko Azure se baat karni ho, wahan workload identity federation, jo OIDC ka wahi idea hai jo humne Session 20 aur 28 mein dekha tha.

## Azure par Terraform: Naya Contractor

Session 27 mein humne kaha tha ki har landlord ke liye alag contractor, yaani provider, hota hai. Azure ka contractor azurerm hai. Plan, apply, destroy, wahi sab. Naye resource ka naam alag: azurerm_resource_group, azurerm_storage_account. Register, yaani state, yahan Azure Blob Storage mein rakhte hain, aur wahan bhi lock milta hai. Provider block mein features {} chahiye. Azure ka apna tool Bicep bhi hai, jo sirf Azure ke liye hai. Par jo team do landlord ke saath kaam karti hai, wo aksar ek hi tool, Terraform, rakhti hai. Version aur authentication ke exact tareeke ke liye provider ke docs dekho.

## Guardrails: Policy, Lock aur Cost

Azure mein teen guardrails Atithi ke kaam ke hain. Pehla Azure Policy: ek niyam jo poore subscription par lagta hai, jaise "har resource par owner tag ho" ya "storage account public na ho". Niyam todne wala resource ban hi nahi paata, ya report mein laal dikhta hai. Ye wahi policy as code ka idea hai jo Session 28 mein tha. Doosra resource lock: production ke group par delete lock lagao, to galti se bhi group delete nahi hota, jab tak koi pehle lock na hataye. Teesra Cost Management: budget aur alert, aur dekho ki kharcha kis tag par ja raha hai. Ye teen ek baar lagao, aur phir naye logon ko Contributor dena bhi kam darawna lagta hai.

## Lab: Azure CLI se Pehla Resource

Lab: Azure free account ya sandbox lo, aur Azure CLI install karo. Pehle az login, phir az account show, taaki dekho ki kaun sa subscription chal raha hai. Phir:

Storage account ka naam chhote akshar aur ank mein, poori duniya mein unique. --allow-blob-public-access false wahi Block Public Access ka idea hai jo Session 12 mein tha. Role assignments dekho. Email se --assignee personal Microsoft account par aksar fail hota hai, isliye apni object ID se dekho. Naye account par pehli baar storage banate waqt SubscriptionNotFound jaisa gumrah karne wala error aa sakta hai; asal wajah ye hoti hai ki Microsoft.Storage provider register nahi hai, to az provider register --namespace Microsoft.Storage chalao aur register hone do. Aakhir mein az group delete --name rg-demo --yes --no-wait, aur portal mein confirm karo ki sab hat gaya. Ek group, ek delete.

## Recap aur Bridge

Recap: Azure ka naksha, RBAC aur managed identity. Ab buildings aur operations command: core services, ACR aur AKS.

---

# EPISODE 3: Buildings aur Operations Command

## Ek Website, Chaar Zaroorat

Atithi ki booking website ko Azure par chalane ke liye wahi chaar cheezein chahiye jo AWS par thi: building, campus, records office aur warehouse. Dekhte hain ki Azure inhe kaise deta hai, aur kab kaun sa raasta chunna chahiye.

## Compute, Network, Storage aur Database

Compute mein seedhi building: Virtual Machine, aur uski Auto Scaling ka naam VM Scale Sets. App Service ek managed web hosting hai: bas code do, building landlord sambhalta hai. Container Apps aur AKS trucks ke liye. Functions freelancer ke liye. Campus mein VNet aur subnets, aur door guard NSG, jo subnet par ya building ke network card par lagta hai. Load Balancer layer 4 par kaam karta hai, Application Gateway layer 7 par, yaani marshal jo raasta dekh kar bhejta hai. Private endpoint se kisi managed service tak raasta campus ke andar se hi ata hai. Warehouse mein Blob, shared files ke liye Files, aur building ki disk ke liye Managed Disks. Records office mein Azure SQL, Azure Database for PostgreSQL, aur loose forms ke liye Cosmos DB. Seedha rule: jitna managed, utna kam kaam, aur utna kam control.

## Key Vault aur Azure Monitor

Key cabinet Azure mein Key Vault hai: secrets, keys aur certificates. App ki managed identity ko Key Vault par secrets padhne ka role do, aur password kisi file ya environment mein likhna nahi padega. Meters aur CCTV Azure Monitor mein: metrics, logs ke liye Log Analytics, aur alerts, jinhe action group se email ya phone par bheja jaata hai. Ye Session 15 ke CloudWatch aur SNS ka Azure roop hai, aur jo kuch Session 26 mein Prometheus aur Grafana se dekha, wo kisi bhi landlord par waise hi chalega.

## ACR aur AKS

AKS Azure ka managed operations command hai, GKE jaisa. Reception, ledger aur allocation officer, yaani control plane, Azure sambhalta hai. Aap node pools chalate ho, jo VM scale sets par chalte hain. Truck designs ACR, yaani Azure Container Registry, mein rakhte hain: wahi depot jo Session 22 mein tha. AKS ko ACR se pull karne ki permission az aks update --attach-acr se, ya cluster banate waqt --attach-acr flag se, mil jaati hai. az aks get-credentials kubeconfig mein naya context jod deta hai. Uske baad sab kuch wahi kubectl get, apply, describe, logs jo GKE par kiya tha. Yahi multi-cloud ka asli fayda hai: ek baar seekha, kai landlord par chala. Ek chetavani: control plane ka paisa tier par nirbhar hai, aur node, load balancer, public IP sab ghante ke hisaab se lagte hain.

## Lab: ACR aur AKS par rooms-service

Lab: pehle budget alert. Phir:

Free account par az acr build aksar TasksOperationsNotAllowed deta hai, kyunki ACR Tasks band hota hai. Tab laptop par docker build --platform linux/amd64, phir az acr login aur docker push karo; Apple chip par --platform zaroori hai kyunki AKS ke node amd64 hote hain. Aur az aks create mein --node-vm-size do: free account par har size allowed nahi hota, aur error khud allowed sizes ki list dikha deta hai. Cluster banne mein kuch minute lagte hain. kubectl get nodes se dekho ki ek node Ready hai. Session 24 ka Deployment aur LoadBalancer Service YAML lo, image ka naam ACR ke address se badlo, kubectl apply, aur kubectl get svc -w se EXTERNAL-IP aane do. Browser ya curl se /health. Wahi YAML, naya landlord. Aakhir mein az group delete --name rg-aks --yes --no-wait, kyunki node aur load balancer paisa lete hain. Flags aur size ke naam badalte rehte hain, isliye az aks create --help se apna version dekh lo.

## Recap aur Bridge

Recap: Azure ke core services, aur AKS par wahi Kubernetes. Ab Azure ka ready-made head office: Azure DevOps.

---

# EPISODE 4: Ready-made Head Office

## Planning Wall se Parts Store Tak

Head office mein hum pehle se vault (Git), foreman (Jenkins) aur conveyor (Actions) dekh chuke hain. Azure ek poora ready-made head office deta hai, jisme sab ek jagah: Boards, yaani planning wall, jahan kaam track hota hai. Repos, yaani vault, jahan Git ka code rehta hai. Pipelines, yaani conveyor. Test Plans, yaani inspection. Aur Artifacts, yaani parts store, jahan packages rakhe jaate hain. Ek kaam ka card shuru se deploy tak traceable rehta hai.

## Boards, Repos aur Branch Policies

Boards mein epics, user stories aur tasks, Kanban ya Scrum ke saath. Repos mein Git ka vault, aur branch policies, jo wahi master par taala hai jo Session 16B mein GitHub par tha: main par seedha push band, pull request mein kam se kam ek review, aur build successful hona zaroori. Commit ya PR mein AB#123 likho to wo work item se judta hai. Ye traceability audit mein kaam aati hai: kaun sa feature, kis code se, kis deploy se. Aur agar aapka code GitHub par hai, to Azure Pipelines GitHub ke repo ke saath bhi chalta hai. Azure ka head office zaroori nahi ki vault bhi Azure mein ho.

## YAML Pipeline: Stages, Jobs, Steps

Azure Pipelines mein conveyor YAML mein likhi jaati hai: trigger kab chalegi, pool kaun si machine, stages, har stage ke andar jobs, aur jobs ke andar steps. Jenkins se mila lo to: stage wahi, job ek workbench par chalne wala blok, step wahi sh. Azure se baat karne ke liye service connection, jise key cabinet ka ek entry samjho. Behtar hai ki wo workload identity federation se bane, yaani koi lambi umar wala secret nahi. Concept bilkul wahi jo Jenkins aur GitHub Actions mein tha. Sirf syntax alag hai, aur isliye ek baar seekha to teeno aate hain.

## Environments, Approvals aur Secrets

Deploy ke liye environments. Environment par approvals aur checks lagte hain: prod ke liye ek duty manager ki manjoori, ya sirf main branch se deploy. Ye wahi input step hai jo Jenkins mein tha, par yahan ye platform ka hissa hai aur workbench ko rokta nahi. Secrets ke liye variable groups, jo Key Vault se jode ja sakte hain, to password pipeline ke YAML ya Git mein nahi aata. Aur pipeline logs mein secrets chhupe hote hain, par ye surakshit baad mein nahi, isliye unhe print mat karo. Artifacts mein build ka output ya package rakho, jise baad ke stages utha sakte hain, jaise Session 18 mein archive kiya tha.

## Lab: Do Stage ki Conveyor

Lab: free Azure DevOps organization aur ek project banao. Apna Python repo import karo, ya Atithi ka rooms-service. Phir azure-pipelines.yml:

Pipeline banao aur chalao. Phir ek prod environment banao, uspar approval check lagao, aur ek teesra stage jodo. Dekho ki wo manjoori ka intezaar karta hai. Nayi organization ko shuru mein free hosted minutes nahi milte; pipeline No hosted parallelism has been purchased or granted se fail hoti hai, aur request ka purana form band ho chuka hai. Tab ek self-hosted agent apne laptop par chalao, jo free aur unlimited minutes deta hai, aur YAML mein pool: name: Default likho. Pehli run par pipeline ko pool aur environment ki permission dene wala Permit button dabana padta hai. prod par approval check lagao, aur akele learner ko apna hi approval dene ke liye branch policy mein creator ka vote count hone do. Aakhir mein pipeline ko ACR par image push karne wale step se jodne ki koshish karo, jo isi session ke Episode 3 se mil jaata hai.

## Kab Azure DevOps, Kab Baaki

Kab kaun sa head office? Agar company Microsoft ke tools par hai, aur planning, code aur pipeline ek hi jagah chahiye, to Azure DevOps theek hai. Agar code GitHub par hai aur community bada hai, to GitHub aur Actions. Agar bahut khaas plugins ya on-premise chahiye, to Jenkins. Teeno mein wahi concepts hain: vault, bell, conveyor, stage, approval, key cabinet. Isliye naya tool aane par ghabrao mat. Ye table interview ke liye bhi kaam aati hai.

## Recap aur Bridge

Recap: Azure ki translation, uska naksha, AKS, aur Azure DevOps. Atithi ke paas ab teen landlord ka gyaan hai, aur har tool ka ek ghar. Ab sab kuch ek saath jodte hain: pehla grand opening. Ek revision vault mein jaata hai, ghanti bajti hai, foreman fabricate karta hai, ek truck nikalta hai aur ek guest ko serve karta hai. Agla session: capstone.

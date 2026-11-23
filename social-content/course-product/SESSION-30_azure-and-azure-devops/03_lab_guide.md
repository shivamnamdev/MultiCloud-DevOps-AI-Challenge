# Session 30 lab guide: Azure and Azure DevOps

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **What was tested, and what was not.**
> Run for real in November 2026 on a brand-new Azure free account (Azure CLI 2.93, region Central India) and a brand-new Azure DevOps organization: resource group and storage account, role assignments, delete lock, Azure Policy, Terraform `azurerm` 4.81 (plan, apply, drift, destroy), Azure Container Registry, a one-node AKS cluster running `rooms-service` behind a load balancer, and a three-stage Azure DevOps pipeline with an approval on `prod`, a branch policy and a pull request. Everything was deleted the same day.
> **Not tested:** Key Vault, managed identities, Azure Monitor, VMs, VNets and NSGs, Azure SQL/PostgreSQL, App Service, Bicep, Terraform state in Blob Storage, Azure Boards and the `AB#123` link, Artifacts, variable groups, service connections, and Microsoft-hosted pipeline agents (our new organization had no free hosted minutes, see Part D). The Azure free-offer numbers (credit amount, days) were **not confirmed**; read your own offer page.

| | |
|---|---|
| **Time** | Part A 20 min, Part B 50 min, Part C 45 min (cluster lives about 15), Part D 60 min |
| **Cost** | Part B: pennies at most (empty storage account, deleted). Part C: **billed while the cluster and load balancer exist**; we kept ours about 12 minutes. Part D: free. |
| **Skill check before you start** | Sessions 9, 15, 22, 24, 27, 28 (IAM, budgets, Docker images, `kubectl`, Terraform). A credit card for the Azure account. |

Starter files: `lab_files/terraform/main.tf`, `lab_files/rooms-service/` (a tiny Python service with `/health` and `/rooms`, `Dockerfile`, `k8s/rooms-service.yaml`, `azure-pipelines.yml`).

**Your IDs are private.** Azure prints your subscription ID and tenant ID in many errors and in `az account show`. Do not paste them into screenshots, chats or Git. Our outputs below hide them as `<GUID>`.

---

## Part A: the translation table (Episode 1)

Fill your own table from the real Azure portal. This is our starting point; check every row yourself.

| Idea | AWS | Azure | GCP |
|---|---|---|---|
| Top-level billing/isolation boundary | account | **subscription** | project |
| Folder for one project's resources | (tags, or one account per project) | **resource group** (a real object you can delete in one command) | project |
| People and logins | IAM | **Microsoft Entra ID** (identities) plus **Azure RBAC** (permissions) | Cloud IAM |
| Virtual server | EC2 | Virtual Machine | Compute Engine |
| Private network | VPC | Virtual Network (VNet) | VPC |
| Door guard | security group | Network Security Group (NSG) | firewall rules |
| Object storage | S3 | Blob Storage, inside a **storage account** | Cloud Storage |
| Secrets | Secrets Manager | Key Vault | Secret Manager |
| Image registry | ECR | Azure Container Registry (ACR) | Artifact Registry |
| Managed Kubernetes | EKS | AKS | GKE |

**Three places Azure feels different** (the script's Scene 3, now checked):
1. **A resource group is a real container.** `az group delete` removes everything inside. AWS has no equal.
2. **Roles are granted at a scope.** The same role can be given on the subscription, a resource group or one resource. You will see this in B3.
3. **Some names are global.** A storage account or a container registry name must be unique in the whole world, lower-case letters and digits only (storage: 3 to 24 characters).

---

## Part B: the first resources, guardrails, and Terraform (Episode 2)

### B0. Before anything: budget, login, and one provider step

1. In the portal open **Cost Management, Budgets** and create a small monthly budget with an alert at 80 percent. (On our new account no budget existed until we looked; the CLI showed an empty list.) Creating the budget was **not tested** by us.
2. Log in in your own terminal and check which subscription is active:

```bash
az login
az account show --query "{name:name, state:state}" -o table
```

We saw `Azure subscription 1   Enabled`. Do not run `az account show` without `--query` in a screen share: it prints your subscription and tenant IDs.

3. **New accounts have most resource providers switched off.** Ours had only 17 registered, and `Microsoft.Storage` was not one of them. Check, then register (free, takes about a minute):

```bash
az provider show -n Microsoft.Storage --query registrationState -o tsv
az provider register --namespace Microsoft.Storage
```

**The trap (tested):** before registering, `az storage account create` failed with `(SubscriptionNotFound) Subscription ... was not found`. The subscription is fine; the real cause is the unregistered provider. Terraform's `azurerm` provider registers the core providers for you, which is why the Terraform part worked without this step.

### B1. The script's lab, with two fixes

```bash
az group create --name rg-demo --location centralindia --tags Project=atithi-lab owner=you
SA=atithidemo$RANDOM$RANDOM
az storage account create --name $SA --resource-group rg-demo --location centralindia \
  --sku Standard_LRS --kind StorageV2 --allow-blob-public-access false --min-tls-version TLS1_2
az storage account show -n $SA -g rg-demo \
  --query "{sku:sku.name, publicBlob:allowBlobPublicAccess, tls:minimumTlsVersion, https:enableHttpsTrafficOnly}" -o table
az group list -o table
```

Result: `Standard_LRS / False / TLS1_2 / True`. Public blob access is off, which is the Session 12 "Block Public Access" idea. `az group list` also showed a group named `VisualStudioOnline-...` that we did not create: Azure makes it when you create an Azure DevOps organization. Leave it alone.

### B2. Roles: the script's command fails, here is the fix (tested)

The script's `az role assignment list --assignee YOUR_EMAIL` **fails on a personal Microsoft account**:

```
ERROR: Cannot find user or service principal in graph database for '<your email>'.
```

Your sign-in name is stored in the directory as a guest-style name, so the plain email does not match. Use your object ID, or list the subscription's assignments:

```bash
az role assignment list --all --assignee-object-id $(az ad signed-in-user show --query id -o tsv) -o table
az role assignment list -o table
```

We saw one row: the role **Owner** at the scope `/subscriptions/<GUID>`. That is "role + scope + principal" from the script: you are Owner of the whole subscription, so least privilege starts with creating a smaller role for helpers, not for you.

### B3. Guardrails: lock and policy (tested)

```bash
az lock create --name no-delete --lock-type CanNotDelete --resource-group rg-demo
az group delete --name rg-demo --yes
```

The delete is refused: `(ScopeLocked) The scope '.../resourcegroups/rg-demo' cannot perform delete operation because following scope(s) are locked ... Please remove the lock and try again.` The group is untouched.

Now a policy that demands an `owner` tag on every resource in the group (this uses the built-in "Require a tag on resources"):

```bash
az policy assignment create --name need-owner-tag --display-name "Require owner tag" \
  --policy 871b6d14-10aa-478d-b590-94f262ecfa99 --params '{"tagName":{"value":"owner"}}' \
  --resource-group rg-demo
az storage account create -n atithipol$RANDOM$RANDOM -g rg-demo -l centralindia --sku Standard_LRS   # blocked
az storage account create -n atithitag$RANDOM$RANDOM -g rg-demo -l centralindia --sku Standard_LRS --tags owner=you   # allowed
```

The untagged one is refused with `(RequestDisallowedByPolicy) Resource ... was disallowed by policy` and names your policy. The tagged one is created. In our test the policy took effect **on the first try** (Microsoft says it can take longer).

A policy does not touch resources that already existed: our first storage account (made before the policy, with no `owner` tag) stayed untouched.

### B4. Clean up Part B (tested)

```bash
az lock delete --name no-delete --resource-group rg-demo
az group delete --name rg-demo --yes        # took about 63 seconds
az group list -o table                       # rg-demo is gone
```

### B5. Terraform on Azure (tested)

Files: `lab_files/terraform/main.tf`. It creates a resource group and a storage account with public access off.

```bash
cd lab_files/terraform
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)    # do not echo it
terraform init
terraform plan -var "subscription_id=$ARM_SUBSCRIPTION_ID" -var "suffix=$RANDOM$RANDOM" -out=tfplan
terraform apply tfplan
```

We saw `Plan: 2 to add`, then `Apply complete! Resources: 2 added` (the storage account took **1 minute 22 seconds**; Azure is slower here than AWS S3).

Things we hit or checked:
- **`subscription_id` is required** since `azurerm` 4.0. Leave it out and the plan fails.
- `features {}` is required, even if empty.
- **Logging in:** Terraform uses your `az login` session, so the machine that runs Terraform needs the `az` command. Running Terraform in a Docker container without `az` fails with `could not configure AzureCli Authorizer ... exec: "az": executable file not found`. A raw access token in `ARM_ACCESS_TOKEN` is **not** accepted by the provider (it fell back to the CLI).
- **Drift, tested:** we changed a tag by hand (`az group update -n rg-atithi-tf --set tags.owner=someone-else`) and `terraform plan` showed `~ "owner" = "someone-else" -> "<your value>"` and `Plan: 0 to add, 1 to change`. That is the Session 28 drift lesson on a new landlord.

```bash
terraform destroy -var "subscription_id=$ARM_SUBSCRIPTION_ID" -var "suffix=THE_SAME_SUFFIX"   # about 21 seconds
```

Use the **same** suffix, or Terraform plans to destroy something different from what you built. Keep the state file private; it can hold secrets.

---

## Part C: ACR and AKS (Episode 3)

> **This part costs money while it exists.** Do Part B0's budget first. Do the whole part in one sitting, and delete the group at the end. Our cluster lived about 12 minutes.

### C1. Your service

`lab_files/rooms-service/` has `app.py` (standard library only, port 8080, `/health` and `/rooms`), `test_app.py`, and a `Dockerfile` that runs as a non-root user. Check it locally first: `python3 -m pytest -q` should say `1 passed`.

### C2. Registry and image: the script's `az acr build` fails on free accounts

```bash
az group create --name rg-aks --location centralindia --tags Project=atithi-lab owner=you
ACR=atithiacr$RANDOM$RANDOM          # global name, lower-case letters and digits
az acr create --resource-group rg-aks --name $ACR --sku Basic
az acr build --registry $ACR --image rooms-service:1.0 .
```

**The trap (tested):** on our free account the last command failed with

```
(TasksOperationsNotAllowed) ACR Tasks requests for the registry ... are not permitted. Please file an Azure support request
```

ACR Tasks (the cloud build) is switched off on free subscriptions. The script's other route, a local build and push, worked:

```bash
az acr login --name $ACR
docker build --platform linux/amd64 -t $ACR.azurecr.io/rooms-service:1.0 .
docker push $ACR.azurecr.io/rooms-service:1.0
az acr repository show-tags --name $ACR --repository rooms-service -o tsv     # 1.0
```

`--platform linux/amd64` matters on an Apple-chip Mac: your laptop is arm64, but the cluster's machines are amd64, and an arm64 image would crash with `exec format error`. (We built the amd64 image; running an arm64 one on the cluster was not tried.)

### C3. The cluster

```bash
az aks create --resource-group rg-aks --name aks-atithi --node-count 1 \
  --node-vm-size Standard_D2s_v5 --attach-acr $ACR --generate-ssh-keys --tier free
```

**The trap (tested):** the script's command has no `--node-vm-size`, and the first size we tried, `Standard_D2s_v3`, was refused at once:

```
(BadRequest) The VM size of Standard_D2s_v3 is not allowed in your subscription in location 'centralindia'. The available VM sizes are '...'
```

The error prints the full list of allowed sizes; pick a 2-vCPU one from it (we used `Standard_D2s_v5`). Our new account also had a quota of **4 vCPUs** in Central India, so one two-vCPU node fits and a second small cluster would not. Nothing was created or billed by the refused attempt.

The cluster was ready in **5 minutes 20 seconds** (Kubernetes 1.36). To keep your own `~/.kube/config` clean, write the credentials to a separate file:

```bash
export KUBECONFIG=$PWD/aks-kubeconfig
az aks get-credentials --resource-group rg-aks --name aks-atithi --file $KUBECONFIG --overwrite-existing
kubectl get nodes          # one node, Ready
```

### C4. Deploy

Use `k8s/rooms-service.yaml` (a Deployment with two replicas and a readiness probe on `/health`, plus a `LoadBalancer` Service). Replace `YOUR_ACR_NAME`.

```bash
sed "s/YOUR_ACR_NAME/$ACR/" k8s/rooms-service.yaml | kubectl apply -f -
kubectl rollout status deploy/rooms-service
kubectl get svc rooms-service -w          # wait for EXTERNAL-IP (ours came in about 10 seconds)
curl http://EXTERNAL_IP/health            # {"status": "ok"}   200
curl http://EXTERNAL_IP/rooms             # two rooms          200
curl http://EXTERNAL_IP/nope              # {"error": "not found"}  404
```

All pods pulled the image from ACR **without any pull secret**: `--attach-acr` had given the cluster the right to read your registry. That is the "same YAML, new landlord" point from the script.

### C5. Delete everything, then check

```bash
az group delete --name rg-aks --yes        # took about 6 minutes
az group list -o table
az network public-ip list --query "length(@)" -o tsv     # 0
```

AKS also made a second group, `MC_rg-aks_aks-atithi_centralindia`, for the node and the load balancer; deleting `rg-aks` removed it too. A group named `NetworkWatcherRG` appeared on its own; it is Azure's free Network Watcher and can stay. Check the portal as the script says.

---

## Part D: Azure DevOps (Episode 4)

### D1. Organization and project

At `dev.azure.com`, sign in with the same Microsoft account, create an organization, then a **private** project (we used Git and the Agile process).

**The trap (tested): no free pipeline minutes on a new organization.** Microsoft's own Q&A says it has paused the automatic free grant for new organizations to stop abuse. The old "request parallelism" form we tried was retired. Until a grant arrives, a pipeline fails with `No hosted parallelism has been purchased or granted`. We did not get far enough to see that message because we used the free alternative below, so treat the message as reported by Microsoft, not seen by us.

**The free alternative that does not need approval: a self-hosted agent.** Every organization gets one self-hosted agent with unlimited minutes. We ran one on the laptop for the test (steps in D4).

### D2. Personal access token

Create a token only for this lab: 7 days, scopes **Code** (read and write), **Build** (read and execute), **Project and Team** (read), **Environment** (read and manage), **Agent Pools** (read and manage). Save it to a file, never into chat or Git:

```bash
pbpaste | tr -d ' \r\n' > ~/.azdo_pat && chmod 600 ~/.azdo_pat
```

**Two traps (tested):** a real token is about 84 letters and digits with no spaces. We first saved something with spaces in it (the wrong clipboard text), and the server answered with a redirect to a sign-in page, which looks like a broken website, not a bad token. Also, a token without the **Environment** and **Agent Pools** scopes works for repos and pipelines but gets `401` on environments and pools. You can edit a token's scopes without making a new one. **Revoke the token and delete the file when the lab is done.**

### D3. The pipeline

`lab_files/rooms-service/azure-pipelines.yml` has three stages: `Build` (create a virtual environment, install, run `pytest`, publish `app.py` as an artifact), `DeployDev` (environment `dev`), `DeployProd` (environment `prod`). The deploy steps are just `echo`. Push the files to your project's repo (`app.py`, `test_app.py`, `requirements.txt`, `Dockerfile`, `azure-pipelines.yml`), then **Pipelines, New pipeline, Azure Repos Git, Existing YAML file**.

The `pool:` line says `name: Default` for the self-hosted agent. If you have free hosted minutes, use `vmImage: ubuntu-latest` instead.

### D4. A self-hosted agent for the test (tested on macOS Apple chip)

In **Organization settings, Agent pools, Default, New agent** the portal shows the download for your system. We used the current Mac arm64 build (5.282.0) and checked its SHA-256 against the value the service publishes.

```bash
mkdir agent && cd agent && tar xzf ~/Downloads/vsts-agent-osx-arm64-*.tar.gz
./config.sh --unattended --url https://dev.azure.com/YOUR_ORG --auth pat --pool Default \
  --agent lab-mac --acceptTeeEula        # asks for the token; or set VSTS_AGENT_INPUT_TOKEN
./run.sh                                  # leave it running; "Listening for Jobs"
```

Security: the agent runs whatever the pipelines in your organization tell it to, on your laptop. Use it only for a private project you control, and **remove it afterwards**: stop `run.sh`, then `./config.sh remove --auth pat`, then delete the folder.

### D5. First run: the permission prompt (tested)

Queue the pipeline. In our test it sat at `notStarted` for minutes while the agent showed "online" and idle. The cause: a pipeline must be **permitted** to use a resource (the agent pool, each environment) the first time. The run page shows "This pipeline needs permission to access a resource before this run can continue to ..." with a **View** and **Permit** button. Click Permit for each; we did the same through the API. After that the run proceeded: `Build` succeeded, `DeployDev` succeeded.

### D6. The approval on `prod` (tested)

In **Pipelines, Environments, prod, ... , Approvals and checks, Approvals** add yourself (or a teammate) as approver. The script says the next stage waits, and it does: `DeployProd` stayed pending with your instructions text until we approved, then it ran, and the whole run ended `Build succeeded | DeployDev succeeded | DeployProd succeeded`. Note that approving as the person who started the run works because we left "requester cannot approve" off.

### D7. Branch policy and pull request (tested)

On the repo, **Branches, main, ... , Branch policies**: require **1 reviewer**. Then:

- A direct `git push origin main` is rejected: `TF402455: Pushes to this branch are not permitted; you must use a pull request to update this branch.` This held even for the organization owner.
- **The solo-learner trap:** with the default "requestors can approve their own changes" off, you cannot approve your own pull request, so you are stuck. In the policy, tick **Allow requestors to approve their own changes** for a one-person lab. We did, approved, and the pull request merged (squash).
- The merge to `main` started a pipeline run by itself (`trigger: [ main ]`), and since it reached `prod`, it waited for approval again. **Cancel that run** when you do not want to approve.

`AB#123` links in commit messages (Azure Boards) were **not tested**.

### D8. Clean up

Stop and unregister the agent (D4), revoke your token in the portal and delete `~/.azdo_pat`, and cancel any waiting run. The organization and the project cost nothing; you can keep them for Session 20-style practice or delete the project in **Project settings, Overview, Delete**.

---

## If something goes wrong

| You see | Cause | Fix |
|---|---|---|
| `SubscriptionNotFound` right after login | resource provider not registered | `az provider register --namespace Microsoft.Storage` (or the provider named in the error) |
| `Cannot find user or service principal in graph database` | `--assignee` with a personal email | use `--assignee-object-id $(az ad signed-in-user show --query id -o tsv)` |
| `ScopeLocked` on delete | a delete lock | `az lock delete --name no-delete --resource-group GROUP` |
| `RequestDisallowedByPolicy` | a policy blocks the resource | read the policy name in the error; add the missing tag or setting |
| Storage name rejected | not unique, upper-case, or too long | 3 to 24 lower-case letters and digits, add random digits |
| `TasksOperationsNotAllowed` on `az acr build` | ACR Tasks off on free accounts | build locally and `docker push` (C2) |
| `The VM size ... is not allowed in your subscription` | size not available to your account | choose one from the list in the error; check quota |
| Pods `ErrImagePull` / `exec format error` | image missing, or built for the wrong chip | build with `--platform linux/amd64`; check `az aks create --attach-acr` |
| `could not configure AzureCli Authorizer` | Terraform has no `az` command | run Terraform where `az login` was done |
| Pipeline run stays `notStarted` | needs permission for the pool or environment, or no free hosted minutes | click **Permit**; or use a self-hosted agent |
| Server redirects to a sign-in page when you use the token | token wrong or copied with spaces | recreate it; save with `tr -d ' \r\n'` |
| `401` on environments or pools only | token lacks those scopes | edit the token's scopes |
| Cannot approve your own pull request | creator's vote does not count | allow requestors to approve their own changes (solo lab only) |

## What we did not test

Key Vault, managed identity and `DefaultAzureCredential`, Azure Monitor and Log Analytics, VMs, VNets and NSGs, Azure SQL and PostgreSQL, App Service, Bicep, Terraform state in Blob Storage with a lock, budgets created from the CLI or portal, Azure Boards and `AB#` links, Artifacts, variable groups with Key Vault, service connections, Microsoft-hosted agents, an `az acr build` that works, a second human account, and the exact size of the Azure free credit.

# Session 27 lab guide: Terraform foundations

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal. Commands and outputs below come from real runs (Terraform 1.17.2, AWS provider 6.73, local provider 2.9.1). Your IDs, IPs and timings will differ.

| | |
|---|---|
| **Time** | Part A 15 min, Part B 30 min, Part C 30 min, Part D 20 min |
| **Cost** | Part A is free. Parts B to D can run on a **free local AWS emulator** (no account, no cost) or on **real AWS**, where one `t3.micro` building costs a few cents per hour, if your account is outside the free tier. Always run the destroy at the end. |
| **Skill check** | You can read the plan symbols from the script (`+ - ~ -/+`) and you did Session 14 (VPC, subnet, gateway, route table). |

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  campus/        versions.tf  provider.tf  variables.tf  main.tf  outputs.tf  .gitignore
  emulator/      provider.tf        <- swap this in for practice without an AWS account
```

## Before you start

Install Terraform from the official HashiCorp docs and check it:

```bash
terraform version
```

Expected: `Terraform v1.5` or newer (we ran `v1.17.2`). No Terraform install? You can run any command below as `docker run --rm -v "$PWD":/work -w /work hashicorp/terraform:1.17.2 <command>`.

---

## Part A: the whole workflow with no cloud (Episode 1)

**Goal:** run `init`, `plan`, `apply`, `destroy` once on something that cannot hurt you, and read a plan.

```bash
mkdir tf-hello && cd tf-hello
```

Create `main.tf`:

```hcl
resource "local_file" "hello" {
  filename = "${path.module}/hello.txt"
  content  = "Hello, Atithi"
}
```

```bash
terraform init
terraform plan
```

Expected from `init`: `Installed hashicorp/local v2.9.1 (signed by HashiCorp)` (your version may be newer) and `Terraform has been successfully initialized!`. Expected from `plan` (shortened):

```
  # local_file.hello will be created
  + resource "local_file" "hello" {
      + content              = "Hello, Atithi"
      + filename             = "./hello.txt"
      + id                   = (known after apply)
      ...
    }

Plan: 1 to add, 0 to change, 0 to destroy.
```

```bash
terraform apply        # type yes
cat hello.txt          # Hello, Atithi
ls                     # hello.txt  main.tf  terraform.tfstate  .terraform ...
```

Expected: `Apply complete! Resources: 1 added, 0 changed, 0 destroyed.` Notice the new file `terraform.tfstate`. That is the register of what Terraform built.

### Deliberate break 1: change the content

Edit `main.tf`, change `"Hello, Atithi"` to `"Hello, Atithi Hotels"`, and run `terraform plan`.

Expected: `# local_file.hello must be replaced`, the `-/+` symbol, and `Plan: 1 to add, 0 to change, 1 to destroy.` For this resource a changed `content` cannot be edited in place, so Terraform replaces it. Run `terraform apply` to accept.

### Deliberate break 2: delete the thing by hand

```bash
rm hello.txt
terraform plan
```

Expected: `# local_file.hello will be created` and `Plan: 1 to add, 0 to change, 0 to destroy.` Terraform compared the register with reality and found the file missing. Run `terraform apply` to bring it back.

### Cleanup

```bash
terraform destroy      # type yes
ls                     # main.tf  terraform.tfstate  terraform.tfstate.backup
```

Expected: `Destroy complete! Resources: 1 destroyed.` and `hello.txt` is gone.

### Check yourself

- [ ] You can say what each of the four commands did.
- [ ] You saw `-/+` (replace) and `+` (create) and can say why each appeared.
- [ ] You can explain why `terraform plan` knew the file was missing.

---

## Part B: the campus in code (Episodes 2 and 4)

**Goal:** build the Session 14 public wing from a master plan: a VPC, a subnet cut with `cidrsubnet`, an internet gateway, a route table, a door guard (security group) and a building. Ten resources, one `apply`.

Note on the count: the script says to expect "seven to ten resources". We got **10**, because the AWS provider (6.x) models each security-group rule as its own resource: seven main resources plus the SSH rule plus two web rules.

### Choose your target

**Option 1: real AWS.** Credentials come from the environment, never from the code:

```bash
export AWS_PROFILE=your-profile        # or AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY
aws sts get-caller-identity            # must show your account before you go on
```

**Option 2: free practice, no AWS account.** Run a local AWS emulator and point Terraform at it:

```bash
docker run -d --name floci -p 4566:4566 floci/floci:latest
cp emulator/provider.tf campus/provider.tf     # run from lab_files/; replaces the real provider block
```

The emulator is good enough for every command in this guide, but it is not real AWS. For example, the building has no real public IP (`public_ip = ""`), so you cannot SSH to it. Switch to real AWS for the final check if you want to see it.

### Build

```bash
cd campus
terraform init
terraform fmt
terraform validate
```

Expected: `Installed hashicorp/aws v6.x`, `Success! The configuration is valid.` and no output from `fmt` (the files are already formatted).

Find your public IP and supply it. For the emulator any value works:

```bash
curl -s https://checkip.amazonaws.com
echo 'my_ip_cidr = "YOUR.IP.HERE/32"' > terraform.tfvars      # this file is git-ignored
```

```bash
terraform plan -out=tfplan
```

Read the plan with the three questions from Scene 4 of the script (what is created, what is destroyed, what is changed). Expected:

```
  # aws_instance.web will be created
  # aws_internet_gateway.gw will be created
  # aws_route_table.public will be created
  # aws_route_table_association.public will be created
  # aws_security_group.web will be created
  # aws_subnet.public will be created
  # aws_vpc.main will be created
  # aws_vpc_security_group_ingress_rule.ssh will be created
  # aws_vpc_security_group_ingress_rule.web["443"] will be created
  # aws_vpc_security_group_ingress_rule.web["80"] will be created

Plan: 10 to add, 0 to change, 0 to destroy.
```

```bash
terraform apply tfplan
terraform output
terraform plan
```

Expected: `Apply complete! Resources: 10 added, 0 changed, 0 destroyed.`, `subnet_cidr = "10.0.1.0/24"` (that is `cidrsubnet("10.0.0.0/16", 8, 1)`), and the second `plan` says `Terraform has compared your real infrastructure against your configuration and found no differences`. On real AWS `public_ip` shows an address too; with a `key_name` set (an existing key pair, optional) you can `ssh ubuntu@<public_ip>`.

### Deliberate break: bad building size

Run `terraform plan -var instance_type=m5.24xlarge`.

Expected: the `validation` message `Use t3.micro, t3.small or t3.medium.` and no plan. Your own rule stopped an expensive mistake before any cloud call.

### Check yourself

- [ ] You can name the one resource that decides the subnet range, and what number it produced.
- [ ] The second `plan` showed no differences.
- [ ] You can explain why `for_each` created two web rules (80 and 443) from one block.

---

## Part C: the register, drift, rename (Episode 3)

**Goal:** read the state, see drift, and rename a resource without destroying it. Keep the Part B resources running.

```bash
terraform state list
terraform state show aws_instance.web
```

Expected: eleven entries (ten resources plus `data.aws_ami.ubuntu`), then the building's recorded attributes: ID, AMI, IP and more. Read the state, never edit it by hand. A password variable would also appear here in plain text, which is why state is never committed.

### Deliberate break 1: drift

Change the building's `Owner` tag outside Terraform. On real AWS use the console (EC2, select the instance, Tags, edit). On the emulator:

```bash
ID=$(terraform state show aws_instance.web | awk '/^ +id +=/{gsub(/"/,"",$3);print $3}')
aws --endpoint-url http://localhost:4566 ec2 create-tags --resources $ID --tags Key=Owner,Value=someone-else
```

(If you have no `aws` CLI, skip to the rename and read the drift section in the script.)

```bash
terraform plan
```

Expected:

```
  ~ resource "aws_instance" "web" {
      ~ tags = {
          ~ "Owner" = "someone-else" -> "atithi"
        }
  ...
Plan: 0 to add, 1 to change, 0 to destroy.
```

`terraform apply` puts the tag back to what the code says. The code is the truth.

### Deliberate break 2: rename a resource

Edit `main.tf` and `outputs.tf`: change `aws_instance.web` to `aws_instance.app` (the resource label and the output reference). Run `terraform plan`.

Expected:

```
  # aws_instance.app will be created
  # aws_instance.web will be destroyed
    # (because aws_instance.web is not in configuration)
Plan: 1 to add, 0 to change, 1 to destroy.
```

A new name looks like a new building: Terraform wants to destroy the old one and create another. Do not apply.

### Fix: a `moved` block

Add to `main.tf`:

```hcl
moved {
  from = aws_instance.web
  to   = aws_instance.app
}
```

```bash
terraform plan
```

Expected: `# aws_instance.web has moved to aws_instance.app` and `Plan: 0 to add, 0 to change, 0 to destroy.` Run `terraform apply` once so the register learns the new name.

### Protect the register

`campus/.gitignore` already contains:

```
*.tfstate
*.tfstate.*
.terraform/
terraform.tfvars
```

Commit `.terraform.lock.hcl` (it pins provider versions) but never the state or `terraform.tfvars`.

### Check yourself

- [ ] You saw `~ ... -> ...` for drift and can say who "won".
- [ ] You saw a rename plan as destroy plus create, and `0 to change` after `moved`.
- [ ] You know which of the four lines in `.gitignore` protects secrets, and why.

---

## Part D: destroy and the dependency picture (Episode 4)

**Goal:** see that Terraform tears things down in the reverse order of how they depend on each other.

Optional first. If you have Graphviz (`dot`) installed:

```bash
terraform graph | dot -Tpng > graph.png
```

Without Graphviz `terraform graph` still prints the picture as text (it starts with `digraph G {`). The PNG needs the `dot` tool.

```bash
terraform destroy
```

Type `yes`. Expected, in this order (shortened): the route table association and the three security-group rules go first, then the building, then the route table and gateway, then the door guard and subnet, and the VPC last:

```
aws_route_table_association.public: Destruction complete
aws_vpc_security_group_ingress_rule.ssh: Destruction complete
aws_instance.app: Destruction complete after 10s
aws_security_group.web: Destruction complete
aws_subnet.public: Destruction complete
aws_vpc.main: Destruction complete
Destroy complete! Resources: 10 destroyed.
```

The VPC is last because everything else lives inside it.

### Cleanup (do not skip)

```bash
terraform state list        # expect no output
```

- Real AWS: open the EC2 and VPC consoles, check the region you used, and confirm no instance, VPC, internet gateway or security group named for this lab remains. Also check Elastic IPs.
- Emulator: `docker rm -f floci`.
- Local files you can delete: `tfplan`, `terraform.tfvars`, `.terraform/`.

### Check yourself

- [ ] `terraform state list` shows nothing.
- [ ] You can explain why the VPC was destroyed last.
- [ ] The cloud console (or emulator) shows nothing left.

---

## Final checklist for Session 27

- [ ] Part A: the no-cloud workflow, with replace and create plans read correctly
- [ ] Part B: ten resources built with one apply, a second plan clean
- [ ] Part C: drift seen, rename fixed with `moved`, `.gitignore` in place
- [ ] Part D: destroy done in reverse order, nothing left running

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `No value for required variable my_ip_cidr` | No default on purpose | Create `terraform.tfvars` or use `-var my_ip_cidr=...` |
| `Error acquiring ...` or `credentials` errors on real AWS | Wrong profile or none | `aws sts get-caller-identity`, then `export AWS_PROFILE=...` |
| `InvalidAMIID` or no AMI found | Region has no matching image | Check `var.region`, or search the AMI name in that region |
| Plan wants to replace the building after a rename | Missing `moved` block | Add it before applying |
| `Instance cannot be destroyed` | A `prevent_destroy` setting | Remove it deliberately, then retry |
| `dot: command not found` after `terraform graph` | Graphviz not installed | Skip the PNG, the text graph is enough |

## What we did not test

Part A and the Terraform commands were run with Terraform 1.17.2 in Docker. Parts B to D ran against a local AWS emulator (floci 2.4.0), not real AWS. We did not run: a real `apply` and SSH to a real public IP, real AWS billing, the real AMI search result, or `key_name` with a real key pair. The real-AWS provider file was only checked with `init`, `validate` and `fmt`. Check your own AWS billing page for true costs.

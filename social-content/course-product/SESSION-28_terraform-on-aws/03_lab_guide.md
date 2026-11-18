# Session 28 lab guide: Terraform on AWS

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet to keep next to your terminal. Commands and outputs below come from real runs (Terraform 1.17.2, AWS provider 6.73, Trivy 0.76.2, actionlint, a local AWS emulator). Your IDs and timings will differ.

| | |
|---|---|
| **Time** | Part A 35 min, Part B 30 min, Part C 20 min, Part D 30 min |
| **Cost** | Everything can run on a **free local AWS emulator**: no account, no cost. On **real AWS**, Parts A and B cost almost nothing (one S3 bucket, six VPC and subnet objects are free), but do not add a NAT gateway, load balancer or database to Part C unless you accept hourly charges. Always run the cleanup. |
| **Skill check** | You finished Session 27 (init, plan, apply, destroy, `moved`) and Session 14 (VPC and CIDR). |

Starter files are in `lab_files/` next to this guide:

```
lab_files/
  state_demo/     main.tf  backend.tf.example  backend.hcl.example  backend.hcl.emulator
  modules_demo/   versions.tf  provider.tf  main.tf  modules/network/{main,variables,outputs}.tf
  scan_demo/      bad/main.tf  good/main.tf
  ci/             terraform-ci.yml
  emulator/       provider.tf        <- swap in for the emulator
```

## Before you start

- Terraform 1.10 or newer (the lock-file lock needs 1.10+): `terraform version`.
- Real AWS: `aws sts get-caller-identity` must show your account.
- Emulator instead (free): `docker run -d --name floci -p 4566:4566 floci/floci:latest`. The AWS CLI commands below then need `--endpoint-url http://localhost:4566` and fake credentials: `export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1`.

---

## Part A: the register in a warehouse, with a lock (Episode 1)

**Goal:** move Terraform's state from your laptop into a versioned, private S3 bucket, and watch a second `apply` get refused while the first is running.

### A1. Bootstrap the bucket (once, by hand)

The bucket that holds state cannot be created by the same Terraform that stores state in it, so you make it first. Choose a globally unique name, and replace `YOUR_REGION`.

```bash
BUCKET=YOUR-STATE-BUCKET
aws s3api create-bucket --bucket $BUCKET --region YOUR_REGION \
  --create-bucket-configuration LocationConstraint=YOUR_REGION
aws s3api put-bucket-versioning --bucket $BUCKET --versioning-configuration Status=Enabled
aws s3api put-public-access-block --bucket $BUCKET \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
aws s3api put-bucket-encryption --bucket $BUCKET \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'
```

**Gotcha:** in `us-east-1` leave out the whole `--create-bucket-configuration` line. Passing a `LocationConstraint` there is an error. Expected from `create-bucket`: a JSON `Location` line. The other three commands print nothing when they work.

### A2. Apply once locally

```bash
cd lab_files/state_demo
terraform init
terraform apply          # type yes; takes about 25 seconds
ls
```

Expected: `Apply complete! Resources: 1 added`, and a local `terraform.tfstate`. The resource is a harmless `terraform_data` with a 25-second `sleep`, so you have time to test the lock later.

### A3. Move the register into the bucket

The backend block cannot use variables, so keep the bucket name in a separate file. Copy `backend.hcl.example` to `backend.hcl` and fill it in (emulator users: copy `backend.hcl.emulator` instead), then enable the backend:

```bash
cp backend.tf.example backend.tf
terraform init -migrate-state -backend-config=backend.hcl
```

Terraform asks whether to copy the existing state: answer `yes`. Expected: `Successfully configured the backend "s3"!`

```bash
aws s3 ls s3://$BUCKET/network/
```

Expected: one line, `terraform.tfstate` (about 700 bytes). The register now lives in the warehouse.

### A4. Deliberate break: two applies at once

You need two terminals in `state_demo/`.

Terminal 1:

```bash
terraform apply -replace=terraform_data.slow     # type yes; it now runs for 25 seconds
```

Within those 25 seconds, Terminal 2:

```bash
aws s3 ls s3://$BUCKET/network/      # you will also see terraform.tfstate.tflock
terraform apply
```

Expected in Terminal 2:

```
Error: Error acquiring the state lock

Error message: operation error S3: PutObject, https response error
StatusCode: 412, ... api error PreconditionFailed: At least one of the pre-conditions you specified did not hold
Lock Info:
  ID:        58fc0ed1-cc83-fa6e-21c6-47c3790d70c7
  Path:      <bucket>/network/terraform.tfstate
  Operation: OperationTypeApply
  Who:       root@4e8a8a126dec
  Version:   1.17.2
  Created:   2026-11-18 05:26:50 +0000 UTC
```

Read the `Who` and `Created` lines: they tell you who is applying and since when. When Terminal 1 finishes, the `.tflock` object disappears by itself and a new `apply` works. Note: this lock needs no DynamoDB table (`use_lockfile = true`, Terraform 1.10+).

If a lock is ever stuck after a crashed run, `terraform force-unlock LOCK_ID` removes it. Use it only when you are sure nobody is applying.

### A5. The warehouse remembers: versions and a backup

```bash
aws s3api list-object-versions --bucket $BUCKET --prefix network/terraform.tfstate \
  --query 'Versions[].[VersionId,IsLatest,Size]' --output text
```

Expected: several rows, one per save, newest marked `True`. That is your undo history for the register. A safe backup you can keep outside S3:

```bash
terraform state pull > backup.json
```

(`backup.json` is real state: never commit it.)

### Cleanup for Part A

```bash
terraform destroy         # destroys the sleep resource
```

A versioned bucket cannot be removed with `aws s3 rb --force`: you will get `BucketNotEmpty` because old versions remain. Delete every version first:

```bash
aws s3api list-object-versions --bucket $BUCKET \
  --query '[Versions,DeleteMarkers][][].[Key,VersionId]' --output text |
while read k v; do [ -n "$k" ] && aws s3api delete-object --bucket $BUCKET --key "$k" --version-id "$v" >/dev/null; done
aws s3api delete-bucket --bucket $BUCKET
aws s3 ls                 # the bucket should be gone
```

Also delete `backup.json`, `backend.hcl`, and `backend.tf` if you will not continue.

### Check yourself

- [ ] You moved the state with `init -migrate-state` and saw the object in the bucket.
- [ ] You triggered the lock error and can say what `Who` and `Created` tell you.
- [ ] You can explain why the state bucket is created by hand first.

---

## Part B: one standard design, two campuses (Episode 2)

**Goal:** call one module twice (`dev` and `staging`), with different address ranges, and see that a rename inside the module needs a `moved` block.

```bash
cd lab_files/modules_demo
```

Emulator users: `cp ../emulator/provider.tf provider.tf`.

```bash
terraform init
terraform validate
terraform plan
```

Expected from `init`: `- dev in modules/network` and `- staging in modules/network`. The plan lists six resources, two VPCs and four subnets:

```
  # module.dev.aws_subnet.public[0] will be created
  # module.dev.aws_subnet.public[1] will be created
  # module.dev.aws_vpc.this will be created
  # module.staging.aws_subnet.public[0] will be created
  # module.staging.aws_subnet.public[1] will be created
  # module.staging.aws_vpc.this will be created
Plan: 6 to add, 0 to change, 0 to destroy.
```

```bash
terraform apply
```

Expected: `dev_subnets` and `staging_subnets` outputs, two subnet IDs each. One module, two campuses. We deliberately left out the NAT gateway because it bills by the hour.

### Deliberate break 1: a bad CIDR

```bash
terraform plan -var staging_cidr=banana
terraform plan -var staging_cidr=10.20.0.0
```

Expected for both: `Error: Invalid value for variable` and your message `cidr must be a valid CIDR such as 10.10.0.0/16.` The module's `validation` stopped the mistake before any cloud call. Note what it does not check: it will accept `staging_cidr=10.10.0.0/16`, which **overlaps** dev, because the rule only tests the format. Overlap checking is your Session 14 rule, so do it by hand or add a check.

### Deliberate break 2: rename inside the module

In `modules/network/main.tf` and `outputs.tf` change `aws_vpc.this` to `aws_vpc.campus` (the label and every reference). Then:

```bash
terraform plan
```

Expected: `Plan: 6 to add, 0 to change, 6 to destroy.` The VPC rename looks like a different VPC, and since the subnets belong to it they are replaced too. Do not apply.

### Fix: a `moved` block inside the module

Add to `modules/network/main.tf`:

```hcl
moved {
  from = aws_vpc.this
  to   = aws_vpc.campus
}
```

```bash
terraform plan
```

Expected: two lines, `module.dev.aws_vpc.this has moved to module.dev.aws_vpc.campus` and the same for `staging`, then `Plan: 0 to add, 0 to change, 0 to destroy.` Because the `moved` block lives inside the module, every environment that calls it moves its own copy. Apply it once so the state learns the new name.

### Cleanup for Part B

```bash
terraform destroy         # expect: Destroy complete! Resources: 6 destroyed.
```

### Check yourself

- [ ] One module produced two campuses with different CIDRs.
- [ ] You saw the validation message, and you know what it cannot catch.
- [ ] You saw `6 to destroy` without `moved` and `0 to change` with it.

---

## Part C: a whole environment, plan only (Episode 3)

**Goal:** compose an environment from modules, feed it sizes from `terraform.tfvars`, and learn to read the plan before spending anything.

What we tested: the network module and the composition pattern from Part B (two calls, per-environment inputs, outputs). What we did not run: a full dev environment with the ALB, compute and database modules. Resource syntax for those pieces (RDS with `manage_master_user_password`, `multi_az`, `deletion_protection`, an ALB, target group, listener, launch template, autoscaling group and a NAT gateway with an Elastic IP) passed `terraform validate`, but we did not plan or apply them as one environment. Treat the steps below as an exercise.

1. Create `envs/dev/` with a `main.tf` that calls four modules: `network`, `alb`, `compute`, `database`. Wire them with outputs, for example `module.network.public_subnet_ids` into the `alb` and `compute` modules.
2. Put the sizes in `envs/dev/terraform.tfvars`: smallest instance size, `multi_az = false`, one NAT gateway.
3. Give it its own backend key, `dev/terraform.tfstate`, in the bucket from Part A (`-backend-config` as before).
4. Run **only** `terraform plan`.

Read the plan with the three questions from Session 27: does anything get destroyed, is anything changed that you did not expect, and does the count match your estimate? Write down how many resources of each kind will be created.

**Do not `apply` unless you accept the cost.** A NAT gateway, an application load balancer and an RDS instance each bill by the hour, even when idle. If you do apply: set a budget alert first (Session 15), use the smallest sizes, and run `terraform destroy` immediately after, then check the console for leftovers.

### Check yourself

- [ ] Your plan lists what will be created and you can explain the count.
- [ ] `terraform.tfvars` and state are not in Git.
- [ ] You know which three resources cost money while idle.

---

## Part D: the master plan gets a CI check (Episode 4)

**Goal:** make a pull request fail when it opens SSH to the world.

### D1. See the scan fail and pass, locally

Trivy checks Terraform files for risky settings. `scan_demo/bad/main.tf` has SSH open to `0.0.0.0/0`; `good/main.tf` limits it to one address.

```bash
trivy config --severity HIGH,CRITICAL --exit-code 1 lab_files/scan_demo/bad
echo "exit: $?"
```

(No Trivy install? `docker run --rm -v "$PWD/lab_files/scan_demo/bad":/src aquasec/trivy:0.76.2 config --severity HIGH,CRITICAL --exit-code 1 /src`.)

Expected:

```
Failures: 1 (HIGH: 1, CRITICAL: 0)
AWS-0107 (HIGH): Security group rule allows unrestricted ingress from any IP address.
 main.tf:10
exit: 1
```

Now the fixed version:

```bash
trivy config --severity HIGH,CRITICAL --exit-code 1 lab_files/scan_demo/good
echo "exit: $?"
```

Expected: a report with `0` misconfigurations and `exit: 0`. The only difference between the two folders is `0.0.0.0/0` against a single `/32` address. Note that Trivy downloads its rules (a "checks bundle") the first time, so the first run needs internet.

### D2. Put it in a pull request check

Copy `lab_files/ci/terraform-ci.yml` to `.github/workflows/terraform-ci.yml` in a repo that holds your Terraform code. It runs on every pull request that changes a `.tf` file:

```yaml
- uses: actions/checkout@v7
- uses: hashicorp/setup-terraform@v4
- run: terraform fmt -check -recursive
- run: terraform init -backend=false
- run: terraform validate
- uses: aquasecurity/trivy-action@v0.36.0
  with: { scan-type: config, severity: "HIGH,CRITICAL", exit-code: "1" }
```

What we checked: the file passes `actionlint` with no findings, and the Trivy scan behaves as above. What we did not run: the workflow on GitHub itself. Before you rely on it, look up the latest release of each action and pin a tag or, better, a full commit SHA, as in Session 20.

Test it as a student: on a branch, put `0.0.0.0/0` on port 22 in your Terraform, push, open a pull request, and watch the check fail. Change it to your own IP with `/32`, push again, and watch it pass.

Then make it required: in the repository settings add a branch protection rule for `main` and tick "Require status checks to pass", choosing the `check` job (Session 19).

Optional, for real AWS: add a `plan` step that signs in with an OIDC role instead of stored keys. We did not test that here.

### Check yourself

- [ ] The bad folder exited 1 and the good folder exited 0.
- [ ] You can explain what `-backend=false` does in CI (no state access, so no secrets).
- [ ] The check is required on `main`.

---

## Final checklist for Session 28

- [ ] Part A: state in a versioned bucket, lock error seen, bucket and versions cleaned up
- [ ] Part B: two campuses from one module, bad CIDR rejected, rename fixed with `moved`
- [ ] Part C: an environment plan read and counted (apply only if you accept the cost)
- [ ] Part D: CI scan fails on open SSH and passes after the fix
- [ ] No state files, `terraform.tfvars`, `backend.hcl` or `backup.json` in Git

## If something goes wrong

| Symptom | Likely cause | What to do |
|---|---|---|
| `InvalidLocationConstraint` in `us-east-1` | You passed a `LocationConstraint` | Remove `--create-bucket-configuration` in `us-east-1` |
| `BucketNotEmpty` on delete | Old versions remain | Use the version-deleting loop in Part A cleanup |
| `Error acquiring the state lock` | Another apply is running, or a crash left a lock | Read `Who` and `Created`; `force-unlock` only if nobody is applying |
| `Backend configuration changed` | Backend block or settings changed | `terraform init -reconfigure` or `-migrate-state` |
| Plan wants to replace everything after a rename | Missing `moved` block | Add it before applying |
| Trivy first run is slow or fails offline | It downloads its rules | Run once with internet |

## What we did not test

Parts A, B and D ran against a local AWS emulator (floci) and in Docker, not against real AWS. We did not run: real S3 behaviour and billing, the `us-east-1`-versus-other-region error in practice, a full ALB, compute and database environment (Part C), the CI workflow on GitHub, OIDC, or the Trivy action itself (we ran the Trivy CLI). Check your own AWS billing for true costs.

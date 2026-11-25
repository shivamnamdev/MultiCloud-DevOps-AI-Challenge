# Session 08 lab guide: AWS and EC2 basics

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **Read this first: what was tested, and what was not.**
> This session is mostly about the AWS **console** (account, MFA, budget, the launch wizard, CloudShell) and a **real server** you log into. We have no AWS account and no way to click in the console for you. So:
> - **Not tested at all:** root user and MFA, budgets and the free tier, the console screens, CloudShell, a real EC2 instance, real SSH into it, real public IPs, real prices, the metadata service (IMDSv2), cloud-init and nginx started by user data.
> - **Tested against an emulator:** the same AWS **API** calls from the command line (regions, zones, key pairs, security groups, launching with user data, stop, start, terminate, Elastic IP, leftovers) on `floci`, a free program that imitates AWS on your own machine. It is good for learning the commands and the shape of the answers. It is **not** AWS: its lists of regions, images and prices are its own.
> - **Tested for real, locally:** the four SSH error messages, in a practice container.
> Use this guide to practise the commands for free, then do the console parts on a real account, and tell us where reality differs.

> **Update, tested on real AWS (ap-south-1, one t3.micro, Ubuntu, same day deleted).** The following were run for real and matched the script:
> - Key pair, security group from your own IP only, launch with `userdata.sh`: nginx was serving the page about 36 seconds after the instance was running. SSH worked with the key.
> - **IMDSv2:** no token gives `401`, with a token it answers, and with no role attached the role path gives `404`.
> - **SSH errors:** revoking port 22 in the security group gives `Operation timed out` within seconds (exit 255); re-authorizing fixes it. With nginx stopped, `curl` to port 80 gives **connection refused** (curl exit 7), while a port the security group does not allow (8080) just **hangs** (curl exit 28). Refused means "someone answered: nobody home"; timed out means "the guard dropped you".
> - **Stop/start:** the public IP is gone while stopped and **a new one is assigned on start**.
> - **Elastic IP:** it stayed the same through stop/start; after release the instance got a new ordinary public IP. Unattached Elastic IPs and public IPv4 addresses bill, so release it.
> - Cleanup with `_lab_tools/aws/aws_cleanup_atithi.sh --yes` then `aws_leftovers.sh` printed "NOTHING LEFT". The whole lab cost a few cents of the credits.
> Still not tested: root user and MFA, budgets, CloudShell.

> **Update 2: the console launch wizard, tested for real (24 November 2026, ap-south-1, one t3.micro, deleted the same evening).** A person clicked through the wizard while the AWS CLI checked every result. The run sheet is `DEMO_RUNSHEET.md`; the read-only checker is `_lab_tools/aws/demo_s8_verify.sh`. What the console showed, which the script does not say:
> - **The preselected image is Amazon Linux 2023, not Ubuntu.** If you want Ubuntu, pick it. Then the login user is `ubuntu`, not `ec2-user`. We used Ubuntu 26.04 (amd64), which suits `t3.micro` (see the architecture trap in C3).
> - **The key pair is created at once, in its dialog, and the private key downloads once.** Clicking Launch before the dialog is done is the usual mistake. Create the key pair first, in the Key pair section. Default type is RSA with `.pem`; ED25519 is offered. `chmod 400` the file.
> - **The SSH source defaults to "Anywhere" (`0.0.0.0/0`).** Change it to **My IP**. The security group we got had SSH from our own `/32` and HTTP from anywhere, exactly like the CLI version in C2.
> - **Console launches differ from the CLI in two defaults:** the instance metadata hop limit is **2** (the CLI default is 1), and the root volume is **not encrypted**. In Advanced details set the metadata version to **V2 only** (this is `HttpTokens=required`). Verified: no token gives `401`, a token works.
> - **User data runs only on first boot.** Ours was saved with the last line wrong (it printed text instead of writing the page), so nginx showed its **default welcome page**. Editing the user data afterwards would not have re-run it. We fixed it on the server over SSH with `echo ... | sudo tee /var/www/html/index.html`, and the Atithi page appeared. Lesson: after launch, read the saved user data back (`describe-instance-attribute --attribute userData`) before you blame nginx.
> - **Stop and start:** the public IP changed (`3.109.208.236` to `13.201.189.152`), while the private IP, the disk and our hand-written page stayed.
> - **Cleanup:** terminating the instance deleted the 8 GiB volume with it (`DeleteOnTermination` true). The security group and key pair are separate and must be deleted by hand. `aws_leftovers.sh` then printed "NOTHING LEFT".
> - **Not recorded:** EC2 Instance Connect from the console (its result was not reported back).

| | |
|---|---|
| **Time** | Part A 20 min, Part B 20 min, Part C 40 min, Part D 40 min |
| **Cost** | Free on the emulator. On real AWS everything you launch bills while it exists: use the cleanup list at the end. |
| **Skill check before you start** | Sessions 3 to 7: Linux, SSH keys, the shell. Docker installed. |

## Ticket ATITHI-008: first server for the booking site

**Client asks (Mrs. Mehta):** "Pehla server aaj hi live ho jaye. Bas ek simple page dikhna chahiye, aur sirf meri team andar ja sake."

**Constraints:** region `ap-south-1`; type `t3.micro` (x86 image, see C3); SSH only from your own IP (`/32`), never `0.0.0.0/0`; web (port 80) open to everyone; IMDSv2 required; tag `Project=atithi-lab` and a `Name`; everything deleted at the end.

**Deliver:** a running Ubuntu server with nginx installed through user data (`lab_files/userdata.sh`), and the page `Atithi Hotels: Book Now` in a browser at `http://PUBLIC_IP`.

**Done when** (run each check; "expected" is what we saw on real AWS):

| Check | How | Expected |
|---|---|---|
| Page is live | `curl -s http://PUBLIC_IP` | `<h1>Atithi Hotels: Book Now</h1>...` |
| SSH works from your IP | `ssh -i key.pem ubuntu@PUBLIC_IP` | you are logged in |
| SSH is not open to the world | `aws ec2 describe-security-groups --group-ids SG` | port 22 source is your `/32` only |
| IMDSv2 enforced | metadata address without a token | `401`; with a token it answers |
| Tags present | `aws ec2 describe-instances --instance-ids ID` | `Name` and `Project` tags |

**Trap we hit on a real run:** the saved user data had a wrong last line, so nginx showed its **default welcome page**. User data runs **only on first boot**, so editing it later does not rerun it. Read it back with `aws ec2 describe-instance-attribute --instance-id ID --attribute userData` before blaming nginx.

The handover note you write at the end is at the bottom of Part D.

## Before you start

You need Docker. The AWS command line runs inside a Docker image, so you do not install it. Files are in `lab_files/`.

```bash
chmod +x lab_files/emulator/*
lab_files/emulator/start.sh
export PATH="$PWD/lab_files/emulator:$PATH"
aws --version
```

`start.sh` creates a Docker network, starts the emulator (`floci/floci:latest`, we saw `floci 2.4.0`), and runs `aws sts get-caller-identity`. The folder's `aws` is a tiny wrapper: it runs `amazon/aws-cli` in a container (we saw `aws-cli/2.41.0`) pointed at the emulator, with fake keys, so every `aws ...` command below runs against the practice AWS. Output files go into your current folder. **Real AWS is never touched.** On a real account, you would instead install the AWS CLI and run `aws configure`.

---

## Part A: the safe lease (Episode 1)

This part is console work, so there is nothing to run. Do the script's checklist on your own account: MFA on root, a monthly budget with an 80% email alert, Cost Explorer on, one Region chosen, an account alias. Keep a screenshot of each step.

One thing you **can** run is "who am I", which the next part uses a lot:

```bash
aws sts get-caller-identity
aws sts get-caller-identity --output text
```

On the emulator: `Account` `000000000000` and `Arn` `arn:aws:iam::000000000000:root`. (On real AWS it is a 12-digit account number and, if you are the owner, the root ARN: a reminder that you should not be doing daily work as it.)

---

## Part B: the map, and CLI habits (Episode 2)

### B1. Regions and zones

```bash
aws ec2 describe-regions --query "Regions[].RegionName" --output text
aws ec2 describe-availability-zones --region ap-south-1 --query "AvailabilityZones[].ZoneName"
aws ec2 describe-availability-zones --region ap-south-1 --query "AvailabilityZones[].[ZoneName,State]" --output table
```

On the emulator we got 17 region names, and `ap-south-1a`, `ap-south-1b`, `ap-south-1c` (all `available`). The script asks you to count Mumbai's towers: three. **That number is the emulator's, and so is the list of regions.** The real Mumbai region has three zones to our knowledge, but we did not check it. Run the same two commands in CloudShell on a real account and compare.

### B2. `--output`, `--query` and profiles

You saw `--output text` and `--output table` above, and `--query` with JMESPath (`Regions[].RegionName` picks one field from every item). Profiles keep several sets of keys apart. To keep the practice keys out of your real `~/.aws`, we pointed the CLI at files in the current folder:

```bash
D() { docker run --rm --network awslab -v "$PWD:/work" -w /work \
  -e AWS_CONFIG_FILE=/work/.awsconfig -e AWS_SHARED_CREDENTIALS_FILE=/work/.awscreds \
  -e AWS_ENDPOINT_URL=http://floci-lab:4566 -e AWS_PAGER= amazon/aws-cli "$@"; }
D configure set aws_access_key_id AKIAEXAMPLEKEY --profile atithi
D configure set aws_secret_access_key examplesecret --profile atithi
D configure set region ap-south-1 --profile atithi
D configure list --profile atithi
D sts get-caller-identity --profile atithi --output text
cat .awsconfig
```

(On your own machine you would just type `aws configure --profile atithi`, and the files would be `~/.aws/config` and `~/.aws/credentials`.) Expected: `region : ap-south-1 : config-file`, the keys masked as `****************EKEY` and `****************cret`, and the identity answer. `.awsconfig` held `[profile atithi]` and `region = ap-south-1`. The keys go into a **separate** credentials file, not the config file. `export AWS_PROFILE=atithi` would make all commands use it.

**Check yourself:**

- [ ] You can say what `--query "Regions[].RegionName"` does.
- [ ] You know where a profile's keys are stored.

---

## Part C: the first building (Episode 3, API version)

### C1. The key pair

```bash
aws ec2 create-key-pair --key-name atithi-key --query KeyMaterial --output text > atithi-key.pem
head -c 40 atithi-key.pem; echo
chmod 400 atithi-key.pem
aws ec2 describe-key-pairs --query 'KeyPairs[].[KeyName,KeyType]' --output text
aws ec2 create-key-pair --key-name atithi-key
```

Expected (ours): `-----BEGIN RSA PRIVATE KEY-----`, then `atithi-key  rsa`, and the second create failed with `InvalidKeyPair.Duplicate`. Like the console, the private key is shown **once**, at creation. The `--query KeyMaterial --output text > file` pattern is how you keep it. **Do not commit the `.pem`.**

### C2. The door guard

```bash
SG=$(aws ec2 create-security-group --group-name web-sg --description "web door guard" --query GroupId --output text)
aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 22 --cidr 203.0.113.7/32
aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 describe-security-groups --group-ids $SG --query 'SecurityGroups[0].[IpPermissions[].[FromPort,IpRanges[0].CidrIp],IpPermissionsEgress[].IpProtocol]'
```

Expected (ours): inbound `22 from 203.0.113.7/32` and `80 from 0.0.0.0/0`, and outbound `-1` (all protocols, so everything is open by default). `203.0.113.7` is a documentation address standing in for "my IP"; on real AWS use your own (`curl -s https://checkip.amazonaws.com`) followed by `/32`. That is what the console's "My IP" does. Anything not listed inbound is closed. **That the guard is stateful (replies are allowed back automatically) we did not test: the emulator does not filter traffic.**

### C3. Launch with user data, tags and IMDSv2

`lab_files/userdata.sh` is the script's user data.

```bash
aws ec2 describe-images --query 'Images[].[ImageId,Name,Architecture]' --output text
aws ec2 run-instances --image-id ami-ubuntu2404 --instance-type t3.micro --key-name atithi-key ...
```

The first launch **failed**, which is a useful lesson: `The architecture 'arm64' of the specified image does not match the architecture supported by instance type 't3.micro'.` `ami-ubuntu2404` is an ARM image, and `t3` is an x86 family. ARM instances are the `g` types (`t4g`). The emulator also lists x86 images, such as `ami-ubuntu2404-amd64`. So either use an x86 image with `t3.micro`, or an ARM image with `t4g.micro`. We did the second:

```bash
SG=$(aws ec2 describe-security-groups --group-names web-sg --query 'SecurityGroups[0].GroupId' --output text)
I=$(aws ec2 run-instances --image-id ami-ubuntu2404 --instance-type t4g.micro --key-name atithi-key \
  --security-group-ids $SG --user-data file://lab_files/userdata.sh \
  --metadata-options HttpTokens=required,HttpEndpoint=enabled \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=atithi-web-1},{Key=Owner,Value=asha}]' \
  --query 'Instances[0].InstanceId' --output text)
aws ec2 describe-instances --instance-ids $I \
  --query 'Reservations[0].Instances[0].[InstanceType,State.Name,KeyName,PrivateIpAddress,Placement.AvailabilityZone,MetadataOptions.HttpTokens]' --output text
aws ec2 describe-instance-attribute --instance-id $I --attribute userData --query UserData.Value --output text | base64 -d
```

Expected (ours): `t4g.micro running atithi-key 172.31.32.10 us-east-1c required`; the tags `Name atithi-web-1` and `Owner asha`; and the user data script printed back (it is stored base64-encoded). `HttpTokens=required` is what **forces IMDSv2** (the two-step token call of the script). **The emulator did not give the instance a public IP address** (`PublicIpAddress` was `None`), and it did not run the user data. So we did not see the page, nginx, or the metadata service. On real AWS, put `--associate-public-ip-address` or use a public subnet, then open `http://PUBLIC_IP`, and read `/var/log/cloud-init-output.log` if it does not show.

### C4. Buying options and sizes

Reading, no commands: On-Demand, Savings Plans or Reserved, Spot (can be taken back with two minutes' notice, per the script), and Dedicated Hosts. We could not check any prices or the free tier from here; read your own pricing page.

**Check yourself:**

- [ ] You can explain why the first launch failed and how to fix it.
- [ ] You can read `t4g.micro` as family, generation and size.
- [ ] You know which flag forces IMDSv2.

---

## Part D: inside the building, and the cleanup (Episode 4)

### D1. The four SSH answers (tested for real, locally)

We built the practice container from Session 5/6 (an Ubuntu 24.04 machine with an SSH server) and made each mistake on purpose, from inside it, against itself and against an address nobody answers:

| What we did | What SSH said |
|---|---|
| `ssh -i key ubuntu@10.255.255.1` (nothing answers there, packets just vanish) | `ssh: connect to host 10.255.255.1 port 22: Connection timed out` |
| `ssh -o IdentitiesOnly=yes -i wrong.pem ubuntu@localhost` | `ubuntu@localhost: Permission denied (publickey,password).` |
| `ssh -p 2222 ... localhost` (nothing listens on 2222) | `ssh: connect to host localhost port 2222: Connection refused` |
| a key file with mode `644` | `WARNING: UNPROTECTED PRIVATE KEY FILE!` |
| the right key, the wrong user (`ec2-user` on an Ubuntu machine) | `ec2-user@localhost: Permission denied (publickey,password).` |
| the right key and user | `logged in as ubuntu` |

Our practice machine also allows passwords, so its message said `(publickey,password)`. A real EC2 instance allows keys only and says `(publickey)`. The meanings are the script's: timed out means the road is blocked (security group, wrong IP), permission denied means you reached the door with the wrong key or user, and refused means nobody is listening.

### D2. Stop, start, Elastic IP, terminate

```bash
aws ec2 stop-instances --instance-ids $I
aws ec2 describe-instances --instance-ids $I --query 'Reservations[0].Instances[0].State.Name' --output text
aws ec2 start-instances --instance-ids $I
A=$(aws ec2 allocate-address --query AllocationId --output text)
aws ec2 associate-address --instance-id $I --allocation-id $A
aws ec2 stop-instances --instance-ids $I; aws ec2 start-instances --instance-ids $I
aws ec2 describe-instances --instance-ids $I --query 'Reservations[0].Instances[0].PublicIpAddress' --output text
aws ec2 terminate-instances --instance-ids $I
aws ec2 describe-instances --instance-ids $I --query 'Reservations[0].Instances[0].State.Name' --output text
```

What we saw: `stopping`, `stopped`, then `pending`, `running`. With an Elastic IP associated, the instance kept `203.0.113.1` across a stop and start. `terminate-instances` gave `shutting-down` and then `terminated`. We did **not** see the "public address changes after stop and start" part of the script, because the emulator gave no public address without an Elastic IP.

The instance's root volume was `8` GB, `in-use`, with `DeleteOnTermination True`. After terminating, `describe-volumes` listed no volumes. But `describe-addresses` still listed the Elastic IP: `eipalloc-... 203.0.113.1` with no instance. **It is still allocated until you release it**, and on real AWS an unattached Elastic IP bills. That is the script's "check for leftovers".

### D3. Clean up

```bash
aws ec2 release-address --allocation-id $A
aws ec2 delete-key-pair --key-name atithi-key
aws ec2 delete-security-group --group-id $SG
rm -f atithi-key.pem
docker rm -f floci-lab
```

On real AWS, also check EC2's **Volumes** and **Elastic IPs** pages, and **Snapshots**, in every Region you used. We did not test the console flow.

**Check yourself:**

- [ ] You can match each SSH message to its cause.
- [ ] You saw an Elastic IP stay allocated after its instance was terminated.
- [ ] Your emulator and your key file are gone.

---

### Handover note for ATITHI-008 (write it before you delete anything)

```
Ticket:        ATITHI-008 First server
Built:         1 x t3.micro (Ubuntu), nginx via user data, security group with 22 from my /32 and 80 from anywhere
Reach it:      http://<public-ip> (web); ssh -i key.pem ubuntu@<public-ip> from my IP only
On stop/start: the public IP changes (we saw 3.109.208.236 become 13.201.189.152); private IP and disk stay
Cost running:  <hourly price of t3.micro from the pricing page> + 8 GiB gp3 disk; our whole lab ran about one hour: cents
Undo:          terminate the instance (its volume goes with it), delete the security group and the key pair, delete the .pem
Known gaps:    one server only (no failover), HTTP only (no TLS), set up by hand (Terraform, Session 27)
Next ticket:   ATITHI-009 staff access with IAM (Session 9)
```

The **Known gaps** line is the thread to the next session: it names what a later session fixes.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `Could not connect to the endpoint URL` | Emulator not running | `lab_files/emulator/start.sh` |
| `InvalidParameterValue ... architecture` | ARM image on an x86 type (or the reverse) | Match them: `t3` with x86, `t4g` with ARM |
| `InvalidKeyPair.Duplicate` | The key name exists | Choose a new name or delete the old key |
| `UNPROTECTED PRIVATE KEY FILE` | Key mode too open | `chmod 400 key.pem` |
| `Connection timed out` on real AWS | Security group, wrong IP, or no public address | Check the three, from the outside in |
| `Permission denied (publickey)` | Wrong key or user | `ubuntu` on Ubuntu, `ec2-user` on Amazon Linux |

## What we did not test

- **Most of the AWS console:** root and MFA, the budget alert, Cost Explorer, tags for cost allocation, CloudShell, and EC2 Instance Connect. (The launch wizard was tested, see Update 2.)
- **A real instance:** SSH into it, the page served by nginx from user data, `cloud-init-output.log`, the metadata service (IMDSv2) and its two-step call, a public IPv4 address, and what happens to it on stop and start.
- **Real AWS's** region and zone counts, instance types, prices, free tier, and "My IP".
- **Spot and Savings Plans** (reading only).
- **The shared responsibility model** in practice (an idea, not a command).

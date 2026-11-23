# Session 01 lab guide: cloud and DevOps foundations

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal.

> **What was tested, and what was not.**
> Run for real on macOS (Apple Silicon), Docker 29 and a real AWS account (read-only calls): the region and Availability Zone homework, container versus VM timing, and a look at the billing alerts. The cloud-offer facts (free plans, trial credits, DORA) were checked against current public sources in November 2026.
> **Not tested:** installing VirtualBox and booting a VM. We did not install a hypervisor on the test machine. Instead we checked Oracle's release notes and give you the Apple-Silicon rule below, and we tested the **container** half of the story, which needs no install beyond Docker.

| | |
|---|---|
| **Time** | Part A 20 min, Part B 25 min, Part C 20 min, Part D 20 min |
| **Cost** | Free. Part B only reads from AWS. No account at all is needed for Parts A, C and D. |
| **Skill check before you start** | None. A laptop, a browser, and the wish to start. |

---

## Part A: servers, virtualization, and your first VM (Episode 1)

### A1. Feel the over-provisioning problem (pen and paper, 10 min)

Atithi's website gets **1,000 visitors on a normal day** and **50,000 on sale day, two days a year**. One server handles 1,000.

1. How many servers must you **own** to survive sale day? (50.)
2. For how many days a year are 49 of them idle? (363.)
3. What fraction of the servers' capacity is used on average? Work it out: `(363 x 1 + 2 x 50) / (365 x 50)` = **about 2.5 percent**.

That number, not the price of one server, is the pain. Renting for two days is the cloud's answer.

### A2. The VM lab (the script's lab) and the Apple-Silicon rule

On **Windows or an Intel Mac**: install VirtualBox, create a VM with **2 GB RAM and 20 GB disk**, attach an Ubuntu Server ISO and boot it.

On an **Apple-Silicon Mac** (M-series): VirtualBox 7.1 and later does run there, but **only with ARM (arm64) guests**. Oracle's release notes say x86-64 VMs on an Arm host are not supported. So download the **arm64** Ubuntu Server ISO, not the usual `amd64` one. If you pick the wrong ISO the VM will not boot, and the error will not say why. Free alternatives that work on Apple Silicon are UTM and Multipass; we did not test those either.

**Not tested here** (no hypervisor was installed). The numbers 2 GB and 20 GB are the script's choice; Ubuntu Server boots in less, but keep them.

### A3. See virtualization without installing anything (tested)

Your Mac or PC is already using it if you run Docker Desktop. On a Mac:

```bash
sysctl -n kern.hv_support                  # 1 = the CPU/OS offer hardware virtualization to apps
docker info --format '{{.Name}} kernel={{.KernelVersion}} cpus={{.NCPU}} mem={{.MemTotal}}'
```

We saw `1` and `docker-desktop kernel=...-linuxkit cpus=12 mem=8.3 GB`: Docker is running a small hidden **Linux VM** with its own kernel and its own share of CPU and RAM. That is the building-engineer idea from the script, on your own laptop.

### A4. Container versus VM, measured (tested)

```bash
docker pull -q alpine
for i in 1 2 3; do /usr/bin/time -p docker run --rm alpine true 2>&1 | grep real; done
docker run --rm alpine uname -sr           # Linux 7.0.14-linuxkit  (the Docker VM's kernel)
uname -sr                                  # Darwin 27.0.0          (your Mac's kernel)
docker run --rm alpine sh -c 'head -2 /etc/os-release'    # Alpine Linux
```

Our result: **0.14 to 0.18 seconds** to start a container, and **a different operating system than the host** (Alpine, on a Linux kernel, on a Mac). A full VM takes tens of seconds to minutes to boot, because it starts its own whole operating system. The container **shares the kernel** of whatever runs it, which is the "truck inside a building, sharing its management office" picture. On a Mac the kernel being shared is the hidden VM's, which is why `uname` differs. On Linux it would match the host.

---

## Part B: cloud, regions and Availability Zones (Episode 2)

### B1. The homework: count the Availability Zones in your nearest region

No account? Open the provider's "global infrastructure" page and read the table. With an AWS account and the CLI (read-only, free):

```bash
aws ec2 describe-availability-zones --region ap-south-1 \
  --query "AvailabilityZones[].[ZoneName,ZoneId]" --output text
```

Tested results (November 2026, one real account):

| Region | AZs | What we saw |
|---|---|---|
| `ap-south-1` (Mumbai) | 3 | `ap-south-1a`, `1b`, `1c` |
| `ap-southeast-1` (Singapore) | 3 | |
| `eu-west-1` (Ireland) | 3 | |
| `us-east-1` (N. Virginia) | **6** | `1a` to `1f` |
| `ap-south-2` (Hyderabad) | (blocked) | see below |

**Trap 1: not every region is switched on.** Asking about a region your account has not enabled does not say "region disabled". It says:

```
AuthFailure: AWS was not able to validate the provided access credentials
```

`aws ec2 describe-regions --all-regions --query "Regions[].[RegionName,OptInStatus]" --output text` shows `not-opted-in` for Hyderabad on our account. By default this account had **17** regions enabled. Opt-in regions must be enabled in the account settings first, and a region you do not use costs nothing but is one more place to audit.

**Trap 2: zone names are not the same for everyone.** `ap-south-1a` on your account can be a different physical zone than `ap-south-1a` on your friend's. In Mumbai, our account mapped `1a` to `aps1-az1`, `1b` to `aps1-az3`, and `1c` to `aps1-az2`. If two accounts must agree on a physical zone, compare the **Zone ID** (`aps1-az1`), not the name.

### B2. Pick the region with the three reasons

For each of these, write which region you would pick and the reason (guests near, law about where data may live, cost): an Indian hotel booking app; a European bank; a hobby project that only you use.

### B3. Free offers: what is true now (checked November 2026)

| Provider | Offer | Watch for |
|---|---|---|
| AWS | New accounts choose a **Free plan** or a **Paid plan**. Both start with about **$100 in credits** and you can earn about **$100 more** by trying services. The **Free plan ends after six months or when credits run out**, and then the account is **closed**, not billed (you can upgrade to recover it for a limited time). The **Paid plan** has no six-month cap and bills normally after credits. | AWS's own FAQ pages disagree on when credits expire (6 or 12 months). Read the **Credits page in your billing console** for your own date. Joining AWS Organizations moves a Free plan to Paid. |
| Google Cloud | **$300** trial credit for **90 days**, no automatic charge; resources stop when it ends unless you upgrade. | The exact end date of your own trial is shown on your billing page; note it in your calendar on day one. |
| Azure | A free account with credit and some free services is offered. | **We could not confirm the current numbers**, so the script avoids quoting them. Open Microsoft's page on the day you sign up. |

Rules never change: read the page on the day you sign up, put a card on the account only knowing what happens at the end, and set the alert below **on day one**.

### B4. The day-one billing alert (read what exists; tested)

The script says "billing alert on day one". On our AWS account two budgets already existed. You can inspect yours (no cost):

```bash
ACC=$(aws sts get-caller-identity --query Account --output text)
aws budgets describe-budgets --account-id $ACC \
  --query "Budgets[].[BudgetName,BudgetLimit.Amount,BudgetLimit.Unit,TimeUnit]" --output text
aws budgets describe-notifications-for-budget --account-id $ACC --budget-name "My Zero-Spend Budget" \
  --query "Notifications[].[NotificationType,ComparisonOperator,Threshold]" --output text
```

We saw a **Zero-Spend Budget**: limit 1 USD per month, alert when **actual cost is greater than 0.01 USD**, and a second monthly 1 USD budget alerting at actual **85 percent and 100 percent** and **forecast over 100 percent**. The zero-spend one is the best first alert for a learner: the **first cent** of unexpected cost sends you an email.

**Do not print your account number** in screenshots or public logs. We hid it in the output above. (A real leak of this kind is in Session 20.)

Creating a budget from the console or CLI was **not tested** in this session; use the console's "Zero spend budget" template and enter your own email.

---

## Part C: DevOps, and your own release (Episode 3)

### C1. Fill this table for any project you know (10 min, notebook)

| Question | Your answer |
|---|---|
| Who deploys? | |
| How long from "code is done" to "guests see it"? | |
| What broke last time? | |
| Releases per month | |
| Releases that needed an **unplanned fix** afterwards | |
| How long did the fix take? | |

Put a star on every step done **by hand**. That starred list is your automation backlog, and the course will automate one of them with you.

### C2. Turn it into the five DORA numbers

DORA's research now names **five** measures (the fifth, deployment rework rate, was added in the 2024 report):

| # | Measure | Group | Your number |
|---|---|---|---|
| 1 | Deployment frequency (how often you release) | speed | releases per month: |
| 2 | Change lead time (code ready to live) | speed | hours or days: |
| 3 | Failed deployment recovery time (how fast you fix a bad release) | speed (as grouped by some sources) | |
| 4 | Change failure rate (releases that cause a problem) | stability | bad releases / all releases: |
| 5 | Deployment rework rate (unplanned releases forced by a production problem) | stability | unplanned / all: |

Worked example from DORA's own illustration: 10 deployments, 3 of them unplanned because of an incident, so rework rate = 3/10 = **30 percent**.

The **grouping of recovery time** is described differently by different sources (speed versus stability). Do not argue it in an interview; say what each measure means.

---

## Part D: setup and the map (Episode 4)

### D1. Setup checklist (do it now)

```bash
git --version          # Git installed? (Session 16 uses it)
code --version         # VS Code installed? (any editor is fine)
docker --version       # needed from Session 21 on; install early
aws --version          # needed from Session 8 on
```

Also: a GitHub account (Session 16B), a mail address you check, and **no cloud account yet unless you are ready for Session 8**. A cloud account is free to open but you now know what to read first (Part B3) and what to set up first (B4).

### D2. Draw the map

On one page draw Atithi Hotels' three zoom levels and put every tool you have heard of into the right one (Linux, Bash, Python; AWS, Azure, GCP, Terraform, Ansible; Git, Jenkins, GitHub Actions, Docker, Kubernetes, Prometheus, Grafana). You will redraw it at the end of the course and see the difference.

---

## Clean up

Nothing to delete. If you booted a VM in A2, shut it down and remove it in VirtualBox (it keeps a 20 GB disk file until you do).

## If something goes wrong

| You see | Cause | Fix |
|---|---|---|
| The VM shows a black screen or `no bootable medium` | wrong ISO architecture (amd64 on an Apple-Silicon Mac) | use the **arm64** ISO |
| VirtualBox says virtualization is not enabled (Windows/Intel) | VT-x / AMD-V off in BIOS | enable it in BIOS/UEFI |
| `AuthFailure` when listing a region's zones | region not enabled on your account | enable it in account settings, or choose another region |
| `docker: command not found` or daemon errors | Docker Desktop not installed/running | install and start it |
| `aws: command not found` | CLI not installed | install the AWS CLI (Session 8) |
| `describe-budgets` access denied | your IAM user lacks Billing/Budgets permission | ask the account owner; no need to widen yours for this session |

## What we did not test

Installing VirtualBox and booting a VM (any host), UTM and Multipass, creating a budget alert, signing up for Azure or GCP, the exact current Azure offer, and any provider's console screens.

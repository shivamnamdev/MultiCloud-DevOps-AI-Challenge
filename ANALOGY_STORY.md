# One story for the whole Multi-Cloud DevOps course

Every session in this course is taught as part of one story: you are building and running a hotel chain. A single hotel explains Linux well but has no place for Git, Jenkins, Docker, Kubernetes or Terraform. A hotel *company* that rents buildings, designs its services at head office and ships them to every building has a place for all of them.

- This file is the master story and the locked vocabulary.
- [ANALOGY_SESSION_MAP.md](ANALOGY_SESSION_MAP.md) gives the story beat for each of the 33 sessions in [SYLLABUS_BLUEPRINT.md](SYLLABUS_BLUEPRINT.md).

## The story in one telling

You are starting a hotel company. It is called **Atithi Hotels**, from "Atithi Devo Bhava": the guest comes first, exactly as the end user does in software.

1. **The old way (on-premise).** You buy land, construct a building, install generators and hire guards. It takes months and a lot of money before the first guest arrives.
2. **The landlords (cloud).** Three giant real-estate companies (AWS, Azure, GCP) have already built hotel-ready towers in every major city. You rent a building by the hour and return it when you are done. They own the land, the power and the maintenance.
3. **Running one building (Linux).** A rented building is empty. You need a management system inside it: staff with ID cards, locks on every room, a floor layout, logbooks, a security gate and an opening routine every morning. That management system is Linux.
4. **The campus (AWS services).** One building becomes a gated campus: a public wing and a private wing, a main gate, a warehouse, a records office, CCTV and a marshal who sends guests to whichever building is free.
5. **Head office (Git, Jenkins).** What guests actually enjoy are the hotel's services: the restaurant, the booking desk, the spa. Designers at head office write the blueprints for these services. A blueprint vault keeps every revision, and an automated workshop turns each new revision into a finished unit and delivers it.
6. **Trucks and autopilot (Docker, Kubernetes, monitoring).** Each service is built as a sealed service truck (picture a food truck) that parks at any building, plugs into its power and water, and works identically everywhere. An operations command keeps the right number of trucks running across all buildings, and a control room watches everything.
7. **Building from documents (Terraform, Ansible, scripting).** You stop renting and furnishing by hand. A master plan document builds a whole campus, and a checklist crew sets up every building the same way.
8. **More landlords and an assistant (Azure, AI).** You expand to a second and third landlord. The business is the same and only the names change. A very well-read assistant joins every team.
9. **Grand openings (projects).** You open complete hotels end to end, using everything above.

## The three zoom levels

Every topic in the course lives at exactly one level. This is what stops the analogies from clashing.

| Zoom level | What you see | Course topics |
|---|---|---|
| **1. Inside one building** | Staff, rooms, locks, logbooks, gate | Linux, Bash |
| **2. The rented campus** | Buildings, wings, gates, warehouse, landlord's office | AWS, Azure, GCP, Terraform, Ansible |
| **3. Head office** | Blueprints, workshop, trucks, operations command, control room | Git, Jenkins, Docker, Kubernetes, Prometheus/Grafana, AI |

Roads connect all three: the internet.

## Two rules that keep it consistent

1. **Staff are not guests.** Linux users and cloud IAM users are *staff*. End users of the website are *guests*. Guests never get a staff ID card. They only arrive by road, get served and leave.
2. **In this world, buildings can be photocopied.** A furnished building can be cloned in minutes and demolished at no cost. This is the one "magic" rule, and it is the reason cloud, containers and infrastructure-as-code exist.

## The map, module by module

### Foundation (sessions 01–02)

| Concept | In the story |
|---|---|
| On-premise | Buying land and constructing your own hotel |
| Cloud provider | Landlord who rents ready buildings by the hour |
| Virtualization, hypervisor | One huge tower divided into many independent hotels by a building engineer |
| IaaS / PaaS / SaaS | Rent an empty building / rent a fully serviced banquet hall / just book a room |
| Dev vs Ops | Designers at head office vs the people running the hotels, blaming each other |
| DevOps | One team, with a conveyor between design and operations and guest feedback flowing back |
| AI co-programmer | A well-read assistant beside every designer and operator; fast, but its work is always reviewed |
| Prompt engineering | How to brief that assistant: role, context, task, format |

### Roads: networking basics (used everywhere)

| Concept | In the story |
|---|---|
| Internet | The road network |
| IP address | Street address of a building |
| DNS | The directory or maps app that turns a hotel name into an address |
| Routers, hops | Junctions on the way |
| Port | A numbered door on the building (22 staff entrance, 80 public entrance, 443 secured public entrance) |
| SSH | Private staff entrance opened with a personal key |
| Firewall | Guard at the gate with a list of who may enter |
| NAT / masquerade | All outgoing letters carry the hotel's one public address; the dispatch desk remembers who sent what (the same desk as the NAT gateway in the cloud sessions) |
| Port forwarding | The operator at the gate passing a caller on door 22 to the right room inside |

### Linux: managing one building (sessions 03–06, including 05B)

| Concept | In the story |
|---|---|
| Kernel | Core management office that controls power, water and lifts; nobody touches the machines directly |
| Shell, commands | The desk where you give instructions, in the house language |
| root | General manager with the master key |
| sudo user | Duty manager who may borrow the master key, with every use written in a log |
| System user (e.g. `apache`) | Uniformed service staff with one job, who never log in as people |
| `/etc/passwd`, `/etc/shadow` | Staff register, and the locked safe of key codes |
| Groups (primary, secondary) | Home department, plus extra department access cards |
| Password policy (`chage`) | ID card expiry and renewal rules |
| Directories and files | Rooms, and the cupboards inside them |
| Permissions `rwx` for user/group/others | Each lock has three rings (owner, department, everyone) and three rights (look, change, operate) |
| umask | The default lock setting on every new room |
| SUID | A machine that lets any staff member act with the owner's authority for that one job (changing your own key) |
| SGID | Whatever is placed in a department room belongs to the department |
| Sticky bit (`/tmp`) | Shared lost-and-found: anyone can leave things, only the owner can remove their own |
| Directory layout (`/etc`, `/home`, `/var/log`, `/tmp`) | Admin office, staff quarters, logbook room, lost-and-found |
| Process, PID, parent/child | A work order in progress, its token number, a supervisor delegating |
| Services, `systemd` | Always-on departments, and the shift supervisor who starts them in order |
| Boot process | Morning opening routine: power check, pick the playbook, management wakes, supervisor opens departments |
| Logs, `logrotate` | Logbooks, and archiving old registers weekly |
| Packages (`yum`, `apt`) | Procurement from an approved vendor catalogue |
| CPU / RAM / swap | Workforce / work desks / slower overflow room when desks are full |
| Disk, partition | Raw floor space, and the walls that divide it |
| File system (`ext4`, `xfs`) | The shelving system that makes an empty hall usable |
| Mount, `/etc/fstab` | Fitting a door from the corridor to that hall; the "open these doors every morning" list |
| LVM | Banquet halls with movable walls: pool the floor space, carve halls, resize them for events |
| firewalld zones | Security levels for different gates (`block` says "sorry", `drop` stays silent) |
| SELinux | A second security layer: staff and rooms both wear labelled badges, and the labels must match even if you hold the key |
| Apache `httpd` | The front-of-house service that serves visitors on door 80 |
| Bash script, cron | A written slip of instructions for the desk; a routine on a timetable |

### AWS: the rented campus (sessions 08–15)

| Concept | In the story |
|---|---|
| Region, Availability Zone | A city, and separate towers in it with independent power |
| Edge location | A small pickup counter in many cities, so guests collect a brochure close to home |
| EC2 instance, instance type | A rented building, and its size |
| AMI | A fully furnished model hotel you can photocopy |
| Key pair | The building key handed over when the lease is signed |
| EBS, snapshot | An attachable storeroom that outlives the building; a photograph of its contents |
| Auto Scaling | Opening extra identical buildings in wedding season and closing them after |
| Load balancer, health checks | Marshal at the main gate sending guests to buildings that answer "we are open" |
| IAM users, groups, policies | Your company's staff at the *landlord's* office, and written permission letters |
| IAM role | A temporary duty badge that a person or a building can wear |
| Root account, MFA | The owner who signed the lease; a second lock |
| S3 bucket, object | An endless off-site warehouse, and labelled boxes in it (you store things there, you do not live there) |
| S3 static website | A warehouse with a display window: brochures shown with no staff on duty |
| RDS | A records office run by the landlord's professionals: backups and standby copies handled for you |
| VPC, CIDR | Your gated campus, and the range of room numbers allotted to it |
| Public / private subnet | Road-facing wing / back-office wing with no direct road access |
| Internet gateway, route table | Campus main gate; direction boards in each wing |
| NAT gateway | Dispatch desk that lets the back office send couriers out while no outsider can visit |
| Security group / NACL | Guard at a building door (remembers who went out) / guard at the wing entrance (checks both ways, numbered rules) |
| Peering, VPN | Skywalk between two campuses; private tunnel from your old hotel |
| CloudWatch, alarms | Landlord's meters and CCTV; an alarm that phones the manager |
| Lambda | On-call freelancer who appears when a bell rings, does one job and leaves; paid per job |
| SNS / SQS | Public-address announcement / token queue so no request is lost |

Linux users versus IAM users now makes sense: one is staff *inside a building*, the other is staff *at the landlord's office* who can rent or demolish buildings.

### Git, GitHub, Jenkins: head office (sessions 16–20)

| Concept | In the story |
|---|---|
| Code | Blueprints of the hotel's services |
| Git, commit | The blueprint register; a signed, dated revision |
| Working directory, staging area, repository | Drawing table; approval tray; the register itself |
| Branch, merge, conflict | A draft copy; approving it into the master; two designers moved the same wall |
| HEAD, `.git` | The "you are here" pin; the register's back room |
| Stash, detached HEAD, cherry-pick | The designer's own drawer; the archive reading room (look, do not draw); lifting one page from a draft into the master |
| Reset, revert | Removing your own unshared pages; a correction slip added to the register, with no page torn out |
| Fork, tag, branch protection | An outside contractor's own copy of the vault; a release stamp; a lock on the master |
| GitHub / GitLab | The central vault at head office where all designers sync |
| Pull request | "Chief architect, please review before this goes into the master" |
| Build (Maven), artifact | Workshop tools that gather materials and fabricate the unit; the finished unit |
| Tests | Quality inspection |
| Jenkins | Workshop foreman running an automated conveyor |
| Webhook | The vault rings the workshop bell when a new revision arrives |
| Pipeline, stages, Jenkinsfile | The conveyor, its stations, and the conveyor instructions kept with the blueprint |
| Plugins | Attachments the foreman can add |
| Master / agent | Foreman assigns the work; workbenches do the heavy lifting |
| CI / CD | Every revision is fabricated and inspected at once / delivered and installed without anyone carrying it |

### Docker, Kubernetes, monitoring (sessions 21–26)

| Concept | In the story |
|---|---|
| Container | A sealed service **truck** (picture a food truck) with its own equipment and stock. It carries no generator and no water tank: it parks in a building's courtyard, plugs into the building's power and water, and works the same everywhere |
| VM vs container | A whole separate building with its own management vs a truck that borrows the building's power, water and management |
| Image | The master truck design, from which identical trucks roll out |
| Dockerfile | The truck's fit-out sheet |
| Registry (Docker Hub, ECR) | The depot that holds truck designs |
| Port mapping | Connecting the truck's serving window to a building door |
| Volume | Trucks get replaced, so valuables go in the building's locker room |
| Microservices | A truck park: many small trucks, each doing one job |
| Kubernetes | The chain's **operations command**: you state "always keep 5 coffee trucks running" and it makes reality match |
| Cluster, node | All buildings under one command; one building and its courtyard of parking bays |
| API server, etcd, scheduler, controllers | Command reception, master ledger, allocation officer, supervisors who compare ledger with reality |
| kubelet | Resident manager in each building |
| Pod | A parking bay in the courtyard, holding one truck (or a tight pair) |
| Deployment, rolling update | A standing order; replacing trucks one at a time and rolling back if guests complain |
| Service | One permanent extension number that reaches whichever trucks are alive |
| Ingress | Concierge at the grand entrance who reads where the guest wants to go |
| Namespace | Separate wings for dev, staging and production |
| ConfigMap / Secret | Notice board / sealed envelope in the safe |
| HPA, self-healing | More trucks when queues grow; a broken truck is replaced automatically |
| Rescheduling | A truck is never driven from one building to another; a fresh one is sent from the depot |
| Helm | A franchise kit: one command installs a full set of trucks from a settings form |
| GitOps, Argo CD | A **site supervisor** who lives at the campus and, every few minutes, compares the standing orders kept in the **config vault** (a Git repo of manifests) with what is really there, and fixes any difference. Rolling back means putting back an older page in the vault |
| GKE / EKS / AKS | The landlord runs the operations command for you |
| Prometheus, exporters | Inspector who reads every meter every few seconds; the meters themselves |
| Alertmanager | Alarm desk that calls the right duty manager |
| Grafana | The wall of live screens in the control room |

### Terraform, Ansible, scripting (sessions 07, 27–29)

| Concept | In the story |
|---|---|
| Terraform | The campus master plan written as a document; a contractor builds exactly what it says |
| `plan` / `apply` / `destroy` | "Show me what will change" / build it / demolish cleanly |
| State file | The as-built register of what actually exists |
| Provider | An authorised contractor for each landlord (same plan language, different contractor) |
| Module | A reusable standard design |
| Drift | Someone changed a building by hand without updating the plan |
| Ansible | The setup crew that furnishes and configures every building identically |
| Inventory, playbook, task | List of buildings; the checklist; one step |
| Role | A reusable checklist binder |
| Agentless | The crew enters by the staff entrance, does the work and leaves; nobody stays behind |
| Idempotent | Running the checklist twice changes nothing the second time |
| Python, boto3 | A trained operations officer who can do what a slip cannot, and their phone line to the landlord's office |

How they sit together: Terraform builds the campus, Ansible sets up the buildings, Jenkins delivers new trucks, Kubernetes keeps them running, Prometheus watches.

### Azure, AI and the projects (sessions 30–33)

| Concept | In the story |
|---|---|
| Azure, GCP | Other landlords: same kinds of buildings, different names |
| Azure DevOps (Boards, Repos, Pipelines, Test Plans, Artifacts) | A landlord's ready-made head office: planning wall, vault, conveyor, inspection, parts store |
| AI agent | The assistant, now given tools and limited authority to act on its own |
| MCP server | A standard service hatch through which the assistant can safely use the hotel's tools |
| AIOps | The assistant watches the control room and logbooks and gives first response |
| AI API (Gemini) | An outside expert on the phone, paid per question |
| MLOps | A "smart recommendation" service whose trained brain is packaged, shipped and re-trained like any truck |
| GitHub Actions | A conveyor built into the vault itself |
| DevSecOps (SonarQube, Trivy) | Inspection built into the conveyor: a blueprint inspector and an X-ray for finished truck designs |

## Hotel services: what each truck carries

The truck is the packaging. The **hotel service** is what is inside it. Every microservice is named after a real hotel service, so "service" in software and "service" in a hotel mean the same thing to a learner. Use these in sessions 21–26 and 31–33.

**Naming rule:** say "the reservations truck", never "the reservations department". "Department" is already taken (Linux groups, systemd).

| Service in the course | Hotel service it carries |
|---|---|
| `bookings-service` | Reservations desk |
| `rooms-service` | Housekeeping and room status |
| Orders service (food) | Restaurant and room service |
| Payments service | Billing and cashier |
| Background worker (emails, reports) | Laundry round and night audit |
| Frontend / website | The lobby display and booking kiosk screen |

**How services behave** (use one only where the session already teaches the technical idea):

| Software idea | Real hotel moment |
|---|---|
| Queue (SQS, Kafka) | The kitchen order ticket on the kitchen rail: the guest orders, the kitchen cooks at its own pace, nothing is lost |
| Calling a service by name | Housekeeping dials the reservations extension, not a person (Kubernetes Service) |
| Idempotency, safe retry | Two clerks key in the same booking; the reservation number makes the second one change nothing |
| Cache | The availability board at the front desk; if stale, you get overbooking |
| Circuit breaker, timeout | Laundry is down, so the front desk stops promising same-day laundry instead of making every guest wait |
| Request tracing | One request slip with one number passes through every service, so you can see where it stalled |
| Batch job, `cron`, backup | Night audit: closes the day's books at a fixed hour |
| Rate limit | A token system at a busy counter |

**How services are run and changed**

| Software idea | Real hotel moment |
|---|---|
| Rolling update | Renovating floor by floor while the hotel stays open |
| Blue/green | A new wing opens, then guests are moved over at once |
| Canary | A new menu offered to a few tables first |
| Rollback | Back to the old menu or the old rooms |
| Autoscaling, HPA | Extra banquet staff in wedding season |
| Resource requests and limits | Rooms guaranteed to a group booking, and a hall's fire-code maximum |
| OOMKilled | The fire marshal clears an overcrowded hall |
| Readiness probe | Housekeeping marks a room "ready" before a guest is sent up |
| Liveness probe | The duty manager's hourly walk-round: anything not responding is replaced |
| Alert, on-call, runbook | The duty manager's phone, and the written procedure beside it |
| Staging, tests | The test kitchen: the chef tastes before the menu goes live |
| Job (Kubernetes) | One-time wedding set-up |
| CronJob | The daily laundry round or night audit |
| DaemonSet | One guard at every entrance of every building |
| StatefulSet | Room 101 keeps its number and its guest history |
| Taints, node affinity | The spa only on the ground floor; the VIP floor only for VIP guests |
| Security scan | The fire and hygiene inspection |
| Least privilege (IAM) | A guest key card opens only their own room and the gym |

**Not used, on purpose:** "concierge" stays on Ingress, and "assistant" stays AI-only. A housekeeping trolley is not used for a container: the truck is already in every script.

## The thread you can repeat in every session: one guest's journey

1. A guest looks up "Atithi Hotels" in the directory and gets the address (DNS).
2. They drive over public roads and junctions (internet, hops).
3. They reach the campus main gate (internet gateway).
4. The marshal sends them to a building that is open (load balancer).
5. The door guard checks the list and lets them in by door 443 (security group, port).
6. A truck serves them (the application in a container).
7. The truck asks the records office in the private wing for their booking (database) and fetches photos from the warehouse (S3).
8. The control room sees the whole visit on its screens (monitoring).

Each session can open with "where are we on this journey, and at which zoom level?"

## Where the story should stop

- Use it for *why a tool exists and where it sits*. Teach commands, YAML and CIDR arithmetic directly.
- Software copies itself for free; real buildings do not. Rule 2 covers this, and it is worth saying aloud once.
- If a comparison needs more than one sentence of explanation, drop it for that concept.

## Coverage check

Every one of the 33 sessions has a home: 01–02 foundation, 03–06 zoom level 1, 07 the bridge from level 1 to level 2, 08–15 zoom level 2, 16–26 zoom level 3, 27–29 back to zoom level 2, 30 the second landlord, 31–33 grand openings and the assistant.

No story term stands for two things: building = server, truck = container, blueprint = code, landlord = cloud provider, staff = system users, guest = end user, assistant = AI only.

## Settled choices

- The company is Atithi Hotels.
- A container is a **truck**. It is introduced as a food truck; each microservice is a truck carrying one real hotel service (reservations, housekeeping, restaurant, billing, laundry). See "Hotel services" above.
- Added 2026-11-17: hotel services are named as trucks ("the billing truck"), never as "departments".
- Related words: truck design (image), fit-out sheet (Dockerfile), depot (registry), serving window (port), parking bay (Pod), truck park (microservices).

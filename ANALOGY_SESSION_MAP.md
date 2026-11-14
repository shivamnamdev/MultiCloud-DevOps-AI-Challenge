# Story beat for each session

This file applies the hotel-chain story in [ANALOGY_STORY.md](ANALOGY_STORY.md) to the 33 sessions in [SYLLABUS_BLUEPRINT.md](SYLLABUS_BLUEPRINT.md). Use the story words exactly as written there, so one word never stands for two things.

- **Zoom** says where the session sits: 1 = inside one building, 2 = the rented campus, 3 = head office.
- **Story beat** is what happens in the company during that session. It can be the opening of episode 1.
- **New story words** are the terms the session introduces. Later sessions reuse them without re-explaining.

## Foundation

| # | Session | Zoom | Story beat | New story words |
|---|---|---|---|---|
| 00 | the-story-of-atithi-hotels | All | The whole story told once before any tool is taught: one guest's eight-stop journey, the three zoom levels, and where every later session sits. No commands. | previews the main words; each is taught properly in its own session |
| 01 | cloud-and-devops-foundations | All | You start Atithi Hotels. You compare buying land with renting from a landlord, see one tower divided into many hotels, and choose between an empty building, a serviced hall and a booked room. Designers and operators stop blaming each other and share a conveyor. | landlord, building, staff, guest, head office, conveyor |
| 02 | ai-co-programmer-for-devops | 3 | A well-read assistant joins every team. You learn to brief it, to give it tools with limited authority, and to inspect its work before it reaches a guest. | assistant, brief |

## Inside one building

| # | Session | Zoom | Story beat | New story words |
|---|---|---|---|---|
| 03 | linux-foundations | 1 | You get the keys to your first rented building. You meet the core management office, the instruction desk and the floor layout, and you enter by the staff entrance. | management office (kernel), desk (shell), rooms and cupboards, staff entrance (SSH) |
| 04 | linux-users-permissions-ssh | 1 | You hire staff and lock the rooms: the staff register and the safe, departments, three-ring locks, a personal key for the staff entrance, procurement, and the morning opening routine. | general manager (root), duty manager (sudo), department (group), three-ring lock, procurement |
| 05 | linux-sysadmin-and-troubleshooting | 1 | The manager's daily round, and then a bad day. You switch departments on and off, read the live operations board, check storeroom space and the roads, and go through the logbooks in a fixed order. | always-on department (service), shift supervisor (systemd), work order (process), logbook |
| 06 | bash-scripting | 1 | You stop repeating instructions at the desk. You write a slip with conditions and repeats, and put routines on a timetable. | instruction slip, timetable (cron) |
| 07 | python-for-devops | 1 to 2 | A slip is no longer enough. A trained operations officer can phone the landlord's office and work across many buildings at once. | operations officer, phone line to the landlord (boto3) |

## The rented campus

| # | Session | Zoom | Story beat | New story words |
|---|---|---|---|---|
| 08 | aws-ec2-basics | 2 | You meet the landlord AWS and its cities and towers. You open an account, rent a building, choose its size and receive the key. | city (region), tower (availability zone), building size (instance type) |
| 09 | aws-iam | 2 | Staff at the landlord's office decide who may rent or demolish. You write permission letters, hand out duty badges, and lock the owner's account away behind a second lock. | permission letter (policy), duty badge (role), second lock (MFA) |
| 10 | aws-ec2-storage-and-scaling | 2 | You add attachable storerooms and photograph their contents, take a permanent address, photocopy a furnished model hotel, and open extra buildings in wedding season. | storeroom (EBS), photograph (snapshot), model hotel (AMI), wedding season (scaling) |
| 11 | aws-load-balancing | 2 | A marshal at the main gate sends guests only to buildings that answer "we are open", and guest conversations travel in sealed envelopes. | marshal (load balancer), sealed envelope (TLS) |
| 12 | aws-s3 | 2 | The endless warehouse: labelled boxes, older copies kept, old boxes moved to a cheaper godown, a display window for brochures, and brochure stands in every city. | warehouse (bucket), box (object), display window (static site), brochure stand (CloudFront) |
| 13 | aws-rds | 2 | The landlord runs your records office. A ruled ledger with fixed columns sits beside folders of loose forms, with nightly copies, a standby ledger in another tower and photocopies for reading. | records office (RDS), ruled ledger (SQL), loose forms (NoSQL), standby ledger (Multi-AZ) |
| 14 | aws-vpc-networking | 2 | You design the gated campus: its number range, a road-facing wing and a back-office wing, the main gate, direction boards, a dispatch desk, two kinds of guard, a gatehouse for staff and a skywalk to another campus. | campus (VPC), wing (subnet), main gate (internet gateway), dispatch desk (NAT), gatehouse (bastion), skywalk (peering) |
| 15 | aws-monitoring-and-serverless | 2 | The landlord's meters and CCTV, an alarm that phones the manager, a public-address system, and a freelancer who arrives when a bell rings. | meters (metrics), alarm, public-address system (SNS), freelancer (Lambda) |

## Head office

| # | Session | Zoom | Story beat | New story words |
|---|---|---|---|---|
| 16 | git-and-github | 3 | Head office opens. Designers keep blueprints in a register of revisions, work on drafts, ask the chief architect for review, and sort out the day two of them moved the same wall. | blueprint (code), register (Git), vault (GitHub), draft (branch), review (pull request) |
| 17 | jenkins-foundations | 3 | You hire the workshop foreman. Every new revision is fabricated and inspected at once, and you write the first conveyor instructions. | foreman (Jenkins), fabricate (build), inspect (test), finished unit (artifact) |
| 18 | jenkins-pipelines-and-plugins | 3 | The full conveyor: stations in order, stations running side by side, shared instruction binders and attachments. | station (stage), instruction binder (shared library), attachment (plugin) |
| 19 | jenkins-advanced-and-distributed | 3 | Each draft gets its own conveyor. The foreman keeps a locked key cabinet and a backup of workshop records, and workbenches do the heavy lifting. | key cabinet (credentials), workbench (agent) |
| 20 | github-actions-and-devsecops | 3 | A conveyor is built into the vault itself. Inspection moves inside the conveyor: a blueprint inspector and an X-ray for finished truck designs, so a faulty design never reaches the depot. | blueprint inspector (SonarQube), truck X-ray (Trivy) |
| 21 | docker-fundamentals | 3 | A separate building or a truck? You fetch a truck design from the depot, roll out a truck, park it in the courtyard, plug it into the building's power and water, connect its serving window to a building door, and keep valuables in the locker room. | truck (container), truck design (image), serving window (port), locker room (volume) |
| 22 | dockerfile-and-registries | 3 | You write the truck's fit-out sheet, reuse common sheets, label each edition, ship only the finished truck and not the workshop, and store designs in the depot. | fit-out sheet (Dockerfile), edition label (tag), depot (registry) |
| 23 | kubernetes-architecture | 3 | There are too many trucks to manage by hand. The operations command takes over: its reception, master ledger, allocation officer and supervisors, plus a resident manager in every building. | operations command (Kubernetes), master ledger (etcd), resident manager (kubelet) |
| 24 | kubernetes-workloads-on-gke | 3 | You issue standing orders, park trucks in bays, give each service a permanent extension number, use notice boards and sealed envelopes, and open more trucks when queues grow. The landlord GCP runs the command for you. | standing order (Deployment), parking bay (Pod), extension number (Service) |
| 25 | microservices-on-kubernetes | 3 | You open a truck park: many small trucks, each doing one job, that call each other by extension, with a concierge at the entrance and a locker room for the records truck. | truck park (microservices), concierge (Ingress) |
| 26 | prometheus-and-grafana | 3 | The control room opens: an inspector reading every meter, an alarm desk, and a wall of live screens, all installed from one franchise kit. | inspector (Prometheus), alarm desk (Alertmanager), wall of screens (Grafana), franchise kit (Helm) |

## Building from documents

| # | Session | Zoom | Story beat | New story words |
|---|---|---|---|---|
| 27 | terraform-foundations | 2 | You stop renting by hand. You write the campus master plan, preview the changes, let the contractor build, and keep the as-built register. | master plan (Terraform code), contractor (provider), as-built register (state) |
| 28 | terraform-on-aws | 2 | The whole campus from session 14 is built from one plan, using standard designs and a shared register with a lock so two contractors never build at once. | standard design (module), register lock (state locking) |
| 29 | ansible | 2 | The setup crew arrives with a list of buildings, checklists, reusable binders and fill-in forms. It enters by the staff entrance, does the work and leaves. Terraform builds, Ansible furnishes. | setup crew (Ansible), checklist (playbook), binder (role), fill-in form (Jinja2 template) |

## More landlords and grand openings

| # | Session | Zoom | Story beat | New story words |
|---|---|---|---|---|
| 30 | azure-and-azure-devops | 2 and 3 | You sign with a second landlord. A translation table shows the same buildings under new names, and this landlord offers a ready-made head office: planning wall, vault, conveyor and parts store. | second landlord (Azure), planning wall (Boards) |
| 31 | capstone-cicd-pipeline | All | The first grand opening. A revision enters the vault, the bell rings, the foreman fabricates and inspects, a truck design is made, a truck rolls out and parks, and a guest is served. | none: every word is reused |
| 32 | ai-apps-and-mlops-on-cloud | 3 | One truck phones an outside expert for each guest question. Another runs a trained brain under the AWS-run operations command, and that brain is shipped and re-trained like any truck. | outside expert (LLM API), trained brain (model) |
| 33 | aiops-and-mcp-servers | 3 | The assistant takes night duty in the control room, and you fit a service hatch so it can use the hotel's tools safely. | night duty (AIOps), service hatch (MCP server) |

## The guest's journey, by session

The eight steps of the guest's journey in the story file are each taught in one place:

| Journey step | Taught in |
|---|---|
| Looking up the hotel's address | 05 (roads), 12 (brochure stands) |
| Roads and junctions | 05, 14 |
| Campus main gate | 14 |
| Marshal | 11 |
| Door guard and numbered doors | 05, 10, 14 |
| Truck serves the guest | 21 to 25 |
| Records office and warehouse | 12, 13 |
| Control room | 15, 26 |

Session 31 walks the whole journey once, end to end.

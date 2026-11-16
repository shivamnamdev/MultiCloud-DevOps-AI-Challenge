# SYLLABUS BLUEPRINT (DRAFT for author approval): Python-style DevOps course
*Drafted 2026-11-13. Nothing is written until this is approved (BLAST Protocol 0).*

## Decisions already made by the author
- Source notes (CloudDevOpsHub / Vikas Ratnawat) are used as a **topic map only**: no copied wording, analogies, structure, success stories, salary/income claims, branding or batch/pricing/timing details. All scripts are original, in the author's own voice, with new analogies and examples; technical facts are checked against official docs, not the notes.
- Deliverable per session: `02_script.md` only (scripts only; teleprompter text/videos later if wanted).
- Format "like Python": `social-content/course-product/SESSION-NN_<slug>/02_script.md`, **4 episodes per session**, ~5 scenes per episode, Roman Hinglish, `[VISUAL]` cue + voiceover per scene, ~2,500-3,000 spoken words per session.

## Condensing 60 source sessions (~770k words) into 33 sessions (132 episodes, ~15 h)
| # | Session (slug) | Maps from source | Core outcome |
|---|---|---|---|
| 01 | cloud-and-devops-foundations | S02, S03 (+tech parts of S01) | Virtualization, IaaS/PaaS/SaaS, what DevOps really is, CI/CD vocabulary |
| 02 | ai-co-programmer-for-devops | S04, S48, S49 | Prompting, agents, using AI on logs/IaC/review, with verification habits |
| 03 | linux-foundations | S05, S06 | Filesystem, shell, 40 core commands, VM + SSH access |
| 04 | linux-users-permissions-ssh | S06, S08 + author's Linux notes 1-6, 16 | Users/groups, password policy, chmod/chown, umask, SUID/SGID/sticky, SSH keys, apt/dnf, boot process and targets |
| 05 | linux-sysadmin-and-troubleshooting | S07, S09 + author's Linux notes 7-10 | Monitoring commands, process states, services, logs and logrotate, networking, static IP, firewall basics, health-check script |
| 05B | linux-storage-web-server-and-security | S07, S09 + author's Linux notes 10-15 | Partitions, file systems, fstab, swap, LVM, Apache, firewalld zones, SELinux, NAT (on a Red Hat family VM) |
| 06 | bash-scripting | S43 | Variables, conditions, loops, functions, error handling, cron |
| 07 | python-for-devops | S44 | boto3, requests, paramiko, venv, automation scripts (links to Python course) |
| 08 | aws-ec2-basics | S10 | Regions/AZs, account, EC2 launch, key pairs |
| 09 | aws-iam | S12 | Users/roles/policies, least privilege, MFA |
| 10 | aws-ec2-storage-and-scaling | S11, S13 | EBS, snapshots, AMI, Elastic IP, scaling, launch templates |
| 11 | aws-load-balancing | S14 | ALB/NLB, target groups, health checks, TLS |
| 12 | aws-s3 | S15, S16 | Buckets, classes, lifecycle, versioning, static site, CloudFront |
| 13 | aws-rds | S17 | SQL vs NoSQL, RDS, backups, Multi-AZ, replicas |
| 14 | aws-vpc-networking | S18, S19 | CIDR, subnets, IGW/NAT, route tables, NACL vs SG, bastion, peering |
| 15 | aws-monitoring-and-serverless | S20, S21 | CloudWatch, SNS, alarms, Lambda, EventBridge |
| 16 | git-and-github (Part A) | S22, S23 + author's Git cohort days 1-9 | Three zones, reading history, branches, merges, conflicts, inside `.git` |
| 16B | github-and-team-workflows (Part B) | S22, S23 + author's Git cohort days 10-16 | Remotes, pull requests, stash, detached HEAD, cherry-pick, undo, forks, team run |
| 17 | jenkins-foundations | S24, S25 | CI idea, install, freestyle vs pipeline, Maven, Jenkinsfile |
| 18 | jenkins-pipelines-and-plugins | S26, S27 | Stages, parallel, shared libraries, key plugins |
| 19 | jenkins-advanced-and-distributed | S28, S29 | Multibranch, credentials, backup, agents |
| 20 | github-actions-and-devsecops | S46 (part), S53 | Workflows in YAML, Trivy, SonarQube, secrets management |
| 21 | docker-fundamentals | S30, S31 | VM vs container, images/containers, run/exec/logs, volumes |
| 22 | dockerfile-and-registries | S32 | Dockerfile, layers/cache, tagging, multi-stage, push |
| 23 | kubernetes-architecture | S33 | Control plane, nodes, kubectl, local cluster |
| 24 | kubernetes-workloads-on-gke | S34 | Pods, Deployments, Services, HPA, ConfigMaps/Secrets, GKE |
| 25 | microservices-on-kubernetes | S35, S51 | Multi-service app, Ingress, PVC, service-to-service, API gateway |
| 26 | prometheus-and-grafana | S36, S37 | Pull model, PromQL, Helm stack, dashboards, alerts |
| 27 | terraform-foundations | S38 | HCL, providers, plan/apply/destroy, state |
| 28 | terraform-on-aws | S39, S52 | Multi-resource, modules, remote state + locking, 3-tier build |
| 29 | ansible | S40, S41, S42 | Inventory, playbooks, roles, Jinja2, Terraform vs Ansible |
| 30 | azure-and-azure-devops | S47, S54 | Azure vs AWS/GCP mapping, Boards/Repos/Pipelines/Artifacts |
| 31 | capstone-cicd-pipeline | S50 | Spring Boot app: webhook -> Jenkins -> Docker -> deploy |
| 32 | ai-apps-and-mlops-on-cloud | S55, S56 | LLM API in an app, FastAPI model serving on EKS |
| 33 | aiops-and-mcp-servers | S57, S59 | Anomaly detection/self-healing, building an MCP server |

**Intentionally dropped** (not teachable content / not yours to reuse): S00 kickoff, S01 community/job-board parts, S45 ATS resume (can be rewritten as your own career session later), S46 Splunk/Kafka/n8n tangents, S58 graduation, Mock-Interview, FREE Workshops, batch logistics, the `learning-app/` content, and all branding/salary claims.

## Proposed build order and quality gates
1. **Pilot:** write SESSION-21 docker-fundamentals first; author reviews tone/depth before scaling.
2. Then in batches of 3-4 sessions in learning order (Linux -> AWS -> CI/CD -> containers -> IaC -> capstones).
3. Each session must pass: accurate vs official docs (versions/commands re-checked), original analogies, no copied wording from source (spot-check by comparison), 4 episodes x ~5 scenes, hands-on lab in every episode.
4. Record each session in this course's `progress.md`; update `findings.md` if a discovery changes scope.

## Open decisions for the author
- Keep all 33, or a smaller "Core 24" (drop 02, 15, 19, 20, 29, 30, 32, 33 for a later "Advanced" course)?
- Starting point: pilot SESSION-21 (recommended), or a different session?
- Name for the new course (the repo/course folder is still `MultiCloud-DevOps-AI-Challenge`).

## Change log
- **2026-11-16:** Linux grew by one script. Session 05B (storage, web server, security layers) was added for the part of the author's Linux notes that had no home (disks and swap, LVM, Apache, SELinux, NAT), and sessions 04 and 05 were rewritten to carry the rest. Sessions 03 to 05 stay on Ubuntu and name the Red Hat family equivalent once; 05B runs on a Rocky or AlmaLinux VM. No session was renumbered: 33 numbered sessions, 35 session scripts plus Session 00. Detail: `NOTES_INTEGRATION_MAP_LINUX_K8S.md`.
- **2026-11-14:** Git split into 16 (Part A) and 16B (Part B), four episodes each, so the author's 16-day Git cohort is covered in brief without renumbering sessions 17-33. The course is still 33 numbered sessions; it now has 34 session scripts plus Session 00. Detail: `GIT_NOTES_INTEGRATION_MAP.md`. The deep version of this material is a separate dedicated course in `courses/Github-Live-Cohort-Transcript`.

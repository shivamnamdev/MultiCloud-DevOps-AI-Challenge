# Where the author's Linux and Kubernetes notes go

**Status:** Linux part approved by the author and applied on 2026-11-16 (sessions 04, 05 and new 05B; see section 6). Kubernetes part applied on 2026-11-17 to sessions 23 to 25 (see section 7).
**Sources:** `Linux-Handwritten-Notes.md` (17 sections) and `K8s-Handwritten-Notes.md` (12 sections).
**Method:** each note section was checked against the current scripts by keyword search. "In script today" means the topic is at least named there; it does not mean it is taught at the depth of the notes.

Corrections already marked ⚠️ in the two transcriptions are applied when a topic is woven in; the handwritten wording is not carried over where it was wrong.

## 1. Linux notes

| # | Note section | In script today | Goes to | Story words (locked) |
|---|---|---|---|---|
| 1 | User administration: user types, UID ranges, `useradd` options (`-u -g -G -s -d -c`), `passwd`, lock and unlock, `su`, `userdel -r` | Partly (04: users, UID 0, `useradd -m`, `passwd`). Options, locking and `userdel` are missing | **04**, episode 1 | Staff, ID card, general manager, service staff |
| 2 | Groups: primary vs secondary, `groupadd`, `gpasswd`, `usermod -aG` | Partly (04: `groupadd`, `usermod -aG`). Primary vs secondary and `gpasswd` are missing | **04**, episode 1 | Home department, extra department cards |
| 3 | sudo access: `wheel`, `visudo`, sudoers lines | Yes (04), on Ubuntu's `sudo` group only | **04**, episode 1 | Duty manager borrowing the master key |
| 4 | Password policy: `/etc/login.defs`, `chage`, inactive period | No | **04**, episode 1 (one scene) | ID card expiry and renewal rules |
| 5 | File permissions and umask, `chmod` symbolic and octal | Permissions yes (04). `umask` is missing | **04**, episode 2 | Three-ring lock; default lock setting on a new room |
| 6 | Special permissions: SUID, SGID, sticky bit | No | **04**, episode 2 (one scene) | Machine that acts with the owner's authority; department room; lost-and-found |
| 7 | Process management: lifecycle, `ps`, `top`, STAT codes, zombie, `kill`, services | Partly (05: `top`, `kill`, `systemctl`). Lifecycle, STAT codes and zombies are missing | **05**, episode 1 | Work order, token number, shift supervisor |
| 8 | Log management: `/var/log`, `journalctl`, `logrotate` | Partly (05) | **05**, episode 2 | Logbook room, archiving old registers |
| 9 | Networking basics: static IP three ways (`nmcli`, `nmtui`, config file) | No | **05**, episode 3 | Street address of the building |
| 10 | firewalld: zones, services, ports, default zone, sources | Named in 05 only | **05**, episode 3 | Gate guard with a list; security levels for different gates |
| 11 | NAT: masquerade, rich rules, port forwarding | No | **05B** (new, see section 3), with a callback in **14** when the NAT gateway appears | Front desk that sends all letters under one address; passing a caller to the right room |
| 12 | Disk partitions, file systems, `/etc/fstab`, swap | Partly (10: partition, format, mount on an EBS volume). MBR vs GPT and swap are missing | **05B**, then reused in **10** on a cloud volume | Raw floor space, walls, shelving, door from the corridor, overflow room |
| 13 | LVM: PV, VG, LV, extend, reduce, remove | No | **05B** | Banquet halls with movable walls |
| 14 | Apache HTTP server, document root | No | **05B** (it is also the service used in the labs of 08 and 11) | Front-of-house service on door 80 |
| 15 | SELinux: modes, contexts, commands | No | **05B** | Second security layer: labelled badges on staff and rooms |
| 16 | Boot process, run levels | Yes (04, episode 4) | **04**, episode 4 (add targets vs run levels) | Morning opening routine |
| 17 | Command cheat sheet | Not applicable | Student handout at the end of 04, 05 and 05B | Not applicable |

## 2. Kubernetes notes

| # | Note section | In script today | Goes to | Story words (locked) |
|---|---|---|---|---|
| 1 | Pods: everyday commands, questions answered by `describe`, the READY column, pod YAML, changing the image, `logs --previous` | Partly (23, 24). The `describe` questions, READY and `--previous` are missing | **23**, episode on `kubectl`; **24**, episode 1 | Parking bay holding one truck |
| 2 | Pod states and container exit codes | States yes (24). Exit-code table is missing | **24**, episode 1 (one scene), reused in 26 for troubleshooting | A truck that fails to start; the supervisor's report |
| 3 | ReplicaSets: YAML, selector, scale to 5 | Named in 24 only | **24**, episode 2 | Standing order for a fixed number of trucks |
| 4 | Deployments, and what READY counts | Yes (24) | **24**, episode 2 | Standing order; replacing trucks one at a time |
| 5 | Namespaces: why, YAML, commands, switching, cross-namespace DNS | Named in several sessions; never taught as a topic | **24**, episode 3 | Separate wings for dev, staging and production |
| 6 | ResourceQuota and LimitRange | Named in 25 only | **25**, one scene | A wing's power and water budget; the per-truck allowance |
| 7 | Services, exposing a pod | Yes (24) | **24**, episode 3 | One permanent extension number |
| 8 | Persistent Volumes: why, access modes, binding, reclaim policy | Named in 25 | **25**, episode on storage | Locker room that outlives the truck |
| 9 | Persistent Volume Claims: rules, statuses, commands, expanding, binding to a specific PV | Named in 25 | **25**, episode on storage | A truck's request slip for a locker |
| 10 | StorageClass | Named in 25 | **25**, episode on storage | The catalogue of locker types the landlord offers |
| 11 | Horizontal and vertical scaling | HPA yes (24). Vertical is missing | **24**, episode 4 | More trucks vs a bigger truck |
| 12 | Command cheat sheet | Not applicable | Student handout at the end of 24 and 25 | Not applicable |

The Kubernetes notes fit inside sessions 23 to 25 without a new session. Session 24 becomes the heaviest of the three.

## 3. The size decision for Linux

Sections 11 to 15 of the Linux notes (NAT, disks and swap, LVM, Apache, SELinux) are about a third of the notes and none of it is in the scripts. Session 05 already carries processes, logs, networking and a health-check script.

**Recommended:** a new **SESSION-05B, Linux storage, web server and security layers**, four episodes, the same pattern as 16B, so no session is renumbered:

| Ep | Title | From the notes |
|---|---|---|
| 1 | Disks, partitions, file systems, swap | Section 12 |
| 2 | LVM: create, extend, reduce | Section 13 |
| 3 | Apache: install, serve a page, change the document root | Section 14 |
| 4 | SELinux, and NAT with firewalld | Sections 15 and 11 |

Alternative: no new session. Disks and LVM go into session 10 with EBS, Apache into the session 08 lab, SELinux and NAT become one scene each in session 05. This keeps the count but makes session 10 very heavy and reduces LVM and SELinux to mentions.

## 4. The distribution decision

The notes are written on a Red Hat family system: `yum`, `wheel`, `firewalld`, SELinux, `httpd`. The scripts so far use Ubuntu: `apt`, the `sudo` group, `ufw`.

**Recommended:** keep Ubuntu as the main line in sessions 03 to 05 and say the Red Hat equivalent once where they differ (`apt` / `yum`, `sudo` group / `wheel`). Run 05B on a Red Hat family VM (Rocky or AlmaLinux), because firewalld, SELinux and `httpd` are native there. Students then work on both families, which is also what the cloud sessions need (Amazon Linux is in the Red Hat family).

## 5. Decisions needed

1. Linux size: new session 05B (recommended), or distribute into 05, 08 and 10.
2. Distribution: Ubuntu main line with 05B on a Red Hat family VM (recommended), all Ubuntu, or all Red Hat family.
3. Sessions 03 and 04 were already rewritten with the story but without these notes. Confirm they should be reopened to add the missing items from sections 1 to 6.

## 6. What was applied (2026-11-16)

The author approved all three recommendations in section 5.

| Session | What changed | Notes sections |
|---|---|---|
| 04 | User types, UID range, the seven fields of `/etc/passwd`, `useradd` options, primary vs secondary groups, `gpasswd`, a new scene on password policy (`chage`, `/etc/login.defs`, inactive period, lock, `userdel -r`), sudoers lines and `wheel`, `umask`, SUID / SGID / sticky bit, `yum` vs `dnf`, initramfs, run levels vs targets | 1 to 6, 16 |
| 05 | Rewritten with the story. Process lifecycle, PPID, STAT codes, zombies, `killall`, TTY, rsyslog vs journald, journal persistence, `logrotate`, static IP (netplan; `nmtui` / `nmcli` named), firewall with `ufw` and firewalld introduced | 7 to 10 |
| 05B (new) | Partitions, MBR vs GPT, file systems, `/etc/fstab`, swap, LVM, Apache, firewalld zones, SELinux, masquerade, port forwarding, rich rules | 10 to 15 |
| 03 | Not changed. None of the 17 note sections falls in it | none |

### Changes from the plan in sections 1 to 3

- **firewalld hands-on moved from 05 to 05B, episode 3.** Session 05 is on Ubuntu, where the firewall is `ufw`; firewalld is native on the 05B machine and is needed there anyway to open port 80 for Apache. Session 05 keeps the `ufw` lab and introduces firewalld, zones and the `--permanent` + `--reload` habit in words.
- **Static IP is taught in 05 without a hands-on change on the lab VM**, because changing the address inside a cloud VM cuts off the session. The script says to practise it only on a local VM.
- **Episode 3 of 05B is "Apache and firewalld"; episode 4 is "SELinux and NAT".** The document-root change in episode 3 ends on a 403, which episode 4 explains and fixes with the SELinux label.
- **Story word:** masquerade uses "dispatch desk" (the word already used for the NAT gateway in session 14), not "front desk", because session 04 already calls the web server the front desk. `ANALOGY_STORY.md` is updated.

### Statements in the notes that were corrected in the scripts (not marked ⚠️ in the transcription)

| Note section | Note says | Script says |
|---|---|---|
| 7 | If the parent terminates, its children are terminated by default | An orphaned child is adopted by PID 1 (systemd). A zombie is a finished child whose parent has not collected its result; it cannot be killed, the parent has to be fixed |
| 8 | Journal logs are not persistent | True when the journal is in `/run/log/journal`; it is kept on disk when `/var/log/journal` exists, which is the usual case on Ubuntu |
| 10 | firewalld uses the predefined services in `/etc/services` | Not stated. firewalld has its own service definitions (`firewall-cmd --get-services`) |
| 10 | Nine zones | Zones are named, not counted (current releases list one more) |
| 10 | `--add-source=192.168.0.0` for a subnet | `192.168.0.0/24` |
| 13 | `xfs_growfs` with the device path; reduce with `resize2fs` then `lvreduce -L -1G` | `xfs_growfs` with the mount point; `lvextend -r` and `lvreduce -r`, which resize the file system and the volume in the safe order |
| 14 | `yum groupinstall 'Basic Web Server'` | `sudo dnf install -y httpd` |
| 15 | Apache's process label is `httpd_sys_content_t` | The process type is `httpd_t`; `httpd_sys_content_t` is the type of the content it may read |

### Still open

- Lab commands in 04, 05 and 05B have not been run end to end. Run them on Ubuntu (04, 05) and on Rocky or AlmaLinux 9 (05B) before recording.
- Callback to 05B in session 10 (disks, fstab with `nofail`, resize on a cloud volume) is done (2026-11-16). The callback in session 14 (NAT gateway as the landlord's dispatch desk, and port forwarding as its opposite) is done (2026-11-17).
- Kubernetes notes (section 2) applied on 2026-11-17; see section 7.

## 7. What was applied: Kubernetes notes (2026-11-17)

| Note section | Where it went | Change from the plan |
|---|---|---|
| 1 Pods: commands, `describe` questions, READY, pod YAML, changing the image | Session 23, episode 4 (scenes 3 to 5) | `logs --previous` moved to Session 24, episode 1, next to the exit codes |
| 2 Pod states and exit codes | Session 24, episode 1 | Added 143 (SIGTERM) to the table; the notes' correction about phases vs STATUS values is kept |
| 3 ReplicaSets | Session 24, episode 2 | The label-adoption caution (a hand-made pod with a matching label is claimed) was added |
| 4 Deployments and READY | Session 24, episode 2 | READY for a pod counts containers, for a Deployment counts pods (the notes' correction) |
| 5 Namespaces | Session 24, episode 3 | Moved from Session 25 so that Session 24 episode 3 covers wings and Services together; Session 25 episode 2 now carries config, resources and quota |
| 6 ResourceQuota and LimitRange | Session 25, episode 2 | Added that a quota breach shows as `FailedCreate` on the ReplicaSet, not as a Pending pod (the old Session 25 draft said Pending) |
| 7 Services | Session 24, episode 3 | Default `kubernetes` service and `expose` kept as in the notes |
| 8 to 10 Persistent Volumes, Claims, StorageClass | Session 25, episode 3 | `ReadWriteOnce` is per node (the notes' correction), `ReadWriteOncePod` added; a Postgres StatefulSet is mentioned but RDS is recommended for production |
| 11 Horizontal and vertical scaling | Session 24, episode 4 | Tied to Session 10 (Auto Scaling) and Session 13 (instance class vs read replica) |
| 12 Cheat sheet | Handout tables at the end of Sessions 23, 24 and 25 | None |

Open items for Kubernetes: lab commands not run end to end; GKE steps and Autopilot behaviour need a re-check against the live docs before recording; `kind` and `minikube` setup for Ingress and metrics-server is described, not tested.

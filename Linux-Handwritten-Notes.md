# Linux: Class Notes (from handwritten `Linux.pdf`)

> Transcribed from 50 handwritten pages and organised by topic. Hindi/Hinglish remarks are translated into English.
> Items marked **⚠️ Correction** are places where the handwritten note was ambiguous or technically off. I've written the correct version.
> RHEL/CentOS-style commands (`yum`, `firewalld`, `nmtui`, SELinux) are used throughout.

## Contents
1. [User administration](#1-user-administration)
2. [Groups](#2-groups)
3. [sudo access](#3-sudo-access)
4. [Password policy](#4-password-policy)
5. [File permissions and umask](#5-file-permissions-and-umask)
6. [Special permissions (SUID, SGID, Sticky)](#6-special-permissions)
7. [Process management](#7-process-management)
8. [Log management](#8-log-management)
9. [Networking basics](#9-networking-basics)
10. [Firewall (firewalld)](#10-firewall-firewalld)
11. [NAT: masquerade and port forwarding](#11-nat)
12. [Disk partitions, file systems, swap](#12-disk-partitions-file-systems-swap)
13. [LVM](#13-lvm-logical-volume-manager)
14. [HTTP server (Apache)](#14-http-server-apache)
15. [SELinux](#15-selinux)
16. [Linux boot process](#16-linux-boot-process)
17. [Cheat sheet](#17-command-cheat-sheet)

---

## 1. User administration

### Types of users
| Type | Description |
|---|---|
| **Super user (root)** | All privileges |
| **Local user** | Added by root; doesn't have all privileges |
| **System user** | Runs system services, e.g. `apache` handles web services |
| **Sudo user** | A privileged local user |

### UID ranges
- root → UID `0`
- local users → `1000 – 60000`

### Adding a user
```bash
useradd <name>
tail -1 /etc/passwd        # see the entry for the last-created user
man <command>              # manual for any command
```

Files updated when a user is added:
| File | Contents |
|---|---|
| `/etc/passwd` | User account info |
| `/etc/shadow` | User passwords and password policies |
| `/etc/group` | Group info |
| `/etc/gshadow` | Group password info |

**`/etc/passwd` line anatomy**
```
user1 : x : 1003 : 1003 : comment : /home/user1 : /bin/bash
  │     │     │      │       │          │            └─ default shell
  │     │     │      │       │          └─ home directory
  │     │     │      │       └─ comment (GECOS) field
  │     │     │      └─ group ID (GID)
  │     │     └─ user ID (UID)
  │     └─ placeholder: the password lives in /etc/shadow
  └─ username
```

### Common `useradd` / `usermod` options
```bash
useradd -u 1111 user1          # -u : assign UID manually
useradd user2                  # next user gets the next UID after the last one (1112)
useradd -c "Hi comment" user3  # -c : add a comment
usermod -c "hello" user2       # add/change comment on an EXISTING user
```
If you don't give a UID manually, the new UID is generated after the last used UID.

### Passwords and locking
```bash
passwd user3          # set a password
usermod -L user3      # Lock the user
usermod -U user3      # Unlock the user
```
In `/etc/shadow`, `!!` means the account is locked or no password has been set yet.

### Switching users
```bash
su - <username>
ssh <username>@localhost
```

### Deleting users
```bash
userdel <username>      # keeps the home directory
userdel -r <username>   # removes the home directory too
```

---

## 2. Groups

```bash
groupadd gslab     # updates /etc/group and /etc/gshadow
id <username>      # show UID, GID and groups
```

### Primary vs secondary membership
- **Primary group**: mandatory. Every user must be a primary member of exactly one group.
- **Secondary group**: a user can belong to several.

```bash
useradd -g gslab harry   # harry's PRIMARY group is gslab (no separate "harry" group is created)
useradd -G gslab bob     # bob is a SECONDARY member of gslab, primary of his own "bob" group
```
- `-g` → primary group
- `-G` → secondary group(s)

Rules to remember:
- Many users can share one primary group.
- A user can have only **one** primary group. If you set a new primary group, the previous one is replaced (the user is dropped from the old primary).
- A user can be a secondary member of many groups.

### Changing group membership
```bash
usermod -g <group> <user>      # change PRIMARY group
usermod -G <group> <user>      # set secondary group(s), REPLACES the existing list
usermod -aG <group> <user>     # -a = append, ADD to secondary groups without removing others
gpasswd -a <user> <group>      # add a user to a group
gpasswd -d <user> <group>      # remove a user from a group
```
> **⚠️ Correction:** the note says "`-a` stands for all". It actually means **append**. Without `-a`, `-G` overwrites the user's existing secondary groups.

---

## 3. sudo access
```bash
visudo                              # safe editor for /etc/sudoers
```
Entries:
```
harry   ALL=(ALL)   ALL                         # harry can run any command as anyone
harry   ALL=(ALL)   /usr/bin/<command>          # allow only a specific command
harry   ALL=(ALL)   ALL, !/usr/bin/<command>    # everything EXCEPT that command
%<groupname>  ALL=(ALL)  ALL                    # give a whole group sudo rights (note the %)
```
Alternative: make the user a secondary member of the `sudo` (Ubuntu) or `wheel` (RHEL) group for the same effect.

```bash
history        # list previously used commands
```

---

## 4. Password policy

`passwd` modifies `/etc/shadow`.

**`/etc/shadow` entry**
```
test123 : !! : 18524 : 0 : 99999 : 7 : : :
```
| Field | Meaning |
|---|---|
| `!!` | locked / no password yet |
| `18524` | last password change (days since 1 Jan 1970) |
| `0` | minimum days between changes |
| `99999` | maximum days before the password must change |
| `7` | warning days before expiry |

System defaults live in `/etc/login.defs`:
```
PASS_MAX_DAYS   99999
PASS_MIN_DAYS   0
PASS_MIN_LEN    5
PASS_WARN_AGE   7
```

### `chage`: view and edit a user's password policy
```bash
chage -l test1        # list the password policy
chage -m 2 test1      # minimum days before the password can be changed
chage -M 10 test1     # maximum days before the password must be changed
chage -W 3 test1      # start warning 3 days before expiry
date -s 'YYYY-MM-DD HH:MM:SS'   # change the system date (handy for testing expiry)
```

### Inactive period
The number of days after the password expires during which the user can still log in with the old password and set a new one. After that the account is locked and the system admin has to step in.

Example:
| Event | Date |
|---|---|
| Last password change | Oct 14 |
| Password expires | Oct 24 |
| Inactive period ends | Oct 30 |

From Oct 24 to Oct 30 the user can still use the old password and then create a new one. After Oct 30 the admin must reset the credentials.

**Account expiry** is the date when the whole account expires automatically.

---

## 5. File permissions and umask

| Permission | Letter | Value |
|---|---|---|
| Read | `r` | 4 |
| Write | `w` | 2 |
| Execute | `x` | 1 |

Total `rwx` = **7**.

> **⚠️ Correction:** the note labels execute as "s". The letter is `x`. `s` is the SUID/SGID bit.

### umask
`umask` sets the **default** permissions for new files and directories.
```bash
umask      # root shows 0022, a normal local user shows 0002
```
The first digit is the special-permission digit; the remaining three apply to user, group and others.

Calculation (as in the notes, using root's `022`):
```
Directories start from 777 (rwx rwx rwx)
umask 022   →  --- -w- -w-
result 755  →  rwx r-x r-x    (directory)

Files start from 666 (rw- rw- rw-)
result 644  →  rw- r-- r--    (file)
```
Note that files never get execute by default, which is why the base for files is 666.

### Changing permissions: `chmod`
Who: `u` = user, `g` = group, `o` = others, `a` = all.
```bash
chmod u+x /redhat       # add execute for user
chmod g+x /redhat       # add execute for group
chmod o+rw /redhat      # add read+write for others
chmod a+x /redhat       # add execute for everyone
chmod u-x /redhat       # subtract
chmod u=rx /redhat      # '=' OVERWRITES the existing permission
chmod a=rwx /redhat
chmod 567 /redhat       # numeric form: u=r-x (5), g=rw- (6), o=rwx (7)
```
Example: `rw- r-x ---` + `chmod u+x` → `rwx r-x ---`.

---

## 6. Special permissions

| Bit | Applies to | Symbol | Where it shows | Purpose |
|---|---|---|---|---|
| **SUID** | **files** only | `s` | user field, `rws r-x r-x` | Anyone who runs the file runs it with the **file owner's** privileges |
| **SGID** | files **and** directories | `s` | group field, `rwx r-s r-x` | New files inherit the **group ownership** of the directory |
| **Sticky bit** | **directories** only | `t` | others field, `rwx rwx rwt` | Only the file's owner can delete or modify their files in that directory |

- **SUID example.** When you change a password, `/etc/shadow` is updated. Only root can modify `/etc/shadow`. The `passwd` binary has SUID, so a normal user can run it as root and update the file.
- **Sticky bit example.** `/tmp` is writable by everyone. The sticky bit ensures users can't tamper with each other's files there.

---

## 7. Process management

**Process** = an executable task. It has a **PID** (process ID) and a **PPID** (parent PID).

### Lifecycle
- A process is created (the child gets a new PID; its PPID is the parent's PID).
- While the child runs, the parent may go into waiting/sleep.
- When the child completes and returns its result, the parent resumes and the child goes to the zombie/dead state.
- If the parent terminates, its children are terminated by default.
- `/proc` holds the information about running processes. `bash` is itself a process, and it runs as long as your terminal is open.

### Listing processes
```bash
ps          # PID  TTY  TIME  CMD
ps -f       # UID PID PPID C STIME TTY TIME CMD
ps -ef      # every process, full format
ps -aux     # all users' processes: USER PID %CPU %MEM VSZ RSS TTY STAT START TIME CMD
top         # live view of running/sleeping processes
```
- **TTY** = the terminal the process runs on. `?` → background process with no terminal. `pts/0`, `pts/1` → pseudo-terminals (sessions on the machine).
- **VSZ** = virtual memory used, **RSS** = physical memory used.

### `STAT` codes
| Code | Meaning |
|---|---|
| `D` | uninterruptible sleep |
| `R` | running or runnable |
| `S` | interruptible sleep |
| `T` | stopped by a job-control signal |
| `t` | stopped by a debugger during tracing |
| `X` | dead (should never be seen) |
| `Z` | zombie |

Modifiers:
| Code | Meaning |
|---|---|
| `<` | high priority |
| `N` | low priority |
| `L` | has pages locked into memory |
| `s` | session leader |
| `l` | multi-threaded |
| `+` | in the foreground process group (running in front of you, holding the terminal) |

### Managing services and killing processes
```bash
systemctl status sshd       # details/status of a service
systemctl restart sshd
kill <option> <pid>         # e.g. kill -9 <pid>
killall <command-name>
killall -9 -u harry <cmd>   # kill a command for a specific user
```

---

## 8. Log management

| Location | Written by | Persistence |
|---|---|---|
| `/var/log` | `rsyslog.service` | **Persistent** (survives reboot) |
| `/run/log` | `systemd-journald.service` | **Not persistent** (lost on reboot) |

- To see which log file records what: `cat /etc/rsyslog.conf`
- Journal files are not in a readable format, so read them with `journalctl`.
- **logrotate** takes backups of log files. Config: `/etc/logrotate.conf`. When a log reaches a certain size, a date-stamped backup is created.
  - `weekly` → a new log file each week.
  - `rotate 4` → keep at most 4 backups. When the 5th is created, the oldest is deleted.

---

## 9. Networking basics

### Assigning a static IP (3 ways)
1. **`nmtui`**: Network Manager Text User Interface (menu-driven)
2. **`nmcli`**: Network Manager command-line interface
3. Edit the interface config file directly

All of these go through the **NetworkManager** service. After modifying a config file you must **restart/reload** the service.

```bash
ip route                       # shows the default gateway
ssh root@<static-ip-of-VM>     # reach the VM terminal
nmtui
```
`nmtui` flow: **Edit a connection → `enp0s8` → Edit → IPv4 = Manual → Add address → Gateway (from `ip route`) → OK → Back → Quit**, then restart the service (mandatory).

---

## 10. Firewall (firewalld)

A **firewall** is a gateway that filters incoming and outgoing traffic to protect the host.

- **RHEL 7+**: `firewalld.service` (user-friendly, uses predefined services in `/etc/services`, and supports ports).
- Before that, `iptables.service` was used. Only one of the two should manage the rules. `firewalld` was introduced because it is easier than iptables.
- Service ↔ port mappings are in `/etc/services`.

```bash
systemctl status firewalld.service
firewall-cmd --get-services           # all predefined services
firewall-cmd --list-services          # services currently allowed (e.g. dhcpv6, http, nfs, samba, ssh)
firewall-cmd --list-ports             # ports you added manually
firewall-cmd --list-all               # everything for the current zone
firewall-cmd --get-default-zone       # → public
firewall-cmd --get-zones
firewall-cmd --list-all-zones         # 9 zones in total
firewall-cmd --get-active-zones
```

**Zone** = a set of rules that decides which services/ports are open. You can have different zones active at the same time.
Built-in zones (9): `block`, `dmz`, `drop`, `external`, `home`, `internal`, `public`, `trusted`, `work`.

### Add or remove services and ports
```bash
firewall-cmd --add-service=ssh
firewall-cmd --remove-service=ssh
firewall-cmd --add-port=415/tcp --permanent
firewall-cmd --reload
```
- Without `--permanent` a change is only **runtime**. A reload brings the old state back.
- With `--permanent` you **must** run `firewall-cmd --reload` for it to take effect.

### Default zone and sources
```bash
firewall-cmd --set-default-zone=block
firewall-cmd --add-source=192.168.0.0 --zone=block     # put one machine/subnet in the block zone
```
- **`block`**: replies with a "not connected / prohibited" message.
- **`drop`**: silently drops traffic, so there is no reply.

---

## 11. NAT

**NAT** = Network Address *Translation* (the note says "Transmission").

### 1) Masquerade
Private machines (172.25.1.x) reach the internet through a firewall/gateway that has a private IP (172.25.1.4) and a public IP (13.45.23.12).

```
sys1 (172.25.1.1) → Firewall → google.com (1.2.3.4)
   packet leaving:   src 172.25.1.1  dst 1.2.3.4
   masquerade ON → source rewritten to the public IP:
                     src 13.45.23.12 dst 1.2.3.4
   Google replies:   src 1.2.3.4     dst 13.45.23.12 → firewall maps back to sys1
```
```bash
firewall-cmd --add-masquerade --permanent
firewall-cmd --reload
```

### Rich rules
Custom rules written in a rich-language syntax (`man firewalld.richlanguage`).
```bash
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.0.100" service name=ssh reject' --permanent
```

### 2) Port forwarding
Public traffic arriving at the firewall's public IP is forwarded to different internal machines depending on the port:

| Public port | Forwarded to | Service |
|---|---|---|
| 22 | 172.25.1.1 | SSH |
| 21 | 172.25.1.2 | FTP |
| 80 | 172.25.1.3 | HTTP |

(Masquerade = yes.) Then `ssh root@69.12.45.61` from your PC lands on sys1.

Rich rule for port forwarding:
```bash
firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.0.107" \
  forward-port to-addr="192.168.0.100" to-port="22" protocol="tcp" port="22"' --permanent
```
Meaning: traffic from 192.168.0.107 to port 22 is forwarded to machine 192.168.0.100, port 22.

---

## 12. Disk partitions, file systems, swap

**Flow:** raw disk → partition → file system → mount point.

### Partition schemes
| | MBR (old / BIOS) | GPT (UEFI) |
|---|---|---|
| Max partitions | 4 primary, or 3 primary + 1 extended (the extended holds many logical partitions) | 128 |
| Tool | `fdisk` | `gdisk` |

With MBR you can end up with 14 partitions in total: 3 primary + 1 extended containing 11 logical.

### Inspect disks
```bash
fdisk -l
lsblk               # tree view of disks and partitions
blkid               # shows the file system type / UUID
df -h               # mounted file systems and usage
du -sh <dir>        # size of a directory
```

### Add a disk to a VM
VirtualBox: **Settings → Storage → Add hard disk → Create new disk → Next → Next → set size → Create**, then restart the VM.

### Create a partition
```bash
fdisk /dev/sdb
  n        # new partition
  p        # primary
  (first sector: default)
  +500M    # last sector → size
  w        # write
partprobe  # tell the kernel about the changes
```
Inside `fdisk`, `m` shows all options.

### Format and mount
A new partition is raw, so you have to format it and mount it.
```bash
mkfs.ext4 /dev/sdb1          # format  (mkfs.<Tab><Tab> lists the available types)
mount /dev/sdb1 /data        # temporary mount; lost after reboot
```

### Persistent mount via `/etc/fstab`
> ⚠️ A wrong entry in `/etc/fstab` can stop the system from booting, so be careful.
```
# device        mount point  fs    options   dump  fsck-order
/dev/sdb1       /data        ext4  defaults  0     0
# or by UUID (from blkid):
UUID=<uuid>     /data        ext4  defaults  0     0
```
Then `mount -a` mounts everything listed in `/etc/fstab`.
The last two fields are the **dump** value and the **fsck order** (0 = don't check).

### Swap memory
Swap is disk space used when RAM is fully used, so that unwanted/idle processes can be moved out.
```bash
free -h                   # check RAM and swap
fdisk /dev/sdb            # create a partition, then:
  t                       # change type, pick the partition
  l                       # list the hex codes
  82                      # Linux swap
  w
partprobe
mkswap /dev/sdb2          # swap uses mkswap, NOT mkfs
blkid                     # type now shows "swap"
swapon /dev/sdb2          # turn on  (swapoff /dev/sdb2 turns it off)
swapon -a                 # turn on everything in fstab
```
Permanent entry in `/etc/fstab`:
```
UUID=<uuid>   swap   swap   defaults   0 0
```
Extended partitions: create multiple logical partitions inside, then run `partprobe` before using them.

---

## 13. LVM (Logical Volume Manager)

LVM makes storage **flexible**: you can grow (or shrink) a logical volume as needed.

**Building blocks:** Physical partitions → **PV** (physical volume) → **VG** (volume group) → **LV** (logical volume) → file system → mount.

### Create an LV from scratch (example: 10 GB disk `/dev/sdb`)
**Step 1: partitions** (e.g. 1 GB, 2 GB, 1 GB → `sdb1`, `sdb2`, `sdb3`)
```bash
fdisk /dev/sdb      # n, p, size..., then t → 8e (Linux LVM), w
partprobe
lsblk               # verify the three partitions exist
```
**Step 2: physical volumes**
```bash
pvcreate /dev/sdb1 /dev/sdb2 /dev/sdb3
pvs  |  pvdisplay        # list PVs (PE = Physical Extents)
```
**Step 3: volume group** (extent size defaults to 4 MB)
```bash
vgcreate my_vg /dev/sdb1 /dev/sdb2 /dev/sdb3
vgs  |  vgdisplay
```
**Step 4: logical volume**
```bash
lvcreate -n my_lv1 -L 1G my_vg       # -n name, -L size, last arg = VG name
lvs  |  lvdisplay
```
**Step 5: format and mount**
```bash
mkfs.ext4 /dev/my_vg/my_lv1
vim /etc/fstab        # UUID=...   /data   ext4   defaults  0 0
mount -a
df -h
```
Sizing by extents instead of size:
```bash
lvcreate -n my_lv2 -l 100 my_vg      # -l = number of extents,  -L = size directly
mkfs.xfs /dev/my_vg/my_lv2           # → mount it on /data2 via fstab
```

### Extend an LV
```bash
lvextend /dev/my_vg/my_lv2 -L +1G
```
The VG name is part of the device path (`/dev/<vg>/<lv>`). Extending the LV does **not** extend the file system, so you must do that manually. Check the type first:
```bash
xfs_growfs /dev/my_vg/my_lv2         # XFS (can only grow, never shrink)
resize2fs /dev/my_vg/my_lv1          # ext4
```
(Shortcut: `lvextend -r ...` resizes the file system at the same time.)

### Reduce an LV (ext4 only; XFS can't shrink)
Reducing risks data loss, so unmount first.
```bash
umount /data
e2fsck -f /dev/my_vg/my_lv1          # check the file system first
resize2fs /dev/my_vg/my_lv1 1G       # shrink the file system
lvreduce -L -1G /dev/my_vg/my_lv1    # then shrink the LV
mount -a                             # re-mount
```
> **⚠️ Correction / caution:** always shrink the **file system first**, then the LV. `lvreduce -L <size>` sets the *final* size, and `-L -1G` removes 1 GB from the current size.

### Extend a Volume Group
```bash
fdisk /dev/sdb     # new partition (type 8e), w
partprobe
pvcreate /dev/sdb5
vgextend my_vg /dev/sdb5
lvcreate -n my_lv3 -L 3G my_vg
```

### Remove an LV
```bash
lvremove /dev/my_vg/my_lv3 -y
```

---

## 14. HTTP server (Apache)

| Item | Value |
|---|---|
| Ports | HTTP **80**, HTTPS **443** |
| Package | `httpd` (group: "Basic Web Server") |
| Install | `yum groupinstall 'Basic Web Server'` |
| Service | `httpd.service` |
| System user | `apache` (listed in `/etc/passwd`) |
| ServerRoot | `/etc/httpd` (top-most directory of the web server) |
| Config | `/etc/httpd/conf/httpd.conf` (and `/etc/httpd/conf.d/*.conf`) |
| DocumentRoot | `/var/www/html` (content served from here) |
| Index page | `index.html` |

```bash
systemctl start httpd.service
firewall-cmd --add-service=http --permanent
firewall-cmd --reload
```

### Change the document root
```bash
vim /etc/httpd/conf/httpd.conf
  DocumentRoot "<new-root>"
  <Directory "<new-root>">          # also change the default directory block
```
With SELinux enforcing, the new directory also needs the right label (see below).

---

## 15. SELinux

**Security-Enhanced Linux**. It provides **MAC** (Mandatory Access Control). Regular permissions (`chmod`/`chown`, user and group) are **DAC** (Discretionary Access Control).
With SELinux on, a system user can access a file or directory only if its **context/label** allows it.

### Modes
| Mode | Behaviour |
|---|---|
| **Enforcing** | Checks labels and **blocks** disallowed access |
| **Permissive** | Doesn't block. Access is allowed, but **logs** violations |
| **Disabled** | Off. No checks, no logs |

Example: Apache's process label is `httpd_sys_content_t`. A file labelled `tmp_t` is **not allowed** in enforcing mode. In permissive mode it's allowed and a log is written.

### Contexts
Everything (files, directories, processes, ports) has a label with four parts: **user**, **role**, **type**, **sensitivity**.
```bash
ls -ldZ <file-or-dir>       # show the context (the "." after the permissions means a label exists)
```

### Commands
```bash
getenforce                  # current mode
setenforce 0                # permissive
setenforce 1                # enforcing
semanage fcontext -a -t httpd_sys_content_t "/dir(/.*)?"   # define the context for a directory
restorecon -R -v /web       # MANDATORY step: apply the labels
vim /etc/selinux/config     # SELINUX=enforcing | permissive | disabled   (permanent, needs a reboot)
reboot
```
**Notes:**
- Files created while SELinux is **disabled** get no label (no "." in `ls -Z`). When you re-enable SELinux, files get labelled again.
- Use the `httpd` man pages/config to find the default label for web content.

---

## 16. Linux boot process

Six stages:
```
BIOS → MBR → GRUB → Kernel → Init → Runlevel programs
```

1. **BIOS** (Basic Input/Output System): runs system integrity checks, searches for the boot loader (floppy, CD-ROM, hard drive), loads it into memory and hands over control. It executes the **MBR**.
2. **MBR** (Master Boot Record): the 1st sector of the bootable disk (e.g. `/dev/sda`), **512 bytes**:
   - 446 bytes: primary boot loader
   - 64 bytes: partition table
   - 2 bytes: MBR validation check

   It executes **GRUB**.
3. **GRUB** (Grand Unified Bootloader): if several kernels are installed it lets you choose one. It shows a splash screen, waits a few seconds, then loads the default kernel from its config (`/boot/grub/grub.conf`). GRUB understands file systems and loads the **kernel** and **initrd** images.
4. **Kernel**: mounts the root file system (as specified by `root=` in grub.conf) and executes `/sbin/init`, which becomes **PID 1**.
   **initrd** (Initial RAM disk) acts as a temporary root file system until the real root is mounted. It contains the drivers needed to access disks and other hardware.
5. **Init**: reads `/etc/inittab` to decide the run level.
6. **Runlevel programs**: services started from the run-level directory, e.g. "Starting sendmail … OK".

### Run levels
| Level | Mode |
|---|---|
| 0 | Halt |
| 1 | Single-user mode |
| 2 | Multi-user, without NFS |
| 3 | Full multi-user mode |
| 4 | Unused |
| 5 | X11 (graphical) |
| 6 | Reboot |

- Default level: `grep initdefault /etc/inittab`. It's typically **3 or 5**.
- Scripts live in `/etc/rc.d/rc<N>.d/` (`rc0.d` … `rc6.d`).
- Scripts starting with **`S`** run at **startup**, and those starting with **`K`** are **killed** at shutdown. The number after the letter is the sequence order.

> Note: modern systems (RHEL 7+) use **systemd** and *targets* instead of SysV init and `inittab`. These notes describe the classic SysV flow.

---

## 17. Command cheat sheet

| Task | Command |
|---|---|
| Add user (UID / comment / primary grp / secondary grp) | `useradd -u UID -c "text" -g grp -G grp user` |
| Set password | `passwd user` |
| Lock / unlock | `usermod -L user` / `usermod -U user` |
| Delete user (+home) | `userdel [-r] user` |
| Add to secondary group | `usermod -aG grp user` or `gpasswd -a user grp` |
| Remove from group | `gpasswd -d user grp` |
| Password policy | `chage -l/-m/-M/-W user` |
| Permissions | `chmod u+x,g=rx,o-w file` / `chmod 755 file` |
| Show umask | `umask` |
| Processes | `ps -ef`, `ps -aux`, `top` |
| Kill | `kill -9 PID`, `killall name` |
| Service control | `systemctl status/start/restart <svc>` |
| Journal | `journalctl` |
| Firewall | `firewall-cmd --add-service=… --permanent && firewall-cmd --reload` |
| Partition / list disks | `fdisk`, `gdisk`, `lsblk`, `blkid` |
| File system / mount | `mkfs.ext4 DEV`, `mount DEV DIR`, `mount -a`, `df -h` |
| Swap | `mkswap`, `swapon`, `swapoff`, `free -h` |
| LVM | `pvcreate`, `vgcreate`, `lvcreate`, `lvextend`, `lvreduce`, `lvremove` (`pvs`/`vgs`/`lvs`) |
| Apache | `yum groupinstall 'Basic Web Server'`, `systemctl start httpd` |
| SELinux | `getenforce`, `setenforce 0|1`, `semanage fcontext`, `restorecon -Rv` |

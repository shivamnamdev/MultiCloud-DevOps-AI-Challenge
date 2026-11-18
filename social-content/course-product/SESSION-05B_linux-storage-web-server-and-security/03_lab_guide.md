# Session 05B lab guide: Linux storage, web server and security layers

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in device names, UUIDs, dates and sizes.

> **The most important thing to know first: SELinux was NOT tested in this guide.** The practice machine we used (a Rocky Linux container on Docker Desktop) runs on a kernel without SELinux, so `getenforce` says `Disabled` and `semanage` refuses to work. Every SELinux step in Episode 4 comes from the script and from the command sheet, not from our test. Run those steps yourself on a real Rocky or AlmaLinux VM. Part D says exactly what we could and could not check.

| | |
|---|---|
| **Time** | Part A 40 min, Part B 50 min, Part C 40 min, Part D 30 min |
| **Cost** | Free on a laptop VM or the practice container. A cloud VM with extra disks bills while it exists. |
| **Skill check before you start** | Sessions 3 to 5: paths, `sudo`, `systemctl`, `ufw` basics, reading `lsblk`. |

## Before you start

The script wants a Rocky Linux or AlmaLinux 9 VM with two empty extra disks (5 GB and 10 GB). If you have that, use it, read `lsblk` first, and use your own device names (`/dev/sdb`, `/dev/vdb`, `/dev/nvme1n1`) wherever the guide says `/dev/loop0` or `/dev/loop1`.

If you do not, you can practise almost everything in a container. Files are in `lab_files/`: `Dockerfile.rocky` (Rocky Linux 9.9 with systemd, LVM, XFS, Apache, firewalld and the SELinux tools) and `make-disks.sh` (makes the two practice "disks").

```bash
docker build -t atithi-rocky:lab -f lab_files/Dockerfile.rocky lab_files
docker run -d --name atithi-rocky --hostname atithi-rocky --privileged --tmpfs /run --tmpfs /run/lock atithi-rocky:lab
docker cp lab_files/make-disks.sh atithi-rocky:/usr/local/bin/make-disks.sh
docker exec -it atithi-rocky bash
make-disks.sh create
```

Expected (ours): `Rocky Linux 9.9 (Blue Onyx)`, `systemctl is-system-running` says `running`, `httpd` and `firewalld` both `active`, and `make-disks.sh create` prints `5 GB disk : /dev/loop0` and `10 GB disk: /dev/loop1`. In the container you are `root`, so leave out `sudo`.

> **Container warnings.** (1) `--privileged` gives the container wide access to the Docker VM. The "disks" are **loop devices**, which are system-wide in that VM. Use this for practice only, and always run `make-disks.sh remove` and delete the container when you finish. (2) A container has **no `udev`**, so two things behave differently from a real VM, and we worked around both: the kernel's partition devices (`/dev/loop0p1`) do not appear in `/dev` by themselves (run `make-disks.sh nodes` after each `fdisk` or `partprobe`), and LVM must be told not to wait for `udev` (the Dockerfile writes `/etc/lvm/lvmlocal.conf` for that). On a real VM you do neither. (3) There is no real boot, so `/etc/fstab` mounts happen only when you run `mount -a`.

We tested on Rocky Linux `9.9`, Apache `2.4.62`, `firewalld 1.3.4`, on Docker Desktop (Mac, arm64).

---

## Part A: floor, walls, shelves, door and the overflow room (Episode 1)

### A1. Look first

```bash
lsblk
sudo blkid
df -h
```

On a real VM: `sda` with the system, and `sdb`, `sdc` empty. In our container `lsblk` listed `loop0` (5G) and `loop1` (10G) among a few unrelated devices of the Docker VM. Read the names before you type any destructive command.

### A2. Partition, format, mount

The script's `fdisk` keys: `n`, `p`, Enter, Enter, `+2G`, `w`. We sent them in one go:

```bash
printf "n\np\n\n\n+2G\nw\n" | fdisk /dev/loop0
partprobe /dev/loop0
make-disks.sh nodes        # the container needs this; a VM does not
lsblk /dev/loop0
mkfs.ext4 /dev/loop0p1
mkdir -p /data
mount /dev/loop0p1 /data
df -h /data
blkid /dev/loop0p1
```

Expected (ours): `Created a new partition 1 of type 'Linux' and of size 2 GiB.`, `loop0p1 259:0 0 2G 0 part`, then after the mount `/dev/loop0p1 2.0G 24K 1.8G 1% /data` and a `blkid` line with `UUID="81ce8d99-..."`, `TYPE="ext4"`. Type `m` inside `fdisk` to list its commands, and note that nothing is written until `w`.

Read the device name twice before `mkfs`: it wipes whatever was there.

### A3. `/etc/fstab`, and why you test before rebooting

```bash
U=$(blkid -s UUID -o value /dev/loop0p1)
echo "UUID=$U  /data  ext4  defaults  0  0" >> /etc/fstab
umount /data
mount -a && echo "mount -a ok"
df -h /data
```

Expected: `mount -a ok` and the mount is back. Now the safety net the script teaches, with a wrong line:

```bash
echo "UUID=00000000-0000-0000-0000-000000000000  /oops  ext4  defaults  0  0" >> /etc/fstab
mkdir -p /oops
mount -a
sed -i "/\/oops/d" /etc/fstab; rmdir /oops
```

Expected (ours): `mount: /oops: can't find UUID=00000000-0000-0000-0000-000000000000.` That error appears while you are still logged in. On a real server the same line left in `fstab` could stop the next boot. **We could not test an actual reboot in a container.**

### A4. Swap

```bash
free -h | grep -i swap
printf "n\np\n2\n\n+1G\nt\n2\n82\nw\n" | fdisk /dev/loop0
partprobe /dev/loop0; make-disks.sh nodes
fdisk -l /dev/loop0 | tail -3
mkswap /dev/loop0p2
swapon /dev/loop0p2
swapon --show
free -h | grep -i swap
U2=$(blkid -s UUID -o value /dev/loop0p2)
echo "UUID=$U2  swap  swap  defaults  0  0" >> /etc/fstab
swapoff /dev/loop0p2; swapon -a; swapon --show
```

What we saw: the partition table showed `/dev/loop0p2 ... 1G 82 Linux swap / Solaris`; `mkswap` printed `Setting up swapspace version 1, size = 1024 MiB`; `swapon --show` listed our partition **and a second swap that was already there** (`/var/lib/swap`, 1024M, belonging to the Docker VM), and `free -h` showed total swap going from `1.0Gi` to `2.0Gi`. After the `fstab` line, `swapon -a` turned it back on. (An earlier run warned `insecure permissions 0644` on the device file. That was our hand-made device node, and `make-disks.sh nodes` now creates it with mode `660`.)

Clean up the A-part before Part B: `swapoff /dev/loop0p2; umount /data`, and delete the two lines we added from `/etc/fstab` (`grep -n UUID /etc/fstab`, then `sed -i '/loop/d;/UUID=/d' /etc/fstab` **only after you have read what it will match**).

**Check yourself:**

- [ ] You can say the four steps in order: disk, partition, file system, mount.
- [ ] You saw `mount -a` catch a bad line.
- [ ] You can say why `fstab` uses a UUID and not `/dev/sdb1`.

---

## Part B: LVM (Episode 2)

### B1. Three layers

Three partitions of type `8e` on the 10 GB disk, then PV, VG and LV:

```bash
printf "n\np\n1\n\n+2G\nt\n8e\nn\np\n2\n\n+2G\nt\n2\n8e\nn\np\n3\n\n+2G\nt\n3\n8e\nw\n" | fdisk /dev/loop1
partprobe /dev/loop1; make-disks.sh nodes
fdisk -l /dev/loop1 | grep -E "^/dev"
pvcreate /dev/loop1p1 /dev/loop1p2
pvs
vgcreate my_vg /dev/loop1p1 /dev/loop1p2
vgs
lvcreate -n my_lv1 -L 1G my_vg
lvs
ls -l /dev/my_vg/
```

Expected (ours): three `2G ... 8e Linux LVM` partitions; `Physical volume ... successfully created`; `vgs` showing `my_vg 2 0 0 wz--n- 3.99g 3.99g` (just under 4 GB, since LVM keeps a little space for its own metadata); `Logical volume "my_lv1" created.`; and `my_lv1 -> /dev/mapper/my_vg-my_lv1`.

**What we hit in the container.** Without the `lvmlocal.conf` setting, `lvcreate` failed with `/dev/my_vg/my_lv1: not found: device not cleared` and `Aborting. Failed to wipe start of new LV.` That is the missing `udev`. It does not happen on a real VM.

Make a file system and mount it:

```bash
mkfs.ext4 /dev/my_vg/my_lv1
mkdir -p /events
echo "/dev/my_vg/my_lv1  /events  ext4  defaults  0  0" >> /etc/fstab
mount -a
df -h /events
```

Expected: `/dev/mapper/my_vg-my_lv1 974M ... /events`. (A 1 GiB volume shows about `974M` usable.) The script's fstab line can also use the UUID instead of the device path, as in Part A.

### B2. Grow it, with and without `-r`

```bash
lvextend -r -L +1G /dev/my_vg/my_lv1
df -h /events
lvextend -L 3G /dev/my_vg/my_lv1
df -h /events
resize2fs /dev/my_vg/my_lv1
df -h /events
pvcreate /dev/loop1p3
vgextend my_vg /dev/loop1p3
vgs
```

What we saw: `lvextend -r -L +1G` printed `Extended file system ext4 on my_vg/my_lv1.` and `df` said `2.0G`, with the file system mounted and working all the time. `lvextend -L 3G` (no `+`, no `-r`) made the LV `3G` in total, but `df` still said `2.0G`: **the LV grew, the file system did not**. `resize2fs` fixed it: `3.0G`. After `vgextend` the pool showed `my_vg 3 1 0 wz--n- <5.99g <2.99g`.

### B3. Shrink (ext4 only), and the XFS limit

```bash
echo hello > /events/keep.txt; sync
lvreduce -r -f -L 700M /dev/my_vg/my_lv1        # while mounted
umount /events
lvreduce -r -f -L 1G /dev/my_vg/my_lv1
mount -a; df -h /events; cat /events/keep.txt
```

What we saw: with the file system **mounted**, `lvreduce -r` asked `Continue with ext4 file system reduce steps: unmount, fsck, resize2fs? [y/n]:[n]` and, because it ran non-interactively, ended with `File system not reduced.` (That is the script's rule: unmount first.) After `umount`, it ran `fsck`, shrank the file system to `262144 (4k) blocks`, then the LV: `Size of logical volume ... changed from 3.00 GiB (768 extents) to 1.00 GiB (256 extents)`, and `/events` came back at `974M` with `keep.txt` still saying `hello`.

XFS cannot shrink:

```bash
lvcreate -n xfs_lv -L 1G my_vg
mkfs.xfs /dev/my_vg/xfs_lv
mkdir -p /xfsdir; mount /dev/my_vg/xfs_lv /xfsdir; umount /xfsdir
lvreduce -r -f -L 512M /dev/my_vg/xfs_lv
mount /dev/my_vg/xfs_lv /xfsdir
lvextend -r -L +512M /dev/my_vg/xfs_lv; df -h /xfsdir
umount /xfsdir; lvremove -f my_vg/xfs_lv; rmdir /xfsdir
```

Expected (ours): `File system size (1.00 GiB) is larger than the requested size (512.00 MiB).` and `File system reduce is required and not supported (xfs).`; the extend worked, `Extended file system xfs on my_vg/xfs_lv.`, and `df` showed `1.5G`.

### B4. Remove, in the right order

```bash
umount /events
lvremove -f my_vg/my_lv1
mount -a
sed -i '\|/events|d' /etc/fstab
mount -a && echo clean
rmdir /events
vgremove -f my_vg
pvremove -f /dev/loop1p1 /dev/loop1p2 /dev/loop1p3
```

We deliberately ran `mount -a` **before** removing the `fstab` line, and saw `mount: /events: special device /dev/my_vg/my_lv1 does not exist.` After deleting the line, `mount -a` was clean. That is the "supervisor goes to open a door that is gone" of the script. (Our container's system disk is not on LVM, so we could **not** check the script's remark that `lsblk` shows `rl-root` on a real Rocky install.)

### B5. Clean up the practice disks

```bash
make-disks.sh remove
losetup -a
```

Expected: no output from `losetup -a`. After removing the container we also checked that no `loop` devices and no `/dev/mapper` entries (other than `control`) were left in the Docker VM.

**Check yourself:**

- [ ] You built a PV, a VG and an LV and read each with `pvs`, `vgs`, `lvs`.
- [ ] You saw the LV grow while the file system stayed small, then fixed it.
- [ ] You saw XFS refuse to shrink.
- [ ] You can give the order for removing an LV.

---

## Part C: Apache and firewalld (Episode 3)

### C1. The department and its map

```bash
systemctl is-active httpd firewalld
httpd -v | head -1
curl -sI localhost | head -3
grep apache /etc/passwd
grep -E "^(DocumentRoot|ServerRoot)" /etc/httpd/conf/httpd.conf
```

In our image `httpd` was already enabled and running (the Dockerfile enables it; on a VM you run `dnf install -y httpd` and `systemctl enable --now httpd`). We saw `Apache/2.4.62 (Rocky Linux)`, the user `apache:x:48:48:Apache:/usr/share/httpd:/sbin/nologin` (no login), `ServerRoot "/etc/httpd"` and `DocumentRoot "/var/www/html"`.

**The first `curl -I localhost` printed `HTTP/1.1 403 Forbidden`**, not `200`. The folder `/var/www/html` was empty and Apache does not list folders. Write a page and it works:

```bash
echo "<h1>Atithi Hotels: Swagat hai</h1>" > /var/www/html/index.html
curl -sI localhost | head -1
```

Expected: `HTTP/1.1 200 OK`. (The script says "jawab aa gaya" for the first call; a 403 is also an answer, but it is not the page.)

### C2. firewalld

```bash
firewall-cmd --get-default-zone
firewall-cmd --get-zones
firewall-cmd --list-all
```

Expected (ours): `public`; `block dmz drop external home internal public trusted work`; and in `list-all`: `services: cockpit dhcpv6-client ssh`, `masquerade: no`. No `http` yet, as the script says.

Now the guard, from outside. We used a throwaway container as the guest (replace the IP with your machine's):

```bash
IP=$(docker inspect atithi-rocky --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
docker run --rm curlimages/curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://$IP/
firewall-cmd --add-service=http --permanent
firewall-cmd --list-services
firewall-cmd --reload
firewall-cmd --list-services
docker run --rm curlimages/curl -s -m 5 http://$IP/
```

What we saw: first `000` (timed out); after `--add-service=http --permanent` the running list was still `cockpit dhcpv6-client ssh` (**permanent does not change the live rules**); after `--reload` it was `cockpit dhcpv6-client http ssh`; and the last call printed `<h1>Atithi Hotels: Swagat hai</h1>`. That is the two-diary rule of the script, observed.

A port instead of a service: `firewall-cmd --permanent --add-port=8080/tcp; firewall-cmd --reload; firewall-cmd --list-ports` printed `8080/tcp`.

### C3. `block` against `drop`

The script says `block` answers "no", while `drop` stays silent. We put the guest's whole network (`172.17.0.0/16`, the Docker network) into each zone:

```bash
firewall-cmd --zone=block --add-source=172.17.0.0/16
docker run --rm curlimages/curl -sS -m 4 http://$IP/
firewall-cmd --zone=block --remove-source=172.17.0.0/16
firewall-cmd --zone=drop --add-source=172.17.0.0/16
docker run --rm curlimages/curl -sS -m 4 http://$IP/
firewall-cmd --zone=drop --remove-source=172.17.0.0/16
```

What we saw: with `block`, **an instant** `curl: (7) Failed to connect ... Could not connect to server` (about 0.0002 s). With `drop`, **a 4 second wait** and `curl: (28) Connection timed out after 4006 milliseconds`. After removing the source, `200` again. These changes were runtime only (no `--permanent`), so a `--reload` would have removed them anyway.

### C4. A new DocumentRoot (the first part of the script's "403")

```bash
cp /etc/httpd/conf/httpd.conf /root/httpd.conf.bak
mkdir -p /web; echo "<h1>from /web</h1>" > /web/index.html
sed -i 's|^DocumentRoot "/var/www/html"|DocumentRoot "/web"|; s|^<Directory "/var/www/html">|<Directory "/web">|' /etc/httpd/conf/httpd.conf
apachectl configtest
systemctl restart httpd
ls -ld /web; curl -sI localhost | head -1; curl -s localhost
```

What we saw: `Syntax OK` (with a harmless `AH00558 ... Could not reliably determine the server's fully qualified domain name` warning), `drwxr-xr-x ... /web`, `HTTP/1.1 200 OK` and `<h1>from /web</h1>`. **In the script this same step ends in `403 Forbidden`, because SELinux blocks the new folder.** In our container there is no SELinux, so we got `200` and **could not reproduce that 403**.

We did produce a 403 a different way, and it is worth knowing: change only the `DocumentRoot` line and leave the `<Directory>` block at the old path:

```bash
sed -i 's|^<Directory "/web">|<Directory "/var/www/html">|' /etc/httpd/conf/httpd.conf
apachectl configtest; systemctl restart httpd
curl -sI localhost | head -1
tail -2 /var/log/httpd/error_log
```

We saw `Syntax OK` (the config is valid, just wrong), `HTTP/1.1 403 Forbidden`, and in the error log: `[authz_core:error] ... AH01630: client denied by server configuration: /web/`. **That wording means Apache's own config refused it, not SELinux.** So check the Apache error log first: if it says "denied by server configuration", fix the `Directory` block. If the log is silent and the permissions are right, then look at SELinux (`/var/log/audit/audit.log`). The script now says this. Restore: `cp /root/httpd.conf.bak /etc/httpd/conf/httpd.conf; systemctl restart httpd; rm -rf /web`.

**Check yourself:**

- [ ] You saw `http` missing, then added, then live after `--reload`.
- [ ] You can say how `block` and `drop` differ from the guest's side.
- [ ] You can name two different causes of a 403.

---

## Part D: SELinux (not tested) and NAT (Episode 4)

### D1. SELinux: what we could check

```bash
getenforce
ls /sys/fs/selinux
which semanage restorecon ausearch
semanage fcontext -l
```

What we saw in the container: `Disabled`; `ls: cannot access '/sys/fs/selinux'`; `semanage` and `restorecon` and `getenforce` were installed, but `ausearch` was **not** (it belongs to the `audit` package, which is on a normal Rocky install but not in our minimal image); and `semanage fcontext -l` failed with `ValueError: SELinux policy is not managed or store cannot be accessed.` So **we ran none of**: `ls -Z`, `ps -eZ`, `setenforce`, the `ausearch -m AVC` denial, `semanage fcontext -a`, or `restorecon -Rv`.

For you, on a real Rocky or AlmaLinux VM, the script's lab is the one to do: make `/web` and see the 403 with `Syntax OK`; read the denial with `sudo ausearch -m AVC -ts recent`; **prove** the cause with `sudo setenforce 0` (200), then `sudo setenforce 1` straight away; then fix the label (`sudo semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"`, then `sudo restorecon -Rv /web`), check with `ls -ldZ /web`, and confirm `200` with SELinux **enforcing**. Never "fix" it by setting `SELINUX=disabled`. If `semanage` is missing: `sudo dnf install -y policycoreutils-python-utils`.

### D2. NAT: masquerade and port forwarding

```bash
firewall-cmd --permanent --add-masquerade
firewall-cmd --permanent --add-forward-port=port=8080:proto=tcp:toport=80
firewall-cmd --reload
firewall-cmd --list-all | grep -E "masquerade|ports"
curl -s -m 3 -o /dev/null -w '%{http_code}\n' localhost:8080
docker run --rm curlimages/curl -s -m 5 -o /dev/null -w '%{http_code}\n' http://$IP:8080/
```

What we saw: `masquerade: yes` and `ports: 8080/tcp` (we had opened 8080 earlier, so the port was open on top of the forward; in the script the forward alone is the point), the line `forward-ports:` itself printed **empty** in our `grep`, even though the forward worked from outside (read the whole `--list-all` output, we did not look into why). From **inside** (`localhost:8080`): `000`, nothing. From **outside** (`$IP:8080`): `200`, the Apache page. The script's warning is right: the rule works for traffic coming from outside, not for the machine's own `localhost`. We **did not test** forwarding to another machine (`toaddr=`), or that masquerade really rewrites the sender's address for a second machine behind this one: that needs a three-machine setup.

A rich rule, from the script's handout, with our own addresses:

```bash
firewall-cmd --permanent --add-rich-rule='rule family="ipv4" source address="172.17.0.0/16" service name="http" reject'
firewall-cmd --reload
firewall-cmd --list-rich-rules
docker run --rm curlimages/curl -sS -m 5 http://$IP/
```

Expected (ours): the rule listed back, and the guest got `curl: (7) Failed to connect ... Could not connect to server` instantly (`reject` answers "no"). Remove the test rules afterwards:

```bash
firewall-cmd --permanent --remove-rich-rule='rule family="ipv4" source address="172.17.0.0/16" service name="http" reject'
firewall-cmd --permanent --remove-masquerade
firewall-cmd --permanent --remove-forward-port=port=8080:proto=tcp:toport=80
firewall-cmd --permanent --remove-port=8080/tcp
firewall-cmd --reload
```

**Check yourself:**

- [ ] You know which steps of this part you have **not** run yet (all the SELinux ones) and plan to run them on a real VM.
- [ ] You saw port forwarding work from outside and not from `localhost`.

---

## Clean up

```bash
make-disks.sh remove          # inside the container
docker rm -f atithi-rocky     # outside
docker rmi atithi-rocky:lab curlimages/curl
```

Check afterwards that nothing is left in the Docker VM: `docker run --rm --privileged alpine sh -c 'losetup -a; ls /dev/mapper'` should show no loop devices and only `control`. In our first cleanup attempt one loop device stayed attached (shown as `(deleted)`). Removing the container released it. We did not find out exactly why, so do the `swapoff`, the `umount` and `make-disks.sh remove` in that order, and check `losetup -a`.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `/dev/loop0p1: No such file or directory` after `fdisk` | Container has no `udev` | `make-disks.sh nodes` |
| `lvcreate`: `device not cleared`, `Failed to wipe start of new LV` | Container has no `udev` | The `lvmlocal.conf` from the Dockerfile |
| `mount -a` errors after you remove an LV | Its line is still in `/etc/fstab` | Delete the line |
| `lvreduce` says `File system not reduced` | It is mounted, or the answer defaulted to no | `umount` first |
| `File system reduce is required and not supported (xfs)` | XFS cannot shrink | Back up, re-create smaller, restore |
| `curl localhost` gives 403 with `Syntax OK` | Empty `DocumentRoot`, a wrong `Directory` block, or SELinux | Apache `error_log` first, then SELinux |
| A firewall rule disappears on reload | You forgot `--permanent` | Add it, then `--reload` |
| Rule added but not live | Added only with `--permanent` | `firewall-cmd --reload` |
| `Unable to find image` loop leftovers in the Docker VM | A loop device was still in use | `losetup -d` after `swapoff` and `umount` |

## What we did not test

- **SELinux, all of it:** modes, labels, `ausearch`, `semanage fcontext`, `restorecon`, and the 403 caused by it.
- **A real Rocky or AlmaLinux VM:** real disks (`/dev/sdb`), a real reboot with `/etc/fstab`, the system disk on LVM (`rl-root`), MBR against GPT with `gdisk`, `dnf install` of the packages on a fresh machine (our image installed them at build time), and NetworkManager.
- **NAT between machines:** masquerade for a second machine, and forwarding with `toaddr`.
- **A cloud disk:** attaching and extending an EBS volume (Session 10).
- **Hot-adding a disk,** and growing a partition itself.

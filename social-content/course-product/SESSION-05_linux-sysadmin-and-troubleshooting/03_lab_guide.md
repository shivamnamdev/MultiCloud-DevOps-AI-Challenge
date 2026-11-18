# Session 05 lab guide: Linux sysadmin and troubleshooting

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in PIDs, times and sizes.

| | |
|---|---|
| **Time** | Part A 30 min, Part B 40 min, Part C 40 min, Part D 20 min |
| **Cost** | Free with the practice container. A cloud VM can bill: stop it afterwards. |
| **Skill check before you start** | Sessions 3 and 4: the shell, `grep` and pipes, `sudo`, file permissions. |

## Before you start

We used the practice "building" from Sessions 3 and 4: Ubuntu 24.04 in a container with systemd, `sshd`, `rsyslog`, `ufw` and `nginx` installed on top. The Dockerfile is in `lab_files/`.

```bash
docker build -t atithi-ubuntu:lab -f lab_files/Dockerfile.ubuntu lab_files
docker run -d --name atithi-web1 --hostname atithi-web1 --privileged --tmpfs /run --tmpfs /run/lock atithi-ubuntu:lab
docker exec -u root atithi-web1 bash -c 'apt-get update && apt-get install -y nginx'
docker exec -it -u ubuntu -w /home/ubuntu atithi-web1 bash
```

(`--privileged` lets systemd and `ufw` work inside Docker. Use it for practice only.) The commands below say `sudo` where a real server would need it. The practice user `ubuntu` has `sudo` with the password `ubuntu`. We ran the admin commands as `root` through `docker exec -u root`.

> **What is different in a container.** `uptime`, `free`, `nproc` and the kernel messages in `journalctl` describe the **Docker VM** that all containers share, not just your container (we saw `up 2 days`, `7.7Gi` of memory and `12` CPUs, and even kernel messages about other containers being killed). A container has no `netplan` or `NetworkManager`, and `ip a` shows a virtual `eth0`. Everything about processes, services, logs and `ufw` behaves as on a VM.
>
> We also found that a **normal user** could not run `systemctl is-active` at first: it said `Failed to connect to bus`. The container needed the `dbus` package, which the Dockerfile now installs. On a real Ubuntu server it is already there.

---

## Part A: the manager's round and the work orders (Episode 1)

### A1. The four commands

```bash
uptime
nproc
free -h
df -h /
du -sh /var/log /etc
top -bn1 | head -5
```

Expected (shape; our container numbers): a load average line (`load average: 0.01, 0.07, 0.16`), `12` from `nproc`, a `Mem:` line whose `available` column is the number that matters (`6.2Gi` of `7.7Gi`), a `Swap:` line (`1.0Gi` total), `overlay 453G 26G 404G 6% /`, and the `top` header with `Tasks: 27 total, 1 running, 26 sleeping, 0 stopped, 0 zombie`. Compare the load average with `nproc`: a load of 12 on 12 CPUs is full, but the same load on 4 CPUs means waiting work.

### A2. PID, PPID and STAT

```bash
ps -ef | head -3
ps -ef | grep -E "sshd|nginx" | grep -v grep
ps -eo pid,ppid,stat,cmd | head -5
```

In our container: `/sbin/init` was PID `1` with PPID `0`; `sshd` and the `nginx` master had PPID `1` (the shift supervisor started them), and the nginx worker's PPID was the master's PID. That is the tree from the script.

### A3. The CPU lab

```bash
yes > /dev/null &
Y=$!
ps -o pid,ppid,stat,cmd -C yes
top -bn1 | sed -n 7,9p
kill -STOP $Y; ps -o pid,ppid,stat,cmd -C yes
kill -CONT $Y; ps -o pid,ppid,stat,cmd -C yes
kill $Y; sleep 1; ps -C yes -o pid= | wc -l
```

What we saw: `STAT R` and `yes` at `100.0` %CPU on top of `top`; after `kill -STOP` the state was `T`; after `kill -CONT` it was `R` again; after `kill` the count was `0`. The PPID of `yes` was our shell's PID.

### A4. Zombies, orphans and the two kinds of kill

A zombie needs a parent that never collects its child. This Python one-liner makes one (leave it running in the background):

```bash
python3 - <<"PY" &
import os,time
pid=os.fork()
if pid==0: os._exit(0)
time.sleep(30)
PY
sleep 1
ps -eo pid,ppid,stat,cmd | grep " Z" | grep -v grep
```

Expected (ours): `459  457 Z  [python3] <defunct>`: a process in state `Z`. Now try to kill it:

```bash
ZP=$(ps -eo pid,stat | awk '$2 ~ /^Z/{print $1}' | head -1)
PP=$(ps -o ppid= -p $ZP | tr -d ' ')
kill -9 $ZP; sleep 1; ps -p $ZP -o stat=
kill $PP; sleep 1; ps -p $ZP -o stat=
```

What we saw: after `kill -9` on the zombie it was **still `Z`**. After we killed its **parent**, it was gone. That is the script's claim, observed.

An orphan:

```bash
bash -c "sleep 120 & disown; exit"
ps -eo pid,ppid,cmd | grep "sleep 120" | grep -v grep
```

Expected (ours): `480  1  sleep 120`: PPID `1`. systemd adopted the orphan. (Clean it up with `killall sleep`. **Do not** use `pkill -f "sleep 120"` inside the same shell line: the pattern matches your own command line and kills your shell. We did that by mistake and got exit code 143.)

`kill` against `kill -9`:

```bash
bash -c 'trap "" TERM; exec sleep 100' &
P=$!; sleep 1
kill $P; sleep 1; ps -p $P -o stat=
kill -9 $P; sleep 1; ps -p $P -o stat=
```

We saw `S` after the polite `kill` (the process ignored SIGTERM) and nothing after `kill -9`. `killall yes` stopped two `yes` processes at once (count `2` then `0`).

### A5. `/proc`

`ls /proc/1` listed `attr`, `autogroup`, `auxv`, `cgroup` and more; `cat /proc/1/comm` printed `systemd`. The kernel keeps every process's status there.

**Check yourself:**

- [ ] You turned a process from `R` to `T` and back.
- [ ] You made a zombie and saw `kill -9` fail on it.
- [ ] You can say who adopts an orphan.

---

## Part B: services and logs (Episode 2)

### B1. `start`, `enable`, `reload`, `restart`

```bash
sudo systemctl disable nginx
systemctl is-enabled nginx; systemctl is-active nginx
sudo systemctl enable --now nginx
systemctl is-enabled nginx
a=$(systemctl show -p MainPID --value nginx)
sudo systemctl reload nginx;  b=$(systemctl show -p MainPID --value nginx)
sudo systemctl restart nginx; c=$(systemctl show -p MainPID --value nginx)
echo "pid before=$a after reload=$b after restart=$c"
systemctl status nginx --no-pager | head -4
```

What we saw: after `disable`, `is-enabled` said `disabled` while `is-active` said `active` (**running now, not on the morning list**). `enable --now` created the symlink and `is-enabled` said `enabled`. The main PID was `385` before, `385` after `reload` (same process: guests not disturbed) and `662` after `restart` (a new process). The status header read `Loaded: ... enabled; preset: enabled` and `Active: active (running)`.

### B2. Logs

```bash
journalctl -u nginx -n 3 --no-pager
journalctl -p err --since "1 hour ago" --no-pager | tail -3
ls /var/log
ls -d /var/log/journal /run/log/journal
grep -E "^(weekly|rotate)" /etc/logrotate.conf
grep -n "auth" /etc/rsyslog.d/50-default.conf
sudo grep COMMAND /var/log/auth.log | tail -2
```

Expected (ours): the last three lines showed `Stopped`, `Starting` and `Started nginx.service`; `/var/log` held `auth.log`, `syslog`, `kern.log`, `nginx`, `journal` and others; **both** `/var/log/journal` and `/run/log/journal` existed; `weekly` and `rotate 4`; and line 8 of the rsyslog file `auth,authpriv.* /var/log/auth.log`, so login and `sudo` lines go to `auth.log` on Ubuntu, as the script says. (The `-p err` output in a container includes kernel messages from the Docker VM about other containers. On a normal VM it shows your machine only.)

### B3. Break nginx and fix it

```bash
sudo cp /etc/nginx/nginx.conf /root/nginx.conf.bak
sudo sed -i 's/^worker_processes auto;/worker_processes auto/' /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl restart nginx
systemctl is-active nginx
systemctl status nginx --no-pager | head -4
journalctl -u nginx -n 6 --no-pager | grep -iE "emerg|failed"
sudo cp /root/nginx.conf.bak /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl restart nginx; systemctl is-active nginx; systemctl is-enabled nginx
```

Expected (ours):

```
[emerg] 702#702: invalid number of arguments in "worker_processes" directive in /etc/nginx/nginx.conf:3
nginx: configuration file /etc/nginx/nginx.conf test failed
Job for nginx.service failed because the control process exited with error code.
failed
× nginx.service - A high performance web server and a reverse proxy server
     Active: failed (Result: exit-code) ...
```

The journal repeated the same `[emerg]` line and `Failed to start nginx.service`. **The line number was `3`, but the missing `;` was on line `2`.** The parser notices the problem when it reaches the next line, so look at the line above the one it names. After the fix: `syntax is ok`, `test is successful`, `active`, `enabled`.

**Check yourself:**

- [ ] You can say what `start` and `enable` each do, with evidence from `is-active` and `is-enabled`.
- [ ] You saw the same PID after `reload` and a new PID after `restart`.
- [ ] You found the nginx error in the journal, and know to look one line up.

---

## Part C: the network (Episode 3)

### C1. Address, door and outside

```bash
ip -br a | grep -v NONE
ip route | head -2
ss -tulpn | grep -E ":(22|80) "
ping -c 2 -W 2 8.8.8.8
curl -sI https://example.com | head -1
curl -sI http://localhost | head -2
dig example.com +short
dig doesnotexist.invalid +short; echo "exit=$?"
```

Expected (ours): `eth0@if1023 UP 172.17.0.3/16`; `default via 172.17.0.1 dev eth0`; `LISTEN` lines for `0.0.0.0:22` (`sshd`) and `0.0.0.0:80` (`nginx`), plus `[::]` versions; `2 packets transmitted, 2 received, 0% packet loss`; `HTTP/2 200` from example.com; `HTTP/1.1 200 OK` and `Server: nginx/1.24.0 (Ubuntu)` locally; two IP addresses from `dig`; and **nothing printed, with exit code 0**, for the name that does not exist. `dig` succeeds even when the answer is empty, so check the output, not only the exit code. (`ip a` in the container also lists unused `tunl0`, `gre0`... devices. Ignore them.)

### C2. Static IP: the file, checked but not applied

A container has no `netplan` by default, and changing a network address in a shared Docker VM is not something to do for practice. So we only **checked** the YAML. `lab_files/01-config.yaml.example` is the script's idea in a complete file (change the names and addresses to match your `ip a` and `ip route`):

```bash
sudo apt-get install -y netplan.io
sudo cp lab_files/01-config.yaml.example /etc/netplan/01-config.yaml
sudo chmod 600 /etc/netplan/01-config.yaml
sudo netplan generate
cat /run/systemd/network/10-netplan-enp0s3.network
```

What we saw: no error from `netplan generate` (apart from `Failed to send reload request`, because nothing in a container reloads the network), and the rendered file contained `Address=192.168.0.50/24`, `DNS=8.8.8.8`, `DNS=1.1.1.1` and a route `Destination=0.0.0.0/0` with `Gateway=192.168.0.1`. Two errors we provoked on purpose:

- An indentation slip: `/etc/netplan/02-bad.yaml:8:16: Invalid YAML: inconsistent indentation:` with a caret under the problem.
- A world-readable file (`chmod 644`): `WARNING: Permissions for /etc/netplan/01-config.yaml are too open. Netplan configuration should NOT be accessible by others.`

Remove the test files afterwards (`sudo rm /etc/netplan/*.yaml`). **We did not run `netplan try` or `netplan apply`, and we did not test `nmtui` or `nmcli`** (they belong to the Red Hat family part, Session 5B). Run `netplan try` only on your own **local** VM, with the console open, exactly as the script says.

### C3. `ufw`, from inside and from outside

You need a second machine to be the guest. In Docker, a throwaway container does that job:

```bash
IP=$(docker inspect atithi-web1 --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}')
docker run --rm curlimages/curl -s -m 4 -o /dev/null -w '%{http_code}\n' http://$IP/
```

Expected (ours): `200`. No firewall yet. Now, inside the building:

```bash
sudo ufw status
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status verbose
```

We saw `Status: inactive` first; `Rules updated` and `Rules updated (v6)`; `Firewall is active and enabled on system startup`; and then `Default: deny (incoming), allow (outgoing), deny (routed)` with `22/tcp (OpenSSH) ALLOW IN Anywhere`. (`ufw enable` normally asks you to confirm. We piped in a `y` with `echo y |`.) The four checks of the script, in order:

```bash
ss -tulpn | grep :80
curl -s -o /dev/null -w "inside: %{http_code}\n" http://localhost/
docker run --rm curlimages/curl -s -m 5 -o /dev/null -w 'outside: %{http_code}\n' http://$IP/
sudo ufw allow 80/tcp
docker run --rm curlimages/curl -s -m 5 -o /dev/null -w 'outside: %{http_code}\n' http://$IP/
```

What we saw: `inside: 200` but the first outside call gave **`000`** (it timed out, the guard dropped it), and after `ufw allow 80/tcp` the outside call gave **`200`**. `ufw status` then listed `OpenSSH`, `80/tcp` and their `(v6)` twins. Turn the firewall off again when you are done: `sudo ufw --force disable`.

The warning of the script, **allow SSH before you enable the firewall**, is the lesson here: in this container we had the console (`docker exec`), but on a remote VM `ufw enable` without an SSH rule locks you out.

**Check yourself:**

- [ ] You can name the five stops of the script's route, and which command checks each.
- [ ] You saw a service answer on `localhost` but not from outside, and fixed it at the firewall.

---

## Part D: the method and the health-check script (Episode 4)

The five steps are reading and habit, so use them on Parts B and C: write the symptom, ask what changed, read the logs, test one idea, verify and write it down. In B3 the symptom was "`restart` fails", what changed was one line in `nginx.conf`, the log told you the line, you changed one thing, and you verified with `nginx -t` and `is-active`.

### D1. The script

`lab_files/healthcheck.sh` is the script from Episode 4, unchanged:

```bash
#!/usr/bin/env bash
disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -ge 90 ]; then echo "FAIL disk ${disk}%"; fail=1; else echo "OK   disk ${disk}%"; fi
if systemctl is-active --quiet nginx; then echo "OK   nginx"; else echo "FAIL nginx"; fail=1; fi
exit ${fail:-0}
```

```bash
chmod +x healthcheck.sh
./healthcheck.sh; echo "exit=$?"
sudo systemctl stop nginx
./healthcheck.sh; echo "exit=$?"
sed 's/-ge 90/-ge 1/' healthcheck.sh > hc2.sh; bash hc2.sh; echo "exit=$?"
sudo systemctl start nginx
```

Expected (ours):

```
OK   disk 6%
OK   nginx
exit=0
OK   disk 6%
FAIL nginx
exit=1
FAIL disk 6%
FAIL nginx
exit=1
```

The last run lowers the "full" threshold to 1% to prove the disk branch can fail too. Without the `dbus` package, our first attempt printed `Failed to connect to bus: No such file or directory` and `FAIL nginx` **even while nginx was running**, because a normal user in the container could not reach systemd. A health check that cries wolf is the problem the script warns about: test both the pass and the fail path.

**Check yourself:**

- [ ] Your script exits `0` when well and `1` when not.
- [ ] You tested the failing path on purpose.

---

## Clean up

```bash
docker rm -f atithi-web1
docker rmi atithi-ubuntu:lab
docker rmi curlimages/curl
```

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `Failed to connect to bus` as a normal user | No `dbus` in the image | Use the lab Dockerfile (or install `dbus`) |
| Your shell dies after `pkill -f "pattern"` | The pattern matched your own command | Use `killall name` or the PID |
| `nginx -t` names the wrong line | The parser reports where it noticed, not where you slipped | Look at the line above |
| `ufw enable` locks you out of SSH | No SSH rule first | `sudo ufw allow OpenSSH` before `enable` |
| `curl` works on `localhost`, fails from outside | Firewall, or the app listens only on `127.0.0.1` | `ss -tulpn`, then `ufw status` |
| `dig` prints nothing | The name has no answer, but `dig` still exits `0` | Read the output |
| `netplan generate` says "Invalid YAML" | Indentation | Fix with spaces, never tabs |

## What we did not test

- **A real VM:** real memory pressure and swap behaviour, `top` under real load, the real boot, and `netplan try` / `netplan apply`.
- **`nmtui`, `nmcli`** and the Red Hat family's `firewalld` (see the Session 5B guide).
- **`logrotate` actually rotating a file** (we read the config only), and a journal that does **not** persist (our image keeps one on disk).
- **The D (uninterruptible sleep) process state** and a real out-of-memory kill of a service.
- **Cloud security groups,** the "other guard" the script mentions.

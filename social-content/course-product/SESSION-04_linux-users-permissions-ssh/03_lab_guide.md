# Session 04 lab guide: Linux users, permissions and SSH

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in dates, hashes, sizes and process numbers.

| | |
|---|---|
| **Time** | Part A 30 min, Part B 30 min, Part C 30 min, Part D 20 min |
| **Cost** | Free with the practice container. If you use a cloud VM, stop it after the lab. |
| **Skill check before you start** | Session 3: paths, `ls -l`, `cat`, redirects. |

## Before you start

You need an Ubuntu 24.04 machine where you may use `sudo`. We tested in the practice container from Session 3. If you did not build it, build it now (the Dockerfile is in `lab_files/`):

```bash
docker build -t atithi-ubuntu:lab -f lab_files/Dockerfile.ubuntu lab_files
docker run -d --name atithi-web1 --hostname atithi-web1 --privileged --tmpfs /run --tmpfs /run/lock atithi-ubuntu:lab
docker exec -it -u ubuntu -w /home/ubuntu atithi-web1 bash
```

`--privileged` lets systemd run in the container. Use it for practice only. The container runs `sshd` and `rsyslog`, so SSH and `/var/log/auth.log` work. Our tests ran as `root` through `docker exec -u root` for the admin commands (the same effect as `sudo`) and as the staff users when the point was to see what a normal user can do. We tested on Ubuntu `24.04.5 LTS`.

> **Container note.** A container has no real boot, no bootloader and no network card of its own. The boot-process part of Episode 4 is reading, plus `systemctl get-default`. Everything else in this session works in the container exactly as on a VM.

---

## Part A: staff, departments and the ID card (Episode 1)

### A1. A new user

```bash
sudo useradd -m -s /bin/bash -c "Asha Verma" asha
tail -1 /etc/passwd
echo "asha:asha1" | sudo chpasswd
id asha
sudo useradd -m -u 2001 -s /bin/bash ravi
id ravi
ls -l /etc/passwd /etc/shadow
su asha -c "cat /etc/shadow"
```

Expected (ours):

```
asha:x:1001:1001:Asha Verma:/home/asha:/bin/bash
uid=2001(ravi) gid=2001(ravi) groups=2001(ravi)
-rw-r--r-- 1 root root   1144 ... /etc/passwd
-rw-r----- 1 root shadow  769 ... /etc/shadow
cat: /etc/shadow: Permission denied
```

Seven fields in the register line, a literal `x` for the password, and the hash in `/etc/shadow`, which an ordinary user cannot read. `asha` got UID `1001` because we gave no `-u` (the next free number after the built-in `ubuntu` user). (`echo ... | chpasswd` sets a password without typing. On a real server use `sudo passwd asha` and type it.)

### A2. Groups, and the `-a` trap

```bash
sudo groupadd devs; sudo groupadd qa
sudo usermod -aG devs,qa asha; id asha
sudo usermod -G devs asha; id asha
sudo usermod -aG qa asha
sudo gpasswd -d asha devs; id asha
sudo useradd -m -g devs -G qa kiran; id kiran
```

What we saw:

- After `-aG devs,qa`: `groups=1001(asha),2002(devs),2003(qa)`.
- After `usermod -G devs asha` (no `-a`): `groups=1001(asha),2002(devs)`. **`qa` is gone.** That is the trap from the script.
- After adding `qa` back and `gpasswd -d asha devs`: `Removing user asha from group devs`, and `groups=1001(asha),2003(qa)`.
- `useradd -g devs -G qa kiran` gave `gid=2002(devs) groups=2002(devs),2003(qa)`: `-g` is the one primary group, `-G` the extras.

### A3. Password policy

```bash
sudo chage -l asha
sudo chage -M 90 -m 1 -W 7 asha
sudo chage -l asha
grep -E "^(PASS_MAX_DAYS|PASS_MIN_DAYS|PASS_WARN_AGE|UID_MIN|UID_MAX)" /etc/login.defs
```

Before: `Password expires : never`, minimum `0`, maximum `99999`, warning `7`. After: minimum `1`, maximum `90`, warning `7`. The defaults in `/etc/login.defs` (ours): `PASS_MAX_DAYS 99999`, `PASS_MIN_DAYS 0`, `PASS_WARN_AGE 7`, `UID_MIN 1000`, `UID_MAX 60000`.

### A4. Lock, unlock and remove (with a gotcha)

```bash
sudo usermod -L ravi; sudo grep ^ravi /etc/shadow | cut -c1-12
sudo usermod -U ravi
```

Our `ravi` had **no password at all**. The lock showed `ravi:!:20775`, and the unlock **refused**:

```
usermod: unlocking the user's password would result in a passwordless account.
You should set a password with usermod -p to unlock this user's password.
```

So give the user a password first, then try again with `kiran`:

```bash
echo "kiran:kiran1" | sudo chpasswd
sudo grep ^kiran /etc/shadow | cut -c1-14
sudo usermod -L kiran; sudo grep ^kiran /etc/shadow | cut -c1-14
sudo usermod -U kiran; sudo grep ^kiran /etc/shadow | cut -c1-14
```

Expected (ours): `kiran:$y$j9T$K`, then `kiran:!$y$j9T$` (the lock is a `!` in front of the hash), then `kiran:$y$j9T$K` again. Finally:

```bash
sudo userdel -r ravi; ls /home; id ravi
```

We saw `userdel: ravi mail spool (/var/mail/ravi) not found` (harmless), `/home` without `ravi`, and `id: 'ravi': no such user`.

### A5. `sudo`

```bash
su - asha
id
apt-get update
sudo -n true
exit
sudo usermod -aG sudo asha
su - asha -c "id; sudo apt-get update | tail -2"
```

Before the group: `apt-get update` died with `E: List directory /var/lib/apt/lists/partial is missing. - Acquire (13: Permission denied)` and `sudo: a password is required`. After `-aG sudo`: `groups=1001(asha),27(sudo),2003(qa)` and the update fetched about 36 MB. (A running `su - asha` session needs a fresh login to see a new group.)

The sudo log:

```bash
sudo grep COMMAND /var/log/auth.log | tail -2
journalctl -t sudo -n 3 --no-pager
```

We saw `asha : PWD=/home/asha ; USER=root ; COMMAND=/usr/bin/apt-get update` in `/var/log/auth.log`, and session-opened and session-closed lines in the journal. That is "every use is written in the register".

Rules and `visudo`:

```bash
echo "asha ALL=(ALL) /usr/bin/systemctl" | sudo tee /etc/sudoers.d/t1
echo "%devs ALL=(ALL) ALL" | sudo tee -a /etc/sudoers.d/t1
sudo chmod 440 /etc/sudoers.d/t1
sudo visudo -c -f /etc/sudoers.d/t1
echo "asha ALL=(ALL ALL" | sudo tee /etc/sudoers.d/t2
sudo visudo -c -f /etc/sudoers.d/t2
sudo rm /etc/sudoers.d/t1 /etc/sudoers.d/t2
```

Expected: `/etc/sudoers.d/t1: parsed OK`, and for the broken line `/etc/sudoers.d/t2:1:15: syntax error`. That is the safety net: a syntax check before a bad file locks you out of `sudo`. **Never leave a broken file in `/etc/sudoers.d/`.**

**Check yourself:**

- [ ] You can read a `/etc/passwd` line field by field.
- [ ] You saw `usermod -G` without `-a` remove a group.
- [ ] You saw the `!` appear and disappear in `/etc/shadow`.
- [ ] You found the sudo entry in the log.

---

## Part B: permissions (Episode 2)

### B1. Script, secret and the default lock

```bash
su - asha
echo 'echo hello devops' > hello.sh
./hello.sh
chmod u+x hello.sh
./hello.sh
ls -l hello.sh
echo top > secret.txt; chmod 600 secret.txt; ls -l secret.txt
umask
touch naya.txt; mkdir naya-kamra; ls -ld naya.txt naya-kamra
```

Expected (ours): `Permission denied` first, then `hello devops`; `-rwxrw-r-- ... hello.sh` (a new file starts at `664`, `u+x` makes it `764`); `-rw------- ... secret.txt`; `umask` `0002`; `naya.txt` was `-rw-rw-r--` and `naya-kamra` `drwxrwxr-x`.

The script says `umask` is `0022` for root and `0002` or `0022` for normal users. We got `0022` for root and **`0002`** for `asha` (Ubuntu's default for users with their own private group). With `0002`, files are `664` and directories `775`, not `644` and `755`.

A second user and the secret:

```bash
sudo -u kiran cat /home/asha/secret.txt
sudo chmod 640 /home/asha/secret.txt; sudo chown asha:devs /home/asha/secret.txt
ls -l /home/asha/secret.txt
sudo chmod g=rx /home/asha/hello.sh; ls -l /home/asha/hello.sh
sudo chmod 754 /home/asha/hello.sh; ls -l /home/asha/hello.sh
```

Expected: `cat: /home/asha/secret.txt: Permission denied`; `-rw-r----- 1 asha devs ... secret.txt` after the change; `-rwxr-xr--` both times (`g=rx` replaced the group's rights and `754` gives the same result).

### B2. SUID, SGID and the sticky bit

```bash
ls -l /usr/bin/passwd
ls -ld /tmp
sudo mkdir /srv/devs; sudo chown root:devs /srv/devs; sudo chmod g+s,g+w /srv/devs
ls -ld /srv/devs
sudo usermod -aG devs asha
sudo -u asha touch /srv/devs/by_asha; ls -l /srv/devs/by_asha
sudo -u asha mkdir /srv/devs/sub; ls -ld /srv/devs/sub
sudo chmod g-s /srv/devs
sudo -u asha touch /srv/devs/no_sgid; ls -l /srv/devs/no_sgid
sudo -u kiran touch /tmp/kfile; sudo -u asha rm /tmp/kfile
```

What we saw:

- `-rwsr-xr-x 1 root root ... /usr/bin/passwd`: the `s` is SUID.
- `/tmp`: `drwxrwxrwt`: the `t` is the sticky bit.
- `/srv/devs` after `g+s`: `drwxrwsr-x`. A file made by `asha` there was **group `devs`** (`-rw-rw-r-- 1 asha devs`), and a folder made there was `drwxrwsr-x` (it **inherits** the `s`).
- After `chmod g-s`: the new file's group was `asha`, not `devs`. That is the whole point of SGID.
- `rm: cannot remove '/tmp/kfile': Operation not permitted`: `asha` cannot delete `kiran`'s file in `/tmp`.
- (`kiran`'s primary group is `devs`, so a test with `kiran` shows `devs` even without SGID. Use a user whose primary group is different, as with `asha`.)

### B3. The file mode that Git records

```bash
cd /tmp && rm -rf gm && mkdir gm && cd gm && git init -q .
git config user.email a@b.c; git config user.name t
echo "echo hi" > deploy.sh; git add deploy.sh; git commit -qm one
chmod u+x deploy.sh
git diff | grep -E "^(old|new) mode"
```

Expected: `old mode 100644` and `new mode 100755`. This is the diff line the script says to expect in the Git session.

**Check yourself:**

- [ ] You can convert `-rwxr-xr--` to `754` and back.
- [ ] You saw the SGID folder give new files its group, and stop when the bit was removed.
- [ ] You saw the sticky bit refuse a delete.

---

## Part C: SSH keys (Episode 3)

SSH runs in the container (`systemctl is-active ssh` says `active`). On Ubuntu 24.04 `ssh.socket` is also `active` (the daemon is started by a socket). We tested everything with `localhost` as the "server" and `asha` as the user. You need `sshpass` only to automate `ssh-copy-id`'s password question in a test (`sudo apt-get install -y sshpass`). When you do it by hand, type the password at the prompt.

### C1. Make a key pair and put it on the server

```bash
ssh-keygen -t ed25519 -C "asha@laptop" -N "" -f ~/.ssh/id_ed25519
stat -c "%a %n" ~/.ssh ~/.ssh/id_ed25519 ~/.ssh/id_ed25519.pub
ssh-copy-id -o StrictHostKeyChecking=accept-new asha@localhost
stat -c "%a %n" ~/.ssh ~/.ssh/authorized_keys
ssh -o PasswordAuthentication=no asha@localhost "echo logged in as $(whoami) by key"
```

(`-N ""` means no passphrase. Use one on a real laptop.) What we saw: modes `700` (`.ssh`), `600` (private key), `644` (public key); `ssh-copy-id` printed `Now try logging into the machine`; `authorized_keys` was `600`; and the key login printed `logged in as asha by key`. Note that `ssh-copy-id` with `StrictHostKeyChecking=accept-new` skipped the "are you sure you want to continue connecting" question. On a first real connection you will see that question, and `yes` stores the fingerprint. **We did not capture that prompt**, since our run was non-interactive.

### C2. A locked password does not lock the key

```bash
sudo usermod -L asha
ssh -o PasswordAuthentication=no asha@localhost "echo key login works while the password is locked"
sudo usermod -U asha
```

Expected: the echo line printed. The script says that locking a password does not stop SSH-key logins, and that is what we saw on Ubuntu 24.04. To block a person fully, also remove their key from `authorized_keys`. (Expiring the account is another route. We did not test it.)

### C3. Permissions SSH insists on

```bash
chmod 644 ~/.ssh/id_ed25519
ssh -o PasswordAuthentication=no asha@localhost true
chmod 600 ~/.ssh/id_ed25519
chmod 777 ~/.ssh
ssh -o PasswordAuthentication=no -o PreferredAuthentications=publickey asha@localhost true
chmod 700 ~/.ssh
sudo journalctl -u ssh -n 5 --no-pager | grep -i "bad ownership"
```

Expected (ours): with the key at `644`, a banner `WARNING: UNPROTECTED PRIVATE KEY FILE!`. With `.ssh` at `777`, `Permission denied (publickey,password)`, and the server log said `Authentication refused: bad ownership or modes for directory /home/asha/.ssh`. The client complains about the private key, and the server about the folder. Both are fixed with `700` and `600`.

### C4. Switch passwords off, then check the real setting

Keep a second terminal logged in. Back up the file first:

```bash
sudo cp /etc/ssh/sshd_config /root/sshd_config.bak
printf "\nPasswordAuthentication no\nPermitRootLogin no\n" | sudo tee -a /etc/ssh/sshd_config
sudo sshd -t && echo "config ok"
sudo systemctl reload ssh
sudo sshd -T | grep -E "^(passwordauthentication|permitrootlogin)"
sshpass -p asha1 ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no asha@localhost true
ssh -o PasswordAuthentication=no asha@localhost echo key ok
```

Expected (ours): `config ok`, `permitrootlogin no`, `passwordauthentication no`; the password attempt fails with `Permission denied (publickey).`; the key login prints `key ok`. A root login with a key was refused too: `root@localhost: Permission denied (publickey).`

**The trap we found.** Ubuntu reads `/etc/ssh/sshd_config.d/*.conf` **first**, and the first value wins. Cloud images commonly ship a drop-in (often named `50-cloud-init.conf`) that says `PasswordAuthentication yes`. We simulated one:

```bash
echo "PasswordAuthentication yes" | sudo tee /etc/ssh/sshd_config.d/50-cloud-init.conf
sudo systemctl reload ssh
sudo sshd -T | grep ^passwordauthentication
sshpass -p asha1 ssh -o PreferredAuthentications=password -o PubkeyAuthentication=no asha@localhost "echo password login still works"
sudo rm /etc/ssh/sshd_config.d/50-cloud-init.conf; sudo systemctl reload ssh
sudo sshd -T | grep ^passwordauthentication
```

Expected (ours): `passwordauthentication yes` and `password login still works`, **even though the main file says `no`**. After removing the drop-in: `passwordauthentication no`. The lesson: after any SSH change, ask the daemon what it really uses, with `sudo sshd -T`, and look in `/etc/ssh/sshd_config.d/`. (We made that drop-in ourselves. We did not check the file on a real cloud image.)

Restore your config when done: `sudo cp /root/sshd_config.bak /etc/ssh/sshd_config; sudo systemctl reload ssh`.

**Check yourself:**

- [ ] You logged in with a key and no password.
- [ ] You know which side (client or server) complains about which permission.
- [ ] You checked the real value with `sshd -T`, not just the file you edited.

---

## Part D: packages and boot (Episode 4)

```bash
sudo apt-get update
sudo apt-get install -y nginx
systemctl is-active nginx; systemctl is-enabled nginx
curl -sI localhost | head -3
apt-cache policy nginx | sed -n 1,3p
systemctl get-default
```

Expected (ours): `active`, `enabled`, `HTTP/1.1 200 OK` and `Server: nginx/1.24.0 (Ubuntu)`, `Installed: 1.24.0-2ubuntu7.19`, and `graphical.target`.

Two things to know:

- **The stock Ubuntu container image blocks services from starting after an install** (a `policy-rc.d` file that says "no"). Our first attempt gave `inactive`, and `sudo systemctl start nginx` fixed it. The Dockerfile in `lab_files/` removes that file, so on the practice image nginx starts by itself, as it does on a VM.
- **`systemctl get-default` said `graphical.target`, not `multi-user.target`.** The script said a server usually shows `multi-user.target`. On Ubuntu we saw the first, in a container. Either way the machine runs without a screen. We did not check a real Ubuntu Server VM.

The boot chain (firmware, GRUB, kernel and `initramfs`, systemd, services, login) is reading only in a container: PID 1 here is `systemd` (`ps -p 1 -o comm=` printed `systemd`), but there is no firmware or bootloader to look at. `/boot` is empty.

---

## Clean up

```bash
sudo userdel -r asha; sudo userdel -r kiran; sudo groupdel devs; sudo groupdel qa; sudo rm -rf /srv/devs /tmp/gm
docker rm -f atithi-web1
```

(or keep the container for Session 5). Read each `rm -rf` before you press Enter.

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `usermod: unlocking the user's password would result in a passwordless account` | The user never had a password | `passwd user` first |
| User added to a group but still denied | The session is old | Log out and in, or `su - user` |
| `Permission denied (publickey)` after key setup | Wrong modes, or the key is not in `authorized_keys` | `700` `.ssh`, `600` key and `authorized_keys` |
| Passwords still work after you set `no` | A drop-in file in `sshd_config.d` wins | `sudo sshd -T`, then edit the drop-in |
| `sudo: /etc/sudoers.d/x is world writable` or `syntax error` | Wrong mode or a typo in a sudoers file | `chmod 440`, and `visudo -c -f file` |
| nginx installed but not running in the container | `policy-rc.d` | Use the lab Dockerfile, or `systemctl start nginx` |
| `Permission denied` on `apt update` | Not root | `sudo` |

## What we did not test

- **The first-connection fingerprint question** of SSH (non-interactive run).
- **`chage` expiry and the inactive period** actually taking effect over days. We set and read the values only.
- **A passphrase-protected key** and `ssh-agent`.
- **A real Ubuntu Server VM:** `get-default`, real boot, `netplan` (Session 5), a real cloud image's `sshd_config.d`.
- **Red Hat family differences** (`wheel` group, `dnf`, `sshd` service name). They are in the Session 5B guide.
- **GitHub.** The script mentions using the key there; we only made and used the key locally.

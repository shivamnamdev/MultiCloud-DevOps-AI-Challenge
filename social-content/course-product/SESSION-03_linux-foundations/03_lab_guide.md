# Session 03 lab guide: Linux foundations

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in names, dates and sizes.

| | |
|---|---|
| **Time** | Part A 10 min, Part B 20 min, Part C 30 min, Part D 30 min |
| **Cost** | Free if you use the practice container below or a VM on your laptop. A cloud VM can bill: stop or delete it after the lab. |
| **Skill check before you start** | None. You need to be able to open a terminal. |

## Before you start

The script wants an Ubuntu VM. If you do not have one yet, the quickest practice "building" is a container: Ubuntu 24.04 with systemd, an SSH door and the tools of Sessions 3 to 5. You need only Docker.

```bash
docker build -t atithi-ubuntu:lab -f lab_files/Dockerfile.ubuntu lab_files
docker run -d --name atithi-web1 --hostname atithi-web1 --privileged --tmpfs /run --tmpfs /run/lock atithi-ubuntu:lab
docker exec -it -u ubuntu -w /home/ubuntu atithi-web1 bash
```

(`-u ubuntu` makes you a normal staff member, not root. The practice password for `ubuntu` is `ubuntu`.) The image is about 490 MB and `systemctl is-system-running` said `running` after 6 seconds.

> **Two honest warnings about the container.** (1) `--privileged` is needed for systemd to run inside Docker. It gives the container wide access to the Docker host, so use it for practice only, never on a shared machine. (2) A container is **not** a VM: there is no real boot, no disks of its own and no real network card. Everything in this session works in it, and we say where a real VM would look different.
>
> A small thing we fixed in the Dockerfile: Ubuntu's container image ships a stub `man` and strips the manual pages of core commands, so `man ls` printed "This system has been minimized". The Dockerfile puts the pages back.

We tested on Ubuntu `24.04.5 LTS` (`coreutils 9.4`, `vim 9.1`, `nano 7.2`) on Docker Desktop (Mac, arm64). You should see the same prompts and outputs on any Ubuntu 24.04 VM, except where noted.

---

## Part A: first commands and getting help (Episode 1)

```bash
whoami
hostname
uname -a
grep -E "^(PRETTY_NAME|VERSION_ID)" /etc/os-release
ls --help | head -3
man ls | head -5
```

Expected (ours):

```
ubuntu
atithi-web1
Linux atithi-web1 7.0.14-linuxkit #1 SMP PREEMPT ... aarch64 aarch64 aarch64 GNU/Linux
PRETTY_NAME="Ubuntu 24.04.5 LTS"
VERSION_ID="24.04"
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
...
LS(1)                            User Commands                           LS(1)
```

Note the kernel line: inside a Docker Desktop container, `uname -a` shows the Docker VM's kernel (`linuxkit`), not "Ubuntu". On a real Ubuntu VM you would see something like `Linux ... 6.8.0-... #... SMP ... x86_64`. The distribution (`os-release`) is the part that says Ubuntu.

In `man ls`, press `q` to leave. Try the keyboard helpers from the script: Tab to complete, the up arrow, `history`, `Ctrl+R` to search old commands and `Ctrl+C` to stop a command. We did not drive these interactively in our test, because they need a real keyboard.

**Check yourself:**

- [ ] You can read the prompt (`user@host:path$`) and say what `$` versus `#` means.
- [ ] You can split `ls -l /etc` into command, option and argument.

---

## Part B: the floor plan (Episode 2)

```bash
ls -l / | grep -E " (bin|sbin|lib|tmp|etc|var|home|root|dev|proc)( |$)"
ls -ld /opt /srv /mnt /boot /usr/local
ls -a ~
ls -lh /var/log | sort -k5 -h | tail -3
```

What we saw on 24.04:

- `bin -> usr/bin`, `lib -> usr/lib`, `sbin -> usr/sbin` as links (`lrwxrwxrwx`), exactly the "two doors, one tool room" surprise of the script.
- Extra directories named `bin.usr-is-merged`, `lib.usr-is-merged`, `sbin.usr-is-merged`. They are a leftover of Ubuntu's switch to merged `/usr`. Ignore them.
- `/tmp` showed `drwxrwxrwt` (the `t` is the sticky bit, Session 4). `/root` showed `drwx------`: only the general manager may enter.
- `/opt`, `/srv`, `/mnt` and `/boot` were all empty directories in the container. (On a real VM `/boot` is full of kernel files.)
- `ls -a ~` listed `.`, `..`, `.bash_logout`, `.bashrc` and `.profile`.
- The biggest files in `/var/log` were around 200 KB (`kern.log`, `syslog`, `dpkg.log`). On a long-running server they are larger.

Look around without changing anything: `pwd`, `cd /var/log`, `ls`, `cd ~`, `cd ..`, `cd -`, and `ls /etc`.

**Check yourself:**

- [ ] You found the `bin -> usr/bin` line.
- [ ] You can say where configuration lives (`/etc`) and where logs live (`/var/log`).

---

## Part C: core commands, and the overwrite trap (Episode 3)

### C1. A mini project folder

```bash
mkdir -p demo/{src,logs,config}
touch demo/src/app.py demo/config/app.conf
cp demo/config/app.conf demo/config/app.conf.bak
mv demo/src/app.py demo/src/main.py
ls -R demo
```

Expected: `demo/config` holds `app.conf` and `app.conf.bak`, `demo/logs` is empty, `demo/src` holds `main.py`. One `mkdir -p` with braces made three folders.

### C2. `cp` and `mv` overwrite without asking

```bash
cd /tmp
echo old > a; echo new > b
cp b a; echo "a now: $(cat a)"
echo old > a
yes n | cp -i b a; echo "a still: $(cat a)"
echo old > a
yes n | mv -i b a; ls b
echo new > b
cp --update=none b a; echo "a: $(cat a)"
cp -n b a
mkdir dd; cp dd dd2
cp --version | head -1
```

What we saw:

- Plain `cp b a`: `a now: new`. No warning, no prompt, no recycle bin.
- `cp -i` and `mv -i` asked `cp: overwrite 'a'?` / `mv: overwrite 'a'?`. We answered `n` (with `yes n |`), and `a` was still `old`, `b` still existed.
- `cp --update=none b a` left `a` as `old`, silently.
- `cp -n b a` also left `a` alone, but printed a warning on this version: `cp: warning: behavior of -n is non-portable and may change in future; use --update=none instead`. That matches the script's advice.
- `cp dd dd2` on a folder: `cp: -r not specified; omitting directory 'dd'`.
- `cp (GNU coreutils) 9.4`. Older versions may not know `--update=none`.

### C3. Finding things

```bash
mkdir -p /tmp/fx && touch /tmp/fx/x.log /tmp/fx/y.txt
find /tmp/fx -name "*.log"
find /tmp/fx -type f -mtime -1 | sort
which python3
```

Expected: `/tmp/fx/x.log`; both files (they are newer than one day); `/usr/bin/python3`.

### C4. Wildcards and spaces

```bash
cd /tmp/fx
touch app1.conf app2.conf "My Notes.txt" a.bak b.bak
ls *.bak
ls app?.conf
ls "My Notes.txt"
ls My Notes.txt
```

Expected: `a.bak b.bak`; `app1.conf app2.conf`; `My Notes.txt`; and the last one fails twice: `ls: cannot access 'My': No such file or directory` and `ls: cannot access 'Notes.txt': ...`. Without quotes the shell sees two words. The shell, not `ls`, expands `*` and `?`.

### C5. Editors

`nano --version` printed `GNU nano, version 7.2` and `vi --version` printed `VIM - Vi IMproved 9.1`; both are installed in the practice image. **We could not drive an editor interactively in our test**, so try `nano demo/config/app.conf` (type a line, `Ctrl+O`, Enter, `Ctrl+X`) and `vi` (`i`, type, `Esc`, `:wq` or `:q!`) yourself.

### C6. Clean up, and what we did not run

Remove the practice folder with a path you have read twice: `rm -r demo` (from your home folder), and `rm -r /tmp/fx dd`.

> **Not run by us:** the script says GNU `rm` refuses `rm -rf /` but not `rm -rf ~` or a path built from an empty variable. We wanted to test that in a throwaway container, but our tooling blocked those three commands as too dangerous, and we did not work around that. So these three claims are the script's, not ours. If you test them, do it only in a disposable container, never on a machine you care about.

**Check yourself:**

- [ ] You saw `cp` overwrite silently, and `cp -i` ask first.
- [ ] You can say why `ls My Notes.txt` failed.

---

## Part D: reading text and finding the error (Episode 4)

```bash
cd /tmp
printf "INFO start\nERROR db timeout\nERROR db timeout\nWARN slow\n" > app.log
grep ERROR app.log | sort | uniq -c
grep ERROR app.log > errors.txt
wc -l errors.txt
grep -c ERROR app.log
grep -in warn app.log
grep -v INFO app.log | wc -l
```

Expected (ours): `2 ERROR db timeout` (the `uniq -c` count), `2 errors.txt`, `2`, `4:WARN slow` (`-n` gives the line number, `-i` ignores case), and `3`.

### D2. Redirects

```bash
ls /nonexistent 2> err.txt; cat err.txt
echo x >> errors.txt; wc -l < errors.txt
```

Expected: `ls: cannot access '/nonexistent': No such file or directory` in `err.txt`, and `3` lines after `>>` added one (`>` would have replaced the file).

### D3. The small tools

```bash
printf "a,3\nb,1\nc,2\n" > t.csv
cut -d, -f2 t.csv | sort -n
printf "x\ny\nx\n" | uniq -c
head -n 2 app.log; tail -n 1 app.log
```

Expected: `1 2 3` (one per line); `uniq -c` printed `1 x`, `1 y`, `1 x`: the repeated `x` was **not** counted together, because `uniq` only merges **neighbouring** repeats. That is why the script says `sort` first.

### D4. `tail -f`

```bash
printf "line1\n" > f.log
timeout 10 tail -f f.log &
sleep 1; echo line2 >> f.log; echo line3 >> f.log
```

Expected: `line1`, `line2`, `line3` appear live. This is how you watch a log during a deploy.

### D5. Your VM and the first SSH

The script's SSH step (a first connection and the `yes` to trust the machine's fingerprint) needs a real VM, or a second container with an SSH server. **We did not test the cloud, VirtualBox, UTM or WSL routes in this session.** Session 4's guide runs SSH between two containers, including the host-key prompt.

**Check yourself:**

- [ ] You got `2 ERROR db timeout` from your own sample log.
- [ ] You can say what `>`, `>>` and `2>` each do.
- [ ] You saw `uniq -c` miss a non-adjacent repeat.

---

## Clean up

```bash
docker rm -f atithi-web1
docker rmi atithi-ubuntu:lab
```

(Keep the image if you are going on to Session 4 and 5.)

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `man ls` says "This system has been minimized" | Stock Ubuntu container image | Use `lab_files/Dockerfile.ubuntu`, which restores the pages |
| `Permission denied` on a command in `/var/log` | You are a normal user | Read your own files, or use `sudo` (Session 4) |
| `systemctl: ... System has not been booted with systemd` | The container was started without `--privileged --tmpfs /run` | Start it as shown above |
| `cp: -r not specified; omitting directory` | You copied a folder | `cp -r` |
| `ls My Notes.txt` fails | Space in the name | Quote it |

## What we did not test

- **A real VM,** VirtualBox, UTM, WSL, and the cloud free tier.
- **`rm -rf /`, `rm -rf ~` and `rm -rf "$EMPTY/"`.** Blocked by our tooling, so unrun.
- **Interactive keys:** Tab, `Ctrl+R`, `Ctrl+C`, `man` paging, and the editors `nano` and `vi`.
- **Mac terminal differences.** Our tests ran in an Ubuntu container, not in macOS `zsh`.
- **Red Hat family differences** (Rocky, AlmaLinux). They are in the Session 5B guide.

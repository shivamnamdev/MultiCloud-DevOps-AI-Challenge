# Session 06 lab guide: Bash scripting

Companion to `02_script.md`. The script teaches the ideas; this guide is the hands-on sheet you keep open next to your terminal. Every command here was run for real unless a box says otherwise, and the outputs shown are what we saw. Yours will differ in dates, hostnames and sizes.

| | |
|---|---|
| **Time** | Part A 25 min, Part B 30 min, Part C 40 min, Part D 40 min (cron needs a few minutes of waiting) |
| **Cost** | Free with the practice container. |
| **Skill check before you start** | Sessions 3 to 5: paths, permissions, `systemctl`, the first `healthcheck.sh`. |

## Before you start

Use an Ubuntu 24.04 machine, or the practice container (the Dockerfile in `lab_files/` adds `cron`, `shellcheck`, `jq` and Python to the one from Session 5):

```bash
docker build -t atithi-ubuntu:lab -f lab_files/Dockerfile.ubuntu lab_files
docker run -d --name atithi-web1 --hostname atithi-web1 --privileged --tmpfs /run --tmpfs /run/lock atithi-ubuntu:lab
docker cp lab_files atithi-web1:/home/ubuntu/s06
docker exec -u root atithi-web1 chown -R ubuntu:ubuntu /home/ubuntu/s06
docker exec -it -u ubuntu -w /home/ubuntu/s06 atithi-web1 bash
```

(`--privileged` lets systemd and `cron` run in the container. Practice only.) We tested on Ubuntu `24.04`, GNU bash `5.2.21`, `shellcheck 0.9.0`, Docker Desktop (Mac, arm64). The scripts for each part are in `lab_files/episode1` to `episode4`. Run `chmod +x` on any that lose their execute bit after copying.

---

## Part A: the first slip (Episode 1)

```bash
cd episode1
./hello.sh
cp hello.sh h2.sh; chmod -x h2.sh; ./h2.sh
```

Expected: `Hello Asha` and `Single: Hello $name` (double quotes expand, single quotes do not), then `./h2.sh: Permission denied` for the file without the execute bit.

### A1. The two classic slips

```bash
printf '#!/usr/bin/env bash\nname = "Asha"\necho "Hello $name"\n' > bad.sh
bash bad.sh
d="booking site"; mkdir -p "$d"; touch "$d/a"
ls -d $d
ls -d "$d"
```

What we saw: `bad.sh: line 2: name: command not found` then `Hello ` (no spaces around `=`). And `ls -d $d` split the name: `cannot access 'booking'` and `cannot access 'site'`, while `ls -d "$d"` printed `booking site`.

### A2. Arguments, command output and input

```bash
echo Bimal | ./greet.sh Asha 25
```

Expected (ours): `script=./greet.sh first=Asha second=25 count=2 all=Asha 25`, then `today=2026-11-18 old-style=2026-11-18 nested=inner 2026` (backticks and `$( )` agree, and `$( )` nested inside `$( )` works), then `read gave: Bimal`.

### A3. Redirects

```bash
ls > list.txt
echo first > log.txt; echo second >> log.txt; wc -l < log.txt
grep x /nonexistent 2> errors.txt; cat errors.txt
(echo out; ls /nonexistent) > both.txt 2>&1; cat both.txt
```

Expected: `2` lines (`>>` appended), the grep error went into `errors.txt`, and `both.txt` held `out` plus the `ls` error.

### A4. The report slip

`episode1/info.sh` is the lab, with `du -sh "$1"` added.

```bash
./info.sh "booking site"
./info.sh
```

Expected (ours): `Building: atithi-web1 | Staff: ubuntu | Date: 2026-11-18`, the `df` line (`overlay 453G 27G 403G 7% /`), `4.0K booking site`. Without an argument, `du: invalid zero-length file name`. That is the gap Episode 3's `usage` fixes.

**Check yourself:**

- [ ] You saw `name = "Asha"` fail, and can say why.
- [ ] You can say what changes if `$d` has no quotes.
- [ ] You know where an error goes with `>` and where with `2>`.

---

## Part B: decisions and loops (Episode 2)

```bash
cd ../episode2
f=list.txt; touch $f
[ -f "$f" ] && echo "file exists"
[ -d /tmp ] && echo "dir ok"
[ -z "" ] && echo "empty string"
disk=95; [ "$disk" -gt 90 ] && echo "95 > 90 numerically"
[ 95 == 100 ] && echo eq || echo "string 95 != 100"
[[ 95 > 100 ]] && echo "TRUE: [[ > ]] compares letters, not numbers"
[ "$disk" -gt abc ]
```

What we saw: all the first lines as expected; **`[[ 95 > 100 ]]` is true**, because `>` compares text, so `"95"` sorts after `"100"`. Use `-gt` (or `(( ))`) for numbers. `[ "$disk" -gt abc ]` printed `[: abc: integer expression expected`.

Two spacing traps, one silent:

```bash
[ -f"$f" ]; echo "exit=$?"
[-f "$f" ]
```

`[ -f"$f" ]` printed nothing and exited `0` (it became a one-word test, which is always true: a **silent bug**). `[-f` printed `bash: [-f: command not found`.

### B1. `case`, loops, `&&` and `||`, `[[ ]]`

```bash
cmd=restart; case "$cmd" in start) echo starting;; stop) echo stopping;; restart) echo restarting;; *) echo unknown;; esac
cmd=bogus;   case "$cmd" in start) echo s;; *) echo "default: unknown $cmd";; esac
touch a.log b.log; for x in *.log; do echo "log: $x"; done
for i in {1..3}; do printf "$i "; done; echo
mkdir -p releases && cd releases && pwd; cd ..
ping -c1 -W1 not-a-building.invalid >/dev/null 2>&1 || echo "no network"
n=asha; [[ $n == a* ]] && echo "pattern match"
[[ -f list.txt && -r list.txt ]] && echo "file and readable"
```

Expected: `restarting`, `default: unknown bogus`, both log files, `1 2 3`, the path of `releases`, `no network`, `pattern match`, `file and readable`.

### B2. The roll call

```bash
./rollcall.sh
```

(`servers.txt` has `localhost`, `8.8.8.8` and `not-a-building.invalid`.) Expected (ours): `UP localhost`, `UP 8.8.8.8`, `DOWN not-a-building.invalid`, `Not answering: 1`. The third name never resolves, so it is DOWN, as the script says "ping ka jawab nahi".

### B3. The `ssh` inside `while read` trap

We set up a key login to `localhost` (as in Session 4: `ssh-keygen`, add the `.pub` to `~/.ssh/authorized_keys`), and ran:

```bash
printf "one\ntwo\nthree\n" > list3.txt
O="-o StrictHostKeyChecking=no -o LogLevel=ERROR -o BatchMode=yes"
while read -r h; do echo "line: $h"; ssh $O localhost "echo ran-remote"; done < list3.txt
while read -r h; do echo "line: $h"; ssh -n $O localhost "echo ran-remote"; done < list3.txt
```

Without `-n`: **only** `line: one` and `ran-remote` (the loop ended after one line, `ssh` ate the rest of the file). With `-n`: all three lines.

**Check yourself:**

- [ ] You saw `[[ 95 > 100 ]]` be true and know the fix.
- [ ] You saw `ssh` eat the loop's input and fixed it with `-n`.

---

## Part C: a safe slip (Episode 3)

```bash
cd ../episode3
mkdir -p /tmp/rel
./release_unsafe.sh; echo "exit=$?"
./release_safe.sh;   echo "exit=$?"
```

(`release_safe.sh` is the same file with `set -euo pipefail` added.) What we saw: the **unsafe** slip printed all three steps, including `(old release removed)`, and exited **0**, even though step 2 had failed. The **safe** one stopped after step 1 with `exit=1` (here step 1's `cp` is what fails first).

### C1. The three flags and `trap`

```bash
bash -c 'set -u; echo rm -rf "$DIR/"'
bash -c 'false | true; echo "no pipefail: $?"'
bash -c 'set -o pipefail; false | true; echo "pipefail: $?"'
bash -c 'set -e; if false; then :; fi; false || echo "|| handled it"; echo "still running"'
bash -c 'set -e; false; echo "not reached"'; echo "exit=$?"
./trapdemo.sh; ./trapdemo.sh fail; echo "exit=$?"
```

(We used `echo` in front of `rm -rf` on purpose: never test with the real thing.) Expected: `DIR: unbound variable`; `no pipefail: 0` against `pipefail: 1`; `|| handled it` and `still running` (`set -e` does not stop on a failure that is being tested); no `not reached` and `exit=1`; for `trapdemo.sh`: `working`, `finished`, `cleanup ran (exit code 0)`, and for `fail`: `working`, `cleanup ran (exit code 1)`, `exit=1`.

### C2. Functions, and a trap in the script's own advice

```bash
./funcs.sh
./funcs2.sh
```

`funcs.sh` prints:

```
captured: [20:30:30] disk check, limit 90
42
check_disk returned 1
```

The `log` line **was captured into the variable together with the number**, because `log` writes to standard output and `$( )` takes everything. In `funcs2.sh`, `log` writes with `>&2` and the capture holds only `42`. Rule: inside a function whose output you capture, log to **stderr**.

### C3. Finding mistakes

```bash
bash -n syntax_bad.sh; echo "exit=$?"
bash -x ../episode1/hello.sh | head
bash -c 'a=1; set -x; b=$((a+1)); echo $b; set +x; echo untraced'
shellcheck sloppy.sh
shellcheck healthcheck.sh; echo "exit=$?"
```

Expected (ours): `syntax_bad.sh: line 4: syntax error: unexpected end of file` and `exit=2`; `-x` printed lines starting `+ name=Asha`; the `set -x` window traced only two lines; `shellcheck sloppy.sh` found `SC2086` (quote `$file`), `SC2086` for `$HOME/*.log`, and `SC2154` (`x` is referenced but not assigned); and the lab's `healthcheck.sh` passed shellcheck cleanly with `exit=0`.

### C4. The improved health check

```bash
./healthcheck.sh;               echo "exit=$?"
./healthcheck.sh nginx;         echo "exit=$?"
./healthcheck.sh nginx 1;       echo "exit=$?"
./healthcheck.sh nosuchservice; echo "exit=$?"
```

Needs nginx installed and running (the practice image installs `nginx-light`). What we saw:

```
Usage: ./healthcheck.sh <service> [disk-limit-percent]   exit=1
[20:30:41] OK   disk 7%  /  OK   nginx                  exit=0
[20:30:41] FAIL disk 7%  /  OK   nginx                  exit=1   (limit 1%)
[20:30:41] OK   disk 7%  /  FAIL nosuchservice          exit=1
```

After `sudo systemctl stop nginx`, `./healthcheck.sh nginx` printed `FAIL nginx` and `exit=1`. Start nginx again afterwards.

**Check yourself:**

- [ ] You saw the unsafe slip finish with exit 0 after a failed step.
- [ ] You can say when `set -e` does **not** stop a script.
- [ ] You know why `log` should write to stderr in a function you capture.

---

## Part D: cron and a backup (Episode 4)

### D1. The backup slip

```bash
cd ../episode4
cp backup.sh ~/backup.sh; chmod +x ~/backup.sh
mkdir -p ~/atithi-booking/static; echo "<h1>Atithi</h1>" > ~/atithi-booking/index.html; echo x > ~/atithi-booking/static/app.js
~/backup.sh ~/atithi-booking
tar -tzf /tmp/backups/backup-*.tar.gz
~/backup.sh
```

Expected (ours): `20:30:51 OK /tmp/backups/backup-20261118-2030.tar.gz`, then the listing `./`, `./static/`, `./static/app.js`, `./index.html`, and for no argument: `backup.sh: line 3: 1: usage: backup.sh <folder>`.

Old backups are deleted after 7 days (we faked two files with `touch -d "10 days ago"` and `"3 days ago"`): the old one was removed and the newer one kept.

**A defect we found in the script's own backup.** Run it twice within the same minute, the second time with a wrong folder:

```bash
~/backup.sh ~/atithi-booking
stat -c %s /tmp/backups/*.tar.gz
~/backup.sh /no/such/dir
stat -c %s /tmp/backups/*.tar.gz
tar -tzf /tmp/backups/*.tar.gz; echo "tar -tzf exit=$?"
```

We saw `211 bytes` before and **`20 bytes` after**, with `tar -tzf` still exiting `0`. The failed run truncated the good backup, and an empty archive passes the verification step. `episode4/backup2.sh` fixes both: it builds `file.part`, checks that the archive has at least one entry, and only then `mv`s it into place (with a `trap` that removes a half-made `.part`). With it, a failed run left the good file at `211 bytes`.

### D2. The timetable, and four traps

`episode4/crontab.example` has the script's line and one line per trap. Fix the paths, install it, and wait for an even minute:

```bash
cp envprobe.sh ~/envprobe.sh; chmod +x ~/envprobe.sh
crontab crontab.example
crontab -l
```

(`crontab -e` opens an editor. We installed from a file so the test could run unattended.) Watch `/tmp/backup.log`. What we saw:

- **The backup ran:** `20:32:01 OK /tmp/backups/backup-20261118-2032.tar.gz` and later `20:48:01 OK ...`. The second run came much later than 2 minutes: our Docker VM's clock appeared to jump, and we did not find the reason. On a normal machine expect one line every 2 minutes.
- **Cron's environment** (`envprobe.sh` logged it): `PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin SHELL=/bin/sh PWD=/home/ubuntu HOME=/home/ubuntu`. On Ubuntu the PATH had the system folders (so `python3` and `shellcheck` were found), but `SHELL` is **`/bin/sh`, not bash**, and the working folder is your **home**. Anything in `~/.local/bin` or a virtual environment would not be on that PATH.
- **Relative path:** `relative.sh` runs `cat ./data.txt`. Under cron: `cat: ./data.txt: No such file or directory`, because the working folder is the home, not the script's folder.
- **The `%` trap:** the unescaped line `echo "unescaped: $(date +%F)"` never wrote its file; the syslog showed it cut at the `%`: `CMD (echo "unescaped: $(date +)`. The escaped line (`\%F`) worked: `escaped: 2026-11-18`.
- **Where the log is:** `grep CRON /var/log/syslog | tail` showed `CRON[723]: (ubuntu) CMD (/home/ubuntu/backup.sh ...)` for every run, and `journalctl -u cron` showed the service's own lines. We also saw `(CRON) info (No MTA installed, discarding output)`: any output not redirected to a log file is lost on a machine without mail.

**Remove the test timetable now:** `crontab -r`, and check with `crontab -l` (`no crontab for ubuntu`). We also cleared `/tmp/backups` and the `/tmp/*.log` files.

### D3. `flock`

```bash
(flock -n /tmp/x.lock sleep 8 &); sleep 1
flock -n /tmp/x.lock echo "second run started"; echo "exit=$?"
```

Expected (ours): nothing printed and `exit=1` (the second run was refused while the first held the lock). After 8 seconds the same command ran normally.

**Check yourself:**

- [ ] You ran the backup from cron and read its log.
- [ ] You saw the working folder and the shell in cron's environment.
- [ ] You saw the `%` line fail and the `\%` line work.
- [ ] You removed the test crontab.

---

## Clean up

```bash
crontab -r
docker rm -f atithi-web1
docker rmi atithi-ubuntu:lab
```

## If something goes wrong

| Symptom | Likely cause | Fix |
|---|---|---|
| `Permission denied` running `./x.sh` | No execute bit | `chmod u+x` |
| `name: command not found` | Spaces around `=` | `name="Asha"` |
| A folder name is split in two | Unquoted variable | `"$var"` |
| Loop over a file stops after one line | A command in the loop reads the file (`ssh`) | `ssh -n` |
| `[[ a > b ]]` gives odd results for numbers | Text comparison | `-gt`, `-lt` |
| Cron job does nothing | Relative path, wrong shell, `%` in the line, or no log redirect | `grep CRON /var/log/syslog`, redirect `>> log 2>&1` |
| A function's result has extra text | `log` writes to stdout | `log ... >&2` |
| `Failed to connect to bus` as a normal user in the container | No `dbus` | Use the lab image |

## What we did not test

- **Red Hat family cron** (`crond`, `/var/log/cron`), and `@reboot` / `@daily` shortcuts.
- **Mail from cron** (no mail system in the container).
- **`ssh` to a different machine** in the `while read` loop: we used `localhost`.
- **A real server's backups to another disk or to S3** (Session 12).
- **Interactive `crontab -e`** and `read -p` typed by a person (we piped input).

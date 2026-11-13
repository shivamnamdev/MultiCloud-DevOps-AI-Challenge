# ✍️ 02: SCRIPT — SESSION-06: Bash Scripting
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S06`
- **Focus:** Shebang/variables/arguments, conditions, loops, functions, error handling, cron
- **Episodes:**
  - Episode 1: Pehli Script: shebang, variables aur arguments
  - Episode 2: Faisle aur Doharav: if, case, for, while
  - Episode 3: Functions aur Safe Scripts: set -euo pipefail
  - Episode 4: Automation: cron aur ek Backup Script

---

# 📺 EPISODE 1: Pehli Script

### [00:00 – 01:15] Scene 1: Wahi 5 Commands, Roz
**[VISUAL: A person typing the same 5 commands every morning. A calendar flips: Mon, Tue, Wed... a boredom meter rises. Then one script file replaces them.]**

**(Voiceover):**
Agar aap roz wahi paanch commands type karte ho, to aap ek script ke umeedwar ho. Bash script sirf commands ki ek list hai jo ek file mein likhi hai aur ek saath chal jaati hai. Lekin script mein variables, conditions aur loops hote hain, jo use ek chhote program mein badal dete hain. Aaj ki shuruaat: pehli script.

### [01:15 – 05:00] Scene 2: Shebang, Chalana aur Variables
**[VISUAL: A file `hello.sh` with `#!/usr/bin/env bash` highlighted. Then `name="Asha"` and `echo "Hello $name"`. Quote types compared.]**

**(Voiceover):**
Script ki pehli line shebang hoti hai, `#!/usr/bin/env bash`, jo batati hai ki ise Bash se chalana hai. Phir `chmod +x hello.sh` aur `./hello.sh`. Variable banane mein `=` ke dono taraf space nahi hota: `name="Asha"`. Use padhte waqt `$name`. Double quotes ke andar variable expand hota hai, single quotes mein nahi. Aur ek zaroori aadat: variables ko hamesha double quotes mein likho, `"$name"`, warna spaces wali values toot jaati hain.

### [05:00 – 08:30] Scene 3: Arguments aur Command Output
**[VISUAL: `./greet.sh Asha 25` with a diagram: $0=script, $1=Asha, $2=25, $#=2, $@=all. Then `today=$(date +%F)`.]**

**(Voiceover):**
Script ko bahar se value deni ho to arguments. `./greet.sh Asha 25` mein `$1` Asha hai, `$2` 25, `$#` arguments ki ginti, aur `$@` sabhi arguments. Kisi command ka output variable mein rakhna ho to `$( )`: `today=$(date +%F)`. Aur user se input chahiye to `read -p "Name: " name`. In teen cheezon se script flexible ban jaati hai, har baar badalne ki zaroorat nahi.

### [08:30 – 11:30] Scene 4: Lab: Server Info Script
**[VISUAL: `info.sh` prints hostname, date, user, disk usage. Terminal output shown.]**

**(Voiceover):**
Lab:
```bash
#!/usr/bin/env bash
host=$(hostname)
user=$(whoami)
today=$(date +%F)
echo "Server: $host | User: $user | Date: $today"
df -h / | tail -1
```
Isse `info.sh` mein save karo, `chmod +x` karo aur chalao. Ab ise badlo: pehla argument ek folder ka path ho, aur script us folder ka size `du -sh "$1"` se print kare. Ek script, do tarah ke kaam.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "#! · var=value · \"$var\" · $1 $@ · $(cmd)".]**

**(Voiceover):**
Recap: shebang, variables, quotes, arguments, command substitution. Ab script ko faisle lena sikhate hain: agar ye ho to wo, warna kuch aur.

---

# 📺 EPISODE 2: Faisle aur Doharav

### [00:00 – 01:15] Scene 1: Script Soch Sake To?
**[VISUAL: A script that blindly runs `cp` even though the file is missing; red error. Next, a script that checks first and prints "File not found".]**

**(Voiceover):**
Ek script jo bina check kiye chale, aksar ek chhoti galti par bada nuksaan karti hai. Achhi script pehle poochhti hai: file hai? Server chal raha hai? Disk bhari to nahi? Faisle ke liye conditions, aur dohrane ke liye loops.

### [01:15 – 05:00] Scene 2: if, test aur Comparison
**[VISUAL: An `if [ -f "$file" ]; then ... fi` block, with test flags: -f file, -d directory, -z empty string, -eq/-gt numbers, == for strings.]**

**(Voiceover):**
`if [ condition ]; then ... fi`. Condition ke andar spaces zaroori hain. File ke liye `-f`, folder ke liye `-d`, khaali string ke liye `-z`. Numbers ki tulna `-eq`, `-gt`, `-lt` se, strings ki `==` se. Dhyaan: numbers aur strings ke operator alag hote hain, ye aksar galti ki wajah banta hai. Agar kai options hon to `case` statement saaf lagta hai, jaise `start`, `stop`, `restart` ke liye.

### [05:00 – 08:30] Scene 3: for aur while
**[VISUAL: A loop: `for f in *.log; do ...; done` highlighting each file in turn. A `while read line` loop streaming lines from a file.]**

**(Voiceover):**
`for f in *.log; do echo "$f"; done` har log file par ek kaam. `for i in {1..5}` ginti ke liye. Aur `while read -r line; do ...; done < file.txt` file ki har line ke liye. Loop ke andar bhi conditions laga sakte ho, jaise sirf bade files ko pakadna. Ek reality check: server list par loop chalana DevOps mein aam hai, jaise har server ko ping karna, aur wahi se automation ki shuruaat hoti hai.

### [08:30 – 11:30] Scene 4: Lab: Server Ping Checker
**[VISUAL: A `servers.txt` with three hostnames. Script loops and prints UP/DOWN with `ping -c1 -W1`.]**

**(Voiceover):**
Lab:
```bash
#!/usr/bin/env bash
while read -r host; do
  if ping -c1 -W1 "$host" >/dev/null 2>&1; then
    echo "UP   $host"
  else
    echo "DOWN $host"
  fi
done < servers.txt
```
`servers.txt` mein `localhost`, `8.8.8.8` aur ek galat naam rakho. Script chalao aur dekho UP aur DOWN. `>/dev/null 2>&1` ka matlab hai output chhupao taaki sirf humara message dikhe.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "if/case · test flags · for/while".]**

**(Voiceover):**
Recap: faisle aur dohrav. Ab script ko professional banate hain: functions, aur wo safety settings jo galti hone par script ko rok deti hain.

---

# 📺 EPISODE 3: Functions aur Safe Scripts

### [00:00 – 01:15] Scene 1: Script Jo Galti Ke Baad Bhi Chalti Rahi
**[VISUAL: A deploy script. Step 2 fails silently, step 3 keeps going and deletes the old release. Red alarm.]**

**(Voiceover):**
Ek deploy script mein step do fail ho gaya, par script aage badh gayi aur purana release delete kar diya. Ab na naya hai na purana. Bash by default galti hone par rukti nahi. Isliye Bash ka sabse zaroori seekh: safe mode mein script likho.

### [01:15 – 05:00] Scene 2: set -euo pipefail
**[VISUAL: Three flags animated: `-e` stops on error, `-u` fails on unset variable, `-o pipefail` fails if any pipe stage fails. A trap mention.]**

**(Voiceover):**
Script ki shuruaat mein `set -euo pipefail` likho. `-e` kisi command ke fail hote hi script rok deta hai. `-u` unset variable use karne par error deta hai, jo `rm -rf "$DIR/"` jaisi galtiyon se bachata hai. `pipefail` pipe ke beech ki command fail hone par bhi pakadta hai. Har command ka status `$?` mein hota hai: 0 matlab safe. Aur safai ke liye `trap 'echo cleanup' EXIT` har exit par chalta hai, error ho ya na ho.

### [05:00 – 08:30] Scene 3: Functions aur Reusable Code
**[VISUAL: A function `log() { echo "[$(date +%T)] $*"; }` called from several lines. Another `backup()` with `local` variables and `return`.]**

**(Voiceover):**
Baar baar likhi jaane wali cheez ko function bana do: `log() { echo "[$(date +%T)] $*"; }`. Function ke arguments bhi `$1`, `$2` hote hain. `local` se variable function ke andar tak seemit rehta hai. `return` ek status code deta hai, output nahi. Aur ek achha pattern: `main()` function mein poori script rakho aur aakhir mein `main "$@"` bulao, taaki padhna aasaan rahe.

### [08:30 – 11:30] Scene 4: Lab: Safe aur Reusable Script
**[VISUAL: An editor with a script using `set -euo pipefail`, `log()`, and a `require()` function. A missing argument triggers a clean usage message.]**

**(Voiceover):**
Lab:
```bash
#!/usr/bin/env bash
set -euo pipefail
log() { echo "[$(date +%T)] $*"; }
usage() { echo "Usage: $0 <directory>"; exit 1; }
[ $# -eq 1 ] || usage
dir="$1"
[ -d "$dir" ] || { log "no such dir: $dir"; exit 2; }
log "size: $(du -sh "$dir" | cut -f1)"
```
Bina argument chalao, ek saaf usage message aayega. Galat folder do, saaf error aur exit code 2. Ye cheezein hi ek script ko "production-safe" banati hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "set -euo pipefail · trap · functions · local · exit codes".]**

**(Voiceover):**
Recap: safe flags, functions, exit codes. Ab ye script khud chale to? Agla episode: cron, aur ek asli backup automation.

---

# 📺 EPISODE 4: Automation — cron aur Backup Script

### [00:00 – 01:15] Scene 1: Raat 2 Baje Kaun Jaage?
**[VISUAL: A clock at 2:00 AM. A laptop is shut, but a small gear icon labelled "cron" turns, running a job.]**

**(Voiceover):**
Backup raat 2 baje lena hai. Aap to sote rahoge. Linux mein cron wo scheduler hai jo aapki taraf se samay par kaam chalata hai. Aaj ke episode ka maksad: ek script likhna jo backup le, purane backups saaf kare, aur khud chale.

### [01:15 – 05:00] Scene 2: cron ka Syntax
**[VISUAL: A crontab line with 5 time fields labelled minute, hour, day of month, month, day of week. Examples: `0 2 * * *`, `*/15 * * * *`, `0 9 * * 1`.]**

**(Voiceover):**
`crontab -e` se schedule likhte hain. Format hai paanch time fields aur phir command: minute, ghanta, mahine ka din, mahina, hafte ka din. `0 2 * * *` har raat 2:00 baje. `*/15 * * * *` har 15 minute mein. `0 9 * * 1` har somvaar subah 9. Cron ka environment chhota hota hai, isliye script ka poora path likho, aur output ko ek log file mein bhejo, jaise `>> /var/log/backup.log 2>&1`.

### [05:00 – 08:30] Scene 3: Backup Script ka Design
**[VISUAL: A flowchart: validate source → create `backup-YYYYMMDD.tar.gz` → verify archive → delete backups older than 7 days → log result.]**

**(Voiceover):**
Ek achha backup script paanch kaam karta hai. Source folder check, tar.gz banana, naam mein tareekh daalna, archive sahi hai ye verify karna, aur purane backups hata dena. Verify ke liye `tar -tzf` se andar ki files list ho jaati hain. Saaf-safai ke liye `find /backups -name "backup-*.tar.gz" -mtime +7 -delete`. Aur kabhi bhi backup usi disk par mat rakho jahan data hai.

### [08:30 – 11:30] Scene 4: Lab: Backup + cron
**[VISUAL: The script runs, a `.tar.gz` appears, `crontab -l` shows the schedule.]**

**(Voiceover):**
Lab:
```bash
#!/usr/bin/env bash
set -euo pipefail
src="${1:?usage: backup.sh <src>}"
dest="/tmp/backups"; mkdir -p "$dest"
file="$dest/backup-$(date +%Y%m%d).tar.gz"
tar -czf "$file" -C "$src" .
tar -tzf "$file" >/dev/null
find "$dest" -name 'backup-*.tar.gz' -mtime +7 -delete
echo "OK $file"
```
Ise chalao, phir `crontab -e` mein `*/2 * * * * /home/you/backup.sh /home/you/demo >> /tmp/backup.log 2>&1` jodo. Do minute baad naya backup aur log dekho. Test ke baad schedule ko wapas theek karna na bhoolna.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "cron 5 fields · full paths · log output · verify backup · delete old".]**

**(Voiceover):**
Recap: Bash se aap Linux ke kaam ko automate kar sakte ho. Lekin jab logic bada ho, cloud APIs se baat karni ho, ya JSON handle karna ho, to Bash thaka deta hai. Agle session mein Python ko DevOps ke liye use karte hain.

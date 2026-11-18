# ✍️ 02: SCRIPT — SESSION-06: Bash Scripting
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S06`
- **Focus:** Shebang, variables, quoting, arguments, command substitution, conditions (`if`, `case`), loops (`for`, `while`), functions, safe mode (`set -euo pipefail`, `trap`), exit codes, cron, a backup script
- **Story position:** Zoom level 1, inside one building. Atithi Hotels ka manager roz wahi round lagata hai; ab wo round ek likhi hui slip ban jaata hai.
- **Story words used:** desk (shell), instruction slip (script), timetable (cron), building (server), logbook, front desk (web server)
- **Lab project:** the booking website folder `atithi-booking` from Session 16 is used as the thing to protect and back up. If students have not reached Session 16 yet, any folder with a few files works.
- **Builds on:** the `healthcheck.sh` written in Session 05, which is improved here.
- **Episodes:**
  - Episode 1: Pehli Slip: Shebang, Variables aur Arguments
  - Episode 2: Faisle aur Doharav: if, case, for, while
  - Episode 3: Safe Slip: Functions, set -euo pipefail aur trap
  - Episode 4: Timetable: cron aur Booking Site ka Backup

---

# 📺 EPISODE 1: Pehli Slip

### [00:00 – 02:30] Scene 1: Wahi Paanch Commands, Roz
**[VISUAL: The Atithi Hotels manager at the desk each morning, reciting the same five instructions to a new assistant. A calendar flips: Mon, Tue, Wed. A boredom meter rises. Then the manager hands over a single written slip, and the assistant carries out all five.]**

**(Voiceover):**
Pichhle session mein manager ka daily round seekha: uptime, free, df, service ka status, aur logbook. Manager roz subah wahi paanch instructions desk par bolta hai. Kisi din ek bhool jaaye to round adhoora rehta hai. Ab socho wo ek parchi par likh de, aur assistant parchi padh kar sab kar de. Linux mein wo parchi bash script hai: ek file jisme commands likhi hain, aur wo ek saath chal jaati hain. Desk, yaani jahan aap instruction bolte ho, shell hai, aur is session mein hum us desk ke liye parchiyan likhna seekhenge. Parchi mein sirf commands nahi hoti. Usme variables, faisle aur dohrav bhi hote hain, aur wahi use ek chhote program mein badal dete hain. Is episode mein: pehli slip.

### [02:30 – 05:15] Scene 2: Shebang, Chalana aur Variables
**[VISUAL: A file `hello.sh` with the first line `#!/usr/bin/env bash` highlighted. Terminal: `chmod u+x hello.sh`, `./hello.sh`. Then two variable lines: `name="Asha"` and `echo "Hello $name"`, with a red cross on `name = "Asha"`. Quote types compared: double quotes expand, single quotes do not.]**

**(Voiceover):**
Slip ki pehli line shebang hoti hai: `#!/usr/bin/env bash`. Ye batati hai ki is parchi ko padhne wala assistant bash hai. Phir wahi cheez jo Session 4 mein seekhi thi: parchi par execute ka haq do, `chmod u+x hello.sh`, aur chalao `./hello.sh`. Variable ek naam wala dabba hai. `name="Asha"` mein `=` ke dono taraf space nahi hota. Space daala to bash socha ki `name` koi command hai. Dabba kholne ke liye `$name`. Double quotes ke andar dabba khul jaata hai, single quotes mein nahi, wahan jo likha hai wahi print hota hai. Aur ek aadat abhi se: variable ko hamesha double quotes mein likho, `"$name"`. Warna agar uski value mein space ho, jaise ek folder ka naam `booking site`, to bash use do tukdon mein tod deta hai aur command galat chal jaati hai.

### [05:15 – 07:55] Scene 3: Arguments, Output aur Input
**[VISUAL: `./greet.sh Asha 25` with a diagram: `$0` = script name, `$1` = Asha, `$2` = 25, `$#` = 2, `$@` = all. Then `today=$(date +%F)`. Then a prompt: `read -p "Name: " name`. A card: "backtick `date` = old style, `$( )` = use this".]**

**(Voiceover):**
Parchi ko bahar se kuch dena ho to arguments. `./greet.sh Asha 25` mein `$0` parchi ka apna naam hai, `$1` Asha, `$2` 25. `$#` batata hai kitne arguments aaye, aur `$@` sabhi arguments ek saath. Kisi command ka jawab dabbe mein rakhna ho to `$( )` lagao: `today=$(date +%F)` aaj ki tareekh ek variable mein rakh deta hai. Purane scripts mein aap ulte quote, yaani backticks, bhi dekhoge, wahi kaam karte hain, par `$( )` padhna aasaan hai aur uske andar `$( )` bhi aa sakta hai. Aur agar parchi chalate waqt insaan se kuch poochna ho to `read -p "Name: " name`. In teen cheezon, argument, command ka output aur input, se ek hi parchi alag alag kaam ke liye chal jaati hai. Har baar usse badalna nahi padta.

### [07:55 – 11:05] Scene 4: Jawab ka Raasta: Redirect aur Pipe
**[VISUAL: Terminal, one idea per line: `ls > list.txt`, `echo "entry" >> log.txt`, `grep ERROR app.log 2> errors.txt`, `./run.sh > out.txt 2>&1`, `ls | wc -l`, `./noisy.sh > /dev/null`. A drain labelled `/dev/null` at the edge of the desk.]**

**(Voiceover):**
Parchi jo bhi kare, uska jawab kahin na kahin jaata hai, aur ye raaste samajhna zaroori hai. Normal jawab ek raaste se aata hai, aur galtiyan ek alag raaste se, jise error stream kehte hain. `>` jawab ko ek file mein likhta hai, aur purani file mita deta hai. `>>` purani file ke aakhir mein jodta hai, jo logbook ke liye sahi hai. Galtiyon ko alag file mein bhejna ho to `2>`. Aur `> out.txt 2>&1` ka matlab hai: normal jawab bhi aur galtiyan bhi, dono ek hi file mein. Pipe, yaani `|`, jo Session 3 mein dekha tha, ek command ka jawab seedha doosri command ko haath mein de deta hai: `ls | wc -l` folder ki files ginta hai. Aur `/dev/null` ek nali hai jisme jo bhi dalo gayab ho jaata hai. Cron wale episode mein `>> log 2>&1` isi ka seedha upyog hoga: parchi ka har jawab, galtiyon ke saath, ek logbook mein.

### [11:05 – 13:35] Scene 5: Lab: Building ki Report Slip
**[VISUAL: `info.sh` in an editor; terminal prints one line with hostname, user and date, then the disk line. Then the same script run with a folder argument and a size line appears.]**

**(Voiceover):**
Lab. Ye slip likho aur `info.sh` naam se save karo:
```bash
#!/usr/bin/env bash
host=$(hostname)
user=$(whoami)
today=$(date +%F)
echo "Building: $host | Staff: $user | Date: $today"
df -h / | tail -1
```
`chmod u+x info.sh` karo aur `./info.sh` chalao. Ab ek badlaav: parchi ko ek folder ka naam argument mein do, aur wo us folder ka size bhi print kare. Isliye aakhir mein ek line jodo: `du -sh "$1"`. Chalao `./info.sh ~/atithi-booking`. Agar abhi Session 16 nahi hua to koi bhi folder chalega. Ek parchi, do tarah ke kaam, aur is baar `"$1"` quotes mein hai, to space wale folder ke naam par bhi chalegi. Bina argument chalaoge to `du: invalid zero-length file name` aayega; uska ilaaj Episode 3 mein hai.

### [13:35 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "#! · var=value · \"$var\" · $1 $@ $# · $(cmd) · read". Under it, small: "slip · box · hand-over note".]**

**(Voiceover):**
Recap: shebang, variables, quotes, arguments, command ka output aur input. Abhi hamari parchi sirf seedhi line mein chalti hai. Ab use faisle lena sikhate hain: agar ye ho to wo, warna kuch aur.

---

# 📺 EPISODE 2: Faisle aur Doharav

### [00:00 – 01:30] Scene 1: Slip Soch Sake To?
**[VISUAL: A slip that says "copy the guest register to the archive". The assistant follows it blindly even though the register is missing, and hands over an empty folder. Red stamp. Then a second slip that begins: "First check the register exists."]**

**(Voiceover):**
Ek parchi jo bina dekhe chale, chhoti galti par bada nuksaan karti hai. Parchi kehti hai guest register archive mein copy karo, aur register hai hi nahi. Assistant bina dekhe khaali folder thama deta hai, aur kisi ko pata bhi nahi chalta. Achhi parchi pehle poochhti hai: file hai? Building jawab de rahi hai? Disk bhari to nahi? Faisle ke liye conditions hain, aur ek kaam baar baar karne ke liye loops.

### [01:30 – 05:00] Scene 2: if, test aur case
**[VISUAL: An `if [ -f "$file" ]; then ... else ... fi` block, with test flags beside it: `-f` file, `-d` directory, `-z` empty string, `-eq -gt -lt` numbers, `==` strings. A second panel: a `case` block with `start)`, `stop)`, `restart)` and a `*)` default.]**

**(Voiceover):**
Faisle ka dhaancha hai `if [ condition ]; then ... fi`. Square brackets ke andar spaces zaroori hain. Ek `[` bhi darasal ek chhoti command hai, isliye uske baad space chahiye. File hai ya nahi, ye `-f` se. Folder ke liye `-d`, khaali string ke liye `-z`. Numbers ki tulna `-eq`, `-gt`, `-lt` se, aur strings ki `==` se. Ye dono alag hain, aur isi mein aksar galti hoti hai. `[[ 95 > 100 ]]` bhi sach nikalta hai, kyunki `>` akshar ke kram se tulna karta hai; numbers ke liye `-gt`. Aur `[ -f$f ]` bina space ke chupchap sach ho jaata hai, jabki `[-f` seedha "command not found" deta hai. Ab wo galti: `[ "$disk" -gt 90 ]` number ki tulna hai, `[ "$cmd" == "start" ]` string ki. Agar kai alag raaste hon, jaise `start`, `stop`, `restart`, to lambi `if` ki chain ki jagah `case` saaf padhta hai. Har raaste ke aakhir mein do semicolon, aur sabse neeche `*)`, yaani jo kisi mein na aaye uska default jawab.

### [05:00 – 07:50] Scene 3: for aur while
**[VISUAL: A loop `for f in *.log; do echo "$f"; done` highlighting each file in turn. A counter loop `for i in {1..5}`. A `while read -r line; do ...; done < file.txt` streaming lines from a file. A warning card: "ssh inside a while-read loop? use `ssh -n`".]**

**(Voiceover):**
`for f in *.log; do echo "$f"; done` har log file par ek ek kaam karta hai. Ginti ke liye `for i in {1..5}`. Aur ek file ki har line par kaam ho, jaise building ki list, to `while read -r line; do ...; done < list.txt`. `-r` ka matlab hai ki backslash ko jaisa hai waisa rehne do. Ek chhoti sachchai: us loop ke andar agar koi command, jaise `ssh`, bhi input padhne lage to wo file ki baaki lines nigal leta hai, aur loop do line mein hi khatam ho jaata hai. Us command par `-n` lagao, `ssh -n`, aur kaam chalega. Loop ke andar conditions bhi laga sakte ho, jaise sirf bade files pakadna. Aur DevOps ki roz ki sachchai: building ki list par ek loop chalana, har ek ko jaanchna, yahi automation ki shuruaat hai.

### [07:50 – 11:05] Scene 4: && aur ||, aur Double Bracket
**[VISUAL: Terminal: `mkdir releases && cd releases`, `ping -c1 8.8.8.8 || echo "no network"`. Then a comparison card: `[ ... ]` works in every shell, `[[ ... ]]` is bash only and understands patterns: `[[ $name == a* ]]`, `[[ -f $f && -r $f ]]`.]**

**(Voiceover):**
Do chhote jodne wale nishaan bahut kaam aate hain. `&&` ka matlab: pehli command theek chali to hi doosri chalao. `mkdir releases && cd releases`: folder bana to andar jao. `||` ka matlab: pehli command fail hui to hi doosri chalao. `ping -c1 8.8.8.8 || echo "no network"`. Dono ko ek lambi parchi ki jagah ek line mein likha ja sakta hai, par line lambi ho to saaf `if` hi behtar hai. Ab ek aur hissa. Bash mein `[ ]` ke alawa double bracket `[[ ]]` bhi hai. Wo sirf bash mein chalta hai, par uske do faayde hain: isme pattern milaye ja sakte hain, jaise `[[ $name == a* ]]`, aur isme variable ke quotes ki utni chinta nahi. Wo ek hi line mein `&&` bhi samajhta hai: `[[ -f $f && -r $f ]]`. Seedhi baat: agar parchi sirf bash par chalegi, to `[[ ]]` use karo. Agar sab shells par chalani ho, to `[ ]`.

### [11:05 – 13:25] Scene 5: Lab: Buildings ka Roll Call
**[VISUAL: A `servers.txt` with three names: `localhost`, `8.8.8.8` and a made-up name. The script loops and prints UP/DOWN with a count at the end.]**

**(Voiceover):**
Lab. Maan lo Atithi ki kai buildings hain. Ek file `servers.txt` mein unke naam likho: `localhost`, `8.8.8.8` aur ek galat naam. Phir ye slip:
```bash
#!/usr/bin/env bash
down=0
while read -r host; do
  if ping -c1 -W1 "$host" >/dev/null 2>&1; then
    echo "UP   $host"
  else
    echo "DOWN $host"
    down=$((down + 1))
  fi
done < servers.txt
echo "Not answering: $down"
```
Chalao aur UP aur DOWN dekho. `>/dev/null 2>&1` ka matlab: ping ka apna shor chhupao, taaki sirf humara message dikhe. Aakhir mein jo ginti aati hai, wo agle episode mein kaam aayegi. Dhyaan rahe: kuch buildings ping ka jawab hi nahi deti, to DOWN ka matlab pakka band hona nahi, "ping ka jawab nahi" hai.

### [13:25 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "if / case · test flags · numbers vs strings · for · while read -r". Under it, small: "check first · repeat for every building".]**

**(Voiceover):**
Recap: faisle aur dohrav. Par ek sawaal baaki hai. Ye parchi agar beech mein kisi kadam par fail ho jaaye, to kya wo aage chalti rahegi? Agla episode isi ke baare mein hai: parchi ko surakshit kaise banate hain.

---

# 📺 EPISODE 3: Safe Slip

### [00:00 – 01:30] Scene 1: Slip Jo Galti ke Baad Bhi Chalti Rahi
**[VISUAL: A release slip with three steps: "1 copy new site files, 2 check them, 3 remove the old release". Step 2 fails silently; step 3 still runs and the old release goes into the shredder. The booking page goes blank. Red alarm.]**

**(Voiceover):**
Ek release ki parchi mein teen kadam hain: nayi website ki files rakho, unhe jaancho, aur purana release hata do. Kadam do fail ho gaya, par parchi ruki nahi. Teen chalu hua aur purana release bhi chala gaya. Ab na naya hai, na purana, aur guests ko khaali page dikh raha hai. Bash by default galti par rukta nahi, wo agli line par badh jaata hai. Isliye bash ki sabse zaroori seekh: parchi ko safe mode mein likho.

### [01:30 – 04:35] Scene 2: set -euo pipefail aur Exit Code
**[VISUAL: Three flags animated one by one: `-e` stops on error, `-u` fails on an unset variable (with `rm -rf "$DIR/"` going red when `$DIR` is empty), `-o pipefail` fails if any stage of a pipe fails. Then `echo $?` printing 0 and 1. A trap line: `trap 'echo cleanup' EXIT`.]**

**(Voiceover):**
Parchi ki shuruaat mein ek line likho: `set -euo pipefail`. `-e` ka matlab: koi command fail ho to parchi wahin ruk jaaye. `-u` ka matlab: jo variable kabhi bana hi nahi, use chhoo to error do. Ye `rm -rf "$DIR/"` jaisi bhayanak galti se bachata hai, jahan `DIR` khaali ho aur command seedhi jad par chal jaaye. `pipefail` ka matlab: pipe ke beech ka koi hissa fail ho to bhi poora pipe fail maano. Har command ke baad uska status `$?` mein hota hai, aur zero ka matlab sab theek. `echo $?` se khud dekh lo. Ek chhoti sachchai: `-e` ki ek seema hai. `if` ke andar ya `||` ke saath chalayi gayi command ke fail hone par wo parchi nahi rokta, kyunki wahan fail hona ek jawab hai, galti nahi. Aur safai ke liye `trap 'echo cleanup' EXIT` ek aisa kaam hai jo parchi ke har tarah se khatam hone par chalta hai, chahe sab theek ho ya na ho.

### [04:35 – 07:45] Scene 3: Functions: Ek Baar Likho, Baar Baar Use Karo
**[VISUAL: A function `log() { echo "[$(date +%T)] $*"; }` called from several lines of a script. Another function `check_disk()` with a `local` variable and a `return 1`. At the end, a `main "$@"` line.]**

**(Voiceover):**
Jo kaam parchi mein baar baar likhna pade, use function bana do: `log() { echo "[$(date +%T)] $*"; }`. Ab har jagah sirf `log "disk check"` likho. Function ke arguments bhi `$1`, `$2` hote hain, parchi ke apne arguments ki tarah. `local` lagane se variable function ke andar tak rehta hai aur bahar ki cheezein kharab nahi karta. `return` ek status code deta hai, yaani zero ya non-zero, text nahi. Text wapas chahiye to function usse `echo` kare aur bahar `$( )` use karo. Ek jaal: jis function ka jawab `$( )` se pakadna ho, uske andar ka `log` agar stdout par likhe, to wo bhi pakda jaata hai; humne `pct=$(check_disk)` mein log ki line aur number dono ek saath paaye. `log` ko `>&2` par bhejo, to sirf number aata hai. Aur ek achha dhancha: poori parchi `main()` function mein rakho, aur sabse neeche ek line `main "$@"`. Padhne wale ko upar se hi pata chal jaata hai ki parchi kya kya karti hai.

### [07:45 – 10:15] Scene 4: Parchi Galat Chale to: bash -x aur shellcheck
**[VISUAL: A slip that prints the wrong thing. Terminal: `bash -n script.sh` (syntax check only), `bash -x script.sh` showing each command with a `+` prefix before it runs, `set -x` / `set +x` around three lines, then `shellcheck script.sh` underlining an unquoted `$file` with a warning code.]**

**(Voiceover):**
Parchi galat chale to ghabrane ki zaroorat nahi, bash khud batata hai ki wo kya kar raha hai. `bash -n script.sh` parchi ko chalaye bina sirf uska vyakaran jaanchta hai. `bash -x script.sh` har command ko chalane se pehle ek plus ke saath dikha deta hai, aur variable ki asli value bhi. Isse turant dikh jaata hai ki kaun si line mein galat value aayi. Poori parchi nahi, sirf teen lines ko dekhna ho to un se pehle `set -x` aur baad mein `set +x` likho. Doosra aujaar hai shellcheck. `sudo apt install shellcheck`, phir `shellcheck script.sh`, aur wo parchi padh kar bata deta hai ki kahan quotes chhoot gaye, kahan variable galat hai. Ye parchi ka grammar-checker hai, aur ek achhi aadat hai ki har naye script par ek baar chalao.

### [10:15 – 13:25] Scene 5: Lab: Session 05 ki Health-Check Parchi ko Sudharo
**[VISUAL: The earlier `healthcheck.sh` opens on the left; on the right, the improved version using functions, safe mode and a usage message. Running it without arguments shows the usage line; running with a bad service name shows FAIL and exit code 1.]**

**(Voiceover):**
Lab. Session 5 ki `healthcheck.sh` yaad hai? Aaj use asli parchi banate hain.
```bash
#!/usr/bin/env bash
set -euo pipefail

log()   { echo "[$(date +%T)] $*"; }
usage() { echo "Usage: $0 <service> [disk-limit-percent]"; exit 1; }

[ $# -ge 1 ] || usage
service="$1"
limit="${2:-90}"
fail=0

disk=$(df / --output=pcent | tail -1 | tr -dc '0-9')
if [ "$disk" -ge "$limit" ]; then log "FAIL disk ${disk}%"; fail=1; else log "OK   disk ${disk}%"; fi

if systemctl is-active --quiet "$service"; then log "OK   $service"; else log "FAIL $service"; fail=1; fi

exit "$fail"
```
Bina argument chalao: saaf usage message aata hai. `./healthcheck.sh nginx` chalao: dono OK. Ab `./healthcheck.sh nginx 1` chalao, disk ki limit ek percent, to FAIL aayega aur `echo $?` mein 1. Ek nayi cheez dekho: `${2:-90}` ka matlab hai doosra argument diya ho to wo, warna 90. Ek ek jagah ek hi kaam, aur parchi ka aakhri jawab exit code mein. Isi tarah ki parchi ko cron aur monitoring bina insaan ke padh sakte hain.

### [13:25 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "set -euo pipefail · trap · functions · local · ${var:-default} · exit codes".]**

**(Voiceover):**
Recap: safe mode, functions, default values aur exit codes. Ab ek parchi ban gayi jo bharosemand hai. Par wo abhi bhi tabhi chalti hai jab aap desk par ho. Agla episode: parchi ko timetable par rakhna, aur ek asli backup.

---

# 📺 EPISODE 4: Timetable

### [00:00 – 01:10] Scene 1: Raat Do Baje Kaun Jaage?
**[VISUAL: A clock at 2:00 AM on the Atithi building wall. The manager is asleep at home. A small mechanical timetable board in the back office clicks over, and an assistant picks up a slip and carries it out. Text: "cron".]**

**(Voiceover):**
Booking website ka backup raat do baje lena hai, jab guests kam hote hain. Aap to so rahe honge. Linux ke paas ek timetable hai jo aapke bina parchiyan chalata hai, aur uska naam cron hai. Aaj ke episode ka maksad: ek parchi likhna jo booking website ka backup le, purane backups hataye, aur timetable se khud chale.

### [01:10 – 03:35] Scene 2: cron ka Syntax
**[VISUAL: A crontab line with five time fields labelled minute, hour, day of month, month, day of week, then the command. Examples highlighted one by one: `0 2 * * *`, `*/15 * * * *`, `0 9 * * 1`. Terminal: `crontab -e`, `crontab -l`.]**

**(Voiceover):**
`crontab -e` se aap apna timetable likhte ho, aur `crontab -l` use dikhata hai. Har line mein paanch time ke khaane aate hain, aur uske baad command. Khaane hain: minute, ghanta, mahine ka din, mahina, aur hafte ka din. Sitara matlab "har". To `0 2 * * *` matlab har din ke do baje, zero minute par. `*/15 * * * *` har paandrah minute mein. `0 9 * * 1` har somvaar subah nau baje. Ek zaroori baat: cron ka apna environment bahut chhota hota hai. Aapka login wala PATH wahan nahi hota. Isliye parchi ka poora path likho, jaise `/home/ubuntu/backup.sh`, aur uska jawab ek log file mein bhejo: `>> /var/log/backup.log 2>&1`. Warna agar kuch toota to kahin likha hi nahi milega.

### [03:35 – 05:40] Scene 3: Backup Slip ka Design
**[VISUAL: A flowchart: check the source folder exists → create `backup-YYYYMMDD-HHMM.tar.gz` → list its contents to verify → delete backups older than 7 days → log result. A side card: "never keep the backup on the same disk as the data".]**

**(Voiceover):**
Achhi backup parchi paanch kaam karti hai. Pehla, source folder hai ya nahi, ye jaanchna. Doosra, `tar.gz` banana, jisme naam mein tareekh aur samay ho, taaki har baar alag file bane. Teesra, jaanchna ki archive sahi bani hai: `tar -tzf` uske andar ki files ki list deta hai, aur list na aaye to archive kharab hai. Chautha, purane backups hatana, jaise `find /backups -name "backup-*.tar.gz" -mtime +7 -delete`, yaani saat din se purane. Paanchwa, ek line log mein likhna. Aur ek rule jo is parchi se bhi bada hai: backup kabhi usi disk par mat rakho jahan asli data hai. Disk gayi to dono gaye.

### [05:40 – 09:15] Scene 4: Lab: Booking Site ka Backup aur cron
**[VISUAL: The script runs against `~/atithi-booking`; a `.tar.gz` appears in `/tmp/backups`. `crontab -l` shows the two-minute test schedule. Two minutes later a second archive appears and the log file shows two OK lines.]**

**(Voiceover):**
Lab. Ye parchi `backup.sh` mein likho:
```bash
#!/usr/bin/env bash
set -euo pipefail
src="${1:?usage: backup.sh <folder>}"
dest="/tmp/backups"
mkdir -p "$dest"
file="$dest/backup-$(date +%Y%m%d-%H%M).tar.gz"
tar -czf "$file" -C "$src" .
tar -tzf "$file" >/dev/null
find "$dest" -name 'backup-*.tar.gz' -mtime +7 -delete
echo "$(date +%T) OK $file"
```
`chmod u+x backup.sh` karo aur chalao `./backup.sh ~/atithi-booking`. Ek `.tar.gz` banegi. Ab timetable: `crontab -e` mein ye line jodo, apna poora path likh kar: `*/2 * * * * /home/aap/backup.sh /home/aap/atithi-booking >> /tmp/backup.log 2>&1`. Do minute baad doosra backup aur log mein nayi line dikhegi. Dhyaan rahe, `/tmp` sirf abhyas ke liye hai, asli backup kisi doosri jagah, jaise cloud storage mein jaana chahiye, jo hum S3 ke session mein karenge. Test ke baad timetable se do-minute wali line zaroor hata do, warna folder bharta jayega. Ek kami humne pakdi: isi minute dobara chalane par agar source galat ho, to `tar -czf` pehle se bani achhi file ko 20 byte ki khaali file bana deta hai, aur `tar -tzf` use bhi theek maanta hai. Ilaaj: pehle `file.part` naam par banao, jaancho, aur tabhi `mv` se asli naam do.

### [09:15 – 13:00] Scene 5: Timetable Gadbad Kare to
**[VISUAL: A timetable board with a slot that did not run. Terminal: `grep CRON /var/log/syslog | tail`, `journalctl -u cron -n 20`, a crontab with `SHELL=/bin/bash` and `PATH=/usr/local/bin:/usr/bin:/bin` at the top, a line using `\%` in a date format, and a lock wrapper: `flock -n /tmp/backup.lock ./backup.sh ...`.]**

**(Voiceover):**
Timetable ki line daal di, aur kuch chala hi nahi. Pehle dekho cron ne parchi uthayi ya nahi. Ubuntu par `grep CRON /var/log/syslog` ya `journalctl -u cron` uska logbook hai. Red Hat family mein wahi service `crond` hai aur uska log `/var/log/cron` mein. Agar cron ne parchi uthayi par wo fail hui, to teen aam wajah hain. Ek, relative path: parchi ke andar `./data` likha hai, par cron ka kaam karne ka folder alag hota hai. Poora path do. Do, PATH: cron ke paas aapka login wala PATH nahi hota. Timetable ke upar `PATH=` aur `SHELL=/bin/bash` likh sakte ho. Teen, percent ka nishaan. Crontab ki line ke andar `%` ka matlab nayi line hota hai, isliye `date +%F` seedha crontab mein likhna ho to `\%F` likhna padta hai. Isliye date wali cheezein parchi ke andar rakho, timetable mein nahi. Ek aur khatra: agar ek backup abhi chal raha hai aur timetable doosra shuru kar de, to dono bhidte hain. `flock -n /tmp/backup.lock ./backup.sh ...` doosre ko chalne hi nahi deta. Aur `@reboot` ya `@daily` jaise chhote naam bhi hote hain, jo aam mauqon par saaf padhe jaate hain.

### [13:00 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "cron: 5 fields · full paths · log the output · verify the archive · delete old ones". Then a teaser: the assistant fumbling with a long, messy slip full of nested quotes and special characters, and a cleaner, trained officer stepping in.]**

**(Voiceover):**
Recap: bash se aap Linux ke roz ke kaam ko automate kar sakte ho. Parchi likhna, use surakshit banana, aur timetable par chadhana. Par jab parchi mein JSON padhna ho, landlord ke office ko phone karna ho, ya logic bada ho jaaye, to bash thakane lagta hai. Agle session mein ek trained operations officer aata hai: Python, aur uska landlord ke office tak ka phone, boto3.

---

# 📎 Student handout: Session 06 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Likhne ka tareeka |
|---|---|
| Shebang | `#!/usr/bin/env bash` |
| Chalana | `chmod u+x file.sh`, `./file.sh` |
| Variable | `name="Asha"`, padhna: `"$name"` |
| Arguments | `$1 $2`, `$#` ginti, `$@` sab, `$0` script ka naam |
| Command ka output | `today=$(date +%F)` |
| Input | `read -p "Name: " name` |
| Default value | `${2:-90}` |
| File / folder jaanch | `[ -f file ]`, `[ -d dir ]`, `[ -z "$s" ]` |
| Number tulna | `-eq -ne -gt -ge -lt -le` |
| String tulna | `==`, `!=` |
| Loop | `for f in *.log; do ...; done`, `while read -r line; do ...; done < file` |
| Safe mode | `set -euo pipefail` |
| Safai | `trap 'cleanup' EXIT` |
| Exit code | `exit 0` theek, `exit 1` galti, `echo $?` dekhne ke liye |
| Function | `name() { ...; }`, `local var=...`, `main "$@"` |
| cron | `crontab -e`, `crontab -l`; `m h dom mon dow command` |
| cron ke liye | poora path, `>> log 2>&1` |
| Backup | `tar -czf out.tar.gz -C src .`, `tar -tzf out.tar.gz`, `find dir -mtime +7 -delete` |

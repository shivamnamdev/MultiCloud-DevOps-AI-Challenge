# ✍️ 02: SCRIPT — SESSION-03: Linux Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S03`
- **Focus:** Why Linux, architecture (kernel/shell), filesystem hierarchy, core commands, files/text tools, getting a Linux VM
- **Story position:** Zoom level 1, inside one building. Atithi Hotels ko apni pehli kiraye ki building ki chaabi milti hai.
- **Story words introduced:** core management office (kernel), instruction desk (shell), main lobby (`/`), kamra aur almari (directory aur file), staff quarters (`/home`), admin office (`/etc`), logbook room (`/var/log`), staff entrance (SSH)
- **Episodes:**
  - Episode 1: Linux kyun? Kernel, Shell aur Distributions
  - Episode 2: Filesystem ka Naksha: / se shuru
  - Episode 3: Core Commands: navigate, create, copy, search
  - Episode 4: Text ka Jaadu: cat, grep, pipes aur apni Linux VM

---

# 📺 EPISODE 1: Linux kyun?

### [00:00 – 03:15] Scene 1: Har Server ka Ek Hi Raaz
**[VISUAL: A world map of data centers. Zoom into a rack, then a boot screen showing a penguin logo. Text: "Most of the cloud runs on this". Then a hand receives the keys to an empty building with an "Atithi Hotels" board.]**

**(Voiceover):**
Session 1 mein Atithi Hotels ne tay kiya tha ki building landlord se kiraye par lenge. Aaj us pehli building ki chaabi milti hai. Par building khaali hai. Use chalane ke liye andar ek management system chahiye: staff, kamre, taale, logbooks. Wo management system Linux hai. AWS ke servers, Google ke servers, Kubernetes ke nodes, Docker ke containers: inke andar zyadatar ek hi cheez chal rahi hai, Linux. Agar aap DevOps seekhna chahte ho, to Linux seekhna optional nahi hai. Achhi baat ye hai ki Linux ko rat ke nahi, samajh ke seekhna hai. Is session ke baad aap kisi bhi Linux server mein jaakar ghabraoge nahi.

### [03:15 – 06:15] Scene 2: Kernel aur Shell: Management Office aur Instruction Desk
**[VISUAL: Inside the building: You (staff) → Instruction desk (shell) → Core management office (kernel) → Power, water, lifts (hardware). Arrows labelled with commands.]**

**(Voiceover):**
Atithi ki building socho. Bijli, paani aur lift ki machines ko koi seedha haath nahi lagata. Unhe ek core management office control karta hai: ye kernel hai. Aur aap us office tak apni baat ek instruction desk ke through pahunchate ho: ye shell hai. Aap desk par instruction dete ho, jaise `ls`. Desk use management office tak bhejta hai, aur kernel hardware se kaam karwa kar jawab wapas karta hai. Kernel Linux ka dil hai: memory, CPU, disk aur process, sab wahi sambhalta hai. Shell wo program hai jo aapki commands ko kernel tak pahunchata hai, jaise Bash.

### [06:15 – 09:05] Scene 3: Distributions aur Open Source
**[VISUAL: A family tree: Linux kernel → Debian → Ubuntu; Red Hat → RHEL/Rocky/CentOS-Stream/Fedora; Alpine; Amazon Linux.]**

**(Voiceover):**
Linux sirf kernel hai. Uske saath tools aur package manager jod kar jo poora system banta hai, use distribution kehte hain. Debian family mein Ubuntu hai, jo apt use karta hai. Red Hat family mein RHEL aur Rocky jaise distros hain, jo dnf ya yum use karte hain. Alpine bahut chhota hota hai aur containers mein aam hai. Amazon Linux AWS ke liye bana hai. Concept sab mein ek jaise hain; fark mostly package manager aur kuch paths ka hota hai. Ye sab open source hai, to koi bhi code padh sakta hai.

### [09:05 – 11:25] Scene 4: Lab: Pehli Command
**[VISUAL: A terminal. User types `whoami`, `hostname`, `uname -a`, `cat /etc/os-release`. Each output is annotated.]**

**(Voiceover):**
Lab. Terminal kholo, yaani instruction desk par aao. `whoami` batata hai aap kaun ho. `hostname` machine ka naam, yaani is building ka naam. `uname -a` kernel ki jaankari. `cat /etc/os-release` batata hai kaun sa distribution aur version chal raha hai. Ye chaaron commands har naye server par sabse pehle chalte hain, kyunki kisi bhi machine par kaam karne se pehle pata hona chahiye ki aap kahan ho. Screenshot lo aur apni notebook mein output likh lo.

### [11:25 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A mini diagram: You → Shell → Kernel → Hardware. Under it, small: "you → instruction desk → management office → machines".]**

**(Voiceover):**
Recap: Linux cloud ka base hai, kernel yaani management office hardware sambhalta hai, shell yaani instruction desk aapki baat kernel tak le jaata hai, aur distributions alag packaging hain. Ab is building ka naksha chahiye. Linux ka filesystem Windows se bilkul alag dikhta hai, aur agla episode usi ka naksha hai.

---

# 📺 EPISODE 2: Filesystem ka Naksha

### [00:00 – 02:40] Scene 1: C Drive Kahan Hai?
**[VISUAL: A Windows Explorer with C:, D:. It morphs into a hotel floor plan with one main lobby marked `/`, and every corridor branching from it like an upside-down tree.]**

**(Voiceover):**
Windows mein C drive, D drive hote hain. Linux mein koi drive letter nahi. Atithi ki building ki tarah, yahan ek hi main lobby hai, aur har corridor wahin se shuru hota hai. Us lobby ko `/` kehte hain, root. Har file, har folder, har device, usi se nikalti ek shaakha hai. Is building mein kamra yaani directory, aur kamre ke andar ki almari yaani file. Is naksha ko samajh liya to server par kuch bhi dhoondhna aasaan ho jata hai.

### [02:40 – 06:30] Scene 2: Zaroori Directories ka Tour
**[VISUAL: An animated floor plan. Highlighted in turn: /home (staff quarters), /etc (admin office), /var (logbook room inside), /bin and /usr (tool room), /tmp (lost-and-found), /root (general manager's cabin), /dev (equipment room), /proc (live status board). Each gets a small icon and a one-line description.]**

**(Voiceover):**
Building ka tour karte hain. `/home` staff quarters hain: har user ka apna kamra aur apni files. `/etc` admin office hai, jahan saari rulebooks rakhi hain, yaani configuration files. `/var` mein badalne wala data rehta hai, aur uske andar `/var/log` logbook room hai. `/bin` aur `/usr/bin` tool room hain, jahan commands ke programs rakhe hain. `/tmp` lost-and-found hai, temporary files ke liye. `/root` general manager ka cabin, yaani root user ka home. `/dev` equipment room, jahan devices ki files hain. `/proc` ek live status board hai, ek virtual jagah jahan kernel running processes ki jaankari dikhata hai. Rule of thumb: kuch kharab ho to logbook room dekho, `/var/log`, aur settings ke liye admin office, `/etc`.

### [06:30 – 08:55] Scene 3: Absolute vs Relative Path, aur Special Symbols
**[VISUAL: A path `/home/asha/projects/app` is drawn from the main lobby. Then relative hops: `.` (here), `..` (parent), `~` (home).]**

**(Voiceover):**
Path do tarah ke hote hain. Absolute path `/` se shuru hota hai, yaani main lobby se poora raasta, jaise `/home/asha/projects`. Relative path wahan se shuru hota hai jahan aap abhi khade ho, jaise `projects/app`. Teen symbols yaad rakho. Ek dot matlab yahin ki directory. Do dots matlab ek level upar. Aur `~` matlab aapka home directory. Aur ek zaroori baat: Linux case-sensitive hai, to `App` aur `app` do alag cheezein hain.

### [08:55 – 11:40] Scene 4: Lab: Building mein Ghoomo
**[VISUAL: Terminal: `pwd`, `ls -l /`, `cd /var/log`, `ls`, `cd ~`, `cd ..`, `cd -`.]**

**(Voiceover):**
Lab: `pwd` se current jagah dekho. `ls -l /` se main lobby ke saare darwaze, yaani root ke andar ke folders. `cd /var/log` karo aur `ls` chalao, ye wahi logbook room hai jahan system ke logs milte hain. `cd ~` se home par wapas. `cd ..` se ek level upar, aur `cd -` se pichli jagah par. Ab apne hi haath se `/etc` mein jaakar `ls` chalao. Aapko admin office ki rulebooks dikhengi. Dhyaan: abhi kuch badalna nahi hai, sirf dekhna hai.

### [11:40 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A cheat card: "/etc config, /var/log logs, /home users, /tmp temp".]**

**(Voiceover):**
Recap: ek building, ek main lobby, sab kuch `/` se shuru. Config admin office mein, `/etc`, aur logs logbook room mein, `/var/log`. Navigation aa gayi. Ab files banana, copy karna, hatana aur dhoondhna seekhte hain, aur wo bhi safely.

---

# 📺 EPISODE 3: Core Commands

### [00:00 – 02:10] Scene 1: Ek Galti, Poora Server Gaya
**[VISUAL: A terminal with `rm -rf /` typed. A big warning hand appears before Enter. Text: "Commands are sharp tools".]**

**(Voiceover):**
Linux mein delete ka koi recycle bin nahi hota. Isliye ye episode commands sikhaata hai, lekin saath mein safe aadat bhi. Ek rule: jo command aap samjhe nahi, wo kabhi production par mat chalao. Aur `rm -rf` ke saath path hamesha do baar padho.

### [02:10 – 05:55] Scene 2: Banana, Copy, Move, Delete
**[VISUAL: Terminal commands with outcome icons: `mkdir`, `touch`, `cp`, `mv`, `rm`, `rmdir`.]**

**(Voiceover):**
`mkdir` naya kamra banata hai, yaani folder. `touch` ek khaali almari, yaani khaali file. `cp source dest` copy karta hai, folder ke liye `cp -r`. `mv` move karta hai aur rename bhi, kyunki rename bas ek move hai. `rm` file hatata hai, aur `rm -r` folder ko andar ki cheezon ke saath. Safe aadat: pehle `ls` se dekho kya hatane wale ho, aur seekhte waqt `rm -i` ka use karo, jo har delete se pehle poochta hai.

### [05:55 – 09:15] Scene 3: Dhoondhna: find aur which
**[VISUAL: Terminal: `find /var/log -name "*.log"`, `find . -type f -mtime -1`, `which python3`, `locate` mention.]**

**(Voiceover):**
Server par file kahan hai? `find` se. `find /var/log -name "*.log"` naam se dhoondhta hai. `find . -type f -mtime -1` pichle ek din mein badli hui files dikhata hai. `which python3` batata hai ki command ka program kis path par hai. Ye teen cheezein roz kaam aati hain, khaaskar jab koi bole ki "kal se kuch toota hai", to pata karo ki kal kaun si file badli.

### [09:15 – 11:40] Scene 4: Lab: Ek Mini Project Folder
**[VISUAL: Terminal builds `demo/{src,logs,config}`, creates files, copies one, renames one, and lists with `ls -R`.]**

**(Voiceover):**
Lab. `mkdir -p demo/{src,logs,config}` ek hi command mein teen folders banata hai. `touch demo/src/app.py demo/config/app.conf` files banao. `cp demo/config/app.conf demo/config/app.conf.bak` se backup. `mv demo/src/app.py demo/src/main.py` se rename. `ls -R demo` se poora tree dekho. Aakhir mein `rm -r demo` se saaf karo, aur dhyaan se padho kya hata rahe ho.

### [11:40 – 13:05] Scene 5: Recap aur Bridge
**[VISUAL: A cheat sheet card of the commands used.]**

**(Voiceover):**
Recap: mkdir, touch, cp, mv, rm, find, which. Ab ye files ke andar kya hai wo padhna aur filter karna seekhte hain. Agle episode mein pipes ka jaadu hai.

---

# 📺 EPISODE 4: Text ka Jaadu aur Apni Linux VM

### [00:00 – 02:05] Scene 1: Log File mein Ek Line Dhoondho
**[VISUAL: The logbook room, shelves full of registers. One register opens into a 100,000-line log file. A search beam moves down and highlights a single `ERROR` line.]**

**(Voiceover):**
Building ke logbook room mein ek lakh lines ki log file hai, aur usme ek error ki line dhoondhni hai. Notepad mein khol ke scroll karoge? Linux ne text ko ek power tool bana diya hai. Aaj hum seekhenge `cat`, `less`, `head`, `tail`, `grep`, aur sabse zaroori idea: pipe.

### [02:05 – 04:45] Scene 2: Padhne ke Tools
**[VISUAL: Terminal: `cat file`, `less file`, `head -n 5 file`, `tail -n 5 file`, `tail -f app.log` with live lines streaming.]**

**(Voiceover):**
`cat` poori file print karta hai. Badi files ke liye `less`, jisme upar neeche scroll karke `q` se bahar nikalte hain. `head -n 5` shuru ki paanch lines, `tail -n 5` aakhri paanch. Aur sabse popular, `tail -f app.log`: file ke ant mein jo nayi lines judti hain wo live dikhata hai. Deploy ke waqt isse logs dekhna DevOps ki roz ki aadat hai.

### [04:45 – 07:40] Scene 3: grep aur Pipe
**[VISUAL: A pipe diagram: `cat app.log` → `grep ERROR` → `sort` → `uniq -c`. Counts appear on the right.]**

**(Voiceover):**
`grep ERROR app.log` sirf wo lines dikhata hai jisme ERROR hai. `grep -i` case ignore karta hai, `grep -v` ulta, `grep -n` line number ke saath. Ab pipe: `|`, jo ek command ka output doosri command ka input bana deta hai. `grep ERROR app.log | sort | uniq -c` batata hai ki kaun si error kitni baar aayi. Chhoti commands ko jod kar bada kaam, yahi Linux ka philosophy hai.

### [07:40 – 11:00] Scene 4: Lab: Apni Linux VM aur Log Analysis
**[VISUAL: A split screen: cloud VM console on left (a Linux VM launched), terminal SSH session on right, with a small inset of a staff entrance door opening. A log file is created with `printf` and analysed.]**

**(Voiceover):**
Lab. Ek Linux VM lo, VirtualBox ya cloud ki free-tier, yaani apni pehli building. Uspar SSH karo. SSH is building ka staff entrance hai: staff isi darwaze se andar aata hai. Ek sample log banao: `printf "INFO start\nERROR db timeout\nERROR db timeout\nWARN slow\n" > app.log`. Ab `grep ERROR app.log | sort | uniq -c` chalao, aur dekho ki "db timeout" do baar aaya hai. Ye ek mini incident investigation hai, jo asli servers par bhi bilkul isi tarah hoti hai.

### [11:00 – 12:55] Scene 5: Recap aur Bridge
**[VISUAL: A card: "cat · less · head · tail · grep · | · sort · uniq".]**

**(Voiceover):**
Recap: padhna, filter karna, pipe se jodna. Aapke paas ab Linux ki neev hai: building ka naksha, navigation aur text tools. Agle session mein is building mein staff rakhenge aur kamron par taale lagayenge: users, permissions aur SSH keys, yaani server ko safe kaise rakhte hain.

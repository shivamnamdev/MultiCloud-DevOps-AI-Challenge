# ✍️ 02: SCRIPT — SESSION-03: Linux Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S03`
- **Focus:** Why Linux, kernel and shell, distributions, prompt and command anatomy, getting help (`--help`, `man`, Tab, history), filesystem hierarchy, absolute and relative paths, reading `ls -l` (file types, links, hidden files), core commands, wildcards, `nano` and `vi` basics, `find` and `which`, reading text (`cat`, `less`, `head`, `tail -f`), `grep`, pipes, redirects, `wc`, `sort`, `cut`, `uniq`, getting a Linux VM
- **Builds on:** Session 01 (the landlord, renting a building), Session 02 (using the assistant to explain a command, then checking it with `man`)
- **Lab project:** Atithi's first rented building, a Linux VM, and its logbook: walk the floor plan, build a small project folder, and find the error in a log
- **Cost rule:** a local VM costs nothing; a cloud free-tier VM can still bill, so stop or delete it after the lab and check the console
- **Tested with:** every command in this script was run on Ubuntu 24.04 in November 2026
- **Story position:** Zoom level 1, inside one building. Atithi Hotels ko apni pehli kiraye ki building ki chaabi milti hai.
- **Story words introduced:** core management office (kernel), instruction desk (shell), main lobby (`/`), kamra aur almari (directory aur file), staff quarters (`/home`), admin office (`/etc`), logbook room (`/var/log`), staff entrance (SSH)
- **Episodes:**
  - Episode 1: Linux kyun? Kernel, Shell aur Distributions
  - Episode 2: Filesystem ka Naksha: / se shuru
  - Episode 3: Core Commands: navigate, create, copy, search
  - Episode 4: Text ka Jaadu: cat, grep, pipes aur apni Linux VM

---

# 📺 EPISODE 1: Linux kyun?

### [00:00 – 02:10] Scene 1: Har Server ka Ek Hi Raaz
**[VISUAL: A world map of data centers. Zoom into a rack, then a boot screen showing a penguin logo. Text: "Most of the cloud runs on this". Then a hand receives the keys to an empty building with an "Atithi Hotels" board.]**

**(Voiceover):**
Session 1 mein Atithi Hotels ne tay kiya tha ki building landlord se kiraye par lenge. Aaj us pehli building ki chaabi milti hai. Par building khaali hai. Use chalane ke liye andar ek management system chahiye: staff, kamre, taale, logbooks. Wo management system Linux hai. AWS ke servers, Google ke servers, Kubernetes ke nodes, Docker ke containers: inke andar zyadatar ek hi cheez chal rahi hai, Linux. Agar aap DevOps seekhna chahte ho, to Linux seekhna optional nahi hai. Achhi baat ye hai ki Linux ko rat ke nahi, samajh ke seekhna hai. Is session ke baad aap kisi bhi Linux server mein jaakar ghabraoge nahi.

### [02:10 – 04:10] Scene 2: Kernel aur Shell: Management Office aur Instruction Desk
**[VISUAL: Inside the building: You (staff) → Instruction desk (shell) → Core management office (kernel) → Power, water, lifts (hardware). Arrows labelled with commands.]**

**(Voiceover):**
Atithi ki building socho. Bijli, paani aur lift ki machines ko koi seedha haath nahi lagata. Unhe ek core management office control karta hai: ye kernel hai. Aur aap us office tak apni baat ek instruction desk ke through pahunchate ho: ye shell hai. Aap desk par instruction dete ho, jaise `ls`. Desk use management office tak bhejta hai, aur kernel hardware se kaam karwa kar jawab wapas karta hai. Kernel Linux ka dil hai: memory, CPU, disk aur process, sab wahi sambhalta hai. Shell wo program hai jo aapki commands ko kernel tak pahunchata hai, jaise Bash.

### [04:10 – 06:05] Scene 3: Distributions aur Open Source
**[VISUAL: A family tree: Linux kernel → Debian → Ubuntu; Red Hat → RHEL/Rocky/CentOS-Stream/Fedora; Alpine; Amazon Linux.]**

**(Voiceover):**
Linux sirf kernel hai. Uske saath tools aur package manager jod kar jo poora system banta hai, use distribution kehte hain. Debian family mein Ubuntu hai, jo apt use karta hai. Red Hat family mein RHEL aur Rocky jaise distros hain, jo dnf ya yum use karte hain. Alpine bahut chhota hota hai aur containers mein aam hai. Amazon Linux AWS ke liye bana hai. Concept sab mein ek jaise hain; fark mostly package manager aur kuch paths ka hota hai. Ye sab open source hai, to koi bhi code padh sakta hai.

### [06:05 – 09:35] Scene 4: Command ka Dhancha aur Madad Kahan Milti Hai
**[VISUAL: A prompt `asha@atithi-web1:~$` with parts labelled: user, building name, where you are, `$`. A command `ls -l /etc` split into three colours: command, option, argument. Then a help trio: `ls --help`, `man ls`, and the Tab and Ctrl+R keys with a small lightning bolt.]**

**(Voiceover):**
Terminal kholte hi ek line dikhti hai, jaise `asha@atithi-web1:~$`. Usme user ka naam, building ka naam, abhi aap kahan ho, `~` matlab home, aur aakhir mein `$`. Dollar ka matlab hai aap normal staff ho. Agar `#` dikhe, to aap general manager, yaani root ho, aur har galti bhaari padti hai. Har command ka dhancha ek hi hota hai: command, option, argument. `ls -l /etc`: `ls` kaam hai, `-l` kaam ka tareeka, `/etc` kis par. Chhote options ek saath likh sakte ho, jaise `-la`. Ab sabse zaroori aadat: madad kahan milti hai. `ls --help` chhota summary deta hai. `man ls` poora manual, jisse `q` dabakar nikalte ho. Tab key naam poora kar deti hai. Upar ka arrow pichhli command laata hai, `history` poori list, aur Ctrl+R se purani command ka koi hissa type karke use dhoondh lo. Command atak jaaye to Ctrl+C. Ye chhoti aadatein hi Linux par tez banati hain, aur Session 2 ka assistant bhi yahin kaam aata hai: use poocho ki ye command kya karti hai, phir `man` se jaanch lo.

### [09:35 – 12:25] Scene 5: Apna Practice Ground: Teen Raaste
**[VISUAL: Three doors to a Linux building: a cloud VM (a rented building), a VM on your laptop (a model room), and a Linux layer on Windows (WSL). A Mac terminal with a note: "close cousin, not the same". A caution tag on the cloud door: "billed while it exists".]**

**(Voiceover):**
Practice ke liye Linux chahiye, aur teen raaste hain. Ek: cloud ki VM, yaani asli kiraye ki building. Isse AWS ya GCP ke free tier se le sakte ho, par free offers ke rules badalte rehte hain aur building ghante ke hisaab se bill karti hai, isliye lab ke baad band karna ya hatana yaad rakho. Do: laptop par VM, jaise VirtualBox ya UTM, jo bilkul free hai aur internet ke bina bhi chalti hai. Teen: Windows par WSL, jo ek asli Linux ka hissa deta hai. Mac ka terminal Linux ka kareebi rishtedaar hai, par bilkul wahi nahi: kuch commands ke options alag hain. Isliye is course ke labs ke liye ek Ubuntu VM lo. Teeno raaste theek hain, par ek rakhna, aur uska ek snapshot ya notes rakhna, taaki beech mein bigad jaaye to wapas aa sako.

### [12:25 – 14:05] Scene 6: Lab: Pehli Command
**[VISUAL: A terminal. User types `whoami`, `hostname`, `uname -a`, `cat /etc/os-release`. Each output is annotated.]**

**(Voiceover):**
Lab. Terminal kholo, yaani instruction desk par aao. `whoami` batata hai aap kaun ho. `hostname` machine ka naam, yaani is building ka naam. `uname -a` kernel ki jaankari. `cat /etc/os-release` batata hai kaun sa distribution aur version chal raha hai. Phir `ls --help` aur `man ls` kholkar dekho. Ye chaaron commands har naye server par sabse pehle chalte hain, kyunki kisi bhi machine par kaam karne se pehle pata hona chahiye ki aap kahan ho. Screenshot lo aur apni notebook mein output likh lo.

### [14:05 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A mini diagram: You → Shell → Kernel → Hardware. Under it, small: "you → instruction desk → management office → machines".]**

**(Voiceover):**
Recap: Linux cloud ka base hai, kernel yaani management office hardware sambhalta hai, shell yaani instruction desk aapki baat kernel tak le jaata hai, aur distributions alag packaging hain. Aur ab aapke paas command ka dhancha, madad ke teen tareeke, aur ek practice ground bhi hai. Ab is building ka naksha chahiye. Linux ka filesystem Windows se bilkul alag dikhta hai, aur agla episode usi ka naksha hai.

---

# 📺 EPISODE 2: Filesystem ka Naksha

### [00:00 – 01:55] Scene 1: C Drive Kahan Hai?
**[VISUAL: A Windows Explorer with C:, D:. It morphs into a hotel floor plan with one main lobby marked `/`, and every corridor branching from it like an upside-down tree.]**

**(Voiceover):**
Windows mein C drive, D drive hote hain. Linux mein koi drive letter nahi. Atithi ki building ki tarah, yahan ek hi main lobby hai, aur har corridor wahin se shuru hota hai. Us lobby ko `/` kehte hain, root. Har file, har folder, har device, usi se nikalti ek shaakha hai. Is building mein kamra yaani directory, aur kamre ke andar ki almari yaani file. Is naksha ko samajh liya to server par kuch bhi dhoondhna aasaan ho jata hai.

### [01:55 – 04:40] Scene 2: Zaroori Directories ka Tour
**[VISUAL: An animated floor plan. Highlighted in turn: /home (staff quarters), /etc (admin office), /var (logbook room inside), /bin and /usr (tool room), /tmp (lost-and-found), /root (general manager's cabin), /dev (equipment room), /proc (live status board). Each gets a small icon and a one-line description.]**

**(Voiceover):**
Building ka tour karte hain. `/home` staff quarters hain: har user ka apna kamra aur apni files. `/etc` admin office hai, jahan saari rulebooks rakhi hain, yaani configuration files. `/var` mein badalne wala data rehta hai, aur uske andar `/var/log` logbook room hai. `/usr/bin` tool room hai, jahan commands ke programs rakhe hain, aur `/bin` uska shortcut. `/tmp` lost-and-found hai, temporary files ke liye. `/root` general manager ka cabin, yaani root user ka home. `/dev` equipment room, jahan devices ki files hain. `/proc` ek live status board hai, ek virtual jagah jahan kernel running processes ki jaankari dikhata hai. Rule of thumb: kuch kharab ho to logbook room dekho, `/var/log`, aur settings ke liye admin office, `/etc`.

### [04:40 – 06:25] Scene 3: Absolute vs Relative Path, aur Special Symbols
**[VISUAL: A path `/home/asha/projects/app` is drawn from the main lobby. Then relative hops: `.` (here), `..` (parent), `~` (home).]**

**(Voiceover):**
Path do tarah ke hote hain. Absolute path `/` se shuru hota hai, yaani main lobby se poora raasta, jaise `/home/asha/projects`. Relative path wahan se shuru hota hai jahan aap abhi khade ho, jaise `projects/app`. Teen symbols yaad rakho. Ek dot matlab yahin ki directory. Do dots matlab ek level upar. Aur `~` matlab aapka home directory. Aur ek zaroori baat: Linux case-sensitive hai, to `App` aur `app` do alag cheezein hain.

### [06:25 – 09:15] Scene 4: `ls -l` ko Padhna: Type, Size aur Shortcut
**[VISUAL: Output of `ls -l /` with each column labelled: type, permissions, links, owner, group, size, date, name. The first letters highlighted: `-` file, `d` directory, `l` link with the arrow in `bin -> usr/bin`, `c` device. Beside it `ls -lh` and `ls -a` showing a hidden `.bashrc`.]**

**(Voiceover):**
`ls` sirf naam dikhata hai. `ls -l` poori kahani. Har line ka pehla akshar batata hai ki ye kya hai: `-` normal file, `d` directory yaani kamra, `l` link yaani shortcut, `c` device. Phir nau akshar permissions ke, jo agle session mein padhenge. Phir owner aur group, size, tareekh aur naam. `ls -lh` size ko `4.0K` ya `1.2M` jaisa padhne layak banata hai. `ls -a` chhupi files dikhata hai, jinka naam dot se shuru hota hai, jaise `.bashrc`. Ek chhoti hairat: naye distributions mein `ls -l /` par `bin -> usr/bin` dikhta hai. Matlab `/bin` asli kamra nahi, `/usr/bin` ka shortcut hai, aur tir ke baad wahi asli cheez hai. Isliye tool room ek hi hai, bas do darwaze.

### [09:15 – 11:55] Scene 5: Baaki Kamre: /opt, /srv, /mnt aur /boot
**[VISUAL: The floor plan again with four more rooms lit: `/opt` (visiting contractors' equipment), `/srv` (what the building serves to guests), `/mnt` (a temporary door to another hall), `/boot` (the key to the morning opening routine), and `/usr/local` (tools the staff installed themselves).]**

**(Voiceover):**
Floor plan ke kuch aur kamre, jo server par roz milte hain. `/opt` bahari contractors ka saaman: wo software jo distribution ka hissa nahi, jaise koi bada vendor ka package. `/usr/local` mein wo tools jo aapne khud lagaye. `/srv` mein wo data jo building guests ko parosti hai, jaise web ki files. `/mnt` ek asthayi darwaza hai, jisse doosra disk jod kar dekhte hain; Session 5B mein disk ka poora kaam aayega. `/boot` mein kernel aur subah ki opening routine ki files hain, aur usse tab tak mat chhedo jab tak pata na ho. Ye sab ek hi rule ka nateeja hai: har cheez ki ek jagah, taaki naya admin bhi pehchaan le.

### [11:55 – 14:35] Scene 6: Lab: Building mein Ghoomo
**[VISUAL: Terminal: `pwd`, `ls -l /`, `cd /var/log`, `ls`, `cd ~`, `cd ..`, `cd -`.]**

**(Voiceover):**
Lab: `pwd` se current jagah dekho. `ls -l /` se main lobby ke saare darwaze, yaani root ke andar ke folders. `cd /var/log` karo aur `ls` chalao, ye wahi logbook room hai jahan system ke logs milte hain. `cd ~` se home par wapas. `cd ..` se ek level upar, aur `cd -` se pichli jagah par. Ab apne hi haath se `/etc` mein jaakar `ls` chalao. Aapko admin office ki rulebooks dikhengi. Phir `ls -l /` chalao aur `bin -> usr/bin` wali line dhoondho, `ls -la ~` se chhupi files dekho, aur `ls -lh /var/log` mein sabse badi file ka size padho. Dhyaan: abhi kuch badalna nahi hai, sirf dekhna hai.

### [14:35 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A cheat card: "/etc config, /var/log logs, /home users, /tmp temp".]**

**(Voiceover):**
Recap: ek building, ek main lobby, sab kuch `/` se shuru. Config admin office mein, `/etc`, aur logs logbook room mein, `/var/log`. Navigation aa gayi. Ab files banana, copy karna, hatana aur dhoondhna seekhte hain, aur wo bhi safely.

---

# 📺 EPISODE 3: Core Commands

### [00:00 – 01:50] Scene 1: Ek Galti, Poora Server Gaya
**[VISUAL: A terminal with `rm -rf /` typed. A big warning hand appears before Enter. Text: "Commands are sharp tools".]**

**(Voiceover):**
Linux mein delete ka koi recycle bin nahi hota. Isliye ye episode commands sikhaata hai, lekin saath mein safe aadat bhi. Ek rule: jo command aap samjhe nahi, wo kabhi production par mat chalao. Aur `rm -rf` ke saath path hamesha do baar padho. Naye GNU `rm` ne `rm -rf /` ko khud rok diya hai, par `rm -rf ~` ya khaali variable wale path ko nahi rokta.

### [01:50 – 03:50] Scene 2: Banana, Copy, Move, Delete
**[VISUAL: Terminal commands with outcome icons: `mkdir`, `touch`, `cp`, `mv`, `rm`, `rmdir`.]**

**(Voiceover):**
`mkdir` naya kamra banata hai, yaani folder. `touch` ek khaali almari, yaani khaali file. `cp source dest` copy karta hai, folder ke liye `cp -r`. `mv` move karta hai aur rename bhi, kyunki rename bas ek move hai. `rm` file hatata hai, aur `rm -r` folder ko andar ki cheezon ke saath. Safe aadat: pehle `ls` se dekho kya hatane wale ho, aur seekhte waqt `rm -i` ka use karo, jo har delete se pehle poochta hai.

### [03:50 – 06:50] Scene 3: Overwrite ka Jaal: cp aur mv
**[VISUAL: Terminal: `echo new > b`, `cp b a` replacing the contents of `a` without a word. A red box: "no warning, no recycle bin". Then the safe versions: `cp -i`, `mv -i`, `cp --update=none`, and `cp -r` for a folder.]**

**(Voiceover):**
Ek aur chup chaap jaal. `cp b a` agar `a` pehle se hai, to bina poochhe `a` ka purana content mita deta hai. `mv b a` bhi wahi karta hai. Recycle bin nahi, chetavani nahi. Safe aadat: `cp -i` aur `mv -i` har overwrite se pehle poochte hain. Jo file pehle se hai use chhodna ho, to `cp --update=none`, jo naye versions mein purane `-n` ki jagah hai. Aur folder copy karna ho to `cp -r`, nahi to `cp: -r not specified; omitting directory` ka message aata hai. Hamare test mein ye sab Ubuntu 24.04 par yahi nikla. Production par config file badalne se pehle hamesha `cp app.conf app.conf.bak`, jaise abhi lab mein kiya.

### [06:50 – 08:40] Scene 4: Dhoondhna: find aur which
**[VISUAL: Terminal: `find /var/log -name "*.log"`, `find . -type f -mtime -1`, `which python3`, `locate` mention.]**

**(Voiceover):**
Server par file kahan hai? `find` se. `find /var/log -name "*.log"` naam se dhoondhta hai. `find . -type f -mtime -1` pichle ek din mein badli hui files dikhata hai. `which python3` batata hai ki command ka program kis path par hai. Ye teen cheezein roz kaam aati hain, khaaskar jab koi bole ki "kal se kuch toota hai", to pata karo ki kal kaun si file badli.

### [08:40 – 12:10] Scene 5: Wildcard aur Text Editor
**[VISUAL: Terminal: `ls *.log`, `ls app?.conf`, `rm -i *.bak` with the matched files highlighted, and `"My Notes.txt"` in quotes. Then `nano app.conf` with its shortcut bar at the bottom (Ctrl+O save, Ctrl+X exit), and a small vim card: `i` insert, `Esc`, `:wq`, `:q!`.]**

**(Voiceover):**
Ek ek naam likhne ki jagah pattern. `*` matlab kuch bhi, `?` matlab ek akshar. `ls *.log` saari log files, `rm -i *.bak` saari backup files, har ek se poochkar. Dhyaan: wildcard ko shell kholta hai, command nahi, isliye `rm *` par do baar sochna. Jis naam mein space ho, use quotes mein likho: `"My Notes.txt"`. Ab file ke andar badalna. Sabse aasaan `nano app.conf`: likho, `Ctrl+O` se save, `Ctrl+X` se bahar, aur neeche shortcut ki line hamesha dikhti rehti hai. Kabhi kisi server par sirf `vi` ya `vim` mile, to teen cheezein. `i` dabao to likh sakte ho. `Esc` dabao to likhna band. Phir `:wq` Enter se save aur bahar, ya `:q!` se bina save kiye bahar. Ye aakhri wala wahi hai jo har naya student ek baar zaroor dhoondhta hai.

### [12:10 – 14:35] Scene 6: Lab: Ek Mini Project Folder
**[VISUAL: Terminal builds `demo/{src,logs,config}`, creates files, copies one, renames one, and lists with `ls -R`.]**

**(Voiceover):**
Lab. `mkdir -p demo/{src,logs,config}` ek hi command mein teen folders banata hai. `touch demo/src/app.py demo/config/app.conf` files banao. `cp demo/config/app.conf demo/config/app.conf.bak` se backup. `mv demo/src/app.py demo/src/main.py` se rename. `ls -R demo` se poora tree dekho. Phir `echo new > b`, `cp b a`, `cat a` se overwrite ka jaal khud dekho, aur `cp -i` se wahi dobara. Ab `ls *.conf*` se dono config files ek saath dekho, aur `nano demo/config/app.conf` mein ek line likhkar save karo. Aakhir mein `rm -r demo` se saaf karo, aur dhyaan se padho kya hata rahe ho.

### [14:35 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A cheat sheet card of the commands used.]**

**(Voiceover):**
Recap: mkdir, touch, cp, mv, rm, find, which, wildcard aur nano. Overwrite ka jaal yaad rakho. Ab ye files ke andar kya hai wo padhna aur filter karna seekhte hain. Agle episode mein pipes ka jaadu hai.

---

# 📺 EPISODE 4: Text ka Jaadu aur Apni Linux VM

### [00:00 – 02:15] Scene 1: Log File mein Ek Line Dhoondho
**[VISUAL: The logbook room, shelves full of registers. One register opens into a 100,000-line log file. A search beam moves down and highlights a single `ERROR` line.]**

**(Voiceover):**
Atithi ki booking site har guest ki request logbook mein likhti hai, aur jab rooms page dheemi chalti hai, to pehla sawaal wahi hota hai ki logbook mein kya likha hai. Building ke logbook room mein ek lakh lines ki log file hai, aur usme ek error ki line dhoondhni hai. Notepad mein khol ke scroll karoge? Linux ne text ko ek power tool bana diya hai. Aaj hum seekhenge `cat`, `less`, `head`, `tail`, `grep`, aur sabse zaroori idea: pipe.

### [02:15 – 04:00] Scene 2: Padhne ke Tools
**[VISUAL: Terminal: `cat file`, `less file`, `head -n 5 file`, `tail -n 5 file`, `tail -f app.log` with live lines streaming.]**

**(Voiceover):**
`cat` poori file print karta hai. Badi files ke liye `less`, jisme upar neeche scroll karke `q` se bahar nikalte hain. `head -n 5` shuru ki paanch lines, `tail -n 5` aakhri paanch. Aur sabse popular, `tail -f app.log`: file ke ant mein jo nayi lines judti hain wo live dikhata hai. Deploy ke waqt isse logs dekhna DevOps ki roz ki aadat hai.

### [04:00 – 05:55] Scene 3: grep aur Pipe
**[VISUAL: A pipe diagram: `cat app.log` → `grep ERROR` → `sort` → `uniq -c`. Counts appear on the right.]**

**(Voiceover):**
`grep ERROR app.log` sirf wo lines dikhata hai jisme ERROR hai. `grep -i` case ignore karta hai, `grep -v` ulta, `grep -n` line number ke saath. Ab pipe: `|`, jo ek command ka output doosri command ka input bana deta hai. `grep ERROR app.log | sort | uniq -c` batata hai ki kaun si error kitni baar aayi. Chhoti commands ko jod kar bada kaam, yahi Linux ka philosophy hai.

### [05:55 – 09:15] Scene 4: Redirect aur Ginti ke Chhote Tools
**[VISUAL: Arrows from a command to a file: `>` writes and replaces, `>>` adds at the end, `2>` catches errors. A small toolbox: `wc -l`, `sort -n`, `cut -d, -f2`, `uniq -c`, `grep -c`. A one-line report: `grep ERROR app.log > errors.txt` then `wc -l errors.txt`.]**

**(Voiceover):**
Output sirf screen par kyun? `>` output ko file mein likhta hai, par purani file mita kar. `>>` file ke ant mein jodta hai. `grep ERROR app.log > errors.txt`. Errors ke liye alag raasta hai, `2>`, jaise `ls /nonexistent 2> err.txt`. Ab chhote tools jo pipe mein kaam aate hain. `wc -l` lines gintata hai. `sort -n` numbers ko sahi kram mein lagata hai. `cut -d, -f2` comma wali file ka doosra column nikalta hai. `uniq -c` gintata hai, par sirf paas paas ki repeat lines, isliye pehle `sort`. `grep -c ERROR app.log` seedha ginti deta hai. Badi file par chalane se pehle ek chhota sample banao aur socho ki kitna output aana chahiye. Phir asli file par chalao.

### [09:15 – 12:50] Scene 5: Lab: Apni Linux VM aur Log Analysis
**[VISUAL: A split screen: cloud VM console on left (a Linux VM launched), terminal SSH session on right, with a small inset of a staff entrance door opening. A log file is created with `printf` and analysed.]**

**(Voiceover):**
Lab. Ek Linux VM lo, VirtualBox ya cloud ki free-tier, yaani apni pehli building. Uspar SSH karo. SSH is building ka staff entrance hai: staff isi darwaze se andar aata hai. Pehli baar Linux poochega ki is machine ki pehchaan par bharosa hai ya nahi, aur `yes` likhne par wo use yaad rakh leta hai. Chaabiyon ka poora kaam agle session mein hai. Ek sample log banao: `printf "INFO start\nERROR db timeout\nERROR db timeout\nWARN slow\n" > app.log`. Ab `grep ERROR app.log | sort | uniq -c` chalao, aur dekho ki "db timeout" do baar aaya hai. Phir `grep ERROR app.log > errors.txt` aur `wc -l errors.txt` se dekho ki do lines hain. Ye ek mini incident investigation hai, jo asli servers par bhi bilkul isi tarah hoti hai.

### [12:50 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "cat · less · head · tail · grep · | · sort · uniq".]**

**(Voiceover):**
Recap: padhna, filter karna, pipe se jodna, aur redirect se report file banana. Aapke paas ab Linux ki neev hai: building ka naksha, navigation aur text tools. Agle session mein is building mein staff rakhenge aur kamron par taale lagayenge: users, permissions aur SSH keys, yaani server ko safe kaise rakhte hain.


---

# 📎 Student handout: Session 03 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Prompt | `user@host:~$`; `$` normal user, `#` root |
| Command ka dhancha | command, option, argument: `ls -l /etc` |
| Madad | `--help`, `man NAME` (`q` se bahar), Tab, upar arrow, `history`, Ctrl+R, Ctrl+C |
| Raaste | `/` root, `~` home, `.` yahin, `..` upar; Linux case-sensitive |
| Kahan kya | `/etc` config, `/var/log` logs, `/home` users, `/tmp` temporary, `/usr/bin` programs, `/proc` live status |
| `ls -l` | Pehla akshar: `-` file, `d` directory, `l` link, `c` device; `-h` size, `-a` chhupi files |
| Banana, hatana | `mkdir -p`, `touch`, `cp -r`, `mv`, `rm -i`, `rm -r` savdhani se; `cp` aur `mv` bina poochhe overwrite karte hain, `-i` lagao |
| Dhoondhna | `find PATH -name "*.log"`, `find . -type f -mtime -1`, `which CMD` |
| Wildcard | `*` kuch bhi, `?` ek akshar; space wale naam quotes mein |
| Editor | `nano FILE` (Ctrl+O, Ctrl+X); `vi`: `i`, `Esc`, `:wq`, `:q!` |
| Padhna | `cat`, `less`, `head -n`, `tail -n`, `tail -f` |
| Filter | `grep` (`-i -v -n -c`), `|`, `sort`, `uniq -c`, `wc -l`, `cut -d, -f2` |
| Redirect | `>` likhta (purani file mita kar), `>>` jodta, `2>` errors |
| Pehli commands | `whoami`, `hostname`, `uname -a`, `cat /etc/os-release` |

# ✍️ 02: SCRIPT — SESSION-03: Linux Foundations
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S03`
- **Focus:** Why Linux, architecture (kernel/shell), filesystem hierarchy, core commands, files/text tools, getting a Linux VM
- **Episodes:**
  - Episode 1: Linux kyun? Kernel, Shell aur Distributions
  - Episode 2: Filesystem ka Naksha: / se shuru
  - Episode 3: Core Commands: navigate, create, copy, search
  - Episode 4: Text ka Jaadu: cat, grep, pipes aur apni Linux VM

---

# 📺 EPISODE 1: Linux kyun?

### [00:00 – 01:15] Scene 1: Har Server ka Ek Hi Raaz
**[VISUAL: A world map of data centers. Zoom into a rack, then a boot screen showing a penguin logo. Text: "Most of the cloud runs on this".]**

**(Voiceover):**
AWS ke servers, Google ke servers, Kubernetes ke nodes, Docker ke containers: inke andar zyadatar ek hi cheez chal rahi hai, Linux. Agar aap DevOps seekhna chahte ho, to Linux seekhna optional nahi hai. Achhi baat ye hai ki Linux ko rat ke nahi, samajh ke seekhna hai. Is session ke baad aap kisi bhi Linux server mein jaakar ghabraoge nahi.

### [01:15 – 04:30] Scene 2: Kernel aur Shell: Restaurant Analogy
**[VISUAL: A restaurant: Customer (you) → Waiter (shell) → Kitchen manager (kernel) → Stove, fridge (hardware). Arrows labelled with commands.]**

**(Voiceover):**
Restaurant socho. Aap customer ho, waiter shell hai, aur kitchen manager kernel hai, jiske haath mein stove aur fridge, yaani hardware hai. Aap waiter ko order dete ho, jaise `ls`. Waiter kitchen manager ko request bhejta hai, aur kernel hardware se kaam karwa kar jawab wapas karta hai. Kernel Linux ka dil hai: memory, CPU, disk aur process, sab wahi sambhalta hai. Shell wo program hai jo aapki commands ko kernel tak pahunchata hai, jaise Bash.

### [04:30 – 08:00] Scene 3: Distributions aur Open Source
**[VISUAL: A family tree: Linux kernel → Debian → Ubuntu; Red Hat → RHEL/Rocky/CentOS-Stream/Fedora; Alpine; Amazon Linux.]**

**(Voiceover):**
Linux sirf kernel hai. Uske saath tools aur package manager jod kar jo poora system banta hai, use distribution kehte hain. Debian family mein Ubuntu hai, jo apt use karta hai. Red Hat family mein RHEL aur Rocky jaise distros hain, jo dnf ya yum use karte hain. Alpine bahut chhota hota hai aur containers mein aam hai. Amazon Linux AWS ke liye bana hai. Concept sab mein ek jaise hain; fark mostly package manager aur kuch paths ka hota hai. Ye sab open source hai, to koi bhi code padh sakta hai.

### [08:00 – 11:30] Scene 4: Lab: Pehli Command
**[VISUAL: A terminal. User types `whoami`, `hostname`, `uname -a`, `cat /etc/os-release`. Each output is annotated.]**

**(Voiceover):**
Lab. Terminal kholo. `whoami` batata hai aap kaun ho. `hostname` machine ka naam. `uname -a` kernel ki jaankari. `cat /etc/os-release` batata hai kaun sa distribution aur version chal raha hai. Ye chaaron commands har naye server par sabse pehle chalte hain, kyunki kisi bhi machine par kaam karne se pehle pata hona chahiye ki aap kahan ho. Screenshot lo aur apni notebook mein output likh lo.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A mini diagram: You → Shell → Kernel → Hardware.]**

**(Voiceover):**
Recap: Linux cloud ka base hai, kernel hardware sambhalta hai, shell aapki baat kernel tak le jaata hai, aur distributions alag packaging hain. Ab ek naksha chahiye. Linux ka filesystem Windows se bilkul alag dikhta hai, aur agla episode usi ka naksha hai.

---

# 📺 EPISODE 2: Filesystem ka Naksha

### [00:00 – 01:15] Scene 1: C Drive Kahan Hai?
**[VISUAL: A Windows Explorer with C:, D:. It morphs into a single upside-down tree with `/` at the top.]**

**(Voiceover):**
Windows mein C drive, D drive hote hain. Linux mein koi drive letter nahi. Sab kuch ek hi tree mein hai, jiski jad ko `/` kehte hain, root. Har file, har folder, har device, us tree ki ek shaakha hai. Is naksha ko samajh liya to server par kuch bhi dhoondhna aasaan ho jata hai.

### [01:15 – 05:30] Scene 2: Zaroori Directories ka Tour
**[VISUAL: An animated tree. Highlighted in turn: /home, /etc, /var, /bin, /usr, /tmp, /root, /dev, /proc. Each gets a small icon and a one-line description.]**

**(Voiceover):**
`/home` mein users ki apni files. `/etc` mein configuration files, isse "settings ki almari" samjho. `/var` mein badalne wala data, jaise logs, `/var/log` mein. `/bin` aur `/usr/bin` mein commands ke programs. `/tmp` temporary files ke liye. `/root` root user ka home. `/dev` mein devices ki files. `/proc` ek virtual jagah hai jahan kernel running processes ki jaankari dikhata hai. Rule of thumb: kuch kharab ho to logs `/var/log` mein dekho, aur config `/etc` mein.

### [05:30 – 08:30] Scene 3: Absolute vs Relative Path, aur Special Symbols
**[VISUAL: A path `/home/asha/projects/app` is drawn from root. Then relative hops: `.` (here), `..` (parent), `~` (home).]**

**(Voiceover):**
Path do tarah ke hote hain. Absolute path `/` se shuru hota hai, jaise `/home/asha/projects`. Relative path aapki current location se, jaise `projects/app`. Teen symbols yaad rakho. Ek dot matlab yahin ki directory. Do dots matlab ek level upar. Aur `~` matlab aapka home directory. Aur ek zaroori baat: Linux case-sensitive hai, to `App` aur `app` do alag cheezein hain.

### [08:30 – 11:30] Scene 4: Lab: Tree mein Ghoomo
**[VISUAL: Terminal: `pwd`, `ls -l /`, `cd /var/log`, `ls`, `cd ~`, `cd ..`, `cd -`.]**

**(Voiceover):**
Lab: `pwd` se current jagah dekho. `ls -l /` se root ke andar ke folders. `cd /var/log` karo aur `ls` chalao, ye wahi jagah hai jahan system ke logs milte hain. `cd ~` se home par wapas. `cd ..` se ek level upar, aur `cd -` se pichli jagah par. Ab apne hi haath se `/etc` mein jaakar `ls` chalao. Aapko system ki settings ki almari dikhegi. Dhyaan: abhi kuch badalna nahi hai, sirf dekhna hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A cheat card: "/etc config, /var/log logs, /home users, /tmp temp".]**

**(Voiceover):**
Recap: ek tree, root se shuru, config `/etc` mein, logs `/var/log` mein. Navigation aa gayi. Ab files banana, copy karna, hatana aur dhoondhna seekhte hain, aur wo bhi safely.

---

# 📺 EPISODE 3: Core Commands

### [00:00 – 01:15] Scene 1: Ek Galti, Poora Server Gaya
**[VISUAL: A terminal with `rm -rf /` typed. A big warning hand appears before Enter. Text: "Commands are sharp tools".]**

**(Voiceover):**
Linux mein delete ka koi recycle bin nahi hota. Isliye ye episode commands sikhaata hai, lekin saath mein safe aadat bhi. Ek rule: jo command aap samjhe nahi, wo kabhi production par mat chalao. Aur `rm -rf` ke saath path hamesha do baar padho.

### [01:15 – 05:00] Scene 2: Banana, Copy, Move, Delete
**[VISUAL: Terminal commands with outcome icons: `mkdir`, `touch`, `cp`, `mv`, `rm`, `rmdir`.]**

**(Voiceover):**
`mkdir` folder banata hai, `touch` khaali file. `cp source dest` copy karta hai, folder ke liye `cp -r`. `mv` move karta hai aur rename bhi, kyunki rename bas ek move hai. `rm` file hatata hai, aur `rm -r` folder ko andar ki cheezon ke saath. Safe aadat: pehle `ls` se dekho kya hatane wale ho, aur seekhte waqt `rm -i` ka use karo, jo har delete se pehle poochta hai.

### [05:00 – 08:30] Scene 3: Dhoondhna: find aur which
**[VISUAL: Terminal: `find /var/log -name "*.log"`, `find . -type f -mtime -1`, `which python3`, `locate` mention.]**

**(Voiceover):**
Server par file kahan hai? `find` se. `find /var/log -name "*.log"` naam se dhoondhta hai. `find . -type f -mtime -1` pichle ek din mein badli hui files dikhata hai. `which python3` batata hai ki command ka program kis path par hai. Ye teen cheezein roz kaam aati hain, khaaskar jab koi bole ki "kal se kuch toota hai", to pata karo ki kal kaun si file badli.

### [08:30 – 11:30] Scene 4: Lab: Ek Mini Project Folder
**[VISUAL: Terminal builds `demo/{src,logs,config}`, creates files, copies one, renames one, and lists with `ls -R`.]**

**(Voiceover):**
Lab. `mkdir -p demo/{src,logs,config}` ek hi command mein teen folders banata hai. `touch demo/src/app.py demo/config/app.conf` files banao. `cp demo/config/app.conf demo/config/app.conf.bak` se backup. `mv demo/src/app.py demo/src/main.py` se rename. `ls -R demo` se poora tree dekho. Aakhir mein `rm -r demo` se saaf karo, aur dhyaan se padho kya hata rahe ho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A cheat sheet card of the commands used.]**

**(Voiceover):**
Recap: mkdir, touch, cp, mv, rm, find, which. Ab ye files ke andar kya hai wo padhna aur filter karna seekhte hain. Agle episode mein pipes ka jaadu hai.

---

# 📺 EPISODE 4: Text ka Jaadu aur Apni Linux VM

### [00:00 – 01:15] Scene 1: Log File mein Ek Line Dhoondho
**[VISUAL: A 100,000-line log file. A search beam moves down and highlights a single `ERROR` line.]**

**(Voiceover):**
Ek lakh lines ki log file mein ek error ki line dhoondhni hai. Notepad mein khol ke scroll karoge? Linux ne text ko ek power tool bana diya hai. Aaj hum seekhenge `cat`, `less`, `head`, `tail`, `grep`, aur sabse zaroori idea: pipe.

### [01:15 – 05:00] Scene 2: Padhne ke Tools
**[VISUAL: Terminal: `cat file`, `less file`, `head -n 5 file`, `tail -n 5 file`, `tail -f app.log` with live lines streaming.]**

**(Voiceover):**
`cat` poori file print karta hai. Badi files ke liye `less`, jisme upar neeche scroll karke `q` se bahar nikalte hain. `head -n 5` shuru ki paanch lines, `tail -n 5` aakhri paanch. Aur sabse popular, `tail -f app.log`: file ke ant mein jo nayi lines judti hain wo live dikhata hai. Deploy ke waqt isse logs dekhna DevOps ki roz ki aadat hai.

### [05:00 – 08:30] Scene 3: grep aur Pipe
**[VISUAL: A pipe diagram: `cat app.log` → `grep ERROR` → `sort` → `uniq -c`. Counts appear on the right.]**

**(Voiceover):**
`grep ERROR app.log` sirf wo lines dikhata hai jisme ERROR hai. `grep -i` case ignore karta hai, `grep -v` ulta, `grep -n` line number ke saath. Ab pipe: `|`, jo ek command ka output doosri command ka input bana deta hai. `grep ERROR app.log | sort | uniq -c` batata hai ki kaun si error kitni baar aayi. Chhoti commands ko jod kar bada kaam, yahi Linux ka philosophy hai.

### [08:30 – 11:30] Scene 4: Lab: Apni Linux VM aur Log Analysis
**[VISUAL: A split screen: cloud VM console on left (a Linux VM launched), terminal SSH session on right. A log file is created with `printf` and analysed.]**

**(Voiceover):**
Lab. Ek Linux VM lo, VirtualBox ya cloud ki free-tier, aur uspar SSH karo. Ek sample log banao: `printf "INFO start\nERROR db timeout\nERROR db timeout\nWARN slow\n" > app.log`. Ab `grep ERROR app.log | sort | uniq -c` chalao, aur dekho ki "db timeout" do baar aaya hai. Ye ek mini incident investigation hai, jo asli servers par bhi bilkul isi tarah hoti hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "cat · less · head · tail · grep · | · sort · uniq".]**

**(Voiceover):**
Recap: padhna, filter karna, pipe se jodna. Aapke paas ab Linux ki neev hai: filesystem, navigation aur text tools. Agle session mein hum seekhenge users, permissions aur SSH keys, yaani server ko safe kaise rakhte hain.

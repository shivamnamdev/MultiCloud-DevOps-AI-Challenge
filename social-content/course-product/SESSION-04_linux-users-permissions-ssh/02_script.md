# ✍️ 02: SCRIPT — SESSION-04: Linux Users, Permissions & SSH
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S04`
- **Focus:** User types and UIDs, `useradd` options, primary and secondary groups, sudo and sudoers, password policy (`chage`), file permissions (chmod/chown), umask, SUID/SGID/sticky bit, SSH keys, package managers, boot process and targets
- **Author's notes woven in:** `Linux-Handwritten-Notes.md` sections 1 to 6 and 16 (map: `NOTES_INTEGRATION_MAP_LINUX_K8S.md`)
- **Distribution:** Ubuntu is the main line; the Red Hat family equivalent is named once where it differs
- **Story position:** Zoom level 1, inside one building. Atithi Hotels staff rakhta hai aur kamron par taale lagata hai.
- **Story words used:** staff (users), general manager (root), duty manager (sudo user), staff register (`/etc/passwd`), tijori (`/etc/shadow`), home department aur extra department cards (primary aur secondary groups), ID card ki expiry (password policy), teen-ring taala (permissions), default taala (umask), owner ki power wali machine (SUID), department ka kamra (SGID), lost-and-found (sticky bit), staff entrance (SSH), purchase department (package manager), opening routine (boot), shift supervisor (systemd)
- **Episodes:**
  - Episode 1: Users, Groups aur sudo: Staff, Departments, ID Card ki Expiry aur Master Key
  - Episode 2: File Permissions: Teen-Ring Taala, Default Taala aur Teen Khaas Nishaan
  - Episode 3: SSH Keys: Staff Entrance ki Apni Chaabi
  - Episode 4: Packages aur Boot Process: Purchase Department aur Subah ka Opening Routine

---

# 📺 EPISODE 1: Users, Groups aur sudo

### [00:00 – 01:15] Scene 1: Sabke Paas Master Key Ho To?
**[VISUAL: The Atithi Hotels building. Ten staff members, each holding the same master key. One of them empties the records room by mistake. Cut to a shared server: 10 developers logged in as "root", one deletes a config folder, every terminal flashes red.]**

**(Voiceover):**
Pichhle session mein Atithi Hotels ko apni pehli building mili thi. Ab socho is building mein dus staff hain, aur sabke paas master key hai. Ek ne galti se records room khaali kar diya. Ab pata nahi kisne kiya, aur rok bhi koi nahi sakta tha. Server par bilkul yahi hota hai jab dus developers root se login karte hain aur ek galti se zaroori folder hata deta hai. Linux ka user system isi problem ke liye hai: har staff ki apni pehchaan, aur utni hi power jitni kaam ke liye zaroori hai. Is session mein hum building mein staff rakhenge aur kamron par taale lagayenge. Is episode mein: users, groups aur sudo.

### [01:15 – 04:15] Scene 2: Chaar Tarah ka Staff, UID aur Staff Register
**[VISUAL: Inside the building. Four ID cards in a row: "root, UID 0", "local user, UID 1000+", "system user, no login", "sudo user". The general manager (root) holds the master key. On the desk: a staff register labelled `/etc/passwd` with one line split into seven boxes (`asha : x : 1001 : 1001 : Asha Verma : /home/asha : /bin/bash`), and a locked safe labelled `/etc/shadow`. Guests walk through the lobby with no ID card.]**

**(Voiceover):**
Pehle ek rule yaad rakho: Linux ke users hotel ka staff hain, guests nahi. Guest yaani website ka end user, aur use kabhi staff ID card nahi milta. Staff chaar tarah ka hota hai. Root is building ka general manager hai, jiske paas master key hai. Uska UID, yaani ID card ka number, 0 hota hai, aur wo kuch bhi kar sakta hai. Local user aam staff hai, jise root ne rakha hai: uska apna quarter, yaani home directory, aur limited rights. Inke UID aam taur par 1000 se shuru hote hain. System user insaan hota hi nahi. Wo ek hi kaam wala service staff hai, jaise web server ka user, aur wo login nahi karta. Aur sudo user wo local user hai jise zaroorat par master key udhaar milti hai. Isiliye rule ye hai: roz ka kaam normal user se, aur zaroorat padne par hi power uthao. Staff ki jaankari staff register mein hoti hai, yaani `/etc/passwd`. Uski har line mein saat khaane hote hain: naam, password ki jagah ek `x`, UID, group ka ID, ek comment, home directory aur default shell. Wo `x` batata hai ki password yahan nahi hai. Uska hash ek band tijori mein rehta hai, yaani `/etc/shadow`, jise aam staff padh nahi sakta.

### [04:15 – 07:30] Scene 3: Naya Staff, Home Department aur Extra Cards
**[VISUAL: A new staff member "asha" gets an ID card and a quarter. Her card shows one "home department" stamp and a slot for extra department cards; a card marked "devs" slides in. Terminal: `sudo useradd -m -s /bin/bash -c "Asha Verma" asha`, `tail -1 /etc/passwd`, `sudo passwd asha`, `sudo groupadd devs`, `sudo usermod -aG devs asha`, `id asha`, `sudo gpasswd -d asha devs`.]**

**(Voiceover):**
Naya staff rakhte hain. `sudo useradd -m -s /bin/bash asha` ek naya user banata hai. `-m` uska quarter yaani home directory banata hai, aur `-s` uska shell tay karta hai. Do aur options kaam ke hain: `-u` se UID aap khud dete ho, aur `-c` se comment, jaise poora naam. UID na do to Linux pichhle user ke baad wala number de deta hai. `tail -1 /etc/passwd` se register ki aakhri line dekho, asha wahin milegi. `sudo passwd asha` password set karta hai. Ab departments. Group ek department ki tarah hota hai. Har staff ka ek home department hota hai, yaani primary group, aur ye sirf ek ho sakta hai. Uske upar kitne bhi extra department cards mil sakte hain, yaani secondary groups. `useradd` mein chhota `-g` primary group deta hai aur bada `-G` secondary. `sudo groupadd devs` department banata hai, aur `sudo usermod -aG devs asha` asha ko us department ka card deta hai. Yahan `-a` ka matlab append hai, aur use bhoolna khatarnaak hai, kyunki tab asha ke baaki department cards chhin jaate hain, yaani baaki secondary groups hat jaate hain. Card wapas lena ho to `sudo gpasswd -d asha devs`. `id asha` batata hai ki user kis kis group mein hai.

### [07:30 – 10:00] Scene 4: ID Card ki Expiry: Password Policy
**[VISUAL: An ID card with an expiry date and a small "renew before" stamp. A timeline: last change → expiry → inactive period ends → account locked. Terminal: `sudo chage -l asha`, `sudo chage -M 90 -m 1 -W 7 asha`. Then a second staff member "ravi": `sudo usermod -L ravi`, `sudo usermod -U ravi`, `sudo userdel -r ravi`.]**

**(Voiceover):**
Atithi mein ID card hamesha ke liye nahi banta. Uski expiry hoti hai aur renewal ke rules hote hain. Linux mein yahi password policy hai. `sudo chage -l asha` asha ki policy dikhata hai. `sudo chage -M 90 asha` ka matlab: nabbe din mein password badalna hi hoga. Chhota `-m` do badlaav ke beech kam se kam din tay karta hai, aur `-W` batata hai expiry se kitne din pehle warning shuru ho. Naye users ke liye default numbers `/etc/login.defs` file mein likhe hote hain. Ek shabd aur: inactive period. Password expire hone ke baad itne din tak user purane password se login karke naya bana sakta hai. Uske baad account band, aur admin ko beech mein aana padta hai. Ab maan lo ravi naam ka staff lambi chhutti par hai. `sudo usermod -L ravi` uska password lock karta hai, aur `-U` kholta hai. Tijori mein lock hua password ek `!` se shuru hota hai. Dhyaan rahe, ye sirf password ko rokta hai. SSH key se login tab bhi chal sakta hai. Aur jab staff company chhod de, `sudo userdel -r ravi` user ko hata deta hai, aur `-r` uska quarter bhi khaali kar deta hai.

### [10:00 – 13:15] Scene 5: Lab: sudo ka Sahi Use
**[VISUAL: A duty manager signs a register, borrows the master key, returns it. Terminal: user "asha" runs `apt update` and gets "Permission denied", then `sudo apt update` works. `visudo` shown with a caution sign and three sample lines: `asha ALL=(ALL) ALL`, `asha ALL=(ALL) /usr/bin/systemctl`, `%devs ALL=(ALL) ALL`.]**

**(Voiceover):**
Hotel mein duty manager general manager nahi hota. Par zaroorat padne par wo master key udhaar le sakta hai, aur har baar register mein entry hoti hai. Linux mein yahi sudo hai. Lab: asha ko `sudo` group mein jodo, Ubuntu par `sudo usermod -aG sudo asha`. Red Hat family mein isi group ka naam `wheel` hota hai. Ab asha ke naam se login karo, `su - asha` se. Bina sudo ke `apt update` chalao, error milegi. Phir `sudo apt update` chalao, kaam karega. Sudo aapka password maangta hai aur har command ka log rakhta hai, isliye ye root login se behtar hai: pata rehta hai kisne kya kiya. Aur sudo rules badalne ho to seedha file mat kholo, `sudo visudo` use karo, kyunki wo syntax check karta hai aur aapko lock hone se bachata hai. Us file ki ek line aisi dikhti hai: `asha ALL=(ALL) ALL`, yaani asha har command chala sakti hai. Aakhri `ALL` ki jagah ek command ka poora path likho to sirf wahi command milti hai. Aur naam se pehle `%` lagao to rule poore group par lagta hai.

### [13:15 – 14:30] Scene 6: Recap aur Bridge
**[VISUAL: A card: "Normal user for daily work · sudo for power · one primary group, many secondary · chage for password rules". Under it, small: "staff · duty manager · departments · ID card expiry".]**

**(Voiceover):**
Recap: aam staff yaani normal user, general manager yaani root, home department aur extra cards yaani primary aur secondary groups, ID card ki expiry yaani password policy, aur duty manager ki udhaar wali master key yaani sudo. Ab sawaal: kis staff ko kis kamre mein kya karne diya jaye, ye kaun tay karta hai? Wo hain kamron ke taale, yaani file permissions, agle episode mein.

---

# 📺 EPISODE 2: File Permissions

### [00:00 – 01:15] Scene 1: Ek Taala, Teen Ring
**[VISUAL: A hotel room door with a lock that has three rings labelled Owner, Department, Everyone. Each ring has three settings: r, w, x. The door fades into a file icon with the same three rings.]**

**(Voiceover):**
Atithi ki building mein har kamre aur har almari par ek teen-ring taala laga hai. Kamra yaani directory, almari yaani file. Pehli ring owner ke liye hai, jisne file banayi. Doosri ring uske department ke liye, yaani group. Teesri ring baaki sab staff ke liye, yaani others. Aur har ring par teen haq hote hain: dekhna yaani read, badalna yaani write, aur chalana yaani execute. Ye 3 gune 3 ka hisaab hi Linux permissions ka poora khel hai.

### [01:15 – 05:00] Scene 2: `ls -l` Padhna aur Octal Numbers
**[VISUAL: `-rwxr-xr--  1 asha devs  120 app.sh` with segments highlighted as three rings. Under it: r=4, w=2, x=1, and sums 7, 5, 4.]**

**(Voiceover):**
`ls -l` ki pehli column dekho: `-rwxr-xr--`. Pehla akshar file ka type hai, phir teen teen ke group, yaani hamari teen rings: owner `rwx`, group `r-x`, others `r--`. Number se bhi likha jaa sakta hai: read ka 4, write ka 2, execute ka 1. To `rwx` yaani 7, `r-x` yaani 5, `r--` yaani 4. Is file ki permission 754 hai. Aur ek baat yaad rakhna: kamre par, yaani directory par, `x` ka matlab hota hai us kamre ke andar ja sakna.

### [05:00 – 08:30] Scene 3: chmod aur chown
**[VISUAL: A hand turning the rings on a lock, then a nameplate on a door being changed. Terminal: `chmod 640 secret.txt`, `chmod u+x deploy.sh`, `sudo chown asha:devs app.log`, `ls -l` shows before/after.]**

**(Voiceover):**
Taale ki rings ghumane ke liye `chmod`. Number se: `chmod 640 secret.txt` owner ko read-write, group ko read, others ko kuch nahi. Symbolic tareeke se: `chmod u+x deploy.sh` owner ko execute deta hai, aur minus se haq wapas liya jaata hai. Barabar ka nishaan, jaise `chmod g=rx deploy.sh`, purani setting mita kar nayi likhta hai, aur `a` ka matlab teeno rings ek saath. Kamre ki nameplate badalne ke liye, yaani owner badalne ke liye, `chown`: `sudo chown asha:devs app.log` owner asha aur group devs kar deta hai. Aur ek khatarnaak aadat: `chmod 777` kabhi mat lagao. Ye taala hata kar darwaza khula chhod dene jaisa hai, sab ko sab kuch mil jaata hai, aur security audits mein pehli galti yahi pakdi jaati hai.

### [08:30 – 11:45] Scene 4: Default Taala aur Teen Khaas Nishaan
**[VISUAL: A new room appears with its lock already set. Terminal: `umask` → `0022`; a small sum: directory 777 − 022 = 755, file 666 − 022 = 644. Then three lines highlighted one by one: `-rwsr-xr-x root root /usr/bin/passwd` (the `s` glows), `drwxrwsr-x root devs /srv/devs` (the group `s` glows), `drwxrwxrwt root root /tmp` (the `t` glows). Small icons: a machine with the owner's badge, a department room, a lost-and-found shelf.]**

**(Voiceover):**
Naya kamra bante hi uspar taala kis setting mein lagta hai? Ye `umask` tay karta hai, yaani default taala. `umask` chalao: root par 0022 dikhega, aam user par 0002 ya 0022. umask wo haq hain jo hata diye jaate hain. Directory 777 se shuru hoti hai, 022 hatao to 755. File 666 se shuru hoti hai, kyunki nayi file ko execute apne aap kabhi nahi milta, to 644 banta hai. Ab teen khaas nishaan, jo `ls -l` mein kabhi kabhi `x` ki jagah dikhte hain. Pehla SUID, owner ki ring mein chhota `s`. Ye ek aisi machine hai jo chalane wale ko us ek kaam ke liye owner ki power de deti hai. `ls -l /usr/bin/passwd` dekho. Password badalne par tijori, yaani `/etc/shadow`, badalti hai, jise sirf root likh sakta hai. `passwd` par SUID hai, isliye aam staff bhi apna password badal paata hai. Doosra SGID, group ki ring mein `s`. Directory par lage to uske andar bani har nayi file us directory ke group ki ho jaati hai, yaani department ke kamre mein rakha saaman department ka. Team ke shared folder par `chmod g+s` isi kaam aata hai. Teesra sticky bit, others ki ring mein `t`. `ls -ld /tmp` dekho. `/tmp` building ka lost-and-found hai: koi bhi saaman rakh sakta hai, par hata sirf wahi sakta hai jiska wo saaman hai.

### [11:45 – 14:30] Scene 5: Lab: Script Chalao aur Secret Chhupao
**[VISUAL: Terminal: create `hello.sh`, run `./hello.sh` → "Permission denied", `chmod u+x hello.sh` → runs. Then a `secret.txt` with 600; another user tries `cat` and is denied. Last: `umask`, `touch naya.txt`, `mkdir naya-kamra`, `ls -l`.]**

**(Voiceover):**
Lab. `echo 'echo hello devops' > hello.sh` se script banao, `./hello.sh` chalao, "Permission denied" aayega kyunki execute ka haq nahi hai. `chmod u+x hello.sh` ke baad chalega. Ab ek `secret.txt` banao, `chmod 600 secret.txt` lagao, yaani sirf owner ki ring khuli hai, aur doosre user se `cat` karke dekho, access nahi milega. Aakhir mein `umask` chalao, ek nayi file aur ek naya folder banao, aur `ls -l` se dekho ki default taale ka hisaab mila ya nahi. Ye principle of least privilege ka pehla abhyas hai: har staff ko utna hi haq jitna uske kaam ke liye chahiye.

### [14:30 – 15:45] Scene 6: Recap aur Bridge
**[VISUAL: A card: "r=4 w=2 x=1 · chmod · chown · umask · s, s, t · never 777".]**

**(Voiceover):**
Recap: teen ring, teen haq, number ka hisaab, chmod aur chown, default taala yaani umask, aur teen khaas nishaan: SUID, SGID aur sticky bit. Ab kamre to safe hain, par staff building ke andar aata kaise hai? Staff entrance se, yaani SSH se. Aur us darwaze ka sabse safe tareeka hai SSH keys. Agle episode mein.

---

# 📺 EPISODE 3: SSH Keys

### [00:00 – 01:15] Scene 1: Password ki Problem
**[VISUAL: The building's staff entrance, door number 22, facing a public road. Strangers keep punching random codes into its keypad. Cut to a server log showing thousands of failed login attempts from random IPs; a counter ticks fast: "password guesses".]**

**(Voiceover):**
Hamari building public road par hai, aur uska staff entrance, yaani SSH ka darwaza number 22, road se dikhta hai. Road se guzarne wala koi bhi keypad par code try kar sakta hai. Internet par jo bhi server khula hai, uspar kuch hi minute mein anjaan logon ke password guess karne ke attempts shuru ho jaate hain. Password kitna bhi accha ho, guess ya leak ho sakta hai. SSH keys is problem ka ek bahut behtar jawab hain: ek lambi jodi jise guess karna lagbhag namumkin hai, aur jiska ek hissa kabhi network par jaata hi nahi.

### [01:15 – 05:00] Scene 2: Public aur Private Key: Taala aur Chaabi
**[VISUAL: A padlock (public key) fitted on the staff entrance of several buildings (servers). One physical key (private key) stays with the staff member's laptop. Authentication: server challenges, laptop proves with key.]**

**(Voiceover):**
Ise taale aur chaabi se samjho. Public key ek taala hai, jo aap building ke staff entrance par lagwa dete ho. Wahi taala aap kitni bhi buildings par laga sakte ho, yaani kitne bhi servers par, aur use sabko dikhane mein koi dikkat nahi. Private key wo chaabi hai, jo sirf aapke paas rehti hai. Jab aap login karte ho, server ek chunauti bhejta hai, aapka laptop private key se use hal karta hai, aur server public key se verify kar leta hai. Chaabi kabhi network par nahi jaati. Isliye private key ko kabhi share mat karo, aur uspar ek passphrase bhi lagao.

### [05:00 – 08:30] Scene 3: Key Banana aur Server par Lagana
**[VISUAL: Terminal: `ssh-keygen -t ed25519 -C "asha@laptop"`, files `~/.ssh/id_ed25519` and `.pub`; `ssh-copy-id user@server`; `ssh user@server`. A list on the staff entrance labelled `authorized_keys`.]**

**(Voiceover):**
`ssh-keygen -t ed25519 -C "asha@laptop"` ek modern key jodi banata hai: `id_ed25519` private hai aur `id_ed25519.pub` public. Public key server par `~/.ssh/authorized_keys` file mein jaati hai. Ye staff entrance par lage taalon ki list hai. `ssh-copy-id user@server` ye kaam aapke liye kar deta hai. Uske baad `ssh user@server` bina password ke login karta hai. Yahi key jodi aage Git wale session mein GitHub par bhi kaam aayegi. Aur pichhle episode ke taale yahan bhi kaam aate hain: `~/.ssh` folder 700 aur private key 600 honi chahiye, warna SSH khud mana kar deta hai.

### [08:30 – 11:30] Scene 4: Lab: Password Login Band Karo
**[VISUAL: The keypad on the staff entrance is removed; only the key lock remains. `/etc/ssh/sshd_config` open with `PasswordAuthentication no` and `PermitRootLogin no`; then `sudo systemctl reload ssh`, with a warning banner "Keep one session open!".]**

**(Voiceover):**
Ab keypad hi hata dete hain, taaki staff entrance sirf chaabi se khule. Lab: pehle key se login kaam karta hai ye pakka karo. Phir `/etc/ssh/sshd_config` mein `PasswordAuthentication no` aur `PermitRootLogin no` karo, aur `sudo systemctl reload ssh` chalao. Doosri setting ka matlab: general manager seedha staff entrance se nahi aata. Har koi apne naam se aata hai, aur zaroorat par sudo se master key udhaar leta hai. Bahut zaroori: ek SSH session khula rakho, aur doosre terminal se naya login test karo. Agar kuch galat hua to aap bahar nahi hoge. Ye chhoti si setting server ko brute-force se kaafi bacha leti hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "ed25519 · .pub on server · private stays home · 700/600 · no password".]**

**(Voiceover):**
Recap: key jodi, public server par, private aapke paas, permissions sahi, password login band. Staff andar aa gaya aur kamre safe hain. Ab building mein naya saaman kaise aata hai, aur subah building khulti kaise hai? Yaani software kaise install hota hai aur system boot kaise hota hai, ye dekhte hain.

---

# 📺 EPISODE 4: Packages aur Boot Process

### [00:00 – 01:15] Scene 1: Software Kahan se Aata Hai?
**[VISUAL: The hotel's purchase desk with an approved vendor catalogue. A staff member orders an oven; it arrives with every fitting it needs. The desk transforms into a terminal with `apt install nginx` and a progress bar.]**

**(Voiceover):**
Atithi ki building mein koi staff bazaar se apni marzi ka saaman utha kar nahi laata. Sab kuch purchase department se aata hai, approved vendor catalogue se, aur saath mein uski zaroori fittings bhi. Linux mein yahi kaam package manager karta hai. Catalogue yaani repository, fittings yaani dependencies. Wo software ko dhoondhta hai, dependencies ke saath download karta hai, aur install, update, remove sab sambhalta hai. Server par kabhi kisi website se installer download karke nahi chalate. Hamesha package manager se.

### [01:15 – 05:00] Scene 2: apt aur dnf
**[VISUAL: Two columns. Ubuntu: `sudo apt update`, `sudo apt install nginx`, `apt search`, `sudo apt remove`. RHEL family: `sudo dnf install nginx`, `dnf search`, `dnf remove`.]**

**(Voiceover):**
Ubuntu aur Debian mein `apt`. `sudo apt update` catalogue ki taaza copy laata hai, yaani package list ka naya version. `sudo apt install nginx` software install karta hai, `apt search` dhoondhta hai, `sudo apt remove` hatata hai. Red Hat family mein `dnf`, yaani `sudo dnf install nginx`. Wahan purana naam `yum` tha, aur aaj bhi `yum` likho to wo `dnf` hi chalata hai. Tool alag hai, idea ek. Security ke liye regular updates zaroori hain, aur production par update karne se pehle test environment mein try karo.

### [05:00 – 08:30] Scene 3: Linux Boot Process
**[VISUAL: The hotel at dawn, opening in order: power check (Firmware: BIOS/UEFI) → picking the day's playbook (Bootloader: GRUB) → management office wakes up (Kernel + initramfs) → shift supervisor arrives (systemd) → departments open (Services) → staff entrance opens (Login prompt). A side card: "run level 3 = multi-user.target · run level 5 = graphical.target". Terminal: `systemctl get-default`.]**

**(Voiceover):**
Computer ON kaise hota hai? Hotel ke subah ke opening routine ki tarah, ek tay kram mein. Pehle bijli aur building ki jaanch: firmware, BIOS ya UEFI, hardware check karta hai. Phir bootloader, GRUB, tay karta hai kaun sa kernel uthana hai aur use memory mein load karta hai. Kernel ke saath ek chhota temporary root bhi load hota hai, initramfs, jisme disk tak pahunchne ke drivers hote hain. Phir management office jaagta hai: kernel hardware chalu karta hai aur pehla process, systemd, start karta hai. systemd hamara shift supervisor hai, jo baaki departments ko sahi kram mein kholta hai, yaani services, jaise networking aur SSH. Aakhir mein staff entrance khulta hai, yaani login aata hai. Purane systems mein supervisor ka naam init tha, aur wo run levels se kaam karta tha: 3 yaani bina graphics ke poora multi-user mode, 5 yaani graphical. systemd mein inhe targets kehte hain: `multi-user.target` aur `graphical.target`. `systemctl get-default` batata hai ki aapka server kis target tak boot hota hai. Jab server boot nahi hota, to is routine ka kaun sa kadam atka hai ye pehchaan kar hi aap sahi jagah dekh paate ho.

### [08:30 – 11:30] Scene 4: Lab: nginx Install aur Check
**[VISUAL: Terminal: `sudo apt update && sudo apt install -y nginx`, `systemctl status nginx`, `curl -I localhost`. Browser tab shows the nginx welcome page. A small inset: a front desk opening at door number 80.]**

**(Voiceover):**
Lab: purchase department se ek naya department mangwate hain. `sudo apt update && sudo apt install -y nginx` chalao. nginx building ka front desk hai, jo darwaza number 80 par guests ko jawab deta hai. `systemctl status nginx` se shift supervisor se poochho ki ye service chal rahi hai ya nahi. `curl -I localhost` se HTTP response header aayega, 200 OK. `systemctl get-default` bhi chala kar dekho: server par aam taur par `multi-user.target` milega. Agar aapka VM cloud mein hai to uska public IP browser mein kholo aur nginx ka welcome page dekho. Agar na dikhe to gate ka guard rok raha ho sakta hai, yaani firewall ya security group, jo hum cloud sessions mein detail se dekhenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "apt/dnf · systemd boots services · targets · know the boot chain".]**

**(Voiceover):**
Recap: saaman purchase department se, yaani packages package manager se. Subah ka opening routine, yaani boot ki chain. Aur ek chalti nginx service. Ab Atithi ki building mein staff hai, taale hain, aur pehla guest serve ho sakta hai. Agle session mein manager ka daily round: jab server dheema ho, bhar jaye ya toote, to use kaise dekhein aur theek karein.

---

# 📎 Student handout: Session 04 command sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Kaam | Command |
|---|---|
| Naya user (home, shell, comment, UID) | `sudo useradd -m -s /bin/bash -c "text" -u UID user` |
| Primary / secondary group ke saath user | `sudo useradd -m -g grp -G grp1,grp2 user` |
| Password set karna | `sudo passwd user` |
| Password lock / unlock | `sudo usermod -L user` / `sudo usermod -U user` |
| User hatana (home ke saath) | `sudo userdel -r user` |
| Group banana | `sudo groupadd grp` |
| Secondary group mein jodna | `sudo usermod -aG grp user` ya `sudo gpasswd -a user grp` |
| Group se hatana | `sudo gpasswd -d user grp` |
| User ke groups dekhna | `id user` |
| Password policy dekhna / badalna | `sudo chage -l user` / `sudo chage -m MIN -M MAX -W WARN user` |
| sudo rules badalna | `sudo visudo` |
| Permissions | `chmod u+x file`, `chmod g=rx file`, `chmod 640 file` |
| Owner aur group badalna | `sudo chown user:grp file` |
| Default permissions | `umask` |
| Shared folder par SGID | `sudo chmod g+s dir` |
| SSH key banana aur bhejna | `ssh-keygen -t ed25519`, `ssh-copy-id user@server` |
| Package (Ubuntu / Red Hat family) | `sudo apt install pkg` / `sudo dnf install pkg` |
| Boot target | `systemctl get-default` |

# ✍️ 02: SCRIPT — SESSION-04: Linux Users, Permissions & SSH
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S04`
- **Focus:** Users/groups/root, sudo, file permissions (chmod/chown), SSH keys, package managers, boot process
- **Story position:** Zoom level 1, inside one building. Atithi Hotels staff rakhta hai aur kamron par taale lagata hai.
- **Story words used:** staff (users), general manager (root), duty manager (sudo user), staff register (`/etc/passwd`), tijori (`/etc/shadow`), department (group), teen-ring taala (permissions), staff entrance (SSH), purchase department (package manager), opening routine (boot), shift supervisor (systemd)
- **Episodes:**
  - Episode 1: Users, Groups aur sudo: Staff, Departments aur Master Key
  - Episode 2: File Permissions: Teen-Ring Taala aur rwx ka Hisaab
  - Episode 3: SSH Keys: Staff Entrance ki Apni Chaabi
  - Episode 4: Packages aur Boot Process: Purchase Department aur Subah ka Opening Routine

---

# 📺 EPISODE 1: Users, Groups aur sudo

### [00:00 – 01:15] Scene 1: Sabke Paas Master Key Ho To?
**[VISUAL: The Atithi Hotels building. Ten staff members, each holding the same master key. One of them empties the records room by mistake. Cut to a shared server: 10 developers logged in as "root", one deletes a config folder, every terminal flashes red.]**

**(Voiceover):**
Pichhle session mein Atithi Hotels ko apni pehli building mili thi. Ab socho is building mein dus staff hain, aur sabke paas master key hai. Ek ne galti se records room khaali kar diya. Ab pata nahi kisne kiya, aur rok bhi koi nahi sakta tha. Server par bilkul yahi hota hai jab dus developers root se login karte hain aur ek galti se zaroori folder hata deta hai. Linux ka user system isi problem ke liye hai: har staff ki apni pehchaan, aur utni hi power jitni kaam ke liye zaroori hai. Is session mein hum building mein staff rakhenge aur kamron par taale lagayenge. Is episode mein: users, groups aur sudo.

### [01:15 – 04:30] Scene 2: Normal User, Root aur UID
**[VISUAL: Inside the building. The general manager (root) holds the master key. Staff wear ID cards. A card shows "UID 0 = root, UID ≥ 1000 = normal users". On the desk: a staff register labelled `/etc/passwd` and a locked safe labelled `/etc/shadow`. Guests walk through the lobby with no ID card.]**

**(Voiceover):**
Pehle ek rule yaad rakho: Linux ke users hotel ka staff hain, guests nahi. Guest yaani website ka end user, aur use kabhi staff ID card nahi milta. Ab staff ko dekho. Root is building ka general manager hai, jiske paas master key hai. Uska UID 0 hota hai, aur wo kuch bhi kar sakta hai. Normal user aam staff hai: uska apna quarter, yaani home directory, aur limited rights. Kuch users insaan hote hi nahi, wo ek hi kaam wale service staff hain, jaise web server ka user, aur wo login nahi karte. Isiliye rule ye hai: roz ka kaam normal user se, aur zaroorat padne par hi power uthao. Staff ki jaankari staff register mein hoti hai, yaani `/etc/passwd`. Password ka hash ek band tijori mein rehta hai, yaani `/etc/shadow`, jise sirf root padh sakta hai.

### [04:30 – 08:00] Scene 3: Users aur Groups ka Management
**[VISUAL: A new staff member "asha" gets an ID card and a quarter, then a department access card marked "devs". Terminal: `sudo useradd -m asha`, `sudo passwd asha`, `sudo groupadd devs`, `sudo usermod -aG devs asha`, `id asha`.]**

**(Voiceover):**
Naya staff rakhte hain. `useradd -m asha` ek naya user banata hai, aur `-m` uska quarter yaani home directory bhi banata hai. `passwd asha` password set karta hai. Ab departments. Group ek department ki tarah hota hai: `groupadd devs` department banata hai, aur `usermod -aG devs asha` asha ko us department ka access card deta hai. Yahan `-a` ka matlab append hai, aur use bhoolna khatarnaak hai, kyunki tab asha ke baaki department cards chhin jaate hain, yaani baaki groups hat jaate hain. `id asha` batata hai ki user kis kis group mein hai.

### [08:00 – 11:30] Scene 4: Lab: sudo ka Sahi Use
**[VISUAL: A duty manager signs a register, borrows the master key, returns it. Terminal: user "asha" runs `apt update` and gets "Permission denied", then `sudo apt update` works. `visudo` shown briefly with a caution sign.]**

**(Voiceover):**
Hotel mein duty manager general manager nahi hota. Par zaroorat padne par wo master key udhaar le sakta hai, aur har baar register mein entry hoti hai. Linux mein yahi sudo hai. Lab: naya user banao aur use `sudo` group mein jodo, Ubuntu par `sudo usermod -aG sudo asha`. Ab asha ke naam se login karo. Bina sudo ke `apt update` chalao, error milegi. Phir `sudo apt update` chalao, kaam karega. Sudo aapka password maangta hai aur har command ka log rakhta hai, isliye ye root login se behtar hai: pata rehta hai kisne kya kiya. Aur sudo rules badalne ho to seedha file mat kholo, `visudo` use karo, kyunki wo syntax check karta hai aur aapko lock hone se bachata hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Normal user for daily work · sudo for power · groups for teams". Under it, small: "staff · duty manager · departments".]**

**(Voiceover):**
Recap: aam staff yaani normal user, general manager yaani root, departments yaani groups, aur duty manager ki udhaar wali master key yaani sudo. Ab sawaal: kis staff ko kis kamre mein kya karne diya jaye, ye kaun tay karta hai? Wo hain kamron ke taale, yaani file permissions, agle episode mein.

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
Taale ki rings ghumane ke liye `chmod`. Number se: `chmod 640 secret.txt` owner ko read-write, group ko read, others ko kuch nahi. Symbolic tareeke se: `chmod u+x deploy.sh` owner ko execute deta hai. Kamre ki nameplate badalne ke liye, yaani owner badalne ke liye, `chown`: `sudo chown asha:devs app.log` owner asha aur group devs kar deta hai. Aur ek khatarnaak aadat: `chmod 777` kabhi mat lagao. Ye taala hata kar darwaza khula chhod dene jaisa hai, sab ko sab kuch mil jaata hai, aur security audits mein pehli galti yahi pakdi jaati hai.

### [08:30 – 11:30] Scene 4: Lab: Script Chalao aur Secret Chhupao
**[VISUAL: Terminal: create `hello.sh`, run `./hello.sh` → "Permission denied", `chmod u+x hello.sh` → runs. Then a `secret.txt` with 600; another user tries `cat` and is denied.]**

**(Voiceover):**
Lab. `echo 'echo hello devops' > hello.sh` se script banao, `./hello.sh` chalao, "Permission denied" aayega kyunki execute ka haq nahi hai. `chmod u+x hello.sh` ke baad chalega. Ab ek `secret.txt` banao, `chmod 600 secret.txt` lagao, yaani sirf owner ki ring khuli hai, aur doosre user se `cat` karke dekho, access nahi milega. Ye principle of least privilege ka pehla abhyas hai: har staff ko utna hi haq jitna uske kaam ke liye chahiye.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "r=4 w=2 x=1 · chmod · chown · never 777".]**

**(Voiceover):**
Recap: teen ring, teen haq, number ka hisaab, chmod aur chown. Ab kamre to safe hain, par staff building ke andar aata kaise hai? Staff entrance se, yaani SSH se. Aur us darwaze ka sabse safe tareeka hai SSH keys. Agle episode mein.

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
`ssh-keygen -t ed25519 -C "asha@laptop"` ek modern key jodi banata hai: `id_ed25519` private hai aur `id_ed25519.pub` public. Public key server par `~/.ssh/authorized_keys` file mein jaati hai. Ye staff entrance par lage taalon ki list hai. `ssh-copy-id user@server` ye kaam aapke liye kar deta hai. Uske baad `ssh user@server` bina password ke login karta hai. Aur pichhle episode ke taale yahan bhi kaam aate hain: `~/.ssh` folder 700 aur private key 600 honi chahiye, warna SSH khud mana kar deta hai.

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
Ubuntu aur Debian mein `apt`. `sudo apt update` catalogue ki taaza copy laata hai, yaani package list ka naya version. `sudo apt install nginx` software install karta hai, `apt search` dhoondhta hai, `sudo apt remove` hatata hai. Red Hat family mein `dnf`, yaani `sudo dnf install nginx`. Tool alag hai, idea ek. Security ke liye regular updates zaroori hain, aur production par update karne se pehle test environment mein try karo.

### [05:00 – 08:30] Scene 3: Linux Boot Process
**[VISUAL: The hotel at dawn, opening in order: power check (Firmware: BIOS/UEFI) → picking the day's playbook (Bootloader: GRUB) → management office wakes up (Kernel) → shift supervisor arrives (systemd) → departments open (Services) → staff entrance opens (Login prompt).]**

**(Voiceover):**
Computer ON kaise hota hai? Hotel ke subah ke opening routine ki tarah, ek tay kram mein. Pehle bijli aur building ki jaanch: firmware, BIOS ya UEFI, hardware check karta hai. Phir bootloader, GRUB, tay karta hai kaun sa kernel uthana hai aur use memory mein load karta hai. Phir management office jaagta hai: kernel hardware chalu karta hai aur pehla process, systemd, start karta hai. systemd hamara shift supervisor hai, jo baaki departments ko sahi kram mein kholta hai, yaani services, jaise networking aur SSH. Aakhir mein staff entrance khulta hai, yaani login aata hai. Jab server boot nahi hota, to is routine ka kaun sa kadam atka hai ye pehchaan kar hi aap sahi jagah dekh paate ho.

### [08:30 – 11:30] Scene 4: Lab: nginx Install aur Check
**[VISUAL: Terminal: `sudo apt update && sudo apt install -y nginx`, `systemctl status nginx`, `curl -I localhost`. Browser tab shows the nginx welcome page. A small inset: a front desk opening at door number 80.]**

**(Voiceover):**
Lab: purchase department se ek naya department mangwate hain. `sudo apt update && sudo apt install -y nginx` chalao. nginx building ka front desk hai, jo darwaza number 80 par guests ko jawab deta hai. `systemctl status nginx` se shift supervisor se poochho ki ye service chal rahi hai ya nahi. `curl -I localhost` se HTTP response header aayega, 200 OK. Agar aapka VM cloud mein hai to uska public IP browser mein kholo aur nginx ka welcome page dekho. Agar na dikhe to gate ka guard rok raha ho sakta hai, yaani firewall ya security group, jo hum cloud sessions mein detail se dekhenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "apt/dnf · systemd boots services · know the boot chain".]**

**(Voiceover):**
Recap: saaman purchase department se, yaani packages package manager se. Subah ka opening routine, yaani boot ki chain. Aur ek chalti nginx service. Ab Atithi ki building mein staff hai, taale hain, aur pehla guest serve ho sakta hai. Agle session mein manager ka daily round: jab server dheema ho, bhar jaye ya toote, to use kaise dekhein aur theek karein.

# ✍️ 02: SCRIPT — SESSION-04: Linux Users, Permissions & SSH
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S04`
- **Focus:** Users/groups/root, sudo, file permissions (chmod/chown), SSH keys, package managers, boot process
- **Episodes:**
  - Episode 1: Users, Groups aur sudo: Society ka Gate Pass
  - Episode 2: File Permissions: rwx ka Hisaab
  - Episode 3: SSH Keys: Password ke Bina Safe Entry
  - Episode 4: Packages aur Boot Process: Software kaise aata hai, System kaise uthta hai

---

# 📺 EPISODE 1: Users, Groups aur sudo

### [00:00 – 01:15] Scene 1: Sab Root Ban Jaayein To?
**[VISUAL: A shared server with 10 developers, all logged in as "root". One of them deletes a config folder. Every terminal flashes red.]**

**(Voiceover):**
Ek server par dus developers, aur sabne root se login kar rakha hai. Ek ne galti se ek zaroori folder hata diya. Ab pata nahi kisne kiya, aur rok bhi koi nahi sakta tha. Linux ka user system isi problem ke liye hai: har insaan ki apni pehchaan aur utni hi power jitni zaroori hai. Is episode mein users, groups aur sudo seekhte hain.

### [01:15 – 04:30] Scene 2: Normal User, Root aur UID
**[VISUAL: A housing society. Residents (normal users) with flat keys; a security head (root) with a master key. A card shows "UID 0 = root, UID ≥ 1000 = normal users".]**

**(Voiceover):**
Society socho. Residents ke paas apne flat ki chaabi hoti hai, aur security head ke paas master key. Root woh master key wala user hai, jiska UID 0 hota hai, aur wo kuch bhi kar sakta hai. Normal user ke paas apna home aur limited rights hote hain. Isiliye rule ye hai: roz ka kaam normal user se, aur zaroorat padne par hi power uthao. Aur users ki jaankari `/etc/passwd` mein hoti hai, jabki password ka hash `/etc/shadow` mein, jise sirf root padh sakta hai.

### [04:30 – 08:00] Scene 3: Users aur Groups ka Management
**[VISUAL: Terminal: `sudo useradd -m asha`, `sudo passwd asha`, `sudo groupadd devs`, `sudo usermod -aG devs asha`, `id asha`.]**

**(Voiceover):**
`useradd -m asha` ek naya user banata hai, `-m` uska home bhi banata hai. `passwd asha` password set karta hai. Group ek chhoti team ki tarah hota hai: `groupadd devs` group banata hai, aur `usermod -aG devs asha` user ko us group mein jodta hai. Yahan `-a` ka matlab append hai, aur use bhoolna khatarnaak hai, kyunki tab user ke baaki groups hat jaate hain. `id asha` batata hai ki user kis kis group mein hai.

### [08:00 – 11:30] Scene 4: Lab: sudo ka Sahi Use
**[VISUAL: Terminal: user "asha" runs `apt update` and gets "Permission denied", then `sudo apt update` works. `visudo` shown briefly with a caution sign.]**

**(Voiceover):**
Lab: naya user banao aur use `sudo` group mein jodo, Ubuntu par `sudo usermod -aG sudo asha`. Ab asha ke naam se login karo. Bina sudo ke `apt update` chalao, error milegi. Phir `sudo apt update` chalao, kaam karega. Sudo har baar aapki pehchaan check karta hai aur log bhi rakhta hai, ye root login se behtar hai. Aur sudo rules badalne ho to seedha file mat kholo, `visudo` use karo, kyunki wo syntax check karta hai aur aapko lock hone se bachata hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Normal user for daily work · sudo for power · groups for teams".]**

**(Voiceover):**
Recap: normal user, root, groups, sudo. Ab sawaal: user ko kya karne diya jaye, ye kaun tay karta hai? Wo hain file permissions, agle episode mein.

---

# 📺 EPISODE 2: File Permissions

### [00:00 – 01:15] Scene 1: Ek File, Teen Darwaze
**[VISUAL: A file icon with three doors labelled Owner, Group, Others. Each door has three locks: r, w, x.]**

**(Voiceover):**
Har file ke teen darwaze hote hain. Pehla owner, jisne file banayi. Doosra group, owner ki team. Teesra others, baaki sab. Aur har darwaze par teen taale: read, write, execute. Ye 3 gune 3 ka hisaab hi Linux permissions ka poora khel hai.

### [01:15 – 05:00] Scene 2: `ls -l` Padhna aur Octal Numbers
**[VISUAL: `-rwxr-xr--  1 asha devs  120 app.sh` with segments highlighted. Under it: r=4, w=2, x=1, and sums 7, 5, 4.]**

**(Voiceover):**
`ls -l` ki pehli column dekho: `-rwxr-xr--`. Pehla akshar file ka type, phir teen teen ke group: owner `rwx`, group `r-x`, others `r--`. Number se bhi likha jaa sakta hai: read ka 4, write ka 2, execute ka 1. To `rwx` yaani 7, `r-x` yaani 5, `r--` yaani 4. Is file ki permission 754 hai. Directory mein `x` ka matlab hota hai us folder ke andar ja sakna, ye yaad rakhna.

### [05:00 – 08:30] Scene 3: chmod aur chown
**[VISUAL: Terminal: `chmod 640 secret.txt`, `chmod u+x deploy.sh`, `sudo chown asha:devs app.log`, `ls -l` shows before/after.]**

**(Voiceover):**
Permission badalne ke liye `chmod`. Number se: `chmod 640 secret.txt` owner ko read-write, group ko read, others ko kuch nahi. Symbolic tareeke se: `chmod u+x deploy.sh` owner ko execute deta hai. Owner badalne ke liye `chown`: `sudo chown asha:devs app.log` owner asha aur group devs kar deta hai. Aur ek khatarnaak aadat: `chmod 777` kabhi mat lagao. Wo sab ko sab kuch de deta hai, aur security audits mein pehli galti yahi pakdi jaati hai.

### [08:30 – 11:30] Scene 4: Lab: Script Chalao aur Secret Chhupao
**[VISUAL: Terminal: create `hello.sh`, run `./hello.sh` → "Permission denied", `chmod u+x hello.sh` → runs. Then a `secret.txt` with 600; another user tries `cat` and is denied.]**

**(Voiceover):**
Lab. `echo 'echo hello devops' > hello.sh` se script banao, `./hello.sh` chalao, "Permission denied" aayega kyunki execute permission nahi hai. `chmod u+x hello.sh` ke baad chalega. Ab ek `secret.txt` banao, `chmod 600 secret.txt` lagao, aur doosre user se `cat` karke dekho, access nahi milega. Ye principle of least privilege ka pehla abhyas hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "r=4 w=2 x=1 · chmod · chown · never 777".]**

**(Voiceover):**
Recap: teen darwaze, teen taale, number ka hisaab, chmod aur chown. Ab remote server par ghusne ka sabse safe tareeka: SSH keys. Agle episode mein.

---

# 📺 EPISODE 3: SSH Keys

### [00:00 – 01:15] Scene 1: Password ki Problem
**[VISUAL: A server log showing thousands of failed login attempts from random IPs. A counter ticks fast: "password guesses".]**

**(Voiceover):**
Internet par jo bhi server khula hai, uspar kuch hi minute mein anjaan logon ke password guess karne ke attempts shuru ho jaate hain. Password kitna bhi accha ho, guess ya leak ho sakta hai. SSH keys is problem ka ek bahut behtar jawab hain: ek lamba, almost-impossible-to-guess jodi, jisme se ek hissa kabhi network par jaata hi nahi.

### [01:15 – 05:00] Scene 2: Public aur Private Key: Taala aur Chaabi
**[VISUAL: A padlock (public key) copied onto many doors (servers). One physical key (private key) stays with the user's laptop. Authentication: server challenges, laptop proves with key.]**

**(Voiceover):**
Ise taale aur chaabi se samjho. Public key ek taala hai, jo aap kisi bhi server par laga sakte ho, sabko dikhane mein koi dikkat nahi. Private key wo chaabi hai, jo sirf aapke paas rehti hai. Jab aap login karte ho, server ek chunauti bhejta hai, aapka laptop private key se use hal karta hai, aur server public key se verify kar leta hai. Chaabi kabhi network par nahi jaati. Isliye private key ko kabhi share mat karo, aur ussi ke liye ek passphrase bhi lagao.

### [05:00 – 08:30] Scene 3: Key Banana aur Server par Lagana
**[VISUAL: Terminal: `ssh-keygen -t ed25519 -C "asha@laptop"`, files `~/.ssh/id_ed25519` and `.pub`; `ssh-copy-id user@server`; `ssh user@server`.]**

**(Voiceover):**
`ssh-keygen -t ed25519 -C "asha@laptop"` ek modern key jodi banata hai: `id_ed25519` private hai aur `id_ed25519.pub` public. Public key server par `~/.ssh/authorized_keys` file mein jaati hai. `ssh-copy-id user@server` ye kaam aapke liye kar deta hai. Uske baad `ssh user@server` bina password ke login karta hai. Aur permissions yaad rakho: `~/.ssh` folder 700 aur private key 600 honi chahiye, warna SSH khud mana kar deta hai.

### [08:30 – 11:30] Scene 4: Lab: Password Login Band Karo
**[VISUAL: `/etc/ssh/sshd_config` open with `PasswordAuthentication no` and `PermitRootLogin no`; then `sudo systemctl reload ssh`, with a warning banner "Keep one session open!".]**

**(Voiceover):**
Lab: pehle key se login kaam karta hai ye pakka karo. Phir `/etc/ssh/sshd_config` mein `PasswordAuthentication no` aur `PermitRootLogin no` karo, aur `sudo systemctl reload ssh` chalao. Bahut zaroori: ek SSH session khula rakho, aur doosre terminal se naya login test karo. Agar kuch galat hua to aap bahar nahi hoge. Ye chhoti si setting server ko brute-force se kaafi bacha leti hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "ed25519 · .pub on server · private stays home · 700/600 · no password".]**

**(Voiceover):**
Recap: key jodi, public server par, private aapke paas, permissions sahi, password login band. Ab server par software kaise aata hai, aur system boot kaise hota hai, ye dekhte hain.

---

# 📺 EPISODE 4: Packages aur Boot Process

### [00:00 – 01:15] Scene 1: Software Kahan se Aata Hai?
**[VISUAL: A phone app store. It transforms into a terminal with `apt install nginx` and a progress bar.]**

**(Voiceover):**
Phone mein app store hota hai. Linux mein bhi hota hai, par command line se: package manager. Wo software ko dhoondhta hai, dependencies ke saath download karta hai, aur install, update, remove sab sambhalta hai. Server par kabhi bhi installer ki website se exe download nahi karte. Hamesha package manager se.

### [01:15 – 05:00] Scene 2: apt aur dnf
**[VISUAL: Two columns. Ubuntu: `sudo apt update`, `sudo apt install nginx`, `apt search`, `sudo apt remove`. RHEL family: `sudo dnf install nginx`, `dnf search`, `dnf remove`.]**

**(Voiceover):**
Ubuntu aur Debian mein `apt`. `sudo apt update` package list ka taaza version laata hai, `sudo apt install nginx` software install karta hai, `apt search` dhoondhta hai, `sudo apt remove` hatata hai. Red Hat family mein `dnf`, yani `sudo dnf install nginx`. Tool alag hai, idea ek. Security ke liye regular updates zaroori hain, aur production par update karne se pehle pehle test environment mein try karo.

### [05:00 – 08:30] Scene 3: Linux Boot Process
**[VISUAL: A relay race: Firmware (BIOS/UEFI) → Bootloader (GRUB) → Kernel → systemd (init) → Services → Login prompt.]**

**(Voiceover):**
Computer ON kaise hota hai? Ek relay race ki tarah. Pehle firmware, BIOS ya UEFI, hardware check karta hai. Phir bootloader, GRUB, kernel ko memory mein load karta hai. Kernel hardware chalu karta hai aur pehla process, systemd, start karta hai. systemd baaki services chalata hai, jaise networking aur SSH, aur aakhir mein login aata hai. Jab server boot nahi hota, to is race ka kaun sa hissa tuta hai ye pehchaan kar hi aap sahi jagah dekh paate ho.

### [08:30 – 11:30] Scene 4: Lab: nginx Install aur Check
**[VISUAL: Terminal: `sudo apt update && sudo apt install -y nginx`, `systemctl status nginx`, `curl -I localhost`. Browser tab shows the nginx welcome page.]**

**(Voiceover):**
Lab: `sudo apt update && sudo apt install -y nginx` chalao. `systemctl status nginx` se dekho ki service chal rahi hai. `curl -I localhost` se HTTP response header aayega, 200 OK. Agar aapka VM cloud mein hai to uska public IP browser mein kholo aur nginx ka welcome page dekho. Agar na dikhe to firewall ya security group ki wajah ho sakti hai, jo hum cloud sessions mein detail se dekhenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "apt/dnf · systemd boots services · know the boot chain".]**

**(Voiceover):**
Recap: packages manager se install, boot ki chain, aur ek chalti nginx service. Ab aapka server chal raha hai. Agle session mein seekhenge ki jab wo dheema ho, bhar jaye ya toote, to usse kaise dekhein aur theek karein.

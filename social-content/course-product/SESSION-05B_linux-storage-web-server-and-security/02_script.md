# ✍️ 02: SCRIPT — SESSION-05B: Linux Storage, Web Server & Security Layers
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S05B`
- **Focus:** Disks, partitions (MBR vs GPT), file systems, mounting and `/etc/fstab`, swap, LVM (create, extend, reduce), Apache `httpd`, firewalld zones, SELinux modes and labels, NAT (masquerade, port forwarding, rich rules)
- **Author's notes woven in:** `Linux-Handwritten-Notes.md` sections 10 to 15 (map: `NOTES_INTEGRATION_MAP_LINUX_K8S.md`)
- **Lab machine:** a Red Hat family VM (Rocky Linux or AlmaLinux 9) with two extra empty disks, 5 GB and 10 GB. In VirtualBox they show up as `/dev/sdb` and `/dev/sdc`. On other platforms the names differ (`/dev/vdb`, `/dev/nvme1n1`); always read `lsblk` first.
- **Story position:** Zoom level 1, inside one building. Atithi Hotels nayi khaali jagah ko kamron mein badalta hai, guests ke liye front-of-house kholta hai, aur chaabi ke upar ek doosri suraksha lagata hai.
- **Story words used:** khaali floor (raw disk), deewarein (partitions), shelving (file system), corridor se darwaza (mount), subah ki darwaza-list (`/etc/fstab`), overflow room (swap), movable deewar wale banquet halls (LVM), floor ka pool (volume group), front-of-house (Apache `httpd`), gate ka guard aur suraksha star (firewalld zones), badge wali doosri suraksha (SELinux), dispatch desk (masquerade), operator jo caller ko sahi kamre tak bhejta hai (port forwarding)
- **Episodes:**
  - Episode 1: Khaali Floor se Kamre tak: Disk, Partition, File System aur Swap
  - Episode 2: LVM: Movable Deewar wale Banquet Halls
  - Episode 3: Apache aur firewalld: Front-of-House aur Gate ka Guard
  - Episode 4: SELinux aur NAT: Badge wali Suraksha aur Dispatch Desk

---

# 📺 EPISODE 1: Khaali Floor se Kamre tak

### [00:00 – 01:30] Scene 1: "No Space Left on Device"
**[VISUAL: The Atithi Hotels building. Every storeroom is stuffed to the ceiling; a staff member cannot put down one more box. A terminal flashes `No space left on device`. The landlord hands over the key to a new floor: bare concrete, no walls, no shelves, no door from the corridor. Cut to a VM settings window where two new empty disks are being attached.]**

**(Voiceover):**
Pichhle session mein manager ke round mein ek line dikhi thi: disk 96% bhari hai. Aaj wo poori bhar gayi, aur server keh raha hai "No space left on device". Atithi landlord se ek nayi floor kiraye par leta hai. Par wo floor bilkul khaali hai: na deewarein, na shelves, na corridor se koi darwaza. Uspar saaman rakhne se pehle teen kaam karne padenge. Server par nayi disk ke saath bilkul yahi hota hai. Is session mein hum khaali jagah ko kamron mein badlenge, guests ke liye front-of-house kholenge, aur chaabi ke upar ek doosri suraksha lagayenge. Is session ke liye ek alag VM lo: Rocky Linux ya AlmaLinux, yaani Red Hat family, aur usme do khaali disks jodo, ek 5 GB aur ek 10 GB. Ab tak hum Ubuntu par the. Yahan package ka tool `dnf` hai, sudo wale group ka naam `wheel` hai, aur baaki sab wahi Linux hai.

### [01:30 – 04:30] Scene 2: Chaar Kadam, aur MBR vs GPT
**[VISUAL: Four panels in a row: bare floor (raw disk) → walls go up (partition) → shelves fitted (file system) → a door cut from the corridor (mount point). Terminal: `lsblk` showing `sda` with its partitions and `sdb`, `sdc` empty; `sudo blkid`; `df -h`. A side table: "MBR: 4 primary, up to 2 TB, `fdisk` · GPT: 128 partitions, `gdisk`".]**

**(Voiceover):**
Raasta hamesha yahi hai: khaali disk, phir partition, phir file system, phir mount. Partition deewarein hain, jo floor ko hisson mein baant-ti hain. File system shelving hai, jiske bina khaali hall mein kuch dhoondha nahi ja sakta. Aur mount corridor se us hall tak ka darwaza hai. `lsblk` disks aur unke partitions ka ped dikhata hai. `sda` par aapka system hai, `sdb` aur `sdc` abhi khaali hain. `sudo blkid` har hisse ka file system aur uska UUID batata hai, yaani uska pakka pehchaan number. Deewar khadi karne ke do purane-naye tareeke hain. MBR purana hai: chaar primary partitions tak, aur do terabyte tak ki disk. Zyada chahiye to chautha partition extended banta hai aur uske andar logical partitions. GPT naya hai: 128 partitions, aur badi disks. MBR ka tool `fdisk` hai, GPT ka `gdisk`, aur aaj ka `fdisk` dono samajhta hai.

### [04:30 – 08:00] Scene 3: Lab: Partition, Format, Mount
**[VISUAL: Terminal: `sudo fdisk /dev/sdb` with the keys typed one by one: `n`, `p`, Enter, Enter, `+2G`, `w`. Then `sudo partprobe`, `lsblk` showing `sdb1`. `sudo mkfs.ext4 /dev/sdb1`, `sudo mkdir /data`, `sudo mount /dev/sdb1 /data`, `df -h /data`. In the story inset: a wall goes up, shelves slide in, a door opens.]**

**(Voiceover):**
Lab. `sudo fdisk /dev/sdb` kholo. Andar `m` saare options dikhata hai. `n` dabao naye partition ke liye, `p` primary ke liye, number aur pehla sector default rehne do, aur aakhri sector ki jagah `+2G` likho, yaani do GB ka hissa. `w` se likh kar bahar aao. Jab tak `w` nahi dabaya, disk par kuch nahi badla. `sudo partprobe` kernel ko batata hai ki deewarein badal gayi hain, aur `lsblk` mein ab `sdb1` dikhega. Ye hissa abhi kachcha hai. `sudo mkfs.ext4 /dev/sdb1` uspar ext4 file system banata hai, yaani shelving lagata hai. Dhyaan se: `mkfs` us hisse ka purana sab kuch mita deta hai, isliye device ka naam do baar padho. Ab darwaza: `sudo mkdir /data`, phir `sudo mount /dev/sdb1 /data`. `df -h /data` mein nayi jagah dikh rahi hai. Par ye darwaza kachcha hai. Reboot ke baad ye mount gayab ho jayega.

### [08:00 – 10:45] Scene 4: Subah ki Darwaza-List: /etc/fstab
**[VISUAL: The shift supervisor's morning list titled `/etc/fstab`: "open these doors every morning". A new line being added: `UUID=3f1c...  /data  ext4  defaults  0  0`, with six labels under the six fields. A warning triangle: "wrong line = building may not open". Terminal: `sudo blkid /dev/sdb1`, `sudo vim /etc/fstab`, `sudo umount /data`, `sudo mount -a`, `df -h /data`.]**

**(Voiceover):**
Subah building khulte waqt shift supervisor ek list padhta hai: kaun kaun se darwaze kholne hain. Wo list `/etc/fstab` hai. Har line mein chhe khaane hote hain: device, mount point, file system ka type, options, aur aakhir mein do number, dump aur fsck ka order. Dono zero rakhna aam baat hai. Device ki jagah `/dev/sdb1` likh sakte ho, par behtar hai UUID likhna, jo `sudo blkid /dev/sdb1` se milta hai. Wajah: disk ka naam reboot par badal sakta hai, UUID nahi badalta. Line jodne ke baad seedha reboot mat karo. Pehle `sudo umount /data`, phir `sudo mount -a`, jo list ki har line ko abhi lagata hai. Error aaya to line galat hai, aur aapne use reboot se pehle pakad liya. Ye aadat zaroori hai, kyunki `/etc/fstab` ki ek galat line server ko boot hone se rok sakti hai.

### [10:45 – 13:15] Scene 5: Lab: Overflow Room: Swap
**[VISUAL: Work desks all full; a slower back room labelled "overflow" takes the idle work. Terminal: `free -h`, `sudo fdisk /dev/sdb` (`n`, `p`, Enter, Enter, `+1G`, `t`, `2`, `82`, `w`), `sudo partprobe`, `sudo mkswap /dev/sdb2`, `sudo swapon /dev/sdb2`, `swapon --show`, `free -h` with the Swap line grown. fstab line: `UUID=...  swap  swap  defaults  0  0`.]**

**(Voiceover):**
Pichhle session mein `free -h` mein swap ki line dekhi thi. Swap wo overflow room hai jahan kernel sust pade kaam ko bhej deta hai jab RAM ki desks bhar jaayein. Wo disk par hota hai, isliye RAM se bahut dheema hai. Swap RAM ka badal nahi, bas ek safety hai. Lab: `sudo fdisk /dev/sdb` mein ek aur partition banao, `+1G` ka. Phir `t` dabao, partition number 2 chuno, aur type code `82` do, yaani Linux swap. `w` se likho aur `sudo partprobe` chalao. Ab yahan `mkfs` nahi chalta. Swap ka apna tool hai: `sudo mkswap /dev/sdb2`. Phir `sudo swapon /dev/sdb2` use chalu karta hai, aur `swapoff` band. `free -h` mein swap ab ek GB badh gaya hai. Ise pakka karne ke liye `/etc/fstab` mein ek line: UUID, phir `swap`, `swap`, `defaults`, aur do zero. `sudo swapon -a` list ke saare swap chalu kar deta hai.

### [13:15 – 14:30] Scene 6: Recap aur Bridge
**[VISUAL: A card: "disk → partition → file system → mount · fstab with UUID · mount -a before reboot · mkswap + swapon". Under it, small: "floor · walls · shelves · door · morning list · overflow room".]**

**(Voiceover):**
Recap: khaali floor yaani disk, deewarein yaani partitions, shelving yaani file system, darwaza yaani mount, subah ki list yaani `/etc/fstab`, aur overflow room yaani swap. Par ek dikkat reh gayi. Ye deewarein pakki hain. Kal `/data` bhar gaya to use bada kaise karoge? Iska jawab hai movable deewarein, yaani LVM, agle episode mein.

---

# 📺 EPISODE 2: LVM

### [00:00 – 01:15] Scene 1: Deewar Pakki Hai, Shaadi Badi Hai
**[VISUAL: A banquet hall with fixed brick walls; a wedding party of 500 arrives at a hall built for 200; the manager looks at the empty hall next door, separated by a wall he cannot move. Then the same floor with sliding partition walls: one hall widens, the next narrows. Cut to `df -h` showing `/data` at 100% while `sdc` sits empty.]**

**(Voiceover):**
Atithi mein kal ek badi shaadi hai. Paanch sau mehmaan aa rahe hain, aur hall do sau ka hai. Bagal wala hall khaali pada hai, par beech ki deewar pakki hai. Normal partition ke saath yahi mushkil hai: `/data` bhar gaya, bagal mein jagah khaali hai, phir bhi use bada karna aasaan nahi. Ab socho deewarein sarakne wali hon: aaj ek hall bada, kal doosra. Linux mein yahi LVM hai, Logical Volume Manager. Aur ye aapke saamne hi tha: `lsblk` mein `sda` ke neeche jo `rl-root` jaisa naam dikhta hai, wo LVM hi hai. Rocky khud apna system LVM par rakhta hai.

### [01:15 – 04:15] Scene 2: Teen Parat: PV, VG, LV
**[VISUAL: Three layers stacked. Bottom: three floor pieces labelled PV (`sdc1`, `sdc2`, `sdc3`). Middle: they merge into one large pool labelled VG `my_vg`, drawn as a grid of small 4 MB tiles (extents). Top: two halls carved out of the pool, LV `my_lv1` and LV `my_lv2`, with free tiles left over. Each hall then gets shelves (file system) and a door (mount).]**

**(Voiceover):**
LVM mein teen parat hain. Sabse neeche physical volume, PV: floor ke wo tukde jo aap LVM ko saunp dete ho, yaani partitions ya poori disks. Beech mein volume group, VG: saare tukde mil kar ek bada pool ban jaate hain. Sabse upar logical volume, LV: us pool mein se kaata gaya ek hall. File system aur mount LV par lagta hai, bilkul normal partition ki tarah. Pool chhoti chhoti tiles mein banta hai, jinhe extents kehte hain. Ek extent ka default size 4 MB hai. Hall bada karna ho to pool se kuch aur tiles de do. Pool hi chhota pad jaye to usme ek naya tukda jod do. Yahi poori lacheelapan hai.

### [04:15 – 08:00] Scene 3: Lab: Pehla Logical Volume
**[VISUAL: Terminal, step by step: `sudo fdisk /dev/sdc` making three partitions (2G, 2G, 2G) each set to type `8e` with `t`; `sudo partprobe`; `lsblk`. `sudo pvcreate /dev/sdc1 /dev/sdc2`, `sudo pvs`. `sudo vgcreate my_vg /dev/sdc1 /dev/sdc2`, `sudo vgs`. `sudo lvcreate -n my_lv1 -L 1G my_vg`, `sudo lvs`. `sudo mkfs.ext4 /dev/my_vg/my_lv1`, `sudo mkdir /events`, fstab line, `sudo mount -a`, `df -h /events`.]**

**(Voiceover):**
Lab, doosri disk par. `sudo fdisk /dev/sdc` mein teen partitions banao, do do GB ke. Har ek ke liye `t` daba kar type `8e` do, yaani Linux LVM. `w` aur `partprobe`. Abhi hum do tukde use karenge, teesra baad ke liye. Kadam ek: `sudo pvcreate /dev/sdc1 /dev/sdc2` dono ko physical volume banata hai. `sudo pvs` se dekho. Kadam do: `sudo vgcreate my_vg /dev/sdc1 /dev/sdc2` dono ko ek pool mein jodta hai, jiska naam `my_vg` hai. `sudo vgs` mein lagbhag chaar GB ka pool dikhega. Kadam teen: `sudo lvcreate -n my_lv1 -L 1G my_vg`. `-n` naam hai, bada `-L` size hai, aur aakhir mein pool ka naam. Size ki jagah chhota `-l` do to aap extents ki ginti dete ho. `sudo lvs` se dekho. Hall ka pata hamesha `/dev/` phir VG ka naam phir LV ka naam hota hai. Kadam chaar, wahi purana kaam: `sudo mkfs.ext4 /dev/my_vg/my_lv1`, `sudo mkdir /events`, `/etc/fstab` mein line, aur `sudo mount -a`. `df -h /events` mein ek GB ka hall taiyaar hai.

### [08:00 – 11:00] Scene 4: Lab: Hall Bada Karo, Pool Bada Karo
**[VISUAL: The sliding wall moves; the hall grows from 1 GB to 2 GB while guests stay inside. Terminal: `sudo lvextend -r -L +1G /dev/my_vg/my_lv1`, `df -h /events` before and after. A side note: "without -r: `resize2fs` for ext4, `xfs_growfs` for XFS". Then the pool grows: `sudo pvcreate /dev/sdc3`, `sudo vgextend my_vg /dev/sdc3`, `sudo vgs`.]**

**(Voiceover):**
Ab shaadi wala din. `sudo lvextend -r -L +1G /dev/my_vg/my_lv1` hall ko ek GB bada karta hai. Plus ka nishaan zaroori hai: `+1G` yaani ek GB aur, sirf `1G` yaani kul size ek GB. Aur `-r` bahut kaam ka hai. Yaad rakho, hall ki deewar sarkaane se shelves apne aap nahi badhti. LV bada hota hai, file system nahi. `-r` dono kaam ek saath kar deta hai. Uske bina aapko khud karna padta: ext4 ke liye `resize2fs` aur device ka naam, XFS ke liye `xfs_growfs` aur mount point. `df -h /events` dekho: do GB, aur hall ek pal ke liye bhi band nahi hua. Ab pool: `sudo pvcreate /dev/sdc3`, phir `sudo vgextend my_vg /dev/sdc3`. `sudo vgs` mein pool do GB badh gaya. Cloud par yahi hoga: nayi disk jodo, pool mein milao, hall bada karo, aur application ko pata bhi nahi chalega.

### [11:00 – 13:15] Scene 5: Chhota Karna aur Hatana: Sambhal Kar
**[VISUAL: A wall sliding inward toward shelves still full of boxes; a red stop sign. Order shown as a numbered list: 1 backup, 2 `umount`, 3 file system check, 4 shrink file system, 5 shrink LV. Terminal: `sudo umount /events`, `sudo lvreduce -r -L 1G /dev/my_vg/my_lv1`, `sudo mount -a`. A note: "XFS cannot shrink". Then the removal order: `umount` → remove the fstab line → `sudo lvremove /dev/my_vg/<lv-name>`.]**

**(Voiceover):**
Bada karna surakshit hai. Chhota karna nahi. Agar deewar andar sarka di aur shelves wahin rahin, to saaman kuchal jayega, yaani data jayega. Isliye order ulta hai: pehle file system chhota, phir LV. Aur usse bhi pehle backup. Kadam: `sudo umount /events`, phir `sudo lvreduce -r -L 1G /dev/my_vg/my_lv1`. Yahan `-r` phir wahi kaam karta hai: pehle file system ki jaanch, phir use chhota karna, phir LV. Yahan `1G` kul naya size hai. Minus ke saath likho to utna ghatta hai. Phir `sudo mount -a`. Ek seema yaad rakho: XFS, jo Red Hat family ka default file system hai, sirf badh sakta hai, ghat nahi sakta. Chhota karna sirf ext4 par chalta hai. Aur jab hall ki zaroorat hi na rahe: use unmount karo, `/etc/fstab` se uski line hatao, phir `sudo lvremove` aur uska poora pata. Line hatana mat bhoolna, warna agli subah supervisor ek aisa darwaza kholne jayega jo hai hi nahi.

### [13:15 – 14:30] Scene 6: Recap aur Bridge
**[VISUAL: A card: "PV → VG → LV → file system → mount · lvextend -r · shrink = file system first · XFS grows only". Under it, small: "floor pieces · pool · halls with sliding walls".]**

**(Voiceover):**
Recap: tukde yaani PV, pool yaani VG, hall yaani LV. Bada karna aasaan, chhota karna sambhal kar, aur XFS kabhi chhota nahi hota. Ye sab aage cloud ke storage session mein kaam aayega, jahan landlord ki attachable disk par yahi commands chalengi. Ab building mein jagah hai. Agle episode mein guests ke liye front-of-house kholte hain: Apache web server, aur gate ka guard, firewalld.

---

# 📺 EPISODE 3: Apache aur firewalld

### [00:00 – 01:15] Scene 1: Building Taiyaar, Par Guest ko Kya Dikhega?
**[VISUAL: The hotel's public entrance, door 80, shut and dark. A guest stands outside. Inside, a uniformed service-staff member with the name tag `apache` waits behind an empty counter. A guard stands at the gate holding a short list that does not include door 80.]**

**(Voiceover):**
Building mein staff hai, taale hain, jagah hai. Par guest jab public entrance par aata hai, to use kuch nahi dikhta, kyunki darwaza number 80 par koi baitha hi nahi. Us darwaze par jo department guests ko panne dikhata hai, wo web server hai. Session 4 mein humne nginx dekha tha. Aaj uska sabse purana saathi: Apache, jiska package aur service ka naam Red Hat family mein `httpd` hai. Aur is baar gate par guard pehle se khada hai, to use bhi samjhana padega.

### [01:15 – 04:30] Scene 2: httpd: Install aur Uska Naksha
**[VISUAL: Terminal: `sudo dnf install -y httpd`, `sudo systemctl enable --now httpd`, `systemctl status httpd`, `curl -I localhost`, `grep apache /etc/passwd`. A map of the department: `/etc/httpd` (ServerRoot), `/etc/httpd/conf/httpd.conf` (main config), `/etc/httpd/conf.d/*.conf` (extra config), `/var/www/html` (DocumentRoot), `/var/log/httpd` (logbooks).]**

**(Voiceover):**
`sudo dnf install -y httpd` department ko purchase department se mangwata hai. `sudo systemctl enable --now httpd` use abhi kholta hai aur subah ki list mein bhi likhta hai. `curl -I localhost` se jawab aa gaya. Ab is department ka naksha yaad rakho. `/etc/httpd` iska ServerRoot hai, yaani poora daftar. Main config `/etc/httpd/conf/httpd.conf` hai, aur `conf.d` folder ki har `.conf` file bhi padhi jaati hai. Guests ko dikhne wale panne DocumentRoot mein rehte hain, jo default mein `/var/www/html` hai, aur pehla panna `index.html`. Logbooks `/var/log/httpd` mein. Aur `grep apache /etc/passwd` chalao: ye wahi uniform wala service staff hai jiski baat Session 4 mein hui thi. `apache` naam ka system user, jo login nahi karta, bas web server chalata hai. Ubuntu par isi software ka package `apache2` hai aur user `www-data`.

### [04:30 – 08:00] Scene 3: firewalld: Gate ka Guard aur Suraksha Star
**[VISUAL: A gate with several lanes, each lane a zone with its own list: `public`, `home`, `trusted`, `block`, `drop`. At `block` the guard says "sorry, not allowed"; at `drop` the guard looks straight ahead and says nothing. Two notebooks in the guard's hand: "today only" (runtime) and "permanent". Terminal: `sudo firewall-cmd --get-default-zone`, `--get-zones`, `--list-all`, `--get-services`.]**

**(Voiceover):**
Red Hat family mein gate ka guard `firewalld` hai, aur usse baat `firewall-cmd` se hoti hai. Pehle isi kaam ke liye log seedha iptables ke rules likhte the; firewalld use aasaan banata hai. Uska sabse zaroori shabd zone hai. Zone ek suraksha star hai: rules ka ek set, jo tay karta hai kaun si services aur ports khule hain. `sudo firewall-cmd --get-zones` bane-banaye zones dikhata hai, jaise `public`, `home`, `trusted`, `block` aur `drop`, aur `--get-default-zone` aam taur par `public` batata hai. Do zones ka farq yaad rakho. `block` mein guard keh deta hai "maaf kijiye, ijaazat nahi", yaani bhejne wale ko mana ka jawab milta hai. `drop` mein guard kuch bolta hi nahi, packet chupchaap gir jaata hai. `sudo firewall-cmd --list-all` current zone ki poori list dikhata hai, aur usme abhi `ssh` hai par `http` nahi. Guard ke paas do diary hain. Seedha rule likho to wo sirf aaj ke liye hai, yaani runtime. `--permanent` ke saath likho to wo pakki diary mein jaata hai, par tab tak lagta nahi jab tak aap `--reload` na karo. Isliye dono saath chalte hain.

### [08:00 – 10:45] Scene 4: Lab: Pehla Panna Guest tak
**[VISUAL: Terminal: `echo "<h1>Atithi Hotels: Swagat hai</h1>" | sudo tee /var/www/html/index.html`. From the laptop: `curl http://VM_IP` hangs and fails. Back on the VM: `sudo firewall-cmd --add-service=http --permanent`, `sudo firewall-cmd --reload`, `sudo firewall-cmd --list-services`. Laptop browser now shows the page. The guard adds "door 80" to the permanent diary.]**

**(Voiceover):**
Lab. `/var/www/html/index.html` mein ek line likho: Atithi Hotels, swagat hai. `curl localhost` par panna aa gaya. Ab apne laptop se `curl http://VM_IP` chalao. Jawab nahi aayega. Pichhle session ka order lagao: front desk sun raha hai, andar se jawab aa raha hai, to teesra kadam, guard. `sudo firewall-cmd --add-service=http --permanent`, phir `sudo firewall-cmd --reload`. `--list-services` mein ab `http` dikhega, aur laptop ke browser mein panna khul jayega. Service ke naam ki jagah number bhi de sakte ho: `--add-port=8080/tcp`. Aur kisi ek network ko alag zone mein daalna ho to `--add-source` ke saath uska address aur `--zone`. Jaise ek shararti subnet ko `block` zone mein.

### [10:45 – 13:15] Scene 5: Lab: Panne Nayi Jagah, aur Ek Ajeeb Inkaar
**[VISUAL: Terminal: `sudo mkdir /web`, a new `index.html` inside it, `sudo vim /etc/httpd/conf/httpd.conf` with two edits highlighted: `DocumentRoot "/web"` and `<Directory "/web">`. `sudo apachectl configtest` → `Syntax OK`. `sudo systemctl restart httpd`. `curl -I localhost` → `403 Forbidden`. `ls -ld /web` shows `drwxr-xr-x`. A puzzled face. In the story inset: the staff member holds the right key, but a second guard blocks the door and points at a badge.]**

**(Voiceover):**
Ab maan lo panne `/var/www/html` mein nahi, pichhle episode jaisi kisi nayi jagah par rakhne hain. `sudo mkdir /web`, aur usme ek naya `index.html`. Phir `/etc/httpd/conf/httpd.conf` mein do jagah badlaav: `DocumentRoot` ki line mein `/web`, aur uske neeche `/var/www/html` wale `Directory` block ka path bhi `/web`. `sudo apachectl configtest` se config jaancho, "Syntax OK" aana chahiye, phir `sudo systemctl restart httpd`. Ab `curl -I localhost`. Jawab: 403 Forbidden. Ajeeb hai. `ls -ld /web` dekho: permissions theek hain, sabko padhne ka haq hai. Taala khula hai, chaabi sahi hai, phir bhi andar jaane nahi diya ja raha. Yahan koi doosra guard hai, jo chaabi nahi, kuch aur dekh raha hai.

### [13:15 – 14:30] Scene 6: Recap aur Bridge
**[VISUAL: A card: "httpd · /etc/httpd/conf/httpd.conf · DocumentRoot · firewall-cmd --permanent + --reload · zones". Then a large "403?" over the `/web` folder.]**

**(Voiceover):**
Recap: `httpd` ka naksha, DocumentRoot, firewalld ke zones, aur `--permanent` ke saath `--reload` ki aadat. Aur ek adhoora sawaal: permissions sahi hain, phir 403 kyun? Us doosre guard ka naam SELinux hai. Agle episode mein hum use samjhenge, aur band kiye bina theek karenge.

---

# 📺 EPISODE 4: SELinux aur NAT

### [00:00 – 01:15] Scene 1: Chaabi Sahi, Phir Bhi "Ruko"
**[VISUAL: The `apache` staff member at the door of room `/web`, key in hand, lock open. A second guard steps in and compares two badges: the one on the staff member's chest and the one on the door. They do not match. "Ruko." Cut to the terminal with `403 Forbidden` still on screen.]**

**(Voiceover):**
Atithi mein suraksha ki do parat hain. Pehli parat taala aur chaabi hai, jo humne Session 4 mein lagayi thi. Doosri parat alag hai: har staff ki chhaati par ek badge hai, aur har kamre ke darwaze par bhi ek badge. Guard dono ko milata hai. Chaabi aapke paas ho, tab bhi badge na mile to andar nahi ja sakte. Pichhle episode ka 403 isi doosri parat ne diya tha. Linux mein iska naam SELinux hai, Security-Enhanced Linux.

### [01:15 – 04:30] Scene 2: DAC, MAC, Teen Modes aur Label
**[VISUAL: Two layers: "DAC: chmod, chown (owner decides)" and above it "MAC: SELinux policy (system decides)". Three switches: Enforcing (blocks + logs), Permissive (logs only), Disabled (nothing). Terminal: `getenforce`, `ls -ldZ /var/www/html` showing `system_u:object_r:httpd_sys_content_t:s0` with the four parts labelled user, role, type, level; `ls -ldZ /web` showing `default_t`; `ps -eZ | grep httpd` showing `httpd_t`.]**

**(Voiceover):**
`chmod` aur `chown` wali permissions ko DAC kehte hain, discretionary access control: file ka owner tay karta hai kaun kya karega. SELinux MAC hai, mandatory access control: system ki ek policy tay karti hai, aur owner use badal nahi sakta. Dono parat paar karni padti hain. SELinux ke teen modes hain. Enforcing: galat access ko rokta hai aur likhta hai. Permissive: rokta nahi, sirf likhta hai. Disabled: kuch nahi karta. `getenforce` current mode batata hai. Ab badge dekhte hain. `ls -ldZ /var/www/html` mein bada `Z` label dikhata hai. Uske chaar hisse hain: user, role, type aur level. Roz ke kaam mein sirf teesra hissa dekhna hota hai, type. Yahan wo `httpd_sys_content_t` hai. `ps -eZ | grep httpd` dekho: web server ka process `httpd_t` type ka hai. Policy kehti hai: `httpd_t` wala staff `httpd_sys_content_t` wale kamre padh sakta hai. Ab `ls -ldZ /web`: type `default_t` hai. Badge alag hai, isliye inkaar.

### [04:30 – 08:00] Scene 3: Lab: Band Mat Karo, Label Theek Karo
**[VISUAL: Terminal: `sudo ausearch -m AVC -ts recent` showing a line with `denied { read }`, `scontext=...httpd_t`, `tcontext=...default_t`. `sudo setenforce 0`, `curl -I localhost` → 200; `sudo setenforce 1` → 403 again. Then the real fix: `sudo dnf install -y policycoreutils-python-utils`, `sudo semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"`, `sudo restorecon -Rv /web`, `ls -ldZ /web`, `curl -I localhost` → 200. A crossed-out line: `SELINUX=disabled`.]**

**(Voiceover):**
Lab. Pehle saboot. `sudo ausearch -m AVC -ts recent` SELinux ke taaza inkaar dikhata hai: `denied`, kisne maanga, `httpd_t`, aur kis par, `default_t`. Ab ek jaanch: `sudo setenforce 0` mode ko permissive kar deta hai. `curl -I localhost` chalao, 200 aa gaya. To pakka ho gaya ki rokne wala SELinux hi tha. Ab turant `sudo setenforce 1` se wapas enforcing karo. Internet par aapko salaah milegi ki SELinux band kar do. Ye waisa hai jaise guard pareshan karta hai to use naukri se nikaal dena. Sahi ilaaj hai kamre par sahi badge lagana. Do kadam. Pehla: `sudo semanage fcontext -a -t httpd_sys_content_t` aur phir quotes mein `/web` ka pattern, jo handout mein likha hai. Ye policy mein likhta hai ki `/web` aur uske andar ki har cheez ka badge kya hona chahiye. Agar `semanage` na mile to `policycoreutils-python-utils` package install karo. Doosra kadam zaroori hai: `sudo restorecon -Rv /web`, jo us rule ke hisaab se badge sach mein chipkata hai. `ls -ldZ /web` mein ab `httpd_sys_content_t` hai, aur `curl` 200 deta hai, enforcing mode mein. Mode ko pakka badalna ho to `/etc/selinux/config` file hai, aur uske liye reboot lagta hai. Production par use enforcing hi rehne do.

### [08:00 – 10:45] Scene 4: NAT: Dispatch Desk ka Ek Hi Pata
**[VISUAL: A campus drawing. Three back-office rooms with internal numbers 172.25.1.1, .2, .3. A dispatch desk at the gate with two addresses: internal 172.25.1.4 and public 13.45.23.12. A letter leaves room .1 with "from 172.25.1.1"; at the desk the sender is rewritten to "from 13.45.23.12"; the reply comes back to the desk, which checks its register and hands it to room .1. Terminal: `sudo firewall-cmd --add-masquerade --permanent`, `sudo firewall-cmd --reload`, `sudo firewall-cmd --list-all` showing `masquerade: yes`.]**

**(Voiceover):**
Aakhri topic, jo aage cloud mein bahut kaam aayega: NAT, network address translation. Building ke andar ke kamron ke number private hote hain. Bahar ki duniya unhe nahi jaanti, aur un number par jawab nahi bhej sakti. To andar ki machine internet se baat kaise kare? Gate par ek dispatch desk hai, jiske paas ek public pata hai. Andar se jo bhi chitthi bahar jaati hai, desk uspar bhejne wale ka pata mita kar apna public pata likh deta hai, aur apne register mein note kar leta hai ki asli bhejne wala kaun tha. Jawab desk par aata hai, aur desk use sahi kamre tak pahuncha deta hai. Ise masquerade kehte hain. firewalld mein ye ek line hai: `sudo firewall-cmd --add-masquerade --permanent`, phir `--reload`. Bahar wala kabhi andar ke kamre ka number nahi dekhta, aur khud se andar aa bhi nahi sakta. Cloud ke networking session mein yahi kaam landlord ki ek service karegi, jiska naam NAT gateway hai.

### [10:45 – 13:15] Scene 5: Lab: Port Forwarding aur Rich Rules
**[VISUAL: An operator at the gate with a board: "door 22 → room .1 (SSH) · door 21 → room .2 (FTP) · door 80 → room .3 (HTTP)". A caller is passed through to the right room. Terminal: `sudo firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80 --permanent`, `sudo firewall-cmd --reload`. Laptop: `curl http://VM_IP:8080` shows the Atithi page. Then a rich rule on screen: `rule family="ipv4" source address="192.168.0.100" service name="ssh" reject`.]**

**(Voiceover):**
Masquerade andar se bahar ka raasta tha. Port forwarding ulta hai: bahar se aane wale ko andar sahi jagah bhejna. Gate ka operator ek board dekhta hai: darwaza 22 par aaye to pehle kamre mein, 80 par aaye to teesre mein. Lab ek hi VM par: `sudo firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80 --permanent`, phir `--reload`. Ab laptop se `curl http://VM_IP:8080` chalao. Aapne 8080 khatkhataya, aur jawab 80 par baithe Apache ne diya. Ye jaanch bahar se hi karna, kyunki ye rule sirf bahar se aane wale traffic par lagta hai, VM ke apne `localhost` par nahi. Usi command mein `toaddr` jod do to traffic kisi doosri machine par chala jaata hai, aur tab masquerade bhi chalu hona chahiye. Aur jab seedhe options kaafi na hon, to rich rules hain: poori sharton wala ek vaakya. Jaise, is ek address se aane wale SSH ko reject karo. Unka poora grammar `man firewalld.richlanguage` mein hai, aur ek namoona handout mein.

### [13:15 – 14:45] Scene 6: Recap aur Bridge
**[VISUAL: A card: "getenforce · ls -Z · semanage fcontext + restorecon · never disable · masquerade = out · forward-port = in". Under it, small: "badges · dispatch desk · operator". Then the whole building lit up: staff, locks, halls with sliding walls, front-of-house open, two layers of guards. A slip of paper with instructions appears on the desk.]**

**(Voiceover):**
Recap: SELinux yaani badge wali doosri suraksha, jise band nahi karte, uska label theek karte hain: `semanage fcontext` aur `restorecon`. Masquerade yaani dispatch desk ka ek public pata, andar se bahar ke liye. Port forwarding yaani operator, bahar se andar ke liye. Is session ke saath Atithi ki ek building poori taiyaar hai: staff, taale, jagah, front-of-house aur do parat ki suraksha. Par aapne dekha, har kaam ke liye kitni commands haath se chalani padin. Agle session mein hum inhe ek slip par likhna seekhenge, taaki desk khud unhe chalaye. Yaani Bash scripting.

---

# 📎 Student handout: Session 05B command sheet
*Not spoken. Shown on screen at the end, or given as a download. Device names (`sdb`, `sdc`) are from the lab VM; read `lsblk` on your own machine first.*

| Kaam | Command |
|---|---|
| Disks aur partitions dekhna | `lsblk`, `sudo fdisk -l`, `sudo blkid` |
| Partition banana | `sudo fdisk /dev/sdb` → `n`, `p`, size `+2G`, `w`; phir `sudo partprobe` |
| Partition type badalna | `fdisk` ke andar `t` → `82` (swap), `8e` (LVM) |
| File system banana | `sudo mkfs.ext4 /dev/sdb1`, `sudo mkfs.xfs /dev/sdb1` |
| Mount (temporary) | `sudo mount /dev/sdb1 /data`, `sudo umount /data` |
| Mount (permanent) | `/etc/fstab`: `UUID=<uuid>  /data  ext4  defaults  0 0`, phir `sudo mount -a` |
| Swap | `sudo mkswap /dev/sdb2`, `sudo swapon /dev/sdb2`, `swapon --show`, `sudo swapoff /dev/sdb2` |
| Swap (permanent) | `/etc/fstab`: `UUID=<uuid>  swap  swap  defaults  0 0`, phir `sudo swapon -a` |
| LVM banana | `sudo pvcreate DEV...`, `sudo vgcreate my_vg DEV...`, `sudo lvcreate -n my_lv1 -L 1G my_vg` |
| LVM dekhna | `sudo pvs`, `sudo vgs`, `sudo lvs` (detail: `pvdisplay`, `vgdisplay`, `lvdisplay`) |
| LV bada karna (file system ke saath) | `sudo lvextend -r -L +1G /dev/my_vg/my_lv1` |
| File system alag se badhana | ext4: `sudo resize2fs /dev/my_vg/my_lv1` · XFS: `sudo xfs_growfs /mountpoint` |
| LV chhota karna (sirf ext4, backup ke baad) | `sudo umount /events`, `sudo lvreduce -r -L 1G /dev/my_vg/my_lv1`, `sudo mount -a` |
| VG bada karna | `sudo pvcreate /dev/sdc3`, `sudo vgextend my_vg /dev/sdc3` |
| LV hatana | `sudo umount /mountpoint`, fstab se line hatao, `sudo lvremove /dev/my_vg/<lv-name>` |
| Apache | `sudo dnf install -y httpd`, `sudo systemctl enable --now httpd`, `sudo apachectl configtest` |
| Firewall dekhna | `sudo firewall-cmd --list-all`, `--get-default-zone`, `--get-zones`, `--get-active-zones` |
| Service / port kholna | `sudo firewall-cmd --add-service=http --permanent`, `sudo firewall-cmd --add-port=8080/tcp --permanent`, `sudo firewall-cmd --reload` |
| Ek network ko zone mein daalna | `sudo firewall-cmd --zone=block --add-source=192.168.0.0/24 --permanent` |
| SELinux mode | `getenforce`, `sudo setenforce 0` (permissive), `sudo setenforce 1` (enforcing) |
| Label dekhna | `ls -ldZ PATH`, `ps -eZ \| grep httpd` |
| Inkaar dekhna | `sudo ausearch -m AVC -ts recent` |
| Label theek karna | `sudo semanage fcontext -a -t httpd_sys_content_t "/web(/.*)?"`, phir `sudo restorecon -Rv /web` |
| Masquerade | `sudo firewall-cmd --add-masquerade --permanent`, `sudo firewall-cmd --reload` |
| Port forwarding | `sudo firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80 --permanent` (doosri machine ke liye `:toaddr=IP` jodo) |
| Rich rule (namoona) | `sudo firewall-cmd --add-rich-rule='rule family="ipv4" source address="192.168.0.100" service name="ssh" reject' --permanent` |

# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-05B_linux-storage-web-server-and-security

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,981 · **Episodes:** 4

---

# EPISODE 1: Khaali Floor se Kamre tak

## "No Space Left on Device"

Pichhle session mein manager ke round mein ek line dikhi thi: disk 96% bhari hai. Aaj wo poori bhar gayi, aur server keh raha hai "No space left on device". Atithi landlord se ek nayi floor kiraye par leta hai. Par wo floor bilkul khaali hai: na deewarein, na shelves, na corridor se koi darwaza. Uspar saaman rakhne se pehle teen kaam karne padenge. Server par nayi disk ke saath bilkul yahi hota hai. Is session mein hum khaali jagah ko kamron mein badlenge, guests ke liye front-of-house kholenge, aur chaabi ke upar ek doosri suraksha lagayenge. Is session ke liye ek alag VM lo: Rocky Linux ya AlmaLinux, yaani Red Hat family, aur usme do khaali disks jodo, ek 5 GB aur ek 10 GB. Ab tak hum Ubuntu par the. Yahan package ka tool dnf hai, sudo wale group ka naam wheel hai, aur baaki sab wahi Linux hai.

## Chaar Kadam, aur MBR vs GPT

Raasta hamesha yahi hai: khaali disk, phir partition, phir file system, phir mount. Partition deewarein hain, jo floor ko hisson mein baant-ti hain. File system shelving hai, jiske bina khaali hall mein kuch dhoondha nahi ja sakta. Aur mount corridor se us hall tak ka darwaza hai. lsblk disks aur unke partitions ka ped dikhata hai. sda par aapka system hai, sdb aur sdc abhi khaali hain. sudo blkid har hisse ka file system aur uska UUID batata hai, yaani uska pakka pehchaan number. Deewar khadi karne ke do purane-naye tareeke hain. MBR purana hai: chaar primary partitions tak, aur do terabyte tak ki disk. Zyada chahiye to chautha partition extended banta hai aur uske andar logical partitions. GPT naya hai: 128 partitions, aur badi disks. MBR ka tool fdisk hai, GPT ka gdisk, aur aaj ka fdisk dono samajhta hai.

## Lab: Partition, Format, Mount

Lab. sudo fdisk /dev/sdb kholo. Andar m saare options dikhata hai. n dabao naye partition ke liye, p primary ke liye, number aur pehla sector default rehne do, aur aakhri sector ki jagah +2G likho, yaani do GB ka hissa. w se likh kar bahar aao. Jab tak w nahi dabaya, disk par kuch nahi badla. sudo partprobe kernel ko batata hai ki deewarein badal gayi hain, aur lsblk mein ab sdb1 dikhega. Ye hissa abhi kachcha hai. sudo mkfs.ext4 /dev/sdb1 uspar ext4 file system banata hai, yaani shelving lagata hai. Dhyaan se: mkfs us hisse ka purana sab kuch mita deta hai, isliye device ka naam do baar padho. Ab darwaza: sudo mkdir /data, phir sudo mount /dev/sdb1 /data. df -h /data mein nayi jagah dikh rahi hai. Par ye darwaza kachcha hai. Reboot ke baad ye mount gayab ho jayega.

## Subah ki Darwaza-List: /etc/fstab

Subah building khulte waqt shift supervisor ek list padhta hai: kaun kaun se darwaze kholne hain. Wo list /etc/fstab hai. Har line mein chhe khaane hote hain: device, mount point, file system ka type, options, aur aakhir mein do number, dump aur fsck ka order. Dono zero rakhna aam baat hai. Device ki jagah /dev/sdb1 likh sakte ho, par behtar hai UUID likhna, jo sudo blkid /dev/sdb1 se milta hai. Wajah: disk ka naam reboot par badal sakta hai, UUID nahi badalta. Line jodne ke baad seedha reboot mat karo. Pehle sudo umount /data, phir sudo mount -a, jo list ki har line ko abhi lagata hai. Error aaya to line galat hai, aur aapne use reboot se pehle pakad liya. Ye aadat zaroori hai, kyunki /etc/fstab ki ek galat line server ko boot hone se rok sakti hai.

## Lab: Overflow Room: Swap

Swap wo overflow room hai jahan kernel sust pade kaam ko bhej deta hai jab RAM ki desks bhar jaayein. Wo disk par hota hai, isliye RAM se bahut dheema hai. Swap RAM ka badal nahi, bas ek safety hai. Lab: sudo fdisk /dev/sdb mein ek aur partition banao, +1G ka. Phir t dabao, partition number 2 chuno, aur type code 82 do, yaani Linux swap. w se likho aur sudo partprobe chalao. Ab yahan mkfs nahi chalta. Swap ka apna tool hai: sudo mkswap /dev/sdb2. Phir sudo swapon /dev/sdb2 use chalu karta hai, aur swapoff band. free -h mein swap ab ek GB badh gaya hai. Ise pakka karne ke liye /etc/fstab mein ek line: UUID, phir swap, swap, defaults, aur do zero. sudo swapon -a list ke saare swap chalu kar deta hai.

## Recap aur Bridge

Recap: khaali floor yaani disk, deewarein yaani partitions, shelving yaani file system, darwaza yaani mount, subah ki list yaani /etc/fstab, aur overflow room yaani swap. Par ek dikkat reh gayi. Ye deewarein pakki hain. Kal /data bhar gaya to use bada kaise karoge? Iska jawab hai movable deewarein, yaani LVM, agle episode mein.

---

# EPISODE 2: LVM

## Deewar Pakki Hai, Shaadi Badi Hai

Atithi mein kal ek badi shaadi hai. Paanch sau mehmaan aa rahe hain, aur hall do sau ka hai. Bagal wala hall khaali pada hai, par beech ki deewar pakki hai. Normal partition ke saath yahi mushkil hai: /data bhar gaya, bagal mein jagah khaali hai, phir bhi use bada karna aasaan nahi. Ab socho deewarein sarakne wali hon: aaj ek hall bada, kal doosra. Linux mein yahi LVM hai, Logical Volume Manager.

## Teen Parat: PV, VG, LV

LVM mein teen parat hain. Sabse neeche physical volume, PV: floor ke wo tukde jo aap LVM ko saunp dete ho, yaani partitions ya poori disks. Beech mein volume group, VG: saare tukde mil kar ek bada pool ban jaate hain. Sabse upar logical volume, LV: us pool mein se kaata gaya ek hall. File system aur mount LV par lagta hai, bilkul normal partition ki tarah. Pool chhoti chhoti tiles mein banta hai, jinhe extents kehte hain. Ek extent ka default size 4 MB hai. Hall bada karna ho to pool se kuch aur tiles de do. Pool hi chhota pad jaye to usme ek naya tukda jod do. Yahi poori lacheelapan hai.

## Lab: Pehla Logical Volume

Lab, doosri disk par. sudo fdisk /dev/sdc mein teen partitions banao, do do GB ke. Har ek ke liye t daba kar type 8e do, yaani Linux LVM. w aur partprobe. Abhi hum do tukde use karenge, teesra baad ke liye. Kadam ek: sudo pvcreate /dev/sdc1 /dev/sdc2 dono ko physical volume banata hai. sudo pvs se dekho. Kadam do: sudo vgcreate my_vg /dev/sdc1 /dev/sdc2 dono ko ek pool mein jodta hai, jiska naam my_vg hai. sudo vgs mein lagbhag chaar GB ka pool dikhega. Kadam teen: sudo lvcreate -n my_lv1 -L 1G my_vg. -n naam hai, bada -L size hai, aur aakhir mein pool ka naam. Size ki jagah chhota -l do to aap extents ki ginti dete ho. sudo lvs se dekho. Hall ka pata hamesha /dev/ phir VG ka naam phir LV ka naam hota hai. Kadam chaar, wahi purana kaam: sudo mkfs.ext4 /dev/my_vg/my_lv1, sudo mkdir /events, /etc/fstab mein line, aur sudo mount -a. df -h /events mein ek GB ka hall taiyaar hai.

## Lab: Hall Bada Karo, Pool Bada Karo

Ab shaadi wala din. sudo lvextend -r -L +1G /dev/my_vg/my_lv1 hall ko ek GB bada karta hai. Plus ka nishaan zaroori hai: +1G yaani ek GB aur, sirf 1G yaani kul size ek GB. Aur -r bahut kaam ka hai. Yaad rakho, hall ki deewar sarkaane se shelves apne aap nahi badhti. LV bada hota hai, file system nahi. -r dono kaam ek saath kar deta hai. Uske bina aapko khud karna padta: ext4 ke liye resize2fs aur device ka naam, XFS ke liye xfs_growfs aur mount point. df -h /events dekho: do GB, aur hall ek pal ke liye bhi band nahi hua. Ab pool: sudo pvcreate /dev/sdc3, phir sudo vgextend my_vg /dev/sdc3. sudo vgs mein pool do GB badh gaya. Cloud par yahi hoga: nayi disk jodo, pool mein milao, hall bada karo, aur application ko pata bhi nahi chalega.

## Chhota Karna aur Hatana: Sambhal Kar

Bada karna surakshit hai. Chhota karna nahi. Agar deewar andar sarka di aur shelves wahin rahin, to saaman kuchal jayega, yaani data jayega. Isliye order ulta hai: pehle file system chhota, phir LV. Aur usse bhi pehle backup. Kadam: sudo umount /events, phir sudo lvreduce -r -L 1G /dev/my_vg/my_lv1. Yahan -r phir wahi kaam karta hai: pehle file system ki jaanch, phir use chhota karna, phir LV. Yahan 1G kul naya size hai. Minus ke saath likho to utna ghatta hai. Phir sudo mount -a. Ek seema yaad rakho: XFS, jo Red Hat family ka default file system hai, sirf badh sakta hai, ghat nahi sakta. Chhota karna sirf ext4 par chalta hai. Aur jab hall ki zaroorat hi na rahe: use unmount karo, /etc/fstab se uski line hatao, phir sudo lvremove aur uska poora pata. Line hatana mat bhoolna, warna agli subah supervisor ek aisa darwaza kholne jayega jo hai hi nahi.

## Recap aur Bridge

Recap: tukde yaani PV, pool yaani VG, hall yaani LV. Bada karna aasaan, chhota karna sambhal kar, aur XFS kabhi chhota nahi hota. Ye sab aage cloud ke storage session mein kaam aayega, jahan landlord ki attachable disk par yahi commands chalengi. Ab building mein jagah hai. Agle episode mein guests ke liye front-of-house kholte hain: Apache web server, aur gate ka guard, firewalld.

---

# EPISODE 3: Apache aur firewalld

## Building Taiyaar, Par Guest ko Kya Dikhega?

Building mein staff hai, taale hain, jagah hai. Par guest jab public entrance par aata hai, to use kuch nahi dikhta, kyunki darwaza number 80 par koi baitha hi nahi. Us darwaze par jo department guests ko panne dikhata hai, wo web server hai. Session 4 mein humne nginx dekha tha. Aaj uska sabse purana saathi: Apache, jiska package aur service ka naam Red Hat family mein httpd hai. Aur is baar gate par guard pehle se khada hai, to use bhi samjhana padega.

## httpd: Install aur Uska Naksha

sudo dnf install -y httpd department ko purchase department se mangwata hai. sudo systemctl enable --now httpd use abhi kholta hai aur subah ki list mein bhi likhta hai. curl -I localhost abhi 403 dega, kyunki /var/www/html mein koi panna hi nahi; panna rakhte hi 200 aayega. Ab is department ka naksha yaad rakho. /etc/httpd iska ServerRoot hai, yaani poora daftar. Main config /etc/httpd/conf/httpd.conf hai, aur conf.d folder ki har .conf file bhi padhi jaati hai. Guests ko dikhne wale panne DocumentRoot mein rehte hain, jo default mein /var/www/html hai, aur pehla panna index.html. Logbooks /var/log/httpd mein. Aur grep apache /etc/passwd chalao: ye wahi uniform wala service staff hai jiski baat Session 4 mein hui thi. apache naam ka system user, jo login nahi karta, bas web server chalata hai. Ubuntu par isi software ka package apache2 hai aur user www-data.

## firewalld: Gate ka Guard aur Suraksha Star

Red Hat family mein gate ka guard firewalld hai, aur usse baat firewall-cmd se hoti hai. Uska sabse zaroori shabd zone hai. Zone ek suraksha star hai: rules ka ek set, jo tay karta hai kaun si services aur ports khule hain. sudo firewall-cmd --get-zones bane-banaye zones dikhata hai, jaise public, home, trusted, block aur drop, aur --get-default-zone aam taur par public batata hai. Do zones ka farq yaad rakho. block mein guard keh deta hai "maaf kijiye, ijaazat nahi", yaani bhejne wale ko mana ka jawab milta hai. drop mein guard kuch bolta hi nahi, packet chupchaap gir jaata hai. sudo firewall-cmd --list-all current zone ki poori list dikhata hai, aur usme abhi ssh hai par http nahi. Guard ke paas do diary hain. Seedha rule likho to wo sirf aaj ke liye hai, yaani runtime. --permanent ke saath likho to wo pakki diary mein jaata hai, par tab tak lagta nahi jab tak aap --reload na karo. Isliye dono saath chalte hain.

## Lab: Pehla Panna Guest tak

Lab. /var/www/html/index.html mein ek line likho: Atithi Hotels, swagat hai. curl localhost par panna aa gaya. Ab apne laptop se curl http://VM_IP chalao. Jawab nahi aayega. Pichhle session ka order lagao: front desk sun raha hai, andar se jawab aa raha hai, to teesra kadam, guard. sudo firewall-cmd --add-service=http --permanent, phir sudo firewall-cmd --reload. --list-services mein ab http dikhega, aur laptop ke browser mein panna khul jayega. Service ke naam ki jagah number bhi de sakte ho: --add-port=8080/tcp. Aur kisi ek network ko alag zone mein daalna ho to --add-source ke saath uska address aur --zone. Jaise ek shararti subnet ko block zone mein.

## Lab: Panne Nayi Jagah, aur Ek Ajeeb Inkaar

Ab maan lo panne /var/www/html mein nahi, pichhle episode jaisi kisi nayi jagah par rakhne hain. sudo mkdir /web, aur usme ek naya index.html. Phir /etc/httpd/conf/httpd.conf mein do jagah badlaav: DocumentRoot ki line mein /web, aur uske neeche /var/www/html wale Directory block ka path bhi /web. sudo apachectl configtest se config jaancho, "Syntax OK" aana chahiye, phir sudo systemctl restart httpd. Ab curl -I localhost. Jawab: 403 Forbidden. Ajeeb hai. ls -ld /web dekho: permissions theek hain, sabko padhne ka haq hai. Taala khula hai, chaabi sahi hai, phir bhi andar jaane nahi diya ja raha. Pehle tail /var/log/httpd/error_log dekho: agar usme "client denied by server configuration" likha hai to galti Apache ki apni config mein hai, jaise Directory wala block badalna reh gaya, SELinux ki nahi. Yahan koi doosra guard hai, jo chaabi nahi, kuch aur dekh raha hai.

## Recap aur Bridge

Recap: httpd ka naksha, DocumentRoot, firewalld ke zones, aur --permanent ke saath --reload ki aadat. Aur ek adhoora sawaal: permissions sahi hain, phir 403 kyun? Us doosre guard ka naam SELinux hai. Agle episode mein hum use samjhenge, aur band kiye bina theek karenge.

---

# EPISODE 4: SELinux aur NAT

## Chaabi Sahi, Phir Bhi "Ruko"

Atithi mein suraksha ki do parat hain. Pehli parat taala aur chaabi hai, jo humne Session 4 mein lagayi thi. Doosri parat alag hai: har staff ki chhaati par ek badge hai, aur har kamre ke darwaze par bhi ek badge. Guard dono ko milata hai. Chaabi aapke paas ho, tab bhi badge na mile to andar nahi ja sakte. Pichhle episode ka 403 isi doosri parat ne diya tha. Linux mein iska naam SELinux hai, Security-Enhanced Linux.

## DAC, MAC, Teen Modes aur Label

chmod aur chown wali permissions ko DAC kehte hain, discretionary access control: file ka owner tay karta hai kaun kya karega. SELinux MAC hai, mandatory access control: system ki ek policy tay karti hai, aur owner use badal nahi sakta. Dono parat paar karni padti hain. SELinux ke teen modes hain. Enforcing: galat access ko rokta hai aur likhta hai. Permissive: rokta nahi, sirf likhta hai. Disabled: kuch nahi karta. getenforce current mode batata hai. Ab badge dekhte hain. ls -ldZ /var/www/html mein bada Z label dikhata hai. Uske chaar hisse hain: user, role, type aur level. Roz ke kaam mein sirf teesra hissa dekhna hota hai, type. Yahan wo httpd_sys_content_t hai. ps -eZ | grep httpd dekho: web server ka process httpd_t type ka hai. Policy kehti hai: httpd_t wala staff httpd_sys_content_t wale kamre padh sakta hai. Ab ls -ldZ /web: type default_t hai. Badge alag hai, isliye inkaar.

## Lab: Band Mat Karo, Label Theek Karo

Lab. Pehle saboot. sudo ausearch -m AVC -ts recent SELinux ke taaza inkaar dikhata hai: denied, kisne maanga, httpd_t, aur kis par, default_t. Ab ek jaanch: sudo setenforce 0 mode ko permissive kar deta hai. curl -I localhost chalao, 200 aa gaya. To pakka ho gaya ki rokne wala SELinux hi tha. Ab turant sudo setenforce 1 se wapas enforcing karo. Internet par aapko salaah milegi ki SELinux band kar do. Ye waisa hai jaise guard pareshan karta hai to use naukri se nikaal dena. Sahi ilaaj hai kamre par sahi badge lagana. Do kadam. Pehla: sudo semanage fcontext -a -t httpd_sys_content_t aur phir quotes mein /web ka pattern, jo handout mein likha hai. Ye policy mein likhta hai ki /web aur uske andar ki har cheez ka badge kya hona chahiye. Agar semanage na mile to policycoreutils-python-utils package install karo. Doosra kadam zaroori hai: sudo restorecon -Rv /web, jo us rule ke hisaab se badge sach mein chipkata hai. ls -ldZ /web mein ab httpd_sys_content_t hai, aur curl 200 deta hai, enforcing mode mein. Mode ko pakka badalna ho to /etc/selinux/config file hai, aur uske liye reboot lagta hai. Production par use enforcing hi rehne do.

## NAT: Dispatch Desk ka Ek Hi Pata

Aakhri topic, jo aage cloud mein bahut kaam aayega: NAT, network address translation. Building ke andar ke kamron ke number private hote hain. Bahar ki duniya unhe nahi jaanti, aur un number par jawab nahi bhej sakti. To andar ki machine internet se baat kaise kare? Gate par ek dispatch desk hai, jiske paas ek public pata hai. Andar se jo bhi chitthi bahar jaati hai, desk uspar bhejne wale ka pata mita kar apna public pata likh deta hai, aur apne register mein note kar leta hai ki asli bhejne wala kaun tha. Jawab desk par aata hai, aur desk use sahi kamre tak pahuncha deta hai. Ise masquerade kehte hain. firewalld mein ye ek line hai: sudo firewall-cmd --add-masquerade --permanent, phir --reload. Bahar wala kabhi andar ke kamre ka number nahi dekhta, aur khud se andar aa bhi nahi sakta. Cloud ke networking session mein yahi kaam landlord ki ek service karegi, jiska naam NAT gateway hai.

## Lab: Port Forwarding aur Rich Rules

Masquerade andar se bahar ka raasta tha. Port forwarding ulta hai: bahar se aane wale ko andar sahi jagah bhejna. Gate ka operator ek board dekhta hai: darwaza 22 par aaye to pehle kamre mein, 80 par aaye to teesre mein. Lab ek hi VM par: sudo firewall-cmd --add-forward-port=port=8080:proto=tcp:toport=80 --permanent, phir --reload. Ab laptop se curl http://VM_IP:8080 chalao. Aapne 8080 khatkhataya, aur jawab 80 par baithe Apache ne diya. Ye jaanch bahar se hi karna, kyunki ye rule sirf bahar se aane wale traffic par lagta hai, VM ke apne localhost par nahi. Usi command mein toaddr jod do to traffic kisi doosri machine par chala jaata hai, aur tab masquerade bhi chalu hona chahiye. Aur jab seedhe options kaafi na hon, to rich rules hain: poori sharton wala ek vaakya. Jaise, is ek address se aane wale SSH ko reject karo. Unka poora grammar man firewalld.richlanguage mein hai, aur ek namoona handout mein.

## Recap aur Bridge

Recap: SELinux yaani badge wali doosri suraksha, jise band nahi karte, uska label theek karte hain: semanage fcontext aur restorecon. Masquerade yaani dispatch desk ka ek public pata, andar se bahar ke liye. Port forwarding yaani operator, bahar se andar ke liye. Is session ke saath Atithi ki ek building poori taiyaar hai: staff, taale, jagah, front-of-house aur do parat ki suraksha. Par aapne dekha, har kaam ke liye kitni commands haath se chalani padin. Agle session mein hum inhe ek slip par likhna seekhenge, taaki desk khud unhe chalaye. Yaani Bash scripting.

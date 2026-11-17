# ✍️ 02: SCRIPT — SESSION-10: EC2 Storage & Scaling
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S10`
- **Focus:** Instance families, EBS volumes (types, attach, partition and mount, resize online), snapshots, Elastic IP, AMIs, vertical vs horizontal scaling, launch templates, Auto Scaling Groups (target tracking, scheduled scaling, health)
- **Builds on:** Session 05B (partition, file system, `/etc/fstab`, LVM idea) — the same commands now run on a cloud volume. Students who skipped 05B should watch Episode 1 of that session first.
- **Story position:** Zoom level 2, the rented campus. Atithi building mein storeroom jodta hai, uski photograph leta hai, building ko photocopy karta hai, aur shaadi ke season mein extra buildings kholta hai.
- **Story words used:** storeroom (EBS), photograph (snapshot), furnished model hotel (AMI), wedding season (scaling), permanent address (Elastic IP), building size (instance type), landlord (AWS), tower (Availability Zone)
- **Lab project:** the Atithi booking page from Session 08, served by a building that grows into several identical buildings.
- **Cost rule:** every lab ends with deleting the volume, snapshot, AMI, its snapshot and the Auto Scaling Group. A forgotten ASG keeps launching buildings.
- **Episodes:**
  - Episode 1: Building ka Size aur Storeroom: Instance Types aur EBS
  - Episode 2: Photograph aur Pakka Address: Snapshot aur Elastic IP
  - Episode 3: Model Hotel: Custom AMI
  - Episode 4: Shaadi ka Season: Launch Template aur Auto Scaling Group

---

# 📺 EPISODE 1: Building ka Size aur Storeroom

### [00:00 – 01:35] Scene 1: Galat Size ki Building
**[VISUAL: Two buildings on the Atithi plot. A tiny hut with a wedding banner, guests spilling onto the road (undersized, slow site). A giant tower hosting one lonely guest, with a huge rent bill (oversized).]**

**(Voiceover):**
Pichhle session mein Atithi ko landlord se pehli building mili aur booking page chalu hua. Par building ka size kaise chuna? Chhoti li to shaadi ke din site dheemi. Badi li to har mahine bahut kiraya, aur guest sirf ek. Size sahi chunna ek hunar hai. Aur size ke saath ek doosra sawaal: data kahan rakhein, kitna, aur building jaaye to data bache ya nahi. Aaj hum dono samajhte hain: building ke size, aur uska storeroom.

### [01:35 – 04:00] Scene 2: Building ki Families
**[VISUAL: A catalogue of building types shown as vehicles: general purpose `t` `m` = sedan; compute `c` = sports car; memory `r` = truck with a huge cargo bed; storage `i` = warehouse van; GPU `g` `p` = rocket. A tag on `t`: "burstable: cheap, fast in bursts".]**

**(Voiceover):**
Session 8 mein humne `t3.micro` ka naam ek line mein padha tha. Pehla akshar family batata hai. General purpose, jaise `t` aur `m`, sab kaamon ke liye. Compute optimised, `c`, jab CPU ka kaam zyada ho. Memory optimised, `r`, jab bahut RAM chahiye, jaise ek bade in-memory cache ke liye. Storage optimised, `i`, bahut tez local storage ke liye. Aur `g` aur `p` GPU wali families hain, jo machine learning ke liye hain. `t` family sasti hoti hai, aur jab kabhi tez kaam aaye to kuch der ke liye bhaagti hai. Chhote web apps ke liye wo achhi hai. Rule: pehle chhoti lo, monitor karo, aur zaroorat ho to badhao. Size badalne ke liye building ko stop karna padta hai.

### [04:00 – 06:40] Scene 3: Storeroom: EBS aur Instance Store
**[VISUAL: A building with an external storeroom labelled EBS bolted on by a corridor, in the same tower (AZ). A second storeroom welded into the building wall: "instance store", with a warning "gone when the building stops". A catalogue of EBS types: `gp3` SSD (default), `io2` fast SSD for databases, `st1` and `sc1` cheap HDD for big sequential data.]**

**(Voiceover):**
Building ke saath do tarah ka storeroom ho sakta hai. EBS, Elastic Block Store, ek alag storeroom hai jo network se juda hai. Building terminate ho jaye, tab bhi uska data bach sakta hai, aur use kisi doosri building mein laga sakte ho, par usi tower, yaani usi AZ mein. Dusra instance store hai, jo building ki deewar mein hi jada hua local storage hai. Building stop ya terminate hui, to uska data gaya. Kaam ka data kabhi instance store par mat rakho. EBS ke prakaar: `gp3` aam general-purpose SSD, aam taur par pehli pasand. `io2` bahut tez, database ke liye. Aur `st1` aur `sc1` sasti HDD, bade sequential data ke liye. Ek yaad: EBS volume ka sirf size nahi, speed ka bhi paisa lagta hai, isliye zaroorat se zyada mat maango.

### [06:40 – 09:15] Scene 4: Storeroom ko Kamre mein Badalna: Session 05B ki Yaad
**[VISUAL: A side-by-side. Left: the three steps from Session 05B in a row: walls (partition), shelves (file system), door from the corridor (mount). Right: the same three steps on the cloud volume `/dev/nvme1n1`, but the first step is greyed: "whole disk used as one hall". A line below: `/etc/fstab` with `UUID=... /data ext4 defaults,nofail 0 2`.]**

**(Voiceover):**
Jo Session 5B mein bhaari mehnat se seekha tha, wo yahan ek kaam ki cheez bana. Naya EBS volume bhi shuru mein khaali floor hai. `lsblk` se dekho, wo `nvme1n1` jaisa dikhega. Cloud par aap aksar poori disk ko bina deewar ke ek hi hall banate ho, to partition ka kadam chhod dete ho. Seedha `mkfs`, phir mount. Aur wahi `/etc/fstab` wali subah ki list: `UUID=... /data ext4 defaults,nofail 0 2`. Yahan ek chhota lafz `nofail` naya hai. Cloud mein volume kabhi kabhi jud hi nahi paata, aur bina `nofail` ke building boot hi nahi hoti. `nofail` kehta hai: ye darwaza na khule to bhi baaki building khol do. LVM bhi yahan chalta hai, par EBS ki apni lacheelapan ke saath, jo hum aage dekhenge.

### [09:15 – 12:10] Scene 5: Sahi Size ka Saboot: CloudWatch aur Right-Sizing
**[VISUAL: A CloudWatch panel for one building: CPU utilization at 8 percent for two weeks, a note "over-sized?". A second panel for a `t3` building: CPU credit balance hitting zero, "throttled". A card for the optimizer service that suggests a size. A small EBS card: `gp2` vs `gp3` with a note "gp3 is usually cheaper at the same size".]**

**(Voiceover):**
Size sahi hai ya nahi, ye anumaan se nahi, meter se pata chalta hai. CloudWatch ek building ka CPU, network aur disk ka graph dikhata hai. Do hafte se CPU aath percent par chal raha hai? To building shayad bahut badi hai. Aur `t` family ki building ke liye ek aur meter: CPU credit balance. `t` family kam kaam mein credits jodti hai aur tez kaam mein kharch karti hai. Credits zero ho gaye to building dheemi kar di jaati hai, aur site bina kisi error ke sust ho jaati hai. Ye ek aam raaz hai ki "site slow kyun" ka jawab. AWS ek optimizer service bhi deti hai jo meter dekh kar size ka sujhav deti hai. Storeroom par bhi yahi soch lagao: purana `gp2` type aksar usi size ke liye `gp3` se mehnga padta hai, isliye naye volume `gp3` lo.

### [12:10 – 14:45] Scene 6: Lab: Volume Lagao, Format Karo, Mount Karo
**[VISUAL: Console: Create volume 8 GB `gp3` in the same AZ as the building, then Actions → Attach volume. Terminal: `lsblk`, `sudo blkid /dev/nvme1n1` (empty), `sudo mkfs -t ext4 /dev/nvme1n1`, `sudo mkdir /data`, `sudo mount /dev/nvme1n1 /data`, `df -h /data`, `sudo blkid` for the UUID, the fstab line, `sudo umount /data`, `sudo mount -a`.]**

**(Voiceover):**
Lab. Building ke tower mein ek 8 GB `gp3` volume banao. Same AZ ka dhyaan rakho, warna attach hi nahi hoga. Phir Actions, Attach volume. SSH karke `lsblk` chalao, naya device dikhega, jaise `nvme1n1`. Pehle `sudo blkid /dev/nvme1n1` chalao: khaali aaya to disk saaf hai. Tabhi `sudo mkfs -t ext4 /dev/nvme1n1`. Ye command us device ka sab kuch mita deti hai, isliye naam do baar padho. Phir `sudo mkdir /data` aur `sudo mount /dev/nvme1n1 /data`. `df -h /data` mein ab alag disk hai. Ab pakka karo: `sudo blkid` se UUID nikalo, `/etc/fstab` mein `nofail` ke saath line jodo, `sudo umount /data`, aur `sudo mount -a`. Agar ye chal gaya to reboot par bhi chalega. Amazon Linux mein default file system `xfs` hota hai, wahi commands, bas `mkfs.xfs`.

### [14:45 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "t m c r i g families · EBS persists, same AZ · gp3 default · mkfs → mount → fstab with nofail".]**

**(Voiceover):**
Recap: building ke size, EBS aur instance store, aur Session 5B ke commands cloud volume par. Ab do sawaal: storeroom ka data kharab ho jaye to? Aur building ka address baar baar kyun badalta hai? Agle episode mein.

---

# 📺 EPISODE 2: Photograph aur Pakka Address

### [00:00 – 01:30] Scene 1: Storeroom Kharab, Data Gaya
**[VISUAL: A storeroom cracks and its shelves collapse. In a vault, a dated photograph of its contents. A new storeroom appears with the photograph's contents restored.]**

**(Voiceover):**
Disk kharab hona, galti se delete ho jana, ya kisi hamle mein data kho jana, sabse bura sapna hai. Iska ilaaj backup hai. AWS mein EBS volume ki backup ko snapshot kehte hain, yaani storeroom ki photograph. Aaj hum photographs lena aur unse storeroom wapas banana seekhte hain. Aur ek chhoti, par sabko tang karne wali cheez, building ka address.

### [01:30 – 04:50] Scene 2: Photograph Kaam Kaise Karti Hai
**[VISUAL: A timeline of three photographs. Photo 1: the whole storeroom. Photo 2: only what changed since Photo 1. Photo 3: only what changed since Photo 2. They live in the landlord's own vault. Arrows: new storeroom in another tower; copy to another city.]**

**(Voiceover):**
Snapshot storeroom ki ek point-in-time copy hai, jo landlord ki apni vault mein rehti hai. Pehli photograph poora storeroom copy karti hai. Uske baad ki sirf wahi cheezein rakhti hain jo badli hain, isliye wo incremental hain aur sasti padti hain. Photograph se naya storeroom kisi bhi tower mein banaya ja sakta hai, aur use doosre shehar, yaani Region, mein copy bhi kiya ja sakta hai, disaster recovery ke liye. Ek chhoti baat: photograph se banaya volume pehli baar kuch dheema padh sakta hai, kyunki uska data piche se laya ja raha hota hai. Aur snapshot ko encrypt karna ho to volume pehle se encrypted rakho. Regular photographs lene ke liye har baar haath se click nahi karte: Data Lifecycle Manager ya AWS Backup unhe timetable par chalate hain, bilkul cron ki tarah.

### [04:50 – 08:00] Scene 3: Building ka Address: Private, Public aur Elastic IP
**[VISUAL: A building with a private address plate (10.x.x.x, only inside the campus) and a public plate that changes after stop and start. A third plate: "Elastic IP", an engraved permanent address that can be moved from one building to another. A bill meter ticking for an unattached one.]**

**(Voiceover):**
Har building ko ek private address milta hai, jo campus ke andar kaam karta hai. Aur internet ke liye ek public address, jo stop aur start ke baad badal sakta hai. Agar address pakka chahiye to Elastic IP: ek permanent address jo aapke account ka hai, aur jise aap ek building se doosri par bhej sakte ho. Khaaskar jab building badalni ho aur address wahi rakhna ho. Par dhyaan: jo Elastic IP kisi se juda nahi hota, usse bhi paise lagte hain, aur ab public IPv4 par aam taur par charge lagta hai. Aur asli production mein aap seedha IP par bharosa nahi karte. Aap ek naam par bharosa karte ho, DNS, aur uske peeche ek load balancer. Wo sab hum agle session mein dekhenge.

### [08:00 – 10:55] Scene 4: Storeroom Bada Karna, Bina Building Roke
**[VISUAL: Console: Modify volume → size 8 GB to 12 GB. Terminal: `lsblk` shows `nvme1n1` at 12G while `df -h /data` still shows 8G, then `sudo resize2fs /dev/nvme1n1` and `df -h /data` shows 12G. For an xfs volume: `sudo xfs_growfs /data`. A caution: "can grow, not shrink; wait before the next change".]**

**(Voiceover):**
Session 5B mein LVM se hall bada karne ki baat hui thi. EBS ki apni ek taakat hai: volume ko bina building roke bada kiya ja sakta hai. Console mein volume chuno, Modify volume, aur size 8 se 12 GB. Par ye sirf storeroom bada karta hai, shelves nahi. `lsblk` mein 12G dikhega, par `df -h /data` ab bhi 8G. Wahi sabak jo LVM mein tha: pehle volume, phir file system. ext4 par `sudo resize2fs /dev/nvme1n1`, xfs par `sudo xfs_growfs /data`. Do seemaayein yaad rakho. Volume sirf badhta hai, ghatta nahi, aur ek badlaav ke baad doosre ke liye kuch ghante rukna padta hai. Isliye size ka andaaza lagakar, thoda bada lo, par bahut bada nahi.

### [10:55 – 13:30] Scene 5: Lab: Photograph se Restore
**[VISUAL: Terminal: `echo "important" | sudo tee /data/note.txt`. Console: Create snapshot of the volume, wait until Completed. Create a new volume from the snapshot, attach it, then `sudo mkdir /restore`, `sudo mount /dev/nvme2n1 /restore`, `cat /restore/note.txt`. Then delete the extra volume and the snapshot.]**

**(Voiceover):**
Lab. `/data` mein ek file banao: `echo "important" | sudo tee /data/note.txt`. Volume ka snapshot lo aur uske `Completed` hone ka intezaar karo. Snapshot se ek naya volume banao, usi tower mein, building se attach karo, aur `sudo mkdir /restore`, `sudo mount /dev/nvme2n1 /restore`. Device ka naam `lsblk` se dekhna, ye aapke setup mein alag ho sakta hai. `cat /restore/note.txt`: file wapas aa gayi. Ye aapka restore test hai. Asli backup wahi hota hai jiska restore test kiya gaya ho. Aur ab safai: extra volume detach karke delete karo, photograph delete karo, fstab ki wo line bhi hatao jo ab kisi kaam ki nahi.

### [13:30 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "snapshot = incremental photograph · test the restore · resize volume then file system · Elastic IP costs when idle".]**

**(Voiceover):**
Recap: photograph, restore test, volume bada karna, aur address ke prakaar. Ab ek badi soch: agar aapko ek jaisi building baar baar chahiye, to? Furnished model hotel, yaani custom AMI.

---

# 📺 EPISODE 3: Model Hotel

### [00:00 – 02:05] Scene 1: Bees Buildings, Ek Jaisa Setup
**[VISUAL: A cook preparing the same dish 20 times by hand, slowly, with small differences each time, while a factory mould stamps 20 identical items in one go. Over the cook: a pile of "nginx, app, agent" install notes.]**

**(Voiceover):**
Maan lo Atithi ko shaadi ke season ke liye bees ek jaisi buildings chahiye: wahi OS, wahi nginx, wahi booking page, wahi monitoring agent. Har ek mein haath se install karoge? Nahi. Ek building ko ek baar poori tarah taiyaar karo, uski ek furnished model hotel jaisi copy rakho, aur us copy se jitni chahiye utni buildings kholo. Wo copy AMI hai. Aur yahi wo rule hai jo Session 0 mein bataya tha: is duniya mein buildings ko photocopy kiya ja sakta hai.

### [02:05 – 05:05] Scene 2: AMI Andar se
**[VISUAL: An AMI box opened to show: a snapshot of the root storeroom, launch permissions, and a device map (which storerooms to attach). An arrow "Launch" produces a running building. Below, a world map with a "copy to another Region" arrow.]**

**(Voiceover):**
AMI ke andar teen cheezein hoti hain: building ke root storeroom ka snapshot, launch permissions, aur ek naksha ki kaun si disk kahan lagegi. Aap landlord ke diye hue AMI se shuru kar sakte ho, jaise Ubuntu ya Amazon Linux. Ya apna AMI bana sakte ho, jisme aapka software pehle se laga ho. Fayda: building jaldi chalu hoti hai aur har baar ek jaisi. Nuksaan: AMI purana ho sakta hai. Security patch ke saath use dobara banana padta hai. Aur AMI Region ke andar hota hai, doosre shehar mein use copy karna padta hai. AMI kisi doosre account ke saath share bhi ho sakta hai, par kuch bhi share karne se pehle uske andar ke secrets zaroor dekh lo.

### [05:05 – 07:45] Scene 3: Model Hotel vs User Data
**[VISUAL: A balance scale. Left: "Golden AMI: everything baked in, fast start, must rebuild for every change". Right: "Base AMI + user data: flexible, installs on every start, slower". A middle path drawn on the scale's beam: "bake the slow and stable, configure the fast-changing at start".]**

**(Voiceover):**
Do raaste hain. Golden image: sab kuch AMI mein pehle se, building turant taiyaar, par har badlaav par naya AMI. Ya base AMI aur user data: lacheela, par har building ke start par install hone mein samay lagta hai. Sabse achha beech ka raasta: jo cheez dheere install hoti hai aur kam badalti hai, jaise runtime ya monitoring agent, use AMI mein pakao. Jo cheez roz badalti hai, jaise booking site ka naya version ya settings, use start par ya deploy ke waqt lagao. Aage hum ye kaam automate karna seekhenge, jaise Jenkins ke pipeline se naya AMI banana, ya Docker se poora kaam badal dena.

### [07:45 – 10:30] Scene 4: Gandi Photocopy se Bacho
**[VISUAL: A model hotel being checked before copying: bash history cleared, `/home/ubuntu/.ssh/authorized_keys` reviewed, a stray `.env` removed, log files rotated and emptied. A note on the Create image dialog: "No reboot" option.]**

**(Voiceover):**
Photocopy banane se pehle model hotel ko saaf karo, warna jo bhi usme hai, wo har building mein jayega. Dekho: koi `.env` ya password wali file to nahi? Bash history mein koi secret to nahi? Kisi ki SSH key `authorized_keys` mein to nahi chhut gayi? Logs bhare hue to nahi? Image banate waqt console ek option deta hai: reboot na karna. Default mein building ek baar band hoti hai, taaki file system ek jaisi halat mein photocopy ho. No reboot se downtime nahi, par data adhura ho sakta hai. Production ke liye aksar ek alag build ki building se AMI banta hai, jise baad mein hata diya jaata hai.

### [10:30 – 13:15] Scene 5: Lab: Apna Model Hotel Banao
**[VISUAL: A running building with nginx and the booking page. Console: Actions → Image and templates → Create image, name `atithi-web-v1`. When "available", Launch instance from "My AMIs" with no user data. The browser shows the Atithi page already there. Then Deregister AMI and Delete snapshot.]**

**(Voiceover):**
Lab. Ek building par nginx lagao aur `/var/www/html/index.html` mein Atithi ka booking page rakho. Building chuno, Actions, Image and templates, Create image, naam `atithi-web-v1`. Kuch minute mein AMI taiyaar. Ab "My AMIs" se ek nayi building launch karo, user data bilkul khaali. Browser mein uska public address kholo: Atithi ka page pehle se chalu hai. Ab dhyaan: kaam ke baad AMI ko Deregister karo, aur uske peeche bana snapshot alag se Delete karo. Deregister se snapshot apne aap nahi jaata, aur wahi storage ka kiraya chalta rehta hai. Aur ek aadat: AMI ke naam mein version rakho, jaise `-v1`, taaki baad mein pata rahe kaun sa kab ka hai.

### [13:15 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "AMI = model hotel · bake slow, configure fast · clean before copying · deregister + delete snapshot".]**

**(Voiceover):**
Recap: AMI, golden image aur user data ka santulan, saaf photocopy aur safai. Ab asli sawaal: shaadi ke season mein buildings ek se zyada kaise chalayein, aur wo apne aap kaise khulein aur band hon? Auto Scaling.

---

# 📺 EPISODE 4: Shaadi ka Season

### [00:00 – 01:20] Scene 1: Sale ka Din, Phir
**[VISUAL: The traffic graph from Session 1 returns, a spike at the wedding-season weekend. This time, new buildings rise on the plot as the line rises, and demolish themselves as it falls. A guest never sees a "we are full" sign.]**

**(Voiceover):**
Hum Session 1 ki sale wali kahani par wapas aate hain. Is baar Atithi ke saamne shaadi ka season hai. Traffic badhta hai, aur nayi buildings apne aap khulti jaati hain. Traffic girta hai, aur wo apne aap band ho jaati hain. Is jaadu ka naam Auto Scaling hai. Isse pehle ek zaroori sawaal: scale karna kya hota hai?

### [01:20 – 03:45] Scene 2: Vertical vs Horizontal Scaling
**[VISUAL: Left: one building growing taller, with a ceiling and a lock "needs a restart". Right: identical buildings multiplying side by side, with a note "stateless, one can fail".]**

**(Voiceover):**
Vertical scaling: ek hi building ko bada karna, yaani zyada CPU, zyada RAM. Isme ek seema hoti hai, aur aksar building ko restart karna padta hai. Horizontal scaling: zyada buildings jodna. Isme seema kam hai, aur ek building girne par baaki chalti rehti hain. Par app ko is tarah banana padta hai ki wo kisi ek building par apni kahani na rakhe, yaani state na rakhe. Booking ka data database mein, photos bucket mein, aur building mein sirf kaam. Cloud ka sabse mazboot raasta horizontal scaling hai, aur Auto Scaling Group uska automation hai. Vertical bhi kabhi kabhi theek hai, jaise ek database ke liye.

### [03:45 – 06:25] Scene 3: Launch Template aur Auto Scaling Group
**[VISUAL: A launch template card: AMI `atithi-web-v1`, type `t3.micro`, key pair, security group, user data, IAM role. An ASG card: min 2, desired 2, max 6, subnets in two towers, a scaling policy "CPU around 50%". A dial shows desired capacity moving between min and max.]**

**(Voiceover):**
Launch template ek nuskha hai: kaun sa AMI, kaun sa size, kaun si chaabi, kaun sa door guard, kaun sa duty badge, user data. Auto Scaling Group, yaani ASG, isi nuske se buildings banata hai. Aap teen number batate ho: minimum, desired aur maximum. Minimum se kam kabhi nahi, maximum se zyada kabhi nahi, aur desired abhi ka lakshya. Do ya zyada towers ke subnets do, taaki ek tower girne par bhi kaam chale. Sabse saral scaling policy target tracking hai: jaise "average CPU 50% ke aas paas rakho", aur ASG khud buildings jodta aur hatata hai. Aur agar koi building unhealthy ho jaye, to ASG use hata kar nayi bana deta hai. Ye self-healing hai.

### [06:25 – 09:10] Scene 4: Season Pehle se Pata Hai To Pehle se Taiyari
**[VISUAL: A calendar with a wedding weekend circled. Three ASG policy cards: target tracking (react), scheduled scaling (be ready before Friday evening), warm-up time (a new building is not counted for a few minutes). A graph showing scale-out in minutes and scale-in more slowly.]**

**(Voiceover):**
Target tracking tab chalta hai jab traffic aa chuka ho. Par Atithi ko shaadi ka weekend pehle se pata hai. Isliye ek aur tareeka hai: scheduled scaling, jisme aap kehte ho "shukravaar shaam se pehle minimum chaar kar do, aur somvaar ko wapas do". Dono ek saath chalte hain, ek pehle se taiyaar, doosra surprise ke liye. Do chhoti baatein jo pareshan karti hain. Ek, nayi building ko chalu hone aur page serve karne mein samay lagta hai. Isliye warm-up time dena padta hai, taaki wo tab tak CPU ke hisaab mein na ginay. Do, scale-out jaldi hota hai, par scale-in dheere, kyunki wapas kam karne mein jaldi karna khatarnaak hai. Isliye dashboard par buildings turant kam hoti nahi dikhengi.

### [09:10 – 12:15] Scene 5: Naya Model Hotel Sab Buildings tak: Instance Refresh
**[VISUAL: A launch template with version 1 (`atithi-web-v1`) and a new version 2 (`atithi-web-v2`). An ASG panel: Instance refresh, minimum healthy 90 percent, warm-up 300 seconds. Four buildings are swapped for new ones two at a time, never all together, while the marshal keeps sending guests to the rest.]**

**(Voiceover):**
Ab ek sawaal jo asli kaam mein roz aata hai: booking page ka naya version aaya, naya AMI bana. Ab bees chalti buildings ko kaise badlein? Launch template ka naya version banao, jisme naya AMI ho. Phir ASG mein Instance refresh chalao. Wo purani buildings ko kuch-kuch karke naye se badalta hai, aur aap batate ho ki kam se kam kitne percent buildings hamesha healthy rahen, jaise nabbe, aur nayi building ko kitna warm-up samay milega. Isse guests ko kabhi poori site band nahi dikhti. Ye wahi cheez hai jo hum aage rolling update ke naam se Kubernetes mein dobara dekhenge. Par yaad rakho, agar naya AMI kharab hai, to refresh usse saari buildings tak le jaayega. Isliye pehle ek building par test karo, ya refresh mein health check rakho jo galti par ruk jaaye.

### [12:15 – 14:40] Scene 6: Lab: ASG aur Load Test
**[VISUAL: Create a launch template using `atithi-web-v1`. Create an ASG across two subnets in two towers with min 1, max 3, target tracking CPU 40%. On a building: `sudo apt install -y stress`, `stress --cpu 2 --timeout 600`. The Activity tab shows "Launching a new EC2 instance". Finally, set desired and minimum to 0 and delete the ASG.]**

**(Voiceover):**
Lab. `atithi-web-v1` AMI se ek launch template banao. Phir ek Auto Scaling Group: do alag towers ke subnets, minimum 1, maximum 3, aur target tracking CPU 40%. Ek building mein SSH karo, `sudo apt install -y stress` aur `stress --cpu 2 --timeout 600`. Ab Activity tab dekho. Jab CPU kuch minute tak 40% se upar rahega, to ek naya "Launching a new EC2 instance" dikhega. CPU ka graph Monitoring tab mein dekho. Aakhir mein ASG ke desired aur minimum ko 0 karo aur ASG delete karo, aur AMI aur uska snapshot bhi. Nahi to ASG building banata hi rahega, aur aapka kiraya chalta rahega.

### [14:40 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "launch template + ASG · min / desired / max · target tracking + scheduled · warm-up · multi-tower · self-healing".]**

**(Voiceover):**
Recap: vertical aur horizontal scaling, launch template, ASG, aur season ke liye scheduled scaling. Par ek sawaal bacha hai: jab buildings kai hon, to guest kis building par jayega? Jawab: gate ka marshal, yaani load balancer. Agle session mein.

---

# 📎 Student handout: Session 10 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Kaam | Command ya yaad rakho |
|---|---|
| Disk dekhna | `lsblk`, `sudo blkid /dev/nvme1n1`, `df -h` |
| Volume format aur mount | `sudo mkfs -t ext4 /dev/nvme1n1`, `sudo mount /dev/nvme1n1 /data` |
| Pakka mount | `/etc/fstab`: `UUID=<uuid> /data ext4 defaults,nofail 0 2`; test `sudo mount -a` |
| Volume bada karna | Console Modify volume; phir `sudo resize2fs /dev/nvme1n1` (ext4) ya `sudo xfs_growfs /data` (xfs) |
| EBS | Alag storeroom; usi AZ mein; gp3 default; sirf badhta hai |
| Instance store | Building ke saath; stop par data gaya |
| Snapshot | Incremental; restore test zaroori; DLM ya AWS Backup se timetable |
| Elastic IP | Pakka public address; juda na ho to bhi kiraya |
| AMI | Model hotel; Region-specific; deregister + snapshot delete |
| Launch template | AMI, type, key, SG, role, user data |
| ASG | min / desired / max; multi-tower; target tracking; scheduled; warm-up |
| Safai | ASG 0 aur delete, AMI, snapshots, volumes, Elastic IP |

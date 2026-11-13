# ✍️ 02: SCRIPT — SESSION-10: EC2 Storage & Scaling
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S10`
- **Focus:** Instance families, EBS volumes & snapshots, Elastic IP, AMIs, vertical vs horizontal scaling, launch templates & Auto Scaling Groups
- **Episodes:**
  - Episode 1: Instance Types aur EBS: Server ka Dimaag aur Disk
  - Episode 2: Snapshots, Elastic IP aur Backup ki Soch
  - Episode 3: Custom AMI: Ek Baar Banao, Baar Baar Chalao
  - Episode 4: Scaling: Launch Template aur Auto Scaling Group

---

# 📺 EPISODE 1: Instance Types aur EBS

### [00:00 – 01:15] Scene 1: Galat Size ka Server
**[VISUAL: A tiny car carrying a truckload (undersized), and a bus carrying one passenger (oversized). Both labelled with bills.]**

**(Voiceover):**
Chhota server liya to app slow. Bada liya to bill bada. Server ka size sahi chunna ek skill hai. Aur uske saath disk ka sawaal: kaun si disk, kitni badi, aur data bachega ya nahi. Aaj hum inhi do cheezon ko samajhte hain.

### [01:15 – 05:00] Scene 2: Instance Families
**[VISUAL: A table of families as vehicle types: General purpose (t, m) = sedan; Compute optimised (c) = sports car; Memory optimised (r) = truck; Storage optimised (i) = warehouse van; GPU (g/p) = rocket.]**

**(Voiceover):**
Instance ke naam ka pehla akshar family batata hai. General purpose, jaise t aur m, sab kaamon ke liye. Compute optimised, jaise c, jab CPU ka kaam zyada ho. Memory optimised, jaise r, jab bahut RAM chahiye, jaise in-memory database. Storage optimised, jaise i, tez local disk ke liye. Aur GPU wali families machine learning ke liye. Burstable t family sasti hoti hai aur kabhi kabhi tez chalti hai, jo chhote web apps ke liye achhi hai. Pehle chhota lo, monitor karo, aur zaroorat ke hisaab se badhao.

### [05:00 – 08:30] Scene 3: EBS: Server ki Alag Disk
**[VISUAL: An EC2 instance with a detachable external disk labelled EBS in the same AZ. Next to it, a "Instance store" disk fused to the machine, with a warning: "Gone when instance stops".]**

**(Voiceover):**
EBS, Elastic Block Store, ek network se judi disk hai. Instance terminate ho jaye, tab bhi EBS volume ka data bach sakta hai, aur use kisi doosre instance par laga sakte ho, par usi AZ mein. Alag se instance store hota hai, jo machine se juda local storage hai, aur instance stop ya terminate hone par data kho deta hai. Kaam ka data kabhi instance store par mat rakho. Volume types mein gp3 general purpose SSD hai aur aam taur par pehli pasand, io2 bahut tez database ke liye, aur st1 aur sc1 sasti HDD hain, bade sequential data ke liye.

### [08:30 – 11:30] Scene 4: Lab: Naya Volume Lagao aur Mount Karo
**[VISUAL: Console: Create volume 8 GB gp3 in the same AZ → Attach to instance. Terminal: `lsblk`, `sudo mkfs -t ext4 /dev/nvme1n1`, `sudo mount /dev/nvme1n1 /data`, `df -h`.]**

**(Voiceover):**
Lab: instance ke AZ mein ek 8 GB gp3 volume banao aur use instance se attach karo. SSH karke `lsblk` chalao, naya device dikhega, jaise `nvme1n1`. Naye volume par pehli baar `sudo mkfs -t ext4 /dev/nvme1n1` se filesystem banao; dhyaan, ye command data mita deti hai, isliye pehle pakka karo ki sahi device hai. Phir `sudo mkdir /data && sudo mount /dev/nvme1n1 /data`, aur `df -h` se check. Ye volume ab aapka alag data disk hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "t/m/c/r/i/g families · EBS persists · gp3 default · same AZ".]**

**(Voiceover):**
Recap: instance families, EBS, volume types. Ab sawaal: ye data backup kaise ho, aur server ka IP bar bar kyun badalta hai? Agle episode mein.

---

# 📺 EPISODE 2: Snapshots, Elastic IP aur Backup ki Soch

### [00:00 – 01:15] Scene 1: Disk Kharab, Data Gaya
**[VISUAL: A volume icon cracks. A snapshot icon in a vault with a clock stamp lights up and a restored volume appears.]**

**(Voiceover):**
Disk kharab hone, galti se delete hone ya ransomware ki wajah se data khona sabse bura sapna hai. Iska ilaaj backup hai, aur AWS mein EBS ke liye backup ko snapshot kehte hain. Aaj hum snapshots aur ek aur chhoti, par sab ko tang karne wali cheez, IP address, dekhte hain.

### [01:15 – 05:00] Scene 2: Snapshot kaise Kaam Karta Hai
**[VISUAL: A timeline: Snapshot 1 (full), Snapshot 2 (only changed blocks), Snapshot 3 (only changed blocks). Stored in S3 (managed by AWS).]**

**(Voiceover):**
Snapshot volume ki ek point-in-time copy hai, jo AWS ke managed storage mein rehti hai. Pehla snapshot poora data copy karta hai, lekin uske baad ke snapshots sirf badle hue blocks save karte hain, isliye wo incremental hote hain aur paisa bachta hai. Snapshot se naya volume bana sakte ho, doosre AZ mein bhi, aur doosre region mein copy bhi kar sakte ho disaster recovery ke liye. Regular snapshots automatically lene ke liye Data Lifecycle Manager ya AWS Backup use hote hain.

### [05:00 – 08:30] Scene 3: Public, Private aur Elastic IP
**[VISUAL: An instance with a private IP (10.x) and a public IP that changes after stop/start; an Elastic IP as a fixed "phone number" re-pointed from one instance to another.]**

**(Voiceover):**
Instance ko private IP milta hai, jo VPC ke andar kaam karta hai. Public IP internet ke liye hota hai, aur stop-start par badal sakta hai. Agar ek fixed address chahiye to Elastic IP, jo ek sthayi public IP hai jise aap kisi instance se jod sakte ho aur zarurat padne par dusre instance par shift kar sakte ho. Par dhyaan: jo Elastic IP kisi se juda nahi hota, uska paisa lagta hai, aur public IPv4 ab AWS mein generally charge hota hai. Aur asli production mein aap sidhe IP ki jagah DNS aur load balancer par bharosa karte ho.

### [08:30 – 11:30] Scene 4: Lab: Snapshot se Restore
**[VISUAL: Create files on `/data`. Console: Snapshot the volume. Create a new volume from the snapshot, attach it, mount it on `/restore`, `ls` shows the files.]**

**(Voiceover):**
Lab: `/data` mein kuch files banao, jaise `echo important > /data/note.txt`. Volume ka snapshot lo. Snapshot se ek naya volume banao, instance par attach karo, aur `sudo mount /dev/nvme2n1 /restore` jaisa kuch karke dekho ki `note.txt` wapas aa gayi. Ye aapka restore test hai. Asli backup wahi hota hai jiska restore test kiya gaya ho. Kaam khatam hone par extra volumes aur snapshots hata do.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Snapshot = incremental backup · test restore · Elastic IP costs if idle".]**

**(Voiceover):**
Recap: snapshots, restore, aur IP ke types. Ab ek badi soch: agar server bahut baar ek jaisa banana ho, to? Custom AMI.

---

# 📺 EPISODE 3: Custom AMI

### [00:00 – 01:15] Scene 1: 20 Server, Ek Jaisa Setup
**[VISUAL: A cook preparing the same recipe 20 times by hand versus a factory mould producing 20 identical items.]**

**(Voiceover):**
Agar aapko ek jaisa setup 20 servers par chahiye: OS, nginx, aapki app, monitoring agent. Har ek par haath se install karoge? Nahi. Ek server ko ek baar taiyaar karo, uska template bana lo, aur us template se jitne chahiye utne servers launch karo. Wo template AMI hai.

### [01:15 – 05:00] Scene 2: AMI kya Hai
**[VISUAL: An AMI "box" containing: root volume snapshot, launch permissions, block device mapping. An arrow shows "Launch → new instance".]**

**(Voiceover):**
AMI mein root volume ka snapshot, launch permissions aur disk mapping hoti hai. Aap AWS ke diye hue AMI se shuru kar sakte ho, jaise Ubuntu ya Amazon Linux. Ya aap apna custom AMI bana sakte ho, jisme aapka software pehle se installed ho. Fayda: server jaldi start hota hai aur har bar ek jaisa banta hai. Nuksaan: AMI purana ho sakta hai, to security patch ke saath use regularly naye sire se banana padta hai. Aur AMI region-specific hota hai; doosre region ke liye use copy karna padta hai.

### [05:00 – 08:30] Scene 3: Golden Image vs User Data
**[VISUAL: A balance scale: "Golden AMI: fast boot, consistent, but must rebuild" vs "Base AMI + user data: flexible, slower boot". A middle path: "Bake slow stuff, configure fast stuff".]**

**(Voiceover):**
Do approach hain. Golden image: sab kuch AMI mein pehle se. Fast boot, par har change par naya AMI. Ya base AMI aur user data: flexible, par boot par install hone mein samay lagta hai. Beech ka rasta sabse achha: jo cheez dheere install hoti hai aur kam badalti hai, jaise runtime ya agent, use AMI mein pakao. Jo cheez roz badalti hai, jaise app version ya config, use boot par ya deploy ke time par laga do. Aage hum is kaam ko automate karna seekhenge.

### [08:30 – 11:30] Scene 4: Lab: Apna AMI Banao
**[VISUAL: A running instance with nginx and a custom index page. Console: Actions → Image and templates → Create image. After available, launch a new instance from "My AMIs"; the page is already there.]**

**(Voiceover):**
Lab: ek instance par nginx install karo aur ek custom `index.html` rakho. Instance select karke Actions, Image and templates, Create image. Kuch minute mein AMI taiyaar hota hai. Ab "My AMIs" se us AMI ka ek naya instance launch karo, user data ke bina, aur browser mein check karo: aapka page pehle se hi chal raha hai. Kaam ke baad AMI ko deregister karo aur uske snapshot bhi hatao, nahi to storage ka paisa lagta rehta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "AMI = template · bake slow, configure fast · rebuild for patches".]**

**(Voiceover):**
Recap: AMI, golden image aur user data ka balance. Ab asli sawaal: traffic badhe to servers ek se zyada kaise chalayein? Auto Scaling.

---

# 📺 EPISODE 4: Scaling — Launch Template aur Auto Scaling Group

### [00:00 – 01:15] Scene 1: Sale ka Din, Phir
**[VISUAL: The sale-day graph from Session 1 returns. This time, new server icons pop up automatically as the line rises, then retire as it falls.]**

**(Voiceover):**
Hum Session 1 ki sale wali kahani par wapas aate hain. Isbaar traffic badhta hai aur nayi servers apne aap aa jaati hain, aur traffic girne par chali bhi jaati hain. Is jaadu ka naam Auto Scaling hai. Isse pehle ek zaroori sawaal: scale ka matlab kya?

### [01:15 – 05:00] Scene 2: Vertical vs Horizontal Scaling
**[VISUAL: Left: one server growing taller (more CPU/RAM) = vertical, with a ceiling and a restart. Right: servers multiplying side by side = horizontal.]**

**(Voiceover):**
Vertical scaling matlab ek hi server ko bada karna: zyada CPU, zyada RAM. Isme ek limit hoti hai aur aksar restart chahiye. Horizontal scaling matlab zyada servers jodna. Isme limit kam hai aur ek server girne par baaki chalte hain, par app ko aise design karna padta hai ki wo kisi ek server par state na rakhe. Cloud ka sabse mazbut rasta horizontal scaling hi hai, aur Auto Scaling Group uska automation hai.

### [05:00 – 08:30] Scene 3: Launch Template aur Auto Scaling Group
**[VISUAL: A launch template card: AMI, type, key, SG, user data. An ASG card: min 2, desired 2, max 6, subnets in 2 AZs, scaling policy "CPU 50%".]**

**(Voiceover):**
Launch template ek nuskha hai: kaun sa AMI, kaun sa instance type, security group, user data. Auto Scaling Group isi nuskhe se instances banata hai. Aap batate ho minimum, desired aur maximum kitne. Aur do ya zyada AZ ke subnets, taaki ek AZ girne par bhi chale. Scaling policy sabse saral: target tracking, jaise "average CPU 50% ke aas paas rakho", aur ASG khud servers jodta aur hatata hai. Agar koi instance unhealthy ho jaye, ASG use badalkar naya bana deta hai, yaani self-healing.

### [08:30 – 11:30] Scene 4: Lab: ASG aur Load Test
**[VISUAL: Create a launch template, then an ASG across two AZs with min 1/max 3 and CPU target 40%. A terminal runs `stress` on one instance; the activity tab shows a new instance launching.]**

**(Voiceover):**
Lab: ek launch template banao, jisme aapka custom AMI ho. Phir Auto Scaling Group banao, do AZ ke subnets, minimum 1, maximum 3, aur target tracking CPU 40%. Ek instance mein SSH karke `sudo apt install -y stress` aur `stress --cpu 2 --timeout 300` chalao. Kuch minute mein ASG ke Activity tab mein dekhoge ki naya instance launch hua. Lab khatam hone par ASG delete karna na bhoolo, nahi to wo instances banata rahega.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Launch template + ASG · min/desired/max · target tracking · multi-AZ · self-healing".]**

**(Voiceover):**
Recap: vertical vs horizontal, launch template, ASG. Lekin ek sawaal bacha hai: jab kai servers hon, to user kis server par jayega? Jawab: load balancer, agle session mein.

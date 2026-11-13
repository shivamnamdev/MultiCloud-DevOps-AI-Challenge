# ✍️ 02: SCRIPT — SESSION-12: Amazon S3
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S12`
- **Focus:** Object storage concepts, storage classes & lifecycle, versioning, bucket policies & Block Public Access, static website + CloudFront
- **Episodes:**
  - Episode 1: S3 kya hai: Bucket, Object aur Key
  - Episode 2: Storage Classes, Lifecycle aur Versioning
  - Episode 3: Access Control: Public Leak kaise Hota Hai
  - Episode 4: Static Website aur CloudFront

---

# 📺 EPISODE 1: S3 kya hai?

### [00:00 – 01:15] Scene 1: Almari ya Godaam?
**[VISUAL: A small cupboard labelled "EBS/Disk" filling up, and a limitless warehouse with labelled boxes labelled "S3". Boxes retrieved by label.]**

**(Voiceover):**
Disk ek almari ki tarah hai: ek server se juda, limited jagah. S3, Simple Storage Service, ek anant godaam hai jahan aap kisi bhi file ko ek label ke saath rakh sakte ho, internet se kahin se bhi nikaal sakte ho. Photos, backups, logs, video, data lake, sab S3 mein jaata hai. Aur dekha jaye to aaj ki zyadatar websites ke images S3 par hi hote hain.

### [01:15 – 05:00] Scene 2: Bucket, Object, Key
**[VISUAL: A bucket named `my-company-logs-2026` containing objects. A key `reports/2026/jan/sales.csv` with "folder" slashes shown as part of the name, not real folders.]**

**(Voiceover):**
Bucket ek container hai, jiska naam poori duniya mein unique hona chahiye. Object matlab file plus uska metadata. Har object ki ek key hoti hai, jaise `reports/2026/jan/sales.csv`. Yeh slash asli folder nahi, bas naam ka hissa hai, par console unhe folders ki tarah dikhata hai. S3 file system nahi, object storage hai: aap poora object daalte ho ya padhte ho, uske beech mein edit nahi karte. Ek object ki size kaafi badi ho sakti hai, aur bucket mein objects ki sankhya ki koi practical limit nahi.

### [05:00 – 08:30] Scene 3: Durability aur Consistency
**[VISUAL: An object being copied across three AZ boxes automatically. A label "11 nines of durability" with a caution: "durability ≠ availability ≠ backup".]**

**(Voiceover):**
S3 Standard aapke object ko ek region ke kai AZ mein copy karke rakhta hai, isliye uski durability bahut zyada hai, jise "eleven nines" kaha jata hai. Lekin dhyaan: durability ka matlab ye nahi ki aap galti se delete kar do to wapas aa jayega. Isliye versioning aur backups alag cheezein hain. Aur S3 ab strongly consistent hai: naya object likha to turant padh sakte ho.

### [08:30 – 11:30] Scene 4: Lab: Bucket Banao aur CLI se Upload
**[VISUAL: Console: Create bucket with Block Public Access ON. Terminal: `aws s3 cp hello.txt s3://BUCKET/`, `aws s3 ls s3://BUCKET/`, `aws s3 sync ./site s3://BUCKET/site/`.]**

**(Voiceover):**
Lab: ek bucket banao, naam unique, Block Public Access on rehne do. Terminal mein `echo hi > hello.txt`, phir `aws s3 cp hello.txt s3://YOUR-BUCKET/`, aur `aws s3 ls s3://YOUR-BUCKET/`. Ek folder bhi upload karo `aws s3 sync ./site s3://YOUR-BUCKET/site/`. Sync sirf badle hue files bhejta hai. Console mein jaakar object kholo aur uska URL dekho; wo private hai, to browser mein access denied aayega. Ye galti nahi, yahi sahi default hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Bucket unique name · object = data + metadata · key not folder · private by default".]**

**(Voiceover):**
Recap: bucket, object, key, durability. Ab paise aur safety: storage classes, lifecycle aur versioning.

---

# 📺 EPISODE 2: Storage Classes, Lifecycle aur Versioning

### [00:00 – 01:15] Scene 1: Purane Logs ka Mehnga Bill
**[VISUAL: A bill bar growing each month because three years of logs sit in the expensive class. A hand moves them to a cheaper class and the bar shrinks.]**

**(Voiceover):**
Tin saal purane logs, jo kisi ne nahi dekhe, ek mehnge storage class mein pade hain aur har mahine paisa le rahe hain. S3 mein data ko uske upyog ke hisaab se alag alag classes mein rakha jaa sakta hai, aur ye movement automatic bhi ho sakti hai. Isse bahut bachat hoti hai.

### [01:15 – 05:00] Scene 2: Storage Classes
**[VISUAL: A ladder from "Hot" to "Cold": Standard → Intelligent-Tiering → Standard-IA → One Zone-IA → Glacier Instant/Flexible Retrieval → Glacier Deep Archive. Each rung shows cost and retrieval speed.]**

**(Voiceover):**
Standard roz ke access ke liye. Standard-IA, infrequent access, jisme storage sasta par retrieval ka kuch charge. One Zone-IA sirf ek AZ mein, aur sasta, par us AZ ke girne par data ka risk. Intelligent-Tiering khud access pattern dekhkar data ko upar neeche karta hai. Glacier classes archive ke liye: bahut sasti, par data wapas laane mein minute se lekar ghante lag sakte hain. Seedha rule: jitni kam zaroorat, utna thanda aur sasta storage, aur jitni jaldi zaroorat, utna mehnga.

### [05:00 – 08:30] Scene 3: Lifecycle Rules aur Versioning
**[VISUAL: A lifecycle timeline: Day 0 Standard → Day 30 Standard-IA → Day 90 Glacier → Day 365 Expire. Next, a versioning stack: v3 current, v2, v1, with a delete marker on top.]**

**(Voiceover):**
Lifecycle rule ek automatic nuskha hai: 30 din baad Standard-IA mein, 90 din baad Glacier mein, aur ek saal baad delete. Versioning ek alag suraksha hai: bucket par on karo to har overwrite ya delete ek naya version banata hai. Galti se delete hone par ek delete marker lagta hai, aur purana version wapas mil sakta hai. Dhyaan: versioning on rakhne par purane versions ka bhi paisa lagta hai, isliye lifecycle rule se purane versions bhi expire karne chahiye.

### [08:30 – 11:30] Scene 4: Lab: Versioning aur Lifecycle
**[VISUAL: Enable versioning. Upload `note.txt` twice with different content. Console: "List versions" shows two. Delete → delete marker appears; remove the marker to restore. Then a lifecycle rule creation screen.]**

**(Voiceover):**
Lab: bucket par versioning on karo. `note.txt` upload karo, phir uska content badal kar dobara upload karo. "Show versions" mein do versions dikhenge. File delete karo: console mein file gayab dikhegi par versions mein delete marker hoga. Marker ko hatao to file wapas aa jayegi. Ab Management tab mein ek lifecycle rule banao: 30 din baad Standard-IA mein, aur purane versions 60 din baad expire. Seekha hua: safety aur cost dono lifecycle se sambhalte hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "classes by access · lifecycle rules · versioning = undo · expire old versions".]**

**(Voiceover):**
Recap: storage classes, lifecycle aur versioning. Ab sabse badi galti jo S3 mein hoti hai: galat access aur public leak.

---

# 📺 EPISODE 3: Access Control

### [00:00 – 01:15] Scene 1: Ek Checkbox, Lakhon Records Leak
**[VISUAL: A news-style headline graphic: "Customer data found in open storage bucket". A bucket icon with a open padlock.]**

**(Voiceover):**
Kai badi kaun si data leaks isliye hui kyunki ek bucket galti se public ho gaya tha. Kisi ne hack nahi kiya, sirf ek setting galat thi. Hum aaj dekhenge ki S3 mein access kaise tay hota hai, aur is galti se kaise bachein. Yaad hai Session 1 ka shared responsibility model? Yeh uska seedha udaharan hai.

### [01:15 – 05:00] Scene 2: Access ke Tareeke aur Block Public Access
**[VISUAL: A control stack: Block Public Access (account + bucket level) on top; below it IAM policies, bucket policies, ACLs (legacy), presigned URLs.]**

**(Voiceover):**
S3 mein access kai layers se tay hota hai. Sabse upar Block Public Access, ek safety switch jo account aur bucket dono level par lagta hai, aur bucket ko galti se public hone se rokta hai. Neeche IAM policies jo batati hain user kya kar sakta hai, aur bucket policy jo bucket ke saath judi hoti hai. ACLs purani cheez hain, naye bucket par by default band rehti hain, aur unhe use na karna hi behtar hai. Aur presigned URL ek temporary link hai jo ek khaas object ko kuch der ke liye share karta hai.

### [05:00 – 08:30] Scene 3: Bucket Policy aur Encryption
**[VISUAL: A bucket policy JSON requiring HTTPS: `"Condition": {"Bool": {"aws:SecureTransport": "false"}}` with Effect Deny. Another showing the encryption setting SSE-S3 default, SSE-KMS option.]**

**(Voiceover):**
Bucket policy mein aap rules likhte ho, jaise "sirf HTTPS se access", jiske liye ek Deny statement hota hai jo `aws:SecureTransport` false hone par request roke. Encryption: ab S3 mein naye objects by default server-side encryption se encrypt hote hain, SSE-S3 ke saath. Zyada control chahiye to SSE-KMS, jisme key aur uska audit aap sambhalte ho. Aur access logs aur CloudTrail se pata chalta hai ki kisne kaun sa object access kiya. Sensitive data ke liye ye sab on rakho.

### [08:30 – 11:30] Scene 4: Lab: Presigned URL aur HTTPS-only Policy
**[VISUAL: Terminal: `aws s3 presign s3://BUCKET/hello.txt --expires-in 300` prints a long URL. The URL opens in a browser; after 5 minutes it returns "Request has expired".]**

**(Voiceover):**
Lab: private object ka presigned URL banao: `aws s3 presign s3://YOUR-BUCKET/hello.txt --expires-in 300`. Is lambe link ko browser mein kholo, file dikhegi, bina bucket public kiye. Paanch minute baad wahi link expire ho jayega. Ab bucket policy mein HTTPS-only wala Deny statement lagao, aur check karo ki Block Public Access chaaron options on hain. Ye do cheezein bahut aam leaks se bacha leti hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Block Public Access ON · least privilege · HTTPS-only · encrypt · presigned for sharing".]**

**(Voiceover):**
Recap: access ki layers, Block Public Access, presigned URLs, encryption. Ab ek mazedaar upyog: S3 par poori website host karna, aur CloudFront se use tez aur surakshit banana.

---

# 📺 EPISODE 4: Static Website aur CloudFront

### [00:00 – 01:15] Scene 1: Bina Server ki Website
**[VISUAL: A portfolio website with HTML, CSS, JS files. No server icon, just an S3 bucket serving them to a browser.]**

**(Voiceover):**
Agar aapki website sirf HTML, CSS aur JavaScript hai, to usse chalane ke liye server ki zaroorat nahi. S3 se seedha chal sakti hai: sasti, tez aur server ki chinta ke bina. Resume, portfolio, documentation site, landing page, sab ke liye perfect hai.

### [01:15 – 05:00] Scene 2: S3 Static Hosting aur uski Seema
**[VISUAL: S3 bucket → "Static website hosting" enabled, index.html, error.html. A note: the S3 website endpoint is HTTP-only; custom domain with HTTPS needs CloudFront.]**

**(Voiceover):**
Bucket par static website hosting on karo, index aur error document batao. Lekin dhyaan do: S3 ka website endpoint sirf HTTP deta hai, HTTPS nahi, aur seedha public bucket par chalane ke liye aapko public read dena padta hai, jo security ke hisaab se kamzor tareeka hai. Isliye aaj ka best practice hai ki bucket private rakho aur CloudFront ke through serve karo.

### [05:00 – 08:30] Scene 3: CloudFront: CDN ka Jaadu
**[VISUAL: A world map. Without CDN: every user hits the origin far away. With CDN: users get cached copies from the nearest edge location. HTTPS padlock, custom domain, and a OAC badge tying CloudFront to a private bucket.]**

**(Voiceover):**
CloudFront ek CDN hai, Content Delivery Network. Wo aapki files ki copies duniya bhar ke edge locations par cache karta hai, to user ko data paas se milta hai aur website tez chalti hai. Wo HTTPS aur custom domain bhi deta hai, ACM ke certificate ke saath, jo CloudFront ke liye us-east-1 region mein hona chahiye. Origin Access Control, OAC, se bucket private rehta hai aur sirf CloudFront usse padh sakta hai. DNS ke liye Route 53 mein domain ko CloudFront se jodna padta hai.

### [08:30 – 11:30] Scene 4: Lab: Portfolio Deploy
**[VISUAL: A simple `index.html` with a name and a link. `aws s3 sync . s3://BUCKET --delete`. A CloudFront distribution is created with the bucket as origin and OAC; the CloudFront domain shows the page.]**

**(Voiceover):**
Lab: ek simple `index.html` banao jisme aapka naam aur ek line ho. `aws s3 sync . s3://YOUR-BUCKET --delete` se upload karo. Phir CloudFront distribution banao: origin aapka S3 bucket, OAC on, default root object `index.html`. Console bucket policy ka text dega jo aapko bucket par lagani hai. Distribution deploy hone par `dxxxx.cloudfront.net` kholo. Dhyaan: file badalne par cache ke wajah se purana page dikh sakta hai, to invalidation chalao ya versioned file names use karo. Lab ke baad distribution aur bucket saaf karna.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "private bucket + CloudFront + OAC · HTTPS · cache invalidation".]**

**(Voiceover):**
Recap: S3 ka poora safar, aur ek surakshit, tez website. Ab data ki baat: jab aapko structured data, tables aur transactions chahiye, to S3 nahi, database. Agle session mein RDS.

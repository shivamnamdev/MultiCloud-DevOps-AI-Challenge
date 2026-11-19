# ✍️ 02: SCRIPT — SESSION-13: AWS RDS
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S13`
- **Focus:** Why a database, SQL vs NoSQL, transactions and constraints, what RDS manages and what you manage, instance class, storage, parameter and subnet groups, automated backups and point-in-time recovery, snapshots, Multi-AZ vs read replicas, security (network, encryption, secrets), connection limits, connecting from EC2 and from Python
- **Builds on:** Session 08 (security groups), Session 09 (roles, instance profile), Session 10 (snapshots as photographs), Session 12 (S3 holds photos and PDFs, not bookings)
- **Story position:** Zoom level 2, the rented campus. Landlord ka chalaya hua records office: ek ruled ledger jahan har booking ki ek line hoti hai, raat ko uski copy, aur doosre tower mein ek standby ledger.
- **Story words used:** records office (RDS), ruled ledger (SQL table), loose forms (NoSQL), standby ledger (Multi-AZ), photocopy for reading (read replica), photograph (snapshot), door guard (security group), duty badge (role), sealed envelope (TLS), staff (database users), guest (end user)
- **Lab project:** the Atithi booking ledger: tables `guests`, `rooms` and `bookings` first on a laptop, then on a managed PostgreSQL instance that only the booking building can reach.
- **Cost rule (AWS):** a running database instance is billed by the hour, plus storage and backups. Free-tier terms for new accounts change, so check the live pricing page first. Every lab ends with deleting the instance and the snapshots made for the lab.
- **Episodes:**
  - Episode 1: Records Office kyun: Ledger vs Loose Forms
  - Episode 2: RDS: Landlord Chalaye Records Office
  - Episode 3: Raat ki Copy, Standby Ledger aur Photocopy
  - Episode 4: Ledger ko Surakshit Rakho aur Connect Karo

---

# 📺 EPISODE 1: Records Office kyun

### [00:00 – 02:15] Scene 1: Register Bhar Gaya, Do Log Ek Saath
**[VISUAL: Atithi's front desk with a paper register. Two receptionists write the same room number for two different guests at the same moment; a red "double booking" stamp lands. Then an Excel sheet with five lakh rows freezes.]**

**(Voiceover):**
Atithi ki booking site ab roz saikdon booking leti hai. Shuru mein ek spreadsheet kaafi lagti thi. Ab do problems hain. Do receptionists ek hi kamra do alag guests ko ek saath de dete hain. Aur sheet itni bhaari ho gayi hai ki khulne mein minute lagte hain. Photos aur invoices ka ghar humne pichhle session mein banaya tha, par booking ki jankari box mein nahi rakhi jaa sakti, kyunki usme rishte hote hain: kaun guest, kaun kamra, kaun si date. Ismein ek ruled ledger chahiye, jahan har line ke columns tay hon, aur jahan ek saath likhne wale ek doosre ko galat na kar saken. Isi ka naam database hai.

### [02:15 – 04:35] Scene 2: Ruled Ledger: Tables aur Rishte
**[VISUAL: Three tables drawn as ledger pages: `guests(id, name, phone)`, `rooms(id, number, rate)`, `bookings(id, guest_id, room_id, check_in, check_out)`. Arrows from `guest_id` and `room_id` back to the other tables. A SQL line `SELECT g.name, r.number FROM bookings b JOIN guests g ON ...`.]**

**(Voiceover):**
Relational database data ko tables mein rakhta hai, jinke beech rishte hote hain. Atithi mein teen tables: `guests`, `rooms` aur `bookings`. `bookings` ki har line mein `guest_id` aur `room_id` hota hai, jo doosre tables ki line ki taraf ishaara karta hai. Isse guest ka naam har booking mein dobara nahi likhna padta. Sawaal poochne ki bhasha SQL hai, aur `JOIN` se teeno tables ek saath padhe jaate hain. Har table ki ek primary key hoti hai, jo har line ko akela pehchaanti hai, aur foreign key wo ishaara hai jo bataata hai ki ye line kis doosre table se judi hai. Ye wahi ruled ledger hai: har column ka naam aur type pehle se tay.

### [04:35 – 06:50] Scene 3: ACID: Poora Ya Kuch Nahi
**[VISUAL: A transaction box with two steps: "create booking row" and "mark room as reserved". A power cut after step 1 shows both rolled back, with the label ROLLBACK. Four letters appear one by one: Atomicity, Consistency, Isolation, Durability.]**

**(Voiceover):**
Booking karne mein do kaam hote hain: ek line `bookings` mein likhna aur kamre ko reserve mark karna. Agar beech mein bijli chali jaaye to kya hoga? Aadhi booking: guest ka paisa gaya, par kamra khaali dikhta hai. Relational database iska jawab transaction se deta hai. Ek transaction mein kai kaam hote hain, aur ya to sab hote hain ya kuch bhi nahi. Ise ACID kehte hain. Atomicity: poora ya kuch nahi. Consistency: rules kabhi nahi tootte. Isolation: do transaction ek doosre ko beech mein nahi dekhte. Durability: commit ke baad data khoya nahi. Yahi wajah hai ki bookings, payments aur inventory ke liye relational database hi pehli pasand hai.

### [06:50 – 09:05] Scene 4: Rules Ledger Ke Andar
**[VISUAL: A `bookings` table with a rule badge on each column: NOT NULL, a foreign key, a CHECK `check_out > check_in`. A second booking for room 101 on overlapping dates is rejected with an error message.]**

**(Voiceover):**
Rules sirf application ki parchi mein rakhne se kaam nahi chalta, kyunki kal koi doosri parchi aayegi aur wo bhool jaayegi. Behtar hai ki rule ledger ke andar hi ho. `NOT NULL`: ye column khaali nahi ho sakta. `FOREIGN KEY`: `room_id` ek asli kamre ki taraf hi ishaara kare. `CHECK (check_out > check_in)`: nikalne ki date aane ki date ke baad ho. Aur `UNIQUE`: ek hi kamra ek hi raat ke liye do baar nahi. Jab rule ledger khud lagata hai, to koi bhi parchi, koi bhi developer, koi bhi galat jaldbaazi use tod nahi sakta. Ye database ka sabse bada faayda hai, aur Excel mein ye nahi milta.

### [09:05 – 11:30] Scene 5: Loose Forms: NoSQL, aur Kab Kya
**[VISUAL: A cabinet of loose forms, each a different shape: one guest preference card with 3 fields, another with 12. Four icons: key-value, document, wide-column, graph. A decision card: "relations, rules, transactions → SQL; one key, huge scale, flexible shape → NoSQL".]**

**(Voiceover):**
Doosri tarah ka records office hai: loose forms ki almari. NoSQL mein har form ka shape alag ho sakta hai, aur zyadatar ek hi key se dhoondha jaata hai. Ye kai tarah ke hote hain: key-value, document, wide-column, graph. AWS mein DynamoDB iska bada udaharan hai. Atithi ke liye: bookings ledger mein jayengi, kyunki rishte aur rules chahiye. Par har guest ke "pasandida pillow ka type" jaise bahut alag shape ke notes loose forms mein bhi rakhe jaa sakte hain. Seedha rule: rishte aur transactions zaroori hain to SQL, aur bahut bade scale par ek key se kaam chalta hai to NoSQL. Aur "NoSQL naya hai, isliye behtar" wali soch galat hai. Pehle sawaal dekho, phir ledger chuno.

### [11:30 – 14:55] Scene 6: Lab: Laptop par Ledger
**[VISUAL: Terminal with `sqlite3 atithi.db`. Tables created, three INSERTs, a JOIN with GROUP BY, then a failing INSERT for a double booking and a `BEGIN; ... ROLLBACK;` block that undoes two statements.]**

**(Voiceover):**
Lab. Cloud ki zaroorat nahi, laptop par SQLite kholo: `sqlite3 atithi.db`. Teen tables banao:
```sql
CREATE TABLE guests(id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE rooms(id INTEGER PRIMARY KEY, number TEXT UNIQUE NOT NULL, rate INT);
CREATE TABLE bookings(id INTEGER PRIMARY KEY, guest_id INT REFERENCES guests(id), room_id INT REFERENCES rooms(id), night TEXT, UNIQUE(room_id, night));
```
Do guests, do kamre aur kuch bookings daalo. Phir `SELECT g.name, COUNT(*) FROM bookings b JOIN guests g ON g.id=b.guest_id GROUP BY g.name;` chalao. Ab wahi kamra wahi raat dobara book karne ki koshish karo: `UNIQUE` use rok dega. Ek chhoti baat: SQLite mein foreign key ki jaanch default mein band hoti hai. `PRAGMA foreign_keys=ON;` likho tabhi galat `guest_id` par booking rukti hai; humne bina iske guest 99 ki booking ghus jaate dekhi. Postgres mein ye jaanch hamesha on hai. Aakhir mein `BEGIN;`, do inserts, phir `ROLLBACK;` likho, aur `SELECT` se dekho ki dono gayab hain. Ye wahi ledger hai jo agle episodes mein landlord ke records office mein jaayega.

### [14:55 – 15:40] Scene 7: Recap aur Bridge
**[VISUAL: A card: "table + key + rules · SQL asks the question · transaction = all or nothing · NoSQL = loose forms, one key · pick by the question".]**

**(Voiceover):**
Recap: ledger, rules aur transactions. Ab ek sawaal: records office khud chalana kaisa hoga? Raat ko patching, har raat ki copy, building girne par standby. Ye sab landlord karta hai, agar aap RDS lete ho.

---

# 📺 EPISODE 2: RDS — Landlord Chalaye Records Office

### [00:00 – 02:00] Scene 1: Raat ke Teen Baje ka Records Officer
**[VISUAL: A records officer at 3 AM in a building, applying a software patch, checking last night's copy, drinking tea. A second frame: the same office with a "managed by the landlord" ribbon, and the officer sleeping.]**

**(Voiceover):**
Maan lo Atithi EC2 building par khud database chalata hai. Phir building ka operating system patch karna aapka kaam, database ka naya version aapka kaam, raat ki copy aapka kaam, aur building gir jaaye to naya standby banana bhi aapka kaam. Landlord ek aur option deta hai: Relational Database Service, RDS. Wo records office ka dhancha, copy aur failover sambhalta hai. Aap ledger ke andar ke data aur sawalon par dhyaan dete ho. Is soch ko "managed service" kehte hain.

### [02:00 – 04:25] Scene 2: Kaun Kya Sambhalta Hai
**[VISUAL: A two-column card. Landlord: hardware, operating system, database software install and patching, automated backups, failover. You: tables and indexes, queries, parameters, who can reach the database, cost. A line in the middle: "no SSH into the database machine".]**

**(Voiceover):**
RDS mein landlord hardware, operating system, database software ki installation aur patching, automatic backups aur failover sambhalta hai. Aap tables aur indexes, queries, settings, aur ye kaun database tak pahunch sakta hai, ye sambhalte ho. Engine aap chunte ho: PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, Db2, aur landlord ka apna Aurora. Ek zaroori baat: database wali machine mein aap SSH nahi kar sakte. Wo landlord ka kamra hai. Isliye "managed" ka matlab hai ki aap aaraam paate ho, aur badle mein kuch control chhodte ho. Ye Session 8 ke shared responsibility model ka hi naya roop hai.

### [04:25 – 07:10] Scene 3: Instance, Storage aur Settings
**[VISUAL: The Create database form. Highlights: engine and version, template (Free tier / Dev-Test / Production), instance class `db.t4g.micro`, storage type and size with "autoscaling limit", a Subnet group, a Parameter group.]**

**(Voiceover):**
Database banate waqt kuch faisle lene hain. Engine aur uska version. Instance class, jaise `db.t4g.micro`, jo CPU aur RAM tay karti hai, bilkul Session 10 ke instance type ki tarah. Storage ka type aur size: storage badh sakta hai par ghata nahi sakte, aur aap storage autoscaling ki upar ki seema rakh sakte ho. Subnet group: wo list jisme batate hain ki database kin subnets mein rahega, aur usme kam se kam do towers chahiye. Parameter group: database ke settings ka set, jaise connection ki seema. Aur ek template: free tier, dev ya production, jo kai default badal deta hai. Free tier ki shartein badalti rehti hain, to live page dekhna.

### [07:10 – 09:30] Scene 4: Endpoint: Naam, IP Nahi
**[VISUAL: A connection string `postgresql://app@atithi-db.abc123.ap-south-1.rds.amazonaws.com:5432/atithi`. Beside it, a failover animation where the name stays and the machine behind it changes. A cross over a typed IP address.]**

**(Voiceover):**
RDS aapko ek endpoint deta hai: ek lamba DNS naam, jaise `atithi-db.abc123.ap-south-1.rds.amazonaws.com`. Application usi naam se judti hai, IP se kabhi nahi. Wajah: jab standby aage aata hai, ya jab database badal kar naya bana liya jaata hai, tab peeche ka IP badal sakta hai, par naam wahi rehta hai. Aur ek jaal: snapshot se naya database restore karoge, to endpoint naya hoga, aur application ka naam badalna padega. Port bhi engine ke hisaab se alag hai: PostgreSQL ka 5432, MySQL ka 3306. Ye raqam door guard ki list mein bhi jaayegi.

### [09:30 – 12:15] Scene 5: Pehle Se Soch Lo: Public Nahi, Delete Protection On
**[VISUAL: A short checklist beside the create form: "Public access: No", "VPC security group: only the booking building", "Encryption: On", "Deletion protection: On", "Backup retention: not zero". A "do not copy a tutorial's 0.0.0.0/0" note.]**

**(Voiceover):**
Banane se pehle ek chhoti checklist. Public access: No. Database ka door guard sirf booking building ke security group ko port par andar aane de. Encryption on, kyunki wo baad mein on nahi ki jaa sakti: ek bina encryption wale database ko encrypt karna ho to snapshot ki copy encryption ke saath banao aur usse restore karo. Deletion protection on, taaki ek galat click records office ko hamesha ke liye na hata de. Aur backup ka retention zero nahi. Zero ka matlab: automatic copy band. Ye sab shuru mein ek jaisa rakhne ki aadat hai, taaki baad mein "kisi ne production mein galat setting chhodi thi" wali kahani na bane.

### [12:15 – 14:50] Scene 6: Lab: Pehla Managed Ledger
**[VISUAL: Console: Create database → Standard create → PostgreSQL → Free tier / Dev-Test template → `db.t4g.micro` → manage master password in Secrets Manager → Public access No → VPC security group `db-sg` with inbound 5432 from `booking-sg` → Create.]**

**(Voiceover):**
Lab. Console mein Create database, Standard create, PostgreSQL. Template free tier ya dev-test, instance class `db.t4g.micro`. Master username rakho, aur password ke liye option chuno ki Secrets Manager use manage kare, taaki password aapke notes mein na ho. Public access No. Ek naya security group `db-sg` banao jisme port 5432 sirf Session 11 ke `booking-sg` se allow ho. Database banne mein kuch minute lagte hain. Ye intezaar karte hue dekho ki Connectivity tab mein endpoint aur port likhe hain. Aur dhyaan: chalta database ghante ke hisaab se bill banata hai, isliye lab khatam hone par delete karna aur final snapshot ka option dekh lena.

### [14:50 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "landlord: hardware, OS, patch, backup · you: schema, queries, access · endpoint name not IP · public No, encryption On, deletion protection On".]**

**(Voiceover):**
Recap: RDS kya sambhalta hai, kya aap, aur banane se pehle ki checklist. Ab uski sabse badi taakat: ek galat DELETE ke baad wapas lautna.

---

# 📺 EPISODE 3: Raat ki Copy, Standby Ledger aur Photocopy

### [00:00 – 01:55] Scene 1: DELETE Without WHERE
**[VISUAL: A receptionist types `DELETE FROM bookings;` and presses enter. The ledger pages go blank. A slider labelled "time" slides back one minute and the pages return.]**

**(Voiceover):**
Ek raat ek developer ne `DELETE FROM bookings;` chalaya, bina WHERE ke. Poori ledger khaali. Ab kya? Agar records office ke paas raat ki copy aur har chhoti likhai ka logbook ho, to ledger ko usi ek minute pehle wapas laaya ja sakta hai. Is feature ka naam point-in-time recovery, PITR, hai. Aur ye wahi sawaal hai jo har naye engineer ko seekhna chahiye: backup sirf "hai" kehne se kaam nahi chalta, uska restore bhi kabhi try kiya hona chahiye.

### [01:55 – 04:40] Scene 2: Automated Backup aur PITR
**[VISUAL: A calendar with a nightly snapshot icon each day, and a continuous line of small log entries between them. A slider: "restore to any second in the retention window (1 to 35 days)". Latest restorable time is a few minutes behind now.]**

**(Voiceover):**
RDS ek automated backup rakhta hai: roz ek snapshot, aur uske beech ke saare badlaav ka transaction log. Retention aap ek se paintees din tak rakh sakte ho. Isse PITR milta hai: us window ke andar kisi bhi second par ledger wapas laao. Do dhyaan ki baatein. Ek, latest restorable time hamesha abhi se kuch minute peeche hota hai, isliye "abhi ke second" par nahi jaa sakte. Do, restore hamesha ek naya records office banata hai, jisme naya endpoint hota hai. Purana wahi rehta hai, jab tak aap use khud na hata do. Manual snapshot alag cheez hai: wo aap delete karoge tab tak rehta hai, aur Session 10 ki photograph jaisa hai.

### [04:40 – 07:25] Scene 3: Recovery ka Asli Kram
**[VISUAL: A runbook, five steps: 1 Stop the writers. 2 Note the time of the mistake. 3 Restore to just before it, as a new instance. 4 Compare the data, copy the lost rows back or switch the app to the new endpoint. 5 Write down what went wrong.]**

**(Voiceover):**
Galti ke baad hadbadi mein restore dabana sabse aam galti hai. Ek runbook rakho. Ek, pehle jo likh rahe hain unhe rok do, taaki naya data na bigde. Do, galti ka samay note karo, jaise logs se. Teen, usse thoda pehle ka samay chun kar naye instance mein restore karo. Chaar, naye mein check karo ki `bookings` ki lines hain. Phir ya to khoyi hui lines purane mein copy kar do, ya application ko naye endpoint par laga do. Paanch, likh lo ki galti kyun hui, aur agli baar `BEGIN` ke bina production mein DELETE na chalane ka rule bana lo. Ye Session 5 ke troubleshooting method jaisa hai: pehle samjho, phir badlo.

### [07:25 – 09:45] Scene 4: Multi-AZ: Doosre Tower mein Standby Ledger
**[VISUAL: A primary ledger in Tower A and an identical standby ledger in Tower B, linked by "synchronous copy". The primary is crossed out; the endpoint name moves to Tower B automatically. A label: "the standby does not answer normal reads".]**

**(Voiceover):**
Ab building girne ka sawaal. Multi-AZ matlab: records office ki ek exact copy doosre tower mein, jisme har likhai saath saath utarti hai, yaani synchronous. Primary kharab ho jaaye, ya tower mein bijli chali jaaye, to RDS khud standby ko aage kar deta hai. Endpoint ka naam wahi rehta hai, aur aam taur par kuch hi minute mein kaam wapas chalta hai. Dhyaan: standby aap ke normal reads ke liye nahi hai. Wo sirf tab hai jab zaroorat pade. Isliye Multi-AZ availability ke liye hai, speed ke liye nahi. Isme doosre ledger ka bhi paisa lagta hai.

### [09:45 – 12:30] Scene 5: Read Replica: Padhne ke liye Photocopy
**[VISUAL: A primary ledger with two photocopies labelled "read replica". Reports and the manager's dashboard read from the copies. A tiny delay marker on the arrow reads "a few seconds behind". A replica being promoted to its own primary.]**

**(Voiceover):**
Read replica alag cheez hai. Wo ledger ki ek photocopy hai, jo kuch second peeche rehti hai, kyunki copy asynchronous hoti hai. Isse reports, analytics aur manager ki dashboard padhne ka kaam copy par chala jaata hai, aur primary par booking likhne ka bojh kam rehta hai. Ye availability ka vaada nahi karti. Zaroorat padne par ek replica ko promote karke apna alag primary banaya ja sakta hai, par ye haath se hota hai. Kuch engines mein replica doosre region mein bhi rakh sakte ho. Seedha rule: building girne ka darr hai to Multi-AZ. Padhne ka bojh bahut hai to read replica. Dono ek hi cheez nahi, aur bahut jagah dono saath chalte hain.

### [12:30 – 14:55] Scene 6: Lab: Snapshot, Restore aur Tulna
**[VISUAL: Terminal and console. `psql` inserts three rows, then console: Actions → Take snapshot `atithi-lab-snap`. Restore snapshot as `atithi-restored`. Both endpoints queried with `SELECT COUNT(*) FROM bookings;`. Then Modify with Multi-AZ box visible but not applied.]**

**(Voiceover):**
Lab. Database mein tab tak kuch bookings daalo. Phir Actions mein jaakar ek manual snapshot lo, `atithi-lab-snap`. Us snapshot se ek naya instance restore karo, naam `atithi-restored`. Dono endpoints par `SELECT COUNT(*) FROM bookings;` chalao, aur dekho ki dono mein wahi ginti hai, par endpoint alag hain. Ab Modify screen par jaao aur dekho ki Multi-AZ aur read replica kahan se on hote hain. Mehnge options hain, isliye sirf padho, apply mat karo. Aakhir mein safai: `atithi-restored` ko hata do, original ko final snapshot ke saath hata do, aur snapshots ko bhi, kyunki wo bina instance ke bhi paisa lete hain.

### [14:55 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "backup + log = PITR · restore = new instance · Multi-AZ = standby, failover · read replica = photocopy for reads · test your restore".]**

**(Voiceover):**
Recap: PITR galti ke liye, Multi-AZ failover ke liye, read replica padhne ke liye. Restore hamesha naya instance. Ab ledger ko surakshit rakhna, aur application se judna.

---

# 📺 EPISODE 4: Ledger ko Surakshit Rakho aur Connect Karo

### [00:00 – 01:40] Scene 1: Khula Records Office
**[VISUAL: A scanner map showing an open database port on the internet with the default user `admin` and the password `admin123`. A red breach banner and a caption "found within hours".]**

**(Voiceover):**
Internet par khula database, aur uska password saral. Scanners ye kuch hi ghanton mein dhoondh lete hain. Records office mein sabse zyada sensitive jankari hoti hai: guests ke naam, phone number, tareekhein. Isliye uski suraksha ek tale se nahi, kai parton mein hoti hai. Network, access, encryption aur secrets. Session 12 mein hum ne ek bucket ko private rakhna seekha tha. Database ke liye wahi niyam aur bhi sakht hai: koi bhi khula darwaza ya khali password sidha nuksaan hai.

### [01:40 – 03:55] Scene 2: Door Guard Zanjeer, Dobara
**[VISUAL: A chain: Laptop → (no path) → Database. Booking building → (port 5432 from `booking-sg` only) → Database in the private wing. A second arrow: the database security group lists `booking-sg` as the source, not an IP range.]**

**(Voiceover):**
Session 11 ki door guard ki zanjeer yahan dobara kaam aati hai. Database ka security group port 5432 sirf `booking-sg` se allow kare, kisi IP ki list se nahi. Isse aap booking buildings badho ya ghatao, rule apne aap kaam karta rahega. Database private wing ke subnet group mein rakho, jaisa hum Session 14 mein banayenge, taaki uske liye internet se koi raasta ho hi nahi. Laptop se kaam karna ho to bastion ya Session Manager se jaao, public access se nahi. Aur ek pakki aadat: pehle woh chhote saalon ke tutorials jisme sab ke liye `0.0.0.0/0` kholne ko kaha jaata hai, unhe kabhi follow mat karo.

### [03:55 – 06:30] Scene 3: Encryption aur Secrets
**[VISUAL: A sealed envelope on the connection (TLS) and a locked cabinet around the storage (encryption at rest with KMS). A vault labelled "Secrets Manager" holding the password. The booking building, wearing a duty badge, asks the vault for it.]**

**(Voiceover):**
Teen aur parton. Ek, encryption at rest: ledger ka storage tale mein, KMS key ke saath, jo creation ke samay hi on hota hai. Do, in transit: connection par sealed envelope, yaani TLS, aur database ko aisa bana sakte ho ki bina TLS ke connection na le. Teen, secrets. Password code mein ya git mein nahi, Secrets Manager mein, aur booking building apne duty badge, yaani Session 9 ke role, se use maangti hai. Isse password kisi file mein baitha hi nahi, aur use ghumaya, yaani rotate, ja sakta hai. Secrets Manager ka bhi alag chhota kharcha hai, jo live pricing page par hai. Aur ledger ke andar bhi least privilege: application ke liye alag user, jise sirf zaroori tables par ijaazat ho.

### [06:30 – 09:15] Scene 4: Connection Pool aur Limits
**[VISUAL: Three booking buildings each opening ten connections to the database; the ledger has a limit of 100 and a "too many connections" error appears when a hundred small workers join. A pool box in front of the database, and RDS Proxy shown as a managed pool.]**

**(Voiceover):**
Ek database ek saath sirf kuch hi connections sambhal sakta hai, aur ye seema instance class se judi hoti hai. Agar har request par naya connection khole, to wo seema jaldi toot sakti hai, aur "too many connections" aata hai. Isliye application ek pool rakhti hai: kuch connections pehle se khule, jinhe requests baari baari use karti hain. Agar bahut saari chhoti parchiyan, jaise Lambda jo hum Session 15 mein dekhenge, ek saath aati hain, to har ek apna connection kholti hai. Tab RDS Proxy jaisi service beech mein pool ka kaam karti hai. Aur ek aur aadat: sawal ko hamesha parameter ke saath bhejo, jodkar nahi. Text jodne se SQL injection hota hai, jisme koi guest ke naam mein `; DROP TABLE` likh kar ledger bigaad sakta hai.

### [09:15 – 11:35] Scene 5: Connect Nahi Ho Raha? Teen Sawaal
**[VISUAL: A decision tree. "Timeout → check door guard and route". "Connection refused → wrong port or database not ready". "Password authentication failed → wrong user or password". "Database does not exist → wrong database name". A terminal shows `nc -vz ENDPOINT 5432`.]**

**(Voiceover):**
Jab connection nahi bana, to Session 5 ka troubleshooting method yaad karo: error ka shabd padho. Timeout ka matlab aksar raaste mein door guard ya route hai: `nc -vz ENDPOINT 5432` chalao, aur check karo ki database ke security group mein booking building ka group hai ya nahi. Connection refused matlab ya to galat port ya database abhi tayyar nahi. "Password authentication failed" matlab user ya password galat, ya Secrets Manager ka naya password abhi application tak nahi pahunchaya. "Database does not exist" matlab database ka naam galat likha, jo instance ke naam se alag hota hai. Har ek ka ilaaj alag hai, isliye pehle shabd padho, phir kuch badlo.

### [11:35 – 14:20] Scene 6: Lab: Building se Ledger tak
**[VISUAL: SSH to the booking building. `sudo apt install -y postgresql-client`. A secret fetched with `aws secretsmanager get-secret-value`. `psql -h ENDPOINT -U atithi_admin -d postgres`. A Python snippet with `psycopg2`, `os.environ["DB_PASSWORD"]`, and a parameterised `INSERT`.]**

**(Voiceover):**
Lab. Session 11 ki booking building mein SSH karo. `sudo apt install -y postgresql-client`. Phir `psql -h YOUR-RDS-ENDPOINT -U atithi_admin -d postgres`. Password Secrets Manager se `aws secretsmanager get-secret-value --secret-id YOUR-SECRET --query SecretString --output text` se lo, aur check karo ki building ke role ko ye padhne ki ijaazat hai. Connect hone par Episode 1 ke teen tables banao, par Postgres mein `id INTEGER PRIMARY KEY` apne aap number nahi deta: `id SERIAL PRIMARY KEY` likho, warna insert `null value in column "id"` ka error deta hai. Phir ek `SELECT`. Ab Python mein `psycopg2` se wahi query chalao: password `os.environ["DB_PASSWORD"]` se aaye, aur insert mein `%s` parameter ho, text jodna nahi. Agar timeout aaye to pichhle scene ka nuskha chalao. Aakhir mein safai: database aur lab ke snapshots delete.

### [14:20 – 15:25] Scene 7: Recap aur Bridge
**[VISUAL: A card: "private wing · SG chain from booking-sg · encrypt at rest and in transit · Secrets Manager + role · pool · parameters, not text join". Then the campus map appears with a thick line around two wings.]**

**(Voiceover):**
Recap: RDS ka poora safar: ledger, copy, standby aur suraksha. Ab ek sawaal baki hai jo humne baar baar tala: "private wing", "door guard ki zanjeer", "route", ye sab asli mein banta kaise hai? Agle session mein hum campus ka naksha khud banayenge: VPC, cloud ka networking ka dil.

---

# 📎 Student handout: Session 13 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| SQL ledger | Tables, primary key, foreign key, JOIN |
| Rules ledger ke andar | NOT NULL, FOREIGN KEY, CHECK, UNIQUE |
| ACID | Atomicity, Consistency, Isolation, Durability; transaction = poora ya kuch nahi |
| NoSQL | Loose forms; ek key se access; scale; sawaal dekh kar chuno |
| RDS landlord sambhalta | Hardware, OS, database patch, backup, failover |
| Aap sambhalte ho | Schema, queries, indexes, access, kharcha |
| Endpoint | DNS naam, IP nahi; restore par naya endpoint |
| Banane se pehle | Public No, encryption On, deletion protection On, retention zero nahi |
| Backup | Daily snapshot + log; retention 1 se 35 din; PITR; restore = naya instance |
| Multi-AZ | Synchronous standby, automatic failover; availability |
| Read replica | Asynchronous copy; padhne ka bojh; manual promote |
| Door guard | Port 5432 ya 3306, sirf application ke security group se |
| Secrets | Secrets Manager + role; password code mein nahi |
| Connect error | Timeout = SG ya route; refused = port; auth failed = user ya password |
| Pool | Connections kam khuli rakho; RDS Proxy; parameter se query |
| Safai | Instance, restored instance, manual snapshots |

# ✍️ 02: SCRIPT — SESSION-13: AWS RDS
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S13`
- **Focus:** SQL vs NoSQL, what RDS manages, backups & PITR, Multi-AZ vs read replicas, security/networking for databases, lab
- **Episodes:**
  - Episode 1: Database kyun: SQL vs NoSQL
  - Episode 2: RDS: Managed Database ka Matlab
  - Episode 3: Backup, Multi-AZ aur Read Replica
  - Episode 4: Database ko Surakshit Rakho aur Connect Karo

---

# 📺 EPISODE 1: Database kyun?

### [00:00 – 01:15] Scene 1: Excel Sheet ka Dard
**[VISUAL: An Excel sheet with 5 lakh rows freezing. Two users edit the same cell; a conflict dialog. A database icon rescues it.]**

**(Voiceover):**
Ek chhota business Excel mein sab kuch rakhta tha. Jab rows lakho mein pahunchi aur do log ek saath edit karne lage, sheet ne jawab de diya. Database is dard ki dawa hai: bahut saara data, bahut saare users, aur data ki sahi suraksha ek saath.

### [01:15 – 05:00] Scene 2: Relational (SQL) Database
**[VISUAL: Two linked tables: Customers (id, name) and Orders (id, customer_id, amount). An arrow shows the foreign key. A query: `SELECT ... JOIN ...`. ACID letters appear.]**

**(Voiceover):**
Relational database data ko tables mein rakhta hai, jinke beech rishta hota hai. Customers ki table, Orders ki table, aur customer_id se judi hui. Aap SQL se sawaal poochte ho aur join se tables jodte ho. Ye ACID transactions deta hai: Atomicity, Consistency, Isolation, Durability. Matlab bank transfer mein paisa ya to poora kat kar doosre mein jayega, ya kuch bhi nahi. Orders, payments, inventory jaisi cheezon ke liye relational database sabse sahi hai.

### [05:00 – 08:30] Scene 3: NoSQL aur Kab Kya
**[VISUAL: Four icons: Key-value (DynamoDB), Document (MongoDB-style JSON), Wide-column, Graph. A decision card: "Fixed schema + joins + transactions → SQL; massive scale/flexible schema/simple access pattern → NoSQL".]**

**(Voiceover):**
NoSQL kai tarah ka hota hai: key-value, document, wide-column, graph. Isme schema flexible hota hai aur bahut bade scale par simple access patterns ke liye tez hota hai. AWS mein DynamoDB iska bada udaharan hai. Seedha rule: agar data mein rishte aur transactions zaroori hain, SQL. Agar sab ek key se access hota hai aur scale bahut bada hai, NoSQL. Aur ek aam galti: "NoSQL naya hai to behtar hai" nahi sochna. Pehle apni access pattern dekho.

### [08:30 – 11:30] Scene 4: Lab: SQL ki Basics
**[VISUAL: A local SQLite or a Docker Postgres terminal: CREATE TABLE, INSERT, SELECT with WHERE, UPDATE, DELETE, and a JOIN.]**

**(Voiceover):**
Lab: bina cloud ke, SQLite par SQL ka abhyas karo. `sqlite3 demo.db` kholo:
```sql
CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);
CREATE TABLE orders(id INTEGER PRIMARY KEY, user_id INT, amount INT);
INSERT INTO users(name) VALUES ('Asha'),('Ravi');
INSERT INTO orders(user_id, amount) VALUES (1, 500),(1, 300),(2, 200);
SELECT u.name, SUM(o.amount) FROM users u JOIN orders o ON o.user_id=u.id GROUP BY u.name;
```
Output mein har user ka total aayega. Ye ek query agle episodes mein RDS ke upar bhi chalegi.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "SQL: tables, joins, ACID · NoSQL: scale, flexible, key access".]**

**(Voiceover):**
Recap: SQL aur NoSQL. Ab database ko khud chalana mushkil hai: patching, backup, failover. AWS RDS ye sab sambhalta hai.

---

# 📺 EPISODE 2: RDS — Managed Database

### [00:00 – 01:15] Scene 1: Raat ko Database Patch Karne ka Dard
**[VISUAL: A DBA at 3 AM applying a security patch, with a backup running and a coffee. RDS icon takes over with a "managed" ribbon.]**

**(Voiceover):**
Agar aap EC2 par khud database chalate ho, to OS patch, database upgrade, backup, monitoring, failover, sab aapka kaam hai. RDS, Relational Database Service, ek managed service hai: ye sab kaam AWS karta hai, aur aap apne data aur queries par dhyaan dete ho.

### [01:15 – 05:00] Scene 2: RDS Kya Sambhalta Hai
**[VISUAL: A split responsibilities card. AWS: hardware, OS patching, DB installation, backups, Multi-AZ failover. You: schema, queries, indexes, parameters, security groups, cost.]**

**(Voiceover):**
RDS mein AWS hardware, OS patching, database software installation, automated backups aur failover sambhalta hai. Aap schema, queries, indexes, aur network access sambhalte ho. Aap engine chun sakte ho: MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, aur AWS ka apna Aurora. Ek important baat: RDS mein aapko database server ka OS login nahi milta, isliye wo "managed" hai, aur aap seedha SSH nahi kar sakte.

### [05:00 – 08:30] Scene 3: Instance Class, Storage aur Parameter Group
**[VISUAL: An RDS create form with highlights: engine version, instance class (db.t3/db.t4g), storage type gp3 with autoscaling, parameter group, subnet group.]**

**(Voiceover):**
Database banate waqt kuch faisle. Engine aur version. Instance class, jaise `db.t4g.micro`, jo CPU aur RAM tay karti hai. Storage type aur size, aur storage autoscaling ki aap limit de sakte ho. Subnet group, jo batata hai ki database kin subnets mein rahega. Aur parameter group, jisme database ke settings hote hain. Ek rule: production database ko public mat banao. Wo private subnet mein rahe, aur sirf application ke security group se access ho.

### [08:30 – 11:30] Scene 4: Lab: RDS Banao
**[VISUAL: Console: Create database, PostgreSQL or MySQL, Free tier template, db.t4g.micro/t3.micro, set master username, store password in Secrets Manager or note securely, Public access "No", pick a VPC security group.]**

**(Voiceover):**
Lab: free tier template ke saath ek chhota PostgreSQL ya MySQL database banao. Master username rakho, aur password surakshit jagah rakho, ya Secrets Manager se managed password chuno. Public access No. Security group aisa ho jo abhi sirf aapke EC2 instance ke security group se port 5432 ya 3306 allow kare. Create hone mein kuch minute lagenge. Cost ka dhyaan: kaam ke baad database delete karo, snapshot ka option dekhkar, kyunki chalte database ka bill lagta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Managed engine · private subnet · SG from app only · delete after lab".]**

**(Voiceover):**
Recap: RDS kya sambhalta hai aur kya aap. Ab uski sabse badi taakat: backup, failover aur read scaling.

---

# 📺 EPISODE 3: Backup, Multi-AZ aur Read Replica

### [00:00 – 01:15] Scene 1: Galat DELETE, Poora Table Gayab
**[VISUAL: A developer runs `DELETE FROM orders;` without a WHERE. A timeline slider rewinds to a minute before.]**

**(Voiceover):**
Ek developer ne `DELETE FROM orders;` chalaya, bina WHERE ke. Poora table khaali. Ab kya? Agar aapke paas backup aur point-in-time recovery ho, to aap database ko us ek minute pehle ki halat mein la sakte ho. Dekhte hain ye kaise hota hai.

### [01:15 – 05:00] Scene 2: Automated Backups aur PITR
**[VISUAL: A calendar with daily snapshot icons and a continuous transaction-log line. A slider "restore to any second within retention window (1-35 days)".]**

**(Voiceover):**
RDS automated backups lete hain: roz ek snapshot, aur saath mein transaction logs. Retention period aap 1 se 35 din tak rakh sakte ho. Isse point-in-time recovery milta hai: retention ke andar kisi bhi second par restore karo. Dhyaan: restore hamesha ek naya database instance banata hai, purane ko nahi badalta. Manual snapshots alag hote hain aur aap unhe delete karoge tab tak rehte hain.

### [05:00 – 08:30] Scene 3: Multi-AZ vs Read Replica
**[VISUAL: Left: a primary in AZ-A with a standby in AZ-B (synchronous replication) and an arrow "automatic failover". Right: a primary with 2 read replicas (asynchronous), arrows labelled "read traffic".]**

**(Voiceover):**
Ye do cheezein aksar confuse karti hain. Multi-AZ high availability ke liye hai: doosre AZ mein ek standby hota hai, jisme data synchronously copy hota hai, aur primary girne par RDS khud standby par failover kar deta hai. Standby par aap normal read nahi karte. Read replica performance ke liye hai: asynchronous copy jo read queries ko baant leti hai, jaise analytics. Kuch engines mein ise alag region mein bhi rakh sakte ho. Seedha rule: failover chahiye to Multi-AZ, read load ghatana ho to replica.

### [08:30 – 11:30] Scene 4: Lab: Snapshot aur Restore
**[VISUAL: Console: take a manual snapshot, then "Restore snapshot" creating a new DB instance with a different name. A final comparison of data in both.]**

**(Voiceover):**
Lab: database mein kuch data daalo, phir manual snapshot lo. Snapshot se ek naya instance restore karo, alag naam ke saath. Dono mein connect karke `SELECT COUNT(*)` chalao. Ab Modify mein dekho ki Multi-AZ kaise on hota hai, aur read replica kaise banti hai, par mehnge options ko sirf padho, free tier ke bahar paise lagte hain. Kaam khatam hone par dono instances aur snapshots delete karna.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "PITR for mistakes · Multi-AZ for failover · replica for reads · restore = new instance".]**

**(Voiceover):**
Recap: backups, PITR, Multi-AZ, read replica. Ab database ko surakshit rakhna aur application se connect karna.

---

# 📺 EPISODE 4: Surakshit Rakho aur Connect Karo

### [00:00 – 01:15] Scene 1: Public Database, Seedha Hack
**[VISUAL: A security scanner showing an open database port on the internet with default credentials. A red breach banner.]**

**(Voiceover):**
Internet par khula database, kamzor password, aur wo kuch hi ghanton mein scan ho jata hai. Database mein sabse sensitive data hota hai, isliye uski suraksha ek nahi, kai layers mein hoti hai: network, access, encryption aur secrets.

### [01:15 – 05:00] Scene 2: Network, Encryption aur Secrets
**[VISUAL: A layered diagram: private subnet; SG allowing only app SG on port 5432; encryption at rest (KMS) and in transit (TLS); credentials in Secrets Manager rotating.]**

**(Voiceover):**
Network: database private subnet mein, aur security group sirf application ke security group ko port par allow kare. Encryption: at rest, jo creation ke samay on hota hai, KMS key ke saath, aur in transit, TLS ke saath. Credentials: password code ya config file mein nahi, Secrets Manager mein, jahan wo automatically rotate bhi ho sakta hai. Aur database user ko sirf zaroori permissions do. Application ke liye alag user, admin user se nahi.

### [05:00 – 08:30] Scene 3: Connection aur Connection Limits
**[VISUAL: An app with a connection pool of 10 connections to the database. A chart: too many connections → "too many connections" error. RDS Proxy shown as an optional layer.]**

**(Voiceover):**
Application database se connection pool ke through jude, har request par naya connection nahi. Har database ki connection limit hoti hai, aur Lambda jaise bahut saare chhote clients us limit ko tod sakte hain. Is liye RDS Proxy jaisi service ya sahi pooling use hoti hai. Connection string mein endpoint DNS naam hota hai, IP nahi, kyunki failover ke baad IP badal sakta hai par naam wahi rehta hai.

### [08:30 – 11:30] Scene 4: Lab: EC2 se Connect
**[VISUAL: SSH to the EC2 app server. `sudo apt install -y postgresql-client`, `psql -h ENDPOINT -U admin -d postgres`, a query, then `\q`. A failed connect due to the wrong security group is fixed.]**

**(Voiceover):**
Lab: EC2 instance par client install karo, `sudo apt install -y postgresql-client`, phir `psql -h YOUR-RDS-ENDPOINT -U admin -d postgres`. Agar connect nahi ho raha, to timeout aaye to security group dekho, aur "password authentication failed" aaye to credentials. Connect hone par ek table banao aur ek query chalao. Ab ek Python snippet likho jo `psycopg2` se wahi query chalaye, aur password environment variable se padhe.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "private subnet · SG chain · encrypt · Secrets Manager · pooling".]**

**(Voiceover):**
Recap: RDS ka poora safar. Ek sawaal ab bhi bacha hai: ye sab private subnet, security groups, aur routing, ye network sach mein kaise kaam karta hai? Agle session mein VPC, cloud ka networking ka dil.

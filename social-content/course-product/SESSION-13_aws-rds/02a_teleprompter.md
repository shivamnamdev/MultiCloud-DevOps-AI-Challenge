# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-13_aws-rds

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,805 · **Episodes:** 4

---

# EPISODE 1: Records Office kyun

## Register Bhar Gaya, Do Log Ek Saath

Atithi ki booking site ab roz saikdon booking leti hai. Shuru mein ek spreadsheet kaafi lagti thi. Ab do problems hain. Do receptionists ek hi kamra do alag guests ko ek saath de dete hain. Aur sheet itni bhaari ho gayi hai ki khulne mein minute lagte hain. Photos aur invoices ka ghar humne pichhle session mein banaya tha, par booking ki jankari box mein nahi rakhi jaa sakti, kyunki usme rishte hote hain: kaun guest, kaun kamra, kaun si date. Ismein ek ruled ledger chahiye, jahan har line ke columns tay hon, aur jahan ek saath likhne wale ek doosre ko galat na kar saken. Isi ka naam database hai.

## Ruled Ledger: Tables aur Rishte

Relational database data ko tables mein rakhta hai, jinke beech rishte hote hain. Atithi mein teen tables: guests, rooms aur bookings. bookings ki har line mein guest_id aur room_id hota hai, jo doosre tables ki line ki taraf ishaara karta hai. Isse guest ka naam har booking mein dobara nahi likhna padta. Sawaal poochne ki bhasha SQL hai, aur JOIN se teeno tables ek saath padhe jaate hain. Har table ki ek primary key hoti hai, jo har line ko akela pehchaanti hai, aur foreign key wo ishaara hai jo bataata hai ki ye line kis doosre table se judi hai. Ye wahi ruled ledger hai: har column ka naam aur type pehle se tay.

## ACID: Poora Ya Kuch Nahi

Booking karne mein do kaam hote hain: ek line bookings mein likhna aur kamre ko reserve mark karna. Agar beech mein bijli chali jaaye to kya hoga? Aadhi booking: guest ka paisa gaya, par kamra khaali dikhta hai. Relational database iska jawab transaction se deta hai. Ek transaction mein kai kaam hote hain, aur ya to sab hote hain ya kuch bhi nahi. Ise ACID kehte hain. Atomicity: poora ya kuch nahi. Consistency: rules kabhi nahi tootte. Isolation: do transaction ek doosre ko beech mein nahi dekhte. Durability: commit ke baad data khoya nahi. Yahi wajah hai ki bookings, payments aur inventory ke liye relational database hi pehli pasand hai.

## Rules Ledger Ke Andar

Rules sirf application ki parchi mein rakhne se kaam nahi chalta, kyunki kal koi doosri parchi aayegi aur wo bhool jaayegi. Behtar hai ki rule ledger ke andar hi ho. NOT NULL: ye column khaali nahi ho sakta. FOREIGN KEY: room_id ek asli kamre ki taraf hi ishaara kare. CHECK (check_out > check_in): nikalne ki date aane ki date ke baad ho. Aur UNIQUE: ek hi kamra ek hi raat ke liye do baar nahi. Jab rule ledger khud lagata hai, to koi bhi parchi, koi bhi developer, koi bhi galat jaldbaazi use tod nahi sakta. Ye database ka sabse bada faayda hai, aur Excel mein ye nahi milta.

## Loose Forms: NoSQL, aur Kab Kya

Doosri tarah ka records office hai: loose forms ki almari. NoSQL mein har form ka shape alag ho sakta hai, aur zyadatar ek hi key se dhoondha jaata hai. Ye kai tarah ke hote hain: key-value, document, wide-column, graph. AWS mein DynamoDB iska bada udaharan hai. Atithi ke liye: bookings ledger mein jayengi, kyunki rishte aur rules chahiye. Par har guest ke "pasandida pillow ka type" jaise bahut alag shape ke notes loose forms mein bhi rakhe jaa sakte hain. Seedha rule: rishte aur transactions zaroori hain to SQL, aur bahut bade scale par ek key se kaam chalta hai to NoSQL. Aur "NoSQL naya hai, isliye behtar" wali soch galat hai. Pehle sawaal dekho, phir ledger chuno.

## Lab: Laptop par Ledger

Lab. Cloud ki zaroorat nahi, laptop par SQLite kholo: sqlite3 atithi.db. Teen tables banao:

Do guests, do kamre aur kuch bookings daalo. Phir SELECT g.name, COUNT(*) FROM bookings b JOIN guests g ON g.id=b.guest_id GROUP BY g.name; chalao. Ab wahi kamra wahi raat dobara book karne ki koshish karo: UNIQUE use rok dega. Ek chhoti baat: SQLite mein foreign key ki jaanch default mein band hoti hai. PRAGMA foreign_keys=ON; likho tabhi galat guest_id par booking rukti hai; humne bina iske guest 99 ki booking ghus jaate dekhi. Postgres mein ye jaanch hamesha on hai. Aakhir mein BEGIN;, do inserts, phir ROLLBACK; likho, aur SELECT se dekho ki dono gayab hain. Ye wahi ledger hai jo agle episodes mein landlord ke records office mein jaayega.

## Recap aur Bridge

Recap: ledger, rules aur transactions. Ab ek sawaal: records office khud chalana kaisa hoga? Raat ko patching, har raat ki copy, building girne par standby. Ye sab landlord karta hai, agar aap RDS lete ho.

---

# EPISODE 2: RDS — Landlord Chalaye Records Office

## Raat ke Teen Baje ka Records Officer

Maan lo Atithi EC2 building par khud database chalata hai. Phir building ka operating system patch karna aapka kaam, database ka naya version aapka kaam, raat ki copy aapka kaam, aur building gir jaaye to naya standby banana bhi aapka kaam. Landlord ek aur option deta hai: Relational Database Service, RDS. Wo records office ka dhancha, copy aur failover sambhalta hai. Aap ledger ke andar ke data aur sawalon par dhyaan dete ho. Is soch ko "managed service" kehte hain.

## Kaun Kya Sambhalta Hai

RDS mein landlord hardware, operating system, database software ki installation aur patching, automatic backups aur failover sambhalta hai. Aap tables aur indexes, queries, settings, aur ye kaun database tak pahunch sakta hai, ye sambhalte ho. Engine aap chunte ho: PostgreSQL, MySQL, MariaDB, Oracle, SQL Server, Db2, aur landlord ka apna Aurora. Ek zaroori baat: database wali machine mein aap SSH nahi kar sakte. Wo landlord ka kamra hai. Isliye "managed" ka matlab hai ki aap aaraam paate ho, aur badle mein kuch control chhodte ho. Ye Session 8 ke shared responsibility model ka hi naya roop hai.

## Instance, Storage aur Settings

Database banate waqt kuch faisle lene hain. Engine aur uska version. Instance class, jaise db.t4g.micro, jo CPU aur RAM tay karti hai, bilkul Session 10 ke instance type ki tarah. Storage ka type aur size: storage badh sakta hai par ghata nahi sakte, aur aap storage autoscaling ki upar ki seema rakh sakte ho. Subnet group: wo list jisme batate hain ki database kin subnets mein rahega, aur usme kam se kam do towers chahiye. Parameter group: database ke settings ka set, jaise connection ki seema. Aur ek template: free tier, dev ya production, jo kai default badal deta hai. Free tier ki shartein badalti rehti hain, to live page dekhna.

## Endpoint: Naam, IP Nahi

RDS aapko ek endpoint deta hai: ek lamba DNS naam, jaise atithi-db.abc123.ap-south-1.rds.amazonaws.com. Application usi naam se judti hai, IP se kabhi nahi. Wajah: jab standby aage aata hai, ya jab database badal kar naya bana liya jaata hai, tab peeche ka IP badal sakta hai, par naam wahi rehta hai. Aur ek jaal: snapshot se naya database restore karoge, to endpoint naya hoga, aur application ka naam badalna padega. Port bhi engine ke hisaab se alag hai: PostgreSQL ka 5432, MySQL ka 3306. Ye raqam door guard ki list mein bhi jaayegi.

## Pehle Se Soch Lo: Public Nahi, Delete Protection On

Banane se pehle ek chhoti checklist. Public access: No. Database ka door guard sirf booking building ke security group ko port par andar aane de. Encryption on, kyunki wo baad mein on nahi ki jaa sakti: ek bina encryption wale database ko encrypt karna ho to snapshot ki copy encryption ke saath banao aur usse restore karo. Deletion protection on, taaki ek galat click records office ko hamesha ke liye na hata de. Aur backup ka retention zero nahi. Zero ka matlab: automatic copy band. Ye sab shuru mein ek jaisa rakhne ki aadat hai, taaki baad mein "kisi ne production mein galat setting chhodi thi" wali kahani na bane.

## Lab: Pehla Managed Ledger

Lab. Console mein Create database, Standard create, PostgreSQL. Template free tier ya dev-test, instance class db.t4g.micro. Master username rakho, aur password ke liye option chuno ki Secrets Manager use manage kare, taaki password aapke notes mein na ho. Public access No. Ek naya security group db-sg banao jisme port 5432 sirf Session 11 ke booking-sg se allow ho. Database banne mein kuch minute lagte hain. Ye intezaar karte hue dekho ki Connectivity tab mein endpoint aur port likhe hain. Aur dhyaan: chalta database ghante ke hisaab se bill banata hai, isliye lab khatam hone par delete karna aur final snapshot ka option dekh lena.

## Recap aur Bridge

Recap: RDS kya sambhalta hai, kya aap, aur banane se pehle ki checklist. Ab uski sabse badi taakat: ek galat DELETE ke baad wapas lautna.

---

# EPISODE 3: Raat ki Copy, Standby Ledger aur Photocopy

## DELETE Without WHERE

Ek raat ek developer ne DELETE FROM bookings; chalaya, bina WHERE ke. Poori ledger khaali. Ab kya? Agar records office ke paas raat ki copy aur har chhoti likhai ka logbook ho, to ledger ko usi ek minute pehle wapas laaya ja sakta hai. Is feature ka naam point-in-time recovery, PITR, hai. Aur ye wahi sawaal hai jo har naye engineer ko seekhna chahiye: backup sirf "hai" kehne se kaam nahi chalta, uska restore bhi kabhi try kiya hona chahiye.

## Automated Backup aur PITR

RDS ek automated backup rakhta hai: roz ek snapshot, aur uske beech ke saare badlaav ka transaction log. Retention aap ek se paintees din tak rakh sakte ho. Isse PITR milta hai: us window ke andar kisi bhi second par ledger wapas laao. Do dhyaan ki baatein. Ek, latest restorable time hamesha abhi se kuch minute peeche hota hai, isliye "abhi ke second" par nahi jaa sakte. Do, restore hamesha ek naya records office banata hai, jisme naya endpoint hota hai. Purana wahi rehta hai, jab tak aap use khud na hata do. Manual snapshot alag cheez hai: wo aap delete karoge tab tak rehta hai, aur Session 10 ki photograph jaisa hai.

## Recovery ka Asli Kram

Galti ke baad hadbadi mein restore dabana sabse aam galti hai. Ek runbook rakho. Ek, pehle jo likh rahe hain unhe rok do, taaki naya data na bigde. Do, galti ka samay note karo, jaise logs se. Teen, usse thoda pehle ka samay chun kar naye instance mein restore karo. Chaar, naye mein check karo ki bookings ki lines hain. Phir ya to khoyi hui lines purane mein copy kar do, ya application ko naye endpoint par laga do. Paanch, likh lo ki galti kyun hui, aur agli baar BEGIN ke bina production mein DELETE na chalane ka rule bana lo. Ye Session 5 ke troubleshooting method jaisa hai: pehle samjho, phir badlo.

## Multi-AZ: Doosre Tower mein Standby Ledger

Ab building girne ka sawaal. Multi-AZ matlab: records office ki ek exact copy doosre tower mein, jisme har likhai saath saath utarti hai, yaani synchronous. Primary kharab ho jaaye, ya tower mein bijli chali jaaye, to RDS khud standby ko aage kar deta hai. Endpoint ka naam wahi rehta hai, aur aam taur par kuch hi minute mein kaam wapas chalta hai. Dhyaan: standby aap ke normal reads ke liye nahi hai. Wo sirf tab hai jab zaroorat pade. Isliye Multi-AZ availability ke liye hai, speed ke liye nahi. Isme doosre ledger ka bhi paisa lagta hai.

## Read Replica: Padhne ke liye Photocopy

Read replica alag cheez hai. Wo ledger ki ek photocopy hai, jo kuch second peeche rehti hai, kyunki copy asynchronous hoti hai. Isse reports, analytics aur manager ki dashboard padhne ka kaam copy par chala jaata hai, aur primary par booking likhne ka bojh kam rehta hai. Ye availability ka vaada nahi karti. Zaroorat padne par ek replica ko promote karke apna alag primary banaya ja sakta hai, par ye haath se hota hai. Kuch engines mein replica doosre region mein bhi rakh sakte ho. Seedha rule: building girne ka darr hai to Multi-AZ. Padhne ka bojh bahut hai to read replica. Dono ek hi cheez nahi, aur bahut jagah dono saath chalte hain.

## Lab: Snapshot, Restore aur Tulna

Is lab ka ticket, ATITHI-013. Mrs. Mehta kehti hain: "Koi booking kabhi gum nahi honi chahiye, galti se bhi nahi." Done when: database private ho aur public se na khule, saat din ka backup ho, deletion protection delete ko roke, aur snapshot se restore karne par purana data wapas mile. Lab. Database mein tab tak kuch bookings daalo. Phir Actions mein jaakar ek manual snapshot lo, atithi-lab-snap. Us snapshot se ek naya instance restore karo, naam atithi-restored. Dono endpoints par SELECT COUNT(*) FROM bookings; chalao, aur dekho ki dono mein wahi ginti hai, par endpoint alag hain. Ab Modify screen par jaao aur dekho ki Multi-AZ aur read replica kahan se on hote hain. Mehnge options hain, isliye sirf padho, apply mat karo. Aakhir mein safai: atithi-restored ko hata do, original ko final snapshot ke saath hata do, aur snapshots ko bhi, kyunki wo bina instance ke bhi paisa lete hain.

## Recap aur Bridge

Recap: PITR galti ke liye, Multi-AZ failover ke liye, read replica padhne ke liye. Restore hamesha naya instance. Ab ledger ko surakshit rakhna, aur application se judna.

---

# EPISODE 4: Ledger ko Surakshit Rakho aur Connect Karo

## Khula Records Office

Internet par khula database, aur uska password saral. Scanners ye kuch hi ghanton mein dhoondh lete hain. Records office mein sabse zyada sensitive jankari hoti hai: guests ke naam, phone number, tareekhein. Isliye uski suraksha ek tale se nahi, kai parton mein hoti hai. Network, access, encryption aur secrets. Session 12 mein hum ne ek bucket ko private rakhna seekha tha. Database ke liye wahi niyam aur bhi sakht hai: koi bhi khula darwaza ya khali password sidha nuksaan hai.

## Door Guard Zanjeer, Dobara

Session 11 ki door guard ki zanjeer yahan dobara kaam aati hai. Database ka security group port 5432 sirf booking-sg se allow kare, kisi IP ki list se nahi. Isse aap booking buildings badho ya ghatao, rule apne aap kaam karta rahega. Database private wing ke subnet group mein rakho, jaisa hum Session 14 mein banayenge, taaki uske liye internet se koi raasta ho hi nahi. Laptop se kaam karna ho to bastion ya Session Manager se jaao, public access se nahi. Aur ek pakki aadat: pehle woh chhote saalon ke tutorials jisme sab ke liye 0.0.0.0/0 kholne ko kaha jaata hai, unhe kabhi follow mat karo.

## Encryption aur Secrets

Teen aur parton. Ek, encryption at rest: ledger ka storage tale mein, KMS key ke saath, jo creation ke samay hi on hota hai. Do, in transit: connection par sealed envelope, yaani TLS, aur database ko aisa bana sakte ho ki bina TLS ke connection na le. Teen, secrets. Password code mein ya git mein nahi, Secrets Manager mein, aur booking building apne duty badge, yaani Session 9 ke role, se use maangti hai. Isse password kisi file mein baitha hi nahi, aur use ghumaya, yaani rotate, ja sakta hai. Secrets Manager ka bhi alag chhota kharcha hai, jo live pricing page par hai. Aur ledger ke andar bhi least privilege: application ke liye alag user, jise sirf zaroori tables par ijaazat ho.

## Connection Pool aur Limits

Ek database ek saath sirf kuch hi connections sambhal sakta hai, aur ye seema instance class se judi hoti hai. Agar har request par naya connection khole, to wo seema jaldi toot sakti hai, aur "too many connections" aata hai. Isliye application ek pool rakhti hai: kuch connections pehle se khule, jinhe requests baari baari use karti hain. Agar bahut saari chhoti parchiyan, jaise Lambda jo hum Session 15 mein dekhenge, ek saath aati hain, to har ek apna connection kholti hai. Tab RDS Proxy jaisi service beech mein pool ka kaam karti hai. Aur ek aur aadat: sawal ko hamesha parameter ke saath bhejo, jodkar nahi. Text jodne se SQL injection hota hai, jisme koi guest ke naam mein ; DROP TABLE likh kar ledger bigaad sakta hai.

## Connect Nahi Ho Raha? Teen Sawaal

Jab connection nahi bana, to Session 5 ka troubleshooting method yaad karo: error ka shabd padho. Timeout ka matlab aksar raaste mein door guard ya route hai: nc -vz ENDPOINT 5432 chalao, aur check karo ki database ke security group mein booking building ka group hai ya nahi. Connection refused matlab ya to galat port ya database abhi tayyar nahi. "Password authentication failed" matlab user ya password galat, ya Secrets Manager ka naya password abhi application tak nahi pahunchaya. "Database does not exist" matlab database ka naam galat likha, jo instance ke naam se alag hota hai. Har ek ka ilaaj alag hai, isliye pehle shabd padho, phir kuch badlo.

## Lab: Building se Ledger tak

Lab. Session 11 ki booking building mein SSH karo. sudo apt install -y postgresql-client. Phir psql -h YOUR-RDS-ENDPOINT -U atithi_admin -d postgres. Password Secrets Manager se aws secretsmanager get-secret-value --secret-id YOUR-SECRET --query SecretString --output text se lo, aur check karo ki building ke role ko ye padhne ki ijaazat hai. Connect hone par Episode 1 ke teen tables banao, par Postgres mein id INTEGER PRIMARY KEY apne aap number nahi deta: id SERIAL PRIMARY KEY likho, warna insert null value in column "id" ka error deta hai. Phir ek SELECT. Ab Python mein psycopg2 se wahi query chalao: password os.environ["DB_PASSWORD"] se aaye, aur insert mein %s parameter ho, text jodna nahi. Agar timeout aaye to pichhle scene ka nuskha chalao. Ab handover note likho: kya banaya, endpoint aur password kahan se milta hai, kitna kharcha, kaise undo karte hain, aur known gaps. Yahan gaps ye hain: Multi-AZ aur read replica nahi lagaye, aur CLI se bana database default mein encrypted nahi tha. Aakhir mein safai: database aur lab ke snapshots delete.

## Recap aur Bridge

Recap: RDS ka poora safar: ledger, copy, standby aur suraksha. Ab ek sawaal baki hai jo humne baar baar tala: "private wing", "door guard ki zanjeer", "route", ye sab asli mein banta kaise hai? Agle session mein hum campus ka naksha khud banayenge: VPC, cloud ka networking ka dil.

# ✍️ 02: SCRIPT — SESSION-08: AWS & EC2 Basics
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S08`
- **Focus:** AWS account safety (root user, MFA, budget alert), Regions, Availability Zones and edge locations, launching an EC2 instance (AMI, instance type, key pair, security group), SSH, user data, instance metadata (IMDSv2), instance states and cost hygiene
- **Story position:** Zoom level 2, the rented campus. Atithi Hotels ab apni pehli building landlord se kiraye par leti hai.
- **Story words used:** landlord (AWS), owner who signed the lease (root user), second lock (MFA), city (Region), tower (Availability Zone), building (EC2 instance), building size (instance type), furnished model hotel (AMI), building key (key pair), guard at the building door (security group), pickup counters near guests (edge locations)
- **Lab project:** the first rented building serves the Atithi booking page. The homepage content is the one-line page from Session 16; if students have not reached it, any one-line page works.
- **Cost rule for every lab:** the session ends with deleting what was created. Free-tier rules differ by account and date, so students read what their own billing page shows.
- **Episodes:**
  - Episode 1: Landlord se Pehla Samjhauta: Account, MFA, Root ka Rule aur Billing Alert
  - Episode 2: Landlord ka Naksha: Region, Availability Zone aur Edge
  - Episode 3: Pehli Building: AMI, Size, Chaabi aur Darwaze ka Guard
  - Episode 4: Building ke Andar ka Kaam: SSH, User Data aur Safai

---

# 📺 EPISODE 1: Landlord se Pehla Samjhauta

### [00:00 – 02:15] Scene 1: Ek Bhoola Hua Building, Ek Bada Bill
**[VISUAL: Aerial view of three giant real-estate towers labelled AWS, Azure, GCP. A student signs a lease for a large building and walks away. A calendar flips through a month. A bill counter climbs to a scary number. A face-palm.]**

**(Voiceover):**
Ab tak Atithi Hotels ne ek hi building ke andar kaam seekha: staff, taale, logbooks, parchiyan. Par building thi kiraye ki, aur jis landlord se mili, usse hum ab milenge. Ek student ne seekhne ke liye ek bahut badi building kiraye par li, aur wapas dena bhool gaya. Mahine ke ant mein bill aaya to hosh ud gaye. Cloud mein ye sabse aam galti hai. Isliye aaj hum pehle lease surakshit karte hain, phir kuch banate hain. Teen cheezein pehle din ki hain: root user ka sahi use, MFA, aur billing alert. Landlord ka naam hai AWS, Amazon Web Services, aur Atithi ka pehla lease isi se hoga.

### [02:15 – 05:00] Scene 2: Root User aur MFA
**[VISUAL: A diagram. On the left, the owner who signed the lease holding the master key in a vault: "root user, the email you signed up with". On the right, daily staff each with a limited badge: "IAM users and roles". A second lock appears on the vault door: an authenticator-app code.]**

**(Voiceover):**
AWS account banate hi aapko ek root user milta hai: wahi email jisse aapne lease par dastakhat kiye. Wo owner hai, jiske paas poora control hai, aur use kuch rok nahi sakta. Wo chaabi jitni kaam ki hai, utni hi khatarnaak. Isliye root par turant MFA lagao, yaani multi-factor authentication, ek doosra taala. Authenticator app se, jo aapke phone par ek badalta hua code deta hai. Aur ek rule: root se roz ka kaam nahi karte. Roz ke kaam ke liye alag staff, yaani IAM user ya role, jo hum agle session mein detail se banayenge. Root ko sirf wo kaam do jo sirf owner hi kar sakta hai, jaise account band karna. Ek aur baat: root ki access keys, yaani code se phone karne wali chaabiyan, kabhi mat banao.

### [05:00 – 08:40] Scene 3: Billing aur Free Tier
**[VISUAL: The AWS Billing console. Budgets → "Create budget" → monthly cost budget → an email alert at 80% of the amount. A free-tier usage page with progress bars. A side card: "read your own account's terms".]**

**(Voiceover):**
Landlord ke office mein sabse pehle meter lagwao: Billing mein Budgets. Ek mahine ka budget tay karo, aur jab wo eighty percent tak pahunche to email aaye. Alert se pehle bhi, kharch ka naksha dekhne ke liye Cost Explorer hai. Har resource par `Owner` aur `Purpose` tag lagao, aur billing mein un tags ko cost allocation ke liye ek baar activate karo, taaki Cost Explorer mein dikhe ki kharch kiska hai. Free tier ke rules aaj kal badalte rehte hain: kuch accounts ko credits milte hain, kuch ko purane tareeke se kuch ghante ka free usage. Isliye course ka koi number mat maano, wahi padho jo aapke apne account ke billing page par likha hai. Ek aur baat: kuch cheezein sirf chalti rehne par paise leti hain, jaise running building, ek aisa public address jo kisi se juda nahi, ya bade storerooms. AWS ab public IPv4 address par bhi ghante ke hisaab se charge karta hai, aur rate pricing page par hai. Alert lagao, aur kaam khatam hote hi safai karo.

### [08:40 – 11:35] Scene 4: Kiski Zimmedari: Landlord ya Aapki?
**[VISUAL: A building cut in half horizontally. Below the line, in the landlord's colour: land, power, towers, the machines that run many buildings. Above the line, in the tenant's colour: the operating system and its updates, the door guard list, the staff accounts, the guests' data. A caption: "of the cloud / in the cloud".]**

**(Voiceover):**
Lease par dastakhat karne se pehle ek sawaal: agar kuch toota to kiski zimmedari hai? Landlord ki zimmedari hai zameen, bijli, towers aur wo bade machines jo kai buildings ek saath chalate hain. Is hisse ko cloud ka hissa kehte hain. Aapki zimmedari hai building ke andar ki cheezein: operating system aur uske updates, darwaze ke guard ki list yaani security group, staff ke accounts, aur guests ka data. Is hisse ko cloud ke andar ka hissa kehte hain. Ye batwara AWS khud shared responsibility model kehta hai. Isliye jis building mein aapne Ubuntu rakha, uske security updates aapko chalane hain, landlord nahi chalayega. Aur jis building mein guard ki list mein poori duniya ko aane diya, uska dosh landlord ka nahi. Aage RDS aur S3 mein ye line thodi upar khiskegi, par ye batwara hamesha rahega.

### [11:35 – 13:30] Scene 5: Lab: Lease ki Checklist
**[VISUAL: A checklist with ticks appearing one by one: MFA on root, budget alert created, Cost Explorer on, Region selected, account alias set. A browser tab showing the account alias in the sign-in URL.]**

**(Voiceover):**
Lab: apne account par ye checklist poori karo. Ek: root user par MFA. Do: ek monthly budget banao jo eighty percent par email bheje. Teen: Cost Explorer chalu karo. Chaar: ek Region chuno jisme aap kaam karoge, aur har console page ke upar kone mein wahi dikh raha hai ye confirm karo. Paanch: account ka ek alias banao, taaki login URL yaad rakhna aasaan ho. Ye dus minute ka kaam hai. Har kadam ka screenshot apni notebook mein rakho. Ye aapko bade bill aur bade risk, dono se bachata hai.

### [13:30 – 14:15] Scene 6: Recap aur Bridge
**[VISUAL: A card: "Root + MFA · no daily root use · no root keys · budget alert · clean up". Under it, small: "owner · second lock · meter".]**

**(Voiceover):**
Recap: lease surakshit hai. Owner ke paas master key aur doosra taala hai, roz ka kaam staff karega, aur meter par nazar hai. Ab sawaal: landlord ki buildings kahan kahan hain? Agle episode mein uska naksha.

---

# 📺 EPISODE 2: Landlord ka Naksha

### [00:00 – 01:50] Scene 1: Ek Sheher mein Baadh Aa Gayi
**[VISUAL: A map of a city flooding. One tower goes dark. Another tower, in a different part of the same city, keeps its lights on. A hotel in the dark tower shows a "closed" sign; a hotel in the lit tower shows "open".]**

**(Voiceover):**
Maan lo Atithi ki saari buildings ek hi tower mein hain, aur us tower ki bijli chali gayi. Ya aag lag gayi. Poora business band. Isliye landlord ne apne towers shehron mein, aur har sheher mein kai alag jagah banaye hain. Is naksha ko samajhna high availability ki pehli seedhi hai. Aur aaj ke baad aapko samajh aayega ki jab AWS mein koi "region" ya "zone" likha dikhe, to wo kya hai.

### [01:50 – 04:45] Scene 2: Region, Availability Zone, Edge
**[VISUAL: A world map. One Region, Mumbai, zooms in: three tower clusters labelled AZ a, AZ b, AZ c, joined by fast lines, each with independent power. Beyond it, smaller dots in many cities labelled "edge locations", with a delivery van carrying a brochure from the nearest dot.]**

**(Voiceover):**
Region ek sheher hai, jaise Mumbai ya Frankfurt. Har sheher mein kai Availability Zones, yaani alag tower hote hain: har ek ki apni bijli aur apna network, par sheher ke andar tez raste se jude hue. Ek tower gira to doosra sambhal leta hai. Isliye app ko do tower mein chalane se wo ek tower ke girne par bhi zinda rehti hai. Edge locations chhote pickup counters hain, jo kai shehron mein hain, jahan se guests ko brochure unke paas se mil jaata hai. Wo CloudFront jaisi services ke liye kaam aate hain, jinhe hum baad mein dekhenge. Aur ek zaroori baat: ek Region ki cheezein doosre Region mein nahi dikhtin. Ye bilkul alag sheher hain.

### [04:45 – 07:25] Scene 3: Sheher Chunne ke Teen Sawaal
**[VISUAL: Three scales. Latency: distance from guests. Law: data must stay in one country. Price: the same building costs different amounts in different cities. A fourth small icon: "not every new service is in every city".]**

**(Voiceover):**
Sheher chunna sirf doori ka sawaal nahi. Teen sawaal poochho. Ek, guests kitne paas hain? Kareeb ka sheher jawab jaldi deta hai. Do, kanoon kya kehta hai? Kuch data ko apne desh ke andar hi rakhna hota hai. Teen, daam kya hai? Wahi building alag shehron mein alag kiraye par milti hai. Aur ek chhoti baat: har nayi service har sheher mein ek saath nahi aati. Seekhne ke liye ek hi Region mein kaam karo, taaki cheezein bikhri na rahein. Ek aam galti: building ek Region mein banayi, aur doosre Region ka console khol kar dhoondh rahe ho, aur lagta hai ki gayab ho gayi.

### [07:25 – 10:30] Scene 4: AWS CLI ki Chhoti Adatein
**[VISUAL: Terminal: `aws sts get-caller-identity`, `aws ec2 describe-instances --output table`, `aws ec2 describe-regions --query "Regions[].RegionName" --output text`, `aws configure --profile atithi`, `aws s3 ls --profile atithi`, `export AWS_PROFILE=atithi`. A note: `--query` uses JMESPath.]**

**(Voiceover):**
AWS CLI ki chaar chhoti adatein roz kaam aati hain. Pehli: `aws sts get-caller-identity`. Ye batata hai ki aap abhi kaun ho aur kis account mein. Jab bhi koi command ajeeb chale, pehle ye chalao. Doosri: `--output`. Wahi jawab table, text ya json mein dekh sakte ho. Teesri: `--query`, jo jawab mein se sirf wo hissa chunta hai jo aapko chahiye, jaise `"Regions[].RegionName"`. Is chhoti bhasha ka naam JMESPath hai, aur Session 7 ka boto3 isi jawab ko Python mein dictionary bana kar deta hai. Chauthi: profile. `aws configure --profile atithi` ek alag naam se alag keys rakhta hai, aur command ke saath `--profile atithi` ya `export AWS_PROFILE=atithi` lagane se wahi use hoti hain. Isse test aur production ke accounts aapas mein nahi milte.

### [10:30 – 13:55] Scene 5: Lab: Naksha Khud Dekho
**[VISUAL: The console's Region selector at the top right. Then the CloudShell icon; a terminal opens inside the browser. Commands: `aws ec2 describe-regions --query "Regions[].RegionName" --output text`, `aws ec2 describe-availability-zones --region ap-south-1 --query "AvailabilityZones[].ZoneName"`.]**

**(Voiceover):**
Lab. Console ke upar kone mein Region ka chunav dekho, aur ek do baar badal kar dekho ki page badal jaata hai. Ab command line se. Sabse aasaan tareeka hai AWS CloudShell: console mein ek chhota terminal-icon hai, jo browser ke andar ek terminal kholta hai, aur wahan AWS ke tool pehle se lage hain, aur aapke login ke saath chalte hain. Wahan `aws ec2 describe-regions --query "Regions[].RegionName" --output text` chalao: regions ki list. Phir `aws ec2 describe-availability-zones --region ap-south-1 --query "AvailabilityZones[].ZoneName"`: Mumbai ke towers. Gino kitne hain. Agar apne laptop se chalana chahte ho to AWS CLI install karke `aws configure` chalana hoga, jisme IAM user ki keys lagti hain. Wo keys hum agle session mein banayenge. Root ki keys kabhi nahi. Ye jaankari tab kaam aayegi jab hum load balancer aur Auto Scaling lagayenge.

### [13:55 – 14:25] Scene 6: Recap aur Bridge
**[VISUAL: A card: "Region → AZs → edge · choose for guests, law, price · one Region at a time".]**

**(Voiceover):**
Recap: sheher, tower aur pickup counter. Ab asli kaam: Atithi apni pehli building kiraye par leta hai.

---

# 📺 EPISODE 3: Pehli Building

### [00:00 – 01:25] Scene 1: Kiraye ki Building, Do Minute Mein
**[VISUAL: A "Launch instance" button being pressed. A progress bar. A building rises on the Atithi campus plot and its lights turn green. Text: "about two minutes".]**

**(Voiceover):**
EC2, yaani Elastic Compute Cloud, landlord ki wo service hai jisse aap ek virtual server, yaani ek kiraye ki building, leti ho. Ek button dabao aur kuch minute mein ek Linux machine aapke saamne hoti hai, bilkul waisi jisse aap pichhle kai sessions mein khelte aaye ho. Aaj hum use ek ek faisle ke saath launch karenge, taaki aap sirf next-next dabate na jao.

### [01:25 – 04:45] Scene 2: Launch Form ke Paanch Faisle
**[VISUAL: The EC2 launch wizard with five sections highlighted in turn: Name and tags, AMI, instance type, key pair, network and security group. A side table for the instance type name `t3.micro`: "t = family, 3 = generation, micro = size".]**

**(Voiceover):**
Paanch faisle. Ek, naam aur tags, taaki baad mein pata chale ki ye building kiski hai: ek `Name` aur ek `Owner`. Do, AMI, yaani Amazon Machine Image: wo poori furnished model hotel jise copy karke building banti hai. Jaise Ubuntu ya Amazon Linux. Teen, instance type, yaani building ka size, jaise `t3.micro`. Naam ko ek line mein padho: `t` family hai, `3` generation hai, aur `micro` size hai. Isse CPU aur RAM tay hoti hai. Chaar, key pair, yaani building ki chaabi, jisse aap SSH se andar aaoge. Paanch, network aur security group, yaani darwaze par guard. Seekhne ke liye wo type chuno jis par console khud "free tier eligible" likhta hai. Ek jodi ka dhyaan: AMI ki architecture aur instance type ki architecture milni chahiye. `t3` x86 hai aur `t4g` ARM (Graviton). ARM wali AMI ko `t3.micro` par chalane ki koshish karo to error aata hai; humne emulator mein yahi dekha.

### [04:45 – 07:25] Scene 3: Security Group: Darwaze ka Guard
**[VISUAL: A guard card at a building door with an inbound list: SSH port 22 from "My IP" only, HTTP port 80 from anywhere. A red cross on "SSH from 0.0.0.0/0". An arrow shows a request going in and the reply coming out automatically.]**

**(Voiceover):**
Security group building ke darwaze par khada guard hai, aur uske paas ek list hai. Inbound rules batate hain ki andar kaun aa sakta hai. SSH ke liye darwaza number 22, jo sirf aapke apne IP ke liye kholo. Console mein ek option hai "My IP", use chuno, poori duniya ke liye nahi. Web ke liye 80 ya 443 sabke liye khola ja sakta hai. Jo darwaza list mein nahi hai, wo by default band hai. Bahar jaane wale raaste, yaani outbound, by default khule hote hain. Aur is guard ki ek khaas aadat: wo stateful hai. Jo request andar aane di, uska jawab bahar jaane ke liye alag se likhna nahi padta. Guard use apne register mein yaad rakhta hai.

### [07:25 – 11:10] Scene 4: Building ke Kiraye ke Tareeke
**[VISUAL: Four lease cards: On-Demand (pay by the second or hour, leave any time), Savings Plan or Reserved (commit for one or three years, lower price), Spot (spare buildings at a big discount, but the landlord can take it back with two minutes' notice), Dedicated Host (a whole tower for you). Beside the cards, family tags: `t` burstable, `m` general, `c` compute, `r` memory.]**

**(Voiceover):**
Building ka size jaise tay hota hai, waise hi kiraya dene ke tareeke bhi alag hain. On-Demand: jab chaho lo, jab chaho chhodo, aur sirf us samay ka kiraya do. Seekhne aur naye kaam ke liye yahi theek hai. Savings Plan ya Reserved: aap ek ya teen saal ka vaada karte ho, aur kiraya kam ho jaata hai. Ye tab sahi hai jab aapko pakka pata ho ki building hamesha chalegi. Spot: landlord ki wo khaali buildings jo abhi bike nahi, badi chhoot par. Par landlord kabhi bhi unhe wapas le sakta hai, do minute ki notice par. To Spot un kaamon ke liye hai jo beech mein rukne par bhi kharab nahi hote. Aur Dedicated Host mein poora tower sirf aapka hota hai, jo kuch kanooni ya license ki zaroorat mein kaam aata hai. Size ka family wala naam bhi dekho: `t` kabhi kabhi tez chalne wale chhote kaam ke liye, `m` aam kaam ke liye, `c` zyada CPU ke liye, `r` zyada memory ke liye. Seekhne mein `t` family kaafi hai.

### [11:10 – 13:45] Scene 5: Lab: Launch aur Andar Jao
**[VISUAL: The final launch screen → instance state "Running" → copy the public IPv4 address → terminal: `chmod 400 atithi-key.pem`, `ssh -i atithi-key.pem ubuntu@<IP>`; inside: `uname -a`, `df -h`.]**

**(Voiceover):**
Lab. Ek Ubuntu ya Amazon Linux building launch karo. Naam `atithi-web-1`, tag Owner mein apna naam. Key pair banao, aur `.pem` file download hogi. Wo chaabi sirf ek hi baar milti hai, use surakshit rakho. Laptop par `chmod 400 atithi-key.pem`, warna SSH khud mana kar dega. Security group mein 22 sirf My IP ke liye. Building Running hote hi public IPv4 address copy karo aur `ssh -i atithi-key.pem ubuntu@IP` chalao. Amazon Linux par user ka naam `ec2-user` hota hai. Andar pahunch kar `uname -a` aur `df -h` chalao. Ye wahi Linux hai jise Session 3 se Session 5B tak aapne seekha, bas ab ye landlord ki building mein hai. Aapne abhi cloud mein ek asli server banaya.

### [13:45 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "AMI · type · key pair · security group · SSH". Under it, small: "model hotel · size · key · door guard".]**

**(Voiceover):**
Recap: furnished model hotel, building ka size, chaabi aur darwaze ka guard. Ab is building par kaam: bina haath lagaye naya setup, aur sabse zaroori, building wapas dena.

---

# 📺 EPISODE 4: Building ke Andar ka Kaam

### [00:00 – 01:20] Scene 1: Har Baar Haath se Setup?
**[VISUAL: A staff member renting the tenth building in a row and typing the same `apt install nginx` for the tenth time, sleepy. A scroll labelled "user data" drops onto the desk.]**

**(Voiceover):**
Ek building mein haath se nginx lagana theek hai. Par dus buildings mein? Pagalpan. EC2 mein ek parchi, jise user data kehte hain, building ke pehli baar chalne par apne aap chalti hai. Isse har nayi building khud taiyaar hoti hai, bina aapke SSH kiye. Aur ye wahi soch hai jo aage Auto Scaling aur infrastructure as code mein bar bar dikhegi.

### [01:20 – 04:35] Scene 2: User Data aur Building ki Apni Jaankari
**[VISUAL: The launch form's Advanced section with a user-data script box. Then, inside the building: a two-step metadata call. Step 1: `TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60")`. Step 2: `curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id`.]**

**(Voiceover):**
User data mein ek shell parchi daalo, jo root ke taur par chalti hai:
```bash
#!/bin/bash
apt-get update -y
apt-get install -y nginx
echo "<h1>Atithi Hotels: Book Now</h1><p>Served by $(hostname)</p>" > /var/www/html/index.html
```
Ye Ubuntu ke liye hai. Amazon Linux par `apt-get` ki jagah `dnf` aur nginx ka apna package chalega. Do cheezein yaad rakho. Ye parchi by default sirf pehle boot par chalti hai. Aur uska jawab `/var/log/cloud-init-output.log` mein milta hai, jahan galti dhoondhni ho to wahin jao. Ab building ki apni jaankari: ek chhoti sewa, jise metadata service kehte hain, building ke andar se hi, ek khaas address par milti hai. Naye tareeke, IMDSv2, mein pehle ek chhota token maangte ho, phir us token ke saath poochte ho, jaise instance-id. Isi sewa mein building ko mila hua IAM role ka temporary badge bhi hota hai, isliye us address tak ki pahunch sambhal kar deni chahiye.

### [04:35 – 07:05] Scene 3: Stop, Terminate aur Paisa
**[VISUAL: A state diagram: Pending → Running → Stopping → Stopped → Terminated. A billing bar under each: compute is charged while Running; the attached storeroom is charged while Stopped; nothing at Terminated except any volumes that were kept. A public address that changes on stop and start.]**

**(Voiceover):**
Building ki haalat samjho. Running mein building ka kiraya lagta hai. Stop karne par building band ho jaati hai aur uska kiraya ruk jaata hai, par us se juda storeroom, yaani EBS volume, ka kiraya chalta rehta hai. Terminate yaani lease ka poora khatm. Building hamesha ke liye gayi, aur by default uska root storeroom bhi. Ek baat aur: building ka public address, jo aapko by default milta hai, stop aur start ke baad badal jaata hai. Pakka address chahiye to Elastic IP lena padta hai, aur wo bhi paise leta hai. Isliye test ke baad stop nahi, terminate karo. Aur phir dekho ki koi volume ya Elastic IP bacha to nahi.

### [07:05 – 10:20] Scene 4: Andar Nahi Jaa Paye to: SSH ke Teen Jawab
**[VISUAL: Three door scenes. A door with a long wait and nobody answering, text: `Connection timed out`. A door that opens but a guard says "wrong key", text: `Permission denied (publickey)`. A door that is reached but nobody is inside, text: `Connection refused`. A fourth card: `WARNING: UNPROTECTED PRIVATE KEY FILE!`.]**

**(Voiceover):**
SSH na chale to error ka text hi aapko sahi jagah bhejta hai. Pehla: `Connection timed out`. Aap darwaze tak pahunche hi nahi. Raaste mein kuch roka hua hai: security group mein 22 nahi hai, ya aapka IP badal gaya hai aur My IP puraana hai, ya aapne galat public address daala. Doosra: `Permission denied (publickey)`. Aap darwaze tak pahunche, par chaabi ya naam galat hai. Galat `.pem`, galat user ka naam, jaise Ubuntu par `ubuntu` aur Amazon Linux par `ec2-user`, ya key ke saath `-i` bhoolna. Teesra: `Connection refused`. Aap pahunche, guard ne roka bhi nahi, par us darwaze par koi sun hi nahi raha: ssh service andar band hai. Aur ek chautha: `UNPROTECTED PRIVATE KEY FILE`. Matlab `.pem` ke permissions khule hain, `chmod 400` lagao. Ye wahi layer-by-layer soch hai jo Session 5 mein thi: kaun si parat tak pahunche aur kahan ruke.

### [10:20 – 13:55] Scene 5: Lab: Web Wali Building aur Safai
**[VISUAL: A new instance launched with the user-data script; security group now allows port 80 from anywhere. After two or three minutes the browser opens `http://PUBLIC_IP` and shows the Atithi page. Then Terminate, and the Volumes and Elastic IPs pages showing nothing left over.]**

**(Voiceover):**
Is lab ka ticket, ATITHI-008. Mrs. Mehta kehti hain: "Pehla server aaj hi live ho jaye. Bas ek simple page dikhna chahiye, aur sirf meri team andar ja sake." Done when: browser mein page dikhe, SSH sirf aapke apne IP se chale, aur har cheez par tag lagi ho. Lab. Ek nayi building launch karo, naam `atithi-web-2`. Advanced mein user data ke andar upar wali parchi daalo. Security group mein 22 My IP ke liye aur 80 sabke liye. Do teen minute baad browser mein `http://PUBLIC_IP` kholo: Atithi ka page, aur neeche building ka naam. Dhyaan rahe, browser kabhi kabhi `https` jodne ki koshish karta hai. Ye abhi sirf `http` par chalega. Agar na dikhe to teen jagah dekho. Pehla, building Running hai aur status checks poore hue? Doosra, security group mein 80 hai? Teesra, `cloud-init-output.log`, jo SSH karke padho. Dekho: ye wahi tareeka hai jo Session 5 mein tha, andar se bahar. Kaam khatam hote hi dono buildings ko terminate karo, aur EC2 ke Volumes aur Elastic IPs ke pannon par dekho ki kuch bacha to nahi. Ab handover note likho: kya banaya, kaise pahunchenge, kitna kharcha, kaise undo karte hain, aur known gaps. Yahan gaps ye hain: ek hi server hai, sirf `http` hai, aur setup haath se kiya gaya hai. Ye gaps aage ke sessions bharenge.

### [13:55 – 15:00] Scene 6: Recap aur Bridge
**[VISUAL: A card: "user data · IMDSv2 · stop ≠ terminate · clean up after every lab".]**

**(Voiceover):**
Recap: user data se apne aap setup, building ki apni jaankari, building ki haalat aur safai. Ab ek bada sawaal: lease par aap akele ho, par Atithi mein kai log kaam karenge. Landlord ke office mein kaun kya kar sakta hai? Agla session isi ke baare mein hai: IAM.

---

# 📎 Student handout: Session 08 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Root user | Owner. MFA lagao, roz ka kaam nahi, access keys kabhi nahi |
| Billing | Budget banao, 80% par email alert, free tier ke rules apne account par padho |
| Region | Sheher. Ek Region ki cheezein doosre mein nahi dikhtin |
| Availability Zone | Region ke andar alag tower, alag bijli |
| Instance type | `t3.micro`: family `t`, generation `3`, size `micro` |
| AMI | Furnished model hotel, jisse building banti hai |
| Key pair | `.pem` ek hi baar milti hai; `chmod 400` |
| SSH | `ssh -i key.pem ubuntu@IP` (Amazon Linux: `ec2-user`) |
| Security group | Inbound: jo likha hai wahi. SSH sirf My IP. Stateful |
| User data | Pehle boot par, root ke taur par; log: `/var/log/cloud-init-output.log` |
| Metadata (IMDSv2) | Pehle token (PUT), phir `X-aws-ec2-metadata-token` header ke saath GET |
| Stop | Compute ka kiraya band, storage ka chalu |
| Terminate | Building aur by default root volume khatm; Elastic IP aur volumes khud check karo |

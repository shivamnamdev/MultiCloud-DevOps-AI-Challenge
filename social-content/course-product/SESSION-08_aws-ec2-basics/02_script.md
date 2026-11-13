# ✍️ 02: SCRIPT — SESSION-08: AWS & EC2 Basics
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S08`
- **Focus:** AWS account safety & billing, global infrastructure, EC2 launch, SSH & user data, stop/terminate and cost hygiene
- **Episodes:**
  - Episode 1: AWS Account: Billing Alert, MFA aur Root ka Rule
  - Episode 2: AWS Global Infrastructure: Region, AZ aur Edge
  - Episode 3: Pehla EC2 Instance: AMI, Type, Key Pair, Security Group
  - Episode 4: Server par Kaam: SSH, User Data aur Cleanup

---

# 📺 EPISODE 1: AWS Account — Billing Alert, MFA aur Root ka Rule

### [00:00 – 01:15] Scene 1: Ek Bhoola Hua Server, Ek Bada Bill
**[VISUAL: A student leaves a large instance running. A calendar flips through a month. A bill counter climbs to a scary number. A face-palm.]**

**(Voiceover):**
Ek student ne seekhne ke liye ek bada server launch kiya aur band karna bhool gaya. Mahine ke ant mein bill dekha to hosh ud gaye. Cloud mein ye sabse aam galti hai, aur isiliye aaj hum pehle account ko surakshit karte hain, phir kuch banate hain. Billing alert, MFA aur root user ka sahi use: teen cheezein jo pehle din ki hain.

### [01:15 – 04:30] Scene 2: Root User aur MFA
**[VISUAL: A diagram: root user with the email/password (master key in a vault) vs IAM users for daily work. MFA code from an authenticator app.]**

**(Voiceover):**
AWS account banate hi aapko root user milta hai, wo email jisse aapne account banaya. Root account ke paas har cheez ka poora control hota hai aur use kuch rok nahi sakta. Isliye root par MFA, yaani multi-factor authentication, turant lagao, authenticator app se. Aur rule: root se roz ka kaam nahi karte. Roz ke kaam ke liye alag IAM user ya role, jo hum IAM session mein detail se seekhenge. Root ko sirf kuch khaas kaamon ke liye use karo.

### [04:30 – 08:00] Scene 3: Billing aur Free Tier ko Samajhna
**[VISUAL: AWS Billing console: Budgets, "Create budget", an email alert at 80% threshold. A free-tier usage page with bars.]**

**(Voiceover):**
AWS Billing mein Budgets banao: jaise "mahine ka budget kuch rupaye", aur 80% par email alert. Free tier ke rules aaj kal alag alag tarah ke hote hain, kuch naye accounts ke liye credits wale, kuch purane wale usage limits, isliye jo bhi aapke account par dikhe, wohi padho. Ek aur baat: kuch cheezein chalu rehne par hi paise leti hain, jaise running instance, elastic IP jo kisi se juda nahi, ya bade volumes. Alert lagao, aur kaam khatam hote hi saaf karo.

### [08:00 – 11:30] Scene 4: Lab: Account Hardening Checklist
**[VISUAL: A checklist with ticks: MFA on root, Budget alert created, Cost Explorer enabled, Region selected, Account alias set.]**

**(Voiceover):**
Lab: apne account mein ye checklist poori karo. Root par MFA. Ek budget banao jo alert bheje. Ek region chuno jisme aap kaam karoge, aur har console page ke upar wahi dikh raha hai ye confirm karo. Aur account ka ek alias banao taaki login URL yaad rakhna aasaan ho. Screenshot lo aur apni notebook mein rakho. Ye 10 minute ka kaam aapko bade bill aur bade risk dono se bachata hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Root + MFA · No daily root use · Budget alert · Clean up".]**

**(Voiceover):**
Recap: account surakshit, billing par nazar. Ab ek sawaal: AWS ke servers kahan hain? Region aur Availability Zone kya hote hain? Agle episode mein.

---

# 📺 EPISODE 2: AWS Global Infrastructure

### [00:00 – 01:15] Scene 1: Ek Sheher mein Baadh Aa Gayi
**[VISUAL: A map of a city flooding. A single data center building goes dark. Another data center in a different part of the city keeps lights on.]**

**(Voiceover):**
Maan lo aapka poora server ek hi building mein hai, aur us building mein bijli chali gayi ya aag lag gayi. Aapka business band. Isiliye AWS ne apne data centers ko kai jagah failaya hai. Is design ko samajhna hi high availability ki pehli seedhi hai.

### [01:15 – 05:00] Scene 2: Region, Availability Zone, Edge
**[VISUAL: A world map with a Region (e.g., Mumbai) zoomed in: three AZ clusters connected by fast lines. Smaller dots labelled "Edge locations".]**

**(Voiceover):**
Region ek bhaugolik ilaaka hai, jaise Mumbai ya Frankfurt. Har region ke andar kai Availability Zones hote hain, yaani alag alag data center ke group, jo ek doosre se door, par tez network se jude hote hain. Agar aap app ko do AZ mein chalate ho, to ek AZ gira to doosra sambhaal leta hai. Edge locations chhote points hain jahan se content users ke kareeb se serve hota hai, CloudFront jaise services ke liye. Region chunte waqt do cheezein dekho: users ke kitne kareeb, aur kaun si services wahan available hain.

### [05:00 – 08:30] Scene 3: Compliance, Latency, Cost: Region Chunne ke Sawaal
**[VISUAL: Three scales: Latency (distance to users), Compliance (data residency), Price (differs by region). Tick marks beside each.]**

**(Voiceover):**
Region sirf distance ka sawaal nahi. Data ki kanooni zaroorat hoti hai: kuch data ko apne desh mein hi rakhna hota hai. Price har region mein alag hota hai. Aur har naya feature har region mein ek saath nahi aata. Seekhne ke liye aap kisi ek region mein hi kaam karo, taaki cheezein bikhri na rahein. Aur ek aam galti: instance ek region mein banaya, aur doosre region ke console mein dhundh rahe ho, aur lagta hai ki gayab ho gaya.

### [08:30 – 11:30] Scene 4: Lab: Console aur CLI se Region Dekho
**[VISUAL: Console's region selector. Terminal: `aws ec2 describe-regions --query "Regions[].RegionName" --output text`, `aws ec2 describe-availability-zones --region ap-south-1`.]**

**(Voiceover):**
Lab: AWS CLI install karke `aws configure` chalao, jisme IAM user ki access keys aur default region daalo. Phir `aws ec2 describe-regions --query "Regions[].RegionName" --output text` se regions ki list, aur `aws ec2 describe-availability-zones` se apne region ke AZ. Gino kitne AZ hain. Ye jaankari tab kaam aati hai jab hum load balancer aur Auto Scaling lagayenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Region → AZs → Edge · choose for latency, law, cost".]**

**(Voiceover):**
Recap: region, AZ, edge. Ab asli cheez: apna pehla server launch karte hain.

---

# 📺 EPISODE 3: Pehla EC2 Instance

### [00:00 – 01:15] Scene 1: Kiraye ka Computer, 2 Minute Mein
**[VISUAL: A "Launch instance" button. A progress bar. A server light turns green. Text: "2 minutes".]**

**(Voiceover):**
EC2, yaani Elastic Compute Cloud, AWS ka virtual server hai. Aap ek button dabate ho aur kuch minute mein ek Linux machine aapke saamne hoti hai. Aaj hum use step by step launch karenge aur har choice ka matlab samjhenge, taaki aap sirf next-next na dabao.

### [01:15 – 05:30] Scene 2: Launch Form ke Paanch Faisle
**[VISUAL: The EC2 launch wizard with five sections highlighted in turn: Name/tags, AMI, Instance type, Key pair, Network/Security group.]**

**(Voiceover):**
Paanch faisle. Ek, naam aur tags, taaki baad mein pata chale ye kiska hai. Do, AMI, yaani Amazon Machine Image, wo template jisse server banta hai: jaise Ubuntu ya Amazon Linux. Teen, instance type, jaise `t3.micro`, jisme CPU aur RAM tay hoti hai; naam ka pehla hissa family aur number generation batata hai. Chaar, key pair, jisse aap SSH se login karoge. Paanch, network aur security group, yaani virtual firewall. Seekhne ke liye free-tier eligible type chuno, jo console khud dikhata hai.

### [05:30 – 08:30] Scene 3: Security Group: Server ka Darwaza
**[VISUAL: A firewall card with inbound rules: SSH 22 from "My IP", HTTP 80 from anywhere. A red cross on "SSH from 0.0.0.0/0".]**

**(Voiceover):**
Security group ek virtual firewall hai. Inbound rules batate hain ki andar kya aa sakta hai. SSH ke liye port 22, aur isse sirf apne IP ke liye kholo, "My IP" option se, poori duniya ke liye nahi. Web server ke liye port 80 ya 443 sabke liye khola ja sakta hai. Outbound by default khula hota hai. Ek khaas baat: security group stateful hota hai, yani jo request andar aane di, uska jawab apne aap bahar jaa sakta hai.

### [08:30 – 11:30] Scene 4: Lab: Launch aur Connect
**[VISUAL: Final launch screen → instance state "Running" → copy public IPv4 → terminal `ssh -i key.pem ubuntu@<IP>`. Key file permission `chmod 400`.]**

**(Voiceover):**
Lab: ek Ubuntu ya Amazon Linux instance launch karo. Key pair banao, `.pem` file download hogi, ise surakshit rakho. Laptop par `chmod 400 key.pem`, warna SSH mana kar dega. Instance ke Running hote hi public IP copy karo aur `ssh -i key.pem ubuntu@IP` chalao; Amazon Linux mein user `ec2-user` hota hai. Login hone ke baad `uname -a` aur `df -h` chalao. Aapne abhi cloud mein ek asli server banaya.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "AMI · type · key pair · security group · SSH".]**

**(Voiceover):**
Recap: AMI, instance type, key pair, security group. Ab is server par kaam: automatic setup, aur sabse zaroori, band karna.

---

# 📺 EPISODE 4: Server par Kaam — SSH, User Data aur Cleanup

### [00:00 – 01:15] Scene 1: Har Baar Haath se Setup?
**[VISUAL: A person launching the 10th server and typing the same `apt install nginx` for the 10th time. A scroll labelled "user data" appears.]**

**(Voiceover):**
Ek server par haath se nginx install karna theek hai. Par dus servers par? Pagalpan. EC2 mein user data ek script hai jo instance ke pehli baar start hone par apne aap chalti hai. Isse har naya server khud taiyaar hota hai.

### [01:15 – 05:00] Scene 2: User Data aur Instance Metadata
**[VISUAL: A launch form's Advanced section with a user-data script. Terminal inside the instance: `curl` to the metadata endpoint showing instance-id.]**

**(Voiceover):**
User data mein ek shell script daalo, jo root ke taur par chalti hai:
```bash
#!/bin/bash
apt-get update -y
apt-get install -y nginx
echo "Hello from $(hostname)" > /var/www/html/index.html
```
Dhyaan: ye sirf pehle boot par chalti hai, aur uska output `/var/log/cloud-init-output.log` mein milta hai. Instance ke andar se metadata service se apni jaankari mil sakti hai, jaise instance-id; naye instances par IMDSv2 token ke saath use hota hai, jo ek surakshit tareeka hai. Metadata mein IAM role ki temporary credentials bhi hoti hain, isliye us endpoint tak access sambhal ke deni hoti hai.

### [05:00 – 08:30] Scene 3: Stop, Terminate aur Paisa
**[VISUAL: A state diagram: Pending → Running → Stopping → Stopped → Terminated. Billing markers: compute stops when Stopped, but EBS storage still billed.]**

**(Voiceover):**
Instance ke states samjho. Running mein compute ka paisa lagta hai. Stop karne par compute band, par uski disk, yaani EBS volume, ka paisa lagta rehta hai. Terminate karne par instance hamesha ke liye khatam, aur by default root disk bhi. Public IP bhi stop-start karne par badal sakta hai, jab tak Elastic IP na lagao. Isliye test ke baad terminate karo, sirf stop nahi, aur check karo ki koi volume ya Elastic IP bacha to nahi.

### [08:30 – 11:30] Scene 4: Lab: Web Server User Data se
**[VISUAL: A new instance launched with the user-data script, port 80 allowed in the security group. A browser shows the hello page. Then terminate and verify.]**

**(Voiceover):**
Lab: ek naya instance launch karo, user data mein upar wali script daalo, aur security group mein port 80 kholo. Do teen minute baad browser mein `http://PUBLIC_IP` kholo aur "Hello from" wali line dekho. Agar na dikhe to `cloud-init-output.log` padho, aur security group check karo. Kaam khatam hone par instance ko terminate karo, aur EC2 ke Volumes aur Elastic IPs ke page par dekho ki kuch bacha to nahi.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "user data · IMDSv2 · stop ≠ terminate · clean up".]**

**(Voiceover):**
Recap: user data se automatic setup, instance states, aur cleanup. Ab sawaal: kaun kya kar sakta hai aapke AWS account mein? Agla session IAM ka hai.

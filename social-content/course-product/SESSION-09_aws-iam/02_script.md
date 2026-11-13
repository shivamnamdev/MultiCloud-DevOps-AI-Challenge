# ✍️ 02: SCRIPT — SESSION-09: AWS IAM
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S09`
- **Focus:** Authentication vs authorization, IAM users/groups/policies, roles, least privilege, leaked-key response
- **Episodes:**
  - Episode 1: IAM kya hai: Who, What aur Which
  - Episode 2: Policies ka JSON: Allow, Deny aur Least Privilege
  - Episode 3: Roles: Keys ke Bina Safe Access
  - Episode 4: Security Hygiene: Access Keys, Rotation aur Leak Response

---

# 📺 EPISODE 1: IAM kya hai?

### [00:00 – 01:15] Scene 1: Ek Intern, Production Database
**[VISUAL: An intern at a desk with "AdministratorAccess" on a badge. A button "Delete production DB" glows. A hand stops the intern.]**

**(Voiceover):**
Ek intern ko galti se poore account ki admin power mil gayi, aur ek click mein production database delete ho gayi. Ye kahani kai companies ki hai. IAM, Identity and Access Management, wo system hai jo tay karta hai ki kaun kya kar sakta hai AWS mein. Cloud ka security yahi se shuru hota hai.

### [01:15 – 05:00] Scene 2: Authentication aur Authorization
**[VISUAL: A building: a security desk checks the ID (authentication), then a keycard opens only some floors (authorization).]**

**(Voiceover):**
Do shabd alag hain. Authentication matlab aap kaun ho: ID card dikhana. Authorization matlab aap kya kar sakte ho: aapka keycard kaun si manzil kholta hai. IAM dono sambhalta hai. Ek user ek insaan ya ek application ki pehchaan hota hai. Group users ki team hai, jaise Developers. Aur policy wo document hai jo likhta hai ki kya allowed aur kya denied hai. Policy users ya groups se judti hai, aur sahi design ye hai ki policy group se jode, har user se alag nahi.

### [05:00 – 08:30] Scene 3: IAM ke Building Blocks
**[VISUAL: A diagram: User → Group → Policy. A role sits separately with a "trust policy" and "permissions policy". AWS-managed vs customer-managed policies shown.]**

**(Voiceover):**
Policies do tarah ki hoti hain: AWS managed, jo AWS ne banayi, jaise `AmazonS3ReadOnlyAccess`, aur customer managed, jo aap banate ho apni zaroorat ke hisaab se. Role ek aisi pehchaan hai jisse koi bhi, user, service ya doosra account, temporarily assume kar sakta hai, bina permanent password ya key ke. IAM global service hai, yani region ke hisaab se nahi, poore account ke liye hai. Ye saari cheezein aap ek hi jagah se manage karte ho.

### [08:30 – 11:30] Scene 4: Lab: Group aur User Banao
**[VISUAL: Console: create group "Developers", attach `AmazonEC2ReadOnlyAccess`, create user "asha", add to group, enable MFA, sign in with the account alias URL.]**

**(Voiceover):**
Lab: IAM console mein ek group banao, `Developers`, aur usme `AmazonEC2ReadOnlyAccess` policy lagao. Phir ek user `asha` banao aur use us group mein daalo. User ke liye console password aur MFA set karo. Ab alias wale login URL se asha ke naam se sign in karo, aur EC2 ke page par jao. Instance dekh sakte ho, par launch ya terminate karne par "not authorized" aayega. Yahi hai authorization ka asli maza.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "User · Group · Policy · Role · MFA".]**

**(Voiceover):**
Recap: pehchaan aur permission alag cheezein hain, aur policy group se jodo. Ab ye policy andar se kaisi dikhti hai, aur least privilege kaise likhte hain.

---

# 📺 EPISODE 2: Policies ka JSON

### [00:00 – 01:15] Scene 1: Ek Line ka Farq
**[VISUAL: Two policy snippets. One has `"Resource": "*"` with a red glow, the other has one bucket ARN. A leak graphic hovers over the first.]**

**(Voiceover):**
Do policies ek jaisi dikhti hain. Ek mein `"Resource": "*"`, doosri mein ek khaas bucket ka naam. Pehli poore account ke saare buckets kholti hai. Ek line ka ye farq badi security incident aur safe system ke beech ka farq ho sakta hai. Aaj policy ko padhna seekhte hain.

### [01:15 – 05:00] Scene 2: Policy ka Structure
**[VISUAL: A JSON policy with four keys colour-coded: Effect, Action, Resource, Condition. Arrows from each to a plain-language sentence.]**

**(Voiceover):**
Policy ek JSON document hai jisme Statement ki list hoti hai. Har statement mein: Effect, Allow ya Deny. Action, kaun si API calls, jaise `s3:GetObject`. Resource, kis cheez par, ARN se, jaise `arn:aws:s3:::my-bucket/*`. Aur optional Condition, jaise sirf kisi IP se ya MFA ke saath. Isko ek vakya mein padho: "Is Effect ke saath, ye Actions, in Resources par, is Condition mein." Aise padhoge to koi bhi policy samajh aa jaati hai.

### [05:00 – 08:30] Scene 3: Evaluation Logic: Deny Sabse Upar
**[VISUAL: A flowchart: Request → explicit Deny? → yes: DENY. no → explicit Allow? → yes: ALLOW. no → DEFAULT DENY.]**

**(Voiceover):**
AWS decision aise leta hai. Pehle default sab kuch deny hota hai. Agar koi policy explicit Allow deti hai to access milta hai. Lekin agar kahin bhi explicit Deny likha hai, to wo sabse upar aata hai, chahe kitni bhi Allow ho. Isliye Deny ek bahut shaktishali cheez hai, aur use soch samajh kar use karo. Aur ek aur cheez: user ki policy aur group ki policy dono judti hain, aur sabka milakar total permission banta hai.

### [08:30 – 11:30] Scene 4: Lab: Least-Privilege S3 Policy
**[VISUAL: A policy editor with a JSON for one bucket. A test with the policy simulator: allowed GetObject, denied DeleteObject.]**

**(Voiceover):**
Lab: ek test bucket ke liye policy likho:
```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Action": ["s3:ListBucket", "s3:GetObject"],
    "Resource": ["arn:aws:s3:::my-test-bucket", "arn:aws:s3:::my-test-bucket/*"]
  }]
}
```
Ise `asha` ya group se jodo, aur IAM Policy Simulator mein `s3:DeleteObject` test karo, wo deny hona chahiye. Dhyaan: bucket aur uske objects ke ARN alag hote hain, isliye dono likhe gaye hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Effect · Action · Resource · Condition · explicit Deny wins".]**

**(Voiceover):**
Recap: policy ka structure, evaluation, least privilege. Ab sawaal: application ko AWS access chahiye to keys kahan rakhein? Jawab: roles.

---

# 📺 EPISODE 3: Roles — Keys ke Bina Safe Access

### [00:00 – 01:15] Scene 1: Keys Jo GitHub par Pahunch Gayi
**[VISUAL: A code file with AWS keys pasted inline. A GitHub push. A scanner bot flags it within seconds. Red "KEYS EXPOSED".]**

**(Voiceover):**
Ek developer ne application ko S3 access dene ke liye access keys code mein likh di, aur git push kar diya. Kuch hi minute mein bots ne wo keys dhoondh kar istemaal karna shuru kar diya. Is problem ka sahi hal keys ko hata dena hai, aur roles ka use karna.

### [01:15 – 05:00] Scene 2: Role aur Temporary Credentials
**[VISUAL: An EC2 instance wearing a "role badge". A box STS hands it temporary credentials with an expiry clock. The app uses them to access S3.]**

**(Voiceover):**
Role ek pehchaan hai jise koi trusted entity temporary taur par assume karti hai. EC2 instance par role lagao, to uske andar chalti application ko AWS khud temporary credentials deta hai, jo apne aap expire hoti hain aur badalti rehti hain. Na code mein key, na file mein. Role ke do hisse: trust policy, jo batati hai kaun ise assume kar sakta hai, aur permissions policy, jo batati hai assume karne ke baad kya kar sakta hai.

### [05:00 – 08:30] Scene 3: Role Kahan Kaam Aate Hain
**[VISUAL: Three icons: EC2 → S3, Lambda → DynamoDB, Account A → Account B. Each with a role arrow.]**

**(Voiceover):**
Teen aam jagah. Ek, EC2 ya container par chalti application ko doosri services tak pahunchana. Do, Lambda function ko kisi service ka access dena. Teen, ek AWS account se doosre account mein safe tareeke se jaana, jisme dono taraf ki permission zaroori hai. Aur jab aap CI/CD pipeline se AWS access karte ho, to bhi long-lived keys ki jagah role use karna aaj ka best practice hai.

### [08:30 – 11:30] Scene 4: Lab: EC2 Role se S3 Padho
**[VISUAL: IAM role "ec2-s3-read" created for EC2 with `AmazonS3ReadOnlyAccess`; attached to an instance. Inside the instance: `aws s3 ls` works without any `aws configure`.]**

**(Voiceover):**
Lab: IAM mein ek role banao, trusted entity EC2, aur policy `AmazonS3ReadOnlyAccess`. Ek instance par ye role lagao, Actions, Security, Modify IAM role. Instance mein SSH karo, AWS CLI install karo aur `aws sts get-caller-identity` chalao: aapko role ka naam dikhega. Phir `aws s3 ls`. Dhyaan do ki `aws configure` kahin nahi chalaya, aur access phir bhi mil raha hai. Ye hai keyless access.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Role = temporary creds · trust policy + permissions policy · no keys in code".]**

**(Voiceover):**
Recap: roles, temporary credentials, trust policy. Ab security ki aadatein: access keys ke saath kya karein aur kya na karein, aur agar keys leak ho jayein to kya karna hai.

---

# 📺 EPISODE 4: Security Hygiene

### [00:00 – 01:15] Scene 1: Ek Raat ki Galti
**[VISUAL: A phone buzzes: "Unusual activity". A billing graph jumps. A countdown timer: "Respond in minutes".]**

**(Voiceover):**
Subah uthe, billing alert dekha, aur account mein anjaane servers chal rahe hain. Keys leak ho gayi thi. Is waqt ghabrane ki jagah ek plan chahiye. Aaj hum IAM ki hygiene seekhte hain aur ek leak response checklist banate hain.

### [01:15 – 05:00] Scene 2: Best Practices ki Checklist
**[VISUAL: A checklist with ticks: MFA everywhere · No root for daily · Least privilege · Roles over keys · Rotate/remove old keys · Review access regularly.]**

**(Voiceover):**
Checklist. Root par MFA, aur root ka roz ka istemaal nahi. Har user ke liye minimum permission. Jahan ho sake keys ki jagah roles. Jo access keys chahiye, unhe regular rotate karo aur jo use nahi hoti, hata do. Console se "Last used" dekhkar purani keys pakdo. Aur IAM Access Analyzer jaise tools se pata lagao ki kaun si cheezein bahar ke logon ke liye khuli hain. Security ek baar ka kaam nahi, ek aadat hai.

### [05:00 – 08:30] Scene 3: Leak Response: Pehle Rok, Phir Dhoondh
**[VISUAL: A flow: 1 Deactivate key, 2 Check CloudTrail for what was done, 3 Remove unknown resources, 4 Create new key/role, 5 Delete old key, 6 Write post-mortem.]**

**(Voiceover):**
Agar keys leak hon: ek, turant us key ko deactivate karo, delete baad mein, pehle band karo. Do, CloudTrail logs mein dekho ki us key se kya kya hua. Teen, jo anjaane resources bane unhe hatao. Chaar, naya role ya key banao, aur code se purani wali hatao. Paanch, git history se bhi secret saaf karo, ya mani lo ki wo leak hi hai aur rotate karo. Chhe, kya hua aur kaise bachenge, ye likho. Ye order isliye hai kyunki pehle nuksaan rokna zaroori hai.

### [08:30 – 11:30] Scene 4: Lab: Key Banao, Test Karo, Deactivate Karo
**[VISUAL: Create an access key for a test user. `aws sts get-caller-identity` works. Console: key set to Inactive. Same command now fails with "InvalidClientTokenId".]**

**(Voiceover):**
Lab: ek test IAM user ke liye access key banao, aur CLI mein profile set karo. `aws sts get-caller-identity` chalao, sab theek. Ab console mein us key ko Inactive karo, aur wahi command dobara chalao. Ab error aayega. Aapne abhi leak response ka pehla kadam practice kiya. Phir user aur key ko delete kar do, kyunki test ke baad safai ki aadat hamesha rakhni hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "Rotate · remove unused · CloudTrail · deactivate first · post-mortem".]**

**(Voiceover):**
Recap: IAM ki hygiene aur leak response. Ab jab hum permission samajh gaye, to dobara server par chalte hain. Agle session mein EC2 ka storage aur scaling: disk, snapshot, AMI aur auto scaling.

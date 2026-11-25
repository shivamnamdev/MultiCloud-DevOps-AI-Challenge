# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-09_aws-iam

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,544 · **Episodes:** 4

---

# EPISODE 1: Landlord ke Office ka Staff

## Ek Intern, Poori Building ki Chaabi

Pichhle session mein Atithi ne apna lease surakshit kiya: owner ke paas master key aur doosra taala. Par ab Atithi mein kai log aayenge: developers, ek tester, ek intern. Kisi ko landlord ke office se kya karne diya jaye? Ek intern ko galti se poore account ki admin power mil gayi, aur ek click mein production ka database delete ho gaya. Ye kahani kai companies ki hai. Landlord ke office ka wo vibhag jo tay karta hai ki kaun kya kar sakta hai, uska naam IAM hai: Identity and Access Management. Cloud ki security yahin se shuru hoti hai.

## Do Alag Staff: Building ka aur Landlord ke Office ka

Ek baat pehle saaf kar lo, kyunki yahin sabse zyada confusion hota hai. Linux ka user wo staff hai jo ek building ke andar kaam karta hai: kamre kholta hai, files padhta hai. IAM ka user wo staff hai jo landlord ke office mein baithta hai, aur jo tay karta hai ki kaun si building kiraye par li jaye, kaun si todi jaye. Dono ke naam ek jaise ho sakte hain, jaise Session 4 ki asha aur aaj ki asha, par wo alag log hain, alag registers mein. Aur guests, yaani website ke end users, in dono mein se kisi ke staff nahi hain. Unhe ID card nahi milta. IAM mein bhi wahi sawal do hain: authentication, yaani aap kaun ho, ID dikhana. Aur authorization, yaani aap kya kar sakte ho, aapka keycard kaun si manzil kholta hai.

## User, Group, Policy aur Role

IAM mein chaar cheezein hain. User: ek insaan ya ek application ki pehchaan. Group: users ka ek vibhag, jaise Developers. Policy: wo permission letter jo likhti hai ki kya allowed hai aur kya nahi. Aur role: ek duty badge jo koi bhi, insaan ho ya service, kuch der ke liye pehen sakta hai. Role ke baare mein agle episodes mein. Sahi design ye hai ki permission letter group par lagao, har user par alag nahi. Naya developer aaya to use group mein daalo, aur kaam ho gaya. Policies do tarah ki hoti hain: AWS ki banayi hui, jaise AmazonEC2ReadOnlyAccess, aur aapki apni likhi hui. Aur IAM global hai, yaani Region ke hisaab se nahi, poore account ke liye ek hi jagah.

## Insaan ke Liye Aaj ka Tareeka

Ek sachchai: aaj kal companies insaan ko IAM user aur lambi chalne wali access key nahi deti. Wo ek single sign-on se, jise IAM Identity Center kehte hain, subah ek chhote samay ka badge deti hain. Isliye ki chaabi kho sakti hai, par badge shaam tak khatm ho jaata hai. Is course mein hum seekhne ke liye seedha IAM user banayenge, kyunki policy, group aur role ka khel wahi dikhata hai. Par jab asli kaam par jao, to pehle poochho ki aapki company badge wala raasta use karti hai ya nahi. Dhyaan rahe, Identity Center ke baare mein hum yahan sirf naam tak ruk rahe hain.

## Wahi Kaam Command se

Console mein click karna samajhne ke liye theek hai, par staff ko ek baar nahi, kai baar rakhna hota hai. Isliye wahi kaam command se bhi karo. aws iam create-group --group-name Developers vibhag banata hai. aws iam attach-group-policy mein group ka naam aur policy ka ARN do, jaise arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess, to letter vibhag par lag jaati hai. aws iam create-user --user-name asha-aws naya staff, aur aws iam add-user-to-group use vibhag mein daalta hai. aws iam list-groups-for-user --user-name asha-aws se tasalli kar lo. Ye chaar kadam hain jo aage Terraform ek hi document mein likh dega, aur wahi dikhayega ki kya badlega. Aur yaad rakho, ye commands tabhi chalengi jab aapke apne user ko IAM ka haq ho, root ki keys se kabhi nahi.

## Lab: Group aur User Banao

Lab. IAM console mein ek group banao, Developers, aur usme AmazonEC2ReadOnlyAccess lagao. Phir ek user banao, jaise asha-aws, taaki Linux ki asha se alag dikhe, aur use group mein daalo. User ko console password do aur MFA lagao. Ab ek private window mein account alias wale URL se asha ke naam se sign in karo. EC2 ke page par jao. Aap buildings dekh sakte ho, par launch ya terminate karne par "not authorized" aayega. Yahi authorization ka asli maza hai. Account ID aur alias dono kisi se bina soche share mat karo, aur root se wapas isi tarah kaam karna band kar do.

## Recap aur Bridge

Recap: authentication aur authorization alag hain, Linux ke staff aur landlord ke office ke staff alag hain, aur permission letter group par lagti hai. Ab wo letter andar se kaisi dikhti hai, aur kam se kam haq wali letter kaise likhte hain.

---

# EPISODE 2: Permission Letter ka JSON

## Ek Line ka Farq

Do permission letters ek jaisi dikhti hain. Ek mein Resource ki jagah sirf ek sitara, "*", yaani sab kuch. Doosri mein ek khaas bucket ka naam. Pehli account ke saare buckets khol deti hai, doosri sirf ek. Ek line ka ye farq ek badi security incident aur ek surakshit system ke beech ka farq ho sakta hai. Aaj hum letter padhna seekhte hain.

## Letter ke Chaar Hisse

Policy ek JSON document hai, jisme Statement ki ek list hoti hai. Har statement mein chaar cheezein. Effect: Allow ya Deny. Action: kaun si API calls, jaise s3:GetObject. Resource: kis cheez par, ARN naam se, jaise arn:aws:s3:::my-test-bucket/*. Aur Condition, jo zaroori nahi hai, jaise sirf kisi IP se ya sirf MFA ke saath. Letter ko ek vakya mein padho: "Is Effect ke saath, ye Actions, in Resources par, is Condition mein." Is tarah padhoge to koi bhi policy samajh aa jaati hai. Ek aur chhoti baat: upar ek Version line hoti hai, 2012-10-17, jo hamesha wahi rakhi jaati hai.

## Faisla Kaise Hota Hai: Deny Sabse Upar

AWS ka faisla ek tay kram mein hota hai. Pehle sab kuch by default deny hai. Agar koi letter explicit Allow deti hai, to access milta hai. Par agar kahin bhi explicit Deny likha hai, to wo sabse upar aata hai, chahe kitni bhi Allow ho. Isliye Deny bahut shaktishali hai, aur use soch samajh kar use karo. User ki apni letters aur group ki letters, sab milakar user ki kul permission banati hain. Do aur parat baad mein milengi. Permissions boundary: ek seema jo bataati hai ki kisi user ko zyada se zyada kya mil sakta hai, chahe use kuch bhi diya jaye. Aur ek company ke bahut saare accounts par ek upar wali rok, jise service control policy kehte hain. Abhi sirf naam yaad rakho.

## Letter ke Do Qism: Kisko aur Kispar

Ab tak letter insaan ke paas rahi: wo identity-based policy hai. Kuch cheezon par letter khud us cheez par bhi lag sakti hai, jaise ek bucket par. Use resource-based policy kehte hain, aur usme ek aur line hoti hai: Principal, yaani kisko. S3 bucket policy iska udaharan hai, jisse hum S3 ke session mein milenge. Aur agar aapko kuch sirf tab allow karna ho jab MFA lagi ho, to Condition mein aws:MultiFactorAuthPresent ko true maango. Jaise sirf wo user instance band kar sake jisne aaj second lock se login kiya ho. Condition hi wo jagah hai jahan letter sakht ya dheeli banti hai.

## Access Denied Aaye to: Kaun Rok Raha Hai?

Sabse aam IAM ka sawaal: "mujhe Access Denied kyun mil raha hai?" Panch shak karo. Pehla, user ya group ki letter mein wo action likha hi nahi. Doosra, kahin ek explicit Deny likha hai, jo sabse upar aata hai. Teesra, permissions boundary ya company ki upar wali rok, jise service control policy kehte hain, wo seema laga rahi hai. Chautha, resource ki apni policy, jaise bucket policy, kisi aur ko hi allow kar rahi hai. Paanchwa, Condition: jaise MFA wali shart poori nahi hui. Kuch services error ke saath ek lamba encoded message deti hain, use aws sts decode-authorization-message se padha ja sakta hai, aur wo batata hai ki kaun si policy ne rok. Aur CloudTrail mein wahi call errorCode: AccessDenied ke saath likhi milti hai. Pehle yaad karo kaun sa action aur kaun sa resource, phir un panch jagah mein se ek ek ko dekho.

## Lab: Least-Privilege Bucket Letter

Lab. Ek test bucket ke liye ek letter likho:

Bucket ka asli naam apna daalo, aur isse Developers group ya asha-aws se jodo. Phir IAM Policy Simulator kholo, user ya group chuno, aur s3:GetObject test karo, wo allowed hona chahiye. Ab s3:DeleteObject test karo, wo deny hona chahiye, kyunki letter mein likha hi nahi. Dhyaan do: bucket aur uske andar ki cheezon ke ARN alag hote hain, isliye dono likhe gaye hain. Ek ko chhodoge to ya list nahi chalegi ya objects nahi khulenge.

## Recap aur Bridge

Recap: letter ka structure, faisla karne ka kram, aur kam se kam haq. Ab ek sawaal jo har application ke saamne aata hai: building mein chal rahe app ko landlord ke office se kuch maangna ho, to chaabi kahan rakhe? Jawab: duty badge, yaani role.

---

# EPISODE 3: Duty Badge

## Chaabi jo GitHub par Pahunch Gayi

Ek developer ne application ko bucket tak pahunchane ke liye access key seedhi code mein likh di, aur git push kar diya. Kuch hi minute mein bots ne wo keys dhoond li, aur Atithi ke lease par saikdon buildings kiraye par li jaane lagi. Session 16B mein humne dekha tha ki ek baar vault mein gaya secret wapas nahi aata. Is problem ka sahi hal keys ko chhupana nahi, hata dena hai. Aur uske liye hai role.

## Role aur Temporary Credentials

Role ek duty badge hai. Koi trusted insaan ya service use kuch der ke liye pehen leti hai. Building par role lagao, to uske andar chalti application ko AWS khud ek chhoti umr wali credential deta hai. Wo kuch ghante mein khatm ho jaati hai aur apne aap badalti rehti hai. Na code mein key, na kisi file mein. Is badge ke do hisse hain. Trust policy: kaun ise pehen sakta hai, jaise EC2 service. Permissions policy: pehen kar kya kar sakta hai. EC2 ke saath role ek wrapper mein aata hai, jise instance profile kehte hain. Console ye khud bana deta hai, par CLI aur Terraform mein aap use alag dekhoge. Session 8 ka metadata address yaad hai? Wahin se building ko ye badge ki credentials milti hain.

## Badge Kahan Kaam Aate Hain

Teen aam jagah. Ek, EC2 ya container par chalti application ko doosri service tak pahunchana, jaise bucket tak. Do, ek Lambda function, yaani on-call freelancer, ko kisi service ka access dena. Teen, ek AWS account se doosre account mein surakshit tareeke se jaana: ek taraf trust, doosri taraf permission. Aur ek chautha, jo Jenkins aur GitHub ke sessions mein aayega: jab CI/CD pipeline AWS tak pahunchta hai, to bhi lambe samay ki key ki jagah badge ya temporary credentials ka use aaj ka behtar tareeka hai.

## Badge Haath se Pehen kar Dekho

Badge pehenne ka kaam ek command bhi karti hai: aws sts assume-role aur role ka ARN. Jawab mein teen cheezein aati hain: access key, secret key aur ek session token, aur ek expiry ka samay. Teeno ek saath chalte hain, aur expiry ke baad bekaar. Ek kaam ki baat: jab key kisi ke haath lag bhi jaaye, to wo ghante bhar mein khatm ho jaati hai, jabki IAM user ki lambi key tab tak chalti hai jab tak aap use band na karo. Yahi badge ki sabse badi taakat hai. Isko aap pehle IAM user se try karo, jab user ko us role par assume karne ki ijaazat ho.

## Lab: EC2 Role se Bucket Padho

Lab. IAM mein ek role banao. Trusted entity: EC2. Policy: AmazonS3ReadOnlyAccess. Naam ec2-s3-read. Ab Session 8 ki ek building launch karo, aur Actions, Security, Modify IAM role se ye role lagao. Building mein SSH karo. Agar AWS CLI nahi hai to install karo. aws sts get-caller-identity chalao, aur jawab mein assumed-role/ec2-s3-read dikhega, yaani aapne badge pehna hai. Phir aws s3 ls, buckets ki list aa jaati hai. Dhyaan do: ek bhi baar aws configure nahi chalaya, aur access mil raha hai. Ye hai keyless access. Lab ke baad building ko terminate karo, aur role ko tabhi hatao jab use kuch nahi use kar raha ho.

## Recap aur Bridge

Recap: duty badge, temporary credentials, trust aur permissions ke do hisse. Ab chaabi ki safai: jo keys abhi bhi rakhni padti hain, unke saath kya karein, aur agar keys leak ho jayein to pehle kya karein.

---

# EPISODE 4: Chaabi ki Safai

## Ek Raat ki Galti

Subah uthe, billing alert dekha, aur account mein anjaane buildings door door ke shehron mein chal rahi hain. Chaabi leak ho gayi thi. Is waqt ghabrane ki jagah ek plan chahiye, aur wo plan pehle se likha hona chahiye. Aaj hum chaabi ki safai ki aadatein seekhte hain, aur ek leak response checklist banate hain.

## Safai ki Checklist

Checklist. Har insaan par MFA, aur root ka roz ka istemaal nahi. Har user ko kam se kam permission. Jahan ho sake, keys ki jagah roles. Jo access keys ab bhi chahiye, unhe regular rotate karo aur jo use nahi hoti, hata do. Console mein har key ke saamne "Last used" dikhta hai, usse purani keys pakdi jaati hain. IAM Access Analyzer jaisa tool bata deta hai ki kaun si cheezein bahar ke logon ke liye khuli hain. Aur ek budget alert, jo Session 8 mein lagaya tha, wahi ghanti hai jo pehle bajti hai. Security ek baar ka kaam nahi, ek aadat hai.

## Leak Response: Pehle Rok, Phir Dhoondh

Agar keys leak ho jaayein, to ek hi kram yaad rakho. Ek: turant us key ko deactivate karo. Delete baad mein, pehle band karo, taaki saboot na jaaye. Do: CloudTrail logs mein dekho ki us key ne kya kya kiya, kaun si Region mein. CloudTrail landlord ka wo register hai jisme har call likhi jaati hai. Teen: jo anjaane buildings, users aur keys bane, unhe hatao. Chaar: naya role ya, na ho sake to, nayi key banao. Paanch: code se aur git history se purani key ke saare nishaan hatao, aur sab se zaroori, maan lo ki wo key hamesha ke liye public ho chuki hai, isliye use delete hi kar do. Chhe: likho ki kya hua aur kaise bachenge. Ye kram isliye hai ki sabse pehle nuksaan rokna zaroori hai. Kabhi kabhi AWS khud bhi ek quarantine policy laga deta hai jab use pata chalta hai ki key public jagah par aa gayi, par us par bharosa mat karo.

## Purani Chaabiyan Dhoondhna

Purani aur bhoole hue keys dhoondhne ke liye ek report hai. aws iam generate-credential-report ek report banata hai, aur aws iam get-credential-report use laata hai. Ye report ek base64 text mein aati hai, isliye --query Content --output text ke baad base64 -d lagao, aur ek CSV table milti hai. Usme har user ke saamne dikhta hai ki password aur keys kab aakhri baar use hui. Kisi user ki key ek mahine se zyada use nahi hui? Wo candidate hai deactivate karne ki. Ek user ki keys aws iam list-access-keys --user-name asha-aws se dikhti hain, aur aws iam get-access-key-last-used batata hai ki ek key ka aakhri use kab hua. Ye pichhle session ki Python wali report jaisa kaam hai: ek chhota loop likh kar roz ye report padhna sambhav hai.

## Lab: Key Banao, Test Karo, Band Karo

Lab. Ek test IAM user ke liye access key banao, aur CLI mein ek alag profile leaktest mein daalo. aws sts get-caller-identity --profile leaktest chalao, sab theek. Ab console mein us key ko Inactive karo, aur wahi command dobara chalao. Error aayega: InvalidClientTokenId. Aapne abhi leak response ka pehla kadam practice kiya. Phir key, user aur profile teeno delete kar do. ~/.aws/credentials mein se leaktest ke lines bhi hata do. Aur ek sawal apne aap se: Atithi ki is lab ke saath, kya koi key kisi file, kisi history ya kisi screenshot mein reh gayi? Test ke baad safai ki aadat hamesha rakhni hai.

## Recap aur Bridge

Recap: chaabi ki safai aur leak response. Ab Atithi ke paas ek surakshit lease hai aur kaun kya kar sakta hai ye tay hai. Agle session mein hum wapas building ke paas jaate hain: usme storeroom jodna, uski photograph lena, building ko photocopy karna, aur shaadi ke season mein extra buildings kholna.

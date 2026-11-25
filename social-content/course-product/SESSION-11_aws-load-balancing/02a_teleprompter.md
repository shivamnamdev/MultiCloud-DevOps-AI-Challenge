# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-11_aws-load-balancing

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,559 · **Episodes:** 4

---

# EPISODE 1: Campus ka Marshal

## Ek Counter, Sau Log

Pichhle session mein Atithi ne shaadi ke season ke liye buildings ko photocopy karna seekha. Ab maan lo bees buildings khuli hain. Guest kis building mein jaye? Ek bank mein ek hi counter khula ho aur sau log line mein hon. Ab ek marshal bula lo jo sabko khaali counter par bhej de. Load balancer wahi marshal hai. Wo guests ki requests ko kai buildings mein baant deta hai, aur jo building kharab ho use chhod kar sirf theek buildings ki taraf bhejta hai.

## Marshal ke Teen Kaam

Marshal ke teen kaam hain. Ek, load baantna, taaki koi ek building na jale. Do, health check: wo har building se poochta rehta hai "kya aap khule ho?", aur jo jawab nahi deti use guest nahi bhejta. Teen, ek hi address: guests ek hi naam par aate hain, aur peeche buildings badalti, badhti aur ghat-ti rehti hain. Isliye marshal aur Auto Scaling hamesha saath chalte hain, ek buildings ki ginti sambhalta hai aur doosra unka raasta. AWS mein is service ka naam Elastic Load Balancing, ELB, hai, aur wo kai tower mein ek saath phailti hai.

## Baantne ke Tareeke aur Chipakna

Marshal guests ko kai tareekon se baant sakta hai. Baari baari se, yaani round robin. Ya us building ko jisme sabse kam guests hain. Kabhi kabhi ek guest ko ek hi building par chipkana padta hai, jaise jab uski kahani us building mein rakhi ho. Ise sticky session kehte hain, aur ye ek cookie se hota hai. Par sticky sessions scaling ko mushkil banate hain: wo building gayi to guest ki kahani gayi. Behtar design: building mein kahani mat rakho. Session ko database ya cache mein rakho, taaki koi bhi building kisi bhi guest ko sambhal sake. Session 10 mein humne ise stateless kaha tha.

## Marshal Guest ka Pata Kaise Batata Hai

Ek chhoti par aham baat. Jab marshal guest ko building tak bhejta hai, to building ko request marshal se aati dikhti hai, guest se nahi. Isliye building ke logbook mein har guest ka address marshal ka hi hota hai. Guest ka asli address marshal ek chhote header mein likh kar bhejta hai, jiska naam X-Forwarded-For hai. Nginx ya app ko wo header padhna aur logbook mein likhna sikhana padta hai. Ye security aur debugging dono ke liye zaroori hai, kyunki warna "koi bahut requests bhej raha hai" ka pata hi nahi chalta ki wo kaun hai. Ek aur dhyaan: ye header koi bhi guest khud bhi bhej sakta hai, isliye usse bharosemand sirf wahi hissa maano jo aapke apne marshal ne likha.

## Lab: Do Buildings, Do Pages

Lab ki taiyaari. Do buildings launch karo, alag alag towers mein, yaani alag AZ mein. User data wahi jo Session 8 mein tha, par page mein building ka naam:

Security group mein 80 kholo. Dono ke public address do alag tabs mein kholo: do alag naam dikhne chahiye. Agle episodes mein inhi ke aage marshal khada karenge. Abhi in dono ko chalta rehne do.

## Recap aur Bridge

Recap: marshal kya karta hai, kyun, aur guest ka asli address kahan milta hai. Ab AWS ke options: ALB aur NLB, aur kab kaun.

---

# EPISODE 2: Do Tarah ke Marshal

## Dak Ghar vs Courier

Do tarah ke courier socho. Ek letter ko khol kar padhta hai aur andar likhe ke hisaab se sahi vibhag mein bhejta hai. Doosra sirf sealed parcel ko bahut tez forward karta hai, bina khole. AWS ke marshals mein bhi yahi farq hai.

## Application Load Balancer

Application Load Balancer, ALB, wo marshal hai jo letter khol kar padhta hai. Wo OSI ki layer 7 par kaam karta hai, yaani HTTP aur HTTPS samajhta hai. Wo request ka path, host naam, header ya query dekhkar routing karta hai. Jaise /api/* booking ki API wali buildings ko, /photos/* photo wali buildings ko, aur admin.atithi.example admin wali buildings ko. Ek hi marshal ke peeche kai alag services chal sakti hain, isliye microservices aur containers ke liye ALB natural choice hai. Wo WebSocket aur HTTP/2 jaise naye tareeke bhi sambhalta hai. Aur wo apne aap kai towers mein cross-zone baantta hai.

## Network Load Balancer aur Baaki

Network Load Balancer, NLB, wo marshal hai jo parcel nahi kholta. Wo layer 4 par TCP aur UDP ko bahut tez, bahut kam deri ke saath forward karta hai. Har tower ke liye ek pakka address mil sakta hai, jo tab kaam aata hai jab client ko firewall mein ek fixed address likhna ho. Aur wo guest ka asli address building tak le jaata hai. Gateway Load Balancer ek aur marshal hai, jo security appliances, jaise inspection wale firewalls, ke liye hai. Classic Load Balancer purana hai aur naye kaam ke liye nahi chuna jaata. Seedha niyam: web aur HTTP ke liye ALB. Bahut tez ya non-HTTP traffic ke liye, ya fixed address ke liye, NLB.

## Marshal ki Suchi: Listener aur Rules

Marshal ke paas ek suchi hoti hai. Listener batata hai kaun se darwaze, yaani port, par wo sunega, jaise 80 ya 443. Listener ke andar rules: pehla rule, agar path /api/ se shuru ho to API wali buildings ko. Doosra rule, agar host admin ka ho to admin ko. Aur ek default rule, jo baaki sabko sambhalta hai. Rules ko ek tay kram mein dekha jaata hai, pehla jo milta hai wahi chalta hai, isliye kram ka dhyaan rakho. Ye wahi case ka tareeka hai jo Session 6 mein dekha tha: ek lambi if ki chain ki jagah saaf suchi.

## Marshal ka Kharch aur Ek Marshal ya Kai?

Marshal ka bhi kiraya lagta hai: ek hissa ghante ka, jab tak wo khada hai, aur ek hissa is par ki kitni baat-cheet usne sambhali. Isliye agar Atithi ki paanch chhoti services hain, aur aap har ek ke liye alag marshal khada kar do, to paanch ghante ke kiraye lagte hain. Ek marshal ke paanch rules sasta padta hai. Par iske apne sauda hain: ek rule ki galti paanchon services ko hila sakti hai. Isliye bade ya alag teams ke liye kabhi kabhi alag marshal hi theek hota hai. Ek aur jaankari: jis marshal ka koi target nahi bacha, wo bhi bill banata hai. Isliye lab ke baad hamesha use hatao.

## Lab: Faisla Karo (Kagaz par)

Lab (kagaz par). Chhe situations ke liye tay karo ALB ya NLB. Path ke hisaab se routing: ALB. UDP par game server: NLB. Client ko ek fixed address chahiye: NLB. Normal website ke liye HTTP routing: ALB. Bahut zyada TCP traffic, HTTP samajhne ki zaroorat nahi: NLB. WebSocket wala chat app: ALB. Har jawab ke saath ek line likho ki kyun. Ye "kyun" hi interview mein poochha jaata hai, aur asli design meeting mein bhi. Ek ulta sawaal bhi socho: ALB ke saath fixed address chahiye to? Uske aage NLB ya Global Accelerator naam ki service lagti hai. Abhi bas ye yaad rakho ki jawab maujood hai.

## Recap aur Bridge

Recap: ALB aur NLB, listener aur rules. Ab andar ke hisse: target group, health check, aur sealed envelope, yaani HTTPS.

---

# EPISODE 3: "Kya Aap Khule Ho?"

## Marshal ko Kaise Pata Building Khuli Hai?

Marshal har building ke paas ek chhota messenger bhejta rehta hai: "kya aap khule ho?" Jo jawab nahi deti, use list se hata deta hai. Jab wo wapas theek ho jaye, use phir list mein jod leta hai. Ye sab target group aur health check se hota hai.

## Target Group aur Health Check

Target group buildings ka wo set hai jise marshal guests bhejta hai. Targets buildings, IP address, ya Lambda ho sakte hain. Health check mein aap path dete ho, jaise /health, interval, aur kitni baar lagataar fail ya pass hone par building unhealthy ya healthy maani jaye. Console mein iske default dikhte hain, unhe dekh kar hi tay karo. Achha health endpoint sirf "200 OK" nahi deta. Wo ye bhi dekhta hai ki building ke zaroori hisse, jaise database ka connection, kaam kar rahe hain. Par ise bhaari mat banao: agar har health check ek lamba kaam kare, to khud health check load ban jaata hai. Aur ek aur baat: agar saari buildings ek saath unhealthy dikhein, to marshal sabko dobara guests bhejne lagta hai, kyunki sab band hone se behtar hai ki kuch to kaam kare.

## Sealed Envelope: TLS aur Certificate

HTTPS ke liye certificate chahiye. Guest aur marshal ke beech baat sealed envelope mein hoti hai: ye TLS hai. AWS Certificate Manager, ACM, mein aap certificate le sakte ho, aur ALB ke 443 wale listener par laga sakte ho. Isse TLS termination kehte hain: envelope marshal ke gate par khulta hai, aur peeche buildings ko ya to seedha HTTP ya naye setup mein phir HTTPS mein bheja jaata hai. Port 80 par ek listener rakho jo guest ko 443 par redirect kare, taaki koi bina envelope ke na jaaye. Certificate ek domain ke naam par hota hai, aur ACM ye pakka karne ke liye DNS validation maangta hai, yaani aapko dikhana padta hai ki wo domain aapka hai. Isliye is hisse ko tabhi chalao jab aapke paas apna domain ho.

## Naam se Pata: Route 53

Ab tak guest ko ALB ka lamba sa DNS naam dena padta tha. Asli guest ko www.atithi.example chahiye. Naam se address ka kaam directory, yaani DNS, karti hai, aur AWS ki directory Route 53 hai. Domain registrar se milta hai. Route 53 mein ek hosted zone banate ho, yaani us domain ke records ka register. Zone aapko chaar name servers deta hai, aur registrar ko batana padta hai ki ab ye chaar is domain ki directory hain. Phir marshal ke liye ek alias record: type A, target aapka ALB. Alias isliye ki ALB ke IP badalte rehte hain, aur Route 53 unhe khud follow karta hai. CNAME bhi ek naam ko doosre naam se jod sakta hai, par zone ke sabse upar wale naam, yaani atithi.example, par CNAME ban hi nahi sakta, aur Route 53 AWS ke resources ki alias queries ka charge nahi leta. Isliye ALB, CloudFront aur S3 website ke liye alias. Route 53 mein routing policy bhi hoti hai: simple, weighted, latency, failover, aur health check bhi. Lab, agar apna domain hai: www ke liye A alias banao, target mein ALB chuno, aur dig www.atithi.example ya nslookup se jawab dekho. Domain nahi hai to ALB ka DNS naam kaafi hai.

## Health Check Fail Hone par Kya Hota Hai

Health check fail ho to console mein target ke saamne ek wajah likhi hoti hai. Usse seedha sahi jagah jao. Timeout aaye, to marshal tak building pahunchi hi nahi: security group ne marshal ko roka, ya port galat hai. Galat status code aaye, jaise 404 jab 200 chahiye tha, to ya to path galat hai ya app ne jawab galat diya. Connection refused aaye, to building mil gayi par us port par koi service sun hi nahi rahi. Ye wahi layer-by-layer soch hai jo Session 5 aur Session 8 mein thi: kaun si parat tak pahunche aur kahan ruke.

## Lab: Marshal Khada Karo

Lab. Pehle target group web-tg: protocol HTTP, port 80, health check path /, aur Episode 1 ki do buildings register karo. Phir ek Application Load Balancer banao: internet-facing, do alag towers ke subnets, aur uska apna naya security group jisme 80 duniya ke liye khula ho. Listener 80 ko web-tg par forward karo. Provisioning ke baad ALB ka DNS naam browser mein kholo, aur baar baar refresh karo: building ka naam badalta dikhega. Ab ek building par sudo systemctl stop nginx chalao. Kuch der mein uska target unhealthy dikhega, aur saare guests sirf doosri building ko jaayenge. Phir nginx wapas chalu karo aur dekho ki target phir healthy ho jaata hai.

## Recap aur Bridge

Recap: target group, health check, aur HTTPS ka sealed envelope. Ab sab ko jodte hain: marshal ke peeche Auto Scaling Group, aur jab sab toote to kya dekhein.

---

# EPISODE 4: Marshal ke Peeche Shaadi ka Season

## Khud Theek, Khud Badhne Wali Site

Ab Atithi wo architecture banata hai jo asli companies chalati hain: ek marshal, uske peeche Auto Scaling Group, do towers mein. Building mare to nayi khud aati hai. Shaadi ke season mein buildings badh jaati hain. Aur guest ko ye sab dikhta bhi nahi.

## Door Guards ki Zanjeer

Ek achha pattern: marshal ke door guard ki list mein 80 aur 443 poori duniya ke liye kholo. Buildings ke door guard ki list mein port 80 sirf marshal ke guard se allow karo. Yahan source mein IP range nahi, balki marshal ka security group likho. Isse buildings seedha internet se nahi, sirf marshal ke raaste se hi milti hain. Ye defence in depth ka seedha udaharan hai, aur isse buildings ke public address ki zaroorat bhi kam ho jaati hai. Aage VPC ke sessions mein hum buildings ko private wing mein rakhne tak ye soch le jayenge.

## ASG ko Marshal se Jodna

ASG ko target group se attach karo. Ab ek zaroori setting: health check type ko EC2 se ELB karo. EC2 type tabhi building badalta hai jab building khud mar jaye. ELB type tab bhi badalta hai jab marshal use unhealthy dekhe, chahe building chal rahi ho par site na chal rahi ho. Saath mein ek grace period do, taaki nayi building ko boot hone ka samay mile, aur wo turant unhealthy na maani jaye. Aur jab building hatayi jaati hai, to marshal pehle chal rahe guests ko khatam hone deta hai. Isko deregistration delay kehte hain, jo by default kuch minute hota hai. Isse guest beech mein nahi kat-ta.

## Gadbad ho to: 502, 503, 504

Marshal ke error numbers samjho, kyunki wahi raasta dikhate hain. 502: marshal ko building se aisa jawab mila jo wo samajh nahi paya, ya building ne beech mein baat kaat di. App ke logs dekho, aur ye ki app crash to nahi hui. 503: marshal ke paas bhejne ke liye koi registered building hi nahi hai. Target group khaali to nahi, ya ASG ne kuch register kiya hi nahi? 504: building ne samay par jawab nahi diya. App dheema hai, ya security group beech mein hai, ya marshal ka idle timeout app ke kaam se chhota hai. Pehle target group mein health dekho, phir security groups, phir app ke logs. Aur marshal ka apna access log, jo ek bucket mein likha ja sakta hai, har request ka nateeja aur wajah dikhata hai.

## Naya Version Dheere Dheere: Weighted Target Groups

Marshal ek aur kaam kar sakta hai: ek rule ke andar do target groups ko alag alag hissa de sakta hai. Maan lo booking page ka naya version web-v2 taiyaar hai. Pehle sirf dus percent guests use do, nabbe purane ko. Agar naye ke errors nahi badhe, to pachaas, phir sau. Aur agar kuch bigde, to ek hi badlaav mein sab wapas purane par. Isko canary release kehte hain: ek chhoti tukdi pehle. Aage Jenkins aur Kubernetes ke sessions mein hum yahi sochenge, par yahan ye ALB ki taakat dikhne ka sabse saaf udaharan hai. Aur isse yaad aata hai ki ALB ka kaam sirf baantna nahi, deploy ko surakshit banana bhi hai.

## Lab: Building Todo aur Dekho

Lab. Session 10 ke AMI se ek launch template aur ek ASG banao: minimum 2, maximum 4, web-tg se attached, health check type ELB. Episode 1 ki do haath se banayi buildings ko ab target group se hata do aur terminate kar do. Ab ASG ki nayi buildings dikhengi, aur ALB ka DNS naam kholne par page chalega. Ek building ko haath se terminate karo, aur dekho ki ASG nayi bana deta hai, aur marshal ki list mein healthy count wapas do ho jaata hai. Phir ek building par nginx band karke dekho ki marshal use unhealthy maan kar ASG ko batata hai, aur ASG use badal deta hai. Aakhir mein safai ka kram: ASG, phir ALB, phir target group, phir AMI aur uska snapshot. ALB ghante ke hisaab se chalta hai, isliye ise sabse pehle mat bhoolna.

## Recap aur Bridge

Recap: ek highly available web architecture: marshal, Auto Scaling, door guards ki zanjeer, aur error numbers. Ab Atithi ki site ke paas apna gate, apni buildings aur apna storage hai. Par booking site ki photos aur brochures ke liye building ka storeroom bahut mehnga aur bahut chhota hai. Agla session ek anant gaudam, S3, ka hai: jahan files internet ke paimane par rakhi jaati hain, building mein nahi. Aur cleanup: ALB aur ASG delete karna na bhoolna.

# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-15_aws-monitoring-and-serverless

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,480 · **Episodes:** 4

---

# EPISODE 1: Meters aur Alarm

## Guest ne Bataya, Humein Pata Hi Nahi

Shaadi ke season ki ek raat. Booking site dheemi hui, phir band ho gayi. Atithi ko pata kaise chala? Ek guest ne social media par likha. Isse sharminda karne wali baat kam hai. Monitoring ka pura maksad yahi hai ki pehle aapko pata chale, guest ko nahi. Pichhle sessions mein humne buildings, godown, records office aur campus banaya. Ab landlord ke paas jo meters aur CCTV pehle se lage hain, unka istemaal seekhte hain. Is poore system ka naam CloudWatch hai.

## Metric, Namespace aur Dimension

Metric ek meter ki reading hai jo samay ke saath badalti hai, jaise building ka CPU. Teen shabd yaad rakho. Namespace: ye meter kis service ka hai, jaise AWS/EC2. Metric ka naam: CPUUtilization. Dimension: ye reading kis cheez ki hai, jaise kaun si building, InstanceId. Aur statistic: us period ka average, maximum ya total. EC2 ke basic metrics paanch minute par aate hain, detailed monitoring ek minute par, jo alag paisa leti hai. Ek zaroori jaal: building ka memory aur disk bharna landlord ko dikhta hi nahi, kyunki wo building ke andar ki baat hai. Unke liye CloudWatch agent building par lagana padta hai.

## Kya Dekhna Chahiye

Meter bahut hain, par har meter ka alarm nahi lagana. Chaar cheezein dekho. Latency: guest ko jawab kitni der mein mila. Traffic: kitne guests aa rahe hain. Errors: kitne request fail hue. Saturation: koi cheez bhar to nahi rahi, jaise CPU, disk ya Session 13 ke database ke connections. Atithi ke liye ye marshal ka TargetResponseTime, RequestCount aur 5xx ginti, building ka CPU, aur database ke connections hain. Session 10 ka ek aur point yaad rakho: T-series building mein CPU credits bhi ek meter hain, aur wo khatam ho jaayein to CPU achanak dheema ho jaata hai.

## Alarm: Meter par Nazar

Alarm ek meter par nazar rakhta hai aur ek shart likhta hai: "agar CPU 70 se upar ho, paanch minute ke teen mein se do readings mein, to ALARM." Alarm ki teen states hain: OK, ALARM, aur INSUFFICIENT_DATA, jab abhi kaafi readings nahi mili. Ek chhota setting zaroori hai: missing data ko kaise maanein. Agar building band hai aur reading nahi aa rahi, to alarm ko ALARM dikhana chahiye ya OK, ye aap tay karte ho. Action mein aap topic par notification bhej sakte ho, Auto Scaling ki policy chala sakte ho, ya EC2 ki building ko reboot, recover ya stop karwa sakte ho. Rule: har alarm ke peeche ek insaan ya ek kaam hona chahiye. Jis alarm par koi kuch nahi karta, wo shor hai, aur shor se log asli alarm bhi sunna band kar dete hain.

## Lab: Pehla CPU Alarm

Lab. Ek lab building par CloudWatch mein alarm banao: CPUUtilization 60 se upar, ek minute ke period par, ek reading ke liye. Detailed monitoring on karo taaki jaldi dikhe, kyunki wo paisa leti hai. Building mein SSH karo, sudo apt install -y stress, phir stress --cpu 2 --timeout 300. Kuch minute mein alarm ALARM state mein chala jaayega. Stress band hone par wapas OK. Abhi action nahi laga, wo agle episode mein. Aakhir mein Session 10 ke Auto Scaling ki baat yaad karo: wahi alarm ka ghanta hai jo "ek aur building kholo" kehta hai. Test ke baad detailed monitoring band kar do.

## Recap aur Bridge

Recap: meter, dimension, alarm aur uski teen states. Ab CCTV: graph batata hai kya, log batata hai kyun. Aur alarm ka phone manager tak kaise pahunche.

---

# EPISODE 2: CCTV aur Public-Address

## Graph Kehta Hai "Kya", Log Kehta Hai "Kyun"

Graph batata hai ki errors badh gaye. Log batata hai ki kyun: "database connection timeout". Dono ke bina tasveer adhoori hai. Session 5 mein humne logs ko building ki logbook ki tarah padha tha. Par agar building hi gayab ho jaaye, ya Auto Scaling ne use hata diya, to uski logbook bhi saath gayi. Isliye logbook ki copy landlord ke CCTV room mein bhejna zaroori hai. Isse hi CloudWatch Logs kehte hain. Aur alert ko sahi logon tak pahunchane ke liye public-address system, yaani SNS.

## CloudWatch Logs: Group, Stream, Retention

Log group ek application ya service ka hota hai, jaise /atithi/booking/app. Log stream ek source ka, jaise ek building. Building se logs bhejne ke liye CloudWatch agent lagta hai, aur building ko Session 9 ka duty badge chahiye jisme logs likhne ki ijaazat ho. Ek jaal: log group ki retention by default kabhi expire nahi hoti, aur storage ka paisa chalta rehta hai. Isliye har log group par retention likho, jaise tees din. Lambda ke logs /aws/lambda/FUNCTION-NAME naam ke group mein apne aap aate hain. Aur ek cheez dhyaan mein rakho: log jitne zyada bhejoge, utna bill, isliye debug logs hamesha nahi.

## Logs Insights aur Metric Filter

Logs Insights ek query tool hai. Ek line: fields @timestamp, @message | filter @message like /ERROR/ | stats count() by bin(5m), aur aapko har paanch minute mein errors ki ginti ka graph milta hai. Ye bash ke grep ERROR | wc -l ka cloud wala roop hai, jo hazaaron buildings ke logs par ek saath chalta hai. Aur ek aur tareeka hai: metric filter. Aap kehte ho "jab log mein ERROR shabd aaye, to ek meter ka count ek badhao", aur ab us meter par alarm bana sakte ho. Isse wo cheezein bhi alarm ban jaati hain jo landlord ke apne meters mein nahi hotin, jaise "payment failed" line.

## SNS: Topic aur Subscription

SNS, Simple Notification Service, landlord ka public-address system hai. Topic ek notice board hai, jaise ops-alerts. Publishers us par message daalte hain: alarm, S3, ya koi Lambda. Subscribers us board ko sunte hain: email, SMS, ek HTTPS endpoint, Lambda ya SQS queue. Ek hi message kai subscribers ko ek saath jaata hai, jise fan-out kehte hain. Email subscription ko confirm karna padta hai, ek link click karke, jaise koi aapka email dusron ke naam par na daal de. Production mein alerts chat tool ya on-call system tak jaate hain. Aur topic par kaun message daal sakta hai, ye bhi ek policy hai, Session 12 ki bucket policy jaisi.

## Paisa ka Alarm: Budget aur Billing

Ek alarm aisa bhi chahiye jo paise par nazar rakhe. Session 8 mein humne budget banaya tha, aur wahi sabse aasaan tareeka hai: AWS Budgets, jisme aap mahine ka kharch tay karte ho aur alert tab aata hai jab asli kharch assi percent par pahunche, aur jab forecast poore budget se upar jaaye. Dusra tareeka CloudWatch ka billing metric hai, EstimatedCharges, par ye sirf us-east-1 region mein dikhta hai aur account mein billing alerts ka option on karna padta hai. Dono alert ek SNS topic par bhej sakte ho. Ek pakki aadat: lab ke din bhi, shuru karne se pehle, ye alert on ho.

## Lab: Alarm se Email

Lab. SNS mein topic ops-alerts banao. Ek subscription banao, protocol email, apna address do, aur inbox mein aaya hua link click karke confirm karo. Pichhle alarm ko edit karo, uske action mein ye topic jodo, aur stress --cpu 2 --timeout 300 dobara chalao. Kuch minute mein ALARM ka email aayega, aur stress ke baad OK ka. Phir ek chhota Logs Insights query likho: agar aapne building ke logs bheje hain to ERROR ginti, nahi to /var/log/syslog ek agent se bhej kar dekho. Aakhir mein AWS Budgets mein ek chhota monthly budget aur usi topic par alert lagao. Isse sab alert ek hi jagah aate hain.

## Recap aur Bridge

Recap: CCTV, Insights, SNS aur paise ka alarm. Ab ek naya sawaal: ek chhote kaam ke liye poori building kholein? Nahi. Ek freelancer.

---

# EPISODE 3: Freelancer

## Ek Kaam, Poori Building

Atithi har room ki photo ka ek chhota thumbnail banana chahta hai. Kaam teen second ka hai. Uske liye ek poori building 24 ghante chalana, jabki wo 99 percent khaali baithi rahe? Landlord ka doosra jawab hai ek freelancer: jab ghanti bajti hai tab hi aata hai, ek kaam karta hai, aur chala jaata hai. Aap sirf us waqt ka paisa dete ho jab wo kaam kar raha tha. Is freelancer ko Lambda kehte hain, aur is soch ko serverless kehte hain: server hai, par aapko use sambhalna nahi padta.

## Lambda Kaise Kaam Karta Hai

Lambda function ek handler hai, jo event milne par chalta hai. Aap runtime chunte ho, jaise Python. Memory tay karte ho, aur usi se CPU bhi tay hoti hai, kyunki zyada memory ka matlab zyada CPU. Timeout tay karte ho, jo zyada se zyada paandrah minute hota hai. Function ko ek execution role chahiye, Session 9 ka duty badge, jisme likha ho wo kya kar sakta hai. Pehli baar chalte waqt thodi der lagti hai, jise cold start kehte hain, jab landlord pehle freelancer ka kamra tayyar karta hai. Lambda lambe chalne wale ya bahut bhaari kaam ke liye nahi hai, par chhote event-driven kaam ke liye bahut accha hai.

## Handler, Event aur Environment

Python mein handler aisa dikhta hai: def lambda_handler(event, context):. event mein ghanti ka data hota hai, aur context mein function ki jaankari. Jo aap return karte ho wo caller ko jaata hai. Settings ko code mein nahi, environment variables mein rakho, jaise Session 6 mein humne limit ko parameter banaya tha. print ya logging ka output CloudWatch Logs mein khud pahunchta hai. Har invocation ke aakhir mein ek REPORT line aati hai jisme duration aur memory dikhti hai, jo memory tay karne mein kaam aati hai. Dependencies badi hon to layers ya container image ka upyog hota hai, aur code ki size ki bhi seema hai.

## Role aur Permission: Do Alag Cheezein

Lambda mein do alag ijaazatein hoti hain, aur log aksar mila dete hain. Pehli: function ko kya karne ki ijaazat hai. Wo execution role se aati hai: jaise s3:GetObject aur logs likhna. Doosri: function ko kaun bula sakta hai. Wo function ki apni resource policy se aati hai: S3 ko ghanti bajane ka haq hai ya nahi. Ye wahi identity policy aur resource policy ka farq hai jo Session 9 mein tha. Console mein trigger jodte waqt doosri ijaazat apne aap lag jaati hai, par CLI ya Terraform mein haath se likhni padti hai. Aur ek aur baat: agar function ko VPC ke andar chalana ho, jaise private wing ka database padhne, to use bahar internet ke liye Session 14 ka dispatch desk chahiye.

## Kitni Baar Chalega aur Kitni Der

Lambda do tarah se bulaya jaata hai. Synchronous: caller intezaar karta hai aur jawab leta hai. Asynchronous: caller ghanti baja kar chala jaata hai, jaise S3 ya SNS. Async mein agar function fail ho, to landlord kuch baar khud dobara koshish karta hai, aur phir bhi fail ho to event ko ek dead-letter queue ya destination mein rakh sakta hai, taaki wo khoye na. Isliye function ko aisa likhna chahiye ki ek hi event do baar aaye to bhi nuksaan na ho, yaani idempotent. Ek aur seema: ek saath kitne freelancer aa sakte hain. Isse account ki concurrency kehte hain, aur ek function ko poori limit khane se rokne ke liye reserved concurrency lagti hai. Session 13 ka database connection wala sawaal yahin wapas aata hai: sau freelancer ek saath sau connections kholenge.

## Lab: Pehla Freelancer

Lab. Lambda console mein ek function banao, naam hello-atithi, runtime Python. Code:

Environment variable GREETING set karo, aur test event {"name": "Asha"} se chalao. Result dekho, phir CloudWatch Logs mein jaakar START, END aur REPORT lines. Memory ko 128 se 512 karke dobara chalao, aur duration aur cost ka farq dekho. Function ki execution role mein sirf basic logging ki ijaazat hai, usse zyada abhi kuch nahi chahiye.

## Recap aur Bridge

Recap: Lambda, handler, role aur resource policy. Ab asli maza: freelancer ko ghanti se jodna, jaise photo ke warehouse mein aate hi kaam shuru ho jaana.

---

# EPISODE 4: Ghanti Bajte Hi Kaam

## Photo Aayi, Thumbnail Ban Gaya

Atithi ka staff warehouse mein ek room ki photo daalta hai, aur kuch hi second mein uska thumbnail ban jaata hai, aur kisi ne kuch nahi chalaya. Ye event-driven architecture hai: ek ghatna doosre kaam ko ghanti ki tarah bulaati hai. Koi server baar baar poochta nahi, "kuch aaya?" Kaam tab hota hai jab zaroorat ho. Aur isme ek aur faayda hai: jab raat ko koi photo nahi aati, to Atithi ko ek paisa nahi lagta.

## Ghanti ke Sources

Lambda ko kai tarah ki ghantiyan bula sakti hain. S3 ka event, jaise "naya box aaya". SNS ka message. API Gateway ke zariye ek HTTP request. SQS queue ka message. Aur EventBridge, jo events ko rules se route karta hai. EventBridge ek schedule par chala sakta hai, jaise cron ki tarah "roz raat", ya kisi ghatna par, jaise "koi building band hui". Yaad hai Session 6 ka cron? EventBridge schedule uska cloud wala roop hai, jisme server ki zaroorat nahi. Ek dhyaan: EventBridge ka cron UTC mein chalta hai, India ke samay mein nahi, isliye ghante ka hisaab sahi karo.

## Do Khatarnak Jaal

Do jaal yaad rakho. Pehla: S3 upload par Lambda chalta hai, aur wo apna output usi bucket aur usi prefix mein likhta hai. Naya box aaya, to ghanti phir bajti hai, phir naya box, aur ye chakkar ghoomta rehta hai, aur bill badhta rehta hai. Hal: output alag bucket ya alag prefix mein likho, aur trigger par prefix aur suffix ka filter lagao, jaise sirf uploads/ aur .jpg. Doosra jaal: S3 event mein key URL-encoded aati hai. Space plus ban jaata hai, aur slash %2F. Isliye Python mein urllib.parse.unquote_plus se decode karo, nahi to function ko box milega hi nahi.

## Failure Ke Liye Taiyar

Freelancer fail ho sakta hai: timeout, galat input, ya koi aur service dheema. Isliye teen cheezein pehle se lagao. Ek, dead-letter queue ya failure destination, taaki asafal events khoyein nahi. Do, us queue ya function ke errors par alarm, jo Episode 2 ke ops-alerts topic par jaaye. Teen, timeout ko soch kar rakho, na bahut chhota, na maximum. Aur ek puraani aadat ka yahan bhi faayda: function ko chhota rakho, ek hi kaam karo, aur uske logs mein "event kya tha, kya kiya, kitna time laga" teen cheezein hamesha likho. Kal subah jab koi poochega ki ek photo ka thumbnail kyun nahi bana, to jawab logs mein hona chahiye.

## Lab: Raat ko Dev Buildings Soti Hain

Lab 1. Session 7 ka boto3 wapas. Ek Lambda stop-dev banao:

Role mein sirf ec2:DescribeInstances aur ec2:StopInstances. Pehle haath se test karo, phir EventBridge mein ek schedule banao, jaise cron(0 20 * * ? ). Ye time hamesha UTC mein hota hai: bees baje UTC India mein raat ke ek bajke tees minute hote hain. Pehle yahan cron(30 15 * ? *) likha tha, jo India mein raat ke nau baje banta hai; humne ghadi se jodkar dekha. Dhyaan: sirf Env equals dev wali buildings band hongi, production ki nahi. Ye tag ka hi kaam hai jo Session 8 mein shuru kiya tha.

## Lab: Warehouse ki Ghanti

Lab 2. Ek naya function photo-logger:

Session 12 ke bucket par event notification lagao: prefix uploads/, suffix .jpg, destination yahi function. uploads/room 101.jpg naam ki file upload karo, jisme space hai, aur CloudWatch Logs mein dekho ki naam sahi decode hua hai. Ab dekho ki function ko resource policy ne kaise ijaazat di. Aakhir mein safai: dono schedule aur triggers, functions, alarm, topic aur budget alert. Lab ke baad stop-dev ka schedule zaroor hata do, nahi to wo chalta rahega.

## Recap aur Bridge

Recap: AWS ka poora safar: buildings, storage, networking, database, meters aur freelancers. Ab Atithi ke paas ek poora campus hai. Par ek sawaal baaki hai, jo hotel chalane se bhi bada hai: ye jo humne banaya, uski blueprint kahan hai? Kal agar koi galti se kuch badal de, to purani halat wapas kaun layega? Agla session head office ka hai: Git, jahan har blueprint ka poora register rakha jaata hai.

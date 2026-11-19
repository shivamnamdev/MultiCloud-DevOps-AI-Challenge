# ✍️ 02: SCRIPT — SESSION-15: AWS Monitoring and Serverless
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S15`
- **Focus:** CloudWatch metrics, namespaces, dimensions, alarms (evaluation periods, missing data, actions), CloudWatch Logs and Logs Insights, retention, metric filters, SNS topics and subscriptions, billing alerts (budgets), Lambda (handler, role, memory, timeout, cold start, retries), event sources (S3, EventBridge), loops and idempotency, scheduled automation
- **Builds on:** Session 07 (boto3, `DryRun`), Session 08 (tags, budget), Session 09 (execution role, resource policy), Session 10 (CPU credits, Auto Scaling), Session 12 (S3), Session 13 (connection limits), Session 14 (Lambda in a VPC needs a path out)
- **Story position:** Zoom level 2, the rented campus. Landlord ke meters aur CCTV, ek alarm jo manager ko phone kare, ek public-address system, aur ek freelancer jo ghanti bajne par aata hai, ek kaam karta hai aur chala jaata hai.
- **Story words used:** meters (metrics), CCTV (logs), alarm, public-address system (SNS), freelancer (Lambda), bell (event), duty badge (role), permission letter (policy), warehouse and box (S3), guest (end user), staff (admin)
- **Lab project:** Atithi's booking building gets a CPU alarm that rings the manager's phone, a billing alert, a freelancer that puts dev buildings to sleep at night, and a freelancer that reacts when a new room photo lands in the warehouse.
- **Cost rule (AWS):** alarms, custom metrics, log storage and Lambda invocations each have their own small charge, and free-tier terms change. Check the live pricing pages first. Every lab ends by deleting the alarms, the topic, the functions and the schedule.
- **Episodes:**
  - Episode 1: Meters aur Alarm: Customer se Pehle Pata Chale
  - Episode 2: CCTV aur Public-Address: Logs aur SNS
  - Episode 3: Freelancer: Lambda ka Pehla Kaam
  - Episode 4: Ghanti Bajte Hi Kaam: Events aur Automation

---

# 📺 EPISODE 1: Meters aur Alarm

### [00:00 – 02:05] Scene 1: Guest ne Bataya, Humein Pata Hi Nahi
**[VISUAL: A guest posting "Atithi's booking page is down" on social media. Head office looks at a dashboard that is blank. A caption: "We found out from a guest".]**

**(Voiceover):**
Shaadi ke season ki ek raat. Booking site dheemi hui, phir band ho gayi. Atithi ko pata kaise chala? Ek guest ne social media par likha. Isse sharminda karne wali baat kam hai. Monitoring ka pura maksad yahi hai ki pehle aapko pata chale, guest ko nahi. Pichhle sessions mein humne buildings, godown, records office aur campus banaya. Ab landlord ke paas jo meters aur CCTV pehle se lage hain, unka istemaal seekhte hain. Is poore system ka naam CloudWatch hai.

### [02:05 – 04:45] Scene 2: Metric, Namespace aur Dimension
**[VISUAL: A graph of `CPUUtilization` for one building. Labels on the graph: namespace `AWS/EC2`, metric `CPUUtilization`, dimension `InstanceId=i-0abc`, period 5 minutes, statistic Average.]**

**(Voiceover):**
Metric ek meter ki reading hai jo samay ke saath badalti hai, jaise building ka CPU. Teen shabd yaad rakho. Namespace: ye meter kis service ka hai, jaise `AWS/EC2`. Metric ka naam: `CPUUtilization`. Dimension: ye reading kis cheez ki hai, jaise kaun si building, `InstanceId`. Aur statistic: us period ka average, maximum ya total. EC2 ke basic metrics paanch minute par aate hain, detailed monitoring ek minute par, jo alag paisa leti hai. Ek zaroori jaal: building ka memory aur disk bharna landlord ko dikhta hi nahi, kyunki wo building ke andar ki baat hai. Unke liye CloudWatch agent building par lagana padta hai.

### [04:45 – 07:15] Scene 3: Kya Dekhna Chahiye
**[VISUAL: A list of four golden signals beside the booking site: latency, traffic, errors, saturation. Each linked to a real meter: ALB `TargetResponseTime`, `RequestCount`, `HTTPCode_Target_5XX_Count`, EC2 CPU and RDS connections.]**

**(Voiceover):**
Meter bahut hain, par har meter ka alarm nahi lagana. Chaar cheezein dekho. Latency: guest ko jawab kitni der mein mila. Traffic: kitne guests aa rahe hain. Errors: kitne request fail hue. Saturation: koi cheez bhar to nahi rahi, jaise CPU, disk ya Session 13 ke database ke connections. Atithi ke liye ye marshal ka `TargetResponseTime`, `RequestCount` aur 5xx ginti, building ka CPU, aur database ke connections hain. Session 10 ka ek aur point yaad rakho: T-series building mein CPU credits bhi ek meter hain, aur wo khatam ho jaayein to CPU achanak dheema ho jaata hai.

### [07:15 – 10:50] Scene 4: Alarm: Meter par Nazar
**[VISUAL: An alarm form: metric CPU > 70 for 2 of 3 data points, period 5 minutes. Three states: OK, ALARM, INSUFFICIENT_DATA. A small box "missing data: treat as ...". Actions: notify a topic, an Auto Scaling policy, an EC2 action.]**

**(Voiceover):**
Alarm ek meter par nazar rakhta hai aur ek shart likhta hai: "agar CPU 70 se upar ho, paanch minute ke teen mein se do readings mein, to ALARM." Alarm ki teen states hain: OK, ALARM, aur INSUFFICIENT_DATA, jab abhi kaafi readings nahi mili. Ek chhota setting zaroori hai: missing data ko kaise maanein. Agar building band hai aur reading nahi aa rahi, to alarm ko ALARM dikhana chahiye ya OK, ye aap tay karte ho. Action mein aap topic par notification bhej sakte ho, Auto Scaling ki policy chala sakte ho, ya EC2 ki building ko reboot, recover ya stop karwa sakte ho. Rule: har alarm ke peeche ek insaan ya ek kaam hona chahiye. Jis alarm par koi kuch nahi karta, wo shor hai, aur shor se log asli alarm bhi sunna band kar dete hain.

### [10:50 – 13:30] Scene 5: Lab: Pehla CPU Alarm
**[VISUAL: Create alarm on `CPUUtilization` > 60 for 1 of 1 data points, period 1 minute. SSH into the building: `sudo apt install -y stress`, `stress --cpu 2 --timeout 300`. The alarm turns ALARM in a few minutes.]**

**(Voiceover):**
Lab. Ek lab building par CloudWatch mein alarm banao: `CPUUtilization` 60 se upar, ek minute ke period par, ek reading ke liye. Detailed monitoring on karo taaki jaldi dikhe, kyunki wo paisa leti hai. Building mein SSH karo, `sudo apt install -y stress`, phir `stress --cpu 2 --timeout 300`. Kuch minute mein alarm ALARM state mein chala jaayega. Stress band hone par wapas OK. Abhi action nahi laga, wo agle episode mein. Aakhir mein Session 10 ke Auto Scaling ki baat yaad karo: wahi alarm ka ghanta hai jo "ek aur building kholo" kehta hai. Test ke baad detailed monitoring band kar do.

### [13:30 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "metric = namespace + name + dimension · agent for memory and disk · four things to watch · alarm states · every alarm has an owner".]**

**(Voiceover):**
Recap: meter, dimension, alarm aur uski teen states. Ab CCTV: graph batata hai kya, log batata hai kyun. Aur alarm ka phone manager tak kaise pahunche.

---

# 📺 EPISODE 2: CCTV aur Public-Address

### [00:00 – 02:05] Scene 1: Graph Kehta Hai "Kya", Log Kehta Hai "Kyun"
**[VISUAL: A graph spike "5xx errors up". A magnifier moves to a log line: "DB connection timeout". Caption: "metrics = what, logs = why".]**

**(Voiceover):**
Graph batata hai ki errors badh gaye. Log batata hai ki kyun: "database connection timeout". Dono ke bina tasveer adhoori hai. Session 5 mein humne logs ko building ki logbook ki tarah padha tha. Par agar building hi gayab ho jaaye, ya Auto Scaling ne use hata diya, to uski logbook bhi saath gayi. Isliye logbook ki copy landlord ke CCTV room mein bhejna zaroori hai. Isse hi CloudWatch Logs kehte hain. Aur alert ko sahi logon tak pahunchane ke liye public-address system, yaani SNS.

### [02:05 – 04:35] Scene 2: CloudWatch Logs: Group, Stream, Retention
**[VISUAL: A log group `/atithi/booking/app` with a log stream per building. A retention dropdown "Never expire" highlighted red, and "30 days" selected. A building running the CloudWatch agent with a duty badge allowing `logs:PutLogEvents`.]**

**(Voiceover):**
Log group ek application ya service ka hota hai, jaise `/atithi/booking/app`. Log stream ek source ka, jaise ek building. Building se logs bhejne ke liye CloudWatch agent lagta hai, aur building ko Session 9 ka duty badge chahiye jisme logs likhne ki ijaazat ho. Ek jaal: log group ki retention by default kabhi expire nahi hoti, aur storage ka paisa chalta rehta hai. Isliye har log group par retention likho, jaise tees din. Lambda ke logs `/aws/lambda/FUNCTION-NAME` naam ke group mein apne aap aate hain. Aur ek cheez dhyaan mein rakho: log jitne zyada bhejoge, utna bill, isliye debug logs hamesha nahi.

### [04:35 – 07:15] Scene 3: Logs Insights aur Metric Filter
**[VISUAL: A Logs Insights query: `fields @timestamp, @message | filter @message like /ERROR/ | stats count() by bin(5m)`. A line chart of errors per five minutes. Beside it, a metric filter turning the word `ERROR` into a metric `ErrorCount`, and an alarm on it.]**

**(Voiceover):**
Logs Insights ek query tool hai. Ek line: `fields @timestamp, @message | filter @message like /ERROR/ | stats count() by bin(5m)`, aur aapko har paanch minute mein errors ki ginti ka graph milta hai. Ye bash ke `grep ERROR | wc -l` ka cloud wala roop hai, jo hazaaron buildings ke logs par ek saath chalta hai. Aur ek aur tareeka hai: metric filter. Aap kehte ho "jab log mein ERROR shabd aaye, to ek meter ka count ek badhao", aur ab us meter par alarm bana sakte ho. Isse wo cheezein bhi alarm ban jaati hain jo landlord ke apne meters mein nahi hotin, jaise "payment failed" line.

### [07:15 – 09:55] Scene 4: SNS: Topic aur Subscription
**[VISUAL: A topic `ops-alerts` as a notice board. Publishers on the left (CloudWatch alarm, S3, Lambda). Subscribers on the right (email, SMS, HTTPS endpoint, Lambda, SQS). A "Confirm subscription" email with a link.]**

**(Voiceover):**
SNS, Simple Notification Service, landlord ka public-address system hai. Topic ek notice board hai, jaise `ops-alerts`. Publishers us par message daalte hain: alarm, S3, ya koi Lambda. Subscribers us board ko sunte hain: email, SMS, ek HTTPS endpoint, Lambda ya SQS queue. Ek hi message kai subscribers ko ek saath jaata hai, jise fan-out kehte hain. Email subscription ko confirm karna padta hai, ek link click karke, jaise koi aapka email dusron ke naam par na daal de. Production mein alerts chat tool ya on-call system tak jaate hain. Aur topic par kaun message daal sakta hai, ye bhi ek policy hai, Session 12 ki bucket policy jaisi.

### [09:55 – 12:25] Scene 5: Paisa ka Alarm: Budget aur Billing
**[VISUAL: Two cards. Card 1: AWS Budgets, monthly budget with alerts at 80% actual and 100% forecast. Card 2: a CloudWatch billing metric `EstimatedCharges` in the us-east-1 region only. Both connect to an SNS topic.]**

**(Voiceover):**
Ek alarm aisa bhi chahiye jo paise par nazar rakhe. Session 8 mein humne budget banaya tha, aur wahi sabse aasaan tareeka hai: AWS Budgets, jisme aap mahine ka kharch tay karte ho aur alert tab aata hai jab asli kharch assi percent par pahunche, aur jab forecast poore budget se upar jaaye. Dusra tareeka CloudWatch ka billing metric hai, `EstimatedCharges`, par ye sirf us-east-1 region mein dikhta hai aur account mein billing alerts ka option on karna padta hai. Dono alert ek SNS topic par bhej sakte ho. Ek pakki aadat: lab ke din bhi, shuru karne se pehle, ye alert on ho.

### [12:25 – 15:00] Scene 6: Lab: Alarm se Email
**[VISUAL: Console: SNS → Create topic `ops-alerts` → Create subscription: email → confirm in inbox. Edit the CPU alarm to notify the topic. Run `stress` again; an email arrives with the alarm name and reason.]**

**(Voiceover):**
Lab. SNS mein topic `ops-alerts` banao. Ek subscription banao, protocol email, apna address do, aur inbox mein aaya hua link click karke confirm karo. Pichhle alarm ko edit karo, uske action mein ye topic jodo, aur `stress --cpu 2 --timeout 300` dobara chalao. Kuch minute mein ALARM ka email aayega, aur stress ke baad OK ka. Phir ek chhota Logs Insights query likho: agar aapne building ke logs bheje hain to `ERROR` ginti, nahi to `/var/log/syslog` ek agent se bhej kar dekho. Aakhir mein AWS Budgets mein ek chhota monthly budget aur usi topic par alert lagao. Isse sab alert ek hi jagah aate hain.

### [15:00 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "log group retention · Logs Insights · metric filter · SNS topic, subscribers, confirm · budget alert before the lab".]**

**(Voiceover):**
Recap: CCTV, Insights, SNS aur paise ka alarm. Ab ek naya sawaal: ek chhote kaam ke liye poori building kholein? Nahi. Ek freelancer.

---

# 📺 EPISODE 3: Freelancer

### [00:00 – 02:05] Scene 1: Ek Kaam, Poori Building
**[VISUAL: A building running 24 hours so it can shrink one room photo each hour; a meter shows 99% idle. A freelancer arrives at the door when a bell rings, does the task, and leaves.]**

**(Voiceover):**
Atithi har room ki photo ka ek chhota thumbnail banana chahta hai. Kaam teen second ka hai. Uske liye ek poori building 24 ghante chalana, jabki wo 99 percent khaali baithi rahe? Landlord ka doosra jawab hai ek freelancer: jab ghanti bajti hai tab hi aata hai, ek kaam karta hai, aur chala jaata hai. Aap sirf us waqt ka paisa dete ho jab wo kaam kar raha tha. Is freelancer ko Lambda kehte hain, aur is soch ko serverless kehte hain: server hai, par aapko use sambhalna nahi padta.

### [02:05 – 04:35] Scene 2: Lambda Kaise Kaam Karta Hai
**[VISUAL: An event enters a function box. Inside the box: handler, runtime (Python), memory, timeout, execution role. A "cold start" delay is drawn on the first call and a "warm" call is instant.]**

**(Voiceover):**
Lambda function ek handler hai, jo event milne par chalta hai. Aap runtime chunte ho, jaise Python. Memory tay karte ho, aur usi se CPU bhi tay hoti hai, kyunki zyada memory ka matlab zyada CPU. Timeout tay karte ho, jo zyada se zyada paandrah minute hota hai. Function ko ek execution role chahiye, Session 9 ka duty badge, jisme likha ho wo kya kar sakta hai. Pehli baar chalte waqt thodi der lagti hai, jise cold start kehte hain, jab landlord pehle freelancer ka kamra tayyar karta hai. Lambda lambe chalne wale ya bahut bhaari kaam ke liye nahi hai, par chhote event-driven kaam ke liye bahut accha hai.

### [04:35 – 07:00] Scene 3: Handler, Event aur Environment
**[VISUAL: A Python file in the console editor with `def lambda_handler(event, context):`. A test event JSON. An Environment variables panel with `GREETING`. A CloudWatch Logs link showing `START`, `END`, `REPORT` lines with duration and memory used.]**

**(Voiceover):**
Python mein handler aisa dikhta hai: `def lambda_handler(event, context):`. `event` mein ghanti ka data hota hai, aur `context` mein function ki jaankari. Jo aap return karte ho wo caller ko jaata hai. Settings ko code mein nahi, environment variables mein rakho, jaise Session 6 mein humne limit ko parameter banaya tha. `print` ya `logging` ka output CloudWatch Logs mein khud pahunchta hai. Har invocation ke aakhir mein ek REPORT line aati hai jisme duration aur memory dikhti hai, jo memory tay karne mein kaam aati hai. Dependencies badi hon to layers ya container image ka upyog hota hai, aur code ki size ki bhi seema hai.

### [07:00 – 09:50] Scene 4: Role aur Permission: Do Alag Cheezein
**[VISUAL: Two arrows around a function. Arrow A, "execution role": function → S3, DynamoDB, logs. Arrow B, "resource policy": S3 or SNS → function. A red cross where the second one is missing, with the message "AccessDenied: cannot invoke".]**

**(Voiceover):**
Lambda mein do alag ijaazatein hoti hain, aur log aksar mila dete hain. Pehli: function ko kya karne ki ijaazat hai. Wo execution role se aati hai: jaise `s3:GetObject` aur logs likhna. Doosri: function ko kaun bula sakta hai. Wo function ki apni resource policy se aati hai: S3 ko ghanti bajane ka haq hai ya nahi. Ye wahi identity policy aur resource policy ka farq hai jo Session 9 mein tha. Console mein trigger jodte waqt doosri ijaazat apne aap lag jaati hai, par CLI ya Terraform mein haath se likhni padti hai. Aur ek aur baat: agar function ko VPC ke andar chalana ho, jaise private wing ka database padhne, to use bahar internet ke liye Session 14 ka dispatch desk chahiye.

### [09:50 – 12:50] Scene 5: Kitni Baar Chalega aur Kitni Der
**[VISUAL: A pie of invoke types: synchronous (caller waits) and asynchronous (caller leaves). An async event failing, a retry arrow twice, then a dead-letter box. A concurrency bar with a "reserved" limit.]**

**(Voiceover):**
Lambda do tarah se bulaya jaata hai. Synchronous: caller intezaar karta hai aur jawab leta hai. Asynchronous: caller ghanti baja kar chala jaata hai, jaise S3 ya SNS. Async mein agar function fail ho, to landlord kuch baar khud dobara koshish karta hai, aur phir bhi fail ho to event ko ek dead-letter queue ya destination mein rakh sakta hai, taaki wo khoye na. Isliye function ko aisa likhna chahiye ki ek hi event do baar aaye to bhi nuksaan na ho, yaani idempotent. Ek aur seema: ek saath kitne freelancer aa sakte hain. Isse account ki concurrency kehte hain, aur ek function ko poori limit khane se rokne ke liye reserved concurrency lagti hai. Session 13 ka database connection wala sawaal yahin wapas aata hai: sau freelancer ek saath sau connections kholenge.

### [12:50 – 15:00] Scene 6: Lab: Pehla Freelancer
**[VISUAL: Console: Create function `hello-atithi`, Python runtime, new role with basic logging. Paste the code, set `GREETING`, Test with `{"name": "Asha"}`, see the result and the REPORT line.]**

**(Voiceover):**
Lab. Lambda console mein ek function banao, naam `hello-atithi`, runtime Python. Code:
```python
import os, json
def lambda_handler(event, context):
    name = event.get("name", "guest")
    greeting = os.environ.get("GREETING", "Namaste")
    print(f"invoked for {name}")
    return {"statusCode": 200, "body": json.dumps({"message": f"{greeting}, {name}!"})}
```
Environment variable `GREETING` set karo, aur test event `{"name": "Asha"}` se chalao. Result dekho, phir CloudWatch Logs mein jaakar `START`, `END` aur `REPORT` lines. Memory ko 128 se 512 karke dobara chalao, aur duration aur cost ka farq dekho. Function ki execution role mein sirf basic logging ki ijaazat hai, usse zyada abhi kuch nahi chahiye.

### [15:00 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "event → handler · role (what it may do) vs resource policy (who may call) · memory sets CPU · timeout ≤ 15 min · async retries, idempotent".]**

**(Voiceover):**
Recap: Lambda, handler, role aur resource policy. Ab asli maza: freelancer ko ghanti se jodna, jaise photo ke warehouse mein aate hi kaam shuru ho jaana.

---

# 📺 EPISODE 4: Ghanti Bajte Hi Kaam

### [00:00 – 01:40] Scene 1: Photo Aayi, Thumbnail Ban Gaya
**[VISUAL: A room photo is dropped into the warehouse. A bell rings; a freelancer produces a small thumbnail in another prefix, and the public-address says "processed". No building is shown.]**

**(Voiceover):**
Atithi ka staff warehouse mein ek room ki photo daalta hai, aur kuch hi second mein uska thumbnail ban jaata hai, aur kisi ne kuch nahi chalaya. Ye event-driven architecture hai: ek ghatna doosre kaam ko ghanti ki tarah bulaati hai. Koi server baar baar poochta nahi, "kuch aaya?" Kaam tab hota hai jab zaroorat ho. Aur isme ek aur faayda hai: jab raat ko koi photo nahi aati, to Atithi ko ek paisa nahi lagta.

### [01:40 – 03:55] Scene 2: Ghanti ke Sources
**[VISUAL: A hub with arrows into a function: S3 event, SNS message, API Gateway request, SQS queue, EventBridge rule. EventBridge is drawn with two kinds of rules: "schedule" and "when something happens in the account".]**

**(Voiceover):**
Lambda ko kai tarah ki ghantiyan bula sakti hain. S3 ka event, jaise "naya box aaya". SNS ka message. API Gateway ke zariye ek HTTP request. SQS queue ka message. Aur EventBridge, jo events ko rules se route karta hai. EventBridge ek schedule par chala sakta hai, jaise cron ki tarah "roz raat", ya kisi ghatna par, jaise "koi building band hui". Yaad hai Session 6 ka cron? EventBridge schedule uska cloud wala roop hai, jisme server ki zaroorat nahi. Ek dhyaan: EventBridge ka cron UTC mein chalta hai, India ke samay mein nahi, isliye ghante ka hisaab sahi karo.

### [03:55 – 06:10] Scene 3: Do Khatarnak Jaal
**[VISUAL: Left: an upload to the warehouse triggers a function that writes its output into the same prefix, which triggers it again, drawn as a spiral with a rising bill. Right: an S3 event key `rooms%2F101%2Ffront+photo.jpg` and the decoded `rooms/101/front photo.jpg`.]**

**(Voiceover):**
Do jaal yaad rakho. Pehla: S3 upload par Lambda chalta hai, aur wo apna output usi bucket aur usi prefix mein likhta hai. Naya box aaya, to ghanti phir bajti hai, phir naya box, aur ye chakkar ghoomta rehta hai, aur bill badhta rehta hai. Hal: output alag bucket ya alag prefix mein likho, aur trigger par prefix aur suffix ka filter lagao, jaise sirf `uploads/` aur `.jpg`. Doosra jaal: S3 event mein key URL-encoded aati hai. Space plus ban jaata hai, aur slash `%2F`. Isliye Python mein `urllib.parse.unquote_plus` se decode karo, nahi to function ko box milega hi nahi.

### [06:10 – 08:35] Scene 4: Failure Ke Liye Taiyar
**[VISUAL: An async failure path: function error → two retries → dead-letter queue → an alarm on queue length → a message to `ops-alerts`. A second panel: a function log filtered for `Task timed out`.]**

**(Voiceover):**
Freelancer fail ho sakta hai: timeout, galat input, ya koi aur service dheema. Isliye teen cheezein pehle se lagao. Ek, dead-letter queue ya failure destination, taaki asafal events khoyein nahi. Do, us queue ya function ke errors par alarm, jo Episode 2 ke `ops-alerts` topic par jaaye. Teen, timeout ko soch kar rakho, na bahut chhota, na maximum. Aur ek puraani aadat ka yahan bhi faayda: function ko chhota rakho, ek hi kaam karo, aur uske logs mein "event kya tha, kya kiya, kitna time laga" teen cheezein hamesha likho. Kal subah jab koi poochega ki ek photo ka thumbnail kyun nahi bana, to jawab logs mein hona chahiye.

### [08:35 – 11:45] Scene 5: Lab: Raat ko Dev Buildings Soti Hain
**[VISUAL: A Lambda `stop-dev` with a role that allows only `ec2:DescribeInstances` and `ec2:StopInstances`. Code using `boto3`, filter `tag:Env=dev`, `instance-state-name=running`. An EventBridge schedule `cron(0 20 * * ? *)` with a note "UTC, 01:30 in India".]**

**(Voiceover):**
Lab 1. Session 7 ka boto3 wapas. Ek Lambda `stop-dev` banao:
```python
import boto3
ec2 = boto3.client("ec2")
def lambda_handler(event, context):
    r = ec2.describe_instances(Filters=[
        {"Name": "tag:Env", "Values": ["dev"]},
        {"Name": "instance-state-name", "Values": ["running"]}])
    ids = [i["InstanceId"] for x in r["Reservations"] for i in x["Instances"]]
    if ids:
        ec2.stop_instances(InstanceIds=ids)
    print(f"stopped: {ids}")
    return {"stopped": ids}
```
Role mein sirf `ec2:DescribeInstances` aur `ec2:StopInstances`. Pehle haath se test karo, phir EventBridge mein ek schedule banao, jaise `cron(0 20 * * ? *)`. Ye time hamesha UTC mein hota hai: bees baje UTC India mein raat ke ek bajke tees minute hote hain. Pehle yahan `cron(30 15 * * ? *)` likha tha, jo India mein raat ke nau baje banta hai; humne ghadi se jodkar dekha. Dhyaan: sirf Env equals dev wali buildings band hongi, production ki nahi. Ye tag ka hi kaam hai jo Session 8 mein shuru kiya tha.

### [11:45 – 14:00] Scene 6: Lab: Warehouse ki Ghanti
**[VISUAL: S3 → Properties → Event notifications → prefix `uploads/`, suffix `.jpg`, destination the function `photo-logger`. The function code prints the decoded key. Upload `uploads/room 101.jpg`; CloudWatch Logs shows `room 101.jpg`.]**

**(Voiceover):**
Lab 2. Ek naya function `photo-logger`:
```python
import urllib.parse
def lambda_handler(event, context):
    for rec in event["Records"]:
        bucket = rec["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(rec["s3"]["object"]["key"])
        print(f"new photo: s3://{bucket}/{key}")
```
Session 12 ke bucket par event notification lagao: prefix `uploads/`, suffix `.jpg`, destination yahi function. `uploads/room 101.jpg` naam ki file upload karo, jisme space hai, aur CloudWatch Logs mein dekho ki naam sahi decode hua hai. Ab dekho ki function ko resource policy ne kaise ijaazat di. Aakhir mein safai: dono schedule aur triggers, functions, alarm, topic aur budget alert. Lab ke baad `stop-dev` ka schedule zaroor hata do, nahi to wo chalta rahega.

### [14:00 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "sources: S3, SNS, API, SQS, EventBridge · UTC cron · no output into the trigger prefix · decode the key · DLQ + alarm · clean up schedules". Then a blueprint roll appears over the campus map.]**

**(Voiceover):**
Recap: AWS ka poora safar: buildings, storage, networking, database, meters aur freelancers. Ab Atithi ke paas ek poora campus hai. Par ek sawaal baaki hai, jo hotel chalane se bhi bada hai: ye jo humne banaya, uski blueprint kahan hai? Kal agar koi galti se kuch badal de, to purani halat wapas kaun layega? Agla session head office ka hai: Git, jahan har blueprint ka poora register rakha jaata hai.

---

# 📎 Student handout: Session 15 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Metric | Namespace + naam + dimension; EC2 basic 5 min, detailed 1 min |
| Memory aur disk | Building ke andar ke meters: CloudWatch agent chahiye |
| Dekhne wali chaar cheezein | Latency, traffic, errors, saturation |
| Alarm | Shart + period + kitni readings; states OK, ALARM, INSUFFICIENT_DATA; missing data setting |
| Alarm action | SNS, Auto Scaling, EC2 reboot / recover / stop |
| Logs | Group, stream; retention hamesha set karo; Lambda logs `/aws/lambda/NAME` |
| Logs Insights | `filter` + `stats count() by bin(5m)`; metric filter se log ka alarm |
| SNS | Topic, subscribers (email, SMS, HTTPS, Lambda, SQS); email confirm; fan-out |
| Paisa | AWS Budgets pehle; `EstimatedCharges` sirf us-east-1 |
| Lambda | Handler, runtime, memory (CPU bhi), timeout ≤ 15 min, cold start |
| Do ijaazatein | Execution role (kya kar sakta hai) vs resource policy (kaun bula sakta hai) |
| Async | Retry, dead-letter queue, idempotent function; concurrency limit |
| Event sources | S3, SNS, API Gateway, SQS, EventBridge (cron UTC) |
| Do jaal | Output usi prefix mein nahi; S3 key `unquote_plus` se decode |
| Safai | Schedules, triggers, functions, alarms, topic, budget |

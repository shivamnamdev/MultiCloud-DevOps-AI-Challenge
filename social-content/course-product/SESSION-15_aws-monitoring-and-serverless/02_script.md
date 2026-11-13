# ✍️ 02: SCRIPT — SESSION-15: AWS Monitoring & Serverless
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S15`
- **Focus:** CloudWatch metrics/alarms/logs, SNS notifications, billing alerts, Lambda, event-driven design with S3/EventBridge
- **Episodes:**
  - Episode 1: Monitoring kyun: CloudWatch Metrics aur Alarms
  - Episode 2: Logs aur SNS: Alert Kisko Jaye
  - Episode 3: Lambda: Serverless ki Pehli Kadam
  - Episode 4: Event-Driven Automation: S3 aur EventBridge

---

# 📺 EPISODE 1: CloudWatch Metrics aur Alarms

### [00:00 – 01:15] Scene 1: Customer ne Bataya, Hum ko Pata Hi Nahi
**[VISUAL: A customer tweeting "Your site is down". The team looks at a dashboard that is empty. Text: "We found out from Twitter".]**

**(Voiceover):**
Sabse sharminda karne wali baat: aapka customer aapko batata hai ki aapki site band hai. Monitoring ka maksad yahi hai ki pehle aapko pata chale, customer ko nahi. AWS mein iska kendra CloudWatch hai.

### [01:15 – 05:00] Scene 2: Metrics, Namespace, Dimension
**[VISUAL: A CloudWatch graph for EC2 CPUUtilization. Labels: Namespace `AWS/EC2`, Metric `CPUUtilization`, Dimension `InstanceId`, Period 5 min, Statistic Average.]**

**(Voiceover):**
Metric ek number hai jo time ke saath badalta hai, jaise CPU utilization. Namespace us service ka naam jisse metric aaya, jaise `AWS/EC2`. Dimension batata hai kis cheez ka, jaise InstanceId. Aur statistic, jaise average ya maximum. EC2 ke basic metrics paanch minute par aate hain, detailed monitoring ek minute par. Dhyaan: memory aur disk usage EC2 ke default metrics mein nahi hote, unhe CloudWatch agent se bhejna padta hai.

### [05:00 – 08:30] Scene 3: Alarms
**[VISUAL: An alarm configuration: metric CPU > 70% for 2 of 3 datapoints at 5 min; states OK / ALARM / INSUFFICIENT_DATA; actions: SNS notification, EC2 action, Auto Scaling.]**

**(Voiceover):**
Alarm ek metric par nazar rakhta hai. "Agar CPU teen mein se do datapoints ke liye 70% se upar ho, to alarm." Alarm ki teen states: OK, ALARM, aur INSUFFICIENT_DATA. Alarm ke action mein aap SNS se notification bhej sakte ho, Auto Scaling policy chala sakte ho, ya EC2 instance ko reboot ya recover karwa sakte ho. Alert ka rule: har alert par koi action hona chahiye. Jo alert se koi kuch nahi karta, wo noise hai, aur noise se log asli alert ko bhi ignore karna seekh jaate hain.

### [08:30 – 11:30] Scene 4: Lab: CPU Alarm
**[VISUAL: Create an alarm on an instance's CPUUtilization > 60% for 1 datapoint of 1 minute. Run `stress --cpu 2 --timeout 300`. The alarm state turns to ALARM.]**

**(Voiceover):**
Lab: ek instance par CloudWatch mein alarm banao, CPUUtilization 60% se upar. Detailed monitoring on rakho taaki jaldi dikhe. Instance mein `stress --cpu 2 --timeout 300` chalao. Kuch minute mein alarm ALARM state mein chala jayega. Abhi action nahi lagaya, agle episode mein SNS se email bhejenge. Test ke baad detailed monitoring band karo agar zaroorat na ho, kyunki uska alag charge lagta hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "metric · namespace · dimension · alarm states · actionable alerts".]**

**(Voiceover):**
Recap: metrics aur alarms. Ab log kahan dekhein, aur alert ko inbox tak kaise pahunchayein.

---

# 📺 EPISODE 2: Logs aur SNS

### [00:00 – 01:15] Scene 1: Metric Bolta Hai "Kya", Log Bolta Hai "Kyun"
**[VISUAL: A graph spike labelled "5xx errors up". A magnifier moves to a log line: "DB connection timeout". Text: "Metrics = what. Logs = why."]**

**(Voiceover):**
Graph aapko batata hai ki errors badh gaye. Log aapko batata hai ki kyun badhe: "database connection timeout". Dono ke bina picture adhoori hai. Isliye CloudWatch Logs mein application aur system logs bhejna zaroori hai, aur SNS se alert ko sahi logon tak pahunchana.

### [01:15 – 05:00] Scene 2: CloudWatch Logs aur Logs Insights
**[VISUAL: A log group `/app/web` with log streams per instance. A Logs Insights query: `fields @timestamp, @message | filter @message like /ERROR/ | stats count() by bin(5m)`.]**

**(Voiceover):**
CloudWatch Logs mein log group ek application ya service ka hota hai, aur log stream ek source ka, jaise ek instance. EC2 se logs bhejne ke liye CloudWatch agent lagana padta hai. Retention set karo, kyunki default mein logs kabhi expire nahi hote, aur paisa lagta rehta hai. Logs Insights ek query tool hai: `filter @message like /ERROR/ | stats count() by bin(5m)` aapko har paanch minute mein kitne errors aaye wo dikha deta hai. Metric filter se log mein se bhi metric aur alarm bana sakte ho.

### [05:00 – 08:30] Scene 3: SNS: Topic aur Subscription
**[VISUAL: A topic "ops-alerts". Publishers on the left (CloudWatch alarm, S3, Lambda). Subscribers on the right (email, SMS, HTTPS, Lambda, SQS). A "confirm subscription" email.]**

**(Voiceover):**
SNS, Simple Notification Service, publish-subscribe system hai. Topic ek notice board hai. Publishers us par message daalte hain, jaise CloudWatch alarm. Subscribers us board ko sunte hain: email, SMS, HTTPS endpoint, Lambda ya SQS. Email subscription confirm karni padti hai, ek link par click karke. Production mein alerts ko chat tool ya on-call system tak le jaate hain. Aur topic ki access policy ko surakshit rakhna zaroori hai.

### [08:30 – 11:30] Scene 4: Lab: Alarm se Email
**[VISUAL: Create SNS topic `ops-alerts`, subscribe an email, confirm. Edit the CPU alarm to notify the topic. Run `stress` again; an email arrives with the alarm details.]**

**(Voiceover):**
Lab: SNS topic `ops-alerts` banao, apna email subscribe karo aur confirm karo. Pichle alarm ke action mein ye topic jodo. Phir `stress` chalao. Kuch minute mein aapke inbox mein ALARM ka email aayega. Ab ek Logs Insights query likho jo pichle ghante ke errors dikhaye, ya agar logs nahi hain to `/var/log/syslog` ko agent se bhejna seekho. Aakhir mein ek billing alarm bhi lagao taaki kharch ka bhi alert mile.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "logs retention · Logs Insights · SNS topic → email/Lambda · billing alert".]**

**(Voiceover):**
Recap: logs, alerts, SNS. Ab ek naya sawaal: kya hum chhote kaam ke liye poora server chalayein? Nahi, Lambda.

---

# 📺 EPISODE 3: Lambda

### [00:00 – 01:15] Scene 1: Ek Chhota Kaam, Poora Server
**[VISUAL: A server running 24 hours to resize one image per hour. A meter shows idle 99%. Replaced by a single lightning bolt triggered on demand.]**

**(Voiceover):**
Ek chhota kaam, jaise har ghante ek image ka size badalna. Uske liye poora EC2 server 24 ghante chalana, jabki wo 99% idle rehta hai. Serverless is par alag soch deta hai: aap sirf code do, AWS jab zaroorat ho tab hi usse chalata hai, aur aap sirf chalne ke samay ka paisa dete ho. Lambda AWS ka function-as-a-service hai.

### [01:15 – 05:00] Scene 2: Lambda kaise Kaam Karta Hai
**[VISUAL: Event → Lambda function (code, memory, timeout, execution role) → result. A cold start shown as a brief "warm-up" delay on first invocation.]**

**(Voiceover):**
Lambda function ek handler hota hai jo ek event milne par chalta hai. Aap runtime chunte ho, jaise Python, memory set karte ho, aur timeout, jo maximum 15 minute tak hota hai. Function ko ek execution role chahiye, jo tay karta hai wo kya kar sakta hai. Pehli baar chalte waqt thodi der lagti hai, jise cold start kehte hain. Lambda lambe chalne wale kaam ya bahut heavy compute ke liye nahi hai, par chhote, event-driven kaam ke liye bahut accha hai.

### [05:00 – 08:30] Scene 3: Handler aur Environment Variables
**[VISUAL: A Python handler `def lambda_handler(event, context): ...` in the console editor. A test event JSON. Environment variables panel with `GREETING`. CloudWatch Logs link for output.]**

**(Voiceover):**
Python mein handler aisa dikhta hai: `def lambda_handler(event, context):`. `event` mein trigger ka data hota hai, aur `context` mein runtime ki jaankari. Return value caller ko jaati hai. Settings ko code mein nahi, environment variables mein rakho. `print` ya `logging` ka output CloudWatch Logs mein khud pahunch jaata hai, aur har invocation ka record milta hai. Dependencies badi hon to layers ya container image ka use hota hai.

### [08:30 – 11:30] Scene 4: Lab: Pehla Lambda
**[VISUAL: Console: Create function (Python), paste the code, Test with a sample event, view the result and logs.]**

**(Voiceover):**
Lab: Lambda console mein ek Python function banao, naam `hello-devops`:
```python
import os, json
def lambda_handler(event, context):
    name = event.get("name", "world")
    greeting = os.environ.get("GREETING", "Hello")
    print(f"invoked for {name}")
    return {"statusCode": 200, "body": json.dumps({"message": f"{greeting}, {name}!"})}
```
Environment variable `GREETING` set karo, ek test event `{"name":"Asha"}` ke saath chalao, aur result aur logs dekho. Execution role mein default basic logging permission hoti hai, usse zyada kuch nahi chahiye.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "event → handler · role · timeout ≤ 15 min · env vars · logs auto".]**

**(Voiceover):**
Recap: Lambda, handler, role. Ab asli maza: Lambda ko events se jodna, jaise file upload hote hi code chalna.

---

# 📺 EPISODE 4: Event-Driven Automation

### [00:00 – 01:15] Scene 1: File Aayi, Kaam Apne Aap Hua
**[VISUAL: A user uploads `photo.jpg` to S3. A lightning bolt triggers a function; a thumbnail appears in another folder; an SNS message "Processed".]**

**(Voiceover):**
Ek user ne S3 mein image upload ki, aur kuch hi second mein uska thumbnail ban gaya, aur kisi ne kuch nahi kiya. Ye event-driven architecture hai: ek ghatna doosri ghatna ko trigger karti hai. Server polling nahi karta, kaam tab hota hai jab zaroorat ho.

### [01:15 – 05:00] Scene 2: Event Sources: S3, SNS, EventBridge
**[VISUAL: A hub showing triggers: S3 event, SNS message, EventBridge rule (schedule/event pattern), API Gateway, SQS. Each arrow into Lambda.]**

**(Voiceover):**
Lambda ko kai sources trigger kar sakte hain. S3 event jaise object created. SNS message. API Gateway ek HTTP request. SQS queue ka message. Aur EventBridge, jo events ko rules se route karta hai, ya schedule par chalata hai, jaise cron ki tarah "har raat 2 baje" ya "jab koi EC2 instance state badle". EventBridge cron ka cloud wala roop hai, bina server ke.

### [05:00 – 08:30] Scene 3: Design Cautions
**[VISUAL: A trap diagram: S3 upload → Lambda writes back to the same bucket → triggers itself in an infinite loop; a red stop sign. A fix: use different prefix/bucket and add idempotency.]**

**(Voiceover):**
Ek khatarnaak galti: S3 ke upload par Lambda trigger hota hai, aur Lambda output usi bucket ya prefix mein likhta hai, jisse wo phir trigger hota hai. Infinite loop, aur bill. Isliye output alag bucket ya prefix mein likho, aur trigger par filter lagao. Aur idempotency: ek event do baar aa sakta hai, isliye function ko aise likho ki do baar chalne par bhi nuksaan na ho. Aur failures ke liye dead-letter queue lagao.

### [08:30 – 11:30] Scene 4: Lab: Daily Cleanup aur S3 Trigger
**[VISUAL: EventBridge schedule rule `rate(1 day)` invoking a Lambda that stops tagged dev instances. Then an S3 trigger with prefix `uploads/` and a Lambda that logs file names.]**

**(Voiceover):**
Lab 1: ek Lambda likho jo `Env=dev` tag wale running instances ko `boto3` se stop kare. Uski execution role mein sirf `ec2:DescribeInstances` aur `ec2:StopInstances` do. EventBridge mein ek schedule rule se use roz raat chalao. Lab 2: S3 bucket par `uploads/` prefix ka trigger lagao, aur Lambda mein event se file ka naam print karo. File upload karke CloudWatch Logs dekho. Ye automation ki asli shuruaat hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "event sources · EventBridge schedule · avoid loops · idempotent · least-privilege role".]**

**(Voiceover):**
Recap: AWS ka pura safar: servers, storage, networking, database, monitoring aur serverless. Ab hum code ki taraf chalte hain. Aap ne jo kuch banaya, usse safely team ke saath share aur track kaise karenge? Git aur GitHub.

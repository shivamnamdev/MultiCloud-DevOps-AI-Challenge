# ✍️ 02: SCRIPT — SESSION-07: Python for DevOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Assumes basics from the "Think in Python" course.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S07`
- **Focus:** Why Python after Bash, venv & dependencies, files/JSON/YAML, HTTP & APIs, boto3 for AWS, SSH automation, error handling
- **Episodes:**
  - Episode 1: Bash se Python tak: kab kaun sa tool, venv aur pip
  - Episode 2: Data Handling: JSON, YAML, files aur requests
  - Episode 3: boto3: Python se AWS ko control karo
  - Episode 4: Robust Automation: errors, logging aur ek Report Script

---

# 📺 EPISODE 1: Bash se Python tak

### [00:00 – 01:15] Scene 1: 200 Line ki Bash Script ka Dard
**[VISUAL: A 200-line Bash file with nested quotes, `awk`, `sed`, and a JSON parse via `grep`. A red "unmaintainable" stamp. Next to it, 20 clean lines of Python.]**

**(Voiceover):**
Bash chhote kaam ke liye zabardast hai. Par jab script mein JSON padhna ho, API call karni ho, ya complex logic ho, to wo thakane lagti hai. Quotes ka jaal, `awk` aur `sed` ki chainein, aur ek jagah typo to poori script behak jaati hai. Python is jagah kam lines mein, saaf tareeke se, kaam kar deti hai. Ye session aapko Python ko ek DevOps औज़ार ki tarah dikhata hai.

### [01:15 – 05:00] Scene 2: Bash vs Python: Kab Kya?
**[VISUAL: A decision tree: "Few commands glued together?" → Bash. "Need JSON/APIs/data/tests?" → Python. "Runs on every Linux box with no install?" → Bash.]**

**(Voiceover):**
Thumb rule: agar kaam kuch commands ko jodne ka hai, jaise ek log search ya file backup, Bash theek hai. Agar aapko data structures chahiye, JSON ya YAML padhna hai, API se baat karni hai, ya testing chahiye, to Python. Python har jagah pehle se install nahi hoti, isliye bahut chhote bootstrap scripts Bash mein hi rakhte hain. Dono ek doosre ke dushman nahi, aap dono ko jodte ho.

### [05:00 – 08:30] Scene 3: Virtual Environment aur pip
**[VISUAL: Terminal: `python3 -m venv .venv`, `source .venv/bin/activate`, `pip install requests boto3`, `pip freeze > requirements.txt`. A project folder with `.venv` ignored in git.]**

**(Voiceover):**
Pehla rule: har project ke liye alag virtual environment. `python3 -m venv .venv` banata hai, `source .venv/bin/activate` use chalu karta hai. Ab `pip install requests boto3` sirf is project ke liye install hoga. `pip freeze > requirements.txt` se dependencies ki list save hoti hai, taaki doosra insaan ya pipeline wahi versions install kar sake. `.venv` folder ko git mein commit nahi karte, `.gitignore` mein daalte hain.

### [08:30 – 11:30] Scene 4: Lab: Pehli DevOps Script
**[VISUAL: A Python file `sysinfo.py` using `platform`, `shutil.disk_usage` and `os`. Terminal prints disk usage with percentage.]**

**(Voiceover):**
Lab:
```python
import platform, shutil

total, used, free = shutil.disk_usage("/")
pct = used / total * 100
print(f"Host: {platform.node()}  OS: {platform.system()}")
print(f"Disk used: {pct:.1f}%")
if pct > 90:
    raise SystemExit("FAIL: disk almost full")
```
`python sysinfo.py` chalao. Dekho: `raise SystemExit` ek non-zero exit code deta hai, jo pipeline ya cron ko batata hai ki kuch galat hai. Ye wahi health-check hai jo hamne Bash mein likhi thi, par ab data structures ke saath, aur aage badhne ke liye taiyaar.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "venv · pip · requirements.txt · exit codes".]**

**(Voiceover):**
Recap: Bash aur Python ka sahi use, venv aur requirements. Ab DevOps ka data: JSON, YAML aur API responses ko Python mein handle karna seekhte hain.

---

# 📺 EPISODE 2: Data Handling — JSON, YAML aur requests

### [00:00 – 01:15] Scene 1: Har Tool JSON Bolta Hai
**[VISUAL: AWS CLI output as JSON, a Kubernetes manifest as YAML, a GitHub API response, all flowing into a Python icon.]**

**(Voiceover):**
DevOps mein har tool data bheji hai: AWS API JSON deti hai, Kubernetes aur CI configs YAML mein hote hain, GitHub API bhi JSON. Isliye Python ka sabse roz ka kaam hai in formats ko padhna, badalna aur likhna.

### [01:15 – 05:00] Scene 2: JSON aur YAML
**[VISUAL: A JSON object next to the same data in YAML. Python: `json.load`, `json.dumps(indent=2)`, `yaml.safe_load`.]**

**(Voiceover):**
`json` module built-in hai: `json.load(file)` file se dictionary, `json.dumps(data, indent=2)` sundar text. YAML ke liye `pip install pyyaml` aur `yaml.safe_load(text)`. Yahan `safe_load` zaroori hai, kyunki sirf `load` aise YAML se code chala sakta tha jo aapne kabhi socha nahi. Dono formats ek dictionary ya list mein badal jaate hain, aur uske baad Python ka normal logic chal sakta hai.

### [05:00 – 08:30] Scene 3: requests se API Call
**[VISUAL: `requests.get(url, timeout=5)`, `resp.raise_for_status()`, `resp.json()`. A status code card: 200, 401, 404, 429, 500.]**

**(Voiceover):**
`requests.get(url, timeout=5)` se API call. Hamesha `timeout` do, warna script ghanton atak sakti hai. `resp.raise_for_status()` 4xx ya 5xx par exception uthata hai, aur `resp.json()` jawab ko dictionary banata hai. Status codes ke arth yaad rakho: 200 theek, 401 pehchaan nahi, 404 mila nahi, 429 bahut zyada requests, 500 server ki galti. Token ya password code mein mat likho, environment variable se padho: `os.environ["TOKEN"]`.

### [08:30 – 11:30] Scene 4: Lab: Health Endpoint Checker
**[VISUAL: `services.yaml` with URLs. A script reads it, calls each URL with a timeout, prints a table of UP/DOWN with latency.]**

**(Voiceover):**
Lab: `services.yaml` mein kuch URLs likho:
```yaml
services:
  - name: example
    url: https://example.com
```
Phir:
```python
import time, requests, yaml
cfg = yaml.safe_load(open("services.yaml"))
for s in cfg["services"]:
    t = time.time()
    try:
        r = requests.get(s["url"], timeout=5)
        r.raise_for_status()
        print(f'UP   {s["name"]} {time.time()-t:.2f}s')
    except requests.RequestException as e:
        print(f'DOWN {s["name"]} {e.__class__.__name__}')
```
Ek galat URL daal kar DOWN bhi dekho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "json · yaml.safe_load · requests + timeout · env vars for secrets".]**

**(Voiceover):**
Recap: JSON, YAML, requests, aur secrets ko code se bahar rakhna. Ab bade khel ka time: Python se seedha AWS ko control karna, boto3 ke saath.

---

# 📺 EPISODE 3: boto3 — Python se AWS

### [00:00 – 01:15] Scene 1: Console ke 50 Click
**[VISUAL: A person clicking through the AWS console to tag 50 instances one by one. A Python script does it in 2 seconds.]**

**(Voiceover):**
Console mein pachaas instances ko ek ek karke tag karna, ye click ka khel hai. Python ke saath ye ek loop hai. AWS ki sabhi cheezein API se control hoti hain, aur Python ka official library boto3 us API ka aasan interface hai. Dhyaan: abhi tak aapne AWS account nahi banaya ho to is episode ko samajhne ke liye dekh lo, aur account bante hi lab chalaana.

### [01:15 – 05:00] Scene 2: Credentials aur Client vs Resource
**[VISUAL: A diagram: Python script → boto3 → credentials chain (env vars, `~/.aws/credentials`, IAM role) → AWS API. A warning on hardcoded keys.]**

**(Voiceover):**
boto3 credentials khud dhoondhta hai: environment variables, `~/.aws/credentials` ya, EC2 par chalti script ke liye, IAM role. Keys ko kabhi code mein mat likho, kabhi git mein mat daalo. Setup ke liye `aws configure`. Code mein `boto3.client("ec2")` low-level API deta hai, jo ek-ek call ko seedha map karta hai. Is course mein hum zyadatar client ka use karenge kyunki wo naye features ke saath hamesha updated rehta hai.

### [05:00 – 08:30] Scene 3: Instances List, Tag aur Pagination
**[VISUAL: Code: `ec2.describe_instances()` with nested Reservations → Instances; a paginator snippet; filter by tag.]**

**(Voiceover):**
`ec2.describe_instances()` ka jawab nested hota hai: Reservations ke andar Instances. Filter lagana ho to `Filters=[{"Name":"tag:Env","Values":["dev"]}]`. Aur bade accounts mein jawab ek baar mein poora nahi aata, to paginator use karo: `ec2.get_paginator("describe_instances")`. Tag lagane ke liye `ec2.create_tags(Resources=[id], Tags=[...])`. Ek important aadat: pehle read-only script likho, aur kuch badalne wali script ke liye `DryRun=True` jaise options pehle try karo.

### [08:30 – 11:30] Scene 4: Lab: Idle Instance Report
**[VISUAL: A script prints instance id, type, state, Name tag. Instances without an "Owner" tag are flagged in yellow.]**

**(Voiceover):**
Lab (jab AWS account ho):
```python
import boto3
ec2 = boto3.client("ec2")
for page in ec2.get_paginator("describe_instances").paginate():
    for r in page["Reservations"]:
        for i in r["Instances"]:
            tags = {t["Key"]: t["Value"] for t in i.get("Tags", [])}
            flag = "" if "Owner" in tags else "  <- no Owner tag"
            print(i["InstanceId"], i["InstanceType"], i["State"]["Name"], tags.get("Name", "-"), flag)
```
Ye read-only hai, kuch badalta nahi. Is tarah ka report cost aur governance mein bahut kaam aata hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "boto3 client · credentials chain · paginate · tags · read-only first".]**

**(Voiceover):**
Recap: boto3 ka client, credentials, pagination aur tags. Ab ek zaroori sawaal: script toote to? Agla episode robustness ka hai.

---

# 📺 EPISODE 4: Robust Automation

### [00:00 – 01:15] Scene 1: Script Jo Chup Chaap Fail Hui
**[VISUAL: A cron job emails nothing for a week. A log shows the script died on day 1 with a ConnectionError. A "silent failure" stamp.]**

**(Voiceover):**
Ek automation script jo ek hafte tak chup-chaap fail hoti rahi, usse zyada khatarnaak kuch nahi, kyunki sab ko lagta hai ki sab theek hai. Isliye robust script ki teen aadatein: errors ko pakadna, logging karna, aur sahi exit code dena.

### [01:15 – 05:00] Scene 2: try/except aur Retry
**[VISUAL: A code block with `try`, `except botocore.exceptions.ClientError as e`, `else`, `finally`. A retry loop with backoff delays 1s, 2s, 4s.]**

**(Voiceover):**
`try/except` mein sirf wohi error pakdo jiske liye aapke paas plan ho, jaise `requests.RequestException` ya `botocore.exceptions.ClientError`. Khali `except:` mat likho, wo har cheez nigal leta hai. Network jaisi temporary problems ke liye retry with backoff: pehle 1 second, phir 2, phir 4 rukkar dobara try karo, aur kuch limit ke baad haar maan lo. Aur `finally` mein safai karo, jaise file ya connection band karna.

### [05:00 – 08:30] Scene 3: logging aur Config
**[VISUAL: Code: `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")`. Output lines. Config via `argparse` and env vars.]**

**(Voiceover):**
`print` ki jagah `logging` use karo: usme time, level aur message hote hain, aur level se control hota hai ki kitna detail dikhe. `logging.info`, `logging.warning`, `logging.error`. Script ke settings ko hardcode mat karo: `argparse` se command-line options lo, jaise `--region` aur `--dry-run`. Aur secrets environment variables se. Aise script alag environments mein bina badle chalti hai.

### [08:30 – 11:30] Scene 4: Lab: Disk aur Service Report
**[VISUAL: A small tool with `argparse`, logging, and a JSON output option. Run with `--json`, pipe into `jq`.]**

**(Voiceover):**
Lab: pehle wala disk-check script lo aur use sudharo. `argparse` se `--path` aur `--threshold` lo, `logging` se result likho, aur `--json` flag par output JSON mein do. Agar threshold cross ho to `sys.exit(1)`. Test: `python check.py --path / --threshold 1` fail hona chahiye, aur `--threshold 99` pass. Ab ye script CI pipeline ya cron mein lagane layak hai.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "specific except · retry/backoff · logging · argparse · exit codes".]**

**(Voiceover):**
Recap: Python ab aapke automation ka dimaag hai. Bash glue hai, Python logic. Ab hum cloud mein utarte hain. AWS ke sessions shuru, aur pehli cheez: EC2, yaani cloud ka server.

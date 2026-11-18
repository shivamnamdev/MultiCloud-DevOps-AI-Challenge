# ✍️ 02: SCRIPT — SESSION-07: Python for DevOps
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`. Assumes basics from the "Think in Python" course.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S07`
- **Focus:** Why Python after Bash, virtual environments and pip, JSON and YAML, HTTP and APIs with `requests`, `boto3` for AWS, error handling, retry, logging, `argparse`, exit codes
- **Story position:** Zoom levels 1 to 2. Slip se kaam nahi chalta, to Atithi ek trained operations officer rakhta hai, jo landlord ke office ko phone bhi kar sakta hai.
- **Story words used:** instruction slip (bash script), operations officer (Python), phone line to the landlord's office (boto3), building (server), landlord (cloud provider), staff at the landlord's office (IAM), logbook, timetable (cron)
- **Lab project:** health checks for the Atithi booking website. Episode 2 needs no cloud account. Episode 3 needs an AWS account and an IAM user with read-only access, so students who have not reached Sessions 08 and 09 watch it first and run the lab after those sessions.
- **Episodes:**
  - Episode 1: Slip se Officer Tak: Bash vs Python, venv aur pip
  - Episode 2: Data Handling: JSON, YAML, files aur requests
  - Episode 3: boto3: Landlord ke Office ko Phone
  - Episode 4: Bharosemand Automation: Errors, Retry, Logging aur ek Report Tool

---

# 📺 EPISODE 1: Slip se Officer Tak

### [00:00 – 02:40] Scene 1: Do Sau Line ki Slip ka Dard
**[VISUAL: A 200-line bash slip pinned to the Atithi back-office wall: nested quotes, `awk`, `sed`, a JSON file being parsed with `grep`. Two staff stand in front of it, confused. A red stamp: "nobody dares touch this". Beside it, a trained operations officer with a 20-line, neatly typed page.]**

**(Voiceover):**
Pichhle session mein humne bash ki parchiyan likhi, aur wo chhote kaam ke liye zabardast hain. Par Atithi ab badi ho rahi hai. Ek din parchi mein booking ka JSON data padhna pada, phir landlord ke office ko poochna pada, aur logic mein teen jagah faisle aaye. Parchi do sau line ki ho gayi, quotes ka jaal, `awk` aur `sed` ki chainein, aur ek jagah typo ho to poori behak jaati hai. Aisi parchi ko koi haath nahi lagata. Is jagah par chahiye ek trained operations officer, yaani Python. Wahi kaam kam lines mein, saaf tareeke se, aur jise baad mein koi bhi padh sake. Is session mein hum Python ko DevOps ka ek aujaar banate dekhenge. Is episode mein: slip se officer tak.

### [02:40 – 05:15] Scene 2: Kab Slip, Kab Officer?
**[VISUAL: A decision tree on the wall: "A few commands glued together?" → slip (Bash). "Need JSON, APIs, data structures, tests?" → officer (Python). "Must run on every Linux box with nothing installed?" → slip (Bash). A small Venn: both tools overlapping in the middle.]**

**(Voiceover):**
Thumb rule seedha hai. Agar kaam kuch commands ko jodne ka hai, jaise log mein search ya folder ka backup, to slip, yaani bash, theek hai. Agar aapko data structures chahiye, JSON ya YAML padhna hai, API se baat karni hai, ya parchi ka test likhna hai, to officer, yaani Python. Python har jagah pehle se installed nahi hoti, isliye bahut chhote bootstrap kaam bash mein hi rakhte hain, jaise naye server par Python install karna. Dono dushman nahi hain. DevOps mein aap dono ko jodte ho: bash ek kaam shuru karta hai, Python uska dimaag chalata hai. Aur jo parchi aapne Session 5 aur 6 mein likhi, wahi kaam aaj hum Python mein dekhenge, taaki farq saamne ho.

### [05:15 – 09:55] Scene 3: Virtual Environment aur pip
**[VISUAL: Terminal: `sudo apt install python3-venv`, `python3 -m venv .venv`, `source .venv/bin/activate`, the prompt changes to `(.venv)`, `pip install requests boto3 pyyaml`, `pip freeze > requirements.txt`. A project folder with `.venv` listed in `.gitignore`. A message "externally-managed-environment" greyed out beside a system-wide pip install.]**

**(Voiceover):**
Pehla rule: har project ke liye alag virtual environment. Ye project ka apna chhota workshop hai, jisme sirf uske aujaar rakhe jaate hain. Ubuntu par pehle `sudo apt install python3-venv` ho sakta hai. Phir `python3 -m venv .venv` workshop banata hai, aur `source .venv/bin/activate` usme ghusa deta hai. Prompt ke aage `(.venv)` aa jayega. `which python` batata hai ki aap venv ka Python chala rahe ho ya system ka, aur bahar nikalne ke liye `deactivate`. `python3 -m pip install` likho to pakka rehta hai ki wahi Python install kar raha hai jo aap chala rahe ho; galat pip se install ho jaana ek aam dikkat hai. Ye teen cheezein har naye project ki pehli aadat banao. Venv, requirements aur gitignore: tino ek saath. Ab `pip install requests boto3 pyyaml` sirf is project ke liye install hoga. Naye Ubuntu par agar aap bina venv ke seedha system mein pip chalane ki koshish karoge, to wo mana kar dega, kyunki system ke apne Python packages kharab ho sakte hain. `pip freeze > requirements.txt` se aujaaron ki list saved ho jaati hai, taaki doosra insaan ya pipeline wahi versions install kar sake: `pip install -r requirements.txt`. `.venv` folder ko git mein commit nahi karte, use `.gitignore` mein daalte hain, jaise Session 16 mein `.env` ke saath kiya tha.

### [09:55 – 12:25] Scene 4: Lab: Pehli Officer wali Report
**[VISUAL: A Python file `sysinfo.py` in an editor. Terminal prints the building name, the OS and the disk percentage. A second run with a low limit prints "FAIL: disk almost full" and `echo $?` shows 1.]**

**(Voiceover):**
Lab:
```python
import platform
import shutil

total, used, free = shutil.disk_usage("/")
pct = used / total * 100
print(f"Building: {platform.node()}  OS: {platform.system()}")
print(f"Disk used: {pct:.1f}%")
if pct > 90:
    raise SystemExit("FAIL: disk almost full")
```
`python sysinfo.py` chalao. `raise SystemExit("...")` ek message print karta hai aur non-zero exit code se band hota hai. Pichhle session wala wahi niyam: cron ya pipeline ko exit code se pata chalta hai ki kuch galat hai. Dekhne ke liye `if pct > 90` ko `if pct > 1` kar do, phir chalao aur `echo $?` dekho. Ye wahi health-check hai jo bash mein likhi thi, par ab data aur logic ke saath, aur aage badhne ke liye taiyaar.

### [12:25 – 13:05] Scene 5: Recap aur Bridge
**[VISUAL: A card: "bash = glue · Python = logic · venv · pip · requirements.txt · exit code".]**

**(Voiceover):**
Recap: bash aur Python ka sahi use, venv, requirements aur exit code. Ab officer ko data padhna sikhate hain: DevOps ke tool JSON aur YAML mein baat karte hain.

---

# 📺 EPISODE 2: Data Handling

### [00:00 – 01:25] Scene 1: Har Tool ek Hi Zubaan Bolta Hai
**[VISUAL: The landlord's office reply as a JSON page, a Kubernetes manifest as YAML, the GitHub vault's reply as JSON, all flowing into one operations-officer desk.]**

**(Voiceover):**
Landlord ke office ka jawab JSON mein aata hai. Kubernetes ki fileein YAML mein hoti hain, aur CI ki settings bhi. GitHub vault se jo jawab milta hai, wo bhi JSON. DevOps ke tool data ki zubaan mein baat karte hain. Isliye officer ka sabse roz ka kaam hai in formats ko padhna, badalna aur likhna.

### [01:25 – 04:15] Scene 2: JSON aur YAML
**[VISUAL: A JSON object next to the same data as YAML. Python snippets below: `json.load(f)`, `json.dumps(data, indent=2)`, `yaml.safe_load(text)`. A caution sign on plain `yaml.load`.]**

**(Voiceover):**
`json` module Python ke saath hi aata hai. `json.load(file)` ek file se dictionary banata hai, aur `json.dumps(data, indent=2)` dictionary ko sundar text bana deta hai. YAML ke liye `pip install pyyaml`, aur `yaml.safe_load(text)`. Yahan `safe_load` zaroori hai, kyunki purana seedha `load` aisi YAML se bhi code chala sakta tha jo aapne soch bhi nahi thi. Naye PyYAML mein bina Loader ke `load` ab TypeError deta hai, par `UnsafeLoader` ke saath humne ek YAML se `os.getcwd` chalwa liya. Dono formats ek dictionary ya list ban jaate hain, aur uske baad Python ka normal logic lag sakta hai: key dhundho, loop chalao, shart lagao. Yaad rakho ki YAML mein spaces se structure hota hai, tab nahi.

### [04:15 – 06:45] Scene 3: requests se API ko Phone
**[VISUAL: Code: `requests.get(url, timeout=5)`, `resp.raise_for_status()`, `resp.json()`. A status code card: 200 theek, 401 pehchaan nahi, 404 mila nahi, 429 bahut zyada requests, 500 server ki galti. A line `token = os.environ["TOKEN"]` with a red cross on a hard-coded token.]**

**(Voiceover):**
Kisi bhi website ya API ko phone karna ho to `requests`. `requests.get(url, timeout=5)`: aur `timeout` hamesha do, warna agar doosri taraf se jawab hi na aaye to parchi ghanton atki rahegi. `resp.raise_for_status()` 4xx ya 5xx jawab par exception uthata hai, aur `resp.json()` jawab ko dictionary bana deta hai. Status codes yaad rakho: 200 theek, 401 pehchaan nahi hui, 404 mila nahi, 429 bahut zyada requests, 500 server ki apni galti. Aur token ya password kabhi code mein mat likho. Environment variable se padho: `os.environ["TOKEN"]`. Wahi niyam jo Git wale session mein tha: secret `.env` mein, aur `.env` register se bahar.

### [06:45 – 10:15] Scene 4: Files aur Folders: with aur pathlib
**[VISUAL: Code: `with open("report.txt", "w") as f: f.write(...)`, then `from pathlib import Path`, `Path("logs").glob("*.log")`, `p.read_text()`, `p.stat().st_size`, `Path.home() / "atithi-booking"`. A card: "with = the file always closes".]**

**(Voiceover):**
Servers par aadhi kahani files ki hoti hai, aur Python mein files ke saath ek aadat zaroori hai: `with open("report.txt", "w") as f:`. `with` ka matlab hai ki kaam khatam hote hi file apne aap band ho jaayegi, chahe beech mein galti ho. Bina `with` ke file khuli reh sakti hai. Folders aur paths ke liye `pathlib` ka `Path` use karo. `Path("logs").glob("*.log")` folder ki saari log files deta hai, bilkul bash ke `*.log` ki tarah. `p.read_text()` poori file padhta hai, aur `p.stat().st_size` uska size. Aur paths jodne ke liye `/` ka nishaan: `Path.home() / "atithi-booking"`. Isse har system par sahi separator lagta hai, aur string jodne ki galtiyan nahi hoti. Isi tarah ek parchi ek folder ki saari log files mein se wo lines chun sakti hai jisme ERROR likha ho, aur wahi bash ke `grep` aur `for` ka kaam hai.

### [10:15 – 13:25] Scene 5: Lab: Booking Site ka Health Checker
**[VISUAL: A `services.yaml` listing three URLs. A Python script reads it, calls each URL with a timeout and prints a table of UP and DOWN with the time each took. One URL is deliberately wrong and shows DOWN.]**

**(Voiceover):**
Lab. `services.yaml` mein Atithi ki cheezein likho. Abhi asli site nahi hai, to example.com use karo:
```yaml
services:
  - name: booking-home
    url: https://example.com
  - name: booking-api
    url: https://example.com/missing
  - name: not-a-site
    url: https://this-site-does-not-exist.invalid
```
Phir checker:
```python
import time
import requests
import yaml

with open("services.yaml") as f:
    cfg = yaml.safe_load(f)

for s in cfg["services"]:
    start = time.time()
    try:
        r = requests.get(s["url"], timeout=5)
        r.raise_for_status()
        print(f'UP   {s["name"]} {time.time() - start:.2f}s')
    except requests.RequestException as e:
        print(f'DOWN {s["name"]} {e.__class__.__name__}')
```
Chalao. Pehli URL UP aani chahiye, doosri 404 se DOWN, aur teesri DNS ki wajah se DOWN. Wahi kaam jo Session 6 mein bash ke ping loop ne kiya tha, par ab ye asli HTTP jawab dekhta hai. Jab Atithi ki site cloud par aayegi, to bas `services.yaml` mein URL badalna hai.

### [13:25 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "json · yaml.safe_load · requests + timeout · raise_for_status · secrets in env vars".]**

**(Voiceover):**
Recap: JSON, YAML, requests, aur secrets ko code se bahar rakhna. Ab bade kaam ka waqt: officer ko landlord ke office ka phone number dete hain. Python se seedha cloud ko control karna, boto3 ke saath.

---

# 📺 EPISODE 3: boto3

### [00:00 – 02:15] Scene 1: Console ke Pachaas Click
**[VISUAL: A staff member in the landlord's portal clicking through fifty rented buildings one at a time to add a label "Owner". A clock ticks. Then a Python loop does it in seconds.]**

**(Voiceover):**
Landlord ke portal par pachaas buildings ko ek ek karke label lagana, ye click ka khel hai. Aur ek bhi chhoot gayi to pata nahi chalega. Landlord ke office ke saare kaam ek API se hote hain, yaani ek phone number se, aur Python ke paas us number ka official phone hai: boto3. Ek loop mein wahi pachaas label lag jaate hain. Dhyaan rahe: is episode ki lab ke liye AWS account chahiye, jo hum agle session mein banayenge, aur ek aisa IAM user jise sirf padhne ka haq ho. Abhi dekh lo, aur account banne ke baad dobara chalana.

### [02:15 – 04:55] Scene 2: Credentials aur Client
**[VISUAL: A diagram: Python script → boto3 → credentials search order (environment variables, `~/.aws/credentials`, an IAM role on the building) → landlord's API. A red banner over a hard-coded access key: "never in code, never in git".]**

**(Voiceover):**
Landlord ke office mein aap bina pehchaan ke phone nahi kar sakte. boto3 pehchaan khud dhoondhta hai, ek tay kram mein: pehle environment variables, phir `~/.aws/credentials` file, aur agar script kisi rented building par chal rahi ho to us building ko mila hua IAM role, yaani temporary duty badge. Isliye keys kabhi code mein mat likho aur kabhi git mein mat daalo. Setup ke liye `aws configure`. Code mein `boto3.client("ec2")` ek seedha phone hai: jo API call hoti hai wahi ek ek karke map hoti hai. boto3 mein `resource` naam ka ek aasan style bhi milta hai, par naye features ke saath client hamesha updated rehta hai, isliye hum is course mein client hi use karenge.

### [04:55 – 06:55] Scene 3: Buildings ki List, Labels aur Pagination
**[VISUAL: Code: `ec2.describe_instances()` with the nested shape Reservations → Instances highlighted; a filter `Filters=[{"Name": "tag:Env", "Values": ["dev"]}]`; a paginator snippet; `ec2.create_tags(Resources=[id], Tags=[...], DryRun=True)`. A speech bubble: "read-only first".]**

**(Voiceover):**
`ec2.describe_instances()` ka jawab nested aata hai: Reservations ke andar Instances, yaani buildings. Filter lagana ho to `Filters=[{"Name": "tag:Env", "Values": ["dev"]}]`. Bade accounts mein landlord jawab ek hi baar mein poora nahi deta, wo panne mein deta hai. Isliye paginator use karo: `ec2.get_paginator("describe_instances")`, aur wo agle panne khud mangwa leta hai. Label lagane ke liye `ec2.create_tags(Resources=[id], Tags=[...])`. Ek aadat jo bahut bachati hai: pehle sirf padhne wali parchi likho. Aur jo kuch badalti hai, usme pehle `DryRun=True` try karo, jisme landlord batata hai ki kaam ho jaata, bina kiye.

### [06:55 – 10:50] Scene 4: Kuch Badalna: Safe Tareeka aur Waiters
**[VISUAL: Code: `ec2.stop_instances(InstanceIds=[iid], DryRun=True)` raising `ClientError` with `Error.Code == "DryRunOperation"`; then the real call; then `ec2.get_waiter("instance_stopped").wait(InstanceIds=[iid])`. A selector line: `Filters=[{"Name": "tag:Env", "Values": ["dev"]}]`. A clock showing 8 pm: "dev buildings sleep at night".]**

**(Voiceover):**
Ab padhne ke baad ek kaam jo kuch badalta hai. Maan lo dev ki buildings raat ko kisi kaam ki nahi hain, aur Atithi unhe raat ko band karke bill bachana chahta hai. Pehle sirf unhe chuno jinka label Env dev ho, filter se. Phir band karne se pehle `DryRun=True` ke saath try karo: `ec2.stop_instances(InstanceIds=[iid], DryRun=True)`. Yahan ek ajeeb baat hai. Agar sab theek hota, to landlord ek error deta hai, `ClientError`, jiska code `DryRunOperation` hota hai. Matlab: ye kaam ho jaata. Agar uski jagah `UnauthorizedOperation` aaye, to aapko uski ijaazat hi nahi hai. Dono ko pakad kar aap bina kuch badle jaan lete ho ki aage badhna theek hai ya nahi. Phir asli call, bina `DryRun`. Aur kaam turant nahi hota, building ko band hone mein kuch samay lagta hai. Isliye boto3 mein waiters hain: `ec2.get_waiter("instance_stopped").wait(InstanceIds=[iid])` jab tak building band na ho jaaye, tab tak parchi ko thama rakhta hai. Ye wahi pattern hai jo aage Terraform aur Ansible ke piche chalta hai: pehle dekho kya badlega, phir badlo, phir tasalli karo.

### [10:50 – 13:30] Scene 5: Lab: Bina Owner Label ki Buildings
**[VISUAL: A script prints each building's id, size, state and Name label. Buildings that have no "Owner" label are flagged "<- no Owner tag". A second run, after one label is added, shows the flag disappear.]**

**(Voiceover):**
Lab, jab AWS account aur read-only IAM user ho:
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
Ye sirf padhti hai, kuch badalti nahi. Agar `NoRegionError` aaye to `aws configure` mein region daalna bhool gaye. Aur khaali account mein koi building nahi hogi, to Session 8 ke baad dobara chalao. Is tarah ki report landlord ke bill aur zimmedari, dono mein bahut kaam aati hai: pata chalta hai ki kaun si building kiski hai, aur kaun si koi bhool gaya.

### [13:30 – 14:10] Scene 6: Recap aur Bridge
**[VISUAL: A card: "boto3 client · credentials order · paginate · tags · DryRun · read-only first".]**

**(Voiceover):**
Recap: boto3 ka client, pehchaan ka kram, pagination aur labels. Ab ek zaroori sawaal: officer ka phone beech mein kat jaaye, ya parchi toot jaaye, to? Agle episode mein bharosemand automation.

---

# 📺 EPISODE 4: Bharosemand Automation

### [00:00 – 01:00] Scene 1: Officer Jo Chup Chaap Fail Hua
**[VISUAL: The back-office timetable ticks every night. A logbook page shows a single error on day 1 ("ConnectionError") and then nothing for six days. A "silent failure" stamp. The manager checks on day 7: nothing has been backed up.]**

**(Voiceover):**
Ek officer jo ek hafte tak chup-chaap fail hota raha, usse zyada khatarnaak kuch nahi. Sab ko lagta hai ki sab theek hai, jabki pehle hi din kaam toot gaya tha. Isliye bharosemand automation ki teen aadatein: galti ko pakadna, uska hisaab logbook mein likhna, aur sahi exit code dena.

### [01:00 – 03:10] Scene 2: try/except aur Retry
**[VISUAL: A code block with `try`, `except botocore.exceptions.ClientError as e`, `else`, `finally`. A retry loop with growing waits: 1 second, 2 seconds, 4 seconds, then giving up. A crossed-out bare `except:`.]**

**(Voiceover):**
`try` aur `except` mein sirf wahi galti pakdo jiske liye aapke paas plan ho. Jaise `requests.RequestException`, ya boto3 ke liye `botocore.exceptions.ClientError`. Khaali `except:` mat likho, wo har cheez nigal leta hai, aur aapko pata hi nahi chalta ki kya toota. Network jaisi temporary problems ke liye retry with backoff: pehli baar fail hone par ek second ruko, phir do, phir char, aur kuch koshishon ke baad haar maan lo aur galti ko upar jaane do. Har baar turant dobara try karna phone line ko aur thakata hai. `else` tab chalta hai jab kuch fail nahi hua, aur `finally` mein safai hoti hai: file ya connection band karna.

### [03:10 – 05:05] Scene 3: logging aur Settings
**[VISUAL: Code: `logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")`. Three output lines with INFO, WARNING and ERROR. Then `argparse` with `--path`, `--threshold`, `--json`, and an environment variable for a secret.]**

**(Voiceover):**
`print` ki jagah `logging` lagao. Usme time, level aur message hote hain, aur level se control hota hai ki kitna detail dikhe: `logging.info`, `logging.warning`, `logging.error`. Ek aur baat: logging ka jawab by default error stream mein jaata hai, aur asli output, jaise JSON, normal output mein, isliye dono ko alag karke pipe kiya ja sakta hai. Parchi ki settings code mein hardcode mat karo. `argparse` se command line ke options lo, jaise `--path` aur `--threshold`, aur secret environment variable se. Aise ek hi script alag alag buildings aur alag alag environments mein bina badle chalti hai.

### [05:05 – 07:55] Scene 4: Shell Command Python se: subprocess
**[VISUAL: Code: `r = subprocess.run(["systemctl", "is-active", "nginx"], capture_output=True, text=True)`, `r.returncode`, `r.stdout.strip()`; then `check=True` raising `CalledProcessError`. A red cross over `subprocess.run(f"ls {user_input}", shell=True)`.]**

**(Voiceover):**
Kabhi kabhi officer ko bash ki koi command chalani padti hai, jaise `systemctl is-active nginx`. Iske liye `subprocess.run`. Command ko ek list ke roop mein do, `["systemctl", "is-active", "nginx"]`, aur `capture_output=True, text=True` lagao, to jawab text mein aata hai. `r.returncode` exit code hai, jo zero ka matlab theek, aur `r.stdout` command ka jawab. Agar chahte ho ki fail hone par galti uthe, to `check=True` lagao, aur fail hone par `CalledProcessError` aayega, jise aap pakad sakte ho. Ek zaroori chetavni: `shell=True` ke saath kisi user se aaya hua text kabhi command mein mat jodo. Koi `; rm -rf` jaisi cheez jod sakta hai, aur wo chal jaayegi. List wala tareeka bina shell ke chalta hai, isliye surakshit hai. Isi se bash aur Python ek doosre ke saath chalte hain: Python faisla leta hai, aur zaroorat padne par bash wali command bula leta hai.

### [07:55 – 11:45] Scene 5: Lab: Disk Report Tool
**[VISUAL: A small tool in the editor. Terminal: `python check.py --path / --threshold 99` prints the log line and exits with 0; `python check.py --path / --threshold 1 --json` prints JSON and exits with 1; the JSON output is piped into `jq`.]**

**(Voiceover):**
Lab. Pichhli disk wali script ko asli tool banate hain:
```python
import argparse
import json
import logging
import shutil
import sys


def is_ok(pct, limit):
    return pct < limit


def main():
    p = argparse.ArgumentParser(description="Disk check for one building")
    p.add_argument("--path", default="/")
    p.add_argument("--threshold", type=int, default=90)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    total, used, _ = shutil.disk_usage(a.path)
    pct = round(used / total * 100, 1)
    ok = is_ok(pct, a.threshold)

    if a.json:
        print(json.dumps({"path": a.path, "used_percent": pct,
                          "threshold": a.threshold, "ok": ok}))
    log = logging.info if ok else logging.error
    log("disk %s used %.1f%% (limit %d%%)", a.path, pct, a.threshold)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
```
`python check.py --path / --threshold 99` pass hona chahiye. `python check.py --threshold 1 --json` fail hoga, exit code 1, aur JSON alag print hoga. Isse `| jq .` se pipe karke dekho. Ek dhyaan: aakhri `if __name__ == "__main__":` wali line zaroori hai. Uske bina `from check import is_ok` karte hi poori script chal padti hai, aur pytest ke arguments par argparse gir jaata hai; humne yahi dekha. Ab ye tool cron mein lagane layak hai. Cron ise chalaye, exit code dekhe, aur kuch toote to aapko pata chale.

### [11:45 – 14:15] Scene 6: Apni Parchi ka Test: pytest
**[VISUAL: A file `test_check.py`: `from check import is_ok`, `def test_pass(): assert is_ok(50, 90)`, `def test_fail(): assert not is_ok(95, 90)`. Terminal: `pip install pytest`, `pytest` printing two green dots. A short note: "logic in a function = testable".]**

**(Voiceover):**
Ek aakhri aadat jo bash mein mushkil thi aur Python mein aasaan hai: apni parchi ka test. Tareeka ye hai ki faisle wala hissa ek chhote function mein rakho. Jaise `check.py` mein `def is_ok(pct, limit): return pct < limit`, aur baaki parchi usi function ko bulaye. Ab ek alag file `test_check.py` mein, `from check import is_ok` ke saath, do chhote test: `assert is_ok(50, 90)` sach hona chahiye, aur `assert not is_ok(95, 90)` bhi. `pip install pytest` karo aur `pytest` chalao. Do hare nishaan matlab faisle ka tarika kaam kar raha hai. Ye test baad mein Jenkins ke pipeline mein bhi chalenge, aur har badlaav se pehle ek automatic inspection ka kaam karenge. Yahi wo jagah hai jahan officer slip se aage nikal jaata hai.

### [14:15 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "specific except · retry + backoff · logging · argparse · exit codes". Then the landlord's tower skyline appears on the horizon: rows of identical buildings in different cities.]**

**(Voiceover):**
Recap: ab officer sirf kaam nahi karta, bharosemand tareeke se karta hai: galti pakadta hai, logbook likhta hai aur sahi exit code deta hai. Bash slip ka kaam karti hai aur Python dimaag ka. Ab hum building ke andar se nikal kar bahar aate hain, landlord ke campus mein. Agla session AWS ka hai, aur pehli cheez: ek asli building kiraye par lena, yaani EC2.

---

# 📎 Student handout: Session 07 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Kaam | Command ya code |
|---|---|
| Virtual environment | `python3 -m venv .venv`, `source .venv/bin/activate` |
| Install aur list | `pip install requests boto3 pyyaml`, `pip freeze > requirements.txt`, `pip install -r requirements.txt` |
| JSON | `json.load(f)`, `json.dumps(data, indent=2)` |
| YAML | `yaml.safe_load(text)` |
| HTTP call | `requests.get(url, timeout=5)`, `resp.raise_for_status()`, `resp.json()` |
| Secret padhna | `os.environ["TOKEN"]` |
| boto3 client | `boto3.client("ec2")`, setup: `aws configure` |
| Panne ka jawab | `client.get_paginator("describe_instances").paginate()` |
| Kuch badalne se pehle | `DryRun=True` |
| Sirf ye galti pakdo | `except requests.RequestException`, `except botocore.exceptions.ClientError` |
| Retry | 1 s, 2 s, 4 s ruk kar; limit ke baad galti uthao |
| Log | `logging.info / warning / error` |
| Command line options | `argparse`: `add_argument("--path")`, `type=int`, `action="store_true"` |
| Exit code | `sys.exit(0)` theek, `sys.exit(1)` galti, `raise SystemExit("msg")` |

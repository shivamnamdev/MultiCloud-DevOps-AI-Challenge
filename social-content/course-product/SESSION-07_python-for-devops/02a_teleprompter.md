# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-07_python-for-devops

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,347 · **Episodes:** 4

---

# EPISODE 1: Slip se Officer Tak

## Do Sau Line ki Slip ka Dard

Pichhle session mein humne bash ki parchiyan likhi, aur wo chhote kaam ke liye zabardast hain. Par Atithi ab badi ho rahi hai. Ek din parchi mein booking ka JSON data padhna pada, phir landlord ke office ko poochna pada, aur logic mein teen jagah faisle aaye. Parchi do sau line ki ho gayi, quotes ka jaal, awk aur sed ki chainein, aur ek jagah typo ho to poori behak jaati hai. Aisi parchi ko koi haath nahi lagata. Is jagah par chahiye ek trained operations officer, yaani Python. Wahi kaam kam lines mein, saaf tareeke se, aur jise baad mein koi bhi padh sake. Is session mein hum Python ko DevOps ka ek aujaar banate dekhenge. Is episode mein: slip se officer tak.

## Kab Slip, Kab Officer?

Thumb rule seedha hai. Agar kaam kuch commands ko jodne ka hai, jaise log mein search ya folder ka backup, to slip, yaani bash, theek hai. Agar aapko data structures chahiye, JSON ya YAML padhna hai, API se baat karni hai, ya parchi ka test likhna hai, to officer, yaani Python. Python har jagah pehle se installed nahi hoti, isliye bahut chhote bootstrap kaam bash mein hi rakhte hain, jaise naye server par Python install karna. Dono dushman nahi hain. DevOps mein aap dono ko jodte ho: bash ek kaam shuru karta hai, Python uska dimaag chalata hai. Aur jo parchi aapne Session 5 aur 6 mein likhi, wahi kaam aaj hum Python mein dekhenge, taaki farq saamne ho.

## Virtual Environment aur pip

Pehla rule: har project ke liye alag virtual environment. Ye project ka apna chhota workshop hai, jisme sirf uske aujaar rakhe jaate hain. Ubuntu par pehle sudo apt install python3-venv ho sakta hai. Phir python3 -m venv .venv workshop banata hai, aur source .venv/bin/activate usme ghusa deta hai. Prompt ke aage (.venv) aa jayega. which python batata hai ki aap venv ka Python chala rahe ho ya system ka, aur bahar nikalne ke liye deactivate. python3 -m pip install likho to pakka rehta hai ki wahi Python install kar raha hai jo aap chala rahe ho; galat pip se install ho jaana ek aam dikkat hai. Ye teen cheezein har naye project ki pehli aadat banao. Venv, requirements aur gitignore: tino ek saath. Ab pip install requests boto3 pyyaml sirf is project ke liye install hoga. Naye Ubuntu par agar aap bina venv ke seedha system mein pip chalane ki koshish karoge, to wo mana kar dega, kyunki system ke apne Python packages kharab ho sakte hain. pip freeze > requirements.txt se aujaaron ki list saved ho jaati hai, taaki doosra insaan ya pipeline wahi versions install kar sake: pip install -r requirements.txt. .venv folder ko git mein commit nahi karte, use .gitignore mein daalte hain, jaise Session 16 mein .env ke saath kiya tha.

## Lab: Pehli Officer wali Report

Lab:

python sysinfo.py chalao. raise SystemExit("...") ek message print karta hai aur non-zero exit code se band hota hai. Pichhle session wala wahi niyam: cron ya pipeline ko exit code se pata chalta hai ki kuch galat hai. Dekhne ke liye if pct > 90 ko if pct > 1 kar do, phir chalao aur echo $? dekho. Ye wahi health-check hai jo bash mein likhi thi, par ab data aur logic ke saath, aur aage badhne ke liye taiyaar.

## Recap aur Bridge

Recap: bash aur Python ka sahi use, venv, requirements aur exit code. Ab officer ko data padhna sikhate hain: DevOps ke tool JSON aur YAML mein baat karte hain.

---

# EPISODE 2: Data Handling

## Har Tool ek Hi Zubaan Bolta Hai

Landlord ke office ka jawab JSON mein aata hai. Kubernetes ki fileein YAML mein hoti hain, aur CI ki settings bhi. GitHub vault se jo jawab milta hai, wo bhi JSON. DevOps ke tool data ki zubaan mein baat karte hain. Isliye officer ka sabse roz ka kaam hai in formats ko padhna, badalna aur likhna.

## JSON aur YAML

json module Python ke saath hi aata hai. json.load(file) ek file se dictionary banata hai, aur json.dumps(data, indent=2) dictionary ko sundar text bana deta hai. YAML ke liye pip install pyyaml, aur yaml.safe_load(text). Yahan safe_load zaroori hai, kyunki purana seedha load aisi YAML se bhi code chala sakta tha jo aapne soch bhi nahi thi. Naye PyYAML mein bina Loader ke load ab TypeError deta hai, par UnsafeLoader ke saath humne ek YAML se os.getcwd chalwa liya. Dono formats ek dictionary ya list ban jaate hain, aur uske baad Python ka normal logic lag sakta hai: key dhundho, loop chalao, shart lagao. Yaad rakho ki YAML mein spaces se structure hota hai, tab nahi.

## requests se API ko Phone

Kisi bhi website ya API ko phone karna ho to requests. requests.get(url, timeout=5): aur timeout hamesha do, warna agar doosri taraf se jawab hi na aaye to parchi ghanton atki rahegi. resp.raise_for_status() 4xx ya 5xx jawab par exception uthata hai, aur resp.json() jawab ko dictionary bana deta hai. Status codes yaad rakho: 200 theek, 401 pehchaan nahi hui, 404 mila nahi, 429 bahut zyada requests, 500 server ki apni galti. Aur token ya password kabhi code mein mat likho. Environment variable se padho: os.environ["TOKEN"]. Wahi niyam jo Git wale session mein tha: secret .env mein, aur .env register se bahar.

## Files aur Folders: with aur pathlib

Servers par aadhi kahani files ki hoti hai, aur Python mein files ke saath ek aadat zaroori hai: with open("report.txt", "w") as f:. with ka matlab hai ki kaam khatam hote hi file apne aap band ho jaayegi, chahe beech mein galti ho. Bina with ke file khuli reh sakti hai. Folders aur paths ke liye pathlib ka Path use karo. Path("logs").glob(".log") folder ki saari log files deta hai, bilkul bash ke .log ki tarah. p.read_text() poori file padhta hai, aur p.stat().st_size uska size. Aur paths jodne ke liye / ka nishaan: Path.home() / "atithi-booking". Isse har system par sahi separator lagta hai, aur string jodne ki galtiyan nahi hoti. Isi tarah ek parchi ek folder ki saari log files mein se wo lines chun sakti hai jisme ERROR likha ho, aur wahi bash ke grep aur for ka kaam hai.

## Lab: Booking Site ka Health Checker

Lab. services.yaml mein Atithi ki cheezein likho. Abhi asli site nahi hai, to example.com use karo:

Phir checker:

Chalao. Pehli URL UP aani chahiye, doosri 404 se DOWN, aur teesri DNS ki wajah se DOWN. Wahi kaam jo Session 6 mein bash ke ping loop ne kiya tha, par ab ye asli HTTP jawab dekhta hai. Jab Atithi ki site cloud par aayegi, to bas services.yaml mein URL badalna hai.

## Recap aur Bridge

Recap: JSON, YAML, requests, aur secrets ko code se bahar rakhna. Ab bade kaam ka waqt: officer ko landlord ke office ka phone number dete hain. Python se seedha cloud ko control karna, boto3 ke saath.

---

# EPISODE 3: boto3

## Console ke Pachaas Click

Landlord ke portal par pachaas buildings ko ek ek karke label lagana, ye click ka khel hai. Aur ek bhi chhoot gayi to pata nahi chalega. Landlord ke office ke saare kaam ek API se hote hain, yaani ek phone number se, aur Python ke paas us number ka official phone hai: boto3. Ek loop mein wahi pachaas label lag jaate hain. Dhyaan rahe: is episode ki lab ke liye AWS account chahiye, jo hum agle session mein banayenge, aur ek aisa IAM user jise sirf padhne ka haq ho. Abhi dekh lo, aur account banne ke baad dobara chalana.

## Credentials aur Client

Landlord ke office mein aap bina pehchaan ke phone nahi kar sakte. boto3 pehchaan khud dhoondhta hai, ek tay kram mein: pehle environment variables, phir ~/.aws/credentials file, aur agar script kisi rented building par chal rahi ho to us building ko mila hua IAM role, yaani temporary duty badge. Isliye keys kabhi code mein mat likho aur kabhi git mein mat daalo. Setup ke liye aws configure. Code mein boto3.client("ec2") ek seedha phone hai: jo API call hoti hai wahi ek ek karke map hoti hai. boto3 mein resource naam ka ek aasan style bhi milta hai, par naye features ke saath client hamesha updated rehta hai, isliye hum is course mein client hi use karenge.

## Buildings ki List, Labels aur Pagination

ec2.describe_instances() ka jawab nested aata hai: Reservations ke andar Instances, yaani buildings. Filter lagana ho to Filters=[{"Name": "tag:Env", "Values": ["dev"]}]. Bade accounts mein landlord jawab ek hi baar mein poora nahi deta, wo panne mein deta hai. Isliye paginator use karo: ec2.get_paginator("describe_instances"), aur wo agle panne khud mangwa leta hai. Label lagane ke liye ec2.create_tags(Resources=[id], Tags=[...]). Ek aadat jo bahut bachati hai: pehle sirf padhne wali parchi likho. Aur jo kuch badalti hai, usme pehle DryRun=True try karo, jisme landlord batata hai ki kaam ho jaata, bina kiye.

## Kuch Badalna: Safe Tareeka aur Waiters

Ab padhne ke baad ek kaam jo kuch badalta hai. Maan lo dev ki buildings raat ko kisi kaam ki nahi hain, aur Atithi unhe raat ko band karke bill bachana chahta hai. Pehle sirf unhe chuno jinka label Env dev ho, filter se. Phir band karne se pehle DryRun=True ke saath try karo: ec2.stop_instances(InstanceIds=[iid], DryRun=True). Yahan ek ajeeb baat hai. Agar sab theek hota, to landlord ek error deta hai, ClientError, jiska code DryRunOperation hota hai. Matlab: ye kaam ho jaata. Agar uski jagah UnauthorizedOperation aaye, to aapko uski ijaazat hi nahi hai. Dono ko pakad kar aap bina kuch badle jaan lete ho ki aage badhna theek hai ya nahi. Phir asli call, bina DryRun. Aur kaam turant nahi hota, building ko band hone mein kuch samay lagta hai. Isliye boto3 mein waiters hain: ec2.get_waiter("instance_stopped").wait(InstanceIds=[iid]) jab tak building band na ho jaaye, tab tak parchi ko thama rakhta hai. Ye wahi pattern hai jo aage Terraform aur Ansible ke piche chalta hai: pehle dekho kya badlega, phir badlo, phir tasalli karo.

## Lab: Bina Owner Label ki Buildings

Lab, jab AWS account aur read-only IAM user ho:

Ye sirf padhti hai, kuch badalti nahi. Agar NoRegionError aaye to aws configure mein region daalna bhool gaye. Aur khaali account mein koi building nahi hogi, to Session 8 ke baad dobara chalao. Is tarah ki report landlord ke bill aur zimmedari, dono mein bahut kaam aati hai: pata chalta hai ki kaun si building kiski hai, aur kaun si koi bhool gaya.

## Recap aur Bridge

Recap: boto3 ka client, pehchaan ka kram, pagination aur labels. Ab ek zaroori sawaal: officer ka phone beech mein kat jaaye, ya parchi toot jaaye, to? Agle episode mein bharosemand automation.

---

# EPISODE 4: Bharosemand Automation

## Officer Jo Chup Chaap Fail Hua

Ek officer jo ek hafte tak chup-chaap fail hota raha, usse zyada khatarnaak kuch nahi. Sab ko lagta hai ki sab theek hai, jabki pehle hi din kaam toot gaya tha. Isliye bharosemand automation ki teen aadatein: galti ko pakadna, uska hisaab logbook mein likhna, aur sahi exit code dena.

## try/except aur Retry

try aur except mein sirf wahi galti pakdo jiske liye aapke paas plan ho. Jaise requests.RequestException, ya boto3 ke liye botocore.exceptions.ClientError. Khaali except: mat likho, wo har cheez nigal leta hai, aur aapko pata hi nahi chalta ki kya toota. Network jaisi temporary problems ke liye retry with backoff: pehli baar fail hone par ek second ruko, phir do, phir char, aur kuch koshishon ke baad haar maan lo aur galti ko upar jaane do. Har baar turant dobara try karna phone line ko aur thakata hai. else tab chalta hai jab kuch fail nahi hua, aur finally mein safai hoti hai: file ya connection band karna.

## logging aur Settings

print ki jagah logging lagao. Usme time, level aur message hote hain, aur level se control hota hai ki kitna detail dikhe: logging.info, logging.warning, logging.error. Ek aur baat: logging ka jawab by default error stream mein jaata hai, aur asli output, jaise JSON, normal output mein, isliye dono ko alag karke pipe kiya ja sakta hai. Parchi ki settings code mein hardcode mat karo. argparse se command line ke options lo, jaise --path aur --threshold, aur secret environment variable se. Aise ek hi script alag alag buildings aur alag alag environments mein bina badle chalti hai.

## Shell Command Python se: subprocess

Kabhi kabhi officer ko bash ki koi command chalani padti hai, jaise systemctl is-active nginx. Iske liye subprocess.run. Command ko ek list ke roop mein do, ["systemctl", "is-active", "nginx"], aur capture_output=True, text=True lagao, to jawab text mein aata hai. r.returncode exit code hai, jo zero ka matlab theek, aur r.stdout command ka jawab. Agar chahte ho ki fail hone par galti uthe, to check=True lagao, aur fail hone par CalledProcessError aayega, jise aap pakad sakte ho. Ek zaroori chetavni: shell=True ke saath kisi user se aaya hua text kabhi command mein mat jodo. Koi ; rm -rf jaisi cheez jod sakta hai, aur wo chal jaayegi. List wala tareeka bina shell ke chalta hai, isliye surakshit hai. Isi se bash aur Python ek doosre ke saath chalte hain: Python faisla leta hai, aur zaroorat padne par bash wali command bula leta hai.

## Lab: Disk Report Tool

Lab. Pichhli disk wali script ko asli tool banate hain:

python check.py --path / --threshold 99 pass hona chahiye. python check.py --threshold 1 --json fail hoga, exit code 1, aur JSON alag print hoga. Isse | jq . se pipe karke dekho. Ek dhyaan: aakhri if __name__ == "__main__": wali line zaroori hai. Uske bina from check import is_ok karte hi poori script chal padti hai, aur pytest ke arguments par argparse gir jaata hai; humne yahi dekha. Ab ye tool cron mein lagane layak hai. Cron ise chalaye, exit code dekhe, aur kuch toote to aapko pata chale.

## Apni Parchi ka Test: pytest

Ek aakhri aadat jo bash mein mushkil thi aur Python mein aasaan hai: apni parchi ka test. Tareeka ye hai ki faisle wala hissa ek chhote function mein rakho. Jaise check.py mein def is_ok(pct, limit): return pct < limit, aur baaki parchi usi function ko bulaye. Ab ek alag file test_check.py mein, from check import is_ok ke saath, do chhote test: assert is_ok(50, 90) sach hona chahiye, aur assert not is_ok(95, 90) bhi. pip install pytest karo aur pytest chalao. Do hare nishaan matlab faisle ka tarika kaam kar raha hai. Ye test baad mein Jenkins ke pipeline mein bhi chalenge, aur har badlaav se pehle ek automatic inspection ka kaam karenge. Yahi wo jagah hai jahan officer slip se aage nikal jaata hai.

## Recap aur Bridge

Recap: ab officer sirf kaam nahi karta, bharosemand tareeke se karta hai: galti pakadta hai, logbook likhta hai aur sahi exit code deta hai. Bash slip ka kaam karti hai aur Python dimaag ka. Ab hum building ke andar se nikal kar bahar aate hain, landlord ke campus mein. Agla session AWS ka hai, aur pehli cheez: ek asli building kiraye par lena, yaani EC2.

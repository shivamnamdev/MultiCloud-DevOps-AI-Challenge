# ✍️ 02: SCRIPT — SESSION-33: AIOps and MCP Servers
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S33`
- **Focus:** AIOps (alert noise, correlation, anomaly detection, root-cause hints, incident summaries, ChatOps), data first and AI second, simple anomaly detection (rolling z-score, same hour last week, Prometheus functions, confirmation window), what an LLM is good and bad at in operations, the autonomy ladder and guardrails for self-healing (allow-list, dry run, approval, rate limit, audit log, kill switch), Model Context Protocol (host, client, server, tools, resources, prompts, transports), MCP security (least privilege, read-only first, tool descriptions and logs as untrusted text, tokens, remote authentication), building a read-only DevOps MCP server (namespace allow-list, input validation, output caps, redaction, tests with a fake `kubectl`, a read-only cluster identity), and the course close
- **Builds on:** Session 04 (least privilege), Session 06 (Bash, exit codes), Session 09 (roles), Session 15 (alarm noise), Session 24 and 25 (pods, `logs`, `rollout`, namespaces), Session 26 (inspector, alarm desk, golden signals, runbooks, post-incident review), Session 31 (rollback, deploy log), Session 32 (untrusted text, privacy, fake client, cost)
- **Story position:** Zoom level 3, head office. Raat ki duty par assistant control room mein baithta hai: wo screens padhta hai, alerts ko jodta hai aur pehla jawab deta hai, par chaabiyan duty manager ke paas hi rehti hain. Aur hotel ke tools tak pahunchne ke liye ek service hatch lagti hai, jisse assistant sirf wahi cheezein chhoo sake jo allowed hain.
- **Story words used:** night duty (AIOps), service hatch (MCP server), assistant (AI only), control room, inspector (Prometheus), alarm desk (Alertmanager), wall of screens (Grafana), runbook, duty manager (on-call), key cabinet (credentials), duty badge (role), parking bay (pod), standing order (Deployment), wing (namespace), truck (container), conveyor (pipeline), foreman (Jenkins), outside expert (LLM API), guest (end user), staff (admin)
- **Lab project:** a small anomaly detector that reads the inspector, a restart helper that only suggests unless a duty manager approves, and a read-only service hatch (`atithi-hatch`) with three tools: list pods, read a few log lines, and ask the inspector one question.
- **Cost rule:** the lab runs on the local cluster and the local inspector from Session 26. If an LLM is used to summarize incidents, use a fake client by default and set a provider budget before a real call (Session 32). Never give the hatch a write-capable cluster identity in the lab.
- **Episodes:**
  - Episode 1: Raat ki Duty: AIOps kya hai aur kya nahi
  - Episode 2: Pehle Dekho, Phir Suggest Karo, Phir Karo: Anomaly aur Safe Healing
  - Episode 3: Service Hatch ka Standard: MCP
  - Episode 4: Apni Service Hatch Banao aur Course ka Antim Sabak

---

# 📺 EPISODE 1: Raat ki Duty

### [00:00 – 03:15] Scene 1: Teen Baje, Do Hazaar Alerts
**[VISUAL: A phone buzzing at 3 a.m. A wall of alerts scrolls: rooms-service latency, bookings 5xx, queue lag, disk, memory. Behind them one cause: the records office has stopped answering. A funnel turns two thousand alerts into one incident card.]**

**(Voiceover):**
Raat ke teen baje Atithi ka records office ruk jaata hai. Control room mein do hazaar alerts: har service ki latency, har truck ke errors, queue ka lag. Duty manager ke phone par ghanti nahi, shor. Session 26 ke alarm desk ne grouping aur inhibition se kaafi shor kam kiya tha, par jab system bada ho, tab bhi insaan ko ek ek alert padhna padta hai. AIOps ka matlab hai operations mein data analysis aur AI ka upyog: alerts ko jodna, normal se alag pattern pakadna, aur duty manager ko kam shor aur zyada samajh dena. Ye manager ki jagah lene ke liye nahi, uski madad ke liye hai. Is session mein assistant raat ki duty par baithta hai, par chaabiyan manager ke paas hi rehti hain.

### [03:15 – 05:55] Scene 2: AIOps ke Paanch Kaam
**[VISUAL: Five cards. 1 Correlation: many alerts, one incident. 2 Anomaly detection: unusual for this hour. 3 Root-cause hints: what broke first, what was deployed. 4 Summaries and ChatOps: "what happened in the last hour?". 5 Automatic fixes (faded, with a warning sign).]**

**(Voiceover):**
AIOps ke paanch kaam. Ek, correlation: ek hi kaaran ke kai alerts ek incident mein. Do, anomaly detection: wo pattern jo us samay ke liye normal nahi, jahan fixed threshold kamzor padte hain. Teen, root-cause ke ishare: kaun si service pehle bigdi, aur us se thodi der pehle kya deploy hua, jaise Session 31 ka deploy log. Chaar, summary aur ChatOps: "pichhle ek ghante mein kya hua?" ka saaf jawab. Aur paanch, automatic fix, jo sabse risky hai, aur jisse hum guardrails ke saath dekhenge. Ek niyam: jitna zyada kaam badle, utna zyada bharosa chahiye, isliye pehle teen kaam aasaan hain aur paanchva sabse mushkil.

### [05:55 – 08:20] Scene 3: Pehle Data, Phir AI
**[VISUAL: A pyramid. Base: reliable meters, logs and traces. Next: labels, ownership and service names. Next: clean alerts, SLOs, runbooks. Top: AI on top, small. A box: "an LLM reads what you give it; give it nothing and it will guess".]**

**(Voiceover):**
Ek sacchai: AIOps ki neev achhi observability hai. Agar saaf meters, logs, labels aur service ke maalik ka naam nahi, to AI bhi andhera hi dikhayega, aur andhere mein LLM aksar andaza lagata hai, jo sunne mein sahi lagta hai par galat hota hai. Isliye is course mein pehle control room, Session 26, aaya, aur AIOps ab. Pehle labels aur ownership theek karo, SLO tay karo, alerts saaf karo, runbook likho. Phir assistant ke paas padhne ke liye kuch bharosemand hoga. Aur wahi runbook assistant ko batayega ki is alert par kya karna hai.

### [08:20 – 11:05] Scene 4: LLM Kahan Achha, Kahan Nahi
**[VISUAL: Two columns. Good: summarize a log excerpt, explain an unfamiliar error, draft a post-incident review from a timeline, translate PromQL, suggest what to check next. Bad: do exact arithmetic on metrics, decide the severity alone, run commands unsupervised, remember what it was never shown. A note: "always show the source lines it used".]**

**(Voiceover):**
LLM kahan achha hai: log ke tukde ka saransh, anjaan error ka matlab, timeline se post-incident review ka pehla draft, PromQL samjhana, aur "agla kya dekhna chahiye" ka suggestion. Kahan nahi: metrics par sahi hisaab, akele severity tay karna, bina nigrani ke commands chalana, aur wo cheezein jo use dikhayi hi nahi gayi. Hisaab ke liye code use karo, jaise agle episode ka z-score. Aur ek niyam jo bahut kaam aata hai: assistant jab kuch kahe, to saath mein wo lines bhi dikhaye jin par uska andaza tika hai, taaki duty manager ek nazar mein jaanch sake. Bina saboot ka jawab, chahe kitna bhi saaf bole, sirf ek raay hai.

### [11:05 – 13:50] Scene 5: Lab: Do Hazaar Mein Se Bees
**[VISUAL: A sheet with twenty sample alerts from a made-up incident: times, service, alert name, and a dependency map. The learner groups them by time window and dependency, finds the first alert, and strikes out noise. A second column: "what runbook line applies".]**

**(Voiceover):**
Lab (kaagaz par): ek kalpanik incident ke bees alerts: records office ki latency, bookings ke 5xx, queue lag, frontend errors, aur do disk ke jo pehle se chal rahe the. Unhe time aur dependency se group karo. Pehla alert kaun sa tha? Kaun sa sirf shor tha? Root cause kya ho sakta hai, aur kya saboot hai? Phir har group ke saamne likho ki Session 26 ke runbook ki kaun si line lagegi. Ye haath se kiya hua kaam hi samjhata hai ki correlation ka asli maqsad kya hai: manager ko ek incident dikhana, bees alert nahi. Agle episode mein isi kaam ka ek chhota hissa code mein karte hain.

### [13:50 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "AIOps = less noise, more insight · correlation, anomaly, hints, summaries · data first · LLM for words, code for math · show the evidence".]**

**(Voiceover):**
Recap: AIOps kya hai, uski neev, aur LLM ki jagah. Ab hands-on: anomaly detection aur surakshit healing.

---

# 📺 EPISODE 2: Pehle Dekho, Phir Suggest Karo, Phir Karo

### [00:00 – 01:25] Scene 1: Threshold Kamzor Kyun
**[VISUAL: A latency graph with a daily wave: high every evening, low at night. A fixed line at one level alarms every evening and misses a small, strange bump at 3 a.m. that is abnormal for that hour.]**

**(Voiceover):**
Fixed threshold, jaise "CPU 80% se upar", har jagah sahi nahi. Shaam ke peak mein 80% normal ho sakta hai, aur raat ke teen baje 40% bhi ajeeb. Booking website ka traffic roz ek lahar ki tarah chalta hai, aur weekend par alag. Anomaly detection ye dekhta hai ki value us samay ke liye normal se alag hai ya nahi. Aur ek chhota sa statistics bhi aksar kaafi madad karta hai, isliye bade ML model se pehle usi se shuru karo.

### [01:25 – 03:40] Scene 2: Seedha Tareeka: z-score aur Pichhle Hafte ka Ghanta
**[VISUAL: A line with a band of the rolling mean plus and minus three standard deviations. A point outside the band is circled. A second chart compares today's 8 p.m. value with the same hour on previous weeks. Notes: "confirm over several points", "flat series need care".]**

**(Voiceover):**
Sabse saral tareeka: rolling average aur standard deviation. Agar naya value average se teen standard deviation se zyada door ho, to anomaly. Isko z-score kehte hain. Roz ki lahar wale data ke liye aur behtar: aaj ke shaam aath baje ko pichhle hafte ke usi ghante se milao. Prometheus ke andar bhi `stddev_over_time` aur `avg_over_time` hain, aur `predict_linear` aage ka raasta dikhata hai, jaise disk kab bharegi. Teen jaal. Ek, ek hi point par alarm mat bajao: kai points tak anomaly rahe tab. Do, jo series bilkul seedhi ho, usme standard deviation sifar hota hai aur z-score fat jaata hai, isliye wahan alag rule. Teen, naye service par detector chup rahe, kyunki history kam hai. Bade ML model tabhi, jab ye saral tareeke kaafi na hon.

### [03:40 – 05:45] Scene 3: Autonomy ki Seedhi
**[VISUAL: A ladder with four steps. 1 Observe and report. 2 Suggest a fix with evidence. 3 Fix after a duty manager's approval. 4 Fix alone, only for low-risk, reversible actions. A red zone at the top: "never alone: delete data, scale a database down, change security rules, spend money".]**

**(Voiceover):**
Automatic fix ek seedhi par chadhta hai. Pehla paaydaan: sirf dekhna aur batana. Doosra: fix suggest karna, saboot ke saath. Teesra: duty manager ki manzoori ke baad fix. Aur sabse upar: sirf kam khatre aur ulte ho sakne wale kaam khud karna, jaise ek atki hui parking bay ko restart karna. Bahut si teams doosre ya teesre paaydaan par hi rukti hain, aur ye bilkul theek hai. Upar ke lal hisse mein kuch kaam kabhi akele nahi: data delete karna, database chhota karna, security ke niyam badalna, aur wo kaam jisme paisa lagta ho. Seedhi ek ek paaydaan chadho, aur har paaydaan par pehle kuch hafte sirf record karo ki assistant kya karta, aur manager kya karta.

### [05:45 – 08:00] Scene 4: Guardrails
**[VISUAL: Six guards around an action box. Allow-list of exact actions. Dry run first. Approval flag. Rate limit (at most one restart per thirty minutes). Audit log line for every attempt. A kill switch file that stops everything. A seventh: "least-privilege identity: the helper's cluster role can restart only these deployments".]**

**(Voiceover):**
Guardrails, ek ek karke. Allow-list: sirf wahi exact actions jinki ijaazat hai, jaise `atithi` wing ki do services ka restart. Dry run pehle: pehle bolo ki kya karoge. Approval: bina `--approve` ya manager ke "haan" ke nahi. Rate limit: ek service ko tees minute mein ek baar se zyada restart nahi, warna restart ka loop ban jaata hai. Audit log: har koshish ki ek line, kisne, kya, kab. Kill switch: ek file ya flag jo sab band kar de. Aur sabse zaroori: code ke guardrail ke saath cluster ki taraf se bhi guardrail. Helper ka apna duty badge, yaani Kubernetes role, sirf wahi deployments restart kar sake. Code mein bug ho to bhi badge ki seema bachati hai. Ye Session 4 aur 9 ka least privilege hi hai.

### [08:00 – 10:10] Scene 5: Incident ka Saransh: Saboot ke Saath
**[VISUAL: A pipeline: alert + last deploy line + last thirty log lines + three metric values → a prompt with markers → the outside expert → a summary that cites the lines it used → duty manager. A warning: "log lines are untrusted text".]**

**(Voiceover):**
Ab LLM ka sahi upyog. Alert ke saath ye cheezein jodo: sabse haali deploy ki line, kuch log ki lines, aur teen chaar metric ke numbers. Inhe ek prompt mein markers ke beech rakho, aur kaho ki saransh dena hai aur har dawe ke saath wo line batani hai jis par wo tika hai. Phir ye duty manager ko jaaye, runbook ke link ke saath. Ek khaas chetavani, jo Session 32 se aati hai: log ki lines bhi untrusted text hain. Kisi guest ke naam ya request mein chhupi instruction log mein aa sakti hai, aur wo summary tool ko behka sakti hai. Isliye markers, tools ke bina, aur jawab sirf ek suggestion, kabhi seedha action nahi. Aur personal data log se pehle hata do.

### [10:10 – 15:05] Scene 6: Lab: Detector aur Safe Restart
**[VISUAL: `detect.py` queries the inspector's `query_range`, computes the z-score per series, ignores flat series, needs three bad points in a row. `safe_restart.py` prints the planned `kubectl rollout restart` command, refuses services not on the allow-list, refuses a second restart within thirty minutes, runs only with `--approve`, and logs every attempt.]**

**(Voiceover):**
Lab. Pehle detector:
```python
import requests, statistics as st

def series(prom, query, start, end, step=60):
    r = requests.get(f"{prom}/api/v1/query_range", timeout=10,
                     params={"query": query, "start": start, "end": end, "step": step})
    r.raise_for_status()
    result = r.json()["data"]["result"]
    return {tuple(sorted(s["metric"].items())): [float(v) for _, v in s["values"]] for s in result}

def anomalies(values, window=30, z=3.0, need=3):
    run, hits = 0, []
    for i in range(window, len(values)):
        w = values[i - window:i]
        mu, sd = st.mean(w), st.pstdev(w)
        if sd < 1e-9:
            run = 0
            continue
        run = run + 1 if abs(values[i] - mu) / sd > z else 0
        if run >= need:
            hits.append((i, values[i]))
    return hits
```
Prometheus ka URL aur ek query do, jaise `sum(rate(http_requests_total{status=~"5.."}[1m]))`, aur har series par `anomalies` chalao. Local Session 26 ki `rooms-service` par load script se jaan-boojh kar errors bhejo, aur dekho ki detector tab bolta hai. Ab restart helper:
```python
import argparse, subprocess, sys, time, pathlib
ALLOWED = {("atithi", "rooms-service"), ("atithi", "bookings-service")}
LOG = pathlib.Path("aiops-actions.log")

ap = argparse.ArgumentParser()
ap.add_argument("namespace"); ap.add_argument("deployment")
ap.add_argument("--approve", action="store_true")
a = ap.parse_args()

if (a.namespace, a.deployment) not in ALLOWED:
    sys.exit("not on the allow-list")
if pathlib.Path("KILL").exists():
    sys.exit("kill switch is on")
recent = [l for l in LOG.read_text().splitlines()] if LOG.exists() else []
now = time.time()
for l in recent:
    t, ns, dep, outcome = l.split(",")
    if (ns, dep) == (a.namespace, a.deployment) and outcome == "done" and now - float(t) < 1800:
        sys.exit("restarted recently, ask a human")
cmd = ["kubectl", "rollout", "restart", f"deployment/{a.deployment}", "-n", a.namespace]
print("PLAN:", " ".join(cmd))
if not a.approve:
    sys.exit("dry run only, add --approve")
subprocess.run(cmd, check=True, timeout=30)
LOG.open("a").write(f"{now},{a.namespace},{a.deployment},done\n")
```
Chalao bina `--approve` ke: sirf plan. Allow-list ke bahar ki service do: mana. Do baar jaldi jaldi `--approve`: doosri baar mana. Ek `KILL` file banao aur dekho ki sab ruk jaata hai.

### [15:05 – 15:35] Scene 7: Recap aur Bridge
**[VISUAL: A card: "z-score plus same-hour compare · confirm over several points · ladder: observe, suggest, approve, small auto · allow-list, dry run, rate limit, audit, kill switch, least-privilege role · summaries with evidence".]**

**(Voiceover):**
Recap: saral anomaly detection aur surakshit healing. Ab ek naya standard jo assistant ko hotel ke tools se jodta hai: service hatch, yaani MCP.

---

# 📺 EPISODE 3: Service Hatch ka Standard

### [00:00 – 03:00] Scene 1: Har Assistant, Har Tool ke Liye Alag Wiring?
**[VISUAL: Three AI apps and five tools joined by a tangle of fifteen custom wires. Then a standard hatch in the middle: three plugs on one side, five on the other, eight connections.]**

**(Voiceover):**
Maan lo Atithi mein teen alag AI apps hain: ek IDE mein, ek chat mein, ek control room ke liye. Aur paanch tools: Git, Kubernetes, Prometheus, ticketing aur docs. Har app ko har tool se alag jodna, pandrah alag taar. Model Context Protocol, yaani MCP, ek standard hai jisse AI apps tools aur data se ek hi tareeke se jud sakti hain. Isse pandrah taar ki jagah aath: har app ek taraf, har tool doosri taraf. Jaise USB: ek port, kai device. Hamari story mein ye service hatch hai: ek saaf khidki jisse assistant hotel ke tools ko chhoota hai, aur har tool apni hatch par apne niyam tay karta hai.

### [03:00 – 06:20] Scene 2: Hatch ke Hisse
**[VISUAL: Host (an AI app) containing an MCP client. The client connects to one or more MCP servers. A server exposes three kinds of things: tools (actions), resources (data to read), prompts (ready templates). Two transports: stdio for local, HTTP for remote.]**

**(Voiceover):**
MCP mein teen bhumikayein. Host wo AI app hai jisse aap baat karte ho. Host ke andar MCP client hota hai, jo server se jud jaata hai. MCP server wo program hai jo capabilities deta hai, yaani hamari service hatch. Server teen cheezein de sakta hai: tools, yaani kaam jaise "pods ki list do"; resources, yaani padhne layak data jaise "ek log ka snapshot"; aur prompts, yaani ready templates. Transport ke do tareeke: local ke liye stdio, jahan host server ko apni hi machine par chalata hai, aur remote ke liye HTTP, jahan server door ki machine par hai aur wahan authentication zaroori hai. Assistant tool chunta hai, par host ke control mein, aur host aksar insaan se manzoori maangta hai.

### [06:20 – 09:25] Scene 3: Hatch ki Suraksha
**[VISUAL: A list of dangers. An unknown server run on your machine. A tool description that contains hidden instructions. A tool returning log lines that contain hidden instructions. A token with write access. A remote hatch with no login. A tool that can run any shell command.]**

**(Voiceover):**
Pehla: koi anjaan server apne host se jodna, matlab anjaan program apni machine par chalana. Doosra: tool ke description mein ya uske jawab mein chhupi instruction ho sakti hai, jise model padhta hai, isliye server ka source dekho aur sirf bharose wale server jodo. Teesra: tool ke jawab, jaise log, bhi untrusted text hain, wahi prompt injection jo Session 32 mein dekha. Chautha: token ka daayra, yaani wahi least privilege: shuruat read-only se, aur cluster ki taraf se bhi read-only badge. Paanchva: remote hatch par login zaroori hai. Chhatha: koi bhi tool jo "koi bhi shell command chalao" kahe, wo hatch nahi, khuli khidki hai. Tool chhote hon, aur apne input ko khud jaanchein.

### [09:25 – 11:50] Scene 4: Hatch Kaun Si Cheezein Kholega
**[VISUAL: A table with columns tool, inputs, returns, risk, and what stops misuse. `list_pods(namespace)`, `get_pod_logs(namespace, pod, tail)`, `query_prometheus(promql)`. All risk "read". A fourth row crossed out: `restart_deployment`, "not in the first version".]**

**(Voiceover):**
Hatch ka design pehle kaagaz par. Teen tools. `list_pods(namespace)`: allowed namespaces mein pods aur unki halat. `get_pod_logs(namespace, pod, tail)`: kuch aakhri lines, jisme tail ki seema ho aur secrets hata diye gaye hon. `query_prometheus(promql)`: inspector se ek sawaal, jisme URL fixed ho, samay ki seema ho aur jawab chhota ho. Teeno ke saamne risk "sirf padhna". Chautha tool, restart, abhi nahi: wo episode 2 ka alag, manzoori wala helper hai, aur use hatch se jodna ek alag, soch-samajh kar liya hua faisla hoga. Pehle hatch se sirf dekhna sikho.

### [11:50 – 13:50] Scene 5: Lab: Design ko Test Karo
**[VISUAL: A worksheet. For each tool the learner writes three abuse cases: a wrong wing, an input with a semicolon, a very large output. Then a note on what the code will do for each one.]**

**(Voiceover):**
Lab (design): har tool ke liye teen galat istemaal likho. Galat wing mein pods maangna. Pod ke naam mein semicolon aur command daalna. Bahut bada output maangna, jaise ek lakh log lines ya ek bahut bhaari PromQL. Phir har ek ke saamne likho ki server kya karega: mana karega, input saaf karega, ya output kaat dega. Agle episode mein hum yahi code mein likhenge, aur jo likha hai wo test bhi karenge.

### [13:50 – 14:20] Scene 6: Recap aur Bridge
**[VISUAL: A card: "host + client + server · tools, resources, prompts · stdio local, HTTP remote with login · untrusted server, description and output · read-only first · small tools, validated inputs".]**

**(Voiceover):**
Recap: MCP ka idea, uske hisse, aur uski suraksha. Ab apni service hatch banate hain.

---

# 📺 EPISODE 4: Apni Service Hatch Banao

### [00:00 – 01:10] Scene 1: Chat Mein Pucho, Control Room Jawab De
**[VISUAL: A chat window. "Why is rooms-service restarting?" The assistant calls `list_pods`, then `get_pod_logs`, then `query_prometheus`, and answers: "memory limit hit, OOMKilled, here are the lines". It adds: "I can't restart anything; the duty manager decides."]**

**(Voiceover):**
Soch ke dekho: duty manager chat mein poochta hai "rooms-service baar baar restart kyun ho rahi hai?" Assistant `list_pods` chalata hai, phir `get_pod_logs`, phir ek `query_prometheus`, aur jawab deta hai ki memory limit par OOMKilled ho raha hai, ye rahi wo lines, aur ye rahi memory ki query. Saath mein saaf kehta hai ki restart wo nahi kar sakta, kyunki hatch mein wo tool hai hi nahi. Faisla manager ka. Is episode mein hum aisi hatch banate hain.

### [01:10 – 04:10] Scene 2: Hatch ka Code
**[VISUAL: A Python file using the official MCP Python SDK's `FastMCP`. A `kubectl` helper using an argument list and a timeout. A name check by regex. `list_pods` with a namespace allow-list. Notes: "no shell", "errors trimmed", "descriptions short".]**

**(Voiceover):**
Official Python SDK ke saath hatch chhoti hoti hai. Ek dhyaan ki baat: version 1 mein `from mcp.server.fastmcp import FastMCP` hai, aur version 2 mein naam `MCPServer` ho gaya. Hum version 1 likhte hain, aur lab mein `pip install "mcp[cli]<2"` lagayenge. Version 2 par jaana ho to bas ek import aur ek naam badlo.
```python
import json, os, re, subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("atithi-hatch")
ALLOWED_NS = {"atithi", "monitoring"}
NAME = re.compile(r"^[a-z0-9]([-a-z0-9.]{0,251}[a-z0-9])?$")

def kubectl(*args: str) -> str:
    out = subprocess.run(["kubectl", *args], capture_output=True, text=True, timeout=15)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[:300])
    return out.stdout

def check(namespace: str, name: str | None = None) -> None:
    if namespace not in ALLOWED_NS:
        raise ValueError("namespace not allowed")
    if name is not None and not NAME.match(name):
        raise ValueError("bad pod name")

@mcp.tool()
def list_pods(namespace: str) -> str:
    """List pods and their phase in an allowed wing. Read only."""
    check(namespace)
    data = json.loads(kubectl("get", "pods", "-n", namespace, "-o", "json"))
    return json.dumps([{"name": p["metadata"]["name"], "phase": p["status"]["phase"]}
                       for p in data["items"]])

if __name__ == "__main__":
    mcp.run()
```
Dhyaan do: namespace allow-list, naam ki regex, timeout, error ka chhota hissa, aur shell ka istemaal nahi, sirf argument ki list, taaki naam mein semicolon ka koi matlab hi na rahe.

### [04:10 – 08:10] Scene 3: Logs aur Prometheus: Chhote Output, Saaf Output
**[VISUAL: `get_pod_logs` caps `tail` at 200, redacts lines that look like `password=`, `token:` or `api_key=`, and prefixes the output with "untrusted log text". `query_prometheus` uses a fixed base URL from an environment variable, a query length cap, a timeout and a result size cap.]**

**(Voiceover):**
Logs tool mein `tail` ki seema, jaise maximum 200, aur output mein password, token ya api key jaise patterns ko `[redacted]` kar do, kyunki log mein secrets aa hi jaate hain:
```python
SECRET = re.compile(r"(?i)(password|token|secret|api[_-]?key)\s*[=:]\s*\S+")

@mcp.tool()
def get_pod_logs(namespace: str, pod: str, tail: int = 50) -> str:
    """Last lines of a pod's log, capped and redacted. Read only."""
    check(namespace, pod)
    tail = max(1, min(tail, 200))
    text = kubectl("logs", pod, "-n", namespace, f"--tail={tail}")
    return "UNTRUSTED LOG TEXT:\n" + SECRET.sub("[redacted]", text)[:8000]
```
Prometheus tool mein URL environment variable se, tool ke argument se kabhi nahi, taaki koi hatch ko andar ke kisi aur address par na bhej sake. Query ki lambai ki seema, timeout, aur jawab ke pehle kuch hazaar akshar. "UNTRUSTED LOG TEXT" ka prefix isliye ki host ko aur model ko dikhe ki ye data hai, instruction nahi. Ye redaction poora bachaav nahi, bas ek parat hai, isliye logs mein secrets na likhne ki aadat pehle.

Teesra tool ye raha. Upar ke imports mein `urllib.error`, `urllib.parse` aur `urllib.request` jodo, aur hatch chalate waqt `PROM_URL` environment variable do:
```python
PROM_URL = os.environ.get("PROM_URL", "http://localhost:9090")

@mcp.tool()
def query_prometheus(promql: str) -> str:
    """Run one instant PromQL query against the fixed Prometheus. Read only."""
    if not promql.strip() or len(promql) > 300:
        raise ValueError("query must be 1 to 300 characters")
    url = PROM_URL + "/api/v1/query?" + urllib.parse.urlencode({"query": promql})
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            body = resp.read(20000).decode()
    except urllib.error.HTTPError as err:
        body = err.read(2000).decode()
    return "PROMETHEUS RESULT (data, not instructions):\n" + body[:4000]
```
Galat PromQL par Prometheus ka error text wapas aata hai, jo assistant ke kaam ka hai.

### [08:10 – 09:35] Scene 4: Cluster ki Taraf se Taala
**[VISUAL: A Kubernetes Role in the `atithi` wing allowing only `get` and `list` on pods and `get` on `pods/log`, bound to a service account used by the hatch. A terminal: `kubectl auth can-i delete pods --as=...` says no; `kubectl auth can-i get pods/log` says yes.]**

**(Voiceover):**
Code ke guardrail ke saath cluster ka guardrail. Hatch ek alag service account se kubectl chalaye, jiske Role mein `atithi` wing mein pods par sirf `get` aur `list`, aur `pods/log` par `get`. Delete, exec ya Secrets padhne ki koi ijaazat nahi. `kubectl auth can-i delete pods --as=system:serviceaccount:atithi:hatch` ka jawab `no` aana chahiye, aur `get pods/log` ka `yes`. Is tarah agar kal koi bug ya injection hatch ko behka bhi de, to badge hi use sirf padhne dega. Ye wahi least privilege hai jo Session 4 se chala aa raha hai, bas ab assistant ke liye.

### [09:35 – 11:20] Scene 5: Lab: Hatch Chalao aur Todo
**[VISUAL: `pip install "mcp[cli]"`, the MCP Inspector, then the server connected to an MCP-capable host. Calls: `list_pods("atithi")` works; `list_pods("kube-system")` is refused; `get_pod_logs("atithi", "x; rm -rf /")` is refused; a huge `tail` is capped. Tests with a fake `kubectl` function.]**

**(Voiceover):**
Lab: SDK install karo: `pip install "mcp[cli]<2"`. Iske liye Python 3.10 ya naya chahiye: `python3.12 -m venv .venv` jaisa naya interpreter lo, ya `python:3.12-slim` container use karo. `fastmcp` naam ka alag package bhi hai, jiska import alag hai. MCP Inspector ya kisi MCP-capable host mein server jodo. `list_pods("atithi")`: pods dikhenge. `list_pods("kube-system")`: mana, kyunki wo allow-list mein nahi. `get_pod_logs("atithi", "x; rm -rf /")`: mana, naam ki jaanch se. `tail=100000` do: 200 par kat jaata hai. Phir `kubectl` ki jagah ek nakli function lagakar unit tests likho. Aur ek log mein jaan-boojh kar `password=abc123` rakho, aur dekho ki `[redacted]` aata hai. Host ki config mein command `python hatch.py`, aur hatch ko wahi service account jo pichhle scene mein banaya.

### [11:20 – 13:10] Scene 6: Hatch aur Helper Saath Mein
**[VISUAL: The control-room loop. Detector flags an anomaly → an incident card with evidence → the assistant uses the hatch to read pods, logs and metrics → proposes "restart rooms-service" → the duty manager runs the approved helper or declines → an audit line and a post-incident review draft.]**

**(Voiceover):**
Ab dono ko jodo, par ek ek kadam. Detector anomaly pakadta hai. Assistant hatch se pods, logs aur metrics padhta hai, aur saboot ke saath ek incident card banata hai, jisme runbook ka link hai. Wo suggest karta hai: "rooms-service ko restart karo". Duty manager helper ko `--approve` ke saath chalata hai, ya mana kar deta hai. Har kadam ki ek line audit log mein. Subah assistant post-incident review ka pehla draft likhta hai, jise manager padhta aur sudharta hai. Dekho kitni baar insaan beech mein hai: faisle ke waqt. Jab kuch hafte ke baad bharosa bane, tab hi kam khatre wale kaam, jaise ek stuck pod ka restart, autonomy ki seedhi par ek paaydaan upar jaa sakte hain, aur sirf wahi.

### [13:10 – 15:30] Scene 7: Course ka Antim Sabak
**[VISUAL: The Build, Ship, Fix arrow with the full course map behind it: Linux, AWS, Git, Jenkins, Docker, Kubernetes, Prometheus, Terraform, Ansible, Azure, AI. Then the Atithi campus from the first session, now lit up end to end. A pilot beside an autopilot panel.]**

**(Voiceover):**
Aapne ek khaali building se shuru kiya. Linux se uske andar ke staff aur darwaze seekhe. AWS se campus. Git aur Jenkins se head office. Docker aur Kubernetes se trucks aur operations command. Prometheus se control room. Terraform aur Ansible se master plan aur setup crew. Azure se doosra landlord. AI se assistant, outside expert aur trained brain. Ye sab ek hi kahani hai: Build, Ship, Fix. Aur assistant ek tez autopilot hai, par pilot kaun hai? Aap. Draft assistant ka, jaanch aapki. Guardrail pehle, autonomy baad mein. Ab agla kadam aapka hai. Apna `atithi-booking`, `atithi-rooms` aur capstone ki conveyor ek GitHub repo mein rakho, README mein guest ki journey ke aath kadam likho, ek chhota architecture diagram banao, aur ek kharab release ko rollback hote hue record karo. Phir jab koi poochhe ki aap kya karte ho, to aap ek asli kahani, aur ek chalti hui conveyor dikha sakte ho. Isi se aap engineer banoge.

---

# 📎 Student handout: Session 33 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| AIOps | Kam shor, zyada samajh: correlation, anomaly, hints, summaries |
| Neev | Pehle meters, labels, ownership, runbooks; phir AI |
| LLM | Shabdon ke liye (summary, explain); hisaab code se; saboot ki lines dikhao |
| Anomaly | Rolling z-score ya pichhle hafte ka same ghanta; kai points tak; flat series alag |
| Prometheus | `stddev_over_time`, `avg_over_time`, `predict_linear` (disk bharne ka samay) |
| Autonomy seedhi | Observe → suggest → approve → chhota, ulta ho sakne wala auto |
| Kabhi akele nahi | Data delete, database chhota, security niyam, paisa |
| Guardrails | Allow-list, dry run, approve, rate limit, audit log, kill switch, least-privilege role |
| Incident saransh | Alert + deploy line + log lines + numbers; markers; saboot; log = untrusted |
| MCP | Host + client + server; tools, resources, prompts; stdio (local), HTTP (remote, login) |
| Hatch ki suraksha | Bharose ka server; description aur output untrusted; read-only; chhote tools |
| Input | Namespace allow-list, naam ki regex, argument list (shell nahi), timeout |
| Output | `tail` cap, size cap, secrets redact, "UNTRUSTED" prefix |
| Cluster badge | Role: sirf `get`, `list`, `pods/log`; `kubectl auth can-i` se jaanch |
| Test | Nakli `kubectl`; MCP Inspector; abuse cases |
| Antim sabak | Build, Ship, Fix; draft AI ka, jaanch aapki; guardrail pehle |

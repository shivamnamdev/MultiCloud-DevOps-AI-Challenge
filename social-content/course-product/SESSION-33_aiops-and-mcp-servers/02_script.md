# ✍️ 02: SCRIPT — SESSION-33: AIOps & MCP Servers
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + desi analogy + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording).*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S33`
- **Focus:** AIOps concepts, anomaly detection on metrics, safe self-remediation, Model Context Protocol (MCP) basics, building a read-only DevOps MCP server, guardrails
- **Episodes:**
  - Episode 1: AIOps kya hai: Alert Noise se Insight Tak
  - Episode 2: Anomaly Detection aur Safe Self-Healing
  - Episode 3: MCP: AI ko Tools se Jodne ka Standard
  - Episode 4: Apna DevOps MCP Server aur Course ka Antim Sabak

---

# 📺 EPISODE 1: AIOps kya hai?

### [00:00 – 01:15] Scene 1: 2000 Alerts, 1 Asli Problem
**[VISUAL: A wall of alerts scrolling: CPU, memory, latency, 5xx, disk. Behind them one root cause: a database failing. A funnel groups 2000 alerts into 1 incident.]**

**(Voiceover):**
Ek database mara aur aapko do hazaar alerts mile: har service ke latency aur error ke. Insaan ke liye asli problem dhoondhna mushkil. AIOps ka matlab hai operations mein AI aur data analysis ka upyog: alerts ko group karna, patterns pehchanna, aur insaan ko kam shor aur zyada samajh dena. Ye insaan ko replace karne ke liye nahi, uski madad ke liye hai.

### [01:15 – 05:00] Scene 2: AIOps ke Upyog
**[VISUAL: Four use cases with icons: Alert correlation/noise reduction, Anomaly detection, Root-cause hints, Summaries/ChatOps. A fifth faded icon: Automated remediation (with a caution).]**

**(Voiceover):**
AIOps ke upyog. Ek, alert correlation: ek hi kaaran ke kai alerts ek incident mein. Do, anomaly detection: normal se alag pattern pakadna, jahan fixed threshold kamzor padte hain. Teen, root-cause ke ishare: kaun si service pehle bigdi, kya deploy hua tha. Chaar, summaries aur ChatOps: LLM se incident ka saransh ya logs ka explanation. Aur paanchva, automatic remediation, jo sabse risky hai, aur jisse hum guardrails ke saath dekhenge.

### [05:00 – 08:30] Scene 3: Data pehle, AI baad mein
**[VISUAL: A pyramid: Reliable telemetry (metrics/logs/traces) → good tagging and service ownership → clean alerts and SLOs → AI/ML on top. The top is small.]**

**(Voiceover):**
Ek sach: AIOps ki neev achhi observability hai. Agar aapke paas saaf metrics, logs, traces, aur service ownership ki jaankari nahi, to AI bhi andhera hi dikhayega. Pehle labels aur tags theek karo, SLOs tay karo, aur alerts saaf karo. Uske baad AI kaam ko tez karta hai. Isliye is course mein pehle monitoring seekhi, aur AIOps ab aata hai. AI ka wada tab sahi hota hai jab data bharosemand ho.

### [08:30 – 11:30] Scene 4: Lab: Alert Noise Count Karo
**[VISUAL: A table of 20 sample alerts from a fake incident with fields: time, service, alert name. The learner groups them by time window and dependency to find the root cause.]**

**(Voiceover):**
Lab (paper): ek kalpanik incident ke 20 alerts diye gaye hain, jinme database latency, API 5xx, queue lag aur frontend errors hain. Unhe time aur dependency ke hisaab se group karo, aur batao ki root cause kya ho sakta hai. Phir sochkar likho ki kaun sa alert sirf shor tha. Ye manual exercise AIOps ke correlation ka asli maqsad samjha deta hai. Agle episode mein hum ek chhota code mein ye wahi kaam karte hain.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "AIOps = less noise, more insight · correlation · anomaly · RCA hints · needs good data".]**

**(Voiceover):**
Recap: AIOps ka matlab aur uski neev. Ab hands-on: anomaly detection aur safe self-healing.

---

# 📺 EPISODE 2: Anomaly Detection aur Safe Self-Healing

### [00:00 – 01:15] Scene 1: Threshold Kamzor Kyun
**[VISUAL: A latency graph with a daily wave pattern. A fixed threshold alarms every evening peak (false positives) but misses a night-time spike that is abnormal for that hour.]**

**(Voiceover):**
Fixed threshold, jaise "CPU 80% se upar", har jagah sahi nahi. Din ke peak mein 80% normal ho sakta hai, aur raat ke 3 baje 40% bhi ajeeb. Anomaly detection ye dekhta hai ki value us samay ke liye normal se alag hai ya nahi. Chhota sa statistics bhi kaafi madad karta hai.

### [01:15 – 05:00] Scene 2: Simple Anomaly Detection
**[VISUAL: A series with a rolling mean ± 3 standard deviations band. A point outside the band is highlighted. Next, seasonality: compare with the same hour last week.]**

**(Voiceover):**
Sabse saral tareeka: rolling average aur standard deviation, yaani z-score. Agar naya value average se teen standard deviations se zyada door ho, to anomaly. Daily pattern wale data ke liye pichle hafte ke usi ghante se compare karo. Prometheus mein bhi `predict_linear` aur `stddev_over_time` jaise functions hain. Zyada complex ML models tabhi lagao jab simple tareeke kaafi na ho. Sabse badi dikkat false positives hain, isliye alert se pehle ek confirmation window rakho.

### [05:00 – 08:30] Scene 3: Remediation ke Guardrails
**[VISUAL: A ladder of autonomy: 1 Observe & report → 2 Suggest a fix → 3 Fix with human approval → 4 Auto-fix for low-risk, reversible actions only. Guardrails: allow-list, dry-run, rate limits, audit log, kill switch.]**

**(Voiceover):**
Automatic fix ek seedhi par chadhta hai. Pehle sirf dekhna aur batana. Phir fix suggest karna. Phir insaan ki manzoori ke saath fix. Aur sabse upar sirf kam khatre aur ulte ho sakne wale kaam khud karna, jaise ek crashed pod ko restart karna. Guardrails: sirf allow-list ke actions, dry-run pehle, rate limit taaki restart ka loop na bane, har action ka audit log, aur ek kill switch. Production database ko delete ya scale-down jaise kaam kabhi auto nahi hone chahiye.

### [08:30 – 11:30] Scene 4: Lab: Anomaly Detector + Safe Restart
**[VISUAL: A Python script fetching a metric from the Prometheus HTTP API (`/api/v1/query_range`), computing a rolling z-score, and printing anomalies. Another script proposing `kubectl rollout restart deployment/catalog` in dry-run mode and requiring `--approve` to run.]**

**(Voiceover):**
Lab:
```python
import requests, statistics as st

def series(prom, query, start, end, step="60"):
    r = requests.get(f"{prom}/api/v1/query_range", timeout=10,
                     params={"query": query, "start": start, "end": end, "step": step})
    r.raise_for_status()
    return [float(v) for _, v in r.json()["data"]["result"][0]["values"]]

def anomalies(values, window=30, z=3.0):
    out = []
    for i in range(window, len(values)):
        w = values[i-window:i]
        mu, sd = st.mean(w), st.pstdev(w) or 1e-9
        if abs(values[i] - mu) / sd > z:
            out.append((i, values[i]))
    return out
```
Prometheus ka URL aur query do, aur anomalies print karo. Phir ek alag script likho jo sirf allow-listed command, jaise `kubectl rollout restart deployment/catalog -n shop`, pehle dry-run mein dikhaye, aur `--approve` flag ke bina chalaye hi nahi. Har action ko ek log file mein likho.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "z-score / seasonality · confirm before alert · autonomy ladder · allow-list + approve + audit".]**

**(Voiceover):**
Recap: simple anomaly detection aur surakshit remediation. Ab ek naya standard jo AI ko tools se jodta hai: MCP.

---

# 📺 EPISODE 3: MCP — AI ko Tools se Jodne ka Standard

### [00:00 – 01:15] Scene 1: Har AI, Har Tool Ke Liye Alag Wiring?
**[VISUAL: Many AI apps and many tools with a tangle of custom connectors (N × M). Then a clean standard plug between them (N + M).]**

**(Voiceover):**
Maan lo aapke paas teen AI apps hain aur paanch tools: GitHub, Kubernetes, Prometheus, ticketing, docs. Har AI ko har tool se alag se jodna, pandrah alag connectors. Model Context Protocol, MCP, ek standard hai jisse AI applications tools aur data se ek hi tareeke se jud sakti hain. Jaise USB: ek port, kai device.

### [01:15 – 05:00] Scene 2: MCP ke Hisse
**[VISUAL: A diagram: Host (AI app, e.g., an IDE or chat app) contains an MCP client → connects to MCP server(s). Server exposes: Tools (actions), Resources (data), Prompts (templates). Transports: stdio (local), HTTP (remote).]**

**(Voiceover):**
MCP mein teen bhumikayein. Host wo AI application hai jisse aap baat karte ho. Host ke andar MCP client hota hai, jo server se jud jaata hai. MCP server wo program hai jo capabilities deta hai. Server teen cheezein de sakta hai: tools, yaani actions jaise "pod list karo", resources, yaani padhne layak data jaise "logs ka ek snapshot", aur prompts, yaani ready templates. Transport ke do tareeke: local ke liye stdio, aur remote ke liye HTTP. AI model tool ko chunta hai, par host ke control mein, aur insaan manzoori de sakta hai.

### [05:00 – 08:30] Scene 3: MCP ki Security
**[VISUAL: A warning list: tool descriptions can be malicious (prompt injection), over-broad permissions, tokens leakage, untrusted servers, confirm destructive actions, read-only by default, sandbox.]**

**(Voiceover):**
MCP ek taakat hai, to usme khatre bhi hain. Kisi anjaan server ko apne host se jodna aise hai jaise anjaan software chalana. Tool ke descriptions aur data mein prompt injection ho sakta hai. Isliye server ko least privilege do: shuruat read-only se, kam scope ka token, aur khatarnaak actions par insaan ki confirmation. Aur secrets ko tool ke output mein mat nikalne do. Production mein sirf wahi servers jodo jin par aap bharosa karte ho aur jinka code ya source aapne dekha hai.

### [08:30 – 11:30] Scene 4: Lab: Pehle Dekho, Phir Banao
**[VISUAL: A sketch of the MCP server we will build: tools `list_pods(namespace)`, `get_pod_logs(pod, tail)`, `query_prometheus(promql)`. A table: tool, inputs, returns, risk level (all read-only).]**

**(Voiceover):**
Lab (design): apne DevOps MCP server ke liye teen tools socho. `list_pods(namespace)` jo pods aur unki states de. `get_pod_logs(pod, tail)` jo aakhri kuch lines de. `query_prometheus(promql)` jo ek query ka result de. Ek table banao: tool ka naam, inputs, return, aur risk, aur teeno ko read-only rakho. Jo bhi tool kuch badalta hai, use abhi mat banao. Agle episode mein hum ise code mein likhenge.

### [11:30 – 13:00] Scene 5: Recap aur Bridge
**[VISUAL: A card: "host + client + server · tools/resources/prompts · stdio vs HTTP · read-only first".]**

**(Voiceover):**
Recap: MCP ka idea, hisse aur security. Ab apna server banate hain.

---

# 📺 EPISODE 4: Apna DevOps MCP Server aur Course ka Antim Sabak

### [00:00 – 01:15] Scene 1: Chat Mein Pucho, Cluster Jawab De
**[VISUAL: A chat UI: "Why is catalog restarting?" The AI calls `list_pods`, then `get_pod_logs`, then answers with the likely cause and a suggested fix, asking for approval before any change.]**

**(Voiceover):**
Soch ke dekho: aap chat mein poochte ho "catalog service baar baar restart kyun ho rahi hai?" AI `list_pods` call karta hai, phir `get_pod_logs`, aur batata hai ki memory limit ki wajah se OOMKilled ho raha hai, aur fix suggest karta hai. Aap hi tay karte ho ki lagu karna hai ya nahi. Is episode mein hum aisa server banate hain.

### [01:15 – 05:00] Scene 2: MCP Server Code
**[VISUAL: A Python file using the official MCP Python SDK: `from mcp.server.fastmcp import FastMCP`, `mcp = FastMCP("devops")`, `@mcp.tool()` decorated functions that run `kubectl get pods -o json` and return trimmed results, `mcp.run()`.]**

**(Voiceover):**
Official Python SDK ke saath server chhota hota hai:
```python
import json, subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("devops")
ALLOWED_NS = {"shop", "monitoring"}

def kubectl(*args: str) -> str:
    out = subprocess.run(["kubectl", *args], capture_output=True, text=True, timeout=15)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip()[:500])
    return out.stdout

@mcp.tool()
def list_pods(namespace: str) -> str:
    """List pods and their status in an allowed namespace (read-only)."""
    if namespace not in ALLOWED_NS:
        raise ValueError(f"namespace not allowed: {namespace}")
    data = json.loads(kubectl("get", "pods", "-n", namespace, "-o", "json"))
    return json.dumps([{"name": p["metadata"]["name"], "phase": p["status"]["phase"]} for p in data["items"]])

if __name__ == "__main__":
    mcp.run()
```
Dhyaan: allow-list, timeout, truncated errors, aur shell ka istemaal nahi, sirf argument list.

### [05:00 – 08:30] Scene 3: Logs Tool aur Hardening
**[VISUAL: A `get_pod_logs(namespace, pod, tail=50)` tool with tail capped at 200 and secrets patterns redacted by regex. Tests with a fake `kubectl`. A config snippet adding the server to an MCP-capable host.]**

**(Voiceover):**
Logs tool mein `tail` ko seemit karo, jaise maximum 200 lines, aur output mein token ya password jaise patterns ko redact karo, kyunki logs mein secrets aa jaate hain. Inputs ko validate karo, jaise pod ka naam sirf allowed characters ka ho, taaki koi command injection na ho. Server ke liye unit tests likho, jahan `kubectl` ki jagah ek fake function ho. Aur host mein server ko config se jodo, jahan command `python server.py` ho, aur host ke docs ke mutabiq ek chhoti config entry. Bina approval ke koi write tool nahi.

### [08:30 – 11:30] Scene 4: Lab: Server Chalao aur Aazmao
**[VISUAL: Run the server with the MCP Inspector or an MCP-capable host. Call `list_pods("shop")`. Try `list_pods("kube-system")` and see the rejection. Try a bad pod name and see validation fail.]**

**(Voiceover):**
Lab: `pip install "mcp[cli]"` karke server banao. MCP Inspector, jo official debugging tool hai, ya kisi MCP-capable host mein server jodo. `list_pods("shop")` chalao: pods dikhenge. `list_pods("kube-system")` chalao: ValueError aana chahiye, kyunki namespace allow-list mein nahi. Ek galat pod naam `get_pod_logs("shop", "x; rm -rf /")` do aur dekho ki validation use rok deta hai. Ye guardrails hi is server ko surakshit banate hain. Tool descriptions ko saaf aur chhota rakho, taaki model sahi tool chune.

### [11:30 – 13:00] Scene 5: Course ka Antim Sabak
**[VISUAL: The Build → Ship → Fix arrow, with the full course map behind it: Linux, Cloud, CI/CD, Containers, Kubernetes, IaC, Monitoring, AI. A pilot in a cockpit with an autopilot indicator.]**

**(Voiceover):**
Aapne Linux se shuru kiya, cloud, CI/CD, containers, Kubernetes, IaC, monitoring aur ab AI tak pahunche. Ye sab ek hi kahani hai: Build, Ship, Fix. AI aapka autopilot hai, wo tez hai, par aapka jawab-deh pilot kaun hai? Aap. Draft AI ka, jaanch aapki. Guardrails pehle, autonomy baad mein. Ab agla kadam aapka hai: Mini Shop aur capstone ko apne GitHub par rakho, README likho, aur ek aisi pipeline banao jise aap kisi ko explain kar sako. Isi se aap asli engineer banoge.

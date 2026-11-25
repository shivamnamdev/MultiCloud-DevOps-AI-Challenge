# 🎙️ 02a: TELEPROMPTER / READ-ALOUD SCRIPT: SESSION-33_aiops-and-mcp-servers

*Extracted word-for-word from `02_script.md` by `tools/teleprompter/extract.py` (voiceover prose only; [VISUAL] directives, code fences and metadata removed; markdown stripped). If you edit spoken text, edit the script first, then re-run extraction. `teleprompter/` videos are built from this file.*

**Spoken words:** ~2,682 · **Episodes:** 4

---

# EPISODE 1: Raat ki Duty

## Teen Baje, Do Hazaar Alerts

Raat ke teen baje Atithi ka records office ruk jaata hai. Control room mein do hazaar alerts: billing ki latency, reservations ke errors, kitchen queue ka lag. Duty manager ke phone par ghanti nahi, shor. Session 26 ke alarm desk ne grouping aur inhibition se kaafi shor kam kiya tha, par jab system bada ho, tab bhi insaan ko ek ek alert padhna padta hai. AIOps ka matlab hai operations mein data analysis aur AI ka upyog: alerts ko jodna, normal se alag pattern pakadna, aur duty manager ko kam shor aur zyada samajh dena. Ye manager ki jagah nahi, madad hai. Is session mein assistant raat ki duty par baithta hai, par chaabiyan manager ke paas hi rehti hain.

## AIOps ke Paanch Kaam

AIOps ke paanch kaam. Ek, correlation: ek hi kaaran ke kai alerts ek incident mein. Do, anomaly detection: wo pattern jo us samay ke liye normal nahi, jahan fixed threshold kamzor padte hain. Teen, root-cause ke ishare: kaun si service pehle bigdi, aur us se thodi der pehle kya deploy hua, jaise Session 31 ka deploy log. Chaar, summary aur ChatOps: "pichhle ek ghante mein kya hua?" ka saaf jawab. Aur paanch, automatic fix, jo sabse risky hai, aur jisse hum guardrails ke saath dekhenge. Ek niyam: jitna zyada kaam badle, utna zyada bharosa chahiye, isliye pehle teen kaam aasaan hain aur paanchva sabse mushkil.

## Pehle Data, Phir AI

Ek sacchai: AIOps ki neev achhi observability hai. Agar saaf meters, logs, labels aur service ke maalik ka naam nahi, to AI bhi andhera hi dikhayega, aur andhere mein LLM aksar andaza lagata hai, jo sunne mein sahi lagta hai par galat hota hai. Isliye is course mein pehle control room, Session 26, aaya, aur AIOps ab. Pehle labels aur ownership theek karo, SLO tay karo, alerts saaf karo, runbook likho. Phir assistant ke paas padhne ke liye kuch bharosemand hoga. Aur wahi runbook assistant ko batayega ki is alert par kya karna hai.

## LLM Kahan Achha, Kahan Nahi

LLM kahan achha hai: log ke tukde ka saransh, anjaan error ka matlab, timeline se post-incident review ka pehla draft, PromQL samjhana, aur "agla kya dekhna chahiye" ka suggestion. Kahan nahi: metrics par sahi hisaab, akele severity tay karna, bina nigrani ke commands chalana, aur wo cheezein jo use dikhayi hi nahi gayi. Hisaab ke liye code use karo, jaise agle episode ka z-score. Aur ek niyam jo bahut kaam aata hai: assistant jab kuch kahe, to saath mein wo lines bhi dikhaye jin par uska andaza tika hai, taaki duty manager ek nazar mein jaanch sake. Bina saboot ka jawab, chahe kitna bhi saaf bole, sirf ek raay hai.

## Lab: Do Hazaar Mein Se Bees

Lab (kaagaz par): ek kalpanik incident ke bees alerts: records office ki latency, bookings ke 5xx, queue lag, frontend errors, aur do disk ke jo pehle se chal rahe the. Unhe time aur dependency se group karo. Pehla alert kaun sa tha? Kaun sa sirf shor tha? Root cause kya ho sakta hai, aur kya saboot hai? Phir har group ke saamne likho ki Session 26 ke runbook ki kaun si line lagegi. Ye haath se kiya hua kaam hi samjhata hai ki correlation ka asli maqsad kya hai: manager ko ek incident dikhana, bees alert nahi. Agle episode mein isi kaam ka ek chhota hissa code mein karte hain.

## Recap aur Bridge

Recap: AIOps kya hai, uski neev, aur LLM ki jagah. Ab hands-on: anomaly detection aur surakshit healing.

---

# EPISODE 2: Pehle Dekho, Phir Suggest Karo, Phir Karo

## Threshold Kamzor Kyun

Fixed threshold, jaise "CPU 80% se upar", har jagah sahi nahi. Shaam ke peak mein 80% normal ho sakta hai, aur raat ke teen baje 40% bhi ajeeb. Booking website ka traffic roz ek lahar ki tarah chalta hai, aur weekend par alag. Anomaly detection ye dekhta hai ki value us samay ke liye normal se alag hai ya nahi. Aur ek chhota sa statistics bhi aksar kaafi madad karta hai, isliye bade ML model se pehle usi se shuru karo.

## Seedha Tareeka: z-score aur Pichhle Hafte ka Ghanta

Sabse saral tareeka: rolling average aur standard deviation. Agar naya value average se teen standard deviation se zyada door ho, to anomaly. Isko z-score kehte hain. Roz ki lahar wale data ke liye aur behtar: aaj ke shaam aath baje ko pichhle hafte ke usi ghante se milao. Prometheus ke andar bhi stddev_over_time aur avg_over_time hain, aur predict_linear aage ka raasta dikhata hai, jaise disk kab bharegi. Teen jaal. Ek, ek hi point par alarm mat bajao: kai points tak anomaly rahe tab. Do, jo series bilkul seedhi ho, usme standard deviation sifar hota hai aur z-score fat jaata hai, isliye wahan alag rule. Teen, naye service par detector chup rahe, kyunki history kam hai. Bade ML model tabhi, jab ye saral tareeke kaafi na hon.

## Autonomy ki Seedhi

Automatic fix ek seedhi par chadhta hai. Pehla paaydaan: sirf dekhna aur batana. Doosra: fix suggest karna, saboot ke saath. Teesra: duty manager ki manzoori ke baad fix. Aur sabse upar: sirf kam khatre aur ulte ho sakne wale kaam khud karna, jaise ek atki hui parking bay ko restart karna. Bahut si teams doosre ya teesre paaydaan par hi rukti hain, aur ye bilkul theek hai. Upar ke lal hisse mein kuch kaam kabhi akele nahi: data delete karna, database chhota karna, security ke niyam badalna, aur wo kaam jisme paisa lagta ho. Seedhi ek ek paaydaan chadho, aur har paaydaan par pehle kuch hafte sirf record karo ki assistant kya karta, aur manager kya karta.

## Guardrails

Guardrails, ek ek karke. Allow-list: sirf wahi exact actions jinki ijaazat hai, jaise atithi wing ki do services ka restart. Dry run pehle: pehle bolo ki kya karoge. Approval: bina --approve ya manager ke "haan" ke nahi. Rate limit: ek service ko tees minute mein ek baar se zyada restart nahi, warna restart ka loop ban jaata hai. Audit log: har koshish ki ek line, kisne, kya, kab. Kill switch: ek file ya flag jo sab band kar de. Aur sabse zaroori: code ke guardrail ke saath cluster ki taraf se bhi guardrail. Helper ka apna duty badge, yaani Kubernetes role, sirf wahi deployments restart kar sake. Code mein bug ho to bhi badge ki seema bachati hai. Ye Session 4 aur 9 ka least privilege hi hai.

## Incident ka Saransh: Saboot ke Saath

Ab LLM ka sahi upyog. Alert ke saath ye cheezein jodo: sabse haali deploy ki line, kuch log ki lines, aur teen chaar metric ke numbers. Inhe ek prompt mein markers ke beech rakho, aur kaho ki saransh dena hai aur har dawe ke saath wo line batani hai jis par wo tika hai. Phir ye duty manager ko jaaye, runbook ke link ke saath. Ek khaas chetavani, jo Session 32 se aati hai: log ki lines bhi untrusted text hain. Kisi guest ke naam ya request mein chhupi instruction log mein aa sakti hai, aur wo summary tool ko behka sakti hai. Isliye markers, tools ke bina, aur jawab sirf ek suggestion, kabhi seedha action nahi. Aur personal data log se pehle hata do.

## Lab: Detector aur Safe Restart

Lab. Pehle detector:

Prometheus ka URL aur ek query do, jaise sum(rate(http_requests_total{status=~"5.."}[1m])), aur har series par anomalies chalao. Local Session 26 ki rooms-service par load script se jaan-boojh kar errors bhejo, aur dekho ki detector tab bolta hai. Do seemayein yaad rakho jo hamare test mein dikhin: jo series hamesha sifar rehti hai (koi error nahi) wo achanak badhe to detector chup rehta hai, kyunki standard deviation sifar hai; aur kuch der ke baad window naye, bure level ko hi normal maan leta hai, isliye alarm band ho jaata hai jabki error ab bhi zyada hain. Ab restart helper:

Chalao bina --approve ke: sirf plan. Do kamiyan hamare test mein dikhin: LOG aur KILL relative path hain, isliye helper ko kisi aur folder se chalao to cooldown aur kill switch kaam hi nahi karte; aur log mein sirf safal restart aati hai, jabki guardrail kehta hai har koshish. Lab ki safe_restart_v2.py dono theek karti hai. Allow-list ke bahar ki service do: mana. Do baar jaldi jaldi --approve: doosri baar mana. Ek KILL file banao aur dekho ki sab ruk jaata hai.

## Recap aur Bridge

Recap: saral anomaly detection aur surakshit healing. Ab ek naya standard jo assistant ko hotel ke tools se jodta hai: service hatch, yaani MCP.

---

# EPISODE 3: Service Hatch ka Standard

## Har Assistant, Har Tool ke Liye Alag Wiring?

Maan lo Atithi mein teen alag AI apps hain: ek IDE mein, ek chat mein, ek control room ke liye. Aur paanch tools: Git, Kubernetes, Prometheus, ticketing aur docs. Har app ko har tool se alag jodna, pandrah alag taar. Model Context Protocol, yaani MCP, ek standard hai jisse AI apps tools aur data se ek hi tareeke se jud sakti hain. Isse pandrah taar ki jagah aath: har app ek taraf, har tool doosri taraf. Jaise USB: ek port, kai device. Hamari story mein ye service hatch hai: ek saaf khidki jisse assistant hotel ke tools ko chhoota hai, aur har tool apni hatch par apne niyam tay karta hai.

## Hatch ke Hisse

MCP mein teen bhumikayein. Host wo AI app hai jisse aap baat karte ho. Host ke andar MCP client hota hai, jo server se jud jaata hai. MCP server wo program hai jo capabilities deta hai, yaani hamari service hatch. Server teen cheezein de sakta hai: tools, yaani kaam jaise "pods ki list do"; resources, yaani padhne layak data jaise "ek log ka snapshot"; aur prompts, yaani ready templates. Transport ke do tareeke: local ke liye stdio, jahan host server ko apni hi machine par chalata hai, aur remote ke liye HTTP, jahan server door ki machine par hai aur wahan authentication zaroori hai. Assistant tool chunta hai, par host ke control mein, aur host aksar insaan se manzoori maangta hai.

## Hatch ki Suraksha

Pehla: koi anjaan server apne host se jodna, matlab anjaan program apni machine par chalana. Doosra: tool ke description mein ya uske jawab mein chhupi instruction ho sakti hai, jise model padhta hai, isliye server ka source dekho aur sirf bharose wale server jodo. Teesra: tool ke jawab, jaise log, bhi untrusted text hain, wahi prompt injection jo Session 32 mein dekha. Chautha: token ka daayra, yaani wahi least privilege: shuruat read-only se, aur cluster ki taraf se bhi read-only badge. Paanchva: remote hatch par login zaroori hai. Chhatha: koi bhi tool jo "koi bhi shell command chalao" kahe, wo hatch nahi, khuli khidki hai. Tool chhote hon, aur apne input ko khud jaanchein.

## Hatch Kaun Si Cheezein Kholega

Hatch ka design pehle kaagaz par. Teen tools. list_pods(namespace): allowed namespaces mein pods aur unki halat. get_pod_logs(namespace, pod, tail): kuch aakhri lines, jisme tail ki seema ho aur secrets hata diye gaye hon. query_prometheus(promql): inspector se ek sawaal, jisme URL fixed ho, samay ki seema ho aur jawab chhota ho. Teeno ke saamne risk "sirf padhna". Chautha tool, restart, abhi nahi: wo episode 2 ka alag, manzoori wala helper hai, aur use hatch se jodna ek alag, soch-samajh kar liya hua faisla hoga. Pehle hatch se sirf dekhna sikho.

## Lab: Design ko Test Karo

Lab (design): har tool ke liye teen galat istemaal likho. Galat wing mein pods maangna. Pod ke naam mein semicolon aur command daalna. Bahut bada output maangna, jaise ek lakh log lines ya ek bahut bhaari PromQL. Phir har ek ke saamne likho ki server kya karega: mana karega, input saaf karega, ya output kaat dega. Agle episode mein hum yahi code mein likhenge, aur jo likha hai wo test bhi karenge.

## Recap aur Bridge

Recap: MCP ka idea, uske hisse, aur uski suraksha. Ab apni service hatch banate hain.

---

# EPISODE 4: Apni Service Hatch Banao

## Chat Mein Pucho, Control Room Jawab De

Soch ke dekho: duty manager chat mein poochta hai "rooms-service baar baar restart kyun ho rahi hai?" Assistant list_pods chalata hai, phir get_pod_logs, phir ek query_prometheus, aur jawab deta hai ki memory limit par OOMKilled ho raha hai, ye rahi wo lines, aur ye rahi memory ki query. Saath mein saaf kehta hai ki restart wo nahi kar sakta, kyunki hatch mein wo tool hai hi nahi. Faisla manager ka. Is episode mein hum aisi hatch banate hain.

## Hatch ka Code

Official Python SDK ke saath hatch chhoti hoti hai. Ek dhyaan ki baat: version 1 mein from mcp.server.fastmcp import FastMCP hai, aur version 2 mein naam MCPServer ho gaya. Hum version 1 likhte hain, aur lab mein pip install "mcp[cli]<2" lagayenge. Version 2 par jaana ho to import aur naam dono badlo: from mcp.server.mcpserver import MCPServer.

Dhyaan do: namespace allow-list, naam ki regex, timeout, error ka chhota hissa, aur shell ka istemaal nahi, sirf argument ki list, taaki naam mein semicolon ka koi matlab hi na rahe.

## Logs aur Prometheus: Chhote Output, Saaf Output

Logs tool mein tail ki seema, jaise maximum 200, aur output mein password, token ya api key jaise patterns ko [redacted] kar do, kyunki log mein secrets aa hi jaate hain:

Prometheus tool mein URL environment variable se, tool ke argument se kabhi nahi, taaki koi hatch ko andar ke kisi aur address par na bhej sake. Query ki lambai ki seema, timeout, aur jawab ke pehle kuch hazaar akshar. "UNTRUSTED LOG TEXT" ka prefix isliye ki host ko aur model ko dikhe ki ye data hai, instruction nahi. Ye redaction poora bachaav nahi, bas ek parat hai: hamare test mein Authorization: Bearer ..., AWS key ID aur URL ke andar ka password nikal gaye (lab ki redact.py inhe pakadti hai), isliye logs mein secrets na likhne ki aadat pehle.

Teesra tool ye raha. Upar ke imports mein urllib.error, urllib.parse aur urllib.request jodo, aur hatch chalate waqt PROM_URL environment variable do:

Galat PromQL par Prometheus ka error text wapas aata hai, jo assistant ke kaam ka hai.

## Cluster ki Taraf se Taala

Code ke guardrail ke saath cluster ka guardrail. Hatch ek alag service account se kubectl chalaye, jiske Role mein atithi wing mein pods par sirf get aur list, aur pods/log par get. Delete, exec ya Secrets padhne ki koi ijaazat nahi. kubectl auth can-i delete pods --as=system:serviceaccount:atithi:hatch ka jawab no aana chahiye, aur get pods/log ka yes. Is tarah agar kal koi bug ya injection hatch ko behka bhi de, to badge hi use sirf padhne dega. Ye wahi least privilege hai jo Session 4 se chala aa raha hai, bas ab assistant ke liye.

## Lab: Hatch Chalao aur Todo

Lab: SDK install karo: pip install "mcp[cli]<2". Iske liye Python 3.10 ya naya chahiye: python3.12 -m venv .venv jaisa naya interpreter lo, ya python:3.12-slim container use karo. fastmcp naam ka alag package bhi hai, jiska import alag hai. MCP Inspector ya kisi MCP-capable host mein server jodo. list_pods("atithi"): pods dikhenge. list_pods("kube-system"): mana, kyunki wo allow-list mein nahi. get_pod_logs("atithi", "x; rm -rf /"): mana, naam ki jaanch se. tail=100000 do: 200 par kat jaata hai. Phir kubectl ki jagah ek nakli function lagakar unit tests likho. Aur ek log mein jaan-boojh kar password=abc123 rakho, aur dekho ki [redacted] aata hai. Host ki config mein command python hatch.py, aur hatch ko wahi service account jo pichhle scene mein banaya.

## Hatch aur Helper Saath Mein

Ab dono ko jodo, par ek ek kadam. Detector anomaly pakadta hai. Assistant hatch se pods, logs aur metrics padhta hai, aur saboot ke saath ek incident card banata hai, jisme runbook ka link hai. Wo suggest karta hai: "rooms-service ko restart karo". Duty manager helper ko --approve ke saath chalata hai, ya mana kar deta hai. Har kadam ki ek line audit log mein. Subah assistant post-incident review ka pehla draft likhta hai, jise manager padhta aur sudharta hai. Dekho kitni baar insaan beech mein hai: faisle ke waqt. Jab kuch hafte ke baad bharosa bane, tab hi kam khatre wale kaam, jaise ek stuck pod ka restart, autonomy ki seedhi par ek paaydaan upar jaa sakte hain, aur sirf wahi.

## Course ka Antim Sabak

Aapne ek khaali building se shuru kiya. Linux se uske andar ke staff aur darwaze seekhe. AWS se campus. Git aur Jenkins se head office. Docker aur Kubernetes se trucks aur operations command. Prometheus se control room. Terraform aur Ansible se master plan aur setup crew. Azure se doosra landlord. AI se assistant, outside expert aur trained brain. Ye sab ek hi kahani hai: Build, Ship, Fix. Aur assistant ek tez autopilot hai, par pilot kaun hai? Aap. Draft assistant ka, jaanch aapki. Guardrail pehle, autonomy baad mein. Ab agla kadam aapka hai. Apna atithi-booking, atithi-rooms aur capstone ki conveyor ek GitHub repo mein rakho, README mein guest ki journey ke aath kadam likho, ek chhota architecture diagram banao, aur ek kharab release ko rollback hote hue record karo. Phir jab koi poochhe ki aap kya karte ho, to aap ek asli kahani, aur ek chalti hui conveyor dikha sakte ho. Isi se aap engineer banoge.

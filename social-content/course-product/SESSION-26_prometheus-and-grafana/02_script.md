# ✍️ 02: SCRIPT — SESSION-26: Prometheus and Grafana
### *DevOps with AI: Build, Ship, Fix — Original Hinglish Script (Faceless Production Edition)*
*Rules: 3s visual hook + promise + course story (Atithi Hotels) + hands-on lab in every episode + binge bridge. Topic map: `SYLLABUS_BLUEPRINT.md` (original wording). Story words: `ANALOGY_STORY.md`.*

## 🎯 Production Metadata
- **Script ID:** `DEVOPS-S26`
- **Focus:** Observability (metrics, logs, traces), golden signals, RED and USE, SLI, SLO and error budget, Prometheus pull model, exporters, metric types, labels and cardinality, instrumenting a Python service, PromQL (`rate`, `sum by`, `histogram_quantile`), `kube-prometheus-stack` with Helm, ServiceMonitor, Grafana panels, variables and dashboards as code, alert rules, Alertmanager (grouping, routing, silence, inhibition), symptom-based alerts, runbooks
- **Builds on:** Session 05 (`top`, `free`, `df`), Session 11 (marshal health check), Session 15 (CloudWatch metrics, alarms, noise), Session 22 (`rooms-service`, `/health`), Session 24 and 25 (pods, namespaces, Helm, PVC, troubleshooting table)
- **Story position:** Zoom level 3, head office. Control room khulta hai: ek inspector jo har meter ko har kuch second mein padhta hai, ek alarm desk jo sahi duty manager ko phone karta hai, aur live screens ki deewar. Sab ek franchise kit se lagta hai.
- **Story words used:** inspector (Prometheus), meters (metrics, exporters), alarm desk (Alertmanager), wall of screens (Grafana), franchise kit (Helm), control room, truck (container), parking bay (pod), wing (namespace), standing order (Deployment), marshal (load balancer), duty manager (on-call), guest (end user), staff (admin)
- **Lab project:** Atithi's `rooms-service` gets a `/metrics` page, the inspector reads it, the wall of screens shows request rate, errors and latency, and an alert rings the alarm desk when guests see errors.
- **Cost rule:** the monitoring stack is heavy for a laptop cluster (give it memory) and is billed like any workload on a cloud cluster, including its disks. Delete the stack and its volumes at the end of the lab.
- **Episodes:**
  - Episode 1: Control Room kyun: Observability aur Golden Signals
  - Episode 2: Inspector: Prometheus, Exporter aur PromQL
  - Episode 3: Franchise Kit aur Screens: Helm Stack aur Grafana
  - Episode 4: Alarm Desk: Alert, Alertmanager aur Runbook

---

# 📺 EPISODE 1: Control Room kyun

### [00:00 – 02:35] Scene 1: Gaadi ka Dashboard
**[VISUAL: A car dashboard with speed, fuel, engine temperature and a warning light. Next frame: a car with no dashboard rolling to a stop on a highway at night.]**

**(Voiceover):**
Gaadi chalate waqt dashboard aapko speed, tel aur engine ka temperature batata hai, aur warning light pehle se chetavani deti hai. Bina dashboard ke gaadi achanak rukti hai. Atithi ki truck park ab Kubernetes par chal rahi hai: dus services, kai wings, kai buildings. Agar kuch dheema hua, to guests ko pehle pata chalega ya hamein? Session 15 mein humne landlord ke meters aur CloudWatch dekhe. Ab head office ka apna control room banate hain, jo trucks ke andar tak dekhta hai, aur jo kisi bhi landlord par ek jaisa chalta hai.

### [02:35 – 05:20] Scene 2: Teen Pillars
**[VISUAL: Three pillars. Metrics: numbers over time ("what is happening"). Logs: records of events ("why"). Traces: the journey of one request across services ("where it got slow"). One sample question under each.]**

**(Voiceover):**
Observability ka matlab hai ki system ke bahar ke signals dekhkar andar ki halat samajh paao. Iske teen pillars. Metrics: samay ke saath badalte numbers, jaise requests per second. Wo batate hain kya ho raha hai. Logs: ghatnaon ke record, jo batate hain kyun. Traces: ek request ka kai services ke beech poora safar, jo batata hai kahan dheema hua. Is session mein hum metrics par dhyaan denge, kyunki Prometheus aur Grafana ki jodi sabse aam hai. Logs ke liye Loki jaise tools, aur traces ke liye OpenTelemetry, aage ki padhai hain, par wahi teen sawaal yaad rakho.

### [05:20 – 07:55] Scene 3: Kya Naapein: Golden Signals
**[VISUAL: Four gauges: Latency, Traffic, Errors, Saturation. Beneath, RED for services (Rate, Errors, Duration) and USE for resources (Utilization, Saturation, Errors).]**

**(Voiceover):**
Kya naapein? Session 15 ke chaar signals yaad hain: latency, traffic, errors aur saturation. Google ke SRE ne inhe golden signals kaha hai. Latency: request kitni der leti hai. Traffic: kitni aa rahi hain. Errors: kitni fail ho rahi hain. Saturation: system kitna bhara hai. Services ke liye RED: Rate, Errors, Duration. Building jaise resources ke liye USE: Utilization, Saturation, Errors, jo Session 5 ke `top`, `free` aur `df` ka systematic roop hai. Chaar golden signals se zyadatar problems pakadi jaati hain, aur har dashboard inhi se shuru hona chahiye, baaki detail neeche.

### [07:55 – 10:55] Scene 4: SLI, SLO aur Error Budget
**[VISUAL: A worksheet for `bookings-service`. SLI: "good requests / all requests" and "95% of requests under 300 ms". SLO: "99.5% good over 30 days". Error budget: "0.5% of requests may fail". A bar showing budget used so far this month.]**

**(Voiceover):**
Naapna kaafi nahi, ek target bhi chahiye. SLI, Service Level Indicator, wo number jo aap naapte ho: kitne percent requests successful, ya kitne percent 300 ms se tez. SLO, Service Level Objective, wo target: "tees din mein 99.5 percent requests successful." Aur error budget: baaki 0.5 percent, yaani jitni galtiyon ki chhoot hai. Ye budget team ko seedha faisla deta hai. Budget bacha hai to naya release karo, aur budget khatam ho gaya to nayi cheezein ruko aur sthirta par kaam karo. Is se "kitna achha kaafi hai" ka jhagda number mein badal jaata hai. Target ko 100 percent mat rakho: wo mehnga hai aur kabhi milta nahi.

### [10:55 – 13:55] Scene 5: Lab: Paper par SLI aur SLO
**[VISUAL: A fill-in sheet for `rooms-service` and `bookings-service`: which SLI, which target, what the error budget is in minutes per month. A line "99.9% over 30 days is about 43 minutes of failure".]**

**(Voiceover):**
Lab (paper). `bookings-service` aur `rooms-service` ke liye teen cheezein likho. Ek SLI: success rate, aur 95th percentile latency. Ek SLO, jaise "tees din mein 99.5 percent successful, aur 95 percent request 300 ms se kam." Aur error budget ko minutes mein badlo: 99.9 percent ka matlab tees din mein lagbhag 43 minute ki chhoot. Phir sochkar likho ki bookings ka SLO rooms ke SLO se zyada sakht kyun hona chahiye. Guest rooms ki list dheemi dekh kar ruk sakta hai, par booking ke beech mein error aaye to wo seedha chala jaata hai. Aur koi bhi SLO bina is jawab ke ki "isko kaun dekhega" adhoora hai.

### [13:55 – 14:25] Scene 6: Recap aur Bridge
**[VISUAL: A card: "metrics = what, logs = why, traces = where · golden signals · RED and USE · SLI measure, SLO target, error budget decides release speed".]**

**(Voiceover):**
Recap: observability, golden signals aur SLO. Ab inspector se milte hain: Prometheus.

---

# 📺 EPISODE 2: Inspector

### [00:00 – 02:15] Scene 1: Inspector Poochhta Hai
**[VISUAL: A Prometheus server visiting apps every 15 seconds: "give me your numbers" to a `/metrics` page, storing the replies in a time-series database. One app does not answer, and its `up` turns to 0.]**

**(Voiceover):**
Prometheus ka tareeka alag hai. Trucks apne numbers inspector ko bhejti nahi. Inspector khud har kuch second mein har truck ke paas jaakar poochta hai: "tumhare numbers do." Isse pull model kehte hain. Ek bonus: agar truck jawab hi na de, to inspector ko turant pata chal jaata hai ki wo gir gayi, kyunki us ka `up` meter zero ho jaata hai. Session 11 ke marshal ke health check ka yahi vichar hai, bas har meter ke liye. Numbers ek time-series database mein jaate hain, aur har number ke saath samay hota hai.

### [02:15 – 05:15] Scene 2: Exporter, Metric ke Types aur Labels
**[VISUAL: Components: Prometheus server (scrape, storage, PromQL), `/metrics` pages, a node exporter beside a building, service discovery in Kubernetes. Metric types: Counter, Gauge, Histogram. Labels such as `method="GET"` and `status="500"`.]**

**(Voiceover):**
Truck ke paas ek `/metrics` page hota hai, jisme uske numbers text mein hote hain. Jo cheezein khud numbers nahi deti, unke liye exporter: building ke CPU, memory aur disk ke liye node exporter, jo Session 5 ke `top` aur `df` ko numbers mein badalta hai. Kubernetes mein service discovery se targets apne aap milte hain. Metric ke teen type. Counter: sirf badhta hai, jaise kul requests. Gauge: upar neeche hota hai, jaise memory. Histogram: values ko buckets mein ginta hai, jisse latency ke percentiles nikalte hain. Labels metric ko dimension dete hain, jaise `method="GET"` aur `status="500"`. Ek dhyaan: label ki values bahut zyada hon, jaise har guest ka ID, to inspector ki memory phat jaati hai. Ise cardinality ka khatra kehte hain.

### [05:15 – 07:15] Scene 3: Apni Service ko Meter Do
**[VISUAL: A Python snippet with `prometheus_client`: a `Counter('http_requests_total', ..., ['method','path','status'])`, a `Histogram('http_request_duration_seconds', ...)`, and a route `/metrics` returning `generate_latest()`. A note: "label by route, never by guest id".]**

**(Voiceover):**
Apni service ke meters khud lagane padte hain. Python mein `prometheus_client` library: ek Counter `http_requests_total` labels `method`, `path` aur `status` ke saath, ek Histogram `http_request_duration_seconds`, aur ek `/metrics` route jo `generate_latest()` ka jawab de. Har request ke baad counter ek badhao, aur samay histogram mein daalo. Label mein route ka template rakho, jaise `/rooms/<id>`, guest ya room ki asli ID nahi. Wahi cardinality ka sabak. Ye Session 22 ki rooms-service ka chhota sa sudhaar hai, aur Session 7 ke Python ka seedha upyog.

### [07:15 – 09:35] Scene 4: PromQL ki Basics
**[VISUAL: Queries and results. `up`. `rate(http_requests_total[5m])`. `sum by (status)(rate(http_requests_total[5m]))`. An error ratio with `status=~"5.."`. `histogram_quantile(0.95, sum by (le)(rate(http_request_duration_seconds_bucket[5m])))`.]**

**(Voiceover):**
PromQL Prometheus ki query language hai. `up` batata hai kaun si trucks zinda hain. Counter ko seedha nahi dekhte, uski rate dekhte hain: `rate(http_requests_total[5m])` pichhle paanch minute mein per second requests. `sum by (status)(...)` unhe status ke hisaab se jodta hai. Error ratio ke liye 5xx ki rate ko poori rate se divide karo: `sum(rate(...{status=~"5.."}[5m])) / sum(rate(...[5m]))`. Aur latency ke liye `histogram_quantile(0.95, ...)`. Ek aam galti: counter ko bina `rate` ke plot karna, jo bas ek badhti hui line dikhata hai aur kuch nahi batata. Aur `[5m]` ka window bahut chhota rakhoge to graph jhatke maarega.

### [09:35 – 12:30] Scene 5: Recording Rule aur Yaadashta ki Seema
**[VISUAL: A heavy PromQL query that takes seconds on a big dashboard, replaced by a stored result from a recording rule `job:http_requests:rate5m`. Beside it, a storage bar: "15 days local retention" and an arrow to a long-term store.]**

**(Voiceover):**
Do baatein jo dashboard badhne par dikhti hain. Ek: bhaari query. Agar ek dashboard har baar sau trucks par `histogram_quantile` chalaye, to wo dheema ho jaata hai. Recording rule us query ka natija inspector khud har minute ek naye metric mein rakh deta hai, jaise `job:http_requests:rate5m`, aur dashboard use seedha padhta hai. Do: yaadashta. Prometheus ka apna storage kuch hafte ke liye hota hai, aur wo ek PVC par hai, Session 25 ka locker. Lambi history, jaise ek saal, ya kai clusters ek jagah, ke liye alag long-term store chahiye, jaise Thanos ya Mimir ya cloud ki managed service. Aur ek dhyaan: Prometheus aapka backup system nahi hai. Wo kal ki sehat batata hai, saal bhar ki audit nahi.

### [12:30 – 15:00] Scene 6: Lab: Inspector ko Service Dikhao
**[VISUAL: `rooms-service` exposing `/metrics`. A `prometheus.yml` with two jobs and `docker run -p 9090:9090 prom/prometheus`. The Prometheus UI Targets page shows both UP. A query graph of request rate after `curl` loops.]**

**(Voiceover):**
Lab. `rooms-service` mein `/metrics` jodo, aur truck chalao. `prometheus.yml`:
```yaml
global: { scrape_interval: 15s }
scrape_configs:
  - job_name: prometheus
    static_configs: [{ targets: ['localhost:9090'] }]
  - job_name: rooms
    static_configs: [{ targets: ['rooms:5000'] }]
```
Dono ko ek hi Docker network par chalao, jaise Session 21 mein: `docker run -d --name prom --network appnet -p 9090:9090 -v "$PWD/prometheus.yml:/etc/prometheus/prometheus.yml" prom/prometheus`. UI mein Status, Targets dekho aur dono UP hone chahiye. Ek chhota loop `for i in $(seq 200); do curl -s localhost:5000/ >/dev/null; done` chalao aur `rate(http_requests_total[1m])` ka graph dekho. Phir truck band karo aur dekho ki `up` zero ho jaata hai. Safai: `docker rm -f prom`.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "pull `/metrics` · exporter for what cannot speak · counter, gauge, histogram · labels but not unbounded · `rate()` on counters · `up` = alive".]**

**(Voiceover):**
Recap: pull model, exporter, metric ke types, aur PromQL. Ab Kubernetes ke liye poora control room ek franchise kit se.

---

# 📺 EPISODE 3: Franchise Kit aur Screens

### [00:00 – 01:40] Scene 1: Poora Control Room, Ek Command
**[VISUAL: A `helm install` command and then pods appearing in a `monitoring` wing: prometheus, alertmanager, grafana, node-exporter, kube-state-metrics.]**

**(Voiceover):**
Kubernetes cluster ko monitor karne ke liye Prometheus, Alertmanager, Grafana, node exporter aur kube-state-metrics, sab chahiye. Haath se lagana ek din ka kaam hai, aur ek bhi jagah galti ho to adhura. Helm mein ek community franchise kit hai, `kube-prometheus-stack`, jo ye sab ek command mein lagata hai, Session 25 ke Helm ka seedha upyog. Atithi ke har wing aur har cluster mein wahi control room chale, ek jaisa.

### [01:40 – 04:05] Scene 2: kube-prometheus-stack ke Hisse
**[VISUAL: `helm repo add prometheus-community ...`, `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`. A diagram: Prometheus Operator, ServiceMonitor and PodMonitor objects, PrometheusRule, Grafana with prebuilt dashboards, node exporter on every node, kube-state-metrics.]**

**(Voiceover):**
Kit mein Prometheus Operator hota hai, jo Kubernetes ke objects se Prometheus ko chalata hai. ServiceMonitor aur PodMonitor naye objects hain jinse aap batate ho ki kaun si service ya pod scrape karni hai, bina `prometheus.yml` ko haath se badle. PrometheusRule se alerts. node exporter har building par, aur kube-state-metrics jo Kubernetes ke objects ke numbers deta hai: kitne pods Ready, kitne Pending. Grafana mein cluster ke liye pehle se bane dashboards aate hain. Production mein values file se retention aur storage tay karo, kyunki Prometheus ka data ek PVC par hai, aur default admin password turant badlo.

### [04:05 – 06:35] Scene 3: ServiceMonitor ka Jaal
**[VISUAL: A ServiceMonitor with `selector.matchLabels: app: rooms` and `endpoints: port: http, path: /metrics`. A red callout: the operator only picks up monitors that carry the label `release: monitoring`. In Prometheus Targets the rooms job is missing, then appears after the label is added.]**

**(Voiceover):**
ServiceMonitor banate waqt ek chhota jaal hai. Aap ek ServiceMonitor likhte ho, selector mein `app: rooms`, endpoint mein port ka naam aur `/metrics`, aur Prometheus ke Targets page par rooms dikhta hi nahi. Wajah: Operator sirf un monitors ko uthata hai jinke paas chart ka tay kiya hua label ho, aksar `release: monitoring`. Aur ye bhi dhyaan rakho ki ServiceMonitor ka selector Service ke labels dekhta hai, pod ke nahi, aur port ka naam Service mein bhi likha hona chahiye. Session 23 ka wahi label aur selector wala sabak: ek akshar ka farq aur chupchap khaali. Pehle Targets page dekho, phir labels.

### [06:35 – 09:15] Scene 4: Grafana: Panel, Variable aur Dashboard
**[VISUAL: Grafana. A Prometheus data source. A dashboard with a stat panel for error percent, a time series for request rate by status, a gauge for CPU, a table of top pods. Dropdown variables `namespace` and `pod`. A row layout: signals on top, detail below.]**

**(Voiceover):**
Grafana mein Prometheus data source hota hai. Panel mein ek PromQL query aur ek visualization: time series, stat, gauge, table. Variables se dashboard dynamic banta hai: dropdown se namespace ya pod chuno aur saare panels badal jaate hain. Achha dashboard ek kahani batata hai. Upar golden signals: request rate, error percent, latency, saturation. Neeche detail, jaise pod-wise CPU. Zyada panels mat daalo, kyunki raat ke do baje jab koi dekhta hai, to usse jaldi samajh aana chahiye ki guests ko dikkat hai ya nahi. Aur dashboard ko JSON ya ConfigMap mein save karo, taaki wo vault mein rahe, review ho, aur cluster dobara bane to wapas aa jaaye.

### [09:15 – 12:45] Scene 5: Guest ki Nazar se: Blackbox Probe
**[VISUAL: Two views of the same outage. Inside view: every truck shows `up = 1`. Outside view: a probe from the internet calls the public address and gets a certificate error. A blackbox exporter checking the HTTPS page and its certificate expiry date.]**

**(Voiceover):**
Ab tak hum andar se dekh rahe the. Ho sakta hai ki saari trucks `up = 1` dikhayen, aur phir bhi guest ko page na khule: certificate expire ho gaya, ya Ingress ka rule galat ho gaya, ya DNS toot gaya. Isliye bahar se bhi dekho. Blackbox exporter inspector ki taraf se ek probe chalata hai: public URL par HTTPS call, jawab ka code, kitna samay laga, aur certificate kitne din mein expire hoga. Alert: "certificate das din mein expire" ek ticket hai, aur "public page fail" ek page. Ye Session 11 ke marshal ke health check ka bahar wala bhai hai, aur wahi sawal: guest ko kya dikhta hai? Ek aur tareeka hai guest ki nazar ka: ek bahar ki cloud ya doosri region se probe lagao, taaki ek hi jagah ka outage dono ko ek saath na chhupa le.

### [12:45 – 15:00] Scene 6: Lab: Cluster ko Dekho aur Apna Panel Banao
**[VISUAL: `helm repo add`, `helm install monitoring ...`, `kubectl get pods -n monitoring`, `kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80`, a secret read for the admin password, built-in dashboard "Kubernetes / Compute Resources / Namespace (Pods)", a custom panel with the rooms request rate.]**

**(Voiceover):**
Lab. `helm repo add prometheus-community https://prometheus-community.github.io/helm-charts`, phir `helm install monitoring prometheus-community/kube-prometheus-stack -n monitoring --create-namespace`. Pods Running hone mein kuch minute lagte hain. Phir `kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80`, browser mein `localhost:3000`, aur admin password Secret se nikalo: `kubectl get secret -n monitoring monitoring-grafana -o jsonpath="{.data.admin-password}" | base64 --decode`. Chart ke naye versions install ke baad apna command bhi print karte hain, use dekh lo. Built-in dashboards kholo. Ab `rooms-service` ke liye ServiceMonitor lagao, label `release: monitoring` ke saath, aur Targets page par uska UP hona dekho. Dhyaan: label ke bina target aata hi nahi, aur label lagane ke baad bhi operator ko config reload karne mein aksar ek do minute lagte hain, to turant na ghabrao. Ek aur baat: Prometheus ka `job` label Service ke naam se banta hai, isliye alert ke `job="rooms"` ke liye Service ka naam `rooms` hona chahiye, warna query mein apna Service ka naam likho. Aur agar service gunicorn ke kai workers par chalti hai, to har worker ke apne counters hote hain; seedhe lab ke liye ek worker rakho, ya `prometheus_client` ka multiprocess mode docs se padho. Ek apna panel banao: `sum by (status)(rate(http_requests_total{namespace="atithi"}[5m]))`. Aakhir mein stack hatao: `helm uninstall monitoring -n monitoring`, aur dekho ki uski PVCs bhi gayi ya nahi.

### [15:00 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "franchise kit = kube-prometheus-stack · ServiceMonitor + the right label · Grafana variables · signals on top, detail below · dashboards as code · uninstall also the volumes".]**

**(Voiceover):**
Recap: franchise kit aur screens. Ab ek kadwi sachchai: deewar ki screens ko raat ko koi nahi dekhta. Alarm desk chahiye.

---

# 📺 EPISODE 4: Alarm Desk

### [00:00 – 01:35] Scene 1: Do Sau Alert, Ek Raat
**[VISUAL: A phone buzzing two hundred times in a night with low-value alerts. An engineer silences the phone. A real critical alert arrives, unseen.]**

**(Voiceover):**
Do sau alerts roz raat, aur ek mahine baad aap phone silent kar dete ho. Phir ek asli alert aata hai aur koi nahi dekhta. Ye alert fatigue hai, aur monitoring ka sabse bada dushman. Session 15 ke alarm ka wahi niyam yahan bhi: jis alert par koi kuch nahi karta, wo shor hai. Achha alert kam hota hai, zaroori hota hai, aur usme likha hota hai ki kya karna hai.

### [01:35 – 04:00] Scene 2: Achhe Alert ke Niyam
**[VISUAL: A checklist. Symptom over cause. Actionable. Severity levels. A `for:` duration. A runbook link. Two examples: "page: guests see errors", "ticket: disk 80%".]**

**(Voiceover):**
Niyam. Symptom par alert do, kaaran par nahi. "Guests ko errors dikh rahe hain" ya "booking ka SLO jal raha hai" page-worthy hai. "CPU 80 percent" aksar nahi, kyunki ho sakta hai koi guest ko asar hi na ho. Har alert actionable ho: koi kuch kar sake. Severity tay karo: page jo raat ko jagaaye, aur ticket jo din mein dekha jaaye. `for:` duration lagao, taaki ek second ke spike par alert na aaye. Aur har alert ke saath ek runbook ka link, jisme likha ho pehle kya check karna hai. Is se naya duty manager bhi, jo us raat pehli baar aaya hai, kaam shuru kar sakta hai.

### [04:00 – 06:35] Scene 3: Alert Rule aur Alertmanager
**[VISUAL: A PrometheusRule YAML with `expr`, `for`, `labels: severity: page`, `annotations: summary, runbook_url`. A flow: Prometheus evaluates the rule → Pending → Firing → Alertmanager groups, deduplicates, routes to chat, email or an on-call tool. A silence and an inhibition rule are shown.]**

**(Voiceover):**
Prometheus rule mein ek expression hoti hai, jaise "5xx ratio 5 percent se upar", ek `for: 5m`, labels aur annotations. Condition sahi hote hi alert Pending hota hai, aur `for` ke baad Firing, aur wo Alertmanager ke paas jaata hai. Alarm desk teen kaam karta hai. Group: sau pods ke sau alerts ek message mein. Route: label ke hisaab se sahi jagah, jaise `severity: page` on-call tool ko, aur `ticket` chat channel ko. Inhibit: jab poori building gir gayi ho, to us par chalne wale pods ke alerts band. Aur silence: maintenance ke dauran ek tay samay ke liye band. Ek alert jo na kisi ko jagata hai na kuch kehta hai, use delete kar do.

### [06:35 – 09:10] Scene 4: Dead Man's Switch aur SLO Burn
**[VISUAL: A "watchdog" alert that always fires. If the alarm desk stops receiving it, a separate service shouts. Next: an error-budget burn chart, a fast burn over one hour and a slow burn over six hours, each with its own severity.]**

**(Voiceover):**
Ek chhupa sawaal: agar alarm desk hi gir jaaye, to kaun batayega? Isliye ek watchdog alert hota hai jo hamesha fire karta hai, aur jab wo aana band ho jaaye to ek bahar ka service shor machata hai. Kit mein ye pehle se hota hai. Aur ek behtar tareeka SLO par alert: burn rate. Maan lo error budget tees din ka hai. Agar pichhle ek ghante mein budget bahut tez jal raha hai, to ye page hai. Agar dheere, par chhe ghante se lagataar, to ye ticket. Isse chhoti spike par raat ko nahi jaagna padta, par lambi dheemi dikkat bhi nahi chhootti. Ye Session 15 ke "kitni readings ke liye" wale alarm ka samajhdar roop hai.

### [09:10 – 11:30] Scene 5: Lab: Alert Jalao
**[VISUAL: A PrometheusRule `RoomsHighErrorRate` with `for: 2m` and `severity: page`. `rooms-service` is switched to a build that returns 500. In Prometheus the alert moves Pending → Firing, and appears in the Alertmanager UI. A runbook page is linked in the annotation.]**

**(Voiceover):**
Lab. Ek PrometheusRule likho, label `release: monitoring` ke saath. Lab cluster par `kind` mein control-plane ke kuch default alerts, jaise `etcdInsufficientMembers` ya `TargetDown`, bhi bajte hain, kyunki wo components bahar se scrape nahi hote. Ye shor hai, asli problem nahi, aur ye hi Session ke shuru wali alert-noise ki baat hai. Apna alert `Watchdog` ke saath Alertmanager mein dikhna chahiye:
```yaml
expr: sum(rate(http_requests_total{job="rooms",status=~"5.."}[5m])) / sum(rate(http_requests_total{job="rooms"}[5m])) > 0.05
for: 2m
labels: { severity: page }
annotations: { summary: "rooms errors above 5%", runbook_url: "RUNBOOK-LINK" }
```
`rooms-service` ko jaan boojh kar tod do, jaise ek `/` route jo 500 de, aur `curl` ke loop se traffic do. Prometheus ke Alerts page par alert Pending se Firing hota dekho, aur Alertmanager UI mein bhi. Phir ek chhota runbook likho: pehla kya dekhna hai, kaise rollback karna hai, Session 24 ke `rollout undo` ke saath. Aakhir mein Alertmanager mein ek silence lagao aur dekho ki alert chup ho gaya.

### [11:30 – 14:10] Scene 6: Raat ke Baad: Seekh, Dosh nahi
**[VISUAL: A timeline of an incident: alert fired, acknowledged, mitigated by rollback, resolved. A short review page with headings: what guests saw, what we did, why it happened, what we change. A banner: "blameless".]**

**(Voiceover):**
Alert ne jagaya, duty manager ne rollback kiya, aur site wapas. Kaam khatam? Nahi. Agle din ek chhoti review likho. Guests ne kya dekha, kab se kab tak. Humne kya kiya. Kyun hua. Aur hum kya badlenge: ek alert, ek test, ek runbook ka hissa. Review mein koi naam nahi liya jaata, kyunki sawal "kisne galti ki" nahi, "system ne ye galti hone kyun di" hai. Isse error budget bhi samajh aata hai, aur wahi budget agle release ka faisla bhi karta hai. Aur ek aadat: har incident ke baad ek alert ya dashboard mein ek sudhaar, taaki wahi raat dobara na aaye. Monitoring tab tak poori nahi hoti jab tak wo har raat ke baad thodi behtar na ho.

### [14:10 – 15:30] Scene 7: Recap aur Bridge
**[VISUAL: A card: "alert on symptoms · actionable · for: · severity routing · runbook link · watchdog · burn-rate alerts". Then a blank master plan on a drawing table appears over the campus map.]**

**(Voiceover):**
Recap: control room ka poora chakra: dekho, naapo, alert karo. Ab ek aur kaam: ab tak Atithi ki buildings, wings aur campus haath se, console mein click karke bane. Wahi problem, jo is poore course ki shuruaat mein thi: "staging production jaisa kyun nahi?" Agle session mein campus ka master plan document likhenge, aur ek contractor use bana dega: Terraform.

---

# 📎 Student handout: Session 26 cheat sheet
*Not spoken. Shown on screen at the end, or given as a download.*

| Cheez | Yaad rakho |
|---|---|
| Teen pillars | Metrics = kya, logs = kyun, traces = kahan |
| Golden signals | Latency, traffic, errors, saturation; RED services ke liye, USE resources ke liye |
| SLI / SLO / budget | Naap / target / chhoot; budget release ki raftaar tay karta hai |
| 99.9% | Tees din mein lagbhag 43 minute ki chhoot |
| Pull model | Inspector `/metrics` par jaata hai; jawab nahi to `up = 0` |
| Exporter | Jo khud numbers nahi deta (node exporter) |
| Metric types | Counter (badhta), gauge (upar neeche), histogram (buckets) |
| Labels | Dimension dete hain; unbounded values nahi (cardinality) |
| PromQL | `rate()` counter par; `sum by`; `histogram_quantile(0.95, ...)` |
| Instrument | `prometheus_client`, `/metrics`, label route template se |
| kube-prometheus-stack | Operator, ServiceMonitor, PrometheusRule, Grafana, exporters |
| ServiceMonitor jaal | Chart ka label (`release: ...`); Service ke labels aur port ka naam |
| Grafana | Variables, signals upar detail neeche, dashboards as code |
| Alert niyam | Symptom, actionable, severity, `for:`, runbook |
| Alertmanager | Group, route, inhibit, silence; watchdog |
| Burn rate | Tez jalna = page; dheere jalna = ticket |
| Safai | `helm uninstall`, PVCs, port-forward band |
